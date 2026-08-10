from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt


FILE_CATEGORIES = {
    "Images": [
        ".jpg", ".jpeg", ".png", ".gif",
        ".bmp", ".webp", ".svg"
    ],
    "Videos": [
        ".mp4", ".mkv", ".avi", ".mov",
        ".wmv", ".flv"
    ],
    "Audio": [
        ".mp3", ".wav", ".aac",
        ".flac", ".ogg"
    ],
    "Documents": [
        ".doc", ".docx", ".txt", ".odt",
        ".rtf"
    ],
    "PDF": [
        ".pdf"
    ],
    "Spreadsheets": [
        ".xls", ".xlsx", ".csv", ".ods"
    ],
    "Presentations": [
        ".ppt", ".pptx", ".odp"
    ],
    "Archives": [
        ".zip", ".rar", ".7z",
        ".tar", ".gz"
    ],
    "Code": [
        ".py", ".js", ".html", ".css",
        ".java", ".cpp", ".c", ".sql"
    ]
}


def get_category(extension):

    extension = extension.lower()

    for category, extensions in FILE_CATEGORIES.items():

        if extension in extensions:
            return category

    return "Other"


def format_size(size_bytes):

    if size_bytes < 1024:
        return f"{size_bytes} B"

    if size_bytes < 1024 ** 2:
        return f"{size_bytes / 1024:.2f} KB"

    if size_bytes < 1024 ** 3:
        return f"{size_bytes / (1024 ** 2):.2f} MB"

    return f"{size_bytes / (1024 ** 3):.2f} GB"


def get_folder():

    while True:

        folder_input = input(
            "\nEnter folder path to analyze: "
        ).strip()

        folder = Path(folder_input).expanduser()

        if folder.exists() and folder.is_dir():
            return folder

        print("Invalid folder path. Please try again.")


def scan_folder(folder):

    files = []

    print("\nScanning folder...")

    for file_path in folder.rglob("*"):

        if not file_path.is_file():
            continue

        try:
            size = file_path.stat().st_size

            extension = file_path.suffix.lower()

            category = get_category(extension)

            files.append({
                "Name": file_path.name,
                "Path": str(file_path),
                "Extension": extension if extension else "No Extension",
                "Category": category,
                "Size Bytes": size,
                "Size MB": size / (1024 ** 2)
            })

        except (PermissionError, OSError):
            print(
                f"Could not access: {file_path}"
            )

    return files


def create_dataframe(files):

    if not files:
        return pd.DataFrame()

    return pd.DataFrame(files)


def display_overview(df):

    total_files = len(df)

    total_size = df["Size Bytes"].sum()

    folders = (
        df["Path"]
        .apply(lambda path: str(Path(path).parent))
        .nunique()
    )

    print("\n" + "=" * 60)
    print("STORAGE OVERVIEW")
    print("=" * 60)

    print(f"Total files      : {total_files}")
    print(f"Folders scanned  : {folders}")
    print(f"Total storage    : {format_size(total_size)}")


def display_category_analysis(df):

    category_stats = (
        df.groupby("Category")
        .agg(
            Files=("Name", "count"),
            Storage_MB=("Size MB", "sum")
        )
        .sort_values(
            "Storage_MB",
            ascending=False
        )
    )

    print("\n" + "=" * 60)
    print("STORAGE BY CATEGORY")
    print("=" * 60)

    for category, row in category_stats.iterrows():

        print(
            f"{category:<15} "
            f"{int(row['Files']):>5} files   "
            f"{row['Storage_MB']:.2f} MB"
        )

    return category_stats


def display_extension_analysis(df):

    extension_stats = (
        df.groupby("Extension")
        .agg(
            Files=("Name", "count"),
            Storage_MB=("Size MB", "sum")
        )
        .sort_values(
            "Storage_MB",
            ascending=False
        )
    )

    print("\n" + "=" * 60)
    print("STORAGE BY FILE TYPE")
    print("=" * 60)

    print(
        extension_stats.head(15).to_string()
    )

    return extension_stats


def display_largest_files(df):

    largest_files = (
        df.sort_values(
            "Size Bytes",
            ascending=False
        )
        .head(10)
    )

    print("\n" + "=" * 60)
    print("10 LARGEST FILES")
    print("=" * 60)

    for index, row in largest_files.iterrows():

        print(
            f"\n{row['Name']}"
        )

        print(
            f"Size: "
            f"{format_size(row['Size Bytes'])}"
        )

        print(
            f"Path: "
            f"{row['Path']}"
        )


def display_empty_files(df):

    empty_files = df[
        df["Size Bytes"] == 0
    ]

    print("\n" + "=" * 60)
    print("EMPTY FILES")
    print("=" * 60)

    print(
        f"Number of empty files: "
        f"{len(empty_files)}"
    )

    if not empty_files.empty:

        for _, row in empty_files.head(20).iterrows():

            print(row["Path"])


def display_duplicate_names(df):

    duplicates = df[
        df.duplicated(
            subset=["Name"],
            keep=False
        )
    ]

    print("\n" + "=" * 60)
    print("DUPLICATE FILE NAMES")
    print("=" * 60)

    if duplicates.empty:

        print("No duplicate filenames found.")

        return

    grouped = duplicates.groupby("Name")

    for name, group in grouped:

        print(f"\n{name}")

        for path in group["Path"]:

            print(f"  {path}")


def generate_charts(df, category_stats):

    # Category storage chart

    plt.figure(figsize=(9, 5))

    category_stats["Storage_MB"].plot(
        kind="bar"
    )

    plt.title("Storage Usage by Category")
    plt.xlabel("Category")
    plt.ylabel("Storage (MB)")

    plt.xticks(rotation=45)

    plt.tight_layout()

    plt.show()

    # File count chart

    plt.figure(figsize=(9, 5))

    category_stats["Files"].plot(
        kind="bar"
    )

    plt.title("Number of Files by Category")
    plt.xlabel("Category")
    plt.ylabel("Number of Files")

    plt.xticks(rotation=45)

    plt.tight_layout()

    plt.show()

    # Storage distribution

    plt.figure(figsize=(8, 8))

    category_stats["Storage_MB"].plot(
        kind="pie",
        autopct="%1.1f%%"
    )

    plt.title("Storage Distribution")

    plt.ylabel("")

    plt.tight_layout()

    plt.show()


def save_report(df):

    output_file = "storage_report.csv"

    df.to_csv(
        output_file,
        index=False
    )

    print(
        f"\nReport saved as '{output_file}'."
    )


def main():

    print("=" * 60)
    print("        FILE & FOLDER STORAGE ANALYZER")
    print("=" * 60)

    folder = get_folder()

    files = scan_folder(folder)

    if not files:

        print(
            "\nNo accessible files found."
        )

        return

    df = create_dataframe(files)

    display_overview(df)

    category_stats = display_category_analysis(
        df
    )

    display_extension_analysis(df)

    display_largest_files(df)

    display_empty_files(df)

    display_duplicate_names(df)

    save_report(df)

    print("\nGenerating charts...")

    generate_charts(
        df,
        category_stats
    )

    print(
        "\nStorage analysis completed."
    )


if __name__ == "__main__":
    main()