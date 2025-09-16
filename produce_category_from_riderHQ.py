#!/usr/bin/env python3
import csv
import sys
import argparse
from datetime import datetime

def parse_full_year(dob_str):
    """
    Convert date strings like '30-Jan-57' to full 4-digit years (e.g., 1957 or 2057).
    Uses cutoff of 25 to determine century.
    """
    try:
        #dob = datetime.strptime(dob_str.strip(), "%d-%b-%y")
        dob = datetime.strptime(dob_str.strip(), "%d-%b-%Y") 
        year = dob.year
        # Adjust century if needed
        if year >= 2025:
            year -= 100  # Convert e.g., 2057 → 1957
        return year
    except Exception as e:
        print(f"[ERROR] Could not parse date: '{dob_str}' ({e})")
        return None

def get_age_category(year):
    """
    Return category based on year of birth.
    """
    if year is None:
        return "Unknown"
    if year >= 2020:
        return "Under-6"
    elif year >= 2018:
        return "Under-8"
    elif year >= 2016:
        return "Under-10"
    elif year >= 2014:
        return "Under-12"
    elif year >= 2012:
        return "Under-14"
    elif year >= 2010:
        return "Under-16"
    elif year >= 2008:
        return "Junior"
    elif year >= 2002:
        return "Under-23"
    elif year >= 1986:
        return "Senior"
    elif year >= 1981:
        return "Masters 40-44"
    elif year >= 1976:
        return "Masters 45-49"
    elif year >= 1971:
        return "Masters 50-54"
    elif year >= 1966:
        return "Masters 55-59"
    elif year >= 1961:
        return "Masters 60-64"
    elif year >= 1956:
        return "Masters 65-69"
    elif year >= 1951:
        return "Masters 70-74"
    else:
        return "Masters 75+"

def categorize_dob(input_file, output_file, debug=False):
    with open(input_file, 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        fieldnames = reader.fieldnames + ['Age Category']
        category_count = {}

        with open(output_file, 'w', newline='') as output_csv:
            writer = csv.DictWriter(output_csv, fieldnames=fieldnames)
            writer.writeheader()

            num_rows = 0

            for row in reader:
                dob_str = row.get('Date of birth', '')
                year = parse_full_year(dob_str)
                category = get_age_category(year)
                row['Age Category'] = category

                category_count[category] = category_count.get(category, 0) + 1
                writer.writerow(row)
                num_rows += 1

                if debug:
                    print(f"[DEBUG] Row {num_rows}: DOB = {dob_str}, Year = {year}, Category = {category}")

    return num_rows, category_count

def main():
    parser = argparse.ArgumentParser(description="Categorize CSV based on Date of Birth")
    parser.add_argument("input_file", help="Path to the input CSV file")
    parser.add_argument("output_file", help="Path to the output CSV file")
    parser.add_argument("-D", "--debug", action="store_true", help="Enable debug output")

    args = parser.parse_args()
    num_rows, category_count = categorize_dob(args.input_file, args.output_file, debug=args.debug)

    print("\nProcessing complete.")
    print(f"Total rows processed: {num_rows}")
    print("Category breakdown:")
    for cat, count in category_count.items():
        print(f"  {cat}: {count}")
    print(f"Updated data saved to: {args.output_file}")

if __name__ == "__main__":
    main()

