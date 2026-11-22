import allure
import pytest
from qase.pytest import qase

from pages.login_page import LoginPage
from pages.menu_page import MenuPage


@qase.id(2)
@pytest.mark.smoke
@pytest.mark.regression
@allure.tag("smoke", "regression")
@allure.severity(allure.severity_level.CRITICAL)
@allure.epic("Mobile Demo App")
@allure.feature("Авторизация")
@allure.story("Выход из аккаунта")
@allure.title("AMT-2: выход из аккаунта")
def test_authorized_user_can_log_out(authorized_driver):
    with allure.step("Открыть боковое меню"):
        menu_page = MenuPage(authorized_driver).open()
        assert menu_page.has_logout_item

    with allure.step("Выбрать пункт Logout"):
        menu_page.open_logout_dialog()
        assert menu_page.logout_dialog_title == "Log Out"
        assert (
            menu_page.logout_dialog_message
            == "Are you sure you want to logout"
        )
        assert menu_page.cancel_logout_button_text == "CANCEL"
        assert menu_page.confirm_logout_button_text == "LOGOUT"

    with allure.step("Подтвердить выход кнопкой LOGOUT"):
        menu_page.confirm_logout()
        assert LoginPage(authorized_driver).title == "Login"
