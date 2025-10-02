#!/usr/bin/env python3
import csv
import re
import sys
import os
from collections import defaultdict

def fix_cat(c):
    if not c:
        return c
    s = re.sub(r"\s+", " ", c.strip())   # collapse spaces
    u = s.upper()
    if re.fullmatch(r"(V\s*70|M\s*70\+?|M70\+?)", u):
        return "M 60-69"
    return s

def main(path):
    if not os.path.isfile(path):
        sys.exit(f"File not found: {path}")

    # Read CSV into memory
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        fieldnames = reader.fieldnames

    # Normalise categories
    for row in rows:
        row["Category"] = fix_cat(row["Category"])

    # Group rows by category
    grouped = defaultdict(list)
    for row in rows:
        try:
            pos = int(row["Pos"])
        except ValueError:
            pos = float("inf")
        grouped[row["Category"]].append((pos, row))

    # Recompute Cat Pos within each category by overall Pos
    for cat, entries in grouped.items():
        for i, (pos, row) in enumerate(sorted(entries, key=lambda x: x[0]), start=1):
            row["Cat Pos"] = str(i)

    # Write back to same file
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"✔ File updated: {path}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(f"Usage: {sys.argv[0]} <csvfile>")
    main(sys.argv[1])

