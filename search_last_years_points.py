#!/usr/bin/python3

# This search through the CSV file provided by RiderHQ - looking at First name, Surname and Year of birth - it then looks at the database for the average_points_last_year - idea we can use this to update the new database!

import sqlite3
import csv
import argparse

def query_database(csv_file, database_file):
    # Connect to the SQLite database
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()

    # Read surnames, first names, and years of birth from the CSV file
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header line
        for row in reader:
            surname = row[4].lower()  # Convert surname to lowercase
            first_name = row[3].lower()  # Convert first name to lowercase
            year_of_birth = row[12]  # Column index for year of birth
            # Query the database for average_points_last_year
            cursor.execute("SELECT average_points_last_year FROM riders WHERE LOWER(surname) = ? AND LOWER(firstname) = ? AND YOB = ?", (surname, first_name, year_of_birth))
            results = cursor.fetchall()
            if results:
                print(f"Found {len(results)} matches for First Name: {row[2]}, Surname: {row[3]}, Year of Birth: {year_of_birth}:")
                for result in results:
                    final_average_points = result[0]
                    print(f"  - Final Average Points Last Year: {final_average_points}")
            else:
                print(f"No match for First Name: {row[3]}, Surname: {row[4]}, Year of Birth: {year_of_birth}")

    # Close the database connection
    conn.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Query SQLite database using surnames, first names, and years of birth from a CSV file")
    parser.add_argument("csv_file", help="Path to the CSV file")
    parser.add_argument("database_file", help="Path to the SQLite database file")
    args = parser.parse_args()

    query_database(args.csv_file, args.database_file)

