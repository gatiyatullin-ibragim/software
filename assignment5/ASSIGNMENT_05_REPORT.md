# Assignment 05 Governance and Implementation Report

## 1. Repository & Acceptance Criteria

### Repository

- Repository link: https://github.com/gatiyatullin-ibragim/software.git
- Baseline commit: `fc3c6a53d5a3ee294481e3fa9fa8f48fcf098b05` (initially observed as short hash `fc3c6a5`)
- Final commit: no final commit was created during this session. The implementation is an uncommitted working-tree state at HEAD `fc3c6a53d5a3ee294481e3fa9fa8f48fcf098b05`.
- Actual worktree final state:

```text
 D assignment4/assignment3/test_booking.py
 A assignment5/app.py
 A assignment5/test_app.py
?? AGENTS.md
?? assignment4/assignment3/test_assignment4_booking.py
```

### Acceptance criteria

1. **Create Task (`POST /tasks`):** A valid task payload creates a new task and returns HTTP `201 Created` with the created task representation.
2. **Invalid Payload Handling:** Malformed/invalid JSON or missing required fields at endpoints accepting JSON return `400 Bad Request` without mutating stored state.
3. **List Tasks (`GET /tasks`):** The collection request returns `200 OK` and a JSON array matching the current store state.
4. **Delete Task (`DELETE /tasks/{id}`):** Deleting an existing ID removes it and returns `200 OK` or `204 No Content`; deleting a non-existent ID returns `404 Not Found`.

## 2. Task #01 - Baseline & Context

### Repository map

- `assignment3/booking.py:1` is the booking availability helper.
- `assignment3/test_booking.py:3` is a direct, assertion-based smoke test.
- `assignment4/assignment3/booking.py:1` duplicates the booking helper.
- `assignment4/assignment3/test_booking.py:3` originally duplicated the test module name.
- `assignment5/README.MD:1` contains the HTTP acceptance criteria only.
- No application entry point, package manifest, lockfile, build configuration, or CI workflow existed at baseline.

### Baseline commands and verbatim outputs

#### Direct assignment3 test

Command:

```sh
cd /Users/gatiyatullinibragim/soft/software/assignment3 && python3 test_booking.py
```

Output:

```text
All tests passed successfully!
```

Exit status: `0`

#### Direct assignment4 test

Command:

```sh
cd /Users/gatiyatullinibragim/soft/software/assignment4/assignment3 && python3 test_booking.py
```

Output:

```text
All tests passed successfully!
```

Exit status: `0`

#### Assignment3 pytest

Command:

```sh
cd /Users/gatiyatullinibragim/soft/software/assignment3 && python3 -m pytest -q
```

Output:

```text
.                                                                        [100%]
1 passed in 0.00s
```

#### Assignment4 pytest

Command:

```sh
cd /Users/gatiyatullinibragim/soft/software/assignment4/assignment3 && python3 -m pytest -q
```

Output:

```text
.                                                                        [100%]
1 passed in 0.01s
```

#### Baseline repository-wide pytest

Command:

```sh
cd /Users/gatiyatullinibragim/soft/software && python3 -m pytest -q
```

Verbatim output:

```text
==================================== ERRORS ====================================
___________ ERROR collecting assignment4/assignment3/test_booking.py ___________
import file mismatch:
imported module 'test_booking' has this __file__ attribute:
  /Users/gatiyatullinibragim/soft/software/assignment3/test_booking.py
which is not the same as the test file we want to collect:
  /Users/gatiyatullinibragim/soft/software/assignment4/assignment3/test_booking.py
HINT: remove __pycache__ / .pyc files and/or use a unique basename for your test file modules
=========================== short test summary info ============================
ERROR assignment4/assignment3/test_booking.py
!!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
1 error in 0.00s
```

Exit status: `2`

#### Baseline Ruff lint

Command:

```sh
cd /Users/gatiyatullinibragim/soft/software && ruff check .
```

Verbatim output:

```text
I001 [*] Import block is un-sorted or un-formatted
 --> assignment3/test_booking.py:1:1
  |
1 | from booking import can_book
  | ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2 |
  |
help: Organize imports
  |
2 |
3 +
4 | def test_all_cases():
  |

I001 [*] Import block is un-sorted or un-formatted
 --> assignment4/assignment3/test_booking.py:1:1
  |
1 | from booking import can_book
  | ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2 |
  |
help: Organize imports
  |
2 |
3 +
4 | def test_all_cases():
  |

Found 2 errors.
[*] 2 fixable with `--fix`.
```

Exit status: `1`

#### Baseline formatting check

Command:

