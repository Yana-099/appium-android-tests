import allure
import pytest
from qase.pytest import qase

from pages.cart_page import CartPage
from pages.products_page import ProductsPage


@qase.id(3)
@pytest.mark.ai_generated
@pytest.mark.regression
@allure.feature("Корзина")
@allure.story("Пустая корзина")
@allure.title("AMT-3: форма пустой корзины")
def test_empty_cart_form(driver):
    with allure.step("Открыть приложение с пустой корзиной"):
        assert ProductsPage(driver).wait_until_loaded().is_open

    cart_page = CartPage(driver).open()

    with allure.step("Проверить верхнюю панель"):
        assert cart_page.has_cart_header

    with allure.step("Проверить форму пустой корзины"):
        assert cart_page.empty_title == "No Items"
        assert cart_page.has_empty_illustration
        assert cart_page.empty_message == (
            "Oh no! Your cart is empty. Fill it up with swag to complete your purchase."
        )
        assert cart_page.shopping_button_text == "Go Shopping"
