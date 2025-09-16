#!/usr/bin/env python3
"""
filter_results.py

Clean CX race CSVs:
  - Remove rows where the FIRST COLUMN is empty
  - Keep rows with Race No < threshold (default: 900) → removes non-league riders
  - Optionally filter by category (e.g. Masters 50/60)
  - Optionally drop DNFs/DSQ (non-numeric Pos)
  - Sort by Pos and renumber Pos starting at 1
  - Preserve original column order; ignore unexpected keys on write

Examples:
  python filter_results.py Vet50-results.csv
  python filter_results.py Vet50-results.csv --inplace
  python filter_results.py Vet50-results.csv -o Vet50-clean.csv --category-field Category --include-categories "Masters 50,Masters 60"
  python filter_results.py Vet50-results.csv --drop-dnfs --max-race-no 900 --work "Masters 50"
"""

import csv
import argparse
from pathlib import Path

def to_int(val, default=None):
    try:
        return int(str(val).strip())
    except Exception:
        return default

def normalize_header(fieldnames):
    """Strip whitespace from header names while preserving order."""
    return [(h.strip() if h is not None else h) for h in (fieldnames or [])]

def read_rows(input_csv):
    """Read CSV with BOM-safe encoding; strip whitespace from keys."""
    with open(input_csv, "r", newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        raw_headers = reader.fieldnames or []
        headers = normalize_header(raw_headers)

        rows = []
        for r in reader:
            # Clean keys (strip) and keep values as-is
            cleaned = {}
            for k, v in r.items():
                nk = k.strip() if isinstance(k, str) else k
                cleaned[nk] = v
            rows.append(cleaned)

    return headers, rows

def first_column_nonempty(row, headers):
    """Return True if the first physical column value is non-empty."""
    if not headers:
        return False
    first_key = headers[0]
    return bool(str(row.get(first_key, "")).strip())

def filter_rows(rows,
                headers,
                max_race_no=900,
                category_field=None,
                include_categories=None,
                drop_dnfs=False):
    """Apply filtering rules and return filtered list."""
    # Ensure required columns exist
    required = {"Race No", "Pos"}
    missing = [c for c in required if c not in headers]
    if missing:
        raise SystemExit(f"Missing required column(s): {', '.join(missing)}")

    include_set = None
    if include_categories:
        include_set = {c.strip() for c in include_categories.split(",") if c.strip()}
        if category_field and category_field not in headers:
            raise SystemExit(f"Category field '{category_field}' not found in header.")

    out = []
    for r in rows:
        # 1) first column must be non-empty
        if not first_column_nonempty(r, headers):
            continue

        # 2) Race No < max_race_no (skip non-numeric)
        race_no = to_int(r.get("Race No"))
        if race_no is None or race_no >= max_race_no:
            continue

        # 3) Optional category include filter
        if include_set and category_field:
            cat_val = (r.get(category_field) or "").strip()
            if cat_val not in include_set:
                continue

        # 4) Optionally drop DNFs/DSQ (keep only numeric Pos)
        pos_val = to_int(r.get("Pos"))
        if drop_dnfs and pos_val is None:
            continue

        out.append(r)

    return out

def sort_and_renumber(filtered):
    """Sort by numeric Pos (non-numeric to end), then renumber Pos from 1."""
    def pos_key(row):
        p = to_int(row.get("Pos"))
        # numeric first, then by value; non-numeric to end
        return (0, p) if p is not None else (1, 10**9)

    filtered.sort(key=pos_key)

    for i, r in enumerate(filtered, start=1):
        r["Pos"] = str(i)

def write_rows(output_csv, headers, rows):
    """Write using original header order; ignore extra keys to avoid ValueError."""
    with open(output_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers, extrasaction="ignore")
        writer.writeheader()
        for r in rows:
            writer.writerow({k: r.get(k, "") for k in headers})

def main():
    ap = argparse.ArgumentParser(
        description="Filter DNFs & non-league riders from CX results and re-rank."
    )
    ap.add_argument("csv_file", help="Path to the CSV file")
    ap.add_argument("-o", "--output", help="Output CSV path (default: input.clean.csv)")
    ap.add_argument("--inplace", action="store_true", help="Overwrite the input file")

    # Filtering options
    ap.add_argument("--max-race-no", type=int, default=900,
                    help="Keep rows with Race No < this value (default: 900)")
    ap.add_argument("--category-field", help="Column name that holds category (e.g., 'Category')")
    ap.add_argument("--include-categories",
                    help="Comma-separated list of categories to keep (e.g., 'Masters 50,Masters 60')")
    ap.add_argument("--drop-dnfs", action="store_true",
                    help="Drop rows where Pos is non-numeric (DNF/DSQ etc.)")

    args = ap.parse_args()

    input_path = Path(args.csv_file)
    if not input_path.exists():
        raise SystemExit(f"File not found: {input_path}")

    output_path = input_path if args.inplace else Path(args.output) if args.output else input_path.with_suffix(".clean.csv")

    # Read & sanitize
    headers, rows = read_rows(input_path)

    # Filter
    filtered = filter_rows(
        rows,
        headers,
        max_race_no=args.max_race_no,
        category_field=args.category_field,
        include_categories=args.include_categories,
        drop_dnfs=args.drop_dnfs
    )

    # Sort & renumber
    sort_and_renumber(filtered)

    # Write
    write_rows(output_path, headers, filtered)

    print(
        f"Updated {input_path.name} → {output_path.name} | "
        f"kept {len(filtered)} rows | "
        f"Race No < {args.max_race_no}"
        + (f" | categories: {args.include_categories}" if args.include_categories else "")
        + (" | DNFs dropped" if args.drop_dnfs else "")
    )

if __name__ == "__main__":
    main()

