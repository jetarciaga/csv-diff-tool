import csv
from pathlib import Path


CSV_FOLDER = Path(__file__).resolve().parents[1] / "csv_compare"

def get_csvs():
    csvs = list(CSV_FOLDER.glob("*.csv"))

    if len(csvs) != 2:
        raise Exception("Expected exactly 2 CSV files in the folder")

    return csvs

def load_csv(filepath: Path):
    with filepath.open(newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        return list(reader), reader.fieldnames

def compare_csv_rows(rows1, rows2, key_fields=None):
    """Compare two lists of CSV rows."""
    if key_fields is None:
        key_fields = rows1[0].keys() if rows1 else []

    dict1 = {tuple(row[k] for k in key_fields): row for row in rows1}
    dict2 = {tuple(row[k] for k in key_fields): row for row in rows2}

    added = [dict2[k] for k in dict2.keys() - dict1.keys()]
    removed = [dict1[k] for k in dict1.keys() - dict2.keys()]
    modified = []

    for k in dict1.keys() & dict2.keys():
        if dict1[k] != dict2[k]:
            modified.append(dict1[k], dict2[k])

    return added, removed, modified

def main():
    csv_files = get_csvs()
    rows1, headers1 = load_csv(csv_files[0])
    rows2, headers2 = load_csv(csv_files[1])

    if headers1 != headers2:
        raise Exception("CSV headers do not match!")

    added, removed, modified = compare_csv_rows(rows1, rows2, key_fields=headers1)

    print(f"\n Added Rows: {len(added)}")
    for row in added:
        print(row)

    print(f"\n Removed Rows: {len(removed)}")
    for row in removed:
        print(row)

    print(f"\n Modified Rows: {len(modified)}")
    for old, new in modified:
        print(f"FROM: {old}")
        print(f"  TO: {new}\n")

if __name__ == "__main__":
    main()

