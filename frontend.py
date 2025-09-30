def display_top_sellers(inventory, top_products):
    """Show nicely formatted top selling products"""
    if not top_products:
        print("No sales yet, so no best sellers!")
        return
    
    print("\n🏆 TOP SELLING PRODUCTS 🏆")
    print(f"{'Rank':<5} {'Product ID':<12} {'Name':20} {'Sold Qty':>10}")
    print("-" * 50)
    for idx, (pid, qty) in enumerate(top_products, start=1):
        name = inventory[pid]['name'] if pid in inventory else "(deleted product)"
        print(f"{idx:<5} {pid:<12} {name:20} {qty:>10}")
# frontend.py
"""
Frontend stuff for my shop system.
I added some emojis to make it less boring lol.
Might add colors someday if I figure out how.
"""

import os
import csv
from datetime import datetime
from backend import BILLS_FOLDER, save_bill_file

def get_float_input(prompt):
    """Keep asking until they give me a proper number"""
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("C'mon, that's not a number! Try again.")

def get_int_input(prompt):
    """Same as above but for whole numbers"""
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("I need a whole number here, please.")

def show_product_menu():
    print("\n--- PRODUCT STUFF ---")
    print("1. Add new product")
    print("2. Change product details")
    print("3. Remove product")
    print("4. Look up products")
    print("5. Go back")
    return input("What do you want to do? ")

def show_order_menu():
    print("\n--- ORDERS ---")
    print("1. Buy stuff (add to cart & checkout)")
    print("2. Never mind, go back")
    return input("Pick one: ")

def show_reports_menu():
    print("\n--- REPORTS & STATS ---")
    print("1. See how much we made on a day")
    print("2. Check what's running low")
    print("3. Back to main menu")
    return input("Your choice: ")

def display_inventory(inventory):
    if not inventory:
        print("Nothing in stock right now. So empty...")
        return
    
    print(f"\n{'ID':12} {'Product Name':20} {'Price':>8} {'In Stock':>10}")
    print("-" * 60)
    for pid, item in inventory.items():
        print(f"{pid:12} {item['name']:20} {item['price']:8.2f} {item['stock']:10}")

def display_search_results(results):
    if not results:
        print("Couldn't find anything matching that.")
        return
    
    print(f"\n{'ID':12} {'Product Name':20} {'Price':>8} {'In Stock':>10}")
    print("-" * 60)
    for pid, item in results:
        print(f"{pid:12} {item['name']:20} {item['price']:8.2f} {item['stock']:10}")

def display_low_stock(products):
    if not products:
        print("Everything looks good! Nothing running dangerously low.")
        return
    
    print(f"\n{'ID':12} {'Product Name':20} {'Left in Stock':>12}")
    print("-" * 50)
    for pid, item in products:
        print(f"{pid:12} {item['name']:20} {item['stock']:12}")

def collect_cart_items(inventory):
    """Let people add stuff to their cart"""
    cart = {}
    
    while True:
        pid = input("\nEnter product ID (or type 'stop' when done): ").strip()
        if pid.lower() == 'stop':
            break
            
        if pid not in inventory:
            print("Hmm, don't have that product ID. Check your spelling?")
            continue
            
        available = inventory[pid]['stock']
        if available == 0:
            print(f"Sorry, {inventory[pid]['name']} is all sold out!")
            continue
            
        try:
            qty = int(input(f"How many? (we have {available}): "))
        except ValueError:
            print("Numbers only please!")
            continue
            
        if qty <= 0:
            print("Seriously? You need to buy at least 1!")
            continue
            
        if qty > available:
            print(f"Whoa there! We only have {available} of those.")
            continue
            
        # Add to cart (or update quantity if already in cart)
        if pid in cart:
            cart[pid] += qty
        else:
            cart[pid] = qty
            
        print(f"✓ Added {qty} {inventory[pid]['name']} to cart")
        
    return cart

def prompt_save_bill(bill_text):
    """Ask if they want to save the receipt"""
    while True:
        print("\nWant to save this receipt?")
        print("1 - Save as text file")
        print("2 - Save as CSV (why though?)")
        print("3 - Nah, don't save it")
        
        choice = input("Your pick: ")
        
        if choice == '1':
            filename = os.path.join(BILLS_FOLDER, f"receipt_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
            save_bill_file(filename, bill_text)
            print(f"Saved as {filename}")
            break
        elif choice == '2':
            filename = os.path.join(BILLS_FOLDER, f"receipt_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
            lines = bill_text.splitlines()
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                for line in lines:
                    writer.writerow([line])
            print(f"Saved as {filename} (CSV format is weird for receipts but whatever)")
            break
        elif choice == '3':
            print("Okay, not saving it.")
            break
        else:
            print("Just pick 1, 2, or 3 please.")