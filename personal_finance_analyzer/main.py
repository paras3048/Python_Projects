import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime


CATEGORIES = [
    "Food",
    "Transport",
    "Shopping",
    "Entertainment",
    "Bills",
    "Education",
    "Health",
    "Other"
]

PAYMENT_METHODS = [
    "Cash",
    "UPI",
    "Card",
    "Bank Transfer"
]


def get_date():
    while True:
        date_input = input("Enter date (YYYY-MM-DD): ").strip()

        try:
            date = datetime.strptime(date_input, "%Y-%m-%d")
            return date.strftime("%Y-%m-%d")

        except ValueError:
            print("Invalid date. Please use YYYY-MM-DD.")


def get_amount():
    while True:
        try:
            amount = float(input("Enter amount: ₹"))

            if amount <= 0:
                print("Amount must be greater than 0.")
            else:
                return amount

        except ValueError:
            print("Please enter a valid number.")


def get_transaction_type():
    while True:
        print("\nTransaction Type")
        print("1. Income")
        print("2. Expense")

        choice = input("Choose type: ").strip()

        if choice == "1":
            return "Income"

        elif choice == "2":
            return "Expense"

        else:
            print("Invalid choice.")


def get_category(transaction_type):

    if transaction_type == "Income":
        return "Income"

    print("\nExpense Categories:")

    for i, category in enumerate(CATEGORIES, start=1):
        print(f"{i}. {category}")

    while True:
        try:
            choice = int(input("Choose category: "))

            if 1 <= choice <= len(CATEGORIES):
                return CATEGORIES[choice - 1]

            print("Invalid category.")

        except ValueError:
            print("Please enter a number.")


def get_payment_method():

    print("\nPayment Methods:")

    for i, method in enumerate(PAYMENT_METHODS, start=1):
        print(f"{i}. {method}")

    while True:
        try:
            choice = int(input("Choose payment method: "))

            if 1 <= choice <= len(PAYMENT_METHODS):
                return PAYMENT_METHODS[choice - 1]

            print("Invalid choice.")

        except ValueError:
            print("Please enter a number.")


def add_transactions():

    transactions = []

    print("\n" + "=" * 50)
    print("ADD TRANSACTIONS")
    print("=" * 50)

    while True:

        print("\nEnter transaction details")

        date = get_date()

        transaction_type = get_transaction_type()

        category = get_category(transaction_type)

        amount = get_amount()

        payment_method = get_payment_method()

        description = input("Enter description: ").strip()

        transactions.append({
            "Date": date,
            "Type": transaction_type,
            "Category": category,
            "Amount": amount,
            "Payment Method": payment_method,
            "Description": description
        })

        print("\nTransaction added successfully.")

        while True:
            choice = input(
                "\nAdd another transaction? (y/n): "
            ).lower().strip()

            if choice in ["y", "n"]:
                break

            print("Please enter y or n.")

        if choice == "n":
            break

    return transactions


def create_dataframe(transactions):

    df = pd.DataFrame(transactions)

    if df.empty:
        return df

    df["Date"] = pd.to_datetime(df["Date"])

    df["Month"] = df["Date"].dt.strftime("%Y-%m")

    df["Signed Amount"] = np.where(
        df["Type"] == "Income",
        df["Amount"],
        -df["Amount"]
    )

    return df


def calculate_summary(df):

    total_income = df.loc[
        df["Type"] == "Income",
        "Amount"
    ].sum()

    total_expenses = df.loc[
        df["Type"] == "Expense",
        "Amount"
    ].sum()

    savings = total_income - total_expenses

    if total_income > 0:
        savings_rate = (savings / total_income) * 100
    else:
        savings_rate = 0

    return (
        total_income,
        total_expenses,
        savings,
        savings_rate
    )


def display_summary(df):

    total_income, total_expenses, savings, savings_rate = (
        calculate_summary(df)
    )

    print("\n" + "=" * 50)
    print("FINANCIAL SUMMARY")
    print("=" * 50)

    print(f"Total Income     : ₹{total_income:,.2f}")
    print(f"Total Expenses   : ₹{total_expenses:,.2f}")
    print(f"Savings          : ₹{savings:,.2f}")
    print(f"Savings Rate     : {savings_rate:.2f}%")

    if savings > 0:
        print("Financial Status : Surplus")

    elif savings < 0:
        print("Financial Status : Deficit")

    else:
        print("Financial Status : Break-even")


