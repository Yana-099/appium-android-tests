from pathlib import Path


def save_failure_screenshot(driver, test_name: str) -> Path:
    artifacts_dir = Path("artifacts")
    artifacts_dir.mkdir(exist_ok=True)
    screenshot_path = artifacts_dir / f"{test_name}.png"
    driver.save_screenshot(str(screenshot_path))
    return screenshot_path
