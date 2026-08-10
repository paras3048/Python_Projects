import json
from pathlib import Path
from datetime import date, timedelta

import pandas as pd
import matplotlib.pyplot as plt


DATA_FILE = Path("habits.json")


# --------------------------------------------------
# DATA MANAGEMENT
# --------------------------------------------------

def load_data():
    """Load habit data from the JSON file."""

    if not DATA_FILE.exists():
        return {
            "habits": [],
            "records": []
        }

    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)

    except json.JSONDecodeError:
        print("Warning: Could not read habits.json.")
        return {
            "habits": [],
            "records": []
        }


def save_data(data):
    """Save habit data to the JSON file."""

    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)


# --------------------------------------------------
# HABIT MANAGEMENT
# --------------------------------------------------

def add_habit(data):

    print("\n" + "=" * 40)
    print("ADD HABIT")
    print("=" * 40)

    name = input("Enter habit name: ").strip()

    if not name:
        print("Habit name cannot be empty.")
        return

    existing = [
        habit.lower()
        for habit in data["habits"]
    ]

    if name.lower() in existing:
        print("This habit already exists.")
        return

    data["habits"].append(name)

    save_data(data)

    print(f"Habit '{name}' added successfully.")


def remove_habit(data):

    if not data["habits"]:
        print("\nNo habits available.")
        return

    print("\nYour Habits:")

    for i, habit in enumerate(
        data["habits"],
        start=1
    ):
        print(f"{i}. {habit}")

    try:
        choice = int(
            input("Enter habit number to remove: ")
        )

        if not 1 <= choice <= len(data["habits"]):
            print("Invalid choice.")
            return

    except ValueError:
        print("Please enter a valid number.")
        return

    habit = data["habits"].pop(choice - 1)

    # Remove records belonging to the habit
    data["records"] = [
        record
        for record in data["records"]
        if record["habit"] != habit
    ]

    save_data(data)

    print(f"Removed habit: {habit}")


def list_habits(data):

    print("\n" + "=" * 40)
    print("YOUR HABITS")
    print("=" * 40)

    if not data["habits"]:
        print("No habits added yet.")
        return

    for i, habit in enumerate(
        data["habits"],
        start=1
    ):
        print(f"{i}. {habit}")


# --------------------------------------------------
# DAILY TRACKING
# --------------------------------------------------

def mark_habits(data):

    if not data["habits"]:
        print("\nAdd some habits first.")
        return

    today = date.today().isoformat()

    print("\n" + "=" * 40)
    print(f"TRACK HABITS — {today}")
    print("=" * 40)

    for habit in data["habits"]:

        existing_record = next(
            (
                record
                for record in data["records"]
                if record["habit"] == habit
                and record["date"] == today
            ),
            None
        )

        if existing_record:
            status = (
                "✓ Done"
                if existing_record["completed"]
                else "✗ Not Done"
            )

            print(
                f"\n{habit} "
                f"[Already recorded: {status}]"
            )

            change = input(
                "Change status? (y/n): "
            ).lower()

            if change != "y":
                continue

            existing_record["completed"] = (
                input(
                    "Completed? (y/n): "
                ).lower() == "y"
            )

        else:

            completed = input(
                f"\nDid you complete '{habit}'? (y/n): "
            ).lower() == "y"

            data["records"].append({
                "date": today,
                "habit": habit,
                "completed": completed
            })

    save_data(data)

    print("\nToday's habits have been recorded.")


# --------------------------------------------------
# ANALYTICS
# --------------------------------------------------

def create_dataframe(data):

    if not data["records"]:
        return pd.DataFrame()

    df = pd.DataFrame(data["records"])

    df["date"] = pd.to_datetime(df["date"])

    df["completed"] = df["completed"].astype(bool)

    return df


def calculate_completion_rates(df):

    if df.empty:
        return pd.Series(dtype=float)

    completion_rates = (
        df.groupby("habit")["completed"]
        .mean()
        .sort_values(
            ascending=False
        )
        * 100
    )

    return completion_rates


def calculate_overall_completion(df):

    if df.empty:
        return 0

    return df["completed"].mean() * 100


def calculate_streak(df, habit):

    habit_df = df[
        df["habit"] == habit
    ].copy()

    if habit_df.empty:
        return 0

    completed_dates = set(
        habit_df.loc[
            habit_df["completed"],
            "date"
        ].dt.date
    )

    current_day = date.today()

    streak = 0

    while current_day in completed_dates:

        streak += 1

        current_day -= timedelta(days=1)

    return streak


