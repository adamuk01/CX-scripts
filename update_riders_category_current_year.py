#!/usr/bin/python3

# This script will examine the database and update the race_category_current_year based on the YOB and gender
# Currently setup for 2025-26 year

import sqlite3
import argparse

def get_race_category(yob):
    if yob in [2020, 2021]:        # Shifted forward by 1 year
        return "U6"
    elif yob in [2018, 2019]:
        return "U8"
    elif yob in [2016, 2017]:
        return "U10"
    elif yob in [2014, 2015]:
        return "U12"
    elif yob in [2012, 2013]:
        return "U14"
    elif yob in [2010, 2011]:
        return "U16"
    elif yob in [2008, 2009]:
        return "Jun"
    elif 2002 <= yob <= 2007:
        return "U23"
    elif 1986 <= yob <= 2001:
        return "Sen"
    elif 1981 <= yob <= 1985:
        return "M40"
    elif 1976 <= yob <= 1980:
        return "M45"
    elif 1971 <= yob <= 1975:
        return "M50"
    elif 1966 <= yob <= 1970:
        return "M55"
    elif 1961 <= yob <= 1965:
        return "M60"
    elif 1956 <= yob <= 1960:
        return "M65"
    elif 1910 <= yob <= 1955:
        return "M70"

    # Add more ranges as needed
    else:
        return None  # or some default value or action if the YOB is outside these ranges

def update_race_category(database_path):
    # Connect to the SQLite database
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    # Select the required fields from the database
    cursor.execute("SELECT id, YOB, gender FROM riders")
    rows = cursor.fetchall()

    for row in rows:
        id, yob, gender = row
        # Calculate the new race category based on the YOB
        race_category = get_race_category(yob)

        if race_category:
            # Append gender to the race category
            if gender.lower() == "female":
                race_category += "F"
            elif gender.lower() == "male":
                race_category += "M"

            # Update the race_category_current_year field in the database
            cursor.execute(
                "UPDATE riders SET race_category_current_year = ? WHERE id = ?",
                (race_category, id)
            )

    # Commit the changes and close the connection
    conn.commit()
    conn.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Update race category in SQLite database.')
    parser.add_argument('database', type=str, help='Path to the SQLite database file.')
    args = parser.parse_args()

    update_race_category(args.database)

