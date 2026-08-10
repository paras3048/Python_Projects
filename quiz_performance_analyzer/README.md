# Quiz Generator & Performance Analyzer

A Python-based command-line quiz application that generates quizzes from a local question bank and analyzes the user's performance over multiple attempts.

The application supports categories, difficulty levels, random question selection, performance tracking, historical analysis, and visualization.

No external dataset, API, or internet connection is required.

## Features

* Randomly generate quizzes
* Select quiz category
* Select difficulty
* Choose number of questions
* Multiple-choice questions
* Automatic score calculation
* Accuracy calculation
* Category-wise performance
* Difficulty-wise performance
* Quiz history
* Average accuracy
* Best accuracy
* Total questions answered
* Accuracy trend visualization
* Category performance visualization
* Persistent history using JSON

## Technologies Used

* Python
* Pandas
* Matplotlib
* JSON
* Random
* `datetime`
* `pathlib`

## Project Structure

```text
quiz-performance-analyzer/
│
├── main.py
├── questions.json
├── requirements.txt
├── README.md
└── quiz_history.json       # Created automatically
```

`quiz_history.json` does not need to be created manually. The program creates it after the first completed quiz.

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

Install the required libraries:

```bash
pip install -r requirements.txt
```

## Running the Project

Run:

```bash
python main.py
```

The application displays:

```text
============================================================
       QUIZ GENERATOR & ANALYZER
============================================================
1. Start Quiz
2. View Quiz History
3. View Overall Performance
4. Accuracy Over Time
5. Category Performance Chart
6. Exit
============================================================
```

## Starting a Quiz

Select:

```text
1. Start Quiz
```

The application asks you to select a category.

Example:

```text
Categories:
0. All Categories
1. Algorithms
2. Data Analysis
3. Python

Choose category: 3
```

You can then select difficulty:

```text
Difficulty:
0. All Difficulties
1. Easy
2. Hard
3. Medium

Choose difficulty: 2
```

Finally, select the number of questions.

```text
Number of questions (1-3): 3
```

The application randomly selects questions matching your choices.

## Quiz Example

```text
------------------------------------------------------------
Question 1/3
Category: Python | Difficulty: Easy

Which keyword is used to define a function in Python?

1. function
2. def
3. func
4. define

Your answer: 2

✓ Correct!
```

The correct answer is displayed when the user answers incorrectly.

## Results

After completing a quiz, the application calculates:

* Total questions
* Correct answers
* Incorrect answers
* Accuracy

Example:

```text
============================================================
QUIZ RESULTS
============================================================
Total Questions : 5
Correct Answers : 4
Incorrect Answers : 1
Accuracy : 80.00%

Good performance!
```

## Category Analysis

The application analyzes how well the user performs in each category.

Example:

```text
============================================================
CATEGORY PERFORMANCE
============================================================
Algorithms           Accuracy: 66.67%
Data Analysis        Accuracy: 100.00%
Python               Accuracy: 80.00%
```

This helps identify areas that need more practice.

## Difficulty Analysis

The application also analyzes performance by difficulty.

Example:

```text
============================================================
DIFFICULTY PERFORMANCE
============================================================
Easy            100.00%
Medium           75.00%
Hard             50.00%
```

## Quiz History

Every completed quiz is stored locally.

Select:

```text
2. View Quiz History
```

Example:

```text
date                 total_questions   correct   accuracy
2026-08-09 10:15:21          5             4       80.00
2026-08-09 10:21:47          5             5      100.00
2026-08-09 10:28:13          5             3       60.00
```

## Overall Performance

Select:

```text
3. View Overall Performance
```

The application calculates:

```text
Quiz Attempts       : 3
Questions Answered  : 15
Correct Answers     : 12
Average Accuracy    : 80.00%
Best Accuracy       : 100.00%
```

## Performance Charts

### Accuracy Over Time

Select:

```text
4. Accuracy Over Time
```

The application plots quiz accuracy across attempts.

This makes it possible to see whether your performance is improving or declining.

### Category Performance

Select:

```text
5. Category Performance Chart
```

The application calculates the average accuracy for each category and generates a bar chart.

## Question Bank

Questions are stored in:

```text
questions.json
```

Each question contains:

```json
{
    "question": "Question text",
    "options": [
        "Option A",
        "Option B",
        "Option C",
        "Option D"
    ],
    "answer": "Correct answer",
    "category": "Python",
    "difficulty": "Easy"
}
```

You can add your own questions by following this structure.

## Data Storage

Quiz history is stored in:

```text
quiz_history.json
```

The file is automatically created after completing the first quiz.

The stored data includes:

* Date and time
* Number of questions
* Correct answers
* Incorrect answers
* Overall accuracy
* Category performance
* Difficulty performance

## Program Workflow

```text
Question Bank
      ↓
Category Selection
      ↓
Difficulty Selection
      ↓
Random Question Selection
      ↓
Quiz
      ↓
Score Calculation
      ↓
Category & Difficulty Analysis
      ↓
Save Attempt
      ↓
Historical Analysis
      ↓
Visualization
```

## Python Concepts Practiced

This project provides practice with:

* Functions
* Lists
* Dictionaries
* JSON
* File handling
* Random selection
* Data validation
* Pandas DataFrames
* `groupby()`
* Aggregation
* Boolean values
* Date and time
* Persistent data
* Matplotlib
* Data visualization

## Learning Objective

The objective is to build a complete application that does more than simply process user input.

The project demonstrates a complete cycle:

```text
Create Data
    ↓
Use Data
    ↓
Store Data
    ↓
Retrieve Data
    ↓
Analyze Data
    ↓
Visualize Data
```

This is an important pattern for larger Python applications.

## Possible Improvements

After completing the project, you can add:

* Question timer
* Negative marking
* Leaderboard
* User profiles
* Question difficulty adaptation
* More question categories
* CSV export
* Question creation through the application
* Question editing and deletion
* SQLite database
* Tkinter GUI
* Detailed per-question history
* Personalized weak-topic recommendations
* Exam mode with a fixed time limit