#!/bin/python3
# Load last year's data from CSV file into the database

import sqlite3
import csv
import sys

def update_database(database_file, csv_file):
    print(f"Connecting to database: {database_file}")
    
    # Connect to SQLite database
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()

    print(f"Opening CSV file: {csv_file}")
    
    # Counters for summary
    total_riders = 0
    riders_found = 0
    riders_not_found = 0

    # Open and read the CSV file
    with open(csv_file, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        
        # Iterate over each row in the CSV file
        for row in csv_reader:
            total_riders += 1
            firstname = row['First name']
            surname = row['Last name']
            YOB = row['YOB']
            race_category_current_year = row['race_category_current_year']
            races_finished = row['races_finished']
            total_points = row['total_points']
            average_position = row['average_position']
            average_points = row['average_points']

            print(f"\nChecking rider: {firstname} {surname} (YOB: {YOB})")

            # Check if the rider exists in the SQLite database
            cursor.execute("SELECT * FROM riders WHERE firstname=? AND surname=? AND YOB=?", (firstname, surname, YOB))
            rider = cursor.fetchone()

            if rider:
                riders_found += 1
                print(f"✅ Rider found in database: {firstname} {surname} (YOB: {YOB})")
                print("Updating database with the following details:")
                print(f" - Race Category Previous Year: {race_category_current_year}")
                print(f" - Races Finished Last Year: {races_finished}")
                print(f" - Average Position Last Year: {average_position}")
                print(f" - Total Points Last Year: {total_points}")
                print(f" - Average Points Last Year: {average_points}")

                # Update the SQLite database with the values from the CSV file
                cursor.execute("""
                    UPDATE riders 
                    SET race_category_previous_year=?, 
                        races_finished_last_year=?, 
                        average_position_last_year=?, 
                        total_points_last_year=?, 
                        average_points_last_year=? 
                    WHERE firstname=? AND surname=? AND YOB=?""",
                    (race_category_current_year, races_finished, average_position, total_points, average_points, firstname, surname, YOB))
                
                conn.commit()
                print("✅ Update committed to the database.")
            else:
                riders_not_found += 1
                print(f"❌ Rider NOT found in database: {firstname} {surname} (YOB: {YOB})")

    print("\nClosing database connection.")
    # Close the database connection
    conn.close()
    print("Database connection closed.")

    # Summary Report
    print("\n===== Summary Report =====")
    print(f"Total riders processed: {total_riders}")
    print(f"✅ Riders found and updated: {riders_found}")
    print(f"❌ Riders not found: {riders_not_found}")
    print("==========================")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <database_file> <csv_file>")
    else:
        database_file = sys.argv[1]
        csv_file = sys.argv[2]
        update_database(database_file, csv_file)

