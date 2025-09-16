#!/usr/bin/python3
# This will allocate a rider 999 points for a particular round
# Must provide database, rider number, and round (from 1 to 12)

import sqlite3
import os
import argparse
import logging

# Configure logging
LOG_FILE = "/nas/CX/NOTES/rider_average_points_update.log"
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

def update_rider_points(db_path, race_number, round_number):
    # Validate round_number
    if not 1 <= round_number <= 12:
        error_msg = "Error: Round number must be between 1 and 12."
        print(error_msg)
        logging.error(error_msg)
        return

    # Check if the database exists
    if not os.path.exists(db_path):
        error_msg = f"Error: Database '{db_path}' does not exist."
        print(error_msg)
        logging.error(error_msg)
        return

    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create dynamic column name based on the round number (e.g., r2_points)
    round_column = f"r{round_number}_points"

    try:
        # Fetch the rider's first name, surname, and current points for the specified round
        cursor.execute(f"""
            SELECT firstname, surname, {round_column}
            FROM riders
            WHERE race_number = ?
        """, (race_number,))
        rider = cursor.fetchone()

        if rider:
            firstname, surname, current_points = rider
            print(f"Rider found: {firstname} {surname}")
            print(f"Current points for round {round_number}: {current_points}")
            logging.info(
                f"Database: '{db_path}', Rider: {race_number} ({firstname} {surname}), "
                f"Current points for round {round_number}: {current_points}"
            )

            # Confirm before updating
            confirmation = input(f"Do you want to update {firstname} {surname}'s points for round {round_number} to 999? (yes/no): ")
            if confirmation.lower() == "yes":
                # Update the rider's points for the specified round to 999
                cursor.execute(f"""
                    UPDATE riders
                    SET {round_column} = 999
                    WHERE race_number = ?
                """, (race_number,))
                conn.commit()
                success_msg = (
                    f"Database: '{db_path}', Rider: {race_number} ({firstname} {surname}), "
                    f"Points for round {round_number} updated to 999."
                )
                print(success_msg)
                logging.info(success_msg)
            else:
                cancel_msg = f"Update canceled for Rider: {race_number} ({firstname} {surname}) in database '{db_path}'."
                print("Update canceled.")
                logging.info(cancel_msg)
        else:
            error_msg = f"No rider found with race number {race_number} in database '{db_path}'."
            print(error_msg)
            logging.warning(error_msg)
    except sqlite3.Error as e:
        error_msg = f"An error occurred while accessing database '{db_path}': {e}"
        print(error_msg)
        logging.error(error_msg)
    finally:
        # Close the connection
        conn.close()
        logging.info(f"Database connection to '{db_path}' closed.")

# Main function to parse command-line arguments
def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Update rider points in an SQLite database.")
    parser.add_argument("db_path", type=str, help="Path to the SQLite database file.")
    parser.add_argument("race_number", type=int, help="Race number of the rider (between 1 and 999).")
    parser.add_argument("round_number", type=int, help="Round number (between 1 and 12).")

    # Parse the arguments
    args = parser.parse_args()

    # Call the function to update the rider's points
    update_rider_points(args.db_path, args.race_number, args.round_number)

if __name__ == "__main__":
    main()

