from appium.options.android import UiAutomator2Options

from config.settings import APP_ACTIVITY, APP_PACKAGE, DEVICE_UDID


def create_android_options() -> UiAutomator2Options:
    return UiAutomator2Options().load_capabilities(
        {
            "platformName": "Android",
            "appium:automationName": "UiAutomator2",
            "appium:udid": DEVICE_UDID,
            "appium:appPackage": APP_PACKAGE,
            "appium:appActivity": APP_ACTIVITY,
            "appium:noReset": False,
        }
    )
