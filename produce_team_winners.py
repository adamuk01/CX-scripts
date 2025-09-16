#!/usr/bin/python3
#
# This will output the team patipation award - it starts with each round and picks the top 6 riders scores. It is more for debugging!
# Checking the results...
# Highest scoring 6 riders from each club to score each round 

import sqlite3
import argparse

parser = argparse.ArgumentParser(description="Produce team partipation award.")
parser.add_argument("input_file", help="Path to the input DB file")
args = parser.parse_args()

db_path = args.input_file

def get_total_points_per_round_per_club(db_path):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Construct the SQL query to retrieve the total points for each club for each round
    sql_query = """
        WITH RankedRiders AS (
            SELECT club_name, 
                   round_number, 
                   round_points,
                   ROW_NUMBER() OVER (PARTITION BY club_name, round_number ORDER BY round_points DESC) AS rank
            FROM (
                SELECT club_name, 
                       'r1_points' AS round_number, 
                       r1_points AS round_points
                FROM riders
                UNION ALL
                SELECT club_name, 
                       'r2_points' AS round_number, 
                       r2_points AS round_points
                FROM riders
                UNION ALL
                SELECT club_name, 
                       'r3_points' AS round_number, 
                       r3_points AS round_points
                FROM riders
                UNION ALL
                SELECT club_name, 
                       'r4_points' AS round_number, 
                       r4_points AS round_points
                FROM riders
                UNION ALL
                SELECT club_name, 
                       'r5_points' AS round_number, 
                       r5_points AS round_points
                FROM riders
                UNION ALL
                SELECT club_name, 
                       'r6_points' AS round_number, 
                       r6_points AS round_points
                FROM riders
                UNION ALL
                SELECT club_name, 
                       'r7_points' AS round_number, 
                       r7_points AS round_points
                FROM riders
                UNION ALL
                SELECT club_name, 
                       'r8_points' AS round_number, 
                       r8_points AS round_points
                FROM riders
                UNION ALL
                SELECT club_name, 
                       'r9_points' AS round_number, 
                       r9_points AS round_points
                FROM riders
                UNION ALL
                SELECT club_name, 
                       'r10_points' AS round_number, 
                       r10_points AS round_points
                FROM riders
                UNION ALL
                SELECT club_name, 
                       'r11_points' AS round_number, 
                       r11_points AS round_points
                FROM riders
                UNION ALL
                SELECT club_name, 
                       'r12_points' AS round_number, 
                       r12_points AS round_points
                FROM riders
                -- Add more UNION ALL statements for additional rounds if needed
            )
        )
        SELECT club_name, 
               round_number, 
               SUM(round_points) AS total_points
        FROM RankedRiders
        WHERE rank <= 6
        GROUP BY club_name, round_number
        ORDER BY club_name, round_number;
    """

    # Execute the query
    cursor.execute(sql_query)
    total_points_per_round_per_club = cursor.fetchall()

    # Close the database connection
    conn.close()

    return total_points_per_round_per_club

if __name__ == "__main__":
    # Example usage
    total_points_per_round_per_club = get_total_points_per_round_per_club(db_path)
    for row in total_points_per_round_per_club:
        print(row)

