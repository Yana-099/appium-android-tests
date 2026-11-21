from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class CheckoutCompletePage(BasePage):
    TITLE = (By.XPATH, "//*[@text='Checkout Complete']")
    ORDER_CONFIRMATION = (By.XPATH, "//*[@text='Thank you for your order']")
    CONTINUE_SHOPPING_BUTTON = (By.XPATH, "//*[@text='Continue Shopping']")

    @property
    def title(self) -> str:
        return self.visible(self.TITLE).text

    @property
    def order_confirmation(self) -> str:
        return self.visible(self.ORDER_CONFIRMATION).text

    @property
    def is_continue_shopping_available(self) -> bool:
        return self.clickable(self.CONTINUE_SHOPPING_BUTTON).is_enabled()
