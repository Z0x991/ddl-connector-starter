# DDL Connector Basic Python Validator

An AI-assisted Python port of the original standalone JavaScript prototype. Uses synthetic records; not yet integrated with the team application.

## Run

Python 3.8 or newer is required. No external packages are needed.

    python demo.py
    python -m unittest -v

On systems where Python is named python3, use python3 instead. Run the commands inside this folder.

## Files

- validator.py: validate_deadlines(records), the validation function.
- test_validator.py: the original 14 checks ported to unittest.
- sample.json: original five synthetic records.
- demo.py: reads the sample and prints results.
- demo-output.json: recorded demo output.
- test-results.txt: actual Python test output, 14 passed.

## Input and output

Input: a list of dictionaries with title and due; calendarId and uid are optional. due is a full ISO timestamp string with seconds and a UTC offset, such as 2026-10-30T23:59:00-05:00. Missing or invalid values require review. This port does not accept Python datetime or date objects.

Output: copies of records with trimmed title, normalizedDue in UTC, issues, and status (valid or needs_review). Original records remain unchanged. Same calendarId and uid flag duplicate or conflicting records in the current batch. Records are never deleted. A valid status is not confirmation that a real assignment deadline is correct.

## Scope

No ICS parsing, platform access, UI, persistence, export, recurrence handling, or teammate-specific integration. Timezone-free and date-only strings require review. Missing identifiers mean duplicate detection is skipped. Duplicate comparisons use title and original due value; other optional fields are not compared. Re-import across separate runs is not tracked.

## Moving from JavaScript

Replace validator.mjs with validator.py, validator.test.mjs with test_validator.py, and demo.mjs with demo.py. Replace README.md, demo-output.json, and test-results.txt with these versions. sample.json is unchanged. The Python function is called validate_deadlines. The existing output keys are preserved. Retire the three old .mjs files once you switch the repository to this version.
