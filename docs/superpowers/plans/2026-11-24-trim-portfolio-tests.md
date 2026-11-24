# Portfolio Test Suite Trimming Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Remove six low-value mobile tests and keep the portfolio documentation aligned with the curated suite.

**Architecture:** Delete only redundant test modules; retain framework and Page Object code because remaining tests still consume it. Update README wording to explain that the portfolio favors distinct techniques over test count.

**Tech Stack:** Python, pytest, Appium, Allure, Markdown

**Spec:** `docs/superpowers/specs/2026-11-24-trim-portfolio-tests-design.md`

## Global Constraints

- Work from fresh `origin/main` commit `8adcaad` in an isolated branch.
- Do not modify the user's dirty `test/qase-login-logout` working tree.
- Do not make remote Qase changes.
- Do not run Appium UI sessions during this cleanup.

## Review Focus

- Removed tests must no longer be collected.
- Retained tests must still import and collect successfully.
- README must not claim removed automated coverage.
- Smoke and regression markers must remain meaningful after logout removal.
- Unit/tool coverage for device profiles, visual comparison, and Telegram must remain green.

---

### Task 1: Remove redundant mobile test modules

**Files:**
- Delete: the six test modules listed in the design spec.

**Interfaces:**
- Consumes: existing pytest discovery conventions.
- Produces: a curated mobile test collection with no replacement code.

- [ ] Delete the six agreed test files.
- [ ] Run `pytest --collect-only -q` and confirm the removed test names are absent.

### Task 2: Align portfolio configuration and documentation

**Files:**
- Modify: `README.md`
- Modify: `CONTRIBUTING.md`
- Modify: `docs/github-actions-self-hosted.md`
- Modify: `pytest.ini`
- Modify: `.github/workflows/android-self-hosted.yml`
- Modify: `pages/menu_page.py`

**Interfaces:**
- Consumes: the final curated test list.
- Produces: accurate portfolio documentation.

- [ ] Add a concise portfolio-scope note explaining the focus on distinct techniques.
- [ ] Remove obsolete `known_bug` launch options and references to deleted files.
- [ ] Remove logout dialog Page Object members no longer consumed by retained tests.
- [ ] Verify documentation references and example paths against existing files.

### Task 3: Verify and commit

**Files:**
- Test: `tests/unit/`, `tests/tools/`, and complete collection.

**Interfaces:**
- Consumes: Tasks 1 and 2.
- Produces: a reviewable branch ready for Pull Request.

- [ ] Run unit/tool tests.
- [ ] Run full pytest collection without starting Appium.
- [ ] Review `git diff --check` and the final diff.
- [ ] Commit the verified cleanup.
