# AGENTS.md

## Repository purpose

This repository contains small Python booking exercises and acceptance criteria.

- `assignment3/booking.py` implements the booking availability helper.
- `assignment3/test_booking.py` contains a direct/assertion-based smoke test.
- `assignment4/assignment3/` is a duplicate copy of the assignment3 implementation and test.
- `assignment5/README.MD` describes acceptance criteria for a task HTTP API; that API is not implemented in the repository.

## Architecture and entry points

- Booking entry point: `can_book(start, end, now, blocked, existing)` in `assignment3/booking.py`.
- Direct test entry point: `assignment3/test_booking.py`, run as a script.
- There is no application server, package manifest, lockfile, build system, or CI workflow in the repository.
- Treat booking implementations in both assignment directories separately unless a later task explicitly consolidates them.

## Setup

Use Python 3. A virtual environment is optional for this repository because it has no declared third-party dependencies.

```sh
cd /path/to/soft/software
python3 --version
```

Do not add or upgrade dependencies without a user-approved change and explicit review.

Assignment5 uses the Python standard library WSGI interface. The application entry
point is `assignment5/app.py:application`.

## Safe read-only and validation commands

Run from the repository root:

```sh
python3 -m pytest -q assignment3
python3 -m pytest -q assignment4/assignment3
python3 assignment3/test_booking.py
python3 assignment4/assignment3/test_booking.py
python3 -m compileall -q assignment3 assignment4
ruff check .
ruff format --check .
mypy assignment3/booking.py assignment3/test_booking.py
mypy assignment4/assignment3/booking.py assignment4/assignment3/test_booking.py
git --no-pager status --porcelain=v1
```

Do not report a command as passed unless it was actually run and the result is known.

## Coding conventions

- Preserve existing Python 3 syntax and public function signatures unless the task explicitly changes them.
- Keep changes focused on the requested assignment directory.
- Use clear, descriptive names and explicit return values.
- Add focused tests for changed behavior, including boundary and invalid-input cases.
- Format Python with Ruff and keep imports/lint clean.
- Avoid duplicate implementations; if consolidation is requested, document migration and compatibility behavior first.

## Test expectations

- Add or update tests for every behavioral change.
- Test boundary cases, especially minute `0` and `1440`, exact duration `120`, touching intervals, overlaps, blocked bookings, and `start == now`.
- Test invalid payload/range behavior once an HTTP/API implementation exists.
- Run the smallest relevant pytest command first, then the repository-wide applicable checks.
- `python3 -m pytest -q` currently has a known duplicate test-module name collision and is not a reliable repository-wide command until test modules are renamed or packages are configured.
- Clean generated `__pycache__` directories after validation when they are not ignored.

## Forbidden actions

- Never expose, add, commit, or print secrets, credentials, tokens, private keys, or `.env` contents.
- Never modify application source or tests in a read-only analysis/review task.
- Never deploy, publish, or otherwise change production systems.
- Never run destructive commands such as `git reset --hard`, `git clean`, force-pushing, or deleting unrelated files or directories.
- Never add dependencies, change package manifests, or update lockfiles without explicit approval and a dependency review.
- Never weaken or bypass validation, authentication, authorization, or test assertions.
- Never claim an HTTP API exists or acceptance criteria pass while it is absent.
