#!/usr/bin/python3

# This will Look for riders with 999 points in any round and replace them with their real average points
# Run at the end of the season.

import sqlite3
import os
import math
import argparse
from decimal import Decimal, ROUND_HALF_UP

def update_999_with_average(db_path):
    # Check if the database exists
    if not os.path.exists(db_path):
        print(f"Error: Database '{db_path}' does not exist.")
        return

    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # List of all round points columns
    round_columns = [f"r{round_num}_points" for round_num in range(1, 13)]

    try:
        # Fetch all riders and their race_number, average_points, and round points
        cursor.execute("""
            SELECT race_number, firstname, surname, average_points, r1_points, r2_points, r3_points, r4_points,
                   r5_points, r6_points, r7_points, r8_points, r9_points, r10_points, r11_points, r12_points
            FROM riders
        """)

        riders = cursor.fetchall()

        # Iterate through each rider's data
        for rider in riders:
            race_number, firstname, surname, average_points, *points = rider

            updated = False  # To track if any updates are made for the rider

            # Iterate through each round column (r1_points to r12_points)
            for i, round_column in enumerate(round_columns):
                if points[i] == 999:  # If any points are 999
                    rounded_points = int(Decimal(average_points).quantize(Decimal('1'), rounding=ROUND_HALF_UP))
                    #rounded_points = round(average_points)  # Round average_points to the nearest integer

                    # Update the points with the rounded average_points value
                    cursor.execute(f"""
                        UPDATE riders
                        SET {round_column} = ?
                        WHERE race_number = ?
                    """, (rounded_points, race_number))

                    updated = True
                    print(f"Updated {round_column} for {firstname} {surname} (Race number: {race_number}) "
                          f"from 999 to {rounded_points}")

            # Commit changes after processing each rider if updates were made
            if updated:
                conn.commit()

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the connection
        conn.close()

# Main function to parse command-line arguments
def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Replace 999 points with average points in an SQLite database.")
    parser.add_argument("db_path", type=str, help="Path to the SQLite database file.")

    # Parse the arguments
    args = parser.parse_args()

    # Call the function to update 999 points with average points
    update_999_with_average(args.db_path)

if __name__ == "__main__":
    main()

