# Mobile Commerce Suite Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reorganize the Android UI tests by business area and add readable product and checkout scenarios.

**Architecture:** Keep the root driver fixture small, add an explicit `authorized_driver`, and scope `cart_with_first_product` to checkout tests. Page Objects own locators and UI actions; tests own Allure steps and assertions.

**Tech Stack:** Python 3.13, pytest 9.2, Appium-Python-Client 6.1.7, Allure pytest, Android UiAutomator2.

**Spec:** `docs/superpowers/specs/2026-11-21-mobile-commerce-suite-design.md`

## Global Constraints

- Target: `emulator-5554`, Appium `http://127.0.0.1:4723`, package `com.saucelabs.mydemoapp.android`.
- Run only the current test being validated; do not run the whole suite.
- Use concrete Russian Allure action names and separate steps for each input field.
- Do not implement checkout-form validation in this work.

## Review Focus

- Guest checkout must display Login rather than a shipping form.
- A checkout fixture must not hide product assertions in product tests.
- Each checkout page must wait for a unique visible control before interacting.
- Payment values must live only in `config/test_data.py`.
- Moving files must preserve pytest discovery and Allure report generation.

### Task 1: Reorganize existing scenarios

**Files:**
- Move: existing tests into `tests/login/`, `tests/products/`, and `tests/lifecycle/`
- Modify: `pytest.ini`

- [ ] Move existing tests into their business directories without changing their behavior.
- [ ] Add and register `smoke`, `regression`, and `negative` markers.
- [ ] Run one moved login test and one moved product test individually.

### Task 2: Shared data and prerequisites

**Files:**
- Modify: `config/test_data.py`, `conftest.py`
- Create: `tests/checkout/conftest.py`

**Interfaces:**
- Produces: `authorized_driver(driver)`, `cart_with_first_product(driver)`.

- [ ] Add named shipping and payment constants to `config/test_data.py`.
- [ ] Implement `authorized_driver` with a readable Allure setup step.
- [ ] Implement checkout-local `cart_with_first_product` without authentication.
- [ ] Run the target checkout prerequisite test individually.

### Task 3: Product and cart page coverage

**Files:**
- Modify: `pages/products_page.py`, `pages/product_details_page.py`, `pages/cart_page.py`
- Create: `tests/products/test_product_card.py`, `tests/products/test_open_cart.py`

**Interfaces:**
- Produces: product details properties, cart state properties, and checkout navigation action.

- [ ] Write the product-card test with individual assertions for name, image, price, and `Add To Cart`.
- [ ] Run it to identify missing page actions.
- [ ] Add only the required Page Object locators and methods.
- [ ] Run the product-card test individually and verify it passes.
- [ ] Repeat the same cycle for the cart-navigation test.

### Task 4: Checkout page objects and scenarios

**Files:**
- Create: `pages/checkout_shipping_page.py`, `pages/checkout_payment_page.py`, `pages/checkout_review_page.py`, `pages/checkout_complete_page.py`
- Create: `tests/checkout/test_checkout_form.py`, `tests/checkout/test_checkout_authorized.py`, `tests/checkout/test_checkout_unauthorized.py`

**Interfaces:**
- Produces: field-level shipping and payment actions plus checkout completion assertions.

- [ ] Inspect the running app for locators on each checkout screen.
- [ ] Write and run the guest-checkout test; verify `Proceed To Checkout` opens Login.
- [ ] Write and run the checkout-form test; add shipping page support until it passes.
- [ ] Write and run the authorized order test with one Allure step per shipping and payment field.
- [ ] Add payment, review, and completion page support until the target test passes.

### Task 5: Report readability and verification

**Files:**
- Modify: affected test files and Page Objects only if target-test verification exposes an issue.

- [ ] Review generated Allure steps for action-oriented Russian names.
- [ ] Run each changed test individually with the emulator connected.
- [ ] Generate a focused Allure report and confirm failure attachments still work.
