#!/usr/bin/env python3
"""
find_duplicate_lines.py

Given multiple CSV files, this script finds and prints lines
that appear in **more than one file** (exact string match).

Usage:
    python find_duplicate_lines.py file1.csv file2.csv file3.csv ...

Author: ChatGPT
Date: August 2025
"""

import argparse
from collections import defaultdict
import os

def find_duplicates(file_list):
    line_occurrences = defaultdict(set)

    for file in file_list:
        if not os.path.exists(file):
            print(f"❌ File not found: {file}")
            continue
        with open(file, "r", encoding="utf-8") as f:
            for line_num, line in enumerate(f, 1):
                clean_line = line.strip()
                if clean_line:
                    line_occurrences[clean_line].add(file)

    # Print duplicates
    duplicates = {line: files for line, files in line_occurrences.items() if len(files) > 1}

    if not duplicates:
        print("✅ No duplicate lines found across the files.")
        return

    print("🔁 Duplicate lines found in multiple files:\n")
    for line, files in duplicates.items():
        file_list_str = ", ".join(sorted(files))
        print(f"'{line}' found in: {file_list_str}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Find duplicate lines across multiple CSV files.")
    parser.add_argument("files", nargs="+", help="CSV file paths to compare")
    args = parser.parse_args()

    find_duplicates(args.files)

