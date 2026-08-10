import csv
import time
from datetime import datetime
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import psutil


LOG_FILE = Path("system_log.csv")


# ============================================================
# SYSTEM INFORMATION
# ============================================================

def get_cpu_usage():

    return psutil.cpu_percent(
        interval=1
    )


def get_memory_usage():

    memory = psutil.virtual_memory()

    return {
        "total": memory.total,
        "used": memory.used,
        "available": memory.available,
        "percentage": memory.percent
    }


def get_disk_usage():

    disk = psutil.disk_usage("/")

    return {
        "total": disk.total,
        "used": disk.used,
        "free": disk.free,
        "percentage": disk.percent
    }


def get_network_usage():

    network = psutil.net_io_counters()

    return {
        "sent": network.bytes_sent,
        "received": network.bytes_recv
    }


def get_process_count():

    return len(
        list(
            psutil.process_iter()
        )
    )


# ============================================================
# FORMATTING
# ============================================================

def format_bytes(value):

    units = [
        "B",
        "KB",
        "MB",
        "GB",
        "TB"
    ]

    value = float(value)

    for unit in units:

        if value < 1024:

            return f"{value:.2f} {unit}"

        value /= 1024

    return f"{value:.2f} PB"


def format_uptime(seconds):

    seconds = int(seconds)

    days = seconds // 86400

    seconds %= 86400

    hours = seconds // 3600

    seconds %= 3600

    minutes = seconds // 60

    seconds %= 60

    return (
        f"{days}d "
        f"{hours}h "
        f"{minutes}m "
        f"{seconds}s"
    )


# ============================================================
# SNAPSHOT
# ============================================================

def get_system_snapshot():

    cpu = get_cpu_usage()

    memory = get_memory_usage()

    disk = get_disk_usage()

    network = get_network_usage()

    process_count = get_process_count()

    uptime = (
        time.time()
        - psutil.boot_time()
    )

    return {
        "timestamp": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),
        "cpu_percent": cpu,
        "memory_percent": memory["percentage"],
        "memory_used": memory["used"],
        "disk_percent": disk["percentage"],
        "disk_used": disk["used"],
        "network_sent": network["sent"],
        "network_received": network["received"],
        "process_count": process_count,
        "uptime_seconds": uptime
    }


# ============================================================
# DISPLAY SNAPSHOT
# ============================================================

def display_snapshot(snapshot):

    print("\n" + "=" * 60)
    print("SYSTEM STATUS")
    print("=" * 60)

    print(
        f"Time            : "
        f"{snapshot['timestamp']}"
    )

    print(
        f"CPU Usage       : "
        f"{snapshot['cpu_percent']:.1f}%"
    )

    print(
        f"Memory Usage    : "
        f"{snapshot['memory_percent']:.1f}%"
    )

    print(
        f"Memory Used     : "
        f"{format_bytes(snapshot['memory_used'])}"
    )

    print(
        f"Disk Usage      : "
        f"{snapshot['disk_percent']:.1f}%"
    )

    print(
        f"Disk Used       : "
        f"{format_bytes(snapshot['disk_used'])}"
    )

    print(
        f"Network Sent    : "
        f"{format_bytes(snapshot['network_sent'])}"
    )

    print(
        f"Network Received: "
        f"{format_bytes(snapshot['network_received'])}"
    )

    print(
        f"Running Processes: "
        f"{snapshot['process_count']}"
    )

    print(
        f"System Uptime   : "
        f"{format_uptime(snapshot['uptime_seconds'])}"
    )


# ============================================================
# LOGGING
# ============================================================

def initialize_log():

    if LOG_FILE.exists():
        return

    columns = [
        "timestamp",
        "cpu_percent",
        "memory_percent",
        "memory_used",
        "disk_percent",
        "disk_used",
        "network_sent",
        "network_received",
        "process_count",
        "uptime_seconds"
    ]

    with open(
        LOG_FILE,
        "w",
        newline=""
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=columns
        )

        writer.writeheader()


def save_snapshot(snapshot):

    initialize_log()

    with open(
        LOG_FILE,
        "a",
        newline=""
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=snapshot.keys()
        )

        writer.writerow(
            snapshot
        )


# ============================================================
# REAL-TIME MONITOR
# ============================================================

