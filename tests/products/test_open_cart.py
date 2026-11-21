import allure
import pytest

from pages.cart_page import CartPage
from pages.product_details_page import ProductDetailsPage
from pages.products_page import ProductsPage


@pytest.mark.regression
@allure.tag("regression")
@allure.epic("Mobile Demo App")
@allure.feature("Корзина")
@allure.story("Переход в корзину")
@allure.title("Пользователь открывает корзину с добавленным товаром")
def test_user_can_open_cart_with_added_product(driver):
    # Нажимаем на карточку первого товара в каталоге.
    with allure.step("Нажать на карточку первого товара"):
        product_name = ProductsPage(driver).wait_until_loaded().open_first_product()

    # Нажимаем кнопку Add to cart.
    with allure.step("Нажать кнопку Add to cart"):
        ProductDetailsPage(driver).add_to_cart()

    # Нажимаем на иконку корзины.
    with allure.step("Нажать на иконку корзины"):
        cart_page = CartPage(driver).open()

    # Проверяем страницу корзины и добавленный товар.
    with allure.step("Проверить товар в корзине"):
        assert cart_page.is_open
        assert cart_page.contains_product(product_name)

    # Проверяем доступность кнопки Proceed To Checkout.
    with allure.step("Проверить кнопку Proceed To Checkout"):
        assert cart_page.is_proceed_to_checkout_available
