# System Resource Monitor & Performance Analyzer

A Python-based command-line system monitoring application that collects information about the user's computer and analyzes system performance over time.

The application monitors CPU, memory, disk, network, processes, and system uptime.

It can also record system metrics to a CSV file and generate performance visualizations.

No external dataset, API, or internet connection is required.

## Features

### System Monitoring

* CPU usage
* RAM usage
* Disk usage
* Network traffic
* Number of running processes
* System uptime

### Process Analysis

* Top CPU-consuming processes
* Top memory-consuming processes

### Performance Logging

* Automatically record system snapshots
* Store measurements in CSV
* Analyze historical measurements

### Alerts

* High CPU warning
* High memory warning
* High disk usage warning
* Critical resource warnings

### Visualization

* CPU usage over time
* Memory usage over time
* CPU vs memory vs disk usage

### Export

* Export performance summary to CSV

## Technologies Used

* Python
* psutil
* Pandas
* Matplotlib
* CSV
* `datetime`
* `pathlib`

## Project Structure

```text
system-resource-monitor/
│
├── main.py
├── requirements.txt
├── README.md
├── system_log.csv        # Created automatically
└── system_summary.csv    # Created when exported
```

The CSV files are generated automatically.

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

The application displays:

```text
=================================================================
          SYSTEM RESOURCE MONITOR
=================================================================
1. Current System Status
2. Live Monitor
3. Top CPU Processes
4. Top Memory Processes
5. Analyze System Logs
6. Check Resource Alerts
7. CPU Usage Chart
8. Memory Usage Chart
9. Resource Comparison Chart
10. Export Summary
11. Exit
=================================================================
```

# Current System Status

Select:

```text
1. Current System Status
```

The program takes a snapshot of the current system.

Example:

```text
============================================================
SYSTEM STATUS
============================================================
Time            : 2026-08-09 12:30:21
CPU Usage       : 23.4%
Memory Usage    : 61.8%
Memory Used     : 9.84 GB
Disk Usage      : 72.1%
Disk Used       : 356.42 GB
Network Sent    : 4.21 GB
Network Received: 18.73 GB
Running Processes: 214
System Uptime   : 2d 7h 34m 21s
```

Every snapshot is also saved to the system log.

## Live Monitor

Select:

```text
2. Live Monitor
```

The program continuously records system information.

Example:

```text
CPU Usage       : 31.2%
Memory Usage    : 63.1%
Disk Usage      : 72.1%
Running Processes: 215
```

A new snapshot is collected approximately every two seconds.

Press:

```text
Ctrl + C
```

to stop monitoring.

## Process Analysis

The application can inspect currently running processes.

### CPU Processes

Select:

```text
3. Top CPU Processes
```

Example:

```text
============================================================
TOP CPU-CONSUMING PROCESSES
============================================================

 PID   Name                  CPU    Memory
 4210  chrome.exe            18.4   4.21
 8932  python.exe            12.7   2.84
 3321  code.exe               8.2   3.17
```

### Memory Processes

Select:

```text
4. Top Memory Processes
```

This identifies applications consuming the most RAM.

## Performance Logging

System snapshots are stored in:

```text
system_log.csv
```

Example:

```text
timestamp,cpu_percent,memory_percent,memory_used,...
2026-08-09 12:30:21,23.4,61.8,...
2026-08-09 12:30:24,31.2,62.1,...
2026-08-09 12:30:27,28.7,62.0,...
```

This means the application is effectively creating its own dataset from your computer's activity.

## Log Analysis

Select:

```text
5. Analyze System Logs
```

The application calculates:

* Number of measurements
* Average CPU usage
* Maximum CPU usage
* Average memory usage
* Maximum memory usage
* Average number of processes
* Maximum number of processes

Example:

```text
============================================================
SYSTEM PERFORMANCE ANALYSIS
============================================================

Samples recorded : 184
Average CPU      : 34.27%
Maximum CPU      : 92.41%
Average Memory   : 63.84%
Maximum Memory   : 71.22%
Average Processes: 216
Maximum Processes: 229
```

## Resource Alerts

Select:

```text
6. Check Resource Alerts
```

The application checks the current system state.

CPU:

```text
>= 90% → Critical
>= 75% → High
```

Memory:

```text
>= 90% → Critical
>= 75% → High
```

Disk:

```text
>= 90% → Critical
>= 80% → High
```

Example:

```text
============================================================
SYSTEM ALERT CHECK
============================================================

⚠ CPU usage is high.
⚠ Memory usage is high.
```

If everything is below the thresholds:

```text
✓ No resource warnings detected.
```

## Visualizations

The application provides three charts.

### CPU Usage Over Time

Shows how CPU utilization changes during the monitoring period.

### Memory Usage Over Time

Shows RAM utilization over time.

### Resource Comparison

Displays CPU, memory, and disk usage together.

This makes it easier to identify periods where multiple resources become heavily utilized.

## Export Summary

Select:

```text
10. Export Summary
```

The application creates:

```text
system_summary.csv
```

Example:

```text
Metric,Value
Average CPU,34.27
Maximum CPU,92.41
Average Memory,63.84
Maximum Memory,71.22
Average Processes,216
Maximum Processes,229
```

## How psutil Works

The main library used by this project is `psutil`.

It provides Python access to operating-system information.

The application uses:

```python
psutil.cpu_percent()
```

for CPU utilization.

```python
psutil.virtual_memory()
```

for RAM information.

```python
psutil.disk_usage()
```

for disk information.

```python
psutil.net_io_counters()
```

for network statistics.

```python
psutil.process_iter()
```

for running processes.

```python
psutil.boot_time()
```

for system boot time.

## Program Architecture

```text
Operating System
       ↓
     psutil
       ↓
System Snapshot
       ↓
    CSV Log
       ↓
   Pandas
       ↓
 ┌─────┼───────────┐
 ↓     ↓           ↓
Stats  Alerts    Charts
```

## Program Workflow

```text
Start Application
       ↓
Collect System Information
       ↓
Display Current Status
       ↓
Save Snapshot
       ↓
Repeat During Monitoring
       ↓
Build Historical Dataset
       ↓
Analyze Performance
       ↓
Detect Resource Problems
       ↓
Visualize Trends
       ↓
Export Summary
```

## Python Concepts Practiced

This project introduces:

* System APIs
* Third-party libraries
* Real-time data collection
* Process management
* CSV logging
* Pandas DataFrames
* Time-series data
* Statistical aggregation
* Threshold-based alerts
* Matplotlib
* Exception handling
* File persistence
* Resource monitoring

## Learning Objective

The main objective is to understand how Python can interact with the operating system rather than only working with manually supplied data.

The project follows this architecture:

```text
Real System
    ↓
Data Collection
    ↓
Data Storage
    ↓
Data Analysis
    ↓
Visualization
    ↓
Decision / Alert
```

This is similar to the basic architecture behind many monitoring systems.

## Important Note

Some process information may be unavailable depending on operating-system permissions.

The program handles inaccessible processes and continues running.

The monitoring application is also intended for educational purposes. It should not be considered a replacement for professional system-monitoring tools.

## Possible Improvements

After completing the basic project, you can extend it with:

* CPU temperature monitoring
* GPU monitoring
* Battery health monitoring
* Per-process CPU tracking
* Per-process RAM tracking
* Network speed calculation
* Download/upload speed graphs
* Configurable alert thresholds
* Automatic alert notifications
* Background monitoring
* SQLite storage
* Tkinter GUI
* Plotly dashboard
* System health score
* Daily performance reports
* Automatic cleanup recommendations
* Process search and filtering
* Resource usage prediction