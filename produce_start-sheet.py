#!/usr/bin/python3
import csv
import argparse

def validate_and_allocate_membership(csv_file, debug=False):
    """
    Reads a CSV file, allocates a race number to non-league riders who have no 'Membership number',
    starting from 900, and returns the updated data.

    Args:
    - csv_file: Path to the input CSV file.
    - debug: Boolean flag to print debug information.
    
    Returns:
    - updated_data: List of updated rows (including the header).
    - count_allocated: The number of rows that had a membership number allocated.
    """
    updated_data = []  # Store the updated data, starting with the header
    membership_number = 900  # Starting number for non-league riders (non-members)
    count_allocated = 0  # Count how many membership numbers were allocated

    with open(csv_file, 'r', newline='') as file:
        reader = csv.reader(file)
        header = next(reader)  # Read and store the header row
        updated_data.append(header)  # Add the header to the updated data

        # Get the index of the 'Membership number' field in the CSV
        membership_number_index = header.index("Membership number")

        # Process each row
        for line_num, row in enumerate(reader, start=2):  # Start at line 2 (after header)
            if not row[membership_number_index]:  # Check if 'Membership number' is empty
                row[membership_number_index] = str(membership_number)  # Allocate a new membership number
                membership_number += 1  # Increment membership number for the next rider
                count_allocated += 1  # Increment counter for allocated numbers

                # Debug: Print allocation info
                if debug:
                    print(f"[DEBUG] Line {line_num}: Allocated Membership number {row[membership_number_index]}")

            updated_data.append(row)  # Add the updated row to the data

    return updated_data, count_allocated

def write_to_csv(data, output_file):
    """
    Writes the processed data to a new CSV file.
    
    Args:
    - data: List of rows (including header) to write to the CSV file.
    - output_file: Path to the output CSV file.
    """
    with open(output_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)

def main():
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Validate CSV file, allocate membership numbers, and output to a new CSV file")
    parser.add_argument("csv_file", help="Path to the input CSV file")
    parser.add_argument("output_file", help="Path to the output CSV file")
    parser.add_argument("-D", "--debug", action="store_true", help="Enable debug mode for printing detailed processing information")

    # Parse the command-line arguments
    args = parser.parse_args()

    # Call the function to process the CSV file and allocate membership numbers
    updated_data, count_allocated = validate_and_allocate_membership(args.csv_file, debug=args.debug)

    # Write the updated data to the output CSV file
    write_to_csv(updated_data, args.output_file)

    # Print a summary of the operation
    print("\nProcessing complete.")
    print(f"Summary: {count_allocated} membership numbers were allocated to non-league riders.")
    print(f"Updated data has been saved to: {args.output_file}")

if __name__ == "__main__":
    main()

