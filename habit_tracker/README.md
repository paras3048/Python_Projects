# CLI Habit Tracker & Analytics

A command-line habit tracking application built with Python.

The application allows users to create personal habits, record daily completion, maintain streaks, and analyze their consistency over time.

Habit data is stored locally in a JSON file, while Pandas is used to perform analytics and Matplotlib is used to generate visualizations.

No external dataset, API, or online service is required.

## Features

* Add habits
* Remove habits
* View all habits
* Track daily completion
* Modify today's recorded status
* Calculate overall completion rate
* Calculate completion rate for each habit
* Calculate current streak
* Calculate best streak
* Identify the most consistent habit
* Analyze weekly performance
* Generate habit performance charts
* Persist data using JSON

## Technologies Used

* Python
* Pandas
* Matplotlib
* JSON
* `datetime`
* `pathlib`

## Project Structure

```text
habit-tracker/
│
├── main.py
├── README.md
└── habits.json        # Created automatically
```

`habits.json` does not need to be created manually. The program creates it automatically when data is first saved.

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

The program will display the main menu:

```text
==================================================
           HABIT TRACKER
==================================================
1. Add Habit
2. Remove Habit
3. View Habits
4. Track Today's Habits
5. View Analytics
6. Weekly Analysis
7. Generate Charts
8. Exit
==================================================
```

## How to Use

### 1. Add a Habit

Select:

```text
1. Add Habit
```

Enter a habit such as:

```text
Exercise
```

You can add multiple habits:

```text
Exercise
Read
Study Python
Drink Water
Meditate
```

### 2. Track Today's Habits

Select:

```text
4. Track Today's Habits
```

The application asks whether each habit was completed.

Example:

```text
Did you complete 'Exercise'? (y/n): y

Did you complete 'Read'? (y/n): y

Did you complete 'Study Python'? (y/n): n
```

The record is automatically associated with the current date.

## Analytics

Select:

```text
5. View Analytics
```

The application calculates:

* Overall completion rate
* Habit-specific completion rates
* Current streak
* Best streak
* Most consistent habit

Example:

```text
============================================================
HABIT ANALYTICS
============================================================

Overall completion rate: 78.33%

Completion by Habit:
Exercise                  90.00%
Read                      80.00%
Study Python              75.00%
Meditation                68.00%

Streaks:
Exercise                  Current: 5 days | Best: 12 days
Read                      Current: 3 days | Best: 8 days
Study Python              Current: 2 days | Best: 7 days

Most consistent habit: Exercise
```

## Streak Calculation

A current streak represents consecutive days where a habit was completed.

For example:

```text
Monday     ✓
Tuesday    ✓
Wednesday  ✓
Thursday   ✗
Friday     ✓
```

The first streak is:

```text
3 days
```

The Friday completion starts a new streak.

The program also calculates the **best streak** across all recorded data.

## Weekly Analysis

Select:

```text
6. Weekly Analysis
```

The program groups records by week and calculates the completion percentage.

Example:

```text
==================================================
WEEKLY COMPLETION
==================================================
2026-07-27/2026-08-02     72.50%
2026-08-03/2026-08-09     84.17%
```

## Visualizations

Select:

```text
7. Generate Charts
```

The application generates two charts.

### Habit Completion Rate

Compares the completion percentage of each habit.

### Daily Habit Completion

Shows how overall habit completion changes over time.

## Data Storage

The application automatically creates:

```text
habits.json
```

Example structure:

```json
{
    "habits": [
        "Exercise",
        "Read",
        "Study Python"
    ],
    "records": [
        {
            "date": "2026-08-09",
            "habit": "Exercise",
            "completed": true
        }
    ]
}
```

This means your habit data remains available even after closing the program.

## Program Workflow

```text
Create Habit
     ↓
Store Habit
     ↓
Daily Tracking
     ↓
Save to JSON
     ↓
Load Historical Data
     ↓
Convert to DataFrame
     ↓
Calculate Statistics
     ↓
Calculate Streaks
     ↓
Generate Visualizations
```

## Python Concepts Practiced

This project introduces:

* Functions
* Lists
* Dictionaries
* JSON file handling
* File persistence
* `pathlib`
* `datetime`
* Date arithmetic
* Pandas DataFrames
* `groupby()`
* Boolean data
* Aggregation
* Sorting
* Matplotlib
* Object/data state management
* CRUD-style operations
* Data analysis

## Learning Objective

The goal is to learn how to build an application that maintains information across multiple sessions.

Unlike the previous projects, the application now has **persistent state**:

```text
User
 ↓
Application
 ↓
JSON Storage
 ↓
Historical Data
 ↓
Pandas Analysis
 ↓
Insights
```

This introduces an important concept used in larger applications: **data persistence**.

## Possible Improvements

After completing the basic version, the project can be extended with:

* Habit categories
* Custom start dates
* Habit frequency
* Weekly/monthly goals
* Habit reminders
* Missed-day detection
* Calendar-style visualization
* Monthly reports
* CSV export
* SQLite database
* Tkinter GUI
* Personal productivity score
* Habit correlation analysis
* Longest streak leaderboard