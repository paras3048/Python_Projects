# File & Folder Storage Analyzer

A Python-based file system analysis tool that scans a user-selected folder and analyzes how files are distributed across categories, file types, and storage sizes.

The project works directly with files already present on the user's computer. No external dataset, API, or downloaded data is required.

## Features

* Analyze any folder on the computer
* Recursively scan subfolders
* Count total files
* Calculate total storage usage
* Categorize files automatically
* Analyze storage by file category
* Analyze storage by file extension
* Identify the 10 largest files
* Find empty files
* Detect duplicate filenames
* Generate storage visualizations
* Export the complete scan to CSV

## File Categories

The program automatically recognizes common file types.

| Category      | Examples                |
| ------------- | ----------------------- |
| Images        | JPG, PNG, GIF, WEBP     |
| Videos        | MP4, MKV, AVI, MOV      |
| Audio         | MP3, WAV, FLAC          |
| Documents     | DOCX, TXT, RTF          |
| PDF           | PDF                     |
| Spreadsheets  | XLSX, CSV, ODS          |
| Presentations | PPTX, ODP               |
| Archives      | ZIP, RAR, 7Z            |
| Code          | PY, JS, HTML, CSS, SQL  |
| Other         | Unrecognized extensions |

## Technologies Used

* Python
* Pandas
* Matplotlib
* pathlib
* os-level file system information through Python

## Project Structure

```text
file-storage-analyzer/
│
├── main.py
└── README.md
```

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

Install the required packages:

```bash
pip install -r requirements.txt
```

## Running the Project

Run:

```bash
python main.py
```

The program will ask for a folder path.

Example:

```text
Enter folder path to analyze: C:\Users\YourName\Downloads
```

The program will recursively scan the selected folder and its subfolders.

## Example Output

```text
============================================================
STORAGE OVERVIEW
============================================================
Total files      : 1842
Folders scanned  : 126
Total storage    : 8.42 GB
```

### Storage by Category

```text
============================================================
STORAGE BY CATEGORY
============================================================
Videos              42 files   4,820.51 MB
Images             631 files   1,745.28 MB
Documents          214 files     512.63 MB
Archives            18 files     341.20 MB
Code                97 files      82.43 MB
Other              840 files     176.31 MB
```

## Largest Files

The program identifies the ten largest files.

Example:

```text
============================================================
10 LARGEST FILES
============================================================

movie.mp4
Size: 1.42 GB
Path: C:\Users\YourName\Downloads\movie.mp4

backup.zip
Size: 856.21 MB
Path: C:\Users\YourName\Downloads\backup.zip
```

## Empty Files

The program searches for files with a size of zero bytes.

```text
============================================================
EMPTY FILES
============================================================
Number of empty files: 7
```

This can be useful for identifying unnecessary or accidentally created files.

## Duplicate Filenames

The program also identifies files with the same filename, even if they are located in different folders.

Example:

```text
============================================================
DUPLICATE FILE NAMES
============================================================

report.pdf
  C:\Documents\report.pdf
  C:\Downloads\report.pdf

image.jpg
  C:\Pictures\image.jpg
  C:\Backup\image.jpg
```

Note that duplicate filenames do not necessarily mean duplicate files. Two files with the same name may contain completely different data.

## Visualizations

The application generates three charts.

### 1. Storage Usage by Category

Shows how much storage each file category consumes.

### 2. Number of Files by Category

Shows the number of files belonging to each category.

### 3. Storage Distribution

Displays the percentage of total storage consumed by each category.

## Output File

The program generates:

```text
storage_report.csv
```

The CSV contains information about every accessible file found during the scan.

Example fields:

```text
Name
Path
Extension
Category
Size Bytes
Size MB
```

Example:

```text
Name,Path,Extension,Category,Size Bytes,Size MB
photo.jpg,C:\Pictures\photo.jpg,.jpg,Images,2456321,2.34
report.pdf,C:\Documents\report.pdf,.pdf,PDF,734532,0.70
```

## Program Workflow

```text
Select Folder
      ↓
Scan Folder
      ↓
Find Files
      ↓
Read File Metadata
      ↓
Classify File Type
      ↓
Create Pandas DataFrame
      ↓
Analyze Storage
      ↓
Identify Large / Empty / Duplicate Files
      ↓
Generate Charts
      ↓
Export CSV Report
```

## Python Concepts Practiced

This project introduces:

* `pathlib`
* File system navigation
* Recursive directory scanning
* File metadata
* File extensions
* Exception handling
* Lists
* Dictionaries
* Functions
* Pandas DataFrames
* `groupby()`
* Aggregation
* Sorting
* Duplicate detection
* CSV export
* Matplotlib visualization

## Important Safety Note

This application is **read-only**.

It does not:

* Delete files
* Move files
* Rename files
* Modify files
* Compress files

It only reads file information and generates an analysis report.

## Learning Objective

The goal is to understand how Python can interact with the operating system and convert filesystem information into structured data that can be analyzed using Pandas.

This project combines two important Python areas:

```text
Python Automation
       +
Data Analysis
```

## Possible Improvements

After completing the basic version, the project could be extended with:

* Detect actual duplicate files using file hashing
* Find files older than a specified date
* Find recently modified files
* Analyze storage by folder
* Generate a complete HTML report
* Add a graphical folder selector
* Add configurable file categories
* Export charts automatically
* Add a "largest folders" analysis
* Compare two folders
* Add a safe cleanup recommendation system