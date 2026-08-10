# Inventory & Sales Management System

A command-line inventory and sales management application built with Python.

The application allows users to create and manage products, track stock, record sales, and analyze business performance.

Product and sales information is stored locally using SQLite. Pandas is used for data analysis and Matplotlib is used for visualization.

No external dataset, API, or online service is required.

## Features

### Inventory Management

* Add products
* View inventory
* Update products
* Delete products
* Track stock quantities
* Identify low-stock products

### Sales Management

* Sell products
* Automatically reduce inventory after a sale
* Record transaction date and time
* Calculate total sale value
* View sales history

### Analytics

* Total revenue
* Total units sold
* Number of transactions
* Average transaction value
* Best-selling products
* Sales by category
* Low-stock report

### Visualization

* Revenue by product
* Revenue distribution by category

## Technologies Used

* Python
* SQLite
* Pandas
* Matplotlib

Python standard-library modules:

* `sqlite3`
* `datetime`

## Project Structure

```text
inventory-sales-system/
│
├── main.py
├── README.md
└── inventory.db        # Created automatically
```

`inventory.db` does not need to be created manually.

The program creates the database and required tables automatically when it is first run.

## Installation

Make sure Python is installed.

Create a virtual environment:

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

Install the required packages:

```bash
pip install -r requirements.txt
```

## Running the Project

Run:

```bash
python main.py
```

The application will display:

```text
============================================================
       INVENTORY & SALES MANAGEMENT
============================================================
1. Add Product
2. View Inventory
3. Update Product
4. Delete Product
5. Sell Product
6. View Sales
7. Sales Summary
8. Best-Selling Products
9. Sales by Category
10. Low Stock Report
11. Product Revenue Chart
12. Category Revenue Chart
13. Exit
============================================================
```

# Adding Products

Select:

```text
1. Add Product
```

Enter information such as:

```text
Product name: Wireless Mouse
Category: Electronics
Price: ₹799
Initial stock: 25
```

The product is stored in the SQLite database.

## Viewing Inventory

Select:

```text
2. View Inventory
```

Example:

```text
===========================================================
INVENTORY
===========================================================
 id  name              category       price  stock
  1  Wireless Mouse    Electronics    799.0     25
  2  Keyboard           Electronics   1299.0     15
  3  Notebook           Stationery     120.0     40
```

## Updating Products

Select:

```text
3. Update Product
```

You can modify:

* Product name
* Category
* Price
* Stock

Leaving a field empty keeps its current value.

## Selling Products

Select:

```text
5. Sell Product
```

For example:

```text
Enter product ID to sell: 1

Product : Wireless Mouse
Price   : ₹799.00
Stock   : 25

Quantity sold: 3
```

The system calculates:

```text
Total = 799 × 3
      = ₹2397
```

It then:

1. Creates a sales record.
2. Reduces inventory by 3.
3. Records the date and time.

The new stock becomes:

```text
22
```

## Sales History

Select:

```text
6. View Sales
```

Example:

```text
sale_id  product          category     quantity  total    date
1        Wireless Mouse   Electronics     3       2397    2026-08-09 11:20:10
2        Notebook         Stationery      5        600    2026-08-09 11:25:42
```

## Sales Summary

Select:

```text
7. Sales Summary
```

Example:

```text
==================================================
SALES SUMMARY
==================================================
Total Revenue     : ₹18,450.00
Units Sold        : 42
Transactions      : 18
Average Sale      : ₹1,025.00
```

## Best-Selling Products

Select:

```text
8. Best-Selling Products
```

The system groups sales by product.

Example:

```text
product          units_sold    revenue
Wireless Mouse       15        11985
Keyboard             10        12990
Notebook             25         3000
```

This helps identify which products are selling the most.

## Sales by Category

Select:

```text
9. Sales by Category
```

Example:

```text
category          units_sold    revenue
Electronics           25        24975
Stationery            40         4800
Accessories            8         3200
```

## Low Stock Report

Select:

```text
10. Low Stock Report
```

The system identifies products with five or fewer units remaining.

Example:

```text
 id  name              category       stock
  4  Wireless Headset  Electronics       3
  7  USB Hub           Accessories        2
```

This can be used as a basic inventory replenishment system.

## Revenue Charts

The project provides two visualizations.

### Product Revenue Chart

Shows the revenue generated by individual products.

### Category Revenue Chart

Shows the proportion of total revenue generated by different categories.

## Database

The application creates:

```text
inventory.db
```

The database contains two tables.

### Products

```text
products
│
├── id
├── name
├── category
├── price
└── stock
```

### Sales

```text
sales
│
├── id
├── product_id
├── quantity
├── total
└── sale_date
```

The relationship is:

```text
Products
    │
    │ product_id
    ↓
Sales
```

This introduces the concept of a **relational database**.

## Program Workflow

```text
Add Products
     ↓
Store in SQLite
     ↓
View / Update Inventory
     ↓
Customer Purchase
     ↓
Create Sales Record
     ↓
Update Stock
     ↓
Analyze Sales
     ↓
Generate Business Insights
     ↓
Create Charts
```

## Python Concepts Practiced

This project introduces:

* SQLite databases
* SQL queries
* Database tables
* Primary keys
* Foreign keys
* CRUD operations
* Pandas
* DataFrames
* SQL + Pandas integration
* `JOIN`
* `GROUP BY`
* Aggregation
* Sorting
* Matplotlib
* Exception handling
* Functions
* Input validation
* Date/time handling
* Persistent application state

## Learning Objective

The goal is to understand how Python applications can work with a real database rather than relying only on JSON or CSV files.

The project combines:

```text
Python
   +
SQLite
   +
Pandas
   +
Matplotlib
```

This creates a much more realistic application architecture.

## Important Safety Behavior

The application prevents a product from being sold when insufficient stock is available.

For example:

```text
Available stock: 4
Quantity requested: 6

Only 4 units are available.
```

Products that already have sales history are also prevented from being deleted so that historical sales records are not accidentally broken.

## Possible Improvements

After completing the basic project, you can add:

* Customer management
* Customer purchase history
* Multiple products in one invoice
* Invoice generation
* Discount system
* Tax/GST calculation
* Profit calculation
* Supplier management
* Purchase/restocking system
* Monthly revenue analysis
* Sales forecasting
* Search products
* Product barcode support
* User login and roles
* Tkinter GUI
* Interactive Plotly dashboard
* Export reports to Excel
* Automated low-stock alerts