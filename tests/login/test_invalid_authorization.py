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
    # Открываем форму login и вводим существующий логин с неверным паролем.
    with allure.step("Ввести существующий логин и неверный пароль"):
        login_page = LoginPage(driver).open()
        login_page.login(STANDARD_USERNAME, INVALID_PASSWORD)

    # Фиксируем состояние экрана с сообщением об ошибке для отчёта Allure.
    with allure.step("Приложить скриншот сообщения об ошибке"):
        allure.attach(
            driver.get_screenshot_as_png(),
            name="Ошибка авторизации при неверном пароле",
            attachment_type=allure.attachment_type.PNG,
        )

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
