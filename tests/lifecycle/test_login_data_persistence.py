import allure
import pytest

from config.settings import APP_PACKAGE
from config.test_data import STANDARD_USERNAME
from pages.login_page import LoginPage


@pytest.mark.known_bug
@pytest.mark.negative
@allure.tag("known_bug", "negative")
@allure.epic("Mobile Demo App")
@allure.feature("Жизненный цикл приложения")
@allure.story("Восстановление формы login")
@allure.title("Поле login сохраняет введённое значение после сворачивания")
def test_login_field_keeps_value_after_backgrounding(driver):
    # Открываем форму login и вводим значение в поле Username.
    with allure.step("Открыть login и ввести значение Username"):
        login_page = LoginPage(driver).open().enter_username(STANDARD_USERNAME)

    # Сворачиваем приложение и возвращаем его на передний план.
    with allure.step("Свернуть и восстановить приложение"):
        driver.background_app(2)
        driver.activate_app(APP_PACKAGE)

    # Проверяем, что введённый логин сохранился после восстановления приложения.
    with allure.step("Проверить сохранение значения в поле Username"):
        assert login_page.entered_username == STANDARD_USERNAME
