#!/usr/bin/python3

# This will look at an input CSV file and output lines where Membership number is > 900

import argparse
import csv

def print_specific_fields_gt_900(csv_file):
    with open(csv_file, 'r', newline='') as file:
        reader = csv.DictReader(file)
        #print("Bib number,Full name,Membership number,Entry type,sex")
        for row in reader:
            membership_number = row.get("Membership number")
            if membership_number and int(membership_number) > 899:
                first_name = row.get("First name")
                last_name = row.get("Last name")
                full_name = f"{first_name} {last_name}"  # Concatenate first name and last name
                entry_type = row.get("Entry type")
                sex = row.get("sex")
                if first_name and last_name and entry_type and sex:
                    print(f"{row['Bib number']},{full_name},{membership_number},{entry_type},{sex},","Non League,N/A,N/A")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Print specific fields from CSV file where Membership number is greater than 900")
    parser.add_argument("csv_file", help="Path to the CSV file")
    args = parser.parse_args()

    print_specific_fields_gt_900(args.csv_file)

