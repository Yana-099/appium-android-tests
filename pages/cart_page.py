from selenium.webdriver.common.by import By

from config.settings import APP_PACKAGE
from pages.base_page import BasePage


class CartPage(BasePage):
    CART_BUTTON = (By.ID, f"{APP_PACKAGE}:id/cartRL")
    TITLE = (By.ID, f"{APP_PACKAGE}:id/productTV")
    PROCEED_TO_CHECKOUT_BUTTON = (By.ID, f"{APP_PACKAGE}:id/cartBt")

    def open(self):
        self.click(self.CART_BUTTON)
        return self

    def contains_product(self, product_name: str) -> bool:
        return self.is_visible((By.XPATH, f'//*[@text="{product_name}"]'))

    @property
    def is_open(self) -> bool:
        return self.visible(self.TITLE).text == "My Cart"

    @property
    def is_proceed_to_checkout_available(self) -> bool:
        return self.clickable(self.PROCEED_TO_CHECKOUT_BUTTON).is_enabled()

    def proceed_to_checkout(self):
        self.click(self.PROCEED_TO_CHECKOUT_BUTTON)
