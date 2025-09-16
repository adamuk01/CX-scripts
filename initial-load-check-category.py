#!/bin/python3
# Check the rider to see if they have change category IF they have update race_category_update & take off 10 points
# Notice we can add on 5 points - just change line 34/35 below

import sqlite3
import sys

def update_race_category_and_points(database_file):
    # Connect to SQLite database
    conn = sqlite3.connect(database_file)
    cursor = conn.cursor()

    # Select records where race_category_previous_year is not equal to race_category_current_year
    cursor.execute("SELECT * FROM riders WHERE race_category_previous_year != race_category_current_year")
    riders_to_update = cursor.fetchall()

    # Get column names
    column_names = [description[0] for description in cursor.description]

    # Update race_category to 'Y' and reduce average_points_last_year by 10 for selected riders
    for rider in riders_to_update:
        rider_dict = dict(zip(column_names, rider))

        if rider_dict['average_points_last_year'] is None:
            print(f"Skipping record with null average_points_last_year: {rider_dict}")
            continue

        try:
            average_points_last_year = int(rider_dict['average_points_last_year'])
        except ValueError:
            print(f"Skipping record with invalid average_points_last_year: {rider_dict}")
            continue

        new_pos = max(0, average_points_last_year - 5)  # Reduce points by 10, ensure it doesn't go negative
#        new_pos = average_points_last_year + 5  # Increase points by 5

        # Update the record
        cursor.execute("UPDATE riders SET race_category_update='Y', average_points_last_year=? WHERE id=?", (new_pos, rider_dict['id']))
        conn.commit()

        # Print the changes
        print(f"Updated record for {rider_dict['firstname']} {rider_dict['surname']} (id={rider_dict['id']}):")
        print(f"  - race_category: 'Y'")
        print(f"  - average_points_last_year: {rider_dict['average_points_last_year']} -> {new_pos}")

    # Close the database connection
    conn.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <database_file>")
    else:
        database_file = sys.argv[1]
        update_race_category_and_points(database_file)

