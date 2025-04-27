import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import sqlite3
from datetime import datetime
from tkinter import scrolledtext
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
matplotlib.use('TkAgg')
import numpy as np

class PoultryManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Dashboard")
        self.root.state("zoomed")
        self.root.config(bg="#F4F4F9")
        
        # Database connection
        self.conn = sqlite3.connect("poultry.db")
        self.cursor = self.conn.cursor()
        
        # Cart for ordering system
        self.cart = []
        self.current_order_id = None
        
        # Create UI
        self.create_sidebar()
        self.create_content_area()
        
        # Initialize frames (only those in sidebar)
        self.create_products_frame()
        self.create_users_frame()
        self.create_feeds_frame()
        self.create_sales_frame()
        
        # Load initial data
        self.load_data()
        
        # Show products by default
        self.show_frame(self.products_frame)
    
    def create_sidebar(self):
        self.sidebar = tk.Frame(self.root, bg="#4CAF50", width=250)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)
        
        title_label = tk.Label(self.sidebar, text="Poultry Management", 
                             font=("Helvetica", 16, "bold"), bg="#4CAF50", fg="white")
        title_label.pack(pady=40)
        
        buttons = [
            ("Products", lambda: self.show_frame(self.products_frame)),
            ("Feeds", lambda: self.show_frame(self.feeds_frame)),
            ("Sales", lambda: self.show_frame(self.sales_frame)),
            ("Users", lambda: self.show_frame(self.users_frame)),
            ("Log Out", self.logout)
        ]
        
        for text, command in buttons:
            btn = tk.Button(self.sidebar, text=text, font=("Helvetica", 12), 
                          bg="#3E8E41", fg="white", height=2, width=20, 
                          command=command, anchor="w")
            btn.pack(fill="x", padx=10, pady=5)
    
    def create_content_area(self):
        self.content_area = tk.Frame(self.root, bg="#E0F7FA")
        self.content_area.pack(side="right", fill="both", expand=True)
    
    def show_frame(self, frame):
        # Only show frames that are in the sidebar
        for f in [self.products_frame, self.users_frame, self.feeds_frame, self.sales_frame]:
            f.pack_forget()
        frame.pack(fill="both", expand=True)

    def create_products_frame(self):
        self.products_frame = tk.Frame(self.content_area, bg="#E0F7FA")
        
        title = tk.Label(self.products_frame, text="Product Management", 
                        font=("Helvetica", 24, "bold"), bg="#E0F7FA")
        title.pack(pady=20)
        
        # Product table
        self.product_table = ttk.Treeview(self.products_frame, 
                                        columns=("ID", "Name", "Category", "Stock", "Price"), 
                                        show="headings", height=15)
        
        self.product_table.heading("ID", text="ID")
        self.product_table.heading("Name", text="Name")
        self.product_table.heading("Category", text="Category")
        self.product_table.heading("Stock", text="Stock")
        self.product_table.heading("Price", text="Price")
        
        self.product_table.column("ID", width=50, anchor="center")
        self.product_table.column("Name", width=150, anchor="center")
        self.product_table.column("Category", width=100, anchor="center")
        self.product_table.column("Stock", width=80, anchor="center")
        self.product_table.column("Price", width=100, anchor="center")
        
        self.product_table.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Action buttons
        button_frame = tk.Frame(self.products_frame, bg="#E0F7FA")
        button_frame.pack(pady=10)
        
        add_button = tk.Button(button_frame, text="Add Product", 
                             command=lambda: self.add_edit_product())
        add_button.pack(side="left", padx=5)
        
        edit_button = tk.Button(button_frame, text="Edit Product", 
                              command=lambda: self.add_edit_product(edit=True))
        edit_button.pack(side="left", padx=5)
        
        delete_button = tk.Button(button_frame, text="Delete Product", 
                                command=self.delete_product)
        delete_button.pack(side="left", padx=5)
        
        refresh_button = tk.Button(button_frame, text="Refresh", 
                                 command=self.load_data)
        refresh_button.pack(side="left", padx=5)

    def create_users_frame(self):
        self.users_frame = tk.Frame(self.content_area, bg="#E0F7FA")
        
        title = tk.Label(self.users_frame, text="User Management", 
                        font=("Helvetica", 24, "bold"), bg="#E0F7FA")
        title.pack(pady=20)
        
        # User table
        self.user_table = ttk.Treeview(self.users_frame, 
                                     columns=("ID", "Name", "Role", "Email"), 
                                     show="headings", height=15)
        
        self.user_table.heading("ID", text="ID")
        self.user_table.heading("Name", text="Name")
        self.user_table.heading("Role", text="Role")
        self.user_table.heading("Email", text="Email")
        
        self.user_table.column("ID", width=50, anchor="center")
        self.user_table.column("Name", width=150, anchor="center")
        self.user_table.column("Role", width=100, anchor="center")
        self.user_table.column("Email", width=200, anchor="center")
        
        self.user_table.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Action buttons
        button_frame = tk.Frame(self.users_frame, bg="#E0F7FA")
        button_frame.pack(pady=10)
        
        add_button = tk.Button(button_frame, text="Add User", 
                             command=lambda: self.add_edit_user())
        add_button.pack(side="left", padx=5)
        
        edit_button = tk.Button(button_frame, text="Edit User", 
                              command=lambda: self.add_edit_user(edit=True))
        edit_button.pack(side="left", padx=5)
        
        delete_button = tk.Button(button_frame, text="Delete User", 
                                command=self.delete_user)
        delete_button.pack(side="left", padx=5)
        
        refresh_button = tk.Button(button_frame, text="Refresh", 
                                 command=self.load_data)
        refresh_button.pack(side="left", padx=5)

    def create_feeds_frame(self):
        self.feeds_frame = tk.Frame(self.content_area, bg="#E0F7FA")
        
        title = tk.Label(self.feeds_frame, text="Feeds Management", 
                        font=("Helvetica", 24, "bold"), bg="#E0F7FA")
        title.pack(pady=20)
        
        # Feeds table
        self.feeds_table = ttk.Treeview(self.feeds_frame, 
                                      columns=("ID", "Name", "Category", "Level"), 
                                      show="headings", height=15)
        
        self.feeds_table.heading("ID", text="ID")
        self.feeds_table.heading("Name", text="Name")
        self.feeds_table.heading("Category", text="Category")
        self.feeds_table.heading("Level", text="Level")
        
        self.feeds_table.column("ID", width=50, anchor="center")
        self.feeds_table.column("Name", width=150, anchor="center")
        self.feeds_table.column("Category", width=100, anchor="center")
        self.feeds_table.column("Level", width=80, anchor="center")
        
        self.feeds_table.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Action buttons
        button_frame = tk.Frame(self.feeds_frame, bg="#E0F7FA")
        button_frame.pack(pady=10)
        
        add_button = tk.Button(button_frame, text="Add Feed", 
                             command=lambda: self.add_edit_feed())
        add_button.pack(side="left", padx=5)
        
        edit_button = tk.Button(button_frame, text="Edit Feed", 
                              command=lambda: self.add_edit_feed(edit=True))
        edit_button.pack(side="left", padx=5)
        
        delete_button = tk.Button(button_frame, text="Delete Feed", 
                                command=self.delete_feed)
        delete_button.pack(side="left", padx=5)
        
        refresh_button = tk.Button(button_frame, text="Refresh", 
                                 command=self.load_data)
        refresh_button.pack(side="left", padx=5)

    def create_sales_frame(self):
        self.sales_frame = tk.Frame(self.content_area, bg="#E0F7FA")
        
        title = tk.Label(self.sales_frame, text="Sales Management", 
                        font=("Helvetica", 24, "bold"), bg="#E0F7FA")
        title.pack(pady=20)
        
        # Sales table
        self.sales_table = ttk.Treeview(self.sales_frame, 
                                      columns=("ID", "Date", "Customer", "Total"), 
                                      show="headings", height=15)
        
        self.sales_table.heading("ID", text="Order ID")
        self.sales_table.heading("Date", text="Date")
        self.sales_table.heading("Customer", text="Customer")
        self.sales_table.heading("Total", text="Total")
        
        self.sales_table.column("ID", width=80, anchor="center")
        self.sales_table.column("Date", width=150, anchor="center")
        self.sales_table.column("Customer", width=150, anchor="center")
        self.sales_table.column("Total", width=100, anchor="center")
        
        self.sales_table.pack(fill="both", expand=True, padx=20, pady=10)
        
        # View details button
        button_frame = tk.Frame(self.sales_frame, bg="#E0F7FA")
        button_frame.pack(pady=10)
        
        details_button = tk.Button(button_frame, text="View Details", 
                                 command=self.view_sale_details)
        details_button.pack(side="left", padx=5)
        
        refresh_button = tk.Button(button_frame, text="Refresh", 
                                 command=self.load_data)
        refresh_button.pack(side="left", padx=5)

    def add_edit_product(self, edit=False):
        if edit:
            selected = self.product_table.selection()
            if not selected:
                messagebox.showwarning("Warning", "Please select a product to edit")
                return
            
            product_id = self.product_table.item(selected[0])['values'][0]
            self.cursor.execute("SELECT * FROM products WHERE id=?", (product_id,))
            product = self.cursor.fetchone()
            
            if not product:
                messagebox.showerror("Error", "Product not found")
                return
        else:
            product = None
        
        # Create dialog window
        dialog = tk.Toplevel(self.root)
        dialog.title("Edit Product" if edit else "Add Product")
        dialog.grab_set()
        
        # Form fields
        tk.Label(dialog, text="Name:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        name_entry = tk.Entry(dialog, width=30)
        name_entry.grid(row=0, column=1, padx=10, pady=5)
        
        tk.Label(dialog, text="Category:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        category_entry = tk.Entry(dialog, width=30)
        category_entry.grid(row=1, column=1, padx=10, pady=5)
        
        tk.Label(dialog, text="Stock:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        stock_entry = tk.Entry(dialog, width=30)
        stock_entry.grid(row=2, column=1, padx=10, pady=5)
        
        tk.Label(dialog, text="Price:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
        price_entry = tk.Entry(dialog, width=30)
        price_entry.grid(row=3, column=1, padx=10, pady=5)
        
        # Fill fields if editing
        if product:
            name_entry.insert(0, product[1])
            category_entry.insert(0, product[2])
            stock_entry.insert(0, product[3])
            price_entry.insert(0, product[4])
        
        # Save button
        def save_product():
            name = name_entry.get().strip()
            category = category_entry.get().strip()
            
            try:
                stock = int(stock_entry.get())
                price = float(price_entry.get())
                
                if stock < 0 or price < 0:
                    raise ValueError("Values must be positive")
            except ValueError:
                messagebox.showerror("Error", "Invalid stock or price value")
                return
            
            if not name or not category:
                messagebox.showerror("Error", "Name and category are required")
                return
            
            try:
                if edit:
                    self.cursor.execute(
                        "UPDATE products SET name=?, category=?, stock=?, price=? WHERE id=?",
                        (name, category, stock, price, product_id)
                    )
                else:
                    self.cursor.execute(
                        "INSERT INTO products (name, category, stock, price) VALUES (?, ?, ?, ?)",
                        (name, category, stock, price)
                    )
                
                self.conn.commit()
                self.load_data()
                dialog.destroy()
                messagebox.showinfo("Success", "Product saved successfully")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save product: {str(e)}")
        
        save_button = tk.Button(dialog, text="Save", command=save_product)
        save_button.grid(row=4, columnspan=2, pady=10)

    def delete_product(self):
        selected = self.product_table.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a product to delete")
            return
        
        product_id = self.product_table.item(selected[0])['values'][0]
        
        if messagebox.askyesno("Confirm", "Delete this product?"):
            try:
                self.cursor.execute("DELETE FROM products WHERE id=?", (product_id,))
                self.conn.commit()
                self.load_data()
                messagebox.showinfo("Success", "Product deleted successfully")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete product: {str(e)}")

    def add_edit_user(self, edit=False):
        if edit:
            selected = self.user_table.selection()
            if not selected:
                messagebox.showwarning("Warning", "Please select a user to edit")
                return
            
            user_id = self.user_table.item(selected[0])['values'][0]
            self.cursor.execute("SELECT * FROM users WHERE id=?", (user_id,))
            user = self.cursor.fetchone()
            
            if not user:
                messagebox.showerror("Error", "User not found")
                return
        else:
            user = None
        
        # Create dialog window
        dialog = tk.Toplevel(self.root)
        dialog.title("Edit User" if edit else "Add User")
        dialog.grab_set()
        
        # Form fields
        tk.Label(dialog, text="Name:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        name_entry = tk.Entry(dialog, width=30)
        name_entry.grid(row=0, column=1, padx=10, pady=5)
        
        tk.Label(dialog, text="Role:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        role_combobox = ttk.Combobox(dialog, values=["Admin", "Manager", "Staff"], width=27)
        role_combobox.grid(row=1, column=1, padx=10, pady=5)
        
        tk.Label(dialog, text="Email:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        email_entry = tk.Entry(dialog, width=30)
        email_entry.grid(row=2, column=1, padx=10, pady=5)
        
        tk.Label(dialog, text="Password:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
        password_entry = tk.Entry(dialog, width=30, show="*")
        password_entry.grid(row=3, column=1, padx=10, pady=5)
        
        # Fill fields if editing
        if user:
            name_entry.insert(0, user[1])
            role_combobox.set(user[2])
            email_entry.insert(0, user[3])
        
        # Save button
        def save_user():
            name = name_entry.get().strip()
            role = role_combobox.get().strip()
            email = email_entry.get().strip()
            password = password_entry.get().strip()
            
            if not name or not role or not email:
                messagebox.showerror("Error", "Name, role and email are required")
                return
            
            if not edit and not password:
                messagebox.showerror("Error", "Password is required for new users")
                return
            
            try:
                if edit:
                    if password:
                        self.cursor.execute(
                            "UPDATE users SET name=?, role=?, email=?, password=? WHERE id=?",
                            (name, role, email, password, user_id)
                        )
                    else:
                        self.cursor.execute(
                            "UPDATE users SET name=?, role=?, email=? WHERE id=?",
                            (name, role, email, user_id)
                        )
                else:
                    self.cursor.execute(
                        "INSERT INTO users (name, role, email, password) VALUES (?, ?, ?, ?)",
                        (name, role, email, password)
                    )
                
                self.conn.commit()
                self.load_data()
                dialog.destroy()
                messagebox.showinfo("Success", "User saved successfully")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save user: {str(e)}")
        
        save_button = tk.Button(dialog, text="Save", command=save_user)
        save_button.grid(row=4, columnspan=2, pady=10)

    def delete_user(self):
        selected = self.user_table.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a user to delete")
            return
        
        user_id = self.user_table.item(selected[0])['values'][0]
        
        if messagebox.askyesno("Confirm", "Delete this user?"):
            try:
                self.cursor.execute("DELETE FROM users WHERE id=?", (user_id,))
                self.conn.commit()
                self.load_data()
                messagebox.showinfo("Success", "User deleted successfully")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete user: {str(e)}")

    def add_edit_feed(self, edit=False):
        if edit:
            selected = self.feeds_table.selection()
            if not selected:
                messagebox.showwarning("Warning", "Please select a feed to edit")
                return
            
            feed_id = self.feeds_table.item(selected[0])['values'][0]
            self.cursor.execute("SELECT * FROM feeds WHERE id=?", (feed_id,))
            feed = self.cursor.fetchone()
            
            if not feed:
                messagebox.showerror("Error", "Feed not found")
                return
        else:
            feed = None
        
        # Create dialog window
        dialog = tk.Toplevel(self.root)
        dialog.title("Edit Feed" if edit else "Add Feed")
        dialog.grab_set()
        
        # Form fields
        tk.Label(dialog, text="Name:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        name_entry = tk.Entry(dialog, width=30)
        name_entry.grid(row=0, column=1, padx=10, pady=5)
        
        tk.Label(dialog, text="Category:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        category_entry = tk.Entry(dialog, width=30)
        category_entry.grid(row=1, column=1, padx=10, pady=5)
        
        tk.Label(dialog, text="Level:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        level_entry = tk.Entry(dialog, width=30)
        level_entry.grid(row=2, column=1, padx=10, pady=5)
        
        # Fill fields if editing
        if feed:
            name_entry.insert(0, feed[1])
            category_entry.insert(0, feed[2])
            level_entry.insert(0, feed[3])
        
        # Save button
        def save_feed():
            name = name_entry.get().strip()
            category = category_entry.get().strip()
            
            try:
                level = int(level_entry.get())
                if level < 0:
                    raise ValueError("Level must be positive")
            except ValueError:
                messagebox.showerror("Error", "Invalid level value")
                return
            
            if not name or not category:
                messagebox.showerror("Error", "Name and category are required")
                return
            
            try:
                if edit:
                    self.cursor.execute(
                        "UPDATE feeds SET name=?, category=?, level=? WHERE id=?",
                        (name, category, level, feed_id)
                    )
                else:
                    self.cursor.execute(
                        "INSERT INTO feeds (name, category, level) VALUES (?, ?, ?)",
                        (name, category, level)
                    )
                
                self.conn.commit()
                self.load_data()
                dialog.destroy()
                messagebox.showinfo("Success", "Feed saved successfully")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save feed: {str(e)}")
        
        save_button = tk.Button(dialog, text="Save", command=save_feed)
        save_button.grid(row=3, columnspan=2, pady=10)

    def delete_feed(self):
        selected = self.feeds_table.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a feed to delete")
            return
        
        feed_id = self.feeds_table.item(selected[0])['values'][0]
        
        if messagebox.askyesno("Confirm", "Delete this feed?"):
            try:
                self.cursor.execute("DELETE FROM feeds WHERE id=?", (feed_id,))
                self.conn.commit()
                self.load_data()
                messagebox.showinfo("Success", "Feed deleted successfully")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete feed: {str(e)}")

    def view_sale_details(self):
        selected = self.sales_table.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a sale to view")
            return
        
        order_id = self.sales_table.item(selected[0])['values'][0]
        
        # Get order details
        self.cursor.execute("SELECT * FROM orders WHERE id=?", (order_id,))
        order = self.cursor.fetchone()
        
        if not order:
            messagebox.showerror("Error", "Order not found")
            return
        
        # Get order items
        self.cursor.execute('''
            SELECT p.name, oi.quantity, oi.price, (oi.quantity * oi.price) as total
            FROM order_items oi
            JOIN products p ON oi.product_id = p.id
            WHERE oi.order_id = ?
        ''', (order_id,))
        items = self.cursor.fetchall()
        
        # Create details window
        details_window = tk.Toplevel(self.root)
        details_window.title(f"Order Details - #{order_id}")
        details_window.geometry("600x400")
        
        # Order info
        info_frame = tk.Frame(details_window)
        info_frame.pack(fill="x", padx=20, pady=10)
        
        tk.Label(info_frame, text=f"Order ID: {order[0]}", font=("Helvetica", 12)).pack(anchor="w")
        tk.Label(info_frame, text=f"Date: {order[2]}").pack(anchor="w")
        tk.Label(info_frame, text=f"Customer: {order[1]}").pack(anchor="w")
        
        # Items table
        tree_frame = tk.Frame(details_window)
        tree_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        tree = ttk.Treeview(tree_frame, columns=("Product", "Qty", "Price", "Total"), 
                           show="headings", height=10)
        
        tree.heading("Product", text="Product")
        tree.heading("Qty", text="Qty")
        tree.heading("Price", text="Price")
        tree.heading("Total", text="Total")
        
        tree.column("Product", width=200)
        tree.column("Qty", width=80, anchor="center")
        tree.column("Price", width=100, anchor="center")
        tree.column("Total", width=120, anchor="center")
        
        for item in items:
            tree.insert("", "end", values=item)
        
        tree.pack(fill="both", expand=True)
        
        # Totals
        totals_frame = tk.Frame(details_window)
        totals_frame.pack(fill="x", padx=20, pady=10)
        
        tk.Label(totals_frame, text=f"Subtotal: ₱{order[3]:.2f}", anchor="center").pack(fill="x")
        tk.Label(totals_frame, text=f"Tax: ₱{order[4]:.2f}", anchor="center").pack(fill="x")
        tk.Label(totals_frame, text=f"Total: ₱{order[5]:.2f}", font=("Helvetica", 12, "bold"), 
                anchor="center").pack(fill="x")

    def load_data(self):
        # Clear all tables
        for table in [self.product_table, self.user_table, self.feeds_table, self.sales_table]:
            for item in table.get_children():
                table.delete(item)
        
        try:
            # Load products
            self.cursor.execute("SELECT * FROM products")
            products = self.cursor.fetchall()
            for product in products:
                self.product_table.insert("", "end", values=product)
            
            # Load users
            self.cursor.execute("SELECT id, name, role, email FROM users")
            users = self.cursor.fetchall()
            for user in users:
                self.user_table.insert("", "end", values=user)
            
            # Load feeds
            self.cursor.execute("SELECT * FROM feeds")
            feeds = self.cursor.fetchall()
            for feed in feeds:
                self.feeds_table.insert("", "end", values=feed)
            
            # Load sales
            self.cursor.execute("SELECT id, order_date, customer_name, total FROM orders ORDER BY order_date DESC")
            sales = self.cursor.fetchall()
            for sale in sales:
                self.sales_table.insert("", "end", values=sale)
            
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    def logout(self):
        if messagebox.askyesno("Logout", "Are you sure you want to log out?"):
            self.conn.close()
            self.root.destroy()
            import subprocess
            subprocess.run(["python", "login.py"])

if __name__ == "__main__":
    # Create database tables if they don't exist
    conn = sqlite3.connect("poultry.db")
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            category TEXT,
            stock INTEGER,
            price REAL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            role TEXT,
            email TEXT,
            password TEXT NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS feeds (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            category TEXT,
            level INTEGER
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT,
            order_date TEXT,
            subtotal REAL,
            tax REAL,
            total REAL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER,
            product_id INTEGER,
            quantity INTEGER,
            price REAL,
            FOREIGN KEY(order_id) REFERENCES orders(id),
            FOREIGN KEY(product_id) REFERENCES products(id)
        )
    ''')
    
    # Add admin user if not exists
    cursor.execute("SELECT COUNT(*) FROM users WHERE role='Admin'")
    if cursor.fetchone()[0] == 0:
        cursor.execute(
            "INSERT INTO users (name, role, email, password) VALUES (?, ?, ?, ?)",
            ("Admin User", "Admin", "admin@example.com", "admin123")
        )
    
    conn.commit()
    conn.close()
    
    # Run the application
    root = tk.Tk()
    app = PoultryManagementSystem(root)
    root.mainloop()