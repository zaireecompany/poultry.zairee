import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import sqlite3
from datetime import datetime
from tkinter import scrolledtext
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
matplotlib.use('TkAgg')

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
        
        # Initialize only the frames that are in the sidebar
        self.create_order_frame()
        self.create_products_frame()
        self.create_feeds_frame()
        
        # Load initial data
        self.load_data()
        
        # Show order by default
        self.show_frame(self.order_frame)
    
    def create_sidebar(self):
        self.sidebar = tk.Frame(self.root, bg="#4CAF50", width=250)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)
        
        title_label = tk.Label(self.sidebar, text="Poultry Management", 
                             font=("Helvetica", 16, "bold"), bg="#4CAF50", fg="white")
        title_label.pack(pady=40)
        
        buttons = [
            ("Order Management", lambda: self.show_frame(self.order_frame)),
            ("Products", lambda: self.show_frame(self.products_frame)),
            ("Feeds", lambda: self.show_frame(self.feeds_frame)),
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
        for f in [self.order_frame, self.products_frame, self.feeds_frame]:
            f.pack_forget()
        frame.pack(fill="both", expand=True)
    
    def create_order_frame(self):
        self.order_frame = tk.Frame(self.content_area, bg="#E0F7FA")
        
        # Order management widgets
        order_top_frame = tk.Frame(self.order_frame, bg="#E0F7FA")
        order_top_frame.pack(fill="x", pady=10)
        
        # Product selection
        product_select_frame = tk.Frame(order_top_frame, bg="#E0F7FA")
        product_select_frame.pack(side="left", padx=20)
        
        tk.Label(product_select_frame, text="Select Product:", 
                font=("Helvetica", 12), bg="#E0F7FA").pack(anchor="w")
        
        self.product_combobox = ttk.Combobox(product_select_frame, font=("Helvetica", 12))
        self.product_combobox.pack(fill="x", pady=5)
        self.product_combobox.bind("<<ComboboxSelected>>", self.update_product_details)
        
        # Product details
        details_frame = tk.Frame(product_select_frame, bg="#E0F7FA")
        details_frame.pack(fill="x", pady=10)
        
        tk.Label(details_frame, text="Price:", font=("Helvetica", 12), bg="#E0F7FA").grid(row=0, column=0, sticky="w")
        self.price_label = tk.Label(details_frame, text="₱0.00", font=("Helvetica", 12), bg="#E0F7FA")
        self.price_label.grid(row=0, column=1, sticky="w")
        
        tk.Label(details_frame, text="Stock:", font=("Helvetica", 12), bg="#E0F7FA").grid(row=1, column=0, sticky="w")
        self.stock_label = tk.Label(details_frame, text="0", font=("Helvetica", 12), bg="#E0F7FA")
        self.stock_label.grid(row=1, column=1, sticky="w")
        
        # Quantity selection
        qty_frame = tk.Frame(product_select_frame, bg="#E0F7FA")
        qty_frame.pack(fill="x", pady=10)
        
        tk.Label(qty_frame, text="Quantity:", font=("Helvetica", 12), bg="#E0F7FA").pack(side="left")
        self.qty_spinbox = tk.Spinbox(qty_frame, from_=1, to=100, width=5, font=("Helvetica", 12))
        self.qty_spinbox.pack(side="left", padx=10)
        
        add_button = tk.Button(product_select_frame, text="Add to Cart", 
                             font=("Helvetica", 12), bg="#4CAF50", fg="white",
                             command=self.add_to_cart)
        add_button.pack(pady=10)
        
        # Cart display
        cart_frame = tk.Frame(order_top_frame, bg="#E0F7FA")
        cart_frame.pack(side="right", padx=20, fill="both", expand=True)
        
        tk.Label(cart_frame, text="Shopping Cart", font=("Helvetica", 14, "bold"), 
                bg="#E0F7FA").pack(anchor="w")
        
        self.cart_tree = ttk.Treeview(cart_frame, columns=("Product", "Qty", "Price", "Total"), 
                                    show="headings", height=8)
        self.cart_tree.heading("Product", text="Product")
        self.cart_tree.heading("Qty", text="Qty")
        self.cart_tree.heading("Price", text="Price")
        self.cart_tree.heading("Total", text="Total")
        self.cart_tree.column("Product", width=200)
        self.cart_tree.column("Qty", width=80, anchor="center")
        self.cart_tree.column("Price", width=100, anchor="center")
        self.cart_tree.column("Total", width=120, anchor="center")
        self.cart_tree.pack(fill="both", expand=True, pady=10)
        
        # Cart actions
        cart_actions = tk.Frame(cart_frame, bg="#E0F7FA")
        cart_actions.pack(fill="x", pady=10)
        
        remove_button = tk.Button(cart_actions, text="Remove Selected", 
                                font=("Helvetica", 12), bg="#FF5722", fg="white",
                                command=self.remove_from_cart)
        remove_button.pack(side="left", padx=5)
        
        clear_button = tk.Button(cart_actions, text="Clear Cart", 
                               font=("Helvetica", 12), bg="#F44336", fg="white",
                               command=self.clear_cart)
        clear_button.pack(side="left", padx=5)
        
        # Order summary
        summary_frame = tk.Frame(self.order_frame, bg="#E0F7FA", bd=1, relief="solid")
        summary_frame.pack(fill="x", padx=20, pady=20)
        
        tk.Label(summary_frame, text="Order Summary", font=("Helvetica", 14, "bold"), 
                bg="#E0F7FA").pack(anchor="w", pady=10)
        
        self.subtotal_label = tk.Label(summary_frame, text="Subtotal: ₱0.00", 
                                     font=("Helvetica", 12), bg="#E0F7FA")
        self.subtotal_label.pack(anchor="center", padx=20)
        
        self.tax_label = tk.Label(summary_frame, text="Tax (5%): ₱0.00", 
                                font=("Helvetica", 12), bg="#E0F7FA")
        self.tax_label.pack(anchor="center", padx=20)
        
        self.total_label = tk.Label(summary_frame, text="Total: ₱0.00", 
                                  font=("Helvetica", 14, "bold"), bg="#E0F7FA")
        self.total_label.pack(anchor="center", padx=20, pady=10)
        
        # Customer info
        customer_frame = tk.Frame(self.order_frame, bg="#E0F7FA")
        customer_frame.pack(fill="x", padx=20, pady=10)
        
        tk.Label(customer_frame, text="Customer Name:", font=("Helvetica", 12), 
                bg="#E0F7FA").pack(side="left")
        self.customer_entry = tk.Entry(customer_frame, font=("Helvetica", 12), width=30)
        self.customer_entry.pack(side="left", padx=10)
        
        # Checkout button
        checkout_button = tk.Button(self.order_frame, text="Process Order", 
                                  font=("Helvetica", 14), bg="#2196F3", fg="white",
                                  command=self.process_order)
        checkout_button.pack(pady=20)
    
    def update_product_details(self, event=None):
        product_name = self.product_combobox.get()
        if product_name:
            self.cursor.execute("SELECT price, stock FROM products WHERE name=?", (product_name,))
            result = self.cursor.fetchone()
            if result:
                price, stock = result
                self.price_label.config(text=f"₱{price:.2f}")
                self.stock_label.config(text=str(stock))
                self.qty_spinbox.config(to=stock)
    
    def add_to_cart(self):
        product_name = self.product_combobox.get()
        if not product_name:
            messagebox.showwarning("Warning", "Please select a product")
            return
        
        try:
            qty = int(self.qty_spinbox.get())
            if qty <= 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Warning", "Please enter a valid quantity")
            return
        
        self.cursor.execute("SELECT id, price, stock FROM products WHERE name=?", (product_name,))
        result = self.cursor.fetchone()
        if not result:
            messagebox.showerror("Error", "Product not found")
            return
        
        product_id, price, stock = result
        
        if qty > stock:
            messagebox.showwarning("Warning", "Not enough stock available")
            return
        
        # Add to cart
        for item in self.cart:
            if item['id'] == product_id:
                item['quantity'] += qty
                break
        else:
            self.cart.append({
                'id': product_id,
                'name': product_name,
                'price': price,
                'quantity': qty
            })
        
        self.update_cart_display()
        
        # Update product stock in UI
        new_stock = stock - qty
        self.stock_label.config(text=str(new_stock))
        self.qty_spinbox.config(to=new_stock)
    
    def remove_from_cart(self):
        selected = self.cart_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select an item to remove")
            return
        
        item = self.cart_tree.item(selected[0])
        product_name = item['values'][0]
        
        # Find and remove from cart
        for i, cart_item in enumerate(self.cart):
            if cart_item['name'] == product_name:
                # Update product stock in UI
                self.cursor.execute("SELECT stock FROM products WHERE name=?", (product_name,))
                current_stock = self.cursor.fetchone()[0]
                returned_qty = cart_item['quantity']
                new_stock = current_stock + returned_qty
                
                # Update the combobox stock if this is the selected product
                if self.product_combobox.get() == product_name:
                    self.stock_label.config(text=str(new_stock))
                    self.qty_spinbox.config(to=new_stock)
                
                # Remove from cart
                del self.cart[i]
                break
        
        self.update_cart_display()
    
    def clear_cart(self):
        if not self.cart:
            return
            
        if messagebox.askyesno("Confirm", "Clear the entire cart?"):
            # Restore all quantities to product stock
            for item in self.cart:
                product_name = item['name']
                self.cursor.execute("SELECT stock FROM products WHERE name=?", (product_name,))
                current_stock = self.cursor.fetchone()[0]
                returned_qty = item['quantity']
                new_stock = current_stock + returned_qty
                
                if self.product_combobox.get() == product_name:
                    self.stock_label.config(text=str(new_stock))
                    self.qty_spinbox.config(to=new_stock)
            
            self.cart = []
            self.update_cart_display()
    
    def update_cart_display(self):
        # Clear current display
        for item in self.cart_tree.get_children():
            self.cart_tree.delete(item)
        
        # Add cart items
        subtotal = 0
        for item in self.cart:
            total = item['price'] * item['quantity']
            subtotal += total
            self.cart_tree.insert("", "end", values=(
                item['name'],
                item['quantity'],
                f"₱{item['price']:.2f}",
                f"₱{total:.2f}"
            ))
        
        # Update totals
        tax = subtotal * 0.5  # 10% tax
        total = subtotal + tax
        
        self.subtotal_label.config(text=f"Subtotal: ₱{subtotal:.2f}")
        self.tax_label.config(text=f"Tax (5%): ₱{tax:.2f}")
        self.total_label.config(text=f"Total: ₱{total:.2f}")
    
    def process_order(self):
        if not self.cart:
            messagebox.showwarning("Warning", "Cart is empty")
            return
        
        customer_name = self.customer_entry.get().strip()
        if not customer_name:
            messagebox.showwarning("Warning", "Please enter customer name")
            return
        
        # Create order in database
        try:
            # Start transaction
            self.cursor.execute("BEGIN TRANSACTION")
            
            # Create order record
            order_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            subtotal = sum(item['price'] * item['quantity'] for item in self.cart)
            tax = subtotal * 0.10
            total = subtotal + tax
            
            self.cursor.execute(
                "INSERT INTO orders (customer_name, order_date, subtotal, tax, total) VALUES (?, ?, ?, ?, ?)",
                (customer_name, order_date, subtotal, tax, total)
            )
            order_id = self.cursor.lastrowid
            
            # Add order items
            for item in self.cart:
                self.cursor.execute(
                    "INSERT INTO order_items (order_id, product_id, quantity, price) VALUES (?, ?, ?, ?)",
                    (order_id, item['id'], item['quantity'], item['price'])
                )
                
                # Update product stock
                self.cursor.execute(
                    "UPDATE products SET stock = stock - ? WHERE id = ?",
                    (item['quantity'], item['id'])
                )
            
            # Commit transaction
            self.conn.commit()
            
            # Generate receipt
            self.generate_receipt(order_id, customer_name, order_date)
            
            # Clear cart
            self.cart = []
            self.update_cart_display()
            self.customer_entry.delete(0, tk.END)
            
            messagebox.showinfo("Success", "Order processed successfully!")
            
            # Reload data to reflect stock changes
            self.load_data()
            
        except Exception as e:
            self.conn.rollback()
            messagebox.showerror("Error", f"Failed to process order: {str(e)}")
    
    def generate_receipt(self, order_id, customer_name, order_date):
        receipt_window = tk.Toplevel(self.root)
        receipt_window.title(f"Receipt - Order #{order_id}")
        receipt_window.geometry("500x700")
        
        # Receipt header
        header_frame = tk.Frame(receipt_window)
        header_frame.pack(pady=10)
        
        tk.Label(header_frame, text="POULTRY MANAGEMENT SYSTEM", 
                font=("Helvetica", 16, "bold")).pack()
        tk.Label(header_frame, text="123 Farm Road, Poultry City").pack()
        tk.Label(header_frame, text="Tel: (123) 456-7890").pack()
        
        # Order info
        info_frame = tk.Frame(receipt_window)
        info_frame.pack(pady=10)
        
        tk.Label(info_frame, text=f"Order #: {order_id}", font=("Helvetica", 12)).pack(anchor="w")
        tk.Label(info_frame, text=f"Date: {order_date}").pack(anchor="w")
        tk.Label(info_frame, text=f"Customer: {customer_name}").pack(anchor="w")
        
        # Items
        items_frame = tk.Frame(receipt_window)
        items_frame.pack(fill="x", padx=20, pady=10)
        
        tk.Label(items_frame, text="Items", font=("Helvetica", 12, "underline")).pack(anchor="w")
        
        # Get order items from database
        self.cursor.execute('''
            SELECT p.name, oi.quantity, oi.price, (oi.quantity * oi.price) as total
            FROM order_items oi
            JOIN products p ON oi.product_id = p.id
            WHERE oi.order_id = ?
        ''', (order_id,))
        items = self.cursor.fetchall()
        
        for item in items:
            item_frame = tk.Frame(items_frame)
            item_frame.pack(fill="x", pady=2)
            
            tk.Label(item_frame, text=f"{item[0]} x{item[1]}", width=30, anchor="w").pack(side="left")
            tk.Label(item_frame, text=f"₱{item[2]:.2f}").pack(side="left", padx=10)
            tk.Label(item_frame, text=f"₱{item[3]:.2f}", width=10, anchor="center").pack(side="right")
        
        # Totals
        totals_frame = tk.Frame(receipt_window)
        totals_frame.pack(fill="x", padx=20, pady=10)
        
        self.cursor.execute("SELECT subtotal, tax, total FROM orders WHERE id=?", (order_id,))
        subtotal, tax, total = self.cursor.fetchone()
        
        tk.Label(totals_frame, text=f"Subtotal: ₱{subtotal:.2f}", anchor="center").pack(fill="x")
        tk.Label(totals_frame, text=f"Tax (10%): ₱{tax:.2f}", anchor="center").pack(fill="x")
        tk.Label(totals_frame, text=f"Total: ₱{total:.2f}", font=("Helvetica", 12, "bold"), 
                anchor="center").pack(fill="x")
        
        # Footer
        footer_frame = tk.Frame(receipt_window)
        footer_frame.pack(pady=20)
        
        tk.Label(footer_frame, text="Thank you for your business!", font=("Helvetica", 12)).pack()
        tk.Label(footer_frame, text="Please come again!").pack()
        
        # Print button
        print_button = tk.Button(receipt_window, text="Print Receipt", 
                               command=lambda: self.print_receipt(receipt_window))
        print_button.pack(pady=10)
    
    def print_receipt(self, window):
        # In a real application, this would send to a printer
        # For now, we'll just show a message
        messagebox.showinfo("Print", "Receipt sent to printer")
        window.destroy()
    
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
    
    def load_data(self):
        # Clear all tables
        for table in [self.product_table, self.feeds_table]:
            for item in table.get_children():
                table.delete(item)
        
        try:
            # Load products
            self.cursor.execute("SELECT * FROM products")
            products = self.cursor.fetchall()
            for product in products:
                self.product_table.insert("", "end", values=product)
            
            # Update product combobox in order frame
            if hasattr(self, 'product_combobox'):
                self.product_combobox['values'] = [p[1] for p in products]
            
            # Load feeds
            self.cursor.execute("SELECT * FROM feeds")
            feeds = self.cursor.fetchall()
            for feed in feeds:
                self.feeds_table.insert("", "end", values=feed)
            
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