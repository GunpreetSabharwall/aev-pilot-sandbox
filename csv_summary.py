"""Print the row count and column averages for a CSV file.

Usage: python csv_summary.py FILE

The first line of the file must be the column names. A column gets an
average only if every non-empty value in it is a number; other columns
are listed as "not numeric". Empty cells are ignored.
"""

import csv
import sys


def _to_number(value):
    try:
        return float(value)
    except ValueError:
        return None


def summarize(lines):
    """Return (row_count, averages, skipped) for CSV text given as lines.

    averages maps each numeric column to its average (None if the column
    has no values); skipped lists the columns that are not numeric.
    """
    reader = csv.DictReader(lines)
    columns = reader.fieldnames or []
    totals = {name: 0.0 for name in columns}
    counts = {name: 0 for name in columns}
    numeric = {name: True for name in columns}
    row_count = 0

    for row in reader:
        row_count += 1
        for name in columns:
            value = (row.get(name) or "").strip()
            if not value or not numeric[name]:
                continue
            number = _to_number(value)
            if number is None:
                numeric[name] = False
            else:
                totals[name] += number
                counts[name] += 1

    averages = {
        name: (totals[name] / counts[name] if counts[name] else None)
        for name in columns
        if numeric[name]
    }
    skipped = [name for name in columns if not numeric[name]]
    return row_count, averages, skipped


def format_summary(row_count, averages, skipped):
    lines = [f"Rows: {row_count}"]
    if averages:
        lines.append("Column averages:")
        for name, average in averages.items():
            shown = "n/a (no values)" if average is None else f"{average:g}"
            lines.append(f"  {name}: {shown}")
    if skipped:
        lines.append("Not numeric: " + ", ".join(skipped))
    return "\n".join(lines)


def main(argv=None):
    args = sys.argv[1:] if argv is None else argv
    if len(args) != 1:
        print("Usage: python csv_summary.py FILE", file=sys.stderr)
        return 2
    path = args[0]
    try:
        with open(path, encoding="utf-8-sig", newline="") as handle:
            result = summarize(handle)
    except OSError as exc:
        print(f"Cannot read {path}: {exc.strerror}", file=sys.stderr)
        return 1
    except csv.Error as exc:
        print(f"Cannot parse {path} as CSV: {exc}", file=sys.stderr)
        return 1
    print(format_summary(*result))
    return 0


if __name__ == "__main__":
    sys.exit(main())
