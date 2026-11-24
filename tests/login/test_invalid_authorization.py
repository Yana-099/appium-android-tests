import allure
import pytest

from config.test_data import INVALID_PASSWORD, STANDARD_USERNAME
from pages.login_page import LoginPage

EXPECTED_LOGIN_ERROR = "Provided credentials do not match any user in this service."


@pytest.mark.negative
@pytest.mark.regression
@allure.tag("negative", "regression")
@allure.epic("Mobile Demo App")
@allure.feature("Авторизация")
@allure.story("Неверные учётные данные")
@allure.title("Пользователь видит понятную ошибку при неверном пароле")
def test_invalid_password_shows_authorization_error(driver):
    with allure.step("Открыть форму Login"):
        login_page = LoginPage(driver).open()

    with allure.step("Ввести существующий логин"):
        login_page.enter_username(STANDARD_USERNAME)

    with allure.step("Ввести неверный пароль"):
        login_page.enter_password(INVALID_PASSWORD)

    with allure.step("Нажать Login"):
        login_page.submit_login()

    # Проверяем, что неверный пароль не авторизовал пользователя.
    with allure.step("Проверить, что пользователь остался на форме Login"):
        assert login_page.is_open, (
            "Пользователь с неверным паролем был авторизован и покинул форму Login."
        )

    # Проверяем понятный текст ошибки, который видит пользователь.
    with allure.step("Проверить текст ошибки авторизации"):
        assert login_page.error_message == EXPECTED_LOGIN_ERROR, (
            "Пользователь остался на форме Login, но приложение не показало "
            "ожидаемое сообщение об ошибке авторизации."
        )
