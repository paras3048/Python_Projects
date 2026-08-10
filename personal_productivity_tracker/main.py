import json
from pathlib import Path
from datetime import datetime, timedelta

import pandas as pd
import matplotlib.pyplot as plt


DATA_FILE = Path("productivity.json")

ACTIVITY_TYPES = [
    "Study",
    "Work",
    "Project",
    "Exercise",
    "Reading",
    "Personal",
    "Other"
]

PRODUCTIVITY_LEVELS = {
    1: "Low",
    2: "Medium",
    3: "High"
}


# ============================================================
# DATA STORAGE
# ============================================================

def load_data():
    """Load productivity records from JSON."""

    if not DATA_FILE.exists():
        return []

    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)

    except json.JSONDecodeError:
        print("Could not read productivity.json.")
        return []


def save_data(records):
    """Save productivity records to JSON."""

    with open(DATA_FILE, "w") as file:
        json.dump(records, file, indent=4)


# ============================================================
# INPUT FUNCTIONS
# ============================================================

def get_date():
    """Get a valid date from the user."""

    while True:

        value = input(
            "Enter date (YYYY-MM-DD): "
        ).strip()

        try:

            datetime.strptime(
                value,
                "%Y-%m-%d"
            )

            return value

        except ValueError:

            print(
                "Invalid date. "
                "Use YYYY-MM-DD."
            )


def get_duration():
    """Get activity duration in minutes."""

    while True:

        try:

            minutes = float(
                input(
                    "Duration (minutes): "
                )
            )

            if minutes > 0:
                return minutes

            print(
                "Duration must be greater than 0."
            )

        except ValueError:

            print(
                "Please enter a valid number."
            )


def choose_activity_type():

    print("\nActivity Types:")

    for i, activity in enumerate(
        ACTIVITY_TYPES,
        start=1
    ):
        print(
            f"{i}. {activity}"
        )

    while True:

        try:

            choice = int(
                input(
                    "Choose activity type: "
                )
            )

            if 1 <= choice <= len(ACTIVITY_TYPES):

                return ACTIVITY_TYPES[
                    choice - 1
                ]

            print("Invalid choice.")

        except ValueError:

            print(
                "Please enter a valid number."
            )


def choose_productivity_level():

    print("\nProductivity Level:")

    for number, level in PRODUCTIVITY_LEVELS.items():

        print(
            f"{number}. {level}"
        )

    while True:

        try:

            choice = int(
                input(
                    "Choose productivity level: "
                )
            )

            if choice in PRODUCTIVITY_LEVELS:

                return PRODUCTIVITY_LEVELS[
                    choice
                ]

            print("Invalid choice.")

        except ValueError:

            print(
                "Please enter a valid number."
            )


# ============================================================
# RECORD ACTIVITIES
# ============================================================

def add_activity(records):

    print("\n" + "=" * 55)
    print("ADD PRODUCTIVITY RECORD")
    print("=" * 55)

    activity_date = get_date()

    activity_type = choose_activity_type()

    duration = get_duration()

    productivity = choose_productivity_level()

    description = input(
        "Description: "
    ).strip()

    record = {
        "date": activity_date,
        "activity": activity_type,
        "duration_minutes": duration,
        "productivity": productivity,
        "description": description
    }

    records.append(record)

    save_data(records)

    print(
        "\nActivity recorded successfully."
    )


def view_records(records):

    if not records:

        print(
            "\nNo productivity records found."
        )

        return

    df = create_dataframe(records)

    display_df = df[
        [
            "date",
            "activity",
            "duration_minutes",
            "productivity",
            "description"
        ]
    ].copy()

    display_df["duration_minutes"] = (
        display_df["duration_minutes"]
        .round(1)
    )

    print("\n" + "=" * 90)
    print("PRODUCTIVITY RECORDS")
    print("=" * 90)

    print(
        display_df.to_string(
            index=False
        )
    )


# ============================================================
# DATAFRAME
# ============================================================

def create_dataframe(records):

    if not records:

        return pd.DataFrame()

    df = pd.DataFrame(records)

    df["date"] = pd.to_datetime(
        df["date"]
    )

    # Convert productivity level
    # into a numerical score.

    productivity_scores = {
        "Low": 1,
        "Medium": 2,
        "High": 3
    }

    df["productivity_score"] = (
        df["productivity"]
        .map(productivity_scores)
    )

    df["productive_minutes"] = (
        df["duration_minutes"]
        * df["productivity_score"]
        / 3
    )

    return df


# ============================================================
# BASIC ANALYTICS
# ============================================================

