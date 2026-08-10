import sqlite3
from datetime import datetime

import pandas as pd
import matplotlib.pyplot as plt


DATABASE = "inventory.db"


# ============================================================
# DATABASE
# ============================================================

def connect_db():
    return sqlite3.connect(DATABASE)


def initialize_database():
    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL,
            stock INTEGER NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            total REAL NOT NULL,
            sale_date TEXT NOT NULL,
            FOREIGN KEY (product_id)
            REFERENCES products(id)
        )
    """)

    connection.commit()
    connection.close()


# ============================================================
# INPUT VALIDATION
# ============================================================

def get_positive_float(prompt):

    while True:

        try:
            value = float(input(prompt))

            if value > 0:
                return value

            print("Value must be greater than 0.")

        except ValueError:
            print("Please enter a valid number.")


def get_non_negative_float(prompt):

    while True:

        try:
            value = float(input(prompt))

            if value >= 0:
                return value

            print("Value cannot be negative.")

        except ValueError:
            print("Please enter a valid number.")


def get_positive_integer(prompt):

    while True:

        try:
            value = int(input(prompt))

            if value > 0:
                return value

            print("Value must be greater than 0.")

        except ValueError:
            print("Please enter a valid integer.")


# ============================================================
# PRODUCT MANAGEMENT
# ============================================================

def add_product():

    print("\n" + "=" * 50)
    print("ADD PRODUCT")
    print("=" * 50)

    name = input("Product name: ").strip()

    if not name:
        print("Product name cannot be empty.")
        return

    category = input("Category: ").strip()

    if not category:
        print("Category cannot be empty.")
        return

    price = get_positive_float(
        "Price: ₹"
    )

    stock = get_positive_integer(
        "Initial stock: "
    )

    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO products
        (name, category, price, stock)
        VALUES (?, ?, ?, ?)
    """, (
        name,
        category,
        price,
        stock
    ))

    connection.commit()
    connection.close()

    print("\nProduct added successfully.")


def view_products():

    connection = connect_db()

    query = """
        SELECT
            id,
            name,
            category,
            price,
            stock
        FROM products
        ORDER BY id
    """

    df = pd.read_sql_query(
        query,
        connection
    )

    connection.close()

    if df.empty:

        print("\nNo products available.")
        return df

    print("\n" + "=" * 75)
    print("INVENTORY")
    print("=" * 75)

    display_df = df.copy()

    display_df["price"] = (
        display_df["price"]
        .map(lambda x: f"₹{x:,.2f}")
    )

    print(
        display_df.to_string(
            index=False
        )
    )

    return df


def update_product():

    df = view_products()

    if df.empty:
        return

    product_id = get_positive_integer(
        "\nEnter product ID to update: "
    )

    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM products WHERE id = ?",
        (product_id,)
    )

    product = cursor.fetchone()

    if product is None:

        print("Product not found.")
        connection.close()
        return

    print("\nLeave a field empty to keep its current value.")

    new_name = input(
        f"Name [{product[1]}]: "
    ).strip()

    new_category = input(
        f"Category [{product[2]}]: "
    ).strip()

    new_price = input(
        f"Price [{product[3]}]: "
    ).strip()

    new_stock = input(
        f"Stock [{product[4]}]: "
    ).strip()

    name = new_name if new_name else product[1]

    category = (
        new_category
        if new_category
        else product[2]
    )

    try:

        price = (
            float(new_price)
            if new_price
            else product[3]
        )

        stock = (
            int(new_stock)
            if new_stock
            else product[4]
        )

        if price < 0 or stock < 0:
            print("Price and stock cannot be negative.")
            connection.close()
            return

    except ValueError:

        print("Invalid price or stock.")
        connection.close()
        return

    cursor.execute("""
        UPDATE products
        SET name = ?,
            category = ?,
            price = ?,
            stock = ?
        WHERE id = ?
    """, (
        name,
        category,
        price,
        stock,
        product_id
    ))

    connection.commit()
    connection.close()

    print("\nProduct updated successfully.")


def delete_product():

    df = view_products()

    if df.empty:
        return

    product_id = get_positive_integer(
        "\nEnter product ID to delete: "
    )

    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT name FROM products WHERE id = ?",
        (product_id,)
    )

    product = cursor.fetchone()

    if product is None:

        print("Product not found.")
        connection.close()
        return

    cursor.execute(
        "SELECT COUNT(*) FROM sales "
        "WHERE product_id = ?",
        (product_id,)
    )

    sales_count = cursor.fetchone()[0]

    if sales_count > 0:

        print(
            "\nThis product has sales history "
            "and cannot be deleted."
        )

        connection.close()
        return

    cursor.execute(
        "DELETE FROM products WHERE id = ?",
        (product_id,)
    )

    connection.commit()
    connection.close()

    print(
        f"\n'{product[0]}' deleted successfully."
    )


