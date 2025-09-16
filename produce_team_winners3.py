#!/usr/bin/python3

# This will output the team patipation award - it starts with each round and picks the top 6 riders scores. Filters out non scoring clubs
# Checking the results...
# Highest scoring 6 riders from each club to score each round 
# BUG in this one....

import sqlite3
import argparse

parser = argparse.ArgumentParser(description="Update race average in DB file.")
parser.add_argument("input_file", help="Path to the input DB file")
args = parser.parse_args()

db_path = args.input_file

def get_total_points_per_club(db_path):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Construct the SQL query to retrieve the total points for each club across all rounds, considering only top 6 riders/results for each club in each round
    sql_query = """
        WITH RankedRiders AS (
            SELECT club_name, 
                   COALESCE(r1_points, 0) + COALESCE(r2_points, 0) + COALESCE(r3_points, 0) AS total_points,
                   ROW_NUMBER() OVER (PARTITION BY club_name ORDER BY COALESCE(r1_points, 0) + COALESCE(r2_points, 0) + COALESCE(r3_points, 0) + COALESCE(r4_points, 0) + COALESCE(r5_points, 0) + COALESCE(r6_points, 0) + COALESCE(r7_points, 0) + COALESCE(r8_points, 0) + COALESCE(r9_points, 0) + COALESCE(r10_points, 0) + COALESCE(r11_points, 0) + COALESCE(r12_points, 0) DESC) AS rank
            FROM riders
        )
        SELECT club_name, 
               SUM(total_points) AS total_points
        FROM RankedRiders
        WHERE rank <= 6
        GROUP BY club_name
        HAVING SUM(total_points) > 0  -- Filter out clubs with total points equal to zero
        ORDER BY total_points DESC;
    """

    # Execute the query
    cursor.execute(sql_query)
    total_points_per_club = cursor.fetchall()

    # Close the database connection
    conn.close()

    return total_points_per_club

if __name__ == "__main__":
    # Example usage
    total_points_per_club = get_total_points_per_club(db_path)
    for row in total_points_per_club:
        print(row)

