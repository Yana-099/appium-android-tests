import allure
import pytest

from config.test_data import STANDARD_PASSWORD, STANDARD_USERNAME
from pages.login_page import LoginPage
from pages.menu_page import MenuPage
from pages.products_page import ProductsPage


@pytest.mark.regression
@allure.tag("regression")
@allure.severity(allure.severity_level.CRITICAL)
@allure.epic("Mobile Demo App")
@allure.feature("Авторизация")
@allure.story("Успешный вход")
@allure.title("Стандартный пользователь может авторизоваться")
def test_standard_user_can_authorize(driver):
    # Открываем приложение и проверяем стартовый экран каталога.
    with allure.step("Открыть приложение"):
        assert ProductsPage(driver).wait_until_loaded().is_open

    # Открываем боковое меню и проверяем доступность пункта Login.
    with allure.step("Открыть боковое меню"):
        menu_page = MenuPage(driver).open()
        assert menu_page.is_open

    # Переходим к форме Login для ввода учётных данных.
    with allure.step("Открыть форму Login"):
        menu_page.open_login()
        login_page = LoginPage(driver)

    # Вводим корректное значение в поле Username и проверяем его сохранение.
    with allure.step("Ввести корректный логин"):
        login_page.enter_username(STANDARD_USERNAME)
        assert login_page.entered_username == STANDARD_USERNAME

    # Вводим пароль и проверяем, что поле содержит маскированное значение.
    with allure.step("Ввести корректный пароль"):
        login_page.enter_password(STANDARD_PASSWORD)
        assert login_page.entered_password
        assert login_page.entered_password != STANDARD_PASSWORD

    # Подтверждаем авторизацию и проверяем переход в каталог с пунктом Logout.
    with allure.step("Нажать кнопку Login"):
        login_page.submit_login()
        assert ProductsPage(driver).wait_until_loaded().is_open
        assert MenuPage(driver).open().has_logout_item
