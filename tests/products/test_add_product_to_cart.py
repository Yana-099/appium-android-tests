import allure
import pytest

from pages.cart_page import CartPage
from pages.product_details_page import ProductDetailsPage
from pages.products_page import ProductsPage


@pytest.mark.regression
@allure.tag("regression")
@allure.severity(allure.severity_level.CRITICAL)
@allure.epic("Mobile Demo App")
@allure.feature("Корзина")
@allure.story("Добавление товара")
@allure.title("Добавление первого товара в корзину")
def test_add_first_product_to_cart(driver):
    # Открываем каталог и запоминаем название первого товара.
    with allure.step("Открыть первый товар в каталоге"):
        products_page = ProductsPage(driver).wait_until_loaded()
        product_name = products_page.open_first_product()

    # Добавляем выбранный товар в корзину и открываем её.
    with allure.step("Добавить товар в корзину"):
        ProductDetailsPage(driver).add_to_cart()
    with allure.step("Открыть корзину"):
        CartPage(driver).open()

    # Проверяем, что выбранный товар отображается в корзине.
    with allure.step("Проверить наличие выбранного товара в корзине"):
        assert CartPage(driver).contains_product(product_name)
