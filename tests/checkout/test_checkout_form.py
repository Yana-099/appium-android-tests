import allure
import pytest

from pages.cart_page import CartPage
from pages.checkout_shipping_page import CheckoutShippingPage
from pages.product_details_page import ProductDetailsPage
from pages.products_page import ProductsPage


@pytest.mark.regression
@allure.tag("regression")
@allure.epic("Mobile Demo App")
@allure.feature("Оформление заказа")
@allure.story("Форма доставки")
@allure.title("Авторизованный пользователь видит обязательные поля доставки")
def test_checkout_shipping_form_displays_required_controls(authorized_driver):
    # Нажимаем на карточку первого товара в каталоге.
    with allure.step("Нажать на карточку первого товара"):
        ProductsPage(authorized_driver).wait_until_loaded().open_first_product()

    # Нажимаем кнопку Add to cart.
    with allure.step("Нажать кнопку Add to cart"):
        ProductDetailsPage(authorized_driver).add_to_cart()

    # Нажимаем на иконку корзины.
    with allure.step("Нажать на иконку корзины"):
        CartPage(authorized_driver).open()

    # Нажимаем кнопку Proceed To Checkout.
    with allure.step("Нажать кнопку Proceed To Checkout"):
        CartPage(authorized_driver).proceed_to_checkout()
        checkout_page = CheckoutShippingPage(authorized_driver)

    # Проверяем заголовок и обязательные поля формы доставки.
    with allure.step("Проверить обязательные поля формы доставки"):
        assert checkout_page.title == "Checkout"
        assert checkout_page.full_name_label == "Full Name*"
        assert checkout_page.address_line_1_label == "Address Line 1*"
        assert checkout_page.city_label == "City*"
        assert checkout_page.zip_code_label == "Zip Code*"
        assert checkout_page.country_label == "Country*"
        assert checkout_page.is_to_payment_available
