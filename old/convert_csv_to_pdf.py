#!/usr/bin/python3

import csv
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, Spacer, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import sys

def csv_to_pdf(csv_file, pdf_file, header_text):
    data = []

    # Read data from CSV file
    with open(csv_file, 'r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            data.append(row)

    # Create PDF document
    doc = SimpleDocTemplate(pdf_file, pagesize=letter)
    story = []

    # Add header
    styles = getSampleStyleSheet()
    header_style = styles["Heading1"]
    header_text = Paragraph(header_text, header_style)
    story.append(header_text)
    story.append(Spacer(1, 12))  # Add some space between header and table

    # Add table
    table = Table(data)
    story.append(table)

    # Build PDF document
    doc.build(story)

if __name__ == "__main__":
    # Check if the correct number of command-line arguments are provided
    if len(sys.argv) != 4:
        print("Usage: python script.py input.csv output.pdf 'Header Text'")
        sys.exit(1)

    # Get input CSV file, output PDF file, and header text from command-line arguments
    input_csv = sys.argv[1]
    output_pdf = sys.argv[2]
    header_text = sys.argv[3]

    # Convert CSV to PDF with header
    csv_to_pdf(input_csv, output_pdf, header_text)

