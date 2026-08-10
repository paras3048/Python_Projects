# Personal Productivity Analyzer

A command-line productivity tracking and analytics application built with Python.

The application allows users to record activities, track the amount of time spent on different tasks, assign productivity levels, and analyze their productivity over time.

The project stores data locally using JSON and uses Pandas and Matplotlib for analysis and visualization.

No external dataset, API, or online service is required.

## Features

### Activity Tracking

* Record activities
* Select activity category
* Record duration
* Assign productivity level
* Add descriptions
* Store records permanently

### Analytics

* Total time spent
* Total productive time
* Average productivity
* Activity-wise time analysis
* Daily productivity
* Weekly productivity
* Best productivity day
* Productivity distribution
* Most time-consuming activity
* Most productive activity type

### Visualization

* Time spent by activity
* Productive hours over time
* Productivity level distribution

### Export

* Export processed data to CSV

## Technologies Used

* Python
* Pandas
* Matplotlib
* JSON
* `datetime`
* `pathlib`

## Project Structure

```text
personal-productivity-analyzer/
│
├── main.py
├── requirements.txt
├── README.md
├── productivity.json          # Created automatically
└── productivity_report.csv    # Created when exported
```

The JSON and CSV files do not need to be created manually.

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
       PERSONAL PRODUCTIVITY ANALYZER
============================================================
1. Add Activity
2. View Records
3. Overall Summary
4. Activity Analysis
5. Daily Analysis
6. Weekly Analysis
7. Best Productivity Day
8. Productivity Distribution
9. Activity Time Chart
10. Productive Hours Chart
11. Productivity Level Chart
12. Export CSV Report
13. Exit
============================================================
```

# Adding an Activity

Select:

```text
1. Add Activity
```

The program asks for:

```text
Date
Activity type
Duration
Productivity level
Description
```

Example:

```text
Enter date (YYYY-MM-DD): 2026-08-09

Activity Types:
1. Study
2. Work
3. Project
4. Exercise
5. Reading
6. Personal
7. Other

Choose activity type: 3

Duration (minutes): 120

Productivity Level:
1. Low
2. Medium
3. High

Choose productivity level: 3

Description: Worked on Python project
```

The record is then saved locally.

## Productivity Levels

The application uses three levels:

| Level  | Score |
| ------ | ----: |
| Low    |     1 |
| Medium |     2 |
| High   |     3 |

The numerical score allows the application to perform quantitative analysis.

## Productive Time

The application calculates weighted productive time.

The basic calculation is:

```text
Productive Time =
Duration × Productivity Score / 3
```

For example:

```text
Duration = 120 minutes
Productivity = High = 3

Productive Time =
120 × 3 / 3

= 120 minutes
```

For medium productivity:

```text
Duration = 120 minutes
Productivity = Medium = 2

Productive Time =
120 × 2 / 3

= 80 minutes
```

This gives a simple way to distinguish between time spent and effective time spent.

# Overall Summary

Select:

```text
3. Overall Summary
```

The application calculates:

```text
=======================================================
OVERALL PRODUCTIVITY
=======================================================
Activities recorded : 25
Total time          : 32.50 hours
Productive time     : 24.75 hours
Average productivity: 2.28/3
```

## Activity Analysis

Select:

```text
4. Activity Analysis
```

The program groups activities and calculates:

* Number of sessions
* Total time
* Productive time
* Average productivity

Example:

```text
activity       sessions   total_minutes   productive_minutes
Study               12          840.00               700.00
Project              8          620.00               550.00
Exercise             5          300.00               220.00
Reading              6          280.00               210.00
```

It also identifies:

```text
Most time spent on   : Study
Most productive type : Project
```

## Daily Analysis

Select:

```text
5. Daily Analysis
```

The program groups activities by date.

Example:

```text
date         total_hours   productive_hours   average_productivity   sessions
2026-08-07        5.50              4.20                 2.30          5
2026-08-08        7.25              5.80                 2.40          7
2026-08-09        4.00              2.75                 2.06          4
```

This allows you to compare productivity across days.

## Weekly Analysis

Select:

```text
6. Weekly Analysis
```

The program groups records into calendar weeks.

Example:

```text
week                  total_hours   productive_hours   average_productivity
2026-08-03/2026-08-09      32.50              24.75                 2.28
```

This is useful for identifying longer-term productivity patterns.

## Best Productivity Day

Select:

```text
7. Best Productivity Day
```

The application finds the date with the highest amount of productive time.

Example:

```text
=======================================================
BEST PRODUCTIVITY DAY
=======================================================
Date            : 2026-08-08
Productive time : 5.80 hours
```

## Productivity Distribution

Select:

```text
8. Productivity Distribution
```

The application shows how many sessions were classified as Low, Medium, or High productivity.

Example:

```text
High      : 12
Medium    : 9
Low       : 4
```

## Visualizations

The application provides three charts.

### 1. Time Spent by Activity

Shows how many hours were spent on each activity category.

### 2. Productive Hours Over Time

Shows how productive hours change across different dates.

### 3. Productivity Level Distribution

Shows the percentage of sessions classified as Low, Medium, or High productivity.

## Data Storage

The application automatically creates:

```text
productivity.json
```

Example:

```json
[
    {
        "date": "2026-08-09",
        "activity": "Project",
        "duration_minutes": 120,
        "productivity": "High",
        "description": "Worked on Python project"
    }
]
```

This means the data persists after the program is closed.

## CSV Export

Select:

```text
12. Export CSV Report
```

The application creates:

```text
productivity_report.csv
```

The exported dataset contains:

```text
date
activity
duration_minutes
productivity
description
productivity_score
productive_minutes
```

The CSV can later be opened in Excel or analyzed with another Python program.

## Program Workflow

```text
Record Activity
       ↓
Store in JSON
       ↓
Load Historical Data
       ↓
Create Pandas DataFrame
       ↓
Transform Time & Productivity
       ↓
Daily / Weekly Analysis
       ↓
Activity Analysis
       ↓
Generate Visualizations
       ↓
Export Report
```

## Python Concepts Practiced

This project introduces:

* Functions
* Lists
* Dictionaries
* JSON persistence
* File handling
* `pathlib`
* `datetime`
* Date conversion
* Date grouping
* Pandas DataFrames
* `groupby()`
* Aggregation
* Data transformation
* Mapping categorical values
* Time-series analysis
* Matplotlib
* CSV export

## Learning Objective

The objective is to understand how Python can transform simple activity records into measurable insights.

The project follows a common data-analysis workflow:

```text
Raw Data
   ↓
Cleaning
   ↓
Transformation
   ↓
Aggregation
   ↓
Analysis
   ↓
Visualization
```

It also demonstrates an important distinction between:

```text
Time Spent
     vs.
Effective / Productive Time
```

The application uses a simple productivity score to demonstrate how qualitative information can be converted into a numerical metric.

## Possible Improvements

After completing the basic version, you can extend the project with:

* Start and end times instead of manually entering duration
* Automatic duration calculation
* Break tracking
* Daily productivity goals
* Weekly targets
* Productivity score out of 100
* Focus-session tracking
* Pomodoro mode
* Comparison between planned and actual time
* Calendar heatmap
* Monthly reports
* Productivity trends
* Activity search and filtering
* SQLite database
* Tkinter GUI
* Interactive Plotly dashboard
* Automatic weekly productivity report