import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


SUBJECTS = ["Maths", "Physics", "Computer Science"]


def get_student_data():
    students = []

    print("\nEnter student details")
    print("-" * 40)

    while True:
        name = input("\nEnter student name (or 'done' to finish): ").strip()

        if name.lower() == "done":
            break

        if not name:
            print("Name cannot be empty.")
            continue

        marks = {}

        for subject in SUBJECTS:
            while True:
                try:
                    mark = float(input(f"Enter marks for {subject}: "))

                    if 0 <= mark <= 100:
                        marks[subject] = mark
                        break

                    print("Marks must be between 0 and 100.")

                except ValueError:
                    print("Please enter a valid number.")

        students.append({
            "Name": name,
            **marks
        })

    return students


def create_dataframe(students):
    df = pd.DataFrame(students)

    if df.empty:
        return df

    df["Total"] = df[SUBJECTS].sum(axis=1)
    df["Average"] = df[SUBJECTS].mean(axis=1)

    df["Percentage"] = df["Average"]

    df["Grade"] = df["Percentage"].apply(assign_grade)

    df["Result"] = np.where(
        df[SUBJECTS].min(axis=1) >= 40,
        "Pass",
        "Fail"
    )

    return df


def assign_grade(percentage):
    if percentage >= 90:
        return "A+"
    elif percentage >= 80:
        return "A"
    elif percentage >= 70:
        return "B"
    elif percentage >= 60:
        return "C"
    elif percentage >= 50:
        return "D"
    elif percentage >= 40:
        return "E"
    else:
        return "F"


def display_student_data(df):
    print("\n" + "=" * 80)
    print("STUDENT PERFORMANCE")
    print("=" * 80)

    print(
        df[
            [
                "Name",
                "Maths",
                "Physics",
                "Computer Science",
                "Total",
                "Average",
                "Grade",
                "Result"
            ]
        ].to_string(index=False)
    )


def display_statistics(df):
    print("\n" + "=" * 50)
    print("CLASS STATISTICS")
    print("=" * 50)

    print(f"Number of students : {len(df)}")

    print(
        f"Class average      : "
        f"{df['Average'].mean():.2f}"
    )

    print(
        f"Highest average    : "
        f"{df['Average'].max():.2f}"
    )

    print(
        f"Lowest average     : "
        f"{df['Average'].min():.2f}"
    )

    pass_count = (df["Result"] == "Pass").sum()
    fail_count = (df["Result"] == "Fail").sum()

    print(f"Students passed    : {pass_count}")
    print(f"Students failed    : {fail_count}")

    if len(df) > 0:
        pass_percentage = (pass_count / len(df)) * 100
        print(f"Pass percentage    : {pass_percentage:.2f}%")


def display_subject_statistics(df):
    print("\n" + "=" * 50)
    print("SUBJECT STATISTICS")
    print("=" * 50)

    for subject in SUBJECTS:
        print(
            f"{subject:<20} "
            f"Average: {df[subject].mean():.2f} | "
            f"Highest: {df[subject].max():.2f} | "
            f"Lowest: {df[subject].min():.2f}"
        )


def display_topper(df):
    topper_index = df["Average"].idxmax()
    topper = df.loc[topper_index]

    print("\n" + "=" * 50)
    print("CLASS TOPPER")
    print("=" * 50)

    print(f"Name       : {topper['Name']}")
    print(f"Average    : {topper['Average']:.2f}")
    print(f"Percentage : {topper['Percentage']:.2f}%")
    print(f"Grade      : {topper['Grade']}")


def display_subject_performance(df):
    averages = df[SUBJECTS].mean()

    best_subject = averages.idxmax()
    weakest_subject = averages.idxmin()

    print("\n" + "=" * 50)
    print("SUBJECT PERFORMANCE")
    print("=" * 50)

    print(f"Best subject    : {best_subject}")
    print(f"Class average   : {averages[best_subject]:.2f}")

    print(f"\nWeakest subject : {weakest_subject}")
    print(f"Class average   : {averages[weakest_subject]:.2f}")


def show_grade_distribution(df):
    grade_counts = df["Grade"].value_counts().sort_index()

    print("\n" + "=" * 50)
    print("GRADE DISTRIBUTION")
    print("=" * 50)

    for grade, count in grade_counts.items():
        print(f"Grade {grade}: {'*' * count} ({count})")


def generate_charts(df):
    # Chart 1: Subject averages

    subject_averages = df[SUBJECTS].mean()

    plt.figure(figsize=(8, 5))

    subject_averages.plot(kind="bar")

    plt.title("Average Marks by Subject")
    plt.xlabel("Subject")
    plt.ylabel("Average Marks")
    plt.ylim(0, 100)
    plt.tight_layout()

    plt.show()

    # Chart 2: Student averages

    plt.figure(figsize=(9, 5))

    plt.bar(df["Name"], df["Average"])

    plt.title("Student Average Performance")
    plt.xlabel("Student")
    plt.ylabel("Average Marks")
    plt.ylim(0, 100)

    plt.xticks(rotation=45)

    plt.tight_layout()

    plt.show()

    # Chart 3: Grade distribution

    grade_counts = df["Grade"].value_counts()

    plt.figure(figsize=(7, 5))

    plt.pie(
        grade_counts.values,
        labels=grade_counts.index,
        autopct="%1.1f%%"
    )

    plt.title("Grade Distribution")

    plt.show()


def save_report(df):
    filename = "student_performance.csv"

    df.to_csv(filename, index=False)

    print(f"\nReport saved as '{filename}'.")


def main():

    print("=" * 60)
    print("       STUDENT PERFORMANCE ANALYTICS SYSTEM")
    print("=" * 60)

    students = get_student_data()

    if not students:
        print("\nNo student data entered.")
        return

    df = create_dataframe(students)

    display_student_data(df)

    display_statistics(df)

    display_subject_statistics(df)

    display_topper(df)

    display_subject_performance(df)

    show_grade_distribution(df)

    save_report(df)

    print("\nGenerating charts...")

    generate_charts(df)

    print("\nAnalysis completed successfully.")


if __name__ == "__main__":
    main()