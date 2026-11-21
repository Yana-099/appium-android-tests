from selenium.webdriver.common.by import By

from config.settings import APP_PACKAGE
from pages.base_page import BasePage


class ProductDetailsPage(BasePage):
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

    def add_to_cart(self):
        self.click(self.ADD_TO_CART_BUTTON)
