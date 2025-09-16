#!/usr/bin/python3

# This will Set average points 999 back to zero. Used for team points...
# Must provide database, Which will be combined database

import sqlite3
import os
import argparse

def update_999_to_zero(db_path):
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
        # Check and update points for each round column (r1_points to r12_points)
        for round_column in round_columns:
            # Fetch riders with 999 in the current round
            cursor.execute(f"""
                SELECT race_number, firstname, surname, {round_column}
                FROM riders
                WHERE {round_column} = 999
            """)

            riders = cursor.fetchall()

            if riders:
                for rider in riders:
                    race_number, firstname, surname, points = rider
                    print(f"Found 999 points for {firstname} {surname} (Race number: {race_number}) in {round_column}")

                    # Update the 999 points to 0
                    cursor.execute(f"""
                        UPDATE riders
                        SET {round_column} = 0
                        WHERE race_number = ?
                    """, (race_number,))

                # Commit the changes for each column
                conn.commit()
                print(f"Updated {len(riders)} riders' {round_column} points from 999 to 0.")
            else:
                print(f"No riders found with 999 points in {round_column}")

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the connection
        conn.close()

# Main function to parse command-line arguments
def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Update 999 points to 0 in an SQLite database.")
    parser.add_argument("db_path", type=str, help="Path to the SQLite database file.")

    # Parse the arguments
    args = parser.parse_args()

    # Call the function to update 999 points to 0
    update_999_to_zero(args.db_path)

if __name__ == "__main__":
    main()