```sh
cd /Users/gatiyatullinibragim/soft/software && ruff format --check .
```

Output:

```text
4 files would be reformatted
```

Exit status: `1`

#### Baseline mypy

Command:

```sh
cd /Users/gatiyatullinibragim/soft/software && mypy assignment3 assignment4
```

Verbatim output:

```text
assignment4/assignment3/booking.py: error: Duplicate module named "booking" (also at "assignment3/booking.py")
assignment4/assignment3/booking.py: note: See https://mypy.readthedocs.io/en/stable/running_mypy.html#mapping-file-paths-to-modules for more info
assignment4/assignment3/booking.py: note: Common resolutions include:
assignment4/assignment3/booking.py: note:     a) using `--exclude` to avoid checking one of them,
assignment4/assignment3/booking.py: note:     b) adding `--explicit-package-bases` or adjusting `MYPYPATH`
Found 1 error in 1 file (errors prevented further checking)
```

Exit status: `2`

#### Baseline compile check

Command:

```sh
cd /Users/gatiyatullinibragim/soft/software && python3 -m compileall -q assignment3 assignment4
```

Output: no text.

Exit status: `0`

#### Baseline unittest discovery

Both assignment directories returned:

```text
----------------------------------------------------------------------
Ran 0 tests in 0.000s

NO TESTS RAN
```

Exit status: `5`

### Baseline weaknesses

**Observed facts**

1. Repository-wide pytest failed because both test directories used `test_booking.py`. This is evidenced by the verbatim import-mismatch output.
2. No HTTP API existed while acceptance criteria were present. `assignment5/README.MD:3-6` documents the endpoints, but baseline showed no corresponding application files.
3. The booking test suite checked only six fixed scenarios in `assignment3/test_booking.py:3-23`; it did not cover malformed ranges or types.
4. Ruff reported import/language-formatting issues in two test modules and four files would be reformatted.
5. Mypy could not analyze both assignment directories together because both contained a module named `booking.py`.

**Assumptions**

- Duplicate booking logic may diverge if future fixes are made in only one directory; this is plausible but was not observed in the initial `cmp` check, which showed both implementations and tests equal.
- Lack of a lockfile or package manifest may cause environment drift; this is plausible, not demonstrated as a historical failure.

## 3. Task #02 - Agent Instructions

`AGENTS.md` was created at the root and documents repository purpose, architecture, setup, safe validation commands, coding conventions, test expectations, and forbidden actions. It explicitly prohibits secrets, production deployment, destructive commands, unreviewed dependencies, and bypassing validations.

Instruction-loading disclosure:

- At the start of read-only analysis, no `AGENTS.md` existed.
- It was loaded for implementation after the user supplied it as a tagged file and after the file was created and updated.
- The implementation obeyed the documented scope: no third-party dependency was added, no production deployment occurred, and no destructive command was used.

## 4. Task #03 - Focused Pattern Decision

### Problem

Baseline assignment5 had no implementation. The implementation risk was to place storage and request handling in one block or reproduce endpoint-specific storage logic. The selected pattern separates HTTP orchestration from storage.

### Pattern evaluated

**Strategy pattern**

- `TaskStorage` is the strategy interface.
- `InMemoryTaskStorage` is the concrete strategy.
- `TaskApplication` receives the strategy through construction and delegates create/list/delete operations.

### Before and after

| Area | Before | After |
|---|---|---|
| Task API | Acceptance criteria in README only | WSGI `TaskApplication` in `assignment5/app.py` |
| Storage | Not implemented | `InMemoryTaskStorage` implementing `TaskStorage` |
| Handler/storage coupling | Potentially duplicated in a handler-only design | Storage operations delegated through `TaskApplication.storage` |
| Replacing storage | Not possible | `TaskApplication(alternate_storage)` works through the abstract interface |

Evidence:

- Strategy interface: [assignment5/app.py:6-17](/Users/gatiyatullinibragim/soft/software/assignment5/app.py:6)
- In-memory implementation: [assignment5/app.py:20-40](/Users/gatiyatullinibragim/soft/software/assignment5/app.py:20)
- Injected storage: [assignment5/app.py:43-45](/Users/gatiyatullinibragim/soft/software/assignment5/app.py:43)
- WSGI entry point: [assignment5/app.py:114-115](/Users/gatiyatullinibragim/soft/software/assignment5/app.py:114)

### Acceptance proof

The test at [assignment5/test_app.py:36-54](/Users/gatiyatullinibragim/soft/software/assignment5/test_app.py:36) exercises create, list, delete, and final list behavior.

