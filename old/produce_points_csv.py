#!/usr/bin/python3

import sqlite3
import csv
import argparse


parser = argparse.ArgumentParser(description="Update race average in DB file.")
parser.add_argument("input_file", help="Path to the input DB file")
parser.add_argument("category", help="Rider category - Under 8 Under 6 etc..")
args = parser.parse_args()

db_file = args.input_file
category = args.category

print("Creating CSV file for points from ",db_file,"with category",category)


def calculate_points(position):
    # Calculate points based on finishing position
    return max(0, 100 - position + 1)

def output_race_results(db_file, output_csv, gender, category):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Query the database to fetch rider race results
    # cursor.execute("SELECT race_number, full_name, club_name, r1_cat_position, r2_cat_position, r3_cat_position, r4_cat_position, r5_cat_position, r6_cat_position, r7_cat_position, r8_cat_position, r9_cat_position, r10_cat_position, r11_cat_position, r12_cat_position FROM riders WHERE race_category = 'Under 6' AND sex = 'Female'")
    cursor.execute("SELECT race_number, full_name, club_name, r1_cat_position, r2_cat_position, r3_cat_position, r4_cat_position, r5_cat_position, r6_cat_position, r7_cat_position, r8_cat_position, r9_cat_position, r10_cat_position, r11_cat_position, r12_cat_position FROM riders WHERE sex = ? AND race_category LIKE ?", (gender, category))
    rows = cursor.fetchall()

    # Calculate points for each rider across all races
    rider_points = {}
    for row in rows:
        rider_number = row[0]
        rider_name = row[1]
        club_name = row[2]
        rider_points.setdefault((rider_number, rider_name, club_name), [0] * 12)  # Initialize points list for each rider
        
        for i, position in enumerate(row[4:], start=0):  # Start from race_position1
            if position is not None:
                rider_points[(rider_number, rider_name, club_name)][i] = calculate_points(position)

    # Calculate best 10 total points for each rider
    rider_best_10_points = {rider: sum(sorted(points, reverse=True)[:10]) for rider, points in rider_points.items()}

    # Sort riders based on best 10 total points in descending order
    sorted_riders = sorted(rider_best_10_points, key=lambda x: rider_best_10_points[x], reverse=True)

    # Write the sorted results to a CSV file
    with open(output_csv, 'w', newline='') as csvfile:
        fieldnames = ['Position', 'Rider Number', 'Rider Name', 'Club Name'] + [f'Race {i+1}' for i in range(12)] + ['Best 10 Total']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for idx, rider in enumerate(sorted_riders, start=1):
            rider_number, rider_name, club_name = rider
            points = rider_points[rider]
            best_10_total = rider_best_10_points[rider]
            writer.writerow({'Position': idx, 'Rider Number': rider_number, 'Rider Name': rider_name, 'Club Name': club_name, **{f'Race {i+1}': points[i] for i in range(12)}, 'Best 10 Total': best_10_total})


    conn.close()

# Find Females
gender = 'Female'
output_csv = 'points-' + gender + "-" + category + '.csv'
output_race_results(db_file, output_csv, gender, category)

# Find Females
gender = 'Male'
output_csv = 'points-' + gender + "-" + category + '.csv'
output_race_results(db_file, output_csv, gender, category)
