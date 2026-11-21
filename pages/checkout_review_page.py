from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class CheckoutReviewPage(BasePage):
    TITLE = (By.XPATH, "//*[@text='Review your order']")
    PLACE_ORDER_BUTTON = (By.XPATH, "//*[@text='Place Order']")

    @property
    def title(self) -> str:
        return self.visible(self.TITLE).text

    def contains_product(self, product_name: str) -> bool:
        return self.is_visible((By.XPATH, f'//*[@text="{product_name}"]'))

    @property
    def is_place_order_available(self) -> bool:
        return self.clickable(self.PLACE_ORDER_BUTTON).is_enabled()

    def place_order(self):
        self.click(self.PLACE_ORDER_BUTTON)