Invalid JSON and missing-field tests verify `400` plus unchanged store state at [assignment5/test_app.py:57-74](/Users/gatiyatullinibragim/soft/software/assignment5/test_app.py:57).

Missing-ID behavior is verified at [assignment5/test_app.py:77-82](/Users/gatiyatullinibragim/soft/software/assignment5/test_app.py:77).

## 5. Task #04 & #05 - Read-Only Risk Review & Risk Register

Scoring uses likelihood × impact. Likelihood and impact ranges are 1–3, so the score ranges from 1–9.

| ID | Category | Cause / Event / Consequence | Component | Evidence | Classification | Likelihood 1-3 | Impact 1-3 | Initial Score | Mitigation | Owner | Verification Plan | Updated Score | Residual Risk |
|---|---|---|---|---|---|---:|---:|---:|---|---|---|---:|---|
| **R1** | **Security / Correctness** | Invalid JSON or missing fields could mutate state or produce an exception; consequence is incorrect API behavior and state corruption. | Assignment5 POST handler | Baseline criteria: `assignment5/README.MD:4`; no baseline implementation existed. | **Confirmed** | 3 | 3 | 9 | Parse JSON before mutation; validate title; return 400. | Application implementer | Run invalid-JSON and missing-field tests and inspect store state. | 3 | Low: malformed body types and content-length handling still need broader integration tests. |
| **R2** | **Agent operations / Maintainability** | Duplicate test module basenames caused pytest import mismatch. | Assignment3 and Assignment4 tests | Baseline pytest output; both modules named `test_booking.py`. | **Confirmed** | 3 | 2 | 6 | Rename Assignment4 test module to `test_assignment4_booking.py`. | Repository maintainer | Run repository-wide pytest. | 2 | Low: package/module naming can regress if duplicate names are reintroduced. |
| R3 | Maintainability | Booking logic is duplicated across assignment directories and may diverge. | Booking assignments | `assignment3/booking.py:1` and `assignment4/assignment3/booking.py:1` | Plausible | 2 | 2 | 4 | Consolidate only with an explicit compatibility decision. | Repository maintainer | Diff or compare modules; add shared package tests. | 4 | Medium: no consolidation or migration plan exists. |
| R4 | Correctness | Booking inputs are not type-validated; malformed values may raise or overlap checks may receive malformed existing entries. | Booking helper | `assignment3/booking.py:2-15` | Plausible | 2 | 3 | 6 | Add explicit numeric/type and existing-entry validation. | Booking owner | Add boundary, negative, malformed-type, and malformed-existing-entry tests. | 6 | Medium: confirmed at code-review level but not in runtime baseline. |
| R5 | Dependency | No package manifest or lockfile pins the environment. | Repository setup | Repository map; no manifest or lockfile found. | Plausible | 2 | 2 | 4 | Introduce and approve a dependency manifest/lock only when dependencies are needed. | Repository maintainer | Verify manifest, lockfile, tool versions, and clean-environment setup. | 4 | Medium: environment reproducibility is unverified. |
| R6 | Agent operations / Testing | Repository-wide lint and formatting checks retain baseline failures. | Assignment3 and Assignment4 files | Final full Ruff lint reported 2 I001 errors; formatting reported 4 files. | **Confirmed** | 2 | 1 | 2 | Format existing assignment files and fix import blocks. | Repository maintainer | Run Ruff lint and format check again. | 2 | Medium until the baseline formatting debt is resolved. |
| R7 | Security / Operations | WSGI implementation lacks authentication, deployment hardening, and real server integration evidence. | Assignment5 application | `assignment5/app.py:47-115`; no server configuration or security tests exist. | Unsupported by repository requirements | 1 | 3 | 3 | Keep as local acceptance implementation; add auth/server controls if deployed. | API owner | Run server integration and security review before deployment. | 3 | High for future deployment; no production deployment is in scope. |

**Top confirmed risks**

1. **R1 - Invalid payload handling:** initially 9/9, reduced to 3/9 by parsing and validation.
2. **R2 - Duplicate pytest modules:** initially 6/9, reduced to 2/9 by renaming the Assignment4 test module.

## 6. Task #06 - Agent-Readiness Audit

| Area | Evaluation | Evidence / Missing Evidence |
|---|---|---|
| Structure | Partial | Assignment directories are understandable, but duplicate modules and no package boundaries reduce robustness. |
| README | Partial | Assignment5 README states acceptance criteria, but it does not document setup, run commands, or API start instructions. |
| Pinned dependencies | Missing | No manifest or lockfile exists. Standard-library implementation does not require third-party dependencies, but tool versions are still unpinned. |
| Checks | Partial | Pytest and compile checks pass; full Ruff lint/format checks fail on baseline files; mypy passes per directory. |
| Security | Partial | Payload validation exists; no authentication, authorization, real-server, or security-test configuration is present. |
| `AGENTS.md` | Present | Root instructions cover purpose, architecture, commands, conventions, test expectations, and forbidden actions. |