def live_monitor():

    print("\n" + "=" * 60)
    print("LIVE SYSTEM MONITOR")
    print("=" * 60)

    print(
        "Press Ctrl+C to stop monitoring."
    )

    try:

        while True:

            snapshot = get_system_snapshot()

            display_snapshot(
                snapshot
            )

            save_snapshot(
                snapshot
            )

            time.sleep(2)

    except KeyboardInterrupt:

        print(
            "\n\nMonitoring stopped."
        )


# ============================================================
# PROCESS ANALYZER
# ============================================================

def get_process_data():

    processes = []

    for process in psutil.process_iter(
        [
            "pid",
            "name",
            "cpu_percent",
            "memory_percent"
        ]
    ):

        try:

            info = process.info

            processes.append({
                "PID": info["pid"],
                "Name": info["name"],
                "CPU": info["cpu_percent"] or 0,
                "Memory": info["memory_percent"] or 0
            })

        except (
            psutil.NoSuchProcess,
            psutil.AccessDenied
        ):

            continue

    return pd.DataFrame(
        processes
    )


def top_cpu_processes():

    df = get_process_data()

    if df.empty:

        print(
            "\nNo process information available."
        )

        return

    df = df.sort_values(
        "CPU",
        ascending=False
    )

    print("\n" + "=" * 70)
    print("TOP CPU-CONSUMING PROCESSES")
    print("=" * 70)

    print(
        df.head(10).to_string(
            index=False
        )
    )


def top_memory_processes():

    df = get_process_data()

    if df.empty:

        print(
            "\nNo process information available."
        )

        return

    df = df.sort_values(
        "Memory",
        ascending=False
    )

    print("\n" + "=" * 70)
    print("TOP MEMORY-CONSUMING PROCESSES")
    print("=" * 70)

    print(
        df.head(10).to_string(
            index=False
        )
    )


# ============================================================
# LOG ANALYSIS
# ============================================================

def load_logs():

    if not LOG_FILE.exists():

        print(
            "\nNo system log exists yet."
        )

        return pd.DataFrame()

    try:

        df = pd.read_csv(
            LOG_FILE
        )

        df["timestamp"] = pd.to_datetime(
            df["timestamp"]
        )

        return df

    except Exception:

        print(
            "\nCould not read system log."
        )

        return pd.DataFrame()


def analyze_logs():

    df = load_logs()

    if df.empty:

        return

    print("\n" + "=" * 60)
    print("SYSTEM PERFORMANCE ANALYSIS")
    print("=" * 60)

    print(
        f"Samples recorded : "
        f"{len(df)}"
    )

    print(
        f"Average CPU      : "
        f"{df['cpu_percent'].mean():.2f}%"
    )

    print(
        f"Maximum CPU      : "
        f"{df['cpu_percent'].max():.2f}%"
    )

    print(
        f"Average Memory   : "
        f"{df['memory_percent'].mean():.2f}%"
    )

    print(
        f"Maximum Memory   : "
        f"{df['memory_percent'].max():.2f}%"
    )

    print(
        f"Average Processes: "
        f"{df['process_count'].mean():.0f}"
    )

    print(
        f"Maximum Processes: "
        f"{df['process_count'].max():.0f}"
    )


# ============================================================
# ALERT ANALYSIS
# ============================================================

def check_system_alerts():

    snapshot = get_system_snapshot()

    print("\n" + "=" * 60)
    print("SYSTEM ALERT CHECK")
    print("=" * 60)

    alerts = []

    if snapshot["cpu_percent"] >= 90:

        alerts.append(
            "CPU usage is critically high."
        )

    elif snapshot["cpu_percent"] >= 75:

        alerts.append(
            "CPU usage is high."
        )

    if snapshot["memory_percent"] >= 90:

        alerts.append(
            "Memory usage is critically high."
        )

    elif snapshot["memory_percent"] >= 75:

        alerts.append(
            "Memory usage is high."
        )

    if snapshot["disk_percent"] >= 90:

        alerts.append(
            "Disk usage is critically high."
        )

    elif snapshot["disk_percent"] >= 80:

        alerts.append(
            "Disk usage is high."
        )

    if not alerts:

        print(
            "✓ No resource warnings detected."
        )

    else:

        for alert in alerts:

            print(
                f"⚠ {alert}"
            )


# ============================================================
# CHARTS
# ============================================================

