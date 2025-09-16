#!/usr/bin/python3

import sqlite3
import csv
import argparse

def get_name_from_database(conn, bc_number, riderHQ_number):
    cursor = conn.cursor()
    name = None

    if bc_number is not None:
        cursor.execute("SELECT surname FROM riders WHERE BC_number = ?", (bc_number,))
        row = cursor.fetchone()
        if row:
            name = row[0]
    elif riderHQ_number is not None:
        cursor.execute("SELECT surname FROM riders WHERE riderHQ_id = ?", (riderHQ_number,))
        row = cursor.fetchone()
        if row:
            name = row[0]

    if name is None:
        return "Name not found"
    else:
        return name

def main(database_file, csv_file):
    # Connect to the SQLite database
    conn = sqlite3.connect(database_file)

    # Open the CSV file and iterate through its rows
    with open(csv_file, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)  # Skip the header row if present
        for row in csv_reader:
            bc_number = row[7] if row[7] != '' else None
            riderHQ_number = row[1] if row[1] != '' else None
            firstname = row[3] if row[3] != '' else None
            surname = row[4] if row[4] != '' else None
            print(f"Processing : {firstname}, {surname} ")
            name = get_name_from_database(conn, bc_number, riderHQ_number)
            print(f"BC Number: {bc_number}, RiderHQ Number: {riderHQ_number}, Name: {name}")

    # Close the database connection
    conn.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Query database using BC number or RiderHQ number from CSV")
    parser.add_argument("database_file", help="Path to the SQLite database file")
    parser.add_argument("csv_file", help="Path to the CSV file")
    args = parser.parse_args()

    main(args.database_file, args.csv_file)


