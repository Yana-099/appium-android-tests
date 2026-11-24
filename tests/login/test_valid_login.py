import allure
import pytest
from qase.pytest import qase

from config.test_data import STANDARD_PASSWORD, STANDARD_USERNAME
from pages.login_page import LoginPage
from pages.menu_page import MenuPage
from pages.products_page import ProductsPage


@qase.id(1)
@pytest.mark.smoke
@pytest.mark.regression
@allure.tag("smoke", "regression")
@allure.severity(allure.severity_level.CRITICAL)
@allure.epic("Mobile Demo App")
@allure.feature("Авторизация")
@allure.story("Успешный вход")
@allure.title("AMT-1: вход с валидными данными")
def test_valid_user_can_log_in(driver):
    with allure.step("Открыть приложение"):
        assert ProductsPage(driver).wait_until_loaded().is_open

    with allure.step("Открыть боковое меню"):
        menu_page = MenuPage(driver).open()
        assert menu_page.is_open

    with allure.step("Выбрать пункт Login"):
        menu_page.open_login()
        login_page = LoginPage(driver)
        assert login_page.title == "Login"
        assert login_page.is_username_field_enabled
        assert login_page.is_password_field_enabled
        assert login_page.login_button_text == "Login"

    with allure.step("Ввести Username"):
        login_page.enter_username(STANDARD_USERNAME)
        assert login_page.entered_username == STANDARD_USERNAME

    with allure.step("Ввести Password"):
        login_page.enter_password(STANDARD_PASSWORD)
        assert login_page.entered_password
        assert login_page.entered_password != STANDARD_PASSWORD

    with allure.step("Нажать кнопку Login"):
        login_page.submit_login()
        assert ProductsPage(driver).wait_until_loaded().is_open
        assert not login_page.error_message

    with allure.step("Проверить наличие пункта Logout"):
        assert MenuPage(driver).open().has_logout_item
