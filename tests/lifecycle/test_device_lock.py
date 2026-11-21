import allure
import pytest

from pages.cart_page import CartPage
from pages.product_details_page import ProductDetailsPage
from pages.products_page import ProductsPage


@pytest.mark.regression
@allure.tag("regression")
@allure.epic("Mobile Demo App")
@allure.feature("Жизненный цикл приложения")
@allure.story("Блокировка устройства")
@allure.title("Блокировка устройства не сбрасывает товар из корзины")
def test_device_lock_preserves_product_in_cart(driver):
    # Выполняем предусловие: добавляем первый товар в корзину.
    with allure.step("Предусловие: открыть карточку товара и добавить его в корзину"):
        selected_product = ProductsPage(driver).wait_until_loaded().open_first_product()
        ProductDetailsPage(driver).add_to_cart()

    # Блокируем и разблокируем экран эмулятора.
    with allure.step("Заблокировать и разблокировать экран устройства"):
        driver.lock()
        assert driver.is_locked()
        driver.unlock()

    # Проверяем восстановление карточки товара и содержимого корзины.
    with allure.step("Проверить сохранение товара в корзине"):
        assert ProductDetailsPage(driver).title == selected_product
        cart_page = CartPage(driver).open()
        assert cart_page.is_open
        assert cart_page.contains_product(selected_product)
