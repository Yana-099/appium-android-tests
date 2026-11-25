from appium.webdriver.common.appiumby import AppiumBy
import allure
from selenium.webdriver.common.by import By

from config.settings import APP_PACKAGE
from pages.base_page import BasePage


class CartPage(BasePage):
    HEADER_MENU = (By.ID, f"{APP_PACKAGE}:id/menuIV")
    HEADER_LOGO = (By.ID, f"{APP_PACKAGE}:id/mTvTitle")
    EMPTY_FORM = (By.ID, f"{APP_PACKAGE}:id/noItemCL")
    EMPTY_TITLE = (By.ID, f"{APP_PACKAGE}:id/noItemTitleTV")
    EMPTY_INFO = (By.ID, f"{APP_PACKAGE}:id/cartInfoLL")
    SHOPPING_BUTTON = (By.ID, f"{APP_PACKAGE}:id/shoppingBt")
    CART_BUTTON = (By.ID, f"{APP_PACKAGE}:id/cartRL")
    TITLE = (By.ID, f"{APP_PACKAGE}:id/productTV")
    PROCEED_TO_CHECKOUT_BUTTON = (By.ID, f"{APP_PACKAGE}:id/cartBt")

    @allure.step("Нажать на иконку корзины")
    def open(self):
        self.click(self.CART_BUTTON)
        return self

    def contains_product(self, product_name: str) -> bool:
        return self.is_visible((By.XPATH, f'//*[@text="{product_name}"]'))

    @property
    def has_cart_header(self) -> bool:
        return all(
            self.is_visible(locator)
            for locator in (self.HEADER_MENU, self.HEADER_LOGO, self.CART_BUTTON)
        )

    @property
    def empty_title(self) -> str:
        return self.visible(self.EMPTY_TITLE).text

    @property
    def has_empty_illustration(self) -> bool:
        form = self.visible(self.EMPTY_FORM)
        return any(
            image.is_displayed()
            for image in form.find_elements(AppiumBy.CLASS_NAME, "android.widget.ImageView")
        )

    @property
    def empty_message(self) -> str:
        info = self.visible(self.EMPTY_INFO)
        return info.find_element(AppiumBy.CLASS_NAME, "android.widget.TextView").text

    @property
    def shopping_button_text(self) -> str:
        return self.visible(self.SHOPPING_BUTTON).text

    @property
    def is_open(self) -> bool:
        return self.visible(self.TITLE).text == "My Cart"

    @property
    def is_proceed_to_checkout_available(self) -> bool:
        return self.clickable(self.PROCEED_TO_CHECKOUT_BUTTON).is_enabled()

    @allure.step("Нажать кнопку Proceed To Checkout")
    def proceed_to_checkout(self):
        self.click(self.PROCEED_TO_CHECKOUT_BUTTON)
