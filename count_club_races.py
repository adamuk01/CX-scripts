#!/usr/bin/python3

import sqlite3
import argparse

import sqlite3

def count_races_per_club(db_file):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    # Query the database to count races per club and order by total races in descending order
    cursor.execute("SELECT club_name, SUM(races_finished) AS total_races FROM riders GROUP BY club_name ORDER BY total_races DESC")
    rows = cursor.fetchall()
    
    # Display the results with rankings
    print("Position, Club, Total Races")
    for position, row in enumerate(rows, start=1):  # Enumerate starting from 1 for ranking
        club, total_races = row
        print(f"{position}, {club}, {total_races}")
    
    conn.close()

# Example usage:
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calculate race count from DB file.")
    parser.add_argument("input_file", help="Path to the input DB file")
    args = parser.parse_args()

    db_file = args.input_file

#    print("Calculating races run by club name from ",db_file)

    count_races_per_club(db_file)

