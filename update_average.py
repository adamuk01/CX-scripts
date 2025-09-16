#!/usr/bin/env python3
"""
update_averages.py

Updates per-rider averages in a denormalised 'riders' table:
- average_position: mean of r1..r12 overall positions (ignoring None/0/placeholder)
- average_points:   mean of r1..r12 points (ignoring None/0/placeholder)

Usage:
  python update_averages.py /path/to/race.db
  python update_averages.py /path/to/race.db --placeholder 999
  python update_averages.py /path/to/race.db --dry-run
"""

import argparse
import sqlite3
from typing import Iterable, Tuple, Optional, Any

POSITION_COLS = [
    "r1_overall_position","r2_overall_position","r3_overall_position",
    "r4_overall_position","r5_overall_position","r6_overall_position",
    "r7_overall_position","r8_overall_position","r9_overall_position",
    "r10_overall_position","r11_overall_position","r12_overall_position",
]
POINTS_COLS = [
    "r1_points","r2_points","r3_points","r4_points","r5_points","r6_points",
    "r7_points","r8_points","r9_points","r10_points","r11_points","r12_points",
]

def to_float(x: Any) -> Optional[float]:
    if x is None:
        return None
    if isinstance(x, (int, float)):
        return float(x)
    s = str(x).strip()
    if s == "":
        return None
    try:
        return float(s)
    except ValueError:
        return None

def mean_filtered(values: Iterable[Any], placeholder: Optional[float] = 999.0, round_mode: str = "nearest"):
    """
    Compute mean ignoring None, 0, and placeholder.
    Returns (mean_float_or_None, count_used)
    """
    cleaned = []
    for v in values:
        f = to_float(v)
        if f is None:
            continue
        if f == 0:
            continue
        if placeholder is not None and f == float(placeholder):
            continue
        cleaned.append(f)

    if not cleaned:
        return None, 0

    m = sum(cleaned) / len(cleaned)

    if round_mode == "nearest":
        return round(m), len(cleaned)  # integer style (for positions)
    elif round_mode == "ceil":
        import math
        return math.ceil(m), len(cleaned)
    elif round_mode == "floor":
        import math
        return math.floor(m), len(cleaned)
    elif round_mode == "1dp":
        return round(m, 1), len(cleaned)
    else:
        return m, len(cleaned)

def ensure_columns(conn: sqlite3.Connection):
    """Create average columns if they don't exist."""
    cur = conn.cursor()
    # Check pragma table_info to see if columns exist
    cur.execute("PRAGMA table_info(riders)")
    cols = {row[1] for row in cur.fetchall()}
    stmts = []
    if "average_position" not in cols:
        stmts.append("ALTER TABLE riders ADD COLUMN average_position INTEGER")
    if "average_points" not in cols:
        stmts.append("ALTER TABLE riders ADD COLUMN average_points REAL")
    for s in stmts:
        cur.execute(s)
    if stmts:
        conn.commit()

def update_averages(db_path: str, placeholder: float = 999.0, dry_run: bool = False) -> Tuple[int, int]:
    conn = sqlite3.connect(db_path)
    try:
        ensure_columns(conn)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

        # Pull only the columns we need
        select_cols = ["id"] + POSITION_COLS + POINTS_COLS
        cur.execute(f"SELECT {', '.join(select_cols)} FROM riders")
        rows = cur.fetchall()

        upd_pos = 0
        upd_pts = 0

        # Begin a transaction
        cur.execute("BEGIN")
        for row in rows:
            rider_id = row["id"]

            # Positions: integer average (nearest)
            pos_vals = [row[c] for c in POSITION_COLS if c in row.keys()]
            avg_pos, used_pos = mean_filtered(pos_vals, placeholder=placeholder, round_mode="nearest")

            # Points: 1 decimal place
            pts_vals = [row[c] for c in POINTS_COLS if c in row.keys()]
            avg_pts_raw, used_pts = mean_filtered(pts_vals, placeholder=placeholder, round_mode="1dp")

            # Only update if we computed something (avoid writing 0s)
            if avg_pos is not None:
                upd_pos += 1
                if not dry_run:
                    cur.execute(
                        "UPDATE riders SET average_position = ? WHERE id = ?",
                        (int(avg_pos), rider_id),
                    )
            if avg_pts_raw is not None:
                upd_pts += 1
                if not dry_run:
                    cur.execute(
                        "UPDATE riders SET average_points = ? WHERE id = ?",
                        (float(avg_pts_raw), rider_id),
                    )

        if dry_run:
            conn.rollback()
        else:
            conn.commit()

        return upd_pos, upd_pts
    finally:
        conn.close()

def main():
    ap = argparse.ArgumentParser(description="Update rider averages in SQLite DB.")
    ap.add_argument("input_file", help="Path to the SQLite DB file")
    ap.add_argument("--placeholder", type=float, default=999.0,
                    help="Value to treat as placeholder (ignored in averages). Default: 999")
    ap.add_argument("--dry-run", action="store_true",
                    help="Compute but do not write changes")
    args = ap.parse_args()

    print(f"Updating database {args.input_file} with new average values "
          f"(placeholder={args.placeholder}{', DRY-RUN' if args.dry_run else ''})")

    pos_count, pts_count = update_averages(args.input_file, placeholder=args.placeholder, dry_run=args.dry_run)
    print(f"Updated average_position for {pos_count} riders; average_points for {pts_count} riders.")

if __name__ == "__main__":
    main()

