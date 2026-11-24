from appium.options.android import UiAutomator2Options

from config.device_profiles import DeviceProfile
from config.settings import APP_ACTIVITY, APP_PACKAGE


def create_android_options(device_profile: DeviceProfile) -> UiAutomator2Options:
    return UiAutomator2Options().load_capabilities(
        {
            "platformName": "Android",
            "appium:automationName": "UiAutomator2",
            "appium:udid": device_profile.udid,
            "appium:platformVersion": device_profile.platform_version,
            "appium:systemPort": device_profile.system_port,
            "appium:appPackage": APP_PACKAGE,
            "appium:appActivity": APP_ACTIVITY,
            "appium:noReset": False,
        }
    )
