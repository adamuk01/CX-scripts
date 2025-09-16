#!/usr/bin/python3

# This will filter the entire gridding sheet, for each race to pick out the riders for this weeks race
# Idea is to dump ALL the gridding data from the database, THEN filter it by who has entered this week
# We need the gridding file to be filtered first - so non-league riders also have a number i.e > 800
# Ths will only grid league members - you then have to add the non-league members to the end of the file.

import csv
import argparse

def create_membership_dict(csv_file):
    membership_dict = {}
    with open(csv_file, 'r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
#            print(row)  # Print each row to see its contents
            membership_number = row.get("Membership number")
            if membership_number:
                membership_dict[membership_number] = row
    return membership_dict


def process_race_data(input_csv, output_csv, membership_csv):
    membership_dict = create_membership_dict(membership_csv)

    total_matched = 0
    total_unmatched = 0

    with open(input_csv, 'r', newline='') as in_file, open(output_csv, 'w', newline='') as out_file:
        reader = csv.DictReader(in_file)
        input_fieldnames = reader.fieldnames  # Get fieldnames from the first row
        writer = csv.DictWriter(out_file, fieldnames=input_fieldnames)
        writer.writeheader()
        for row in reader:
            race_number = row.get("Race No.")
            if race_number in membership_dict:
                writer.writerow(row)
                total_matched += 1
            else:
                total_unmatched += 1

        print(f"Total entries in gridding input CSV: {total_matched + total_unmatched}")
        print(f"Entries matched with membership CSV - league members entered race: {total_matched}")
        print(f"Entries not matched with membership CSV: {total_unmatched}")
        print(f"Total entries in race (league + non-league members): {len(membership_dict)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Match race data with membership data")
    parser.add_argument("input_csv", help="Path to the CSV file with ALL league gridding data for category")
    parser.add_argument("output_csv", help="Path to the output CSV file")
    parser.add_argument("membership_csv", help="Path to the race input file with all riders league + non-league")
    args = parser.parse_args()

    print("Summary:")
    print("Processing:", args.input_csv)

    process_race_data(args.input_csv, args.output_csv, args.membership_csv)

