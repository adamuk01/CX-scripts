#!/usr/bin/python3

# I ran this at the end of the season, it counts up the total mumber of races for each category - so prize money can be allocated.

import sqlite3
import os

# List of SQLite database file paths
database_files = ["Vet50.db", "Women.db" , "Youth.db" , "Senior.db"]  # Replace with actual paths

# Dictionary to store total races per category
category_totals = {}

for db_file in database_files:
    # Connect to the database
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Query to count races finished grouped by category
    query = """
    SELECT race_category_current_year, SUM(races_finished)
    FROM riders  -- Replace 'riders' with the actual table name
    GROUP BY race_category_current_year
    """

    # Execute the query and fetch results
    cursor.execute(query)
    results = cursor.fetchall()

    # Aggregate the results
    for category, total_races in results:
        if category in category_totals:
            category_totals[category] += total_races
        else:
            category_totals[category] = total_races

    # Close the database connection
    conn.close()

# Print the total races for each category
for category, total in category_totals.items():
    print(f"Category: {category}, Total Races: {total}")


