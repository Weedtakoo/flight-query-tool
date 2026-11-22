
"""Flight Schedule Parser and Query Tool - command-line entry point."""
import argparse
import csv
import json
import logging
import os
import sys
from datetime import datetime

from csv_loader import parse_files
from query import run_queries
from validator import load_airports


STUDENT_ID = "251adb128"
FIRST_NAME = "Ziya"
LAST_NAME = "Pirizada"


def _error(message):
    print(f"Error: {message}", file=sys.stderr)


def main(argv: list[str] | None = None) -> int:
    """Run the program and return its exit code."""
    parser = argparse.ArgumentParser(
        description="Flight schedule parser and query tool"
    )

    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("-i", metavar="CSV_FILE")
    source.add_argument("-d", metavar="CSV_FOLDER")
    source.add_argument("-j", metavar="JSON_DATABASE")

    parser.add_argument("-a", metavar="AIRPORTS_FILE")
    parser.add_argument("-o", metavar="OUTPUT_JSON")
    parser.add_argument("-q", metavar="QUERY_JSON")
    parser.add_argument("-r", metavar="RESPONSE_FOLDER")

    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        return int(exc.code)

    if args.i or args.d:
        if not args.a:
            _error("-a is required with -i or -d")
            return 2
    elif args.a:
        _error("-a can only be used with -i or -d")
        return 2

    if args.j and args.o:
        _error("-o cannot be used with -j")
        return 2

    logger = logging.getLogger("flight_parser")
    handler = None

    try:
        if args.i or args.d:
            if args.i:
                if not os.path.isfile(args.i):
                    raise OSError(f"CSV file does not exist: {args.i}")

                paths = [args.i]

            else:
                if not os.path.isdir(args.d):
                    raise OSError(f"CSV folder does not exist: {args.d}")

                paths = [
                    os.path.join(args.d, name)
                    for name in sorted(os.listdir(args.d))
                    if name.lower().endswith(".csv")
                    and os.path.isfile(os.path.join(args.d, name))
                ]

                if not paths:
                    raise OSError("CSV folder contains no .csv files")

            airports = load_airports(args.a)
            records, errors = parse_files(paths, airports)

            output_path = args.o if args.o else "db.json"

            with open(output_path, "w", encoding="utf-8") as file:
                json.dump(records, file, indent=4)

            log_path = os.path.join(
                os.path.dirname(os.path.abspath(output_path)),
                "errors.log"
            )

            logger.setLevel(logging.WARNING)
            logger.propagate = False

            handler = logging.FileHandler(
                log_path,
                mode="w",
                encoding="utf-8"
            )

            handler.setFormatter(
                logging.Formatter(
                    "%(asctime)s %(levelname)s %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S"
                )
            )

            logger.addHandler(handler)

            for error in errors:
                logger.warning(error)

            handler.flush()

        else:
            if not os.path.isfile(args.j):
                raise OSError(
                    f"JSON database does not exist: {args.j}"
                )

            with open(args.j, "r", encoding="utf-8") as file:
                records = json.load(file)

            if not isinstance(records, list) or any(
                not isinstance(record, dict) for record in records
            ):
                raise ValueError(
                    "JSON database must contain an array of objects"
                )

        if args.q:
            with open(args.q, "r", encoding="utf-8") as file:
                queries = json.load(file)

            if not isinstance(queries, (dict, list)):
                raise ValueError(
                    "query file must contain an object or an array"
                )

            response = run_queries(records, queries)

            response_folder = args.r if args.r else "."

            if not os.path.isdir(response_folder):
                raise OSError(
                    f"response folder does not exist: {response_folder}"
                )

            timestamp = datetime.now().strftime("%Y%m%d_%H%M")

            filename = (
                f"response_{STUDENT_ID}_{FIRST_NAME}_"
                f"{LAST_NAME}_{timestamp}.json"
            )

            response_path = os.path.join(
                response_folder,
                filename
            )

            with open(response_path, "w", encoding="utf-8") as file:
                json.dump(response, file, indent=4)

        return 0

    except (OSError, ValueError, json.JSONDecodeError, csv.Error) as exc:
        _error(str(exc))
        return 1

    finally:
        if handler is not None:
            logger.removeHandler(handler)
            handler.close()


if __name__ == "__main__":
    sys.exit(main())
