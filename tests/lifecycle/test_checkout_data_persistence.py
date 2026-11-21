import allure
import pytest

from config.settings import APP_PACKAGE
from config.test_data import (
    SHIPPING_ADDRESS_LINE_1,
    SHIPPING_CITY,
    SHIPPING_COUNTRY,
    SHIPPING_FULL_NAME,
)
from pages.cart_page import CartPage
from pages.checkout_shipping_page import CheckoutShippingPage
from pages.product_details_page import ProductDetailsPage
from pages.products_page import ProductsPage


@pytest.mark.regression
@allure.tag("regression")
@allure.epic("Mobile Demo App")
@allure.feature("Жизненный цикл приложения")
@allure.story("Восстановление формы Checkout")
@allure.title("Данные доставки сохраняются после сворачивания приложения")
def test_checkout_shipping_data_keeps_value_after_backgrounding(authorized_driver):
    # Выполняем предусловие: открываем форму доставки для первого товара.
    with allure.step("Предусловие: открыть форму доставки с первым товаром"):
        ProductsPage(authorized_driver).wait_until_loaded().open_first_product()
        ProductDetailsPage(authorized_driver).add_to_cart()
        CartPage(authorized_driver).open().proceed_to_checkout()
        shipping_page = CheckoutShippingPage(authorized_driver)
        assert shipping_page.title == "Checkout"

    # Заполняем несколько обязательных полей формы доставки.
    with allure.step("Заполнить поля Full Name, Address Line 1, City и Country"):
        shipping_page.enter_full_name(SHIPPING_FULL_NAME)
        shipping_page.enter_address_line_1(SHIPPING_ADDRESS_LINE_1)
        shipping_page.enter_city(SHIPPING_CITY)
        shipping_page.enter_country(SHIPPING_COUNTRY)

    # Сворачиваем приложение и возвращаем его на передний план.
    with allure.step("Свернуть и восстановить приложение"):
        authorized_driver.background_app(2)
        authorized_driver.activate_app(APP_PACKAGE)

    # Проверяем сохранение введённых данных на форме доставки.
    with allure.step("Проверить сохранение данных формы доставки"):
        assert shipping_page.full_name == SHIPPING_FULL_NAME
        assert shipping_page.address_line_1 == SHIPPING_ADDRESS_LINE_1
        assert shipping_page.city == SHIPPING_CITY
        assert shipping_page.country == SHIPPING_COUNTRY
