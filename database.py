import sqlite3

def create_database():
    conn = None
    try:
        # Connect to SQLite database
        conn = sqlite3.connect("poultry.db")
        cursor = conn.cursor()

        # Create Users Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                role TEXT,
                email TEXT,
                password TEXT NOT NULL
            )
        ''')
        
        # Create Products Table (for non-feed items)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                category TEXT,
                stock INTEGER,
                price REAL
            )
        ''')
        
        # Create Feeds Table (specifically for feed products)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS feeds (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                feed_type TEXT,
                stage TEXT,
                stock INTEGER,
                price REAL,
                weight TEXT
            )
        ''')
        
        # Create Orders Table
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
        
        # Create Order Items Table
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
        
        # Create Sales Table (modified to handle both products and feeds)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sales (
                transaction_id TEXT PRIMARY KEY,
                item_type TEXT,
                item_id INTEGER,
                quantity INTEGER,
                price REAL,
                date TEXT
            )
        ''')
        
        # Create Inventory Table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS inventory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                total_users INTEGER,
                total_products INTEGER,
                total_feeds INTEGER,
                total_profit REAL
            )
        ''')

        # Add admin user if not exists
        cursor.execute("SELECT COUNT(*) FROM users WHERE role='Admin'")
        if cursor.fetchone()[0] == 0:
            cursor.execute(
                "INSERT INTO users (name, role, email, password) VALUES (?, ?, ?, ?)",
                ("Admin User", "Admin", "admin@mail.com", "admin123")
            )
            print("Admin user added successfully.")

        # Insert sample products (non-feed items)
        sample_products = [
            # Meat Products
            ("Broiler Chicken", "Meat", 100, 5.00),
            ("Free-Range Chicken", "Meat", 80, 7.50),
            ("Turkey", "Meat", 40, 12.00),
            ("Duck", "Meat", 30, 9.00),
            ("Quail", "Meat", 60, 3.50),
            ("Cornish Hen", "Meat", 45, 8.00),
            
            # Egg Products
            ("Layer Chicken Eggs (Dozen)", "Eggs", 200, 4.00),
            ("Free-Range Eggs (Dozen)", "Eggs", 150, 5.50),
            ("Organic Eggs (Dozen)", "Eggs", 120, 6.50),
            ("Quail Eggs (30 pcs)", "Eggs", 100, 7.00),
            ("Duck Eggs (Dozen)", "Eggs", 80, 8.00),
            ("Omega-3 Enriched Eggs", "Eggs", 90, 7.50),
            
            # Healthcare Products
            ("Vaccination Kit", "Healthcare", 50, 25.00),
            ("Poultry Vitamins (1L)", "Healthcare", 70, 18.00),
            ("Antibiotics (100 tablets)", "Healthcare", 45, 30.00),
            ("Dewormer (500ml)", "Healthcare", 55, 22.00),
            ("Disinfectant (5L)", "Healthcare", 65, 28.00),
            ("Wound Spray", "Healthcare", 85, 15.00),
            ("Probiotics (1kg)", "Healthcare", 60, 20.00),
            ("Electrolytes (500g)", "Healthcare", 95, 12.00),
            
            # Equipment
            ("Automatic Feeder", "Equipment", 30, 45.00),
            ("Automatic Waterer", "Equipment", 25, 50.00),
            ("Heating Lamp", "Equipment", 40, 22.00),
            ("Egg Incubator (100 eggs)", "Equipment", 15, 120.00),
            ("Brooder Box", "Equipment", 20, 65.00),
            ("Nesting Box", "Equipment", 35, 28.00),
            ("Poultry Netting (50m)", "Equipment", 18, 75.00),
            ("Egg Scale", "Equipment", 50, 15.00),
            
            # Miscellaneous
            ("Egg Cartons (50 pcs)", "Miscellaneous", 200, 8.00),
            ("Poultry Leg Bands (100 pcs)", "Miscellaneous", 150, 6.00),
            ("Record Book", "Miscellaneous", 80, 5.00),
            ("Poultry Scale", "Miscellaneous", 25, 85.00),
            ("Plucking Machine", "Miscellaneous", 10, 250.00),
            ("Egg Washer", "Miscellaneous", 12, 180.00),
            ("Manure Spreader", "Miscellaneous", 8, 350.00),
            ("Poultry Carrier", "Miscellaneous", 30, 40.00),
            ("Fly Trap", "Miscellaneous", 60, 12.00),
            ("Rodent Control", "Miscellaneous", 45, 18.00),
            ("Poultry Book", "Miscellaneous", 70, 15.00),
            ("First Aid Kit", "Miscellaneous", 55, 25.00),
            ("Egg Grading Tray", "Miscellaneous", 90, 10.00),
            ("Poultry Apron", "Miscellaneous", 40, 22.00)
        ]
        cursor.executemany("INSERT INTO products (name, category, stock, price) VALUES (?, ?, ?, ?)", sample_products)
        print("Sample products added successfully.")

        # Insert sample feeds (separate table)
        sample_feeds = [
            # name, feed_type, stage, stock, price, weight
            ("Organic Starter Feed", "Organic", "Starter", 150, 15.00, "50kg"),
            ("Conventional Starter Feed", "Conventional", "Starter", 120, 14.00, "50kg"),
            ("Grower Feed", "Conventional", "Grower", 110, 13.50, "50kg"),
            ("Organic Layer Feed", "Organic", "Layer", 130, 16.00, "50kg"),
            ("Conventional Layer Feed", "Conventional", "Layer", 140, 15.50, "50kg"),
            ("Broiler Feed", "Conventional", "Broiler", 90, 18.00, "50kg"),
            ("Medicated Feed", "Medicated", "All Stages", 75, 19.00, "50kg"),
            ("Grit Supplement", "Supplement", "All Stages", 60, 12.00, "10kg"),
            ("Oyster Shell", "Supplement", "Layer", 85, 10.00, "10kg"),
            ("Poultry Premix", "Supplement", "All Stages", 50, 22.00, "5kg")
        ]
        cursor.executemany("INSERT INTO feeds (name, feed_type, stage, stock, price, weight) VALUES (?, ?, ?, ?, ?, ?)", sample_feeds)
        print("Sample feeds added successfully.")

        # Insert sample sales (can reference either products or feeds)
        sample_sales = [
            # transaction_id, item_type, item_id, quantity, price, date
            ("TXN001", "product", 1, 10, 50.00, "2025-04-01"),  # Broiler Chicken
            ("TXN002", "feed", 3, 5, 67.50, "2025-04-02"),      # Grower Feed
            ("TXN003", "product", 7, 8, 32.00, "2025-04-03")    # Layer Chicken Eggs
        ]
        cursor.executemany("INSERT INTO sales (transaction_id, item_type, item_id, quantity, price, date) VALUES (?, ?, ?, ?, ?, ?)", sample_sales)
        print("Sample sales added successfully.")

        # Insert initial inventory data
        cursor.execute("INSERT INTO inventory (total_users, total_products, total_feeds, total_profit) VALUES (?, ?, ?, ?)",
                       (1, len(sample_products), len(sample_feeds), 149.50))  # Sum of sample sales
        print("Initial inventory data added successfully.")

        # Commit changes
        conn.commit()

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

    finally:
        # Ensure the connection is closed
        if conn:
            conn.close()

# Call the function to create the database and insert sample data
create_database()