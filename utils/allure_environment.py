from pathlib import Path

from config.device_profiles import DeviceProfile
from config.settings import APP_PACKAGE, APPIUM_SERVER_URL


def write_allure_environment(device_profile: DeviceProfile) -> None:
    results_dir = device_profile.allure_results_dir
    results_dir.mkdir(parents=True, exist_ok=True)
    environment = (
        f"Appium URL={APPIUM_SERVER_URL}\n"
        f"Device profile={device_profile.name}\n"
        f"Device={device_profile.udid}\n"
        f"Platform=Android\n"
        f"Platform version={device_profile.platform_version}\n"
        f"UiAutomator2 system port={device_profile.system_port}\n"
        f"Application package={APP_PACKAGE}\n"
    )
    (results_dir / "environment.properties").write_text(environment, encoding="utf-8")
    categories_source = Path(__file__).resolve().parents[1] / "config" / "allure_categories.json"
    (results_dir / "categories.json").write_text(
        categories_source.read_text(encoding="utf-8"),
        encoding="utf-8",
    )