**Justified readiness level: Level 2 - Documented**

The repository has explicit agent instructions and a passing test suite, but it is not Level 3 because a baseline final commit is absent, full lint/format checks are failing, dependencies/tools are not pinned, CI is absent, and no real WSGI server integration evidence exists.

## 7. Task #07 - Mitigation & Verification

### M1 - Invalid JSON and missing fields

The WSGI handler was changed to parse JSON before storage mutation, reject non-dictionaries, validate a non-empty `title`, and return 400 responses. Storage mutation occurs only after validation.

Relevant code:

- [assignment5/app.py:59-81](/Users/gatiyatullinibragim/soft/software/assignment5/app.py:59)
- [assignment5/test_app.py:57-74](/Users/gatiyatullinibragim/soft/software/assignment5/test_app.py:57)

### M2 - Duplicate test module name

The Assignment4 test was renamed from `test_booking.py` to `test_assignment4_booking.py`. The old tracked file was deleted and the new file was created.

### Git diff highlights

Final diff statistics:

```text
 assignment4/assignment3/test_booking.py | 28 --------
 assignment5/app.py                      | 115 +++++++++++++++++++++++++++++++
 assignment5/test_app.py                | 92 +++++++++++++++++++++++++
 3 files changed, 207 insertions(+), 28 deletions(-)
```

Summary:

```text
 delete mode 100644 assignment4/assignment3/test_booking.py
 create mode 100644 assignment5/app.py
 create mode 100644 assignment5/test_app.py
```

### Before/after test results

Before implementation:

```sh
python3 -m pytest -q
```

```text
==================================== ERRORS ====================================
___________ ERROR collecting assignment4/assignment3/test_booking.py ___________
import file mismatch:
imported module 'test_booking' has this __file__ attribute:
  /Users/gatiyatullinibragim/soft/software/assignment3/test_booking.py
which is not the same as the test file we want to collect:
  /Users/gatiyatullinibragim/soft/software/assignment4/assignment3/test_booking.py
HINT: remove __pycache__ / .pyc files and/or use a unique basename for your test file modules
=========================== short test summary info ============================
ERROR assignment4/assignment3/test_booking.py
!!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
1 error in 0.00s
```

Exit status: `2`.

After implementation:

```sh
python3 -m pytest -q
```

```text
.......                                                                  [100%]
7 passed in 0.02s
```

Exit status: `0`.

The Assignment5 focused test run produced:

```sh
cd assignment5 && python3 -m pytest -q
```

```text
.....                                                                    [100%]
5 passed in 0.01s
```

Assignment3 and Assignment4 per-directory runs each passed once. Compile check passed with no output.

Per-directory mypy output:

```text
Success: no issues found in 2 source files
```

This exact success text was produced independently for Assignment3, Assignment4, and Assignment5.

Residual limitations:

- The full Ruff linter and formatter remain failing on existing assignment3/assignment4 files.
- A combined mypy run still risks duplicate-module naming unless run per directory.
- No real HTTP server was started or tested.
- No final commit exists, so there is no immutable final commit hash.

## 8. Task #08 - Background Agent Safeguards

### Hypothetical task specification

**Task:** Resolve remaining formatting debt and establish clean repository validation.

**Execution location**

- Create an isolated branch and worktree from the verified baseline commit.
- Suggested branch name: `agent/formatting-and-ci-readiness`.
- The worktree must not contain production deployment configuration or secrets.

**Allowed files**

- `assignment3/booking.py`
- `assignment3/test_booking.py`
- `assignment4/assignment3/booking.py`
- `assignment4/assignment3/test_assignment4_booking.py`
- `assignment5/app.py`
- `assignment5/test_app.py`
- `AGENTS.md`
- `ASSIGNMENT_05_REPORT.md`
- A package/tool configuration file only if explicitly approved.

**Allowed commands**

- Read-only `git status`, `git diff`, `git show`, and file listing.
- `python3 -m pytest -q`
- `python3 -m compileall -q assignment3 assignment4 assignment5`
- `ruff check` and `ruff format --check`
- `mypy` per directory, or combined only after package naming is approved.
- `ruff format` only for explicitly listed formatting files.

**Timeouts**

- Each terminal command: 5-minute timeout.
- Full agent turn: 30-minute timeout.
- Stop immediately on unexpected file changes or destructive-command attempts.