def overall_summary(records):

    df = create_dataframe(records)

    if df.empty:

        print(
            "\nNo data available."
        )

        return

    total_minutes = (
        df["duration_minutes"].sum()
    )

    total_hours = (
        total_minutes / 60
    )

    productive_minutes = (
        df["productive_minutes"].sum()
    )

    average_productivity = (
        df["productivity_score"].mean()
    )

    activity_count = len(df)

    print("\n" + "=" * 55)
    print("OVERALL PRODUCTIVITY")
    print("=" * 55)

    print(
        f"Activities recorded : "
        f"{activity_count}"
    )

    print(
        f"Total time          : "
        f"{total_hours:.2f} hours"
    )

    print(
        f"Productive time     : "
        f"{productive_minutes / 60:.2f} hours"
    )

    print(
        f"Average productivity: "
        f"{average_productivity:.2f}/3"
    )


def activity_analysis(records):

    df = create_dataframe(records)

    if df.empty:
        return

    activity_stats = (
        df.groupby("activity")
        .agg(
            sessions=(
                "activity",
                "count"
            ),
            total_minutes=(
                "duration_minutes",
                "sum"
            ),
            productive_minutes=(
                "productive_minutes",
                "sum"
            ),
            average_productivity=(
                "productivity_score",
                "mean"
            )
        )
        .sort_values(
            "total_minutes",
            ascending=False
        )
    )

    print("\n" + "=" * 80)
    print("ACTIVITY ANALYSIS")
    print("=" * 80)

    print(
        activity_stats.round(2).to_string()
    )

    if not activity_stats.empty:

        most_time = (
            activity_stats[
                "total_minutes"
            ].idxmax()
        )

        most_productive = (
            activity_stats[
                "average_productivity"
            ].idxmax()
        )

        print(
            f"\nMost time spent on    : "
            f"{most_time}"
        )

        print(
            f"Most productive type  : "
            f"{most_productive}"
        )


# ============================================================
# DAILY ANALYSIS
# ============================================================

def daily_analysis(records):

    df = create_dataframe(records)

    if df.empty:
        return

    daily = (
        df.groupby("date")
        .agg(
            total_minutes=(
                "duration_minutes",
                "sum"
            ),
            productive_minutes=(
                "productive_minutes",
                "sum"
            ),
            average_productivity=(
                "productivity_score",
                "mean"
            ),
            sessions=(
                "activity",
                "count"
            )
        )
        .sort_index()
    )

    print("\n" + "=" * 80)
    print("DAILY PRODUCTIVITY")
    print("=" * 80)

    display_daily = daily.copy()

    display_daily[
        "total_hours"
    ] = (
        display_daily["total_minutes"]
        / 60
    )

    display_daily[
        "productive_hours"
    ] = (
        display_daily["productive_minutes"]
        / 60
    )

    print(
        display_daily[
            [
                "total_hours",
                "productive_hours",
                "average_productivity",
                "sessions"
            ]
        ]
        .round(2)
        .to_string()
    )


# ============================================================
# WEEKLY ANALYSIS
# ============================================================

def weekly_analysis(records):

    df = create_dataframe(records)

    if df.empty:
        return

    df["week"] = (
        df["date"]
        .dt
        .to_period("W")
        .astype(str)
    )

    weekly = (
        df.groupby("week")
        .agg(
            total_minutes=(
                "duration_minutes",
                "sum"
            ),
            productive_minutes=(
                "productive_minutes",
                "sum"
            ),
            average_productivity=(
                "productivity_score",
                "mean"
            ),
            sessions=(
                "activity",
                "count"
            )
        )
    )

    weekly["total_hours"] = (
        weekly["total_minutes"] / 60
    )

    weekly["productive_hours"] = (
        weekly["productive_minutes"] / 60
    )

    print("\n" + "=" * 90)
    print("WEEKLY PRODUCTIVITY")
    print("=" * 90)

    print(
        weekly[
            [
                "total_hours",
                "productive_hours",
                "average_productivity",
                "sessions"
            ]
        ]
        .round(2)
        .to_string()
    )


# ============================================================
# BEST DAY
# ============================================================

def best_day(records):

    df = create_dataframe(records)

    if df.empty:
        return

    daily = (
        df.groupby("date")[
            "productive_minutes"
        ]
        .sum()
        .sort_values(
            ascending=False
        )
    )

    best_date = daily.index[0]

    best_minutes = daily.iloc[0]

    print("\n" + "=" * 55)
    print("BEST PRODUCTIVITY DAY")
    print("=" * 55)

    print(
        f"Date            : "
        f"{best_date.date()}"
    )

    print(
        f"Productive time : "
        f"{best_minutes / 60:.2f} hours"
    )


# ============================================================
# MOST PRODUCTIVE PERIOD
# ============================================================

