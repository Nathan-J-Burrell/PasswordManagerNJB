import sqlite3
import tkinter as tk
from tkinter import messagebox

# Database setup
def setup_db():
    conn = sqlite3.connect('passwords.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS passwords (
        id INTEGER PRIMARY KEY,
        website TEXT,
        username TEXT,
        password TEXT
    )
    ''')
    conn.commit()
    conn.close()

# Add password
def add_password(website, username, password):
    if not website or not username or not password:
        messagebox.showerror("Error", "All fields must be filled!")
        return
    try:
        conn = sqlite3.connect('passwords.db')
        cursor = conn.cursor()
        cursor.execute('''
        INSERT INTO passwords (website, username, password)
        VALUES (?, ?, ?)
        ''', (website, username, password))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Password added successfully!")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Amend password
def amend_password(id, new_password):
    if not id or not new_password:
        messagebox.showerror("Error", "All fields must be filled!")
        return
    try:
        conn = sqlite3.connect('passwords.db')
        cursor = conn.cursor()
        cursor.execute('''
        UPDATE passwords
        SET password = ?
        WHERE id = ?
        ''', (new_password, id))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Password amended successfully!")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Delete password
def delete_password(id):
    if not id:
        messagebox.showerror("Error", "ID must be provided!")
        return
    try:
        conn = sqlite3.connect('passwords.db')
        cursor = conn.cursor()
        cursor.execute('''
        DELETE FROM passwords
        WHERE id = ?
        ''', (id,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Password deleted successfully!")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Display passwords
def display_passwords():
    try:
        conn = sqlite3.connect('passwords.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM passwords')
        rows = cursor.fetchall()
        conn.close()
        return rows
    except Exception as e:
        messagebox.showerror("Error", str(e))
        return []

# Search passwords
def search_passwords(query):
    try:
        conn = sqlite3.connect('passwords.db')
        cursor = conn.cursor()
        cursor.execute('''
        SELECT * FROM passwords
        WHERE website LIKE ? OR username LIKE ?
        ''', ('%' + query + '%', '%' + query + '%'))
        rows = cursor.fetchall()
        conn.close()
        return rows
    except Exception as e:
        messagebox.showerror("Error", str(e))
        return []

# GUI setup
def setup_gui():
    root = tk.Tk()
    root.title("Password Manager")
    root.geometry("300x500")
    root.configure(bg="#f0f0f0")

    container = tk.Frame(root, bg="#ffffff", padx=20, pady=20)
    container.pack(pady=20)

    tk.Label(container, text="Password Manager", bg="#ffffff", fg="#4cafaa", font=("Roboto Mono", 16)).pack(pady=10)

    # Add password
    tk.Label(container, text="Website", bg="#ffffff").pack(anchor="w")
    website_entry = tk.Entry(container)
    website_entry.pack(fill="x")

    tk.Label(container, text="Username", bg="#ffffff").pack(anchor="w")
    username_entry = tk.Entry(container)
    username_entry.pack(fill="x")

    tk.Label(container, text="Password", bg="#ffffff").pack(anchor="w")
    password_entry = tk.Entry(container, show="*")
    password_entry.pack(fill="x")

    def toggle_password():
        if password_entry.cget('show') == '*':
            password_entry.config(show='')
            show_button.config(text='Hide')
        else:
            password_entry.config(show='*')
            show_button.config(text='Show')

    show_button = tk.Button(container, text="Show", command=toggle_password, bg="#4cafaa", fg="#fff")
    show_button.pack(fill="x", pady=5)

    def add_password_gui():
        website = website_entry.get()
        username = username_entry.get()
        password = password_entry.get()
        add_password(website, username, password)

    tk.Button(container, text="Add Password", command=add_password_gui, bg="#4cafaa", fg="#fff").pack(fill="x", pady=5)

    # Amend password
    tk.Label(container, text="ID to Amend", bg="#ffffff").pack(anchor="w")
    id_amend_entry = tk.Entry(container)
    id_amend_entry.pack(fill="x")

    tk.Label(container, text="New Password", bg="#ffffff").pack(anchor="w")
    new_password_entry = tk.Entry(container, show="*")
    new_password_entry.pack(fill="x")

    def amend_password_gui():
        id = id_amend_entry.get()
        new_password = new_password_entry.get()
        amend_password(id, new_password)

    tk.Button(container, text="Amend Password", command=amend_password_gui, bg="#4cafaa", fg="#fff").pack(fill="x", pady=5)

    # Delete password
    tk.Label(container, text="ID to Delete", bg="#ffffff").pack(anchor="w")
    id_delete_entry = tk.Entry(container)
    id_delete_entry.pack(fill="x")

    def delete_password_gui():
        id = id_delete_entry.get()
        delete_password(id)

    tk.Button(container, text="Delete Password", command=delete_password_gui, bg="#4cafaa", fg="#fff").pack(fill="x", pady=5)

    # Display passwords
    def display_passwords_gui():
        rows = display_passwords()
        display_window = tk.Toplevel(root)
        display_window.title("Stored Passwords")
        display_window.configure(bg="#f0f0f0")
        for i, row in enumerate(rows):
            tk.Label(display_window, text=f"ID: {row[0]}, Website: {row[1]}, Username: {row[2]}, Password: {row[3]}", bg="#f0f0f0").pack(anchor="w")

    tk.Button(container, text="Display Passwords", command=display_passwords_gui, bg="#4cafaa", fg="#fff").pack(fill="x", pady=5)

    # Search passwords
    tk.Label(container, text="Search", bg="#ffffff").pack(anchor="w")
    search_entry = tk.Entry(container)
    search_entry.pack(fill="x")

    def search_passwords_gui():
        query = search_entry.get()
        rows = search_passwords(query)
        search_window = tk.Toplevel(root)
        search_window.title("Search Results")
        search_window.configure(bg="#f0f0f0")
        for i, row in enumerate(rows):
            tk.Label(search_window, text=f"ID: {row[0]}, Website: {row[1]}, Username: {row[2]}, Password: {row[3]}", bg="#f0f0f0").pack(anchor="w")

    tk.Button(container, text="Search", command=search_passwords_gui, bg="#4cafaa", fg="#fff").pack(fill="x", pady=5)

    root.mainloop()

if __name__ == "__main__":
    setup_db()
    setup_gui()