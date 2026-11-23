# AI Usage Disclosure

## Tools used

- ChatGPT GPT-6 (OpenAI)

## Conversation links

- Link 1: https://chatgpt.com/share/6b03d57d-60d4-83ed-84d5-bace52d8a9da
- Link 2: N/A

## What I used them for

- Understanding Python code and assignment requirements.
- Explaining and debugging input validation.
- Reviewing CSV parsing, header handling and duplicate detection.
- Debugging query filtering and ensuring all selected conditions are applied using `all()`.
- Improving error handling for invalid JSON databases and invalid query parameters.
- Identifying edge cases and preparing additional tests.
- Understanding the purpose of the changes rather than just copying code.

## Which parts of the code were AI-generated or substantially AI-assisted

| File | Function or part | How (generated / modified / explained) |
|---|---|---|
| validator.py | Airport code validation in validate_row() | Modified with AI assistance to check the required three-uppercase-letter format and airport list membership. |
| csv_loader.py | CSV header handling in parse_files() | Modified with AI assistance to skip the first line unconditionally. |
| flight_parser.py | JSON database validation in main() | Modified with AI assistance to ensure the database is a list containing dictionaries. |
| query.py | sort_by validation in _valid_query() | Modified with AI assistance to reject invalid data types safely. |
| query.py | Numeric validation in _valid_query() | Modified with AI assistance to handle OverflowError for extremely large integers. |
| query.py | Query filtering and validation | Explained and reviewed with AI assistance. |

## Key prompts

1. Review my Python flight schedule parser against the assignment requirements. Identify problems, explain why they are problems, and show exactly what code needs to be replaced.
2. Help me test the corrected implementation with edge cases, explain the expected results, and identify any remaining issues.

## What I changed or verified myself

- I reviewed the explanations and made the suggested changes to my Python files.
- I worked through the validation and query logic to understand how it works.
- I ran the provided public test suite and obtained 29 passing tests out of 29.
- I ran additional tests for invalid airport codes, invalid JSON database structures, invalid sort_by values, extremely large integers and empty JSON arrays.
- I checked the actual terminal outputs against the expected results.
- I reviewed the code changes and verified that the existing public tests continued to pass after the modifications.