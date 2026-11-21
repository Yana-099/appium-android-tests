# Appium Android UI Tests

Portfolio project with automated UI tests for the [Sauce Labs My Demo App](https://github.com/saucelabs/my-demo-app-android) Android application.

The project demonstrates a maintainable mobile test automation framework built with Python, pytest, Appium, Page Object Model, and Allure reporting.

## Highlights

- Page Object Model structure with reusable page classes.
- One test scenario per file, grouped by business area.
- Allure steps, labels, screenshots, page source, and Android logcat attachments on failure.
- Centralized test data in `config/test_data.py`.
- pytest markers: `smoke`, `regression`, `negative`, `known_bug`, and `crash_demo`.
- A deliberately failing crash demonstration is isolated and runs only with `--run-crash-demo`.

## Tech stack

- Python 3
- pytest
- Appium Python Client
- UiAutomator2
- Android Emulator
- Allure Report

## Project structure

```text
config/     # Appium configuration, capabilities, and test data
pages/      # Page Object classes
tests/      # Test scenarios grouped by feature
utils/      # Android, Allure, and screenshot helpers
artifacts/  # Local failure artifacts (not committed)
```

## Prerequisites

Before running the tests, make sure you have:

1. Python 3 installed.
2. An Android emulator or device available through ADB.
3. Appium server installed and started.
4. The Sauce Labs My Demo App installed on the target device.
5. Allure CLI installed if you want to open Allure reports.

The current local configuration is stored in `config/settings.py`:

- device: `emulator-5554`
- Appium server: `http://127.0.0.1:4723`
- application id: `com.saucelabs.mydemoapp.android`

## Installation

```bash
python -m venv .venv
```

Activate the virtual environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install project dependencies:

```bash
pip install -r requirements.txt
```

## Running tests

Run one specific test file:

```bash
pytest tests/login/test_authorization.py -v
```

Run tests with a marker:

```bash
pytest -m smoke -v
pytest -m regression -v
pytest -m negative -v
pytest -m known_bug -v
```

The crash diagnostic demonstration is intentionally failing and skipped by default. Run it explicitly only when needed:

```bash
pytest tests/lifecycle/test_crash_demo.py --run-crash-demo -v
```

## Allure reports

Pytest writes raw results to `allure-results/`. To open a report after a test run:

```bash
allure serve allure-results
```

## Test data and safety

Credentials and payment values in `config/test_data.py` are public demo data for the test application; they are not personal or production credentials. Do not add real secrets, tokens, or personal data to the repository.

## Notes

This repository is intended as a QA automation portfolio project. Local environments, generated reports, screenshots, logs, and bundled tools are excluded from Git.
