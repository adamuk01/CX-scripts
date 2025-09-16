#!/usr/bin/python3

# This script will update the databases, updating the number of races finished

import sqlite3
import argparse

def update_positive_values(db_file):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    try:
        # Retrieve records and update positive_values field
        cursor.execute("SELECT id,r1_overall_position,r2_overall_position,r3_overall_position,r4_overall_position,r5_overall_position,r6_overall_position,r7_overall_position,r8_overall_position,r9_overall_position,r10_overall_position,r11_overall_position,r12_overall_position FROM riders")
        records = cursor.fetchall()
        for record in records:
            positive_count = sum(1 for field in record if field is not None) - 1
            cursor.execute("UPDATE riders SET races_finished = ? WHERE id = ?", (positive_count, record[0]))

#            print ("UPDATE riders SET races_finished = ",positive_count," WHERE id = ?",record[0])

        # Commit changes
        conn.commit()
        print("Updated races_finished value for each rider successfully.")

    except sqlite3.Error as e:
        print("SQLite error:", e)

    finally:
        # Close the connection
        conn.close()

# Example usage:

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Update race count in DB file.")
	parser.add_argument("input_file", help="Path to the input DB file")
	args = parser.parse_args()

	db_file = args.input_file

	print("Updating database",db_file,"with new values")
	update_positive_values(db_file)

