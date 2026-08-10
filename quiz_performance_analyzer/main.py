import json
import random
from pathlib import Path
from datetime import datetime

import pandas as pd
import matplotlib.pyplot as plt


QUESTIONS_FILE = Path("questions.json")
HISTORY_FILE = Path("quiz_history.json")


# ==================================================
# FILE HANDLING
# ==================================================

def load_questions():

    if not QUESTIONS_FILE.exists():
        print("questions.json not found.")
        return []

    try:
        with open(QUESTIONS_FILE, "r") as file:
            return json.load(file)

    except json.JSONDecodeError:
        print("Could not read questions.json.")
        return []


def load_history():

    if not HISTORY_FILE.exists():
        return []

    try:
        with open(HISTORY_FILE, "r") as file:
            return json.load(file)

    except json.JSONDecodeError:
        return []


def save_history(history):

    with open(HISTORY_FILE, "w") as file:
        json.dump(
            history,
            file,
            indent=4
        )


# ==================================================
# QUESTION FILTERING
# ==================================================

def get_categories(questions):

    return sorted(
        set(
            question["category"]
            for question in questions
        )
    )


def get_difficulties(questions):

    return sorted(
        set(
            question["difficulty"]
            for question in questions
        )
    )


def choose_category(questions):

    categories = get_categories(questions)

    print("\nCategories:")

    print("0. All Categories")

    for i, category in enumerate(
        categories,
        start=1
    ):
        print(f"{i}. {category}")

    while True:

        try:
            choice = int(
                input("Choose category: ")
            )

            if choice == 0:
                return None

            if 1 <= choice <= len(categories):
                return categories[choice - 1]

            print("Invalid choice.")

        except ValueError:
            print("Enter a valid number.")


def choose_difficulty(questions):

    difficulties = get_difficulties(questions)

    print("\nDifficulty:")

    print("0. All Difficulties")

    for i, difficulty in enumerate(
        difficulties,
        start=1
    ):
        print(f"{i}. {difficulty}")

    while True:

        try:
            choice = int(
                input("Choose difficulty: ")
            )

            if choice == 0:
                return None

            if 1 <= choice <= len(difficulties):
                return difficulties[choice - 1]

            print("Invalid choice.")

        except ValueError:
            print("Enter a valid number.")


# ==================================================
# QUIZ SETUP
# ==================================================

def choose_question_count(available_count):

    while True:

        try:
            count = int(
                input(
                    f"Number of questions "
                    f"(1-{available_count}): "
                )
            )

            if 1 <= count <= available_count:
                return count

            print("Invalid number.")

        except ValueError:
            print("Enter a valid number.")


def filter_questions(
    questions,
    category=None,
    difficulty=None
):

    filtered = questions

    if category is not None:

        filtered = [
            question
            for question in filtered
            if question["category"] == category
        ]

    if difficulty is not None:

        filtered = [
            question
            for question in filtered
            if question["difficulty"] == difficulty
        ]

    return filtered


# ==================================================
# QUIZ ENGINE
# ==================================================

def ask_question(question, number, total):

    print("\n" + "-" * 60)

    print(
        f"Question {number}/{total}"
    )

    print(
        f"Category: {question['category']} | "
        f"Difficulty: {question['difficulty']}"
    )

    print("\n" + question["question"])

    options = question["options"]

    for i, option in enumerate(
        options,
        start=1
    ):
        print(
            f"{i}. {option}"
        )

    while True:

        try:

            answer = int(
                input("\nYour answer: ")
            )

            if 1 <= answer <= len(options):
                break

            print("Invalid option.")

        except ValueError:

            print(
                "Please enter a number."
            )

    correct_answer = question["answer"]

    selected_answer = options[
        answer - 1
    ]

    is_correct = (
        selected_answer == correct_answer
    )

    if is_correct:
        print("✓ Correct!")

    else:
        print(
            f"✗ Incorrect. "
            f"Correct answer: {correct_answer}"
        )

    return {
        "category": question["category"],
        "difficulty": question["difficulty"],
        "correct": is_correct
    }


