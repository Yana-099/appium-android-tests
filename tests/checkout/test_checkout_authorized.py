import allure
import pytest

from config.test_data import (
    PAYMENT_CARDHOLDER_NAME,
    PAYMENT_CARD_NUMBER,
    PAYMENT_EXPIRATION_DATE,
    PAYMENT_SECURITY_CODE,
    SHIPPING_ADDRESS_LINE_1,
    SHIPPING_ADDRESS_LINE_2,
    SHIPPING_CITY,
    SHIPPING_COUNTRY,
    SHIPPING_FULL_NAME,
    SHIPPING_STATE,
    SHIPPING_ZIP_CODE,
)
from pages.cart_page import CartPage
from pages.checkout_complete_page import CheckoutCompletePage
from pages.checkout_payment_page import CheckoutPaymentPage
from pages.checkout_review_page import CheckoutReviewPage
from pages.checkout_shipping_page import CheckoutShippingPage
from pages.product_details_page import ProductDetailsPage
from pages.products_page import ProductsPage


@pytest.mark.regression
@allure.tag("regression")
@allure.severity(allure.severity_level.CRITICAL)
@allure.epic("Mobile Demo App")
@allure.feature("Оформление заказа")
@allure.story("Авторизованный пользователь оформляет заказ")
@allure.title("Авторизованный пользователь оформляет заказ с первым товаром")
def test_authorized_user_places_order(authorized_driver):
    # Открываем карточку первого товара каталога.
    with allure.step("Нажать на карточку первого товара"):
        selected_product = ProductsPage(authorized_driver).wait_until_loaded().open_first_product()

    # Добавляем выбранный товар в корзину.
    with allure.step("Нажать кнопку Add to cart"):
        ProductDetailsPage(authorized_driver).add_to_cart()

    # Открываем корзину с добавленным товаром.
    with allure.step("Нажать на иконку корзины"):
        CartPage(authorized_driver).open()
        assert CartPage(authorized_driver).contains_product(selected_product)

    # Открываем форму доставки.
    with allure.step("Нажать кнопку Proceed To Checkout"):
        CartPage(authorized_driver).proceed_to_checkout()
        shipping_page = CheckoutShippingPage(authorized_driver)
        assert shipping_page.title == "Checkout"

    # Заполняем все поля формы доставки перед переходом к оплате.
    with allure.step("Заполнить форму доставки"):
        shipping_page.enter_full_name(SHIPPING_FULL_NAME)
        shipping_page.enter_address_line_1(SHIPPING_ADDRESS_LINE_1)
        shipping_page.enter_address_line_2(SHIPPING_ADDRESS_LINE_2)
        shipping_page.enter_city(SHIPPING_CITY)
        shipping_page.enter_state(SHIPPING_STATE)
        shipping_page.enter_zip_code(SHIPPING_ZIP_CODE)
        shipping_page.enter_country(SHIPPING_COUNTRY)

    # Проверяем, что форма доставки заполнена тестовыми данными.
    with allure.step("Проверить заполнение формы доставки"):
        assert shipping_page.full_name == SHIPPING_FULL_NAME
        assert shipping_page.address_line_1 == SHIPPING_ADDRESS_LINE_1
        assert shipping_page.address_line_2 == SHIPPING_ADDRESS_LINE_2
        assert shipping_page.city == SHIPPING_CITY
        assert shipping_page.state == SHIPPING_STATE
        assert shipping_page.zip_code == SHIPPING_ZIP_CODE
        assert shipping_page.country == SHIPPING_COUNTRY
        assert not shipping_page.has_validation_errors

    # Открываем форму способа оплаты.
    with allure.step("Нажать кнопку To Payment"):
        shipping_page.go_to_payment()
        payment_page = CheckoutPaymentPage(authorized_driver)
        assert payment_page.title == "Checkout"

    # Заполняем все поля формы оплаты перед проверкой заказа.
    with allure.step("Заполнить форму оплаты"):
        payment_page.enter_cardholder_name(PAYMENT_CARDHOLDER_NAME)
        payment_page.enter_card_number(PAYMENT_CARD_NUMBER)
        payment_page.enter_expiration_date(PAYMENT_EXPIRATION_DATE)
        payment_page.enter_security_code(PAYMENT_SECURITY_CODE)

    # Проверяем, что форма оплаты заполнена тестовыми данными.
    with allure.step("Проверить заполнение формы оплаты"):
        assert payment_page.cardholder_name == PAYMENT_CARDHOLDER_NAME
        assert payment_page.card_number == PAYMENT_CARD_NUMBER
        assert payment_page.expiration_date == PAYMENT_EXPIRATION_DATE
        assert payment_page.security_code == PAYMENT_SECURITY_CODE

    # Открываем страницу проверки заказа.
    with allure.step("Нажать кнопку Review Order"):
        payment_page.review_order()
        review_page = CheckoutReviewPage(authorized_driver)
        assert review_page.title == "Review your order"

    # Проверяем выбранный товар и доступность оформления заказа.
    with allure.step("Проверить товар на странице Review your order"):
        assert review_page.contains_product(selected_product)
        assert review_page.is_place_order_available

    # Подтверждаем оформление заказа.
    with allure.step("Нажать кнопку Place Order"):
        review_page.place_order()
        complete_page = CheckoutCompletePage(authorized_driver)

    # Проверяем сообщение об успешном оформлении заказа.
    with allure.step("Проверить сообщение об успешном оформлении заказа"):
        assert complete_page.title == "Checkout Complete"
        assert complete_page.order_confirmation == "Thank you for your order"
        assert complete_page.is_continue_shopping_available
