
"""Reading CSV files into flight records and error messages."""
import csv
import os

from validator import validate_row, to_record


def parse_files(paths: list[str], airports: set[str]) -> tuple[list[dict], list[str]]:
    """Process CSV files in order and reject invalid or duplicate rows."""
    records = []
    errors = []
    seen = set()

    for path in paths:
        filename = os.path.basename(path)

        with open(path, "r", encoding="utf-8-sig", newline="") as file:
            reader = csv.reader(file)

            for fields in reader:
                line_number = reader.line_num

                # Skip empty lines
                if not fields or (len(fields) == 1 and fields[0].strip() == ""):
                    continue

                # Skip comment lines
                if fields[0].lstrip().startswith("#"):
                    continue

                # Skip the CSV header
                if line_number == 1:
                    continue

                error = validate_row(fields, airports)

                if error is None:
                    record = to_record(fields)

                    duplicate_key = (
                        record["flight_id"],
                        record["departure_datetime"]
                    )

                    if duplicate_key in seen:
                        error = "DUPLICATE_FLIGHT"
                    else:
                        seen.add(duplicate_key)
                        records.append(record)

                if error is not None:
                    detail = ",".join(fields)
                    errors.append(
                        f"{filename}:{line_number}: {error} | {detail}"
                    )

    return records, errors
