#!/usr/bin/python3

# This will add the 1BX setting to the CSV file by querying ALL the databases

import sqlite3
import csv
import argparse
import os
from collections import defaultdict

# List of paths to your SQLite databases
db_paths = [
    "Senior.db",
    "Vet50.db",
    "Women.db",
    "Youth.db",
]

# Track how many hits each database gives
db_hit_count = defaultdict(int)
not_found_count = 0

# Function to query each database for the membership number
def query_databases(membership_number):
    global not_found_count
    for db_path in db_paths:
        # Connect to the SQLite database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        try:
            # Query to find the IBX value
            query = "SELECT IBX FROM riders WHERE race_number = ?"
            cursor.execute(query, (membership_number,))
            result = cursor.fetchone()
        except Exception as e:
            print(f"Error querying {db_path}: {e}")
            result = None

        conn.close()

        if result:
            db_hit_count[db_path] += 1
            return result[0]

    # Not found in any DB
    not_found_count += 1
    return None

# Main function to process the CSV file
def process_csv(csv_file, debug=False):
    temp_file = csv_file + ".tmp"

    with open(csv_file, mode='r', newline='') as infile, open(temp_file, mode='w', newline='') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames + ['1BX']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)

        writer.writeheader()

        for row in reader:
            membership_number = row["Membership number"].strip()

            result = query_databases(membership_number)
            row['1BX'] = result if result is not None else "N/A"
            writer.writerow(row)

            if debug:
                print(f"[DEBUG] Membership number: {membership_number} -> 1BX: {row['1BX']}")

    os.replace(temp_file, csv_file)
    print(f"\n✅ CSV file '{csv_file}' has been updated with 1BX values.\n")

    # Summary
    print("📊 Summary of Database Hits:")
    total_hits = 0
    for db in db_paths:
        count = db_hit_count[db]
        total_hits += count
        print(f"  - {db}: {count} matches")

    print(f"\n🔍 Not found in any DB: {not_found_count}")
    print(f"📈 Total 1BX values populated: {total_hits}")
    print("✅ Done.")

# Argument parsing
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Update CSV with 1BX values from SQLite databases.")
    parser.add_argument("csv_file", help="Path to the CSV file")
    parser.add_argument("--debug", action="store_true", help="Enable debug output")

    args = parser.parse_args()
    process_csv(args.csv_file, debug=args.debug)

