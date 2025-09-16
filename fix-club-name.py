#!/usr/bin/env python3
"""
fix_club_names.py

This script scans a CSV file exported from the cyclocross league system,
looking for entries where a rider's club is listed as:
    "Another Club/Team (not listed below)"

In these cases, the correct club name is actually in the *next* column.

The script:
- Accepts the CSV file path and SQLite database path as command-line arguments
- Locates affected rows
- Updates the `club_name` field in the `riders` table based on `race_number`

Usage:
    python fix_club_names.py riders.csv cx_league.db

Author: ChatGPT + Adam's tweaks
Date: August 2025
"""

import csv
import sqlite3
import argparse
import os
import sys

def fix_club_names(csv_file, db_file):
    if not os.path.exists(csv_file):
        print(f"CSV file not found: {csv_file}")
        sys.exit(1)
    if not os.path.exists(db_file):
        print(f"SQLite DB not found: {db_file}")
        sys.exit(1)

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    updates = 0
    with open(csv_file, newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) < 6:
                continue  # Skip malformed rows
            race_number = row[1].strip()
            club_flag = row[4].strip()
            corrected_club = row[5].strip()

            if club_flag == "Another Club/Team (not listed below)":
                print(f"Updating rider {race_number}: club → {corrected_club}")
                cursor.execute(
                    "UPDATE riders SET club_name = ? WHERE race_number = ?",
                    (corrected_club, race_number)
                )
                updates += 1

    conn.commit()
    conn.close()
    print(f"\n✅ Update complete. {updates} record(s) updated.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fix club names in a CX league SQLite DB from CSV input.")
    parser.add_argument("csv_file", help="Path to input CSV file")
    parser.add_argument("db_file", help="Path to SQLite database file")

    args = parser.parse_args()
    fix_club_names(args.csv_file, args.db_file)

