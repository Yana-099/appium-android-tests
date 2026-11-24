from dataclasses import replace
from pathlib import Path

import pytest

from config.capabilities import create_android_options
from config.device_profiles import get_device_profile
from utils.allure_environment import write_allure_environment


def test_default_device_profile_preserves_current_emulator_and_results_directory():
    profile = get_device_profile()

    assert profile.name == "pixel_api31"
    assert profile.udid == "emulator-5554"
    assert profile.platform_version == "12"
    assert profile.system_port == 8200
    assert profile.allure_results_dir.as_posix() == "allure-results"


def test_small_phone_profile_has_independent_appium_and_results_settings():
    profile = get_device_profile("small_phone_api34")

    assert profile.name == "small_phone_api34"
    assert profile.udid == "emulator-5556"
    assert profile.platform_version == "14"
    assert profile.system_port == 8201
    assert profile.allure_results_dir.as_posix() == "allure-results-small_phone_api34"


def test_unknown_device_profile_is_rejected_with_available_names():
    with pytest.raises(ValueError, match="pixel_api31, small_phone_api34"):
        get_device_profile("unknown")


def test_android_options_use_selected_profile_capabilities():
    profile = get_device_profile("small_phone_api34")

    capabilities = create_android_options(profile).to_capabilities()

    assert capabilities["appium:udid"] == "emulator-5556"
    assert capabilities["appium:platformVersion"] == "14"
    assert capabilities["appium:systemPort"] == 8201


def test_allure_environment_is_written_to_selected_profile_directory(
    tmp_path, monkeypatch
):
    profile = replace(
        get_device_profile("small_phone_api34"),
        allure_results_dir=Path("profile-results"),
    )
    monkeypatch.chdir(tmp_path)

    write_allure_environment(profile)

    environment = (tmp_path / "profile-results" / "environment.properties").read_text(
        encoding="utf-8"
    )
    assert "Device profile=small_phone_api34" in environment
    assert "Device=emulator-5556" in environment
    assert (tmp_path / "profile-results" / "categories.json").exists()
