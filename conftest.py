from pathlib import Path

import allure
import pytest
from appium import webdriver
from allure_commons.types import AttachmentType

from config.capabilities import create_android_options
from config.settings import APP_PACKAGE, APPIUM_SERVER_URL
from config.test_data import STANDARD_PASSWORD, STANDARD_USERNAME
from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from utils.android_device import AndroidDeviceCommandError, get_crash_logcat, get_logcat
from utils.allure_environment import write_allure_environment
from utils.allure_results import remove_internal_fixture_steps
from utils.screenshots import save_failure_screenshot


def pytest_addoption(parser):
    parser.addoption(
        "--run-crash-demo",
        action="store_true",
        default=False,
        help="run intentionally failing crash demonstration tests",
    )


def pytest_collection_modifyitems(config, items):
    if config.getoption("--run-crash-demo"):
        return

    skip_crash_demo = pytest.mark.skip(
        reason="Демонстрационный кейс падения. Запустите с --run-crash-demo."
    )
    for item in items:
        if "crash_demo" in item.keywords:
            item.add_marker(skip_crash_demo)


@pytest.fixture
def driver(request):
    write_allure_environment()
    session = webdriver.Remote(APPIUM_SERVER_URL, options=create_android_options())

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
                    get_crash_logcat(APP_PACKAGE) if is_crash_demo else get_logcat(),
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
    remove_internal_fixture_steps(results_dir=Path("allure-results"))
