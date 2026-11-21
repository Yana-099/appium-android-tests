from pathlib import Path

from config.settings import APP_PACKAGE, APPIUM_SERVER_URL, DEVICE_UDID


def write_allure_environment() -> None:
    results_dir = Path("allure-results")
    results_dir.mkdir(exist_ok=True)
    environment = (
        f"Appium URL={APPIUM_SERVER_URL}\n"
        f"Device={DEVICE_UDID}\n"
        f"Platform=Android\n"
        f"Application package={APP_PACKAGE}\n"
    )
    (results_dir / "environment.properties").write_text(environment, encoding="utf-8")
    categories_source = Path(__file__).resolve().parents[1] / "config" / "allure_categories.json"
    (results_dir / "categories.json").write_text(
        categories_source.read_text(encoding="utf-8"),
        encoding="utf-8",
    )
