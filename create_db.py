#!/usr/bin/python3

import sqlite3
import argparse

parser = argparse.ArgumentParser(description="Create a SQLite DB file.")
parser.add_argument("output_file", help="Path to the output db file")
args = parser.parse_args()

output_file = args.output_file

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect(output_file + '.db')
c = conn.cursor()

# Create a table to store rider information
c.execute('''CREATE TABLE IF NOT EXISTS riders (
                id INTEGER PRIMARY KEY,
		BC_number INTEGER,
                race_number INTEGER,
                firstname TEXT,
                surname TEXT,
                gender TEXT,
                club_name TEXT,

                race_category_current_year TEXT,
                race_category_previous_year TEXT,
                race_category_update TEXT,

                average_position_last_year REAL,
                total_points_last_year INTEGER,
                average_points_last_year REAL,
                races_finished_last_year INTEGER,

		        DOB TEXT,
		        YOB INTEGER,
                IBX TEXT,

                average_position REAL,
                average_points REAL,
                races_finished INTEGER,
                total_points INTEGER,
                best_X_points INTEGER,

                r1_cat_position INTEGER,
                r1_overall_position INTEGER,
                r1_points INTEGER,

                r2_cat_position INTEGER,
                r2_overall_position INTEGER,
                r2_points INTEGER,

                r3_cat_position INTEGER,
                r3_overall_position INTEGER,
                r3_points INTEGER,

                r4_cat_position INTEGER,
                r4_overall_position INTEGER,
                r4_points INTEGER,

                r5_cat_position INTEGER,
                r5_overall_position INTEGER,
                r5_points INTEGER,

                r6_cat_position INTEGER,
                r6_overall_position INTEGER,
                r6_points INTEGER,

                r7_cat_position INTEGER,
                r7_overall_position INTEGER,
                r7_points INTEGER,

                r8_cat_position INTEGER,
                r8_overall_position INTEGER,
                r8_points INTEGER,

                r9_cat_position INTEGER,
                r9_overall_position INTEGER,
                r9_points INTEGER,

                r10_cat_position INTEGER,
                r10_overall_position INTEGER,
                r10_points INTEGER,

                r11_cat_position INTEGER,
                r11_overall_position INTEGER,
                r11_points INTEGER,

                r12_cat_position INTEGER,
                r12_overall_position INTEGER,
                r12_points INTEGER
             )''')


# Commit changes and close connection
conn.commit()
conn.close()
