#!/usr/bin/python3

# This will look at the riderHQ input deck, cross refernce by name and YOB for the AllRiders.db and update the new database with average_points_last_year
# Probably need to do the same for "races_finished_last_year" and "total_points_last_year" 
# NOTE - UNTESTED!

import sqlite3
import csv
import argparse

def update_database(csv_file, source_db, other_db):
    # Connect to the source database
    source_conn = sqlite3.connect(source_db)
    source_cursor = source_conn.cursor()

    # Connect to the other database
    other_conn = sqlite3.connect(other_db)
    other_cursor = other_conn.cursor()

    # Read surnames, first names, and years of birth from the CSV file
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header line
        for row in reader:
            surname = row[4].lower()  # Convert surname to lowercase
            first_name = row[3].lower()  # Convert first name to lowercase
            year_of_birth = row[12]  # Column index for year of birth
            # Query the source database for final_average_points_last_year
            source_cursor.execute("SELECT average_points_last_year FROM riders WHERE LOWER(surname) = ? AND LOWER(firstname) = ? AND YOB = ?", (surname, first_name, year_of_birth))
            result = source_cursor.fetchone()
            if result:
                final_average_points = result[0]
                # Update the other database with the final_average_points_last_year
                other_cursor.execute("UPDATE riders SET average_points_last_year = ? WHERE LOWER(surname) = ? AND LOWER(firstname) = ? AND YOB = ?", (final_average_points, surname, first_name, year_of_birth))
                print(f"Updated record for {first_name} {surname}, Year of Birth: {year_of_birth}, Final Average Points Last Year: {final_average_points}")
            else:
                print(f"No match found for {first_name} {surname}, Year of Birth: {year_of_birth}")

    # Commit changes and close connections for both databases
    source_conn.commit()
    source_conn.close()
    other_conn.commit()
    other_conn.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Update another SQLite database using surnames, first names, and years of birth from a CSV file")
    parser.add_argument("csv_file", help="Path to the RiderHQ input CSV file for this year")
    parser.add_argument("source_db", help="Path to the source SQLite database file. i.e last years data")
    parser.add_argument("other_db", help="Path to the other SQLite database file, i.e this years data")
    args = parser.parse_args()

    update_database(args.csv_file, args.source_db, args.other_db)

