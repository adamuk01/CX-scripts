#!/usr/bin/python3

# This script will update the databases, updating the best 9 races AND the total points for the rider
# MAY need to change this if some rounds are cancelled!

import sqlite3
import argparse

def update_top_ten_field(db_file):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Query the database to fetch user records
    cursor.execute("SELECT race_number, r1_points, r2_points, r3_points, r4_points, r5_points, r6_points, r7_points, r8_points, r9_points, r10_points, r11_points, r12_points FROM riders")
    rows = cursor.fetchall()
#    print (rows)

    for row in rows:
        race_number = row[0]
#        print (race_number)
#        integers = sorted(filter(lambda x: x is not None, row[1:]), reverse=True)
#        integers = sorted(filter(lambda x: isinstance(x, int), row[1:]), reverse=True) # This was before we added 999 filter!
        integers = sorted(filter(lambda x: isinstance(x, int) and x != 999, row[1:]), reverse=True)

#        print (integers)
        top_x_sum = sum(integers[:10]) # CHANGE THIS TO BE THE NUMBER OF ROUNDS THAT COUNT - I assume 9 - might change if rounds are cancelled!
        all_races_sum = sum(integers[:12])
        
        # Update the "top_ten" field for the current user
        cursor.execute("UPDATE riders SET best_X_points = ? WHERE race_number = ?", (top_x_sum, race_number))
        cursor.execute("UPDATE riders SET total_points = ? WHERE race_number = ?", (all_races_sum, race_number))

    conn.commit()
    conn.close()

# Example usage:

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Update race count in DB file.")
	parser.add_argument("input_file", help="Path to the input DB file")
	args = parser.parse_args()

	db_file = args.input_file

	print("Updating database",db_file,"with new  top 9 values")
	update_top_ten_field(db_file)
