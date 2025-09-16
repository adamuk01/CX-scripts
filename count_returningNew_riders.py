#!/usr/bin/env python3
"""
count_riders.py

This script connects to a rider SQLite database and counts how many riders
have a race_category_previous_year set (returning riders) versus those
with it NULL (new riders).
"""

import sqlite3
import argparse

def count_riders(db_path):
    """
    Connects to the SQLite database and counts riders with and without
    a previous year race category.
    """
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    # Count riders who have a previous year category (returning riders)
    cur.execute("""
        SELECT COUNT(*) 
        FROM riders 
        WHERE race_category_previous_year IS NOT NULL;
    """)
    returning = cur.fetchone()[0]

    # Count riders who do not have a previous year category (new riders)
    cur.execute("""
        SELECT COUNT(*) 
        FROM riders 
        WHERE race_category_previous_year IS NULL;
    """)
    new = cur.fetchone()[0]

    conn.close()
    return returning, new

if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description="Count riders with/without a previous year race category"
    )
    parser.add_argument(
        "database",
        help="Path to the SQLite rider database file"
    )
    args = parser.parse_args()

    # Run the count function
    returning, new = count_riders(args.database)

    # Print results
    print(f"Returning riders (raced last year): {returning}")
    print(f"New riders (no previous category): {new}")
    print(f"Total riders: {returning + new}")

