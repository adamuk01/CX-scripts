#!/usr/bin/python3

import sqlite3
import csv
import argparse

def dump_table_to_csv(db_file, table_name, csv_file):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Get column names from the specified table
    cursor.execute(f"PRAGMA table_info({table_name})")
    column_names = [column[1] for column in cursor.fetchall()]

    # Execute a query to select data from the specified table
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()

    # Write the selected data to the CSV file
    with open(csv_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(column_names)
        writer.writerows(rows)

    conn.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Dump SQLite table to a CSV file.")
    parser.add_argument("db_file", help="Path to the SQLite database file")
    parser.add_argument("csv_file", help="Path to the CSV file to create")
    args = parser.parse_args()

    table_name = 'riders'

    dump_table_to_csv(args.db_file, table_name, args.csv_file)