def run_quiz(questions):

    category = choose_category(
        questions
    )

    difficulty = choose_difficulty(
        questions
    )

    available_questions = filter_questions(
        questions,
        category,
        difficulty
    )

    if not available_questions:

        print(
            "\nNo questions match "
            "your selection."
        )

        return None

    count = choose_question_count(
        len(available_questions)
    )

    selected_questions = random.sample(
        available_questions,
        count
    )

    print("\n" + "=" * 60)
    print("STARTING QUIZ")
    print("=" * 60)

    results = []

    for number, question in enumerate(
        selected_questions,
        start=1
    ):

        result = ask_question(
            question,
            number,
            count
        )

        results.append(result)

    return results


# ==================================================
# RESULTS
# ==================================================

def calculate_results(results):

    total = len(results)

    correct = sum(
        result["correct"]
        for result in results
    )

    incorrect = total - correct

    accuracy = (
        correct / total * 100
        if total > 0
        else 0
    )

    return {
        "total": total,
        "correct": correct,
        "incorrect": incorrect,
        "accuracy": accuracy
    }


def display_results(results):

    summary = calculate_results(
        results
    )

    print("\n" + "=" * 60)
    print("QUIZ RESULTS")
    print("=" * 60)

    print(
        f"Total Questions : "
        f"{summary['total']}"
    )

    print(
        f"Correct Answers : "
        f"{summary['correct']}"
    )

    print(
        f"Incorrect Answers : "
        f"{summary['incorrect']}"
    )

    print(
        f"Accuracy : "
        f"{summary['accuracy']:.2f}%"
    )

    if summary["accuracy"] >= 90:

        print(
            "\nExcellent performance!"
        )

    elif summary["accuracy"] >= 75:

        print(
            "\nGood performance!"
        )

    elif summary["accuracy"] >= 50:

        print(
            "\nYou passed, but there is "
            "room for improvement."
        )

    else:

        print(
            "\nKeep practicing!"
        )


def category_results(results):

    df = pd.DataFrame(results)

    if df.empty:
        return

    category_stats = (
        df.groupby("category")["correct"]
        .agg(
            [
                "count",
                "sum",
                "mean"
            ]
        )
    )

    category_stats["accuracy"] = (
        category_stats["mean"] * 100
    )

    print("\n" + "=" * 60)
    print("CATEGORY PERFORMANCE")
    print("=" * 60)

    for category, row in category_stats.iterrows():

        print(
            f"{category:<20} "
            f"Accuracy: "
            f"{row['accuracy']:.2f}%"
        )


def difficulty_results(results):

    df = pd.DataFrame(results)

    if df.empty:
        return

    difficulty_stats = (
        df.groupby("difficulty")["correct"]
        .mean()
        * 100
    )

    print("\n" + "=" * 60)
    print("DIFFICULTY PERFORMANCE")
    print("=" * 60)

    for difficulty, accuracy in (
        difficulty_stats.items()
    ):

        print(
            f"{difficulty:<15} "
            f"{accuracy:.2f}%"
        )


# ==================================================
# HISTORY
# ==================================================

def save_attempt(results):

    summary = calculate_results(
        results
    )

    history = load_history()

    attempt = {
        "date": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),
        "total_questions": summary["total"],
        "correct": summary["correct"],
        "incorrect": summary["incorrect"],
        "accuracy": summary["accuracy"],
        "category_results": {},
        "difficulty_results": {}
    }

    df = pd.DataFrame(results)

    category_stats = (
        df.groupby("category")["correct"]
        .mean()
        * 100
    )

    for category, accuracy in (
        category_stats.items()
    ):

        attempt["category_results"][
            category
        ] = accuracy

    difficulty_stats = (
        df.groupby("difficulty")["correct"]
        .mean()
        * 100
    )

    for difficulty, accuracy in (
        difficulty_stats.items()
    ):

        attempt["difficulty_results"][
            difficulty
        ] = accuracy

    history.append(attempt)

    save_history(history)


# ==================================================
# HISTORICAL ANALYSIS
# ==================================================

