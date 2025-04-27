import tkinter as tk
from tkinter import messagebox
import sqlite3
import subprocess
import os

def verify_login(username, password):
    conn = sqlite3.connect("poultry.db")
    cursor = conn.cursor()

    cursor.execute("SELECT role FROM users WHERE email=? AND password=?", (username, password))
    user = cursor.fetchone()
    conn.close()
    
    return user[0] if user else None

def handle_login(event=None):
    username = username_entry.get()
    password = password_entry.get()

    if username.strip() == "Enter your email" or password.strip() == "Enter your password":
        messagebox.showwarning("Login Failed", "Please enter your credentials.")
        return

    role = verify_login(username, password)
    
    if role:
        messagebox.showinfo("Login Success", f"Welcome, {role}!")
        root.destroy()
        
        # Launch appropriate dashboard based on role
        if role.lower() == "admin":
            subprocess.run(["python", "admin_main.py"])
        elif role.lower() == "manager":
            subprocess.run(["python", "hr_manager.py"])
        else:
            subprocess.run(["python", "user_main.py"])
    else:
        messagebox.showerror("Login Failed", "Invalid username or password.")

def add_placeholder(entry, placeholder, is_password=False):
    def on_focus_in(event):
        if entry.get() == placeholder:
            entry.delete(0, tk.END)
            entry.config(fg="black", show="*" if is_password else "")

    def on_focus_out(event):
        if not entry.get():
            entry.insert(0, placeholder)
            entry.config(fg="grey", show="" if is_password else "")

    entry.insert(0, placeholder)
    entry.config(fg="grey")
    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)

# Create login window
root = tk.Tk()
root.title("Login - Poultry Management System")
root.state('zoomed')  # Maximize window without fullscreen
root.config(bg="#DFF6FF")  

# Create a main container frame that will center our content
main_container = tk.Frame(root, bg="#DFF6FF")
main_container.pack(expand=True, fill="both")

# Header
title_label = tk.Label(main_container, text="LOGIN", 
                      font=("Helvetica", 26, "bold"), fg="#004AAD", bg="#DFF6FF")
title_label.pack(pady=40)

# Frame for login form (fixed size)
form_frame = tk.Frame(main_container, bg="white", padx=40, pady=60, 
                     relief="ridge", bd=3, width=500, height=400)
form_frame.pack_propagate(False)  # Prevent frame from resizing to widgets
form_frame.pack()

# Username field
username_entry = tk.Entry(form_frame, font=("Helvetica", 18), width=25, bd=3, relief="solid")
username_entry.pack(pady=20, ipady=12)
add_placeholder(username_entry, "Enter your email")

# Password field
password_entry = tk.Entry(form_frame, font=("Helvetica", 18), width=25, bd=3, relief="solid")
password_entry.pack(pady=20, ipady=12)
add_placeholder(password_entry, "Enter your password", is_password=True)

# Login button
login_button = tk.Button(main_container, text="Login", font=("Helvetica", 20), 
                       command=handle_login, bg="#28A745", fg="white", 
                       width=20, height=2, bd=4, relief="raised")
login_button.pack(pady=30)

# Footer
footer_label = tk.Label(main_container, text="© 2025 Poultry Management System", 
                       font=("Helvetica", 14), fg="#004AAD", bg="#DFF6FF")
footer_label.pack(pady=20)

root.bind("<Return>", handle_login)

root.mainloop()