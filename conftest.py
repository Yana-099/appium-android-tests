import allure
import pytest
from appium import webdriver
from allure_commons.types import AttachmentType

from config.capabilities import create_android_options
from config.device_profiles import (
    DEFAULT_DEVICE_PROFILE,
    DEVICE_PROFILES,
    DeviceProfile,
    get_device_profile,
)
from config.settings import APP_PACKAGE, APPIUM_SERVER_URL
from config.test_data import STANDARD_PASSWORD, STANDARD_USERNAME
from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from utils.android_device import AndroidDeviceCommandError, get_crash_logcat, get_failure_logcat
from utils.allure_environment import write_allure_environment
from utils.allure_results import remove_internal_fixture_steps
from utils.screenshots import save_failure_screenshot

DEVICE_PROFILE_KEY = pytest.StashKey[DeviceProfile]()


def pytest_addoption(parser):
    parser.addoption(
        "--device",
        action="store",
        choices=tuple(DEVICE_PROFILES),
        default=DEFAULT_DEVICE_PROFILE,
        help="Android device profile used for this test run",
    )
    parser.addoption(
        "--run-crash-demo",
        action="store_true",
        default=False,
        help="run intentionally failing crash demonstration tests",
    )


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    device_profile = get_device_profile(config.getoption("--device"))
    config.stash[DEVICE_PROFILE_KEY] = device_profile
    config.option.allure_report_dir = str(device_profile.allure_results_dir)


def pytest_collection_modifyitems(config, items):
    if config.getoption("--run-crash-demo"):
        return

    skip_crash_demo = pytest.mark.skip(
        reason="Демонстрационный кейс падения. Запустите с --run-crash-demo."
    )
    for item in items:
        if "crash_demo" in item.keywords:
            item.add_marker(skip_crash_demo)


@pytest.fixture(scope="session")
def device_profile(pytestconfig) -> DeviceProfile:
    return pytestconfig.stash[DEVICE_PROFILE_KEY]


@pytest.fixture
def driver(request, device_profile):
    write_allure_environment(device_profile)
    session = webdriver.Remote(
        APPIUM_SERVER_URL,
        options=create_android_options(device_profile),
    )

    def close_appium_session():
        with allure.step("Закрыть Appium-сессию"):
            session.quit()

    request.addfinalizer(close_appium_session)
    return session


@pytest.fixture
def authorized_driver(driver):
    with allure.step("Авторизовать стандартного пользователя"):
        LoginPage(driver).open().login(STANDARD_USERNAME, STANDARD_PASSWORD)
        ProductsPage(driver).wait_until_loaded()
    return driver


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        session = item.funcargs.get("driver")
        if session:
            device_profile = item.funcargs["device_profile"]
            screenshot_path = save_failure_screenshot(session, item.name)
            allure.attach.file(
                str(screenshot_path),
                name="Скриншот при ошибке",
                attachment_type=AttachmentType.PNG,
            )
            allure.attach(
                session.page_source,
                name="Исходный код страницы при ошибке",
                attachment_type=AttachmentType.XML,
            )
            try:
                is_crash_demo = "crash_demo" in item.keywords
                allure.attach(
                    (
                        get_crash_logcat(device_profile.udid, APP_PACKAGE)
                        if is_crash_demo
                        else get_failure_logcat(device_profile.udid, APP_PACKAGE)
                    ),
                    name=(
                        "Android logcat: причина аварийного завершения"
                        if is_crash_demo
                        else "Android logcat при ошибке"
                    ),
                    attachment_type=AttachmentType.TEXT,
                )
            except AndroidDeviceCommandError as error:
                allure.attach(
                    str(error),
                    name="Не удалось получить Android logcat",
                    attachment_type=AttachmentType.TEXT,
                )


@pytest.hookimpl(trylast=True)
def pytest_sessionfinish(session, exitstatus):
    device_profile = session.config.stash[DEVICE_PROFILE_KEY]
    remove_internal_fixture_steps(results_dir=device_profile.allure_results_dir)
