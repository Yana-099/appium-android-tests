import allure
import pytest

from pages.product_details_page import ProductDetailsPage
from pages.products_page import ProductsPage


@pytest.mark.regression
@allure.tag("regression")
@allure.epic("Mobile Demo App")
@allure.feature("Жизненный цикл приложения")
@allure.story("Системная кнопка Назад")
@allure.title("Системная кнопка Назад возвращает пользователя в каталог без краша")
def test_system_back_returns_to_catalog_without_crash(driver):
    # Выполняем предусловие: открываем карточку первого товара.
    with allure.step("Предусловие: открыть карточку первого товара"):
        selected_product = ProductsPage(driver).wait_until_loaded().open_first_product()
        assert ProductDetailsPage(driver).title == selected_product

    # Нажимаем системную кнопку Назад на устройстве.
    with allure.step("Нажать системную кнопку Назад"):
        driver.back()

    # Проверяем доступность каталога после возврата.
    with allure.step("Проверить доступность каталога товаров"):
        assert ProductsPage(driver).wait_until_loaded().is_open
