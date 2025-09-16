#!/usr/bin/python3
#!/usr/bin/python3
import csv
import argparse

def sort_csv(csv_file, debug=False):
    """
    Reads a CSV file, sorts it based on 'Entry type' and 'Last name',
    and writes the sorted data back to the file.

    Args:
    - csv_file: Path to the input CSV file.
    - debug: Boolean flag to print debug information.

    Returns:
    - The number of rows sorted (excluding the header).
    """

    # Read the CSV file into a list of dictionaries
    with open(csv_file, 'r', newline='') as file:
        reader = csv.DictReader(file)
        data = list(reader)  # Reading all rows except the header

        # Debug: Print the original data before sorting
        if debug:
            print("\n[DEBUG] Original data before sorting:")
            for row in data:
                print(row)

    # Sort the data by 'Entry type' and 'Last name'
    sorted_data = sorted(data, key=lambda row: (row['Entry type'], row['Last name']))

    # Debug: Print the sorted data
    if debug:
        print("\n[DEBUG] Sorted data after sorting:")
        for row in sorted_data:
            print(row)

    # Write the sorted data back to the CSV file
    with open(csv_file, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=reader.fieldnames)
        writer.writeheader()
        writer.writerows(sorted_data)

    # Return the number of rows sorted (excluding the header)
    return len(sorted_data)

def main():
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Sort CSV file by 'Entry type' and 'Last name'")
    parser.add_argument("csv_file", help="Path to the CSV file")
    parser.add_argument("-D", "--debug", action="store_true", help="Enable debug mode for printing information")

    # Parse the command-line arguments
    args = parser.parse_args()

    # Call the sort function with the debug flag
    num_sorted = sort_csv(args.csv_file, debug=args.debug)

    # Print a summary of how many lines were sorted
    print(f"\nSummary: {num_sorted} rows were sorted (excluding the header).")

if __name__ == "__main__":
    main()

