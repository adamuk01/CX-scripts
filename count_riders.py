#!/usr/bin/env python3
"""
count_riders.py

Counts the number of riders in the SQLite database (`riders` table),
and optionally compares this with the number of lines in a CSV file.

Usage:
    python count_riders.py cx_league.db [riders.csv]

Author: ChatGPT + Adam's tweaks
Date: August 2025
"""

import sqlite3
import csv
import argparse
import os
import sys

def count_db_riders(db_file):
    if not os.path.exists(db_file):
        print(f"❌ SQLite DB not found: {db_file}")
        sys.exit(1)
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT COUNT(*) FROM riders")
        count = cursor.fetchone()[0]
        return count
    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")
        sys.exit(1)
    finally:
        conn.close()

def count_csv_lines(csv_file):
    if not os.path.exists(csv_file):
        print(f"❌ CSV file not found: {csv_file}")
        sys.exit(1)
    with open(csv_file, newline='') as f:
        reader = csv.reader(f)
        line_count = sum(1 for row in reader if row and row[0].strip())
        return line_count

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Count riders in SQLite DB and optional CSV file.")
    parser.add_argument("db_file", help="Path to SQLite database file")
    parser.add_argument("csv_file", nargs="?", help="Optional: path to input CSV file")

    args = parser.parse_args()

    db_count = count_db_riders(args.db_file)
    print(f"📦 Riders in DB:     {db_count}")

    if args.csv_file:
        csv_count = count_csv_lines(args.csv_file)
        print(f"📄 Rows in CSV:     {csv_count}")

        if db_count == csv_count:
            print("✅ Record count matches.")
        else:
            print("⚠️  Record count mismatch!")

