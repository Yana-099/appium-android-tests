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
    with allure.step("Открыть боковое меню и перейти на форму Login"):
        login_page = LoginPage(driver).open()

    # Проверяем заголовок формы.
    with allure.step("Проверить заголовок формы: Login"):
        assert login_page.title == "Login"

    # Проверяем текст подсказки для тестовых учётных данных.
    with allure.step("Проверить подсказку по выбору учётных данных"):
        assert login_page.help_text == LOGIN_HELP_TEXT

    # Проверяем подпись поля имени пользователя.
    with allure.step("Проверить подпись поля Username"):
        assert login_page.username_label == "Username"

    # Проверяем подпись поля пароля.
    with allure.step("Проверить подпись поля Password"):
        assert login_page.password_label == "Password"

    # Проверяем доступность поля имени пользователя.
    with allure.step("Проверить доступность поля Username"):
        assert login_page.is_username_field_enabled

    # Проверяем доступность поля пароля.
    with allure.step("Проверить доступность поля Password"):
        assert login_page.is_password_field_enabled

    # Проверяем доступность кнопки входа.
    with allure.step("Проверить доступность кнопки Login"):
        assert login_page.login_button_text == "Login"
        assert login_page.is_login_button_enabled
