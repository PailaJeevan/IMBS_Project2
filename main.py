# main.py
"""
Main shop management program
I built this to stop messing up my inventory counts
It's not perfect but it works for my small shop
"""

from backend import (
    load_inventory, add_new_product, modify_product, remove_product, 
    find_products, reduce_stock, log_sale, get_daily_sales, 
    get_low_stock_products, create_bill_text
)
from frontend import (
    get_float_input, get_int_input, show_product_menu, show_order_menu,
    show_reports_menu, display_inventory, display_search_results, 
    display_low_stock, collect_cart_items, prompt_save_bill
)
from datetime import datetime

def main():
    print("Starting up Shop Manager...")
    inventory = load_inventory()
    print("Ready!\n")
    
    while True:
        print("\n" + "="*50)
        print("        🏪 MY SHOP MANAGER")
        print("="*50)
        print("1. Manage Products")
        print("2. Process Orders")
        print("3. Reports & Stats")
        print("4. Exit")
        print("-"*50)
        
        choice = input("What do you want to do? (1-4): ").strip()
        
        if choice == '1':
            # Product management
            while True:
                sub_choice = show_product_menu()
                
                if sub_choice == '1':
                    # Add product
                    print("\n--- ADD NEW PRODUCT ---")
                    pid = input("Product ID: ").strip()
                    name = input("Product Name: ").strip()
                    
                    if not pid or not name:
                        print("Need both ID and name!")
                        continue
                    
                    price = get_float_input("Price: ")
                    stock = get_int_input("Initial stock quantity: ")
                    
                    success, message = add_new_product(inventory, pid, name, price, stock)
                    print(message)
                    
                elif sub_choice == '2':
                    # Update product
                    print("\n--- UPDATE PRODUCT ---")
                    pid = input("Enter product ID to update: ").strip()
                    
                    if pid not in inventory:
                        print("That product doesn't exist!")
                        continue
                    
                    print(f"\nCurrent details:")
                    print(f"  Name: {inventory[pid]['name']}")
                    print(f"  Price: {inventory[pid]['price']:.2f}")
                    print(f"  Stock: {inventory[pid]['stock']}")
                    
                    new_name = input("\nNew name (press Enter to keep current): ").strip()
                    new_name = new_name if new_name else None
                    
                    new_price_input = input("New price (press Enter to keep current): ").strip()
                    new_price = float(new_price_input) if new_price_input else None
                    
                    new_stock_input = input("New stock quantity (press Enter to keep current): ").strip()
                    new_stock = int(new_stock_input) if new_stock_input else None
                    
                    success, message = modify_product(inventory, pid, new_name, new_price, new_stock)
                    print(message)
                    
                elif sub_choice == '3':
                    # Delete product
                    print("\n--- DELETE PRODUCT ---")
                    pid = input("Enter product ID to remove: ").strip()
                    
                    if pid not in inventory:
                        print("Product not found!")
                        continue
                    
                    # Double check - don't want accidental deletions!
                    confirm = input(f"Are you SURE you want to delete {inventory[pid]['name']}? (y/n): ")
                    if confirm.lower() == 'y':
                        success, message = remove_product(inventory, pid)
                        print(message)
                    else:
                        print("Phew! Cancelled deletion.")
                        
                elif sub_choice == '4':
                    # Search products
                    print("\n--- SEARCH PRODUCTS ---")
                    search_term = input("Enter product name or ID to search for: ").strip()
                    results = find_products(inventory, search_term)
                    display_search_results(results)
                    
                elif sub_choice == '5':
                    # Go back
                    break
                else:
                    print("Huh? Please pick 1-5")
        
        elif choice == '2':
            # Order processing
            while True:
                sub_choice = show_order_menu()
                
                if sub_choice == '1':
                    print("\n--- PROCESS ORDER ---")
                    
                    if not inventory:
                        print("No products available yet! Add some products first.")
                        continue
                    
                    # Show what's available
                    print("\nAvailable products:")
                    display_inventory(inventory)
                    
                    # Build the cart
                    print("\nLet's add items to your cart:")
                    cart = collect_cart_items(inventory)
                    
                    if not cart:
                        print("Cart is empty, nothing to checkout.")
                        continue
                    
                    # Apply discount?
                    discount = 0
                    if input("\nApply discount? (y/n): ").lower() == 'y':
                        discount = get_float_input("Discount percentage (0-100): ")
                        if discount < 0 or discount > 100:
                            print("Invalid discount, ignoring...")
                            discount = 0
                    
                    # Generate and show bill
                    bill_text, total = create_bill_text(inventory, cart, discount)
                    print("\n" + "="*60)
                    print("FINAL RECEIPT")
                    print("="*60)
                    print(bill_text)
                    
                    # Update inventory and log sale
                    print("\nUpdating inventory...")
                    for pid, qty in cart.items():
                        reduce_stock(inventory, pid, qty)
                    
                    log_sale(cart, total)
                    print("Sale recorded!")
                    
                    # Offer to save receipt
                    prompt_save_bill(bill_text)
                    
                elif sub_choice == '2':
                    break
                else:
                    print("Please pick 1 or 2")
        
        elif choice == '3':
            # Reports
            while True:
                sub_choice = show_reports_menu()
                
                if sub_choice == '1':
                    # Daily sales
                    print("\n--- DAILY SALES REPORT ---")
                    date_str = input("Enter date (YYYY-MM-DD): ").strip()
                    
                    try:
                        # Validate date format
                        datetime.strptime(date_str, '%Y-%m-%d')
                    except ValueError:
                        print("Invalid date format! Use YYYY-MM-DD")
                        continue
                    
                    sales_total = get_daily_sales(date_str)
                    print(f"\nTotal sales on {date_str}: ${sales_total:.2f}")
                    
                elif sub_choice == '2':
                    # Low stock alert
                    print("\n--- LOW STOCK REPORT ---")
                    try:
                        threshold = int(input("Alert threshold (default 5): ") or "5")
                    except ValueError:
                        threshold = 5
                        print("Using default threshold of 5")
                    
                    low_stock = get_low_stock_products(inventory, threshold)
                    display_low_stock(low_stock)
                    
                elif sub_choice == '3':
                    break
                else:
                    print("Please pick 1-3")
        
        elif choice == '4':
            # Exit
            print("\nThanks for using My Shop Manager!")
            print("Have a great day! 👋")
            break
        
        else:
            print("Not sure what that means. Please pick 1, 2, 3, or 4.")

if __name__ == "__main__":
    main()