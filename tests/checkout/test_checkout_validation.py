import allure
import pytest

from pages.cart_page import CartPage
from pages.checkout_shipping_page import CheckoutShippingPage
from pages.product_details_page import ProductDetailsPage
from pages.products_page import ProductsPage


@pytest.mark.negative
@pytest.mark.regression
@allure.tag("negative", "regression")
@allure.epic("Mobile Demo App")
@allure.feature("Оформление заказа")
@allure.story("Валидация формы доставки")
@allure.title("Обязательные поля доставки показывают точные сообщения об ошибках")
def test_checkout_shipping_required_fields_show_validation_messages(authorized_driver):
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

    # Нажимаем кнопку To Payment с незаполненными обязательными полями.
    with allure.step("Нажать кнопку To Payment"):
        checkout_page.go_to_payment()

    # Проверяем точные сообщения под обязательными полями.
    with allure.step("Проверить сообщения валидации обязательных полей"):
        assert checkout_page.full_name_error == "Please provide your full name."
        assert checkout_page.address_line_1_error == "Please provide your address."
        assert checkout_page.city_error == "Please provide your city."
        assert checkout_page.zip_code_error == "Please provide your zip"
        assert checkout_page.country_error == "Please provide your"
