import allure
import pytest

from pages.products_page import ProductsPage


@pytest.mark.regression
@allure.tag("regression")
@allure.severity(allure.severity_level.MINOR)
@allure.epic("Mobile Demo App")
@allure.feature("Каталог")
@allure.story("Сортировка товаров")
@allure.title("Товары сортируются по имени по убыванию")
def test_products_can_be_sorted_by_name_descending(driver):
    # Открываем каталог товаров и применяем сортировку по имени по убыванию.
    with allure.step("Применить сортировку по имени по убыванию"):
        products_page = ProductsPage(driver).wait_until_loaded()
        products_page.sort_by_name_descending()

    # Проверяем, что названия товаров расположены в обратном алфавитном порядке.
    with allure.step("Проверить порядок названий товаров"):
        assert products_page.product_names == sorted(
            products_page.product_names, reverse=True
        )