def display_expense_analysis(df):

    expenses = df[df["Type"] == "Expense"]

    if expenses.empty:
        print("\nNo expenses found.")
        return

    category_totals = (
        expenses
        .groupby("Category")["Amount"]
        .sum()
        .sort_values(ascending=False)
    )

    print("\n" + "=" * 50)
    print("EXPENSE BY CATEGORY")
    print("=" * 50)

    for category, amount in category_totals.items():
        print(f"{category:<20} ₹{amount:,.2f}")

    highest_category = category_totals.idxmax()

    print(
        f"\nHighest spending category: "
        f"{highest_category}"
    )


def display_payment_analysis(df):

    expenses = df[df["Type"] == "Expense"]

    if expenses.empty:
        return

    payment_totals = (
        expenses
        .groupby("Payment Method")["Amount"]
        .sum()
        .sort_values(ascending=False)
    )

    print("\n" + "=" * 50)
    print("EXPENSE BY PAYMENT METHOD")
    print("=" * 50)

    for method, amount in payment_totals.items():
        print(f"{method:<20} ₹{amount:,.2f}")


def display_monthly_analysis(df):

    monthly = (
        df.groupby(["Month", "Type"])["Amount"]
        .sum()
        .unstack(fill_value=0)
    )

    if "Income" not in monthly:
        monthly["Income"] = 0

    if "Expense" not in monthly:
        monthly["Expense"] = 0

    monthly["Savings"] = (
        monthly["Income"] - monthly["Expense"]
    )

    print("\n" + "=" * 65)
    print("MONTHLY ANALYSIS")
    print("=" * 65)

    print(
        monthly[
            ["Income", "Expense", "Savings"]
        ].to_string()
    )


def display_largest_expense(df):

    expenses = df[df["Type"] == "Expense"]

    if expenses.empty:
        return

    largest_index = expenses["Amount"].idxmax()

    largest = expenses.loc[largest_index]

    print("\n" + "=" * 50)
    print("LARGEST EXPENSE")
    print("=" * 50)

    print(f"Date        : {largest['Date'].date()}")
    print(f"Category    : {largest['Category']}")
    print(f"Amount      : ₹{largest['Amount']:,.2f}")
    print(f"Description : {largest['Description']}")


def generate_charts(df):

    expenses = df[df["Type"] == "Expense"]

    if expenses.empty:
        print("\nNot enough expense data for charts.")
        return

    # Chart 1: Expense by category

    category_totals = (
        expenses
        .groupby("Category")["Amount"]
        .sum()
        .sort_values(ascending=False)
    )

    plt.figure(figsize=(9, 5))

    category_totals.plot(kind="bar")

    plt.title("Expenses by Category")
    plt.xlabel("Category")
    plt.ylabel("Amount (₹)")
    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.show()

    # Chart 2: Monthly income vs expenses

    monthly = (
        df.groupby(["Month", "Type"])["Amount"]
        .sum()
        .unstack(fill_value=0)
    )

    monthly.plot(
        kind="bar",
        figsize=(9, 5)
    )

    plt.title("Monthly Income vs Expenses")
    plt.xlabel("Month")
    plt.ylabel("Amount (₹)")
    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.show()

    # Chart 3: Expense distribution

    plt.figure(figsize=(7, 7))

    category_totals.plot(
        kind="pie",
        autopct="%1.1f%%"
    )

    plt.title("Expense Distribution")
    plt.ylabel("")

    plt.tight_layout()
    plt.show()


def save_report(df):

    output_file = "finance_report.csv"

    df.to_csv(output_file, index=False)

    print(
        f"\nFinancial report saved as "
        f"'{output_file}'."
    )


def main():

    print("=" * 60)
    print("          PERSONAL FINANCE ANALYZER")
    print("=" * 60)

    transactions = add_transactions()

    if not transactions:
        print("\nNo transactions entered.")
        return

    df = create_dataframe(transactions)

    display_summary(df)

    display_expense_analysis(df)

    display_payment_analysis(df)

    display_monthly_analysis(df)

    display_largest_expense(df)

    save_report(df)

    print("\nGenerating financial charts...")

    generate_charts(df)

    print("\nAnalysis completed successfully.")


if __name__ == "__main__":
    main()