def show_history():

    history = load_history()

    if not history:

        print(
            "\nNo quiz history available."
        )

        return

    df = pd.DataFrame(history)

    print("\n" + "=" * 60)
    print("QUIZ HISTORY")
    print("=" * 60)

    display_df = df[
        [
            "date",
            "total_questions",
            "correct",
            "accuracy"
        ]
    ].copy()

    display_df["accuracy"] = (
        display_df["accuracy"]
        .round(2)
    )

    print(
        display_df.to_string(
            index=False
        )
    )


def show_overall_performance():

    history = load_history()

    if not history:

        print(
            "\nNo quiz history available."
        )

        return

    df = pd.DataFrame(history)

    average_accuracy = (
        df["accuracy"].mean()
    )

    best_accuracy = (
        df["accuracy"].max()
    )

    total_questions = (
        df["total_questions"].sum()
    )

    total_correct = (
        df["correct"].sum()
    )

    print("\n" + "=" * 60)
    print("OVERALL PERFORMANCE")
    print("=" * 60)

    print(
        f"Quiz Attempts       : {len(df)}"
    )

    print(
        f"Questions Answered  : {total_questions}"
    )

    print(
        f"Correct Answers     : {total_correct}"
    )

    print(
        f"Average Accuracy    : "
        f"{average_accuracy:.2f}%"
    )

    print(
        f"Best Accuracy       : "
        f"{best_accuracy:.2f}%"
    )


# ==================================================
# VISUALIZATION
# ==================================================

def generate_performance_chart():

    history = load_history()

    if len(history) < 2:

        print(
            "\nAt least two quiz attempts "
            "are needed for a performance chart."
        )

        return

    df = pd.DataFrame(history)

    plt.figure(figsize=(9, 5))

    plt.plot(
        range(
            1,
            len(df) + 1
        ),
        df["accuracy"],
        marker="o"
    )

    plt.title(
        "Quiz Accuracy Over Time"
    )

    plt.xlabel("Quiz Attempt")

    plt.ylabel("Accuracy (%)")

    plt.ylim(0, 100)

    plt.grid()

    plt.tight_layout()

    plt.show()


def generate_category_chart():

    history = load_history()

    if not history:

        print(
            "\nNo quiz history available."
        )

        return

    category_scores = {}

    for attempt in history:

        for category, score in (
            attempt["category_results"].items()
        ):

            category_scores.setdefault(
                category,
                []
            )

            category_scores[
                category
            ].append(score)

    averages = {
        category: sum(scores) / len(scores)
        for category, scores
        in category_scores.items()
    }

    if not averages:
        return

    series = pd.Series(
        averages
    ).sort_values(
        ascending=False
    )

    plt.figure(figsize=(9, 5))

    series.plot(
        kind="bar"
    )

    plt.title(
        "Average Accuracy by Category"
    )

    plt.xlabel("Category")

    plt.ylabel("Accuracy (%)")

    plt.ylim(0, 100)

    plt.xticks(
        rotation=45
    )

    plt.tight_layout()

    plt.show()


# ==================================================
# MENU
# ==================================================

def display_menu():

    print("\n" + "=" * 60)
    print("       QUIZ GENERATOR & ANALYZER")
    print("=" * 60)

    print("1. Start Quiz")
    print("2. View Quiz History")
    print("3. View Overall Performance")
    print("4. Accuracy Over Time")
    print("5. Category Performance Chart")
    print("6. Exit")

    print("=" * 60)


# ==================================================
# MAIN
# ==================================================

def main():

    questions = load_questions()

    if not questions:

        print(
            "No questions available."
        )

        return

    while True:

        display_menu()

        choice = input(
            "Enter your choice: "
        ).strip()

        if choice == "1":

            results = run_quiz(
                questions
            )

            if results:

                display_results(
                    results
                )

                category_results(
                    results
                )

                difficulty_results(
                    results
                )

                save_attempt(
                    results
                )

        elif choice == "2":

            show_history()

        elif choice == "3":

            show_overall_performance()

        elif choice == "4":

            generate_performance_chart()

        elif choice == "5":

            generate_category_chart()

        elif choice == "6":

            print(
                "\nThank you for using "
                "Quiz Analyzer!"
            )

            break

        else:

            print(
                "\nInvalid choice."
            )


if __name__ == "__main__":
    main()