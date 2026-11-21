import allure
import pytest

from pages.login_page import LOGIN_HELP_TEXT, LoginPage


@pytest.mark.smoke
@pytest.mark.regression
@allure.tag("smoke", "regression")
@allure.epic("Mobile Demo App")
@allure.feature("Авторизация")
@allure.story("Проверка формы login")
@allure.title("Форма login содержит обязательные элементы")
def test_login_form_displays_required_controls(driver):
    # Открываем форму авторизации через боковое меню.
    with allure.step("Открыть форму login"):
        login_page = LoginPage(driver).open()

    # Проверяем заголовок, подсказку и подписи полей формы.
    with allure.step("Проверить тексты и подписи формы"):
        assert login_page.title == "Login"
        assert login_page.help_text == LOGIN_HELP_TEXT
        assert login_page.username_label == "Username"
        assert login_page.password_label == "Password"

    # Убеждаемся, что элементы формы доступны для взаимодействия.
    with allure.step("Проверить доступность элементов формы"):
        assert login_page.are_controls_enabled
        assert login_page.login_button_text == "Login"
