# Typing Speed & Accuracy Tester

A desktop application built with Python that measures typing speed and accuracy.

The application generates text internally and allows the user to type the displayed text. After the test, it calculates typing speed, accuracy, elapsed time, character count, and typing errors.

No external dataset, API, internet connection, or external Python library is required.

## Features

* Graphical user interface
* Three difficulty levels:

  * Easy
  * Medium
  * Hard
* Random text generation
* Real-time timer
* Words Per Minute (WPM) calculation
* Typing accuracy calculation
* Character count
* Error detection
* Test reset functionality
* Result display
* Multiple typing sessions during one application run

## Technologies Used

* Python
* Tkinter
* Random
* Time

All libraries used by the project are part of Python's standard library.

## Project Structure

```text
typing-speed-tester/
│
├── main.py
├── requirements.txt
└── README.md
```

## Requirements

* Python 3.x
* Tkinter

Tkinter is included with most standard Python installations.

No `pip install` command is required.

## Running the Project

Open the project directory in a terminal and run:

```bash
python main.py
```

The application window will open automatically.

## How to Use

### Step 1 — Select Difficulty

Choose one of:

```text
Easy
Medium
Hard
```

### Step 2 — Start the Test

Click:

```text
Start Test
```

The program will randomly select a paragraph based on the selected difficulty.

### Step 3 — Type the Text

Type the displayed paragraph into the text box.

The timer starts automatically when the test begins.

### Step 4 — Submit

Click:

```text
Submit
```

The application calculates your performance.

## Example Result

```text
WPM: 54.72
Accuracy: 94.83%
Time: 38.21 seconds
Characters Typed: 248
Errors: 9
```

## WPM Calculation

Words Per Minute is calculated using:

```text
WPM = Number of Words / Time in Minutes
```

For example, if a user types 50 words in 2 minutes:

```text
WPM = 50 / 2
WPM = 25
```

## Accuracy Calculation

Accuracy compares the characters typed by the user with the original text.

The program checks each character position and calculates the percentage of correctly typed characters.

## Difficulty Levels

### Easy

Short and simple sentences.

Example:

```text
Python is easy to learn and fun to use.
```

### Medium

Longer sentences with more complex wording.

Example:

```text
Python provides powerful libraries for data analysis and visualization.
```

### Hard

Longer technical sentences requiring greater typing speed and accuracy.

Example:

```text
Efficient programming requires developers to understand algorithms, data structures, debugging techniques, and software design.
```

## Program Workflow

```text
Select Difficulty
       ↓
Generate Random Text
       ↓
Start Timer
       ↓
User Types Text
       ↓
Stop Timer
       ↓
Compare Original & Typed Text
       ↓
Calculate WPM
       ↓
Calculate Accuracy
       ↓
Display Results
```

## Python Concepts Practiced

This project introduces several concepts beyond basic Python:

* Object-Oriented Programming
* Classes
* Objects
* Methods
* Tkinter GUI
* Event-driven programming
* `time` module
* `random` module
* String manipulation
* Loops
* Conditional statements
* Exception-safe input handling
* Mathematical calculations
* Lists and dictionaries
* GUI state management

## Learning Objective

The goal of this project is to understand how Python can be used to build an interactive application rather than a simple terminal-based program.

It also introduces the concept of event-driven programming, where actions such as button clicks trigger specific functions.

## Possible Improvements

After completing the basic version, the project can be extended with:

* Personal best WPM
* Average WPM across multiple tests
* Accuracy history
* Typing performance graph
* Countdown before the test
* Custom typing duration
* Larger text library
* Live character highlighting
* Error highlighting
* Dark mode
* Sound effects
* Save results to CSV
* User profiles
* Persistent typing statistics

## Future Data Flow

A future version could store test results like:

```text
Date | Difficulty | WPM | Accuracy | Errors | Time
```

This would allow the project to evolve from a simple typing tester into a **typing performance analytics application**.