**Forbidden actions**

- No source/test changes outside the human-approved file scope.
- No dependency additions or manifest updates without approval.
- No production deployment, network publishing, secret access, or credential use.
- No `git reset --hard`, `git clean`, force push, merge, release, or commit without approval.
- No bypassing, deleting, or weakening assertions and checks.

**Required artifacts**

- Exact `git diff` of changed files.
- Full pytest, Ruff, formatting, mypy, and compile outputs.
- A final worktree status.
- A list of assumptions and unresolved failures.

**Mandatory human approval gate**

The agent must stop after implementation and before commit, push, merge, dependency changes, formatting changes to unrelated files, or any destructive action. A human must review and approve the diff and verification outputs.

**Rollback plan**

1. Stop the agent and remove it from the worktree.
2. Inspect `git diff`.
3. If the isolated branch/worktree is disposable, delete only that explicitly identified worktree and branch after human approval.
4. Restore no user-unrelated files.
5. Preserve the original baseline commit `fc3c6a53d5a3ee294481e3fa9fa8f48fcf098b05`.

## 9. Task #09 - Release Decision

**Decision: CONDITIONAL**

Justification:

- The full pytest suite passed with `7 passed`.
- Assignment5 has five focused tests covering create/list/delete, invalid JSON state preservation, missing fields, missing IDs, and strategy replacement.
- Mypy passed for all three areas when run per directory.
- The compile check passed.
- R1 and R2, the two requested confirmed risks, were addressed and received updated scores of 3/9 and 2/9.
- The readiness level is Level 2 - Documented, not Level 3 - Agent-ready.
- Full repository Ruff lint and formatting checks still fail.
- No final commit exists.
- No real server integration, CI workflow, dependency lock, or deployment security evidence exists.

Before release, at minimum: resolve or explicitly document remaining Ruff failures, create and review a final commit, start and integration-test the WSGI application over a real server, and ensure repository-wide CI commands are green.

## 10. Task #10 - AI Reflection

I used an AI assistant operating through the Copilot SDK in VS Code. The underlying model identifier was not disclosed, so I will not claim one. Context included the repository, tagged `AGENTS.md`, acceptance criteria, prior read-only findings, terminal results, and explicit placeholders for the implementation pattern and two risks. The most useful contribution was turning the duplicate test basename and invalid-payload gap into concrete, verifiable changes: test collection became repository-wide successful, and invalid requests were shown not to mutate state. A weak point was interpreting the original placeholder text as a storage/filtering pattern; the user clarified only that both storage strategy and invalid payload/duplicate test mitigations were required, while the task did not prescribe the HTTP implementation framework. I personally verified behavior with the real commands and outputs, not assumptions: full pytest reported seven passes, focused Assignment5 pytest reported five passes, compileall returned no errors, and per-directory mypy reported no issues. I also reported Ruff and formatting failures rather than hiding them. `AGENTS.md` materially improved scope discipline by listing forbidden actions and safe commands. It prevented source changes during the baseline phase, prohibited secret exposure and deployment, and helped distinguish actual command success from unavailable or failing checks. Its safe-command list should later be expanded because it still names pre-mitigation test paths and omits Assignment5 commands.

## AI Evidence Appendix

| Tool & Model | Date | Prompt Summary | Output Used | Problems Found | Changes Made | Verification Source |
|---|---|---|---|---|---|---|
| Copilot SDK in VS Code; model identifier not disclosed | 2026-11-20 | Inspect repository, run baseline checks, draft governance instructions, perform read-only risk review | Repository map, direct pytest outputs, full pytest error, Ruff, mypy, compileall, git status | Duplicate test names, missing HTTP implementation, shallow test coverage, formatting debt, duplicate modules | Created root `AGENTS.md`; no application source changes | Baseline commands and git status captured in session |
| Copilot SDK in VS Code; model identifier not disclosed | 2026-11-20 | Implement requested storage pattern and two mitigations | Verified baseline commit and acceptance criteria | Invalid JSON could mutate or fail storage; duplicate module basename blocked repository pytest | Renamed Assignment4 test; added WSGI application and five tests; updated instructions | Focused and full pytest, Ruff, formatting, per-directory mypy, compileall |
| Copilot SDK in VS Code; model identifier not disclosed | 2026-11-20 | Generate this submission report using only verified facts | Session terminal outputs, full HEAD hash, remote URL, final git diff/status, numbered files | No final commit, four formatting files, remaining full-lint failures | Added `ASSIGNMENT_05_REPORT.md`; no source changes in report-only step | Report evidence appendix and final git verification |
