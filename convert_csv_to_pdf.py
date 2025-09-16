#!/usr/bin/python3

# Convert a CSV file to PDF and put a header above it

import csv
import sys
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import styles

def create_pdf(input_file, output_file, custom_text):
    # Open the CSV file for reading
    with open(input_file, 'r') as csv_file:
        # Create a CSV reader object
        reader = csv.reader(csv_file)

        # Extract headers
        headers = next(reader)

        # Extract data rows
        data = [row for row in reader]

        # Create a PDF document
        pdf = SimpleDocTemplate(output_file, pagesize=A4)
        elements = []

        # Add custom text above the table
        if custom_text:
            styles = getSampleStyleSheet()
            custom_text = Paragraph(custom_text, styles['Title'])
            elements.append(custom_text)
            elements.append(Spacer(1, 12))  # Add blank line

        # Create a table from the CSV data
        table_data = [headers] + data
        table = Table(table_data, repeatRows=1)  # Repeat the header row on each page

        # Customize table style
        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.white),  # Set header background to white
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),  # Set header text color to black
            ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold', 8),  # Set header font to bold with size 8
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),  # Left-align all text
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Add padding for header row
            ('GRID', (0, 0), (-1, -1), 1, colors.black)  # Add grid to the entire table
        ])

        # Apply the table style
        table.setStyle(style)


        # Add table to the PDF document
        elements.append(table)
        pdf.build(elements)

# Check if the correct number of command-line arguments are provided
if len(sys.argv) < 3:
    print("Usage: python convert_csv_to_pdf.py input_file output_file [custom_text]")
    sys.exit(1)

# Extract input and output file paths from command-line arguments
input_file = sys.argv[1]
output_file = sys.argv[2]

# Extract custom text from command-line arguments if provided
custom_text = None
if len(sys.argv) > 3:
    custom_text = sys.argv[3]

# Call the function to create the PDF
create_pdf(input_file, output_file, custom_text)

