
"""Row validation: airport list loading, single-row checks, record building."""
import math
import re
from datetime import datetime


def load_airports(path: str) -> set[str]:
    """Read an airport list file and return the set of codes."""
    airports = set()

    with open(path, "r", encoding="utf-8") as file:
        for line in file:
            code = line.strip()

            if code == "" or code.startswith("#"):
                continue

            airports.add(code)

    return airports


def validate_row(fields: list[str], airports: set[str]) -> str | None:
    """Return the first validation error code, or None for a valid row."""
    if len(fields) != 6:
        return "WRONG_FIELD_COUNT"

    values = [field.strip() for field in fields]

    if any(value == "" for value in values):
        return "MISSING_FIELD"

    flight_id, origin, destination, departure, arrival, price_text = values

    if re.fullmatch(r"[A-Za-z0-9]{2,8}", flight_id, flags=re.ASCII) is None:
        return "INVALID_FLIGHT_ID"

    if re.fullmatch(r"[A-Z]{3}", origin, flags=re.ASCII) is None or origin not in airports:
        return "INVALID_ORIGIN"

    if re.fullmatch(r"[A-Z]{3}", destination, flags=re.ASCII) is None or destination not in airports:
        return "INVALID_DESTINATION"

    if origin == destination:
        return "SAME_ORIGIN_DESTINATION"

    try:
        departure_time = datetime.strptime(departure, "%Y-%m-%d %H:%M")
        if departure_time.strftime("%Y-%m-%d %H:%M") != departure:
            return "INVALID_DEPARTURE"
    except ValueError:
        return "INVALID_DEPARTURE"

    try:
        arrival_time = datetime.strptime(arrival, "%Y-%m-%d %H:%M")
        if arrival_time.strftime("%Y-%m-%d %H:%M") != arrival:
            return "INVALID_ARRIVAL"
    except ValueError:
        return "INVALID_ARRIVAL"

    if arrival_time <= departure_time:
        return "ARRIVAL_NOT_AFTER_DEPARTURE"

    try:
        price = float(price_text)
    except ValueError:
        return "INVALID_PRICE"

    if not math.isfinite(price):
        return "INVALID_PRICE"

    if price <= 0:
        return "NON_POSITIVE_PRICE"

    return None


def to_record(fields: list[str]) -> dict:
    """Turn a valid CSV row into a flight record dictionary."""
    values = [field.strip() for field in fields]

    return {
        "flight_id": values[0],
        "origin": values[1],
        "destination": values[2],
        "departure_datetime": values[3],
        "arrival_datetime": values[4],
        "price": float(values[5]),
    }