def plot_cpu_usage():

    df = load_logs()

    if df.empty:

        return

    plt.figure(
        figsize=(10, 5)
    )

    plt.plot(
        df["timestamp"],
        df["cpu_percent"],
        marker="o"
    )

    plt.title(
        "CPU Usage Over Time"
    )

    plt.xlabel(
        "Time"
    )

    plt.ylabel(
        "CPU Usage (%)"
    )

    plt.ylim(
        0,
        100
    )

    plt.xticks(
        rotation=45
    )

    plt.grid()

    plt.tight_layout()

    plt.show()


def plot_memory_usage():

    df = load_logs()

    if df.empty:

        return

    plt.figure(
        figsize=(10, 5)
    )

    plt.plot(
        df["timestamp"],
        df["memory_percent"],
        marker="o"
    )

    plt.title(
        "Memory Usage Over Time"
    )

    plt.xlabel(
        "Time"
    )

    plt.ylabel(
        "Memory Usage (%)"
    )

    plt.ylim(
        0,
        100
    )

    plt.xticks(
        rotation=45
    )

    plt.grid()

    plt.tight_layout()

    plt.show()


def plot_resource_comparison():

    df = load_logs()

    if df.empty:

        return

    plt.figure(
        figsize=(10, 5)
    )

    plt.plot(
        df["timestamp"],
        df["cpu_percent"],
        label="CPU"
    )

    plt.plot(
        df["timestamp"],
        df["memory_percent"],
        label="Memory"
    )

    plt.plot(
        df["timestamp"],
        df["disk_percent"],
        label="Disk"
    )

    plt.title(
        "System Resource Usage"
    )

    plt.xlabel(
        "Time"
    )

    plt.ylabel(
        "Usage (%)"
    )

    plt.ylim(
        0,
        100
    )

    plt.legend()

    plt.xticks(
        rotation=45
    )

    plt.grid()

    plt.tight_layout()

    plt.show()


# ============================================================
# EXPORT SUMMARY
# ============================================================

def export_summary():

    df = load_logs()

    if df.empty:

        return

    summary = pd.DataFrame({
        "Metric": [
            "Average CPU",
            "Maximum CPU",
            "Average Memory",
            "Maximum Memory",
            "Average Processes",
            "Maximum Processes"
        ],
        "Value": [
            df["cpu_percent"].mean(),
            df["cpu_percent"].max(),
            df["memory_percent"].mean(),
            df["memory_percent"].max(),
            df["process_count"].mean(),
            df["process_count"].max()
        ]
    })

    output_file = (
        "system_summary.csv"
    )

    summary.to_csv(
        output_file,
        index=False
    )

    print(
        f"\nSummary exported to "
        f"'{output_file}'."
    )


# ============================================================
# MENU
# ============================================================

def display_menu():

    print("\n" + "=" * 65)
    print("          SYSTEM RESOURCE MONITOR")
    print("=" * 65)

    print("1. Current System Status")
    print("2. Live Monitor")
    print("3. Top CPU Processes")
    print("4. Top Memory Processes")
    print("5. Analyze System Logs")
    print("6. Check Resource Alerts")
    print("7. CPU Usage Chart")
    print("8. Memory Usage Chart")
    print("9. Resource Comparison Chart")
    print("10. Export Summary")
    print("11. Exit")

    print("=" * 65)


# ============================================================
# MAIN
# ============================================================

def main():

    initialize_log()

    print("=" * 65)
    print("          SYSTEM RESOURCE MONITOR")
    print("=" * 65)

    while True:

        display_menu()

        choice = input(
            "Enter your choice: "
        ).strip()

        if choice == "1":

            snapshot = get_system_snapshot()

            display_snapshot(
                snapshot
            )

        elif choice == "2":

            live_monitor()

        elif choice == "3":

            top_cpu_processes()

        elif choice == "4":

            top_memory_processes()

        elif choice == "5":

            analyze_logs()

        elif choice == "6":

            check_system_alerts()

        elif choice == "7":

            plot_cpu_usage()

        elif choice == "8":

            plot_memory_usage()

        elif choice == "9":

            plot_resource_comparison()

        elif choice == "10":

            export_summary()

        elif choice == "11":

            print(
                "\nSystem monitor closed."
            )

            break

        else:

            print(
                "\nInvalid choice. "
                "Please select 1-11."
            )


if __name__ == "__main__":
    main()