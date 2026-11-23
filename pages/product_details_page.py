import allure
from selenium.webdriver.common.by import By

from config.settings import APP_PACKAGE
from pages.base_page import BasePage


class ProductDetailsPage(BasePage):
    VISUAL_RIGHT_INSET = 16
    TITLE = (By.ID, f"{APP_PACKAGE}:id/productTV")
    PRODUCT_IMAGE = (By.ID, f"{APP_PACKAGE}:id/productIV")
    PRICE = (By.ID, f"{APP_PACKAGE}:id/priceTV")
    ADD_TO_CART_BUTTON = (By.ID, f"{APP_PACKAGE}:id/cartBt")

    @property
    def title(self) -> str:
        return self.visible(self.TITLE).text

    @property
    def has_image(self) -> bool:
        return self.visible(self.PRODUCT_IMAGE).is_displayed()

    @property
    def price(self) -> str:
        return self.visible(self.PRICE).text

    @property
    def is_add_to_cart_available(self) -> bool:
        return self.clickable(self.ADD_TO_CART_BUTTON).is_enabled()

    @property
    def visual_region(self) -> tuple[int, int, int, int]:
        elements = (
            self.visible(self.PRODUCT_IMAGE),
            self.visible(self.TITLE),
            self.visible(self.PRICE),
            self.visible(self.ADD_TO_CART_BUTTON),
        )
        top = min(int(element.rect["y"]) for element in elements)
        bottom = max(
            int(element.rect["y"] + element.rect["height"])
            for element in elements
        )
        window_width = int(self.driver.get_window_size()["width"])
        right = window_width - self.VISUAL_RIGHT_INSET
        return 0, top, right, bottom

    @allure.step("Нажать кнопку Add to cart")
    def add_to_cart(self):
        self.click(self.ADD_TO_CART_BUTTON)