def productivity_distribution(records):

    df = create_dataframe(records)

    if df.empty:
        return

    distribution = (
        df["productivity"]
        .value_counts()
    )

    print("\n" + "=" * 55)
    print("PRODUCTIVITY DISTRIBUTION")
    print("=" * 55)

    for level in [
        "High",
        "Medium",
        "Low"
    ]:

        count = distribution.get(
            level,
            0
        )

        print(
            f"{level:<10}: {count}"
        )


# ============================================================
# CHARTS
# ============================================================

def generate_activity_chart(records):

    df = create_dataframe(records)

    if df.empty:

        print(
            "\nNo data available."
        )

        return

    activity_hours = (
        df.groupby("activity")[
            "duration_minutes"
        ]
        .sum()
        / 60
    )

    activity_hours = (
        activity_hours
        .sort_values(
            ascending=False
        )
    )

    plt.figure(
        figsize=(9, 5)
    )

    activity_hours.plot(
        kind="bar"
    )

    plt.title(
        "Time Spent by Activity"
    )

    plt.xlabel(
        "Activity"
    )

    plt.ylabel(
        "Hours"
    )

    plt.xticks(
        rotation=45
    )

    plt.tight_layout()

    plt.show()


def generate_daily_chart(records):

    df = create_dataframe(records)

    if df.empty:
        return

    daily = (
        df.groupby("date")[
            "productive_minutes"
        ]
        .sum()
        / 60
    )

    plt.figure(
        figsize=(10, 5)
    )

    daily.plot(
        marker="o"
    )

    plt.title(
        "Productive Hours Over Time"
    )

    plt.xlabel(
        "Date"
    )

    plt.ylabel(
        "Productive Hours"
    )

    plt.grid()

    plt.tight_layout()

    plt.show()


def generate_productivity_chart(records):

    df = create_dataframe(records)

    if df.empty:
        return

    distribution = (
        df["productivity"]
        .value_counts()
        .reindex(
            [
                "Low",
                "Medium",
                "High"
            ],
            fill_value=0
        )
    )

    plt.figure(
        figsize=(7, 7)
    )

    distribution.plot(
        kind="pie",
        autopct="%1.1f%%"
    )

    plt.title(
        "Productivity Level Distribution"
    )

    plt.ylabel("")

    plt.tight_layout()

    plt.show()


# ============================================================
# EXPORT
# ============================================================

def export_report(records):

    df = create_dataframe(records)

    if df.empty:

        print(
            "\nNo data to export."
        )

        return

    output_file = (
        "productivity_report.csv"
    )

    export_df = df.copy()

    export_df["date"] = (
        export_df["date"]
        .dt
        .strftime("%Y-%m-%d")
    )

    export_df.to_csv(
        output_file,
        index=False
    )

    print(
        f"\nReport saved as "
        f"'{output_file}'."
    )


# ============================================================
# MENU
# ============================================================

def display_menu():

    print("\n" + "=" * 60)
    print("       PERSONAL PRODUCTIVITY ANALYZER")
    print("=" * 60)

    print("1. Add Activity")
    print("2. View Records")
    print("3. Overall Summary")
    print("4. Activity Analysis")
    print("5. Daily Analysis")
    print("6. Weekly Analysis")
    print("7. Best Productivity Day")
    print("8. Productivity Distribution")
    print("9. Activity Time Chart")
    print("10. Productive Hours Chart")
    print("11. Productivity Level Chart")
    print("12. Export CSV Report")
    print("13. Exit")

    print("=" * 60)


# ============================================================
# MAIN
# ============================================================

def main():

    records = load_data()

    print("=" * 60)
    print("       PERSONAL PRODUCTIVITY ANALYZER")
    print("=" * 60)

    while True:

        display_menu()

        choice = input(
            "Enter your choice: "
        ).strip()

        if choice == "1":

            add_activity(
                records
            )

        elif choice == "2":

            view_records(
                records
            )

        elif choice == "3":

            overall_summary(
                records
            )

        elif choice == "4":

            activity_analysis(
                records
            )

        elif choice == "5":

            daily_analysis(
                records
            )

        elif choice == "6":

            weekly_analysis(
                records
            )

        elif choice == "7":

            best_day(
                records
            )

        elif choice == "8":

            productivity_distribution(
                records
            )

        elif choice == "9":

            generate_activity_chart(
                records
            )

        elif choice == "10":

            generate_daily_chart(
                records
            )

        elif choice == "11":

            generate_productivity_chart(
                records
            )

        elif choice == "12":

            export_report(
                records
            )

        elif choice == "13":

            print(
                "\nThank you for using "
                "Personal Productivity Analyzer!"
            )

            break

        else:

            print(
                "\nInvalid choice. "
                "Please select 1-13."
            )


if __name__ == "__main__":
    main()