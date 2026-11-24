# Appium Android UI Tests

[![Python](https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![pytest](https://img.shields.io/badge/pytest-9.2.0-0A9EDC?logo=pytest&logoColor=white)](https://pytest.org/)
[![Appium](https://img.shields.io/badge/Appium-6.1.7-EE376D?logo=appium&logoColor=white)](https://appium.io/)
[![Android](https://img.shields.io/badge/Platform-Android-3DDC84?logo=android&logoColor=white)](https://www.android.com/)
[![Smoke tests](https://github.com/Yana-099/appium-android-tests/actions/workflows/android-self-hosted.yml/badge.svg?branch=main)](https://github.com/Yana-099/appium-android-tests/actions/workflows/android-self-hosted.yml)
[![Allure Report](https://img.shields.io/badge/Allure_Report-GitHub_Pages-7B68EE?logo=allure&logoColor=white)](https://yana-099.github.io/appium-android-tests/)

Portfolio project with automated UI tests for the [Sauce Labs My Demo App](https://github.com/saucelabs/my-demo-app-android) Android application.

The project demonstrates a maintainable mobile test automation framework built with Python, pytest, Appium, Page Object Model, and Allure reporting.

## Highlights

- Page Object Model structure with reusable page classes.
- One test scenario per file, grouped by business area.
- Allure steps, labels, screenshots, page source, and Android logcat attachments on failure.
- Pillow-based visual regression test with baseline, actual, diff, and comparison metrics in Allure.
- Centralized test data in `config/test_data.py`.
- pytest markers: `smoke`, `regression`, `negative`, `visual`, and `crash_demo`.
- A deliberately failing crash demonstration is isolated and runs only with `--run-crash-demo`.

## Portfolio scope

The mobile suite is intentionally curated rather than optimized for test count. Each retained scenario demonstrates either distinct business coverage or a separate automation capability, such as Android lifecycle handling, ADB interaction, visual comparison, failure diagnostics, or parameterized device profiles. Redundant checks and persistently unstable scenarios are kept out of the automated portfolio suite so its regular runs remain focused and trustworthy.

## Allure step design

The project uses a hybrid approach to Allure steps:

- Reusable UI actions, such as opening a product, adding it to the cart, opening the cart, and proceeding through Checkout, are declared with `@allure.step` in Page Object methods.
- Scenario-specific business checks, form validation, lifecycle actions, diagnostic attachments, and assertions remain explicit `with allure.step(...)` blocks in the test files.
- Soft assertions are intentionally not used: the project uses regular `assert` statements so a critical scenario stops at the exact point of failure.

This keeps repeated implementation details in one place while preserving clear, business-readable steps in Allure reports.

## Tech stack

- Python 3
- pytest
- Appium Python Client
- UiAutomator2
- Android Emulator
- Allure Report
- Pillow

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

The shared Appium configuration is stored in `config/settings.py`, while named devices are defined in `config/device_profiles.py`:

- default profile: `pixel_api31` (`emulator-5554`)
- additional profile: `small_phone_api34` (`emulator-5556`)
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
pytest tests/login/test_valid_login.py -v
```

Run tests with a marker:

```bash
pytest -m smoke -v
pytest -m regression -v
pytest -m negative -v
pytest -m visual -v
```

Select a device profile when pytest starts:

```powershell
pytest -m smoke --device pixel_api31
pytest -m smoke --device small_phone_api34
```

When `--device` is omitted, pytest uses `pixel_api31` to preserve the existing local workflow. The Small Phone profile expects its emulator to be available as `emulator-5556`.

The crash diagnostic demonstration is intentionally failing and skipped by default. Run it explicitly only when needed:

```bash
pytest tests/lifecycle/test_crash_demo.py --run-crash-demo -v
```

## Visual regression test

The product card visual test complements functional assertions by checking the rendered layout of the product image, title, price, rating, color selector, quantity controls, and Add to cart button. The captured region excludes Android system bars and the transient right-edge scrollbar.

Run the visual test separately:

```bash
pytest -m visual -v
```

The committed baseline supports one fixed environment profile:

- device: `emulator-5554`
- resolution: `1080x2400`
- orientation: portrait
- baseline: `tests/visual/baselines/android-emulator-5554/product_card.png`

Pillow compares the baseline and actual RGB images without resizing them. A pixel is treated as changed when at least one color channel differs by more than `8`; the test fails when changed pixels occupy more than `0.1%` of the captured region. These thresholds were calibrated on repeated runs of the fixed emulator profile and should be recalibrated before adding another device or Android configuration.

Every comparison adds the following attachments to Allure:

- `Визуальный эталон` — committed baseline image;
- `Фактический результат` — screenshot captured during the current run;
- `Визуальная разница` — grayscale actual image with changed pixels highlighted in red;
- `Метрики визуального сравнения` — JSON with changed-pixel counts, ratio, thresholds, and pass status.

If image dimensions differ, the test does not resize them. Allure receives both input images, a side-by-side diagnostic image, and structured error details. Baselines are never updated automatically during a normal test run.

## Allure reports

Pytest writes raw results to `allure-results/`. To open a report after a test run:

```bash
allure serve allure-results
```

## Test data and safety

Credentials and payment values in `config/test_data.py` are public demo data for the test application; they are not personal or production credentials. Do not add real secrets, tokens, or personal data to the repository.

## Device profiles and multi-device execution

Each pytest process runs on one selected Android device profile. The available profiles are:

- `pixel_api31` — the current Pixel 6 emulator and default profile;
- `small_phone_api34` — a lightweight Small Phone emulator with Android 14 / API 34, Google APIs x86_64, 2 CPU cores, and 2 GB RAM.

Each profile provides its own UDID, Android version, UiAutomator2 system port, visual-baseline directory, and Allure results directory. The default profile keeps `allure-results/`; the Small Phone profile writes to `allure-results-small_phone_api34/`.

Several profiles can be tested sequentially by running pytest once per profile. Parallel execution is technically possible with the separate UDIDs, system ports, and result directories, but it is intentionally not implemented to keep this portfolio project simple. A later GitHub Actions update may add a device selector and an `all` option that runs these commands sequentially.

## Notes

This repository is intended as a QA automation portfolio project. Local environments, generated reports, screenshots, logs, and bundled tools are excluded from Git.
