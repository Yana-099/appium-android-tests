# Portfolio Test Suite Trimming Design

## Intent

Keep the project focused on demonstrating distinct mobile automation techniques built with an AI coding agent. Prefer a smaller stable suite where each mobile test adds either unique business coverage or a unique framework capability.

## Scope

Remove six redundant or persistently failing mobile tests:

- `tests/login/test_amt_2_logout.py`
- `tests/login/test_login_form.py`
- `tests/products/test_add_product_to_cart.py`
- `tests/checkout/test_checkout_form.py`
- `tests/lifecycle/test_background_with_open_menu.py`
- `tests/lifecycle/test_login_data_persistence.py`

Update README, contributor guidance, pytest markers, and GitHub Actions choices so they match the remaining suite. Remove Page Object methods used only by the deleted logout test. Keep the Qase test case for logout outside the automated repository if it remains useful as a manual case or known product issue.

## Non-goals

- Do not change Page Object behavior used by retained tests.
- Do not remove stable tests that demonstrate unique Android, visual, reporting, or multi-device capabilities.
- Do not change Qase remotely in this change.

## Validation

- Pytest collection contains none of the six removed test functions.
- Unit/tool tests pass.
- Remaining mobile tests collect successfully without starting Appium sessions.
- README contains no obsolete logout command or claim that the removed known-bug test remains automated.
