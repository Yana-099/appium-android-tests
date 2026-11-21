import allure
import pytest

from config.settings import APP_PACKAGE
from pages.menu_page import MenuPage


@pytest.mark.regression
@allure.tag("regression")
@allure.epic("Mobile Demo App")
@allure.feature("Жизненный цикл приложения")
@allure.story("Сворачивание приложения")
@allure.title("Приложение не падает при сворачивании с открытым меню")
def test_app_does_not_crash_after_backgrounding_with_open_menu(driver):
    # Выполняем предусловие: открываем боковое меню на главном экране.
    with allure.step("Предусловие: открыть боковое меню"):
        menu_page = MenuPage(driver).open()

    # Сворачиваем приложение и возвращаем его на передний план.
    with allure.step("Свернуть и восстановить приложение"):
        driver.background_app(2)
        driver.activate_app(APP_PACKAGE)

    # Проверяем, что приложение не упало и меню осталось доступным.
    with allure.step("Проверить доступность бокового меню"):
        assert menu_page.is_open
