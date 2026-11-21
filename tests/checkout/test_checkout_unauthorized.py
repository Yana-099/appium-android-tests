import allure
import pytest

from pages.cart_page import CartPage
from pages.login_page import LoginPage
from pages.product_details_page import ProductDetailsPage
from pages.products_page import ProductsPage


@pytest.mark.negative
@pytest.mark.regression
@allure.tag("negative", "regression")
@allure.severity(allure.severity_level.CRITICAL)
@allure.epic("Mobile Demo App")
@allure.feature("Оформление заказа")
@allure.story("Checkout неавторизованного клиента")
@allure.title("Неавторизованный клиент переходит на форму Login")
def test_unauthorized_customer_is_redirected_to_login_from_checkout(driver):
    # Нажимаем на карточку первого товара в каталоге.
    with allure.step("Нажать на карточку первого товара"):
        ProductsPage(driver).wait_until_loaded().open_first_product()

    # Нажимаем кнопку Add to cart.
    with allure.step("Нажать кнопку Add to cart"):
        ProductDetailsPage(driver).add_to_cart()

    # Нажимаем на иконку корзины.
    with allure.step("Нажать на иконку корзины"):
        cart_page = CartPage(driver).open()

    # Нажимаем кнопку Proceed To Checkout.
    with allure.step("Нажать кнопку Proceed To Checkout"):
        cart_page.proceed_to_checkout()

    # Проверяем, что открыта форма Login.
    with allure.step("Проверить открытие формы Login"):
        assert LoginPage(driver).title == "Login"
