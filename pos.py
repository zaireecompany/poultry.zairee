import tkinter as tk
from tkinter import ttk, messagebox
import random
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

# Function to change the content of the dashboard based on button clicked
def change_content(frame):
    for f in [inventory_frame, sales_frame, products_frame, users_frame, feeds_frame]:
        f.grid_forget()
    frame.grid(row=1, column=1, padx=20, pady=20, sticky="nsew")
    
    if frame == inventory_frame:
        update_inventory_summary()

# Function to update inventory summary
def update_inventory_summary():
    user_count = user_table.index("end")
    product_count = product_table.index("end")
    feed_count = feeds_table.index("end")
    
    user_count_label.config(text=f"Users: {user_count}")
    product_count_label.config(text=f"Products: {product_count}")
    feed_count_label.config(text=f"Feeds: {feed_count}")

# Create the main window
root = tk.Tk()
root.title("Poultry Management Dashboard")
root.state("zoomed")  # Open in full screen
root.config(bg="#F4F4F9")

# Content Area
content_area = tk.Frame(root, bg="#E0F7FA")
content_area.grid(row=1, column=1, padx=20, pady=20, sticky="nsew")

# Frames for different sections
inventory_frame = tk.Frame(content_area, bg="#E0F7FA")
sales_frame = tk.Frame(content_area, bg="#E0F7FA")
products_frame = tk.Frame(content_area, bg="#E0F7F9")
users_frame = tk.Frame(content_area, bg="#E0F7FA")
feeds_frame = tk.Frame(content_area, bg="#E0F7FA")

# Function to create a styled table
def create_styled_table(frame, columns, data):
    table = ttk.Treeview(frame, columns=columns, show="headings", height=15)
    for col in columns:
        table.heading(col, text=col)
        table.column(col, width=200, anchor="center")
    
    for item in data:
        table.insert("", "end", values=item)

    table.pack(expand=True, fill=tk.BOTH)  # Pack the table into the frame
    return table

# 🛒 Product Management Section
product_columns = ("ID", "Name", "Category", "Stock", "Price")
product_data = [(i + 1, f"Product {i + 1}", "Category", 100, "$10") for i in range(10)]
product_table = create_styled_table(products_frame, product_columns, product_data)

# 👤 User Management Section
user_columns = ("ID", "Name", "Role", "Email")
user_data = [(i + 1, f"User {i + 1}", "Admin", f"user{i + 1}@email.com") for i in range(10)]
user_table = create_styled_table(users_frame, user_columns, user_data)

# 📦 Feeds Management Section
feeds_columns = ("ID", "Name", "Category", "Level")
feeds_data = [(i + 1, f"Feed {i + 1}", "Category", random.randint(1, 100)) for i in range(10)]
feeds_table = create_styled_table(feeds_frame, feeds_columns, feeds_data)

# Inventory Summary Section
summary_frame = tk.Frame(inventory_frame, bg="#E0F7FA")
summary_frame.pack(pady=20)

# User, Product, Feed Count Labels
user_count_label = tk.Label(summary_frame, text="Users: 0", font=("Helvetica", 18), bg="#E0F7FA")
user_count_label.grid(row=0, column=0, padx=20)

product_count_label = tk.Label(summary_frame, text="Products: 0", font=("Helvetica", 18), bg="#E0F7FA")
product_count_label.grid(row=0, column=1, padx=20)

feed_count_label = tk.Label(summary_frame, text="Feeds: 0", font=("Helvetica", 18), bg="#E0F7FA")
feed_count_label.grid(row=0, column=2, padx=20)

# Navigation Buttons
button_frame = tk.Frame(root, bg="#F4F4F9")
button_frame.grid(row=0, column=1, padx=20, pady=20, sticky="ew")

inventory_button = tk.Button(button_frame, text="Inventory", command=lambda: change_content(inventory_frame))
inventory_button.pack(side=tk.LEFT, padx=5)

sales_button = tk.Button(button_frame, text="Sales", command=lambda: change_content(sales_frame))
sales_button.pack(side=tk.LEFT, padx=5)

products_button = tk.Button(button_frame, text="Products", command=lambda: change_content(products_frame))
products_button.pack(side=tk.LEFT, padx=5)

users_button = tk.Button(button_frame, text="Users", command=lambda: change_content(users_frame))
users_button.pack(side=tk.LEFT, padx=5)

feeds_button = tk.Button(button_frame, text="Feeds", command=lambda: change_content(feeds_frame))
feeds_button.pack(side=tk.LEFT, padx=5)

# Show the inventory frame initially
change_content(inventory_frame)

# Run the main loop
root.mainloop()
