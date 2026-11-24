from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class DeviceProfile:
    name: str
    udid: str
    platform_version: str
    system_port: int
    allure_results_dir: Path
    visual_baseline_dir: str


DEFAULT_DEVICE_PROFILE = "pixel_api31"

DEVICE_PROFILES = {
    "pixel_api31": DeviceProfile(
        name="pixel_api31",
        udid="emulator-5554",
        platform_version="12",
        system_port=8200,
        allure_results_dir=Path("allure-results"),
        visual_baseline_dir="android-emulator-5554",
    ),
    "small_phone_api34": DeviceProfile(
        name="small_phone_api34",
        udid="emulator-5556",
        platform_version="14",
        system_port=8201,
        allure_results_dir=Path("allure-results-small_phone_api34"),
        visual_baseline_dir="small_phone_api34",
    ),
}


def get_device_profile(name: str | None = None) -> DeviceProfile:
    profile_name = name or DEFAULT_DEVICE_PROFILE
    try:
        return DEVICE_PROFILES[profile_name]
    except KeyError as error:
        available_profiles = ", ".join(DEVICE_PROFILES)
        raise ValueError(
            f"Unknown device profile '{profile_name}'. "
            f"Available profiles: {available_profiles}."
        ) from error