# ============================================================
# SALES
# ============================================================

def sell_product():

    df = view_products()

    if df.empty:
        return

    product_id = get_positive_integer(
        "\nEnter product ID to sell: "
    )

    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            name,
            price,
            stock
        FROM products
        WHERE id = ?
    """, (product_id,))

    product = cursor.fetchone()

    if product is None:

        print("Product not found.")
        connection.close()
        return

    product_id, name, price, stock = product

    if stock <= 0:

        print(
            f"\n'{name}' is out of stock."
        )

        connection.close()
        return

    print(f"\nProduct : {name}")
    print(f"Price   : ₹{price:,.2f}")
    print(f"Stock   : {stock}")

    quantity = get_positive_integer(
        "Quantity sold: "
    )

    if quantity > stock:

        print(
            f"\nOnly {stock} units are available."
        )

        connection.close()
        return

    total = quantity * price

    sale_date = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    cursor.execute("""
        INSERT INTO sales
        (product_id, quantity, total, sale_date)
        VALUES (?, ?, ?, ?)
    """, (
        product_id,
        quantity,
        total,
        sale_date
    ))

    cursor.execute("""
        UPDATE products
        SET stock = stock - ?
        WHERE id = ?
    """, (
        quantity,
        product_id
    ))

    connection.commit()
    connection.close()

    print("\n" + "=" * 40)
    print("SALE COMPLETED")
    print("=" * 40)

    print(f"Product  : {name}")
    print(f"Quantity : {quantity}")
    print(f"Price    : ₹{price:,.2f}")
    print(f"Total    : ₹{total:,.2f}")


# ============================================================
# SALES HISTORY
# ============================================================

def view_sales():

    connection = connect_db()

    query = """
        SELECT
            sales.id AS sale_id,
            products.name AS product,
            products.category AS category,
            sales.quantity AS quantity,
            sales.total AS total,
            sales.sale_date AS date
        FROM sales
        JOIN products
        ON sales.product_id = products.id
        ORDER BY sales.sale_date DESC
    """

    df = pd.read_sql_query(
        query,
        connection
    )

    connection.close()

    if df.empty:

        print("\nNo sales recorded.")
        return df

    print("\n" + "=" * 75)
    print("SALES HISTORY")
    print("=" * 75)

    display_df = df.copy()

    display_df["total"] = (
        display_df["total"]
        .map(lambda x: f"₹{x:,.2f}")
    )

    print(
        display_df.to_string(
            index=False
        )
    )

    return df


# ============================================================
# ANALYTICS
# ============================================================

def sales_summary():

    connection = connect_db()

    query = """
        SELECT
            SUM(total) AS revenue,
            SUM(quantity) AS units_sold,
            COUNT(*) AS transactions
        FROM sales
    """

    result = pd.read_sql_query(
        query,
        connection
    )

    connection.close()

    revenue = result.loc[0, "revenue"]

    units = result.loc[0, "units_sold"]

    transactions = result.loc[0, "transactions"]

    revenue = revenue if pd.notna(revenue) else 0
    units = units if pd.notna(units) else 0
    transactions = (
        transactions
        if pd.notna(transactions)
        else 0
    )

    print("\n" + "=" * 50)
    print("SALES SUMMARY")
    print("=" * 50)

    print(f"Total Revenue     : ₹{revenue:,.2f}")
    print(f"Units Sold        : {int(units)}")
    print(f"Transactions      : {int(transactions)}")

    if transactions > 0:

        print(
            f"Average Sale      : "
            f"₹{revenue / transactions:,.2f}"
        )


def best_selling_products():

    connection = connect_db()

    query = """
        SELECT
            products.name AS product,
            SUM(sales.quantity) AS units_sold,
            SUM(sales.total) AS revenue
        FROM sales
        JOIN products
        ON sales.product_id = products.id
        GROUP BY products.id
        ORDER BY units_sold DESC
    """

    df = pd.read_sql_query(
        query,
        connection
    )

    connection.close()

    if df.empty:

        print("\nNo sales data available.")
        return

    print("\n" + "=" * 60)
    print("BEST-SELLING PRODUCTS")
    print("=" * 60)

    print(
        df.to_string(
            index=False
        )
    )


def category_sales():

    connection = connect_db()

    query = """
        SELECT
            products.category AS category,
            SUM(sales.quantity) AS units_sold,
            SUM(sales.total) AS revenue
        FROM sales
        JOIN products
        ON sales.product_id = products.id
        GROUP BY products.category
        ORDER BY revenue DESC
    """

    df = pd.read_sql_query(
        query,
        connection
    )

    connection.close()

    if df.empty:

        print("\nNo sales data available.")
        return

    print("\n" + "=" * 60)
    print("SALES BY CATEGORY")
    print("=" * 60)

    print(
        df.to_string(
            index=False
        )
    )


def low_stock_report():

    connection = connect_db()

    query = """
        SELECT
            id,
            name,
            category,
            stock
        FROM products
        WHERE stock <= 5
        ORDER BY stock ASC
    """

    df = pd.read_sql_query(
        query,
        connection
    )

    connection.close()

    print("\n" + "=" * 50)
    print("LOW STOCK REPORT")
    print("=" * 50)

    if df.empty:

        print("No products currently have low stock.")
        return

    print(
        df.to_string(
            index=False
        )
    )


# ============================================================
# CHARTS
# ============================================================

def generate_sales_chart():

    connection = connect_db()

    query = """
        SELECT
            products.name AS product,
            SUM(sales.total) AS revenue
        FROM sales
        JOIN products
        ON sales.product_id = products.id
        GROUP BY products.id
        ORDER BY revenue DESC
    """

    df = pd.read_sql_query(
        query,
        connection
    )

    connection.close()

    if df.empty:

        print("\nNo sales data available.")
        return

    plt.figure(figsize=(9, 5))

    plt.bar(
        df["product"],
        df["revenue"]
    )

    plt.title(
        "Revenue by Product"
    )

    plt.xlabel("Product")
    plt.ylabel("Revenue (₹)")

    plt.xticks(
        rotation=45
    )

    plt.tight_layout()

    plt.show()


def generate_category_chart():

    connection = connect_db()

    query = """
        SELECT
            products.category AS category,
            SUM(sales.total) AS revenue
        FROM sales
        JOIN products
        ON sales.product_id = products.id
        GROUP BY products.category
        ORDER BY revenue DESC
    """

    df = pd.read_sql_query(
        query,
        connection
    )

    connection.close()

    if df.empty:

        print("\nNo sales data available.")
        return

    plt.figure(figsize=(8, 8))

    plt.pie(
        df["revenue"],
        labels=df["category"],
        autopct="%1.1f%%"
    )

    plt.title(
        "Revenue Distribution by Category"
    )

    plt.tight_layout()

    plt.show()


# ============================================================
# MENU
# ============================================================

def display_menu():

    print("\n" + "=" * 60)
    print("       INVENTORY & SALES MANAGEMENT")
    print("=" * 60)

    print("1. Add Product")
    print("2. View Inventory")
    print("3. Update Product")
    print("4. Delete Product")
    print("5. Sell Product")
    print("6. View Sales")
    print("7. Sales Summary")
    print("8. Best-Selling Products")
    print("9. Sales by Category")
    print("10. Low Stock Report")
    print("11. Product Revenue Chart")
    print("12. Category Revenue Chart")
    print("13. Exit")

    print("=" * 60)


# ============================================================
# MAIN
# ============================================================

def main():

    initialize_database()

    print("=" * 60)
    print("       INVENTORY & SALES MANAGEMENT")
    print("=" * 60)

    while True:

        display_menu()

        choice = input(
            "Enter your choice: "
        ).strip()

        if choice == "1":

            add_product()

        elif choice == "2":

            view_products()

        elif choice == "3":

            update_product()

        elif choice == "4":

            delete_product()

        elif choice == "5":

            sell_product()

        elif choice == "6":

            view_sales()

        elif choice == "7":

            sales_summary()

        elif choice == "8":

            best_selling_products()

        elif choice == "9":

            category_sales()

        elif choice == "10":

            low_stock_report()

        elif choice == "11":

            generate_sales_chart()

        elif choice == "12":

            generate_category_chart()

        elif choice == "13":

            print(
                "\nThank you for using "
                "Inventory & Sales Management!"
            )

            break

        else:

            print(
                "\nInvalid choice. "
                "Please select 1-13."
            )


if __name__ == "__main__":
    main()