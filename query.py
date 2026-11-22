
"""Running queries against the flight database."""
from datetime import datetime
import math


FILTER_KEYS = {
    "flight_id", "origin", "destination",
    "departure_datetime", "arrival_datetime",
    "price", "min_price"
}

SORT_KEYS = {
    "flight_id", "origin", "destination",
    "departure_datetime", "arrival_datetime", "price"
}

ALLOWED_KEYS = FILTER_KEYS | {"sort_by", "order", "limit"}


def _valid_datetime(value):
    if not isinstance(value, str):
        return False

    try:
        parsed = datetime.strptime(value, "%Y-%m-%d %H:%M")
        return parsed.strftime("%Y-%m-%d %H:%M") == value
    except ValueError:
        return False


def _valid_query(query):
    if not isinstance(query, dict):
        return False

    if any(key not in ALLOWED_KEYS for key in query):
        return False

    for key in ("flight_id", "origin", "destination"):
        if key in query and not isinstance(query[key], str):
            return False

    for key in ("departure_datetime", "arrival_datetime"):
        if key in query and not _valid_datetime(query[key]):
            return False

    for key in ("price", "min_price"):
        if key in query:
            value = query[key]

            if isinstance(value, bool) or not isinstance(value, (int, float)):
                return False

            try:
                if not math.isfinite(value):
                    return False
            except OverflowError:
                return False

    if "sort_by" in query:
        if not isinstance(query["sort_by"], str):
            return False

        if query["sort_by"] not in SORT_KEYS:
            return False

    if "order" in query:
        if "sort_by" not in query or query["order"] not in ("asc", "desc"):
            return False

    if "limit" in query:
        limit = query["limit"]

        if isinstance(limit, bool) or not isinstance(limit, int) or limit < 0:
            return False

    return True


def run_query(db: list[dict], query: dict) -> dict:
    """Return the result of one query."""
    if not _valid_query(query):
        return {
            "query": query,
            "error": "INVALID_QUERY",
            "matches": []
        }

    matches = []

    for flight in db:
        conditions = []

        if "flight_id" in query:
            conditions.append(flight["flight_id"] == query["flight_id"])

        if "origin" in query:
            conditions.append(flight["origin"] == query["origin"])

        if "destination" in query:
            conditions.append(flight["destination"] == query["destination"])

        if "departure_datetime" in query:
            conditions.append(
                flight["departure_datetime"] >= query["departure_datetime"]
            )

        if "arrival_datetime" in query:
            conditions.append(
                flight["arrival_datetime"] <= query["arrival_datetime"]
            )

        if "price" in query:
            conditions.append(flight["price"] <= query["price"])

        if "min_price" in query:
            conditions.append(flight["price"] >= query["min_price"])

        if not conditions or all(conditions):
            matches.append(flight)

    if "sort_by" in query:
        matches.sort(
            key=lambda flight: flight[query["sort_by"]],
            reverse=query.get("order", "asc") == "desc"
        )

    if "limit" in query:
        matches = matches[:query["limit"]]

    return {
        "query": query,
        "matches": matches
    }


def run_queries(db: list[dict], queries: dict | list) -> list[dict]:
    """Process one query or a list of queries."""
    if isinstance(queries, list):
        return [run_query(db, query) for query in queries]

    return [run_query(db, queries)]
