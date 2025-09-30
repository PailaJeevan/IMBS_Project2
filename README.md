# 🏪 Inventory Management & Billing System -- Python Console Application

## 📌 Project Overview

This is a **console-based Python application** designed to help small
shops manage their inventory, process customer orders, and generate
receipts.
The system keeps track of products, stock levels, and daily sales while
providing simple reporting features --- all without requiring external
frameworks or databases.
Data is stored in **CSV files** for easy portability and editing.

------------------------------------------------------------------------

## 🎯 Objectives

-   Manage **product inventory** with add, update, delete, and search
    functionality.
-   Process **customer orders** with cart-based checkout and automatic
    stock updates.
-   Generate and save **bills/receipts** in `.txt` or `.csv` formats.
-   Provide **reports** on daily sales and low-stock alerts.

------------------------------------------------------------------------

## 🚀 Features

### 📦 Product Management

-   Add new products with unique **Product ID**.
-   Update product details (**Name, Price, Stock Quantity**).
-   Delete products safely (with confirmation).
-   Search products by **ID or Name**.

### 🛒 Order Processing

-   Add multiple items to a shopping cart.
-   Validate stock availability before checkout.
-   Auto-update inventory after purchase.
-   Optional **discounts** on total bill.

### 🧾 Billing

-   Generate text-based receipts with:
    -   Item details (Name, Qty, Price, Total)
    -   Subtotal, Discounts, and Final Total
    -   Date & Time of purchase
-   Option to save bill as:
    -   **Text file (.txt)**
    -   **CSV file (.csv)**

### 📊 Reports

-   View **total sales** for a specific date.
-   Identify **low-stock products** below a set threshold.
-   Display **top-selling products** (from sales history).

------------------------------------------------------------------------

## 🛠 Tools & Libraries

-   **Python Standard Library only**:
    -   `csv` -- store and read product/sales data
    -   `datetime` -- record sales timestamps
    -   `os` -- manage files and directories

> ✅ No external dependencies required. Works on any Python 3.x
> installation.

------------------------------------------------------------------------

## 📂 Project Structure

    Inventory-Management-System/
    │── backend.py      # Core business logic (inventory, sales, billing)
    │── frontend.py     # Console UI and input/output helpers
    │── main.py         # Entry point (menus, workflows)
    │── products.csv    # Inventory data (auto-created if missing)
    │── sales.csv       # Sales log (auto-created after first sale)
    │── receipts/       # Folder to store generated bills

------------------------------------------------------------------------

## ▶️ How to Run

1.  Make sure you have **Python 3.x** installed.

2.  Clone or download this project.

3.  Run the program:

    ``` bash
    python main.py
    ```

4.  Follow the interactive console menus.

------------------------------------------------------------------------

## 📊 Example Workflow

1.  **Add Products** → Enter Product ID, Name, Price, Stock.\
2.  **Process Order** → Select items, confirm quantities, apply
    discounts.\
3.  **Generate Bill** → View receipt, optionally save as `.txt` or
    `.csv`.\
4.  **Reports** → Check daily sales or low-stock alerts.

------------------------------------------------------------------------

## 📌 Future Enhancements

-   Export reports in **CSV/Excel** format.\
-   Support for **user authentication** (admin/cashier roles).\
-   Integration with a **GUI interface** (Tkinter or PyQt).\
-   Proper per-item tracking in sales log (instead of whole-bill
    totals).

------------------------------------------------------------------------
## ✅ Key Deliverables

-   Inventory CRUD operations
-   Order management & billing system
-   Report generation (sales & stock)
-   File-based persistence with CSV
-   Console-based user interface

------------------------------------------------------------------------
## 📩 Contact

- 👨‍💻 **Developer:** Paila Jeevan
- 📧 **Email:** pailajeevan21@gmail.com
- 🌐 **GitHub:**
https://github.com/PailaJeevan

💡 Feel free to fork, contribute, or drop a message if you have ideas to
improve this project!
