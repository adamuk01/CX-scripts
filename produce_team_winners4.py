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
    WITH UnpivotedRiders AS (
    SELECT club_name,
           race_number, -- Assuming you have a unique race_number column
           1 AS round_number, COALESCE(r1_points, 0) AS points
    FROM riders
    UNION ALL
    SELECT club_name,
           race_number,
           2 AS round_number, COALESCE(r2_points, 0) AS points
    FROM riders
    UNION ALL
    SELECT club_name,
           race_number,
           3 AS round_number, COALESCE(r3_points, 0) AS points
    FROM riders
    UNION ALL
    SELECT club_name,
           race_number,
           4 AS round_number, COALESCE(r4_points, 0) AS points
    FROM riders
    UNION ALL
    SELECT club_name,
           race_number,
           5 AS round_number, COALESCE(r5_points, 0) AS points
    FROM riders
    UNION ALL
    SELECT club_name,
           race_number,
           6 AS round_number, COALESCE(r6_points, 0) AS points
    FROM riders
    UNION ALL
    SELECT club_name,
           race_number,
           7 AS round_number, COALESCE(r7_points, 0) AS points
    FROM riders
    UNION ALL
    SELECT club_name,
           race_number,
           8 AS round_number, COALESCE(r8_points, 0) AS points
    FROM riders
    UNION ALL
    SELECT club_name,
           race_number,
           9 AS round_number, COALESCE(r9_points, 0) AS points
    FROM riders
    UNION ALL
    SELECT club_name,
           race_number,
           10 AS round_number, COALESCE(r10_points, 0) AS points
    FROM riders
    UNION ALL
    SELECT club_name,
           race_number,
           11 AS round_number, COALESCE(r11_points, 0) AS points
    FROM riders
    UNION ALL
    SELECT club_name,
           race_number,
           12 AS round_number, COALESCE(r12_points, 0) AS points
    FROM riders
    ),
    RankedRiders AS (
      SELECT club_name,
             race_number,
             points,
             ROW_NUMBER() OVER (PARTITION BY club_name, round_number ORDER BY points DESC) AS rank
        FROM UnpivotedRiders
    )
    SELECT club_name,
         SUM(points) AS total_points
    FROM RankedRiders
    WHERE rank <= 6  -- Only include the top 6 riders per club for each round
    GROUP BY club_name
    HAVING SUM(points) > 0  -- Filter out clubs with zero total points
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

