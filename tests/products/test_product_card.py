import allure
import pytest

from pages.product_details_page import ProductDetailsPage
from pages.products_page import ProductsPage


@pytest.mark.smoke
@pytest.mark.regression
@allure.tag("smoke", "regression")
@allure.epic("Mobile Demo App")
@allure.feature("Товары")
@allure.story("Карточка товара")
@allure.title("Карточка первого товара содержит основные элементы")
def test_first_product_card_displays_required_information(driver):
    # Нажимаем на карточку первого товара в каталоге.
    selected_product_name = ProductsPage(driver).wait_until_loaded().open_first_product()
    product_details_page = ProductDetailsPage(driver)

    # Проверяем название выбранного товара.
    with allure.step("Проверить название выбранного товара"):
        assert product_details_page.title == selected_product_name

    # Проверяем отображение изображения товара.
    with allure.step("Проверить изображение товара"):
        assert product_details_page.has_image

    # Проверяем отображение цены товара.
    with allure.step("Проверить цену товара"):
        assert product_details_page.price

    # Проверяем доступность кнопки добавления товара в корзину.
    with allure.step("Проверить кнопку Add To Cart"):
        assert product_details_page.is_add_to_cart_available
