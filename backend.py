import os
import csv

def get_top_selling_products(limit=5):
    """
    Show the top N selling products by total quantity sold.
    Default = top 5.
    """
    if not os.path.exists(SALES_FILE):
        print("No sales recorded yet.")
        return []

    sales_count = {}
    try:
        with open(SALES_FILE, 'r', newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) >= 3:
                    pid, qty = row[1], int(row[2])
                    sales_count[pid] = sales_count.get(pid, 0) + qty
    except Exception as e:
        print(f"Error reading sales file: {e}")
        return []

    # Sort by quantity sold
    top_products = sorted(sales_count.items(), key=lambda x: x[1], reverse=True)[:limit]
    return top_products
# backend.py
"""
Backend logic for my shop system.
I built this after I messed up counting inventory by hand too many times.
Still using CSV files because databases seem complicated.
"""

import csv
import os
from datetime import datetime

# Where we store our data
PRODUCTS_FILE = 'products.csv'
SALES_FILE = 'sales.csv'
BILLS_FOLDER = 'receipts'

# Make sure the receipts folder exists
os.makedirs(BILLS_FOLDER, exist_ok=True)

def load_inventory():
    """
    Load all our products from the CSV file.
    If the file doesn't exist or is messed up, we start fresh.
    """
    inventory = {}
    
    if not os.path.exists(PRODUCTS_FILE):
        print("(First time running? No products file found, starting fresh)")
        return inventory
    
    try:
        with open(PRODUCTS_FILE, 'r', newline='') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Skip empty rows or messed up data
                if not row.get('Product ID') or not row.get('Name'):
                    continue
                    
                inventory[row['Product ID']] = {
                    'name': row['Name'],
                    'price': float(row['Price']),
                    'stock': int(row['Stock Quantity'])
                }
        print(f"Loaded {len(inventory)} products from file")
    except Exception as e:
        print(f"Uh oh, had trouble reading the products file: {e}")
        print("We'll start with an empty inventory")
    
    return inventory

def save_inventory(inventory):
    """Save our current inventory back to the CSV file"""
    try:
        with open(PRODUCTS_FILE, 'w', newline='') as f:
            fieldnames = ['Product ID', 'Name', 'Price', 'Stock Quantity']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            for pid, item in inventory.items():
                writer.writerow({
                    'Product ID': pid,
                    'Name': item['name'],
                    'Price': item['price'],
                    'Stock Quantity': item['stock']
                })
    except Exception as e:
        print(f"CRITICAL: Failed to save inventory! Error: {e}")
        # In a real app I'd handle this better but for now... yolo

def add_new_product(inventory, pid, name, price, stock):
    """Add a new product to our inventory"""
    if pid in inventory:
        return False, f"Oops! Product ID '{pid}' already exists. Use a different ID."
    
    inventory[pid] = {
        'name': name,
        'price': price,
        'stock': stock
    }
    
    save_inventory(inventory)
    return True, f"Nice! Added '{name}' to inventory."

def modify_product(inventory, pid, new_name=None, new_price=None, new_stock=None):
    """Change details of an existing product"""
    if pid not in inventory:
        return False, "Can't find that product. Wrong ID?"
    
    product = inventory[pid]
    
    if new_name:
        old_name = product['name']
        product['name'] = new_name
        print(f"Changed name from '{old_name}' to '{new_name}'")
    
    if new_price is not None:
        old_price = product['price']
        product['price'] = new_price
        print(f"Changed price from {old_price:.2f} to {new_price:.2f}")
    
    if new_stock is not None:
        old_stock = product['stock']
        product['stock'] = new_stock
        print(f"Changed stock from {old_stock} to {new_stock}")
    
    save_inventory(inventory)
    return True, "Product updated successfully!"

def remove_product(inventory, pid):
    """Completely remove a product from inventory"""
    if pid not in inventory:
        return False, "Product not found. Maybe it was already deleted?"
    
    product_name = inventory[pid]['name']
    del inventory[pid]
    
    save_inventory(inventory)
    return True, f"Removed '{product_name}' from inventory."

def find_products(inventory, search_term):
    """Search for products by name or ID"""
    search_term = search_term.lower()
    results = []
    
    for pid, item in inventory.items():
        if (search_term in pid.lower() or 
            search_term in item['name'].lower()):
            results.append((pid, item))
    
    return results

def reduce_stock(inventory, pid, quantity):
    """Reduce stock when someone buys something"""
    if pid not in inventory:
        return False, "Product not found. This shouldn't happen..."
    
    if inventory[pid]['stock'] < quantity:
        return False, f"Not enough {inventory[pid]['name']} in stock!"
    
    inventory[pid]['stock'] -= quantity
    save_inventory(inventory)
    return True, f"Stock updated for {inventory[pid]['name']}"

def log_sale(cart, total_amount):
    """
    Record a sale in our sales log.
    TODO: This should probably track individual item totals instead of the whole bill total
    for each item, but it works for now.
    """
    sale_time = datetime.now()
    
    try:
        with open(SALES_FILE, 'a', newline='') as f:
            writer = csv.writer(f)
            for pid, qty in cart.items():
                writer.writerow([
                    sale_time.strftime('%Y-%m-%d'),
                    pid,
                    qty,
                    total_amount  # This is the whole bill total, not per item
                ])
    except Exception as e:
        print(f"Warning: Failed to log sale: {e}")

def get_daily_sales(date_string):
    """How much money did we make on a specific day?"""
    total = 0.0
    
    if not os.path.exists(SALES_FILE):
        return total
    
    try:
        with open(SALES_FILE, 'r', newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                if row and row[0] == date_string:
                    total += float(row[3])  # This counts the whole bill multiple times if multiple items
    except Exception as e:
        print(f"Had trouble reading sales data: {e}")
    
    return total

def get_low_stock_products(inventory, threshold=5):
    """Find products that are running low"""
    low_stock = []
    for pid, item in inventory.items():
        if item['stock'] <= threshold:
            low_stock.append((pid, item))
    
    return low_stock

def create_bill_text(inventory, cart, discount_percent=0):
    """Generate a nice-looking receipt"""
    now = datetime.now()
    lines = []
    
    lines.append("RECEIPT")
    lines.append("=" * 50)
    lines.append(f"Date: {now.strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("")
    lines.append(f"{'Item':20} {'Qty':>4} {'Price':>9} {'Total':>10}")
    lines.append("-" * 50)
    
    subtotal = 0.0
    
    for pid, quantity in cart.items():
        product = inventory[pid]
        item_total = product['price'] * quantity
        subtotal += item_total
        
        # Truncate long names
        name = product['name']
        if len(name) > 20:
            name = name[:17] + "..."
        
        lines.append(f"{name:20} {quantity:4} {product['price']:9.2f} {item_total:10.2f}")
    
    lines.append("-" * 50)
    lines.append(f"{'Subtotal:':>43} {subtotal:10.2f}")
    
    if discount_percent > 0:
        discount_amount = subtotal * (discount_percent / 100)
        final_total = subtotal - discount_amount
        lines.append(f"{'Discount (' + str(discount_percent) + '%):':>43} -{discount_amount:10.2f}")
        lines.append(f"{'Total:':>43} {final_total:10.2f}")
    else:
        final_total = subtotal
        lines.append(f"{'Total:':>43} {final_total:10.2f}")
    
    lines.append("=" * 50)
    lines.append("Thank you for your business!")
    
    return "\n".join(lines), final_total

def save_bill_file(filename, content):
    """Save a bill/receipt to a file"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
    except Exception as e:
        print(f"Failed to save receipt: {e}")