def calculate_best_streak(df, habit):

    habit_df = df[
        df["habit"] == habit
    ].copy()

    if habit_df.empty:
        return 0

    completed_dates = sorted(
        set(
            habit_df.loc[
                habit_df["completed"],
                "date"
            ].dt.date
        )
    )

    if not completed_dates:
        return 0

    best_streak = 1
    current_streak = 1

    for i in range(
        1,
        len(completed_dates)
    ):

        difference = (
            completed_dates[i]
            - completed_dates[i - 1]
        ).days

        if difference == 1:
            current_streak += 1
        else:
            current_streak = 1

        best_streak = max(
            best_streak,
            current_streak
        )

    return best_streak


def display_analytics(data):

    df = create_dataframe(data)

    if df.empty:
        print("\nNo tracking data available.")
        return

    print("\n" + "=" * 60)
    print("HABIT ANALYTICS")
    print("=" * 60)

    overall = calculate_overall_completion(df)

    print(
        f"\nOverall completion rate: "
        f"{overall:.2f}%"
    )

    rates = calculate_completion_rates(df)

    print("\nCompletion by Habit:")

    for habit, rate in rates.items():

        print(
            f"{habit:<25} "
            f"{rate:.2f}%"
        )

    print("\nStreaks:")

    for habit in data["habits"]:

        current = calculate_streak(
            df,
            habit
        )

        best = calculate_best_streak(
            df,
            habit
        )

        print(
            f"{habit:<25} "
            f"Current: {current} days | "
            f"Best: {best} days"
        )

    best_habit = rates.idxmax()

    print(
        f"\nMost consistent habit: "
        f"{best_habit}"
    )


# --------------------------------------------------
# WEEKLY ANALYSIS
# --------------------------------------------------

def weekly_analysis(data):

    df = create_dataframe(data)

    if df.empty:
        print("\nNo tracking data available.")
        return

    df["week"] = df["date"].dt.to_period("W").astype(str)

    weekly = (
        df.groupby("week")["completed"]
        .mean()
        * 100
    )

    print("\n" + "=" * 50)
    print("WEEKLY COMPLETION")
    print("=" * 50)

    for week, percentage in weekly.items():

        print(
            f"{week:<25} "
            f"{percentage:.2f}%"
        )


# --------------------------------------------------
# VISUALIZATION
# --------------------------------------------------

def generate_charts(data):

    df = create_dataframe(data)

    if df.empty:
        print("\nNot enough data for charts.")
        return

    rates = calculate_completion_rates(df)

    # Chart 1 — Habit Completion

    plt.figure(figsize=(9, 5))

    rates.plot(
        kind="bar"
    )

    plt.title(
        "Habit Completion Rate"
    )

    plt.xlabel("Habit")
    plt.ylabel("Completion (%)")

    plt.ylim(0, 100)

    plt.xticks(rotation=45)

    plt.tight_layout()

    plt.show()

    # Chart 2 — Daily Completion

    daily = (
        df.groupby("date")["completed"]
        .mean()
        * 100
    )

    plt.figure(figsize=(10, 5))

    daily.plot(
        marker="o"
    )

    plt.title(
        "Daily Habit Completion"
    )

    plt.xlabel("Date")
    plt.ylabel("Completion (%)")

    plt.ylim(0, 100)

    plt.grid()

    plt.tight_layout()

    plt.show()


# --------------------------------------------------
# MENU
# --------------------------------------------------

def display_menu():

    print("\n" + "=" * 50)
    print("           HABIT TRACKER")
    print("=" * 50)

    print("1. Add Habit")
    print("2. Remove Habit")
    print("3. View Habits")
    print("4. Track Today's Habits")
    print("5. View Analytics")
    print("6. Weekly Analysis")
    print("7. Generate Charts")
    print("8. Exit")

    print("=" * 50)


# --------------------------------------------------
# MAIN PROGRAM
# --------------------------------------------------

def main():

    data = load_data()

    print("=" * 50)
    print("        CLI HABIT TRACKER & ANALYTICS")
    print("=" * 50)

    while True:

        display_menu()

        choice = input(
            "Enter your choice: "
        ).strip()

        if choice == "1":

            add_habit(data)

        elif choice == "2":

            remove_habit(data)

        elif choice == "3":

            list_habits(data)

        elif choice == "4":

            mark_habits(data)

        elif choice == "5":

            display_analytics(data)

        elif choice == "6":

            weekly_analysis(data)

        elif choice == "7":

            generate_charts(data)

        elif choice == "8":

            print(
                "\nThank you for using "
                "Habit Tracker!"
            )

            break

        else:

            print(
                "\nInvalid choice. "
                "Please select 1-8."
            )


if __name__ == "__main__":
    main()