from selenium.webdriver.common.by import By

from config.settings import APP_PACKAGE
from pages.base_page import BasePage


class CheckoutPaymentPage(BasePage):
    TITLE = (By.ID, f"{APP_PACKAGE}:id/enterPaymentTitleTV")
    CARDHOLDER_NAME_FIELD = (By.ID, f"{APP_PACKAGE}:id/nameET")
    CARD_NUMBER_FIELD = (By.ID, f"{APP_PACKAGE}:id/cardNumberET")
    EXPIRATION_DATE_FIELD = (By.ID, f"{APP_PACKAGE}:id/expirationDateET")
    SECURITY_CODE_FIELD = (By.ID, f"{APP_PACKAGE}:id/securityCodeET")
    REVIEW_ORDER_BUTTON = (By.ID, f"{APP_PACKAGE}:id/paymentBtn")

    @property
    def title(self) -> str:
        return self.visible(self.TITLE).text

    def enter_cardholder_name(self, value: str):
        self.replace_value(self.CARDHOLDER_NAME_FIELD, value)

    @property
    def cardholder_name(self) -> str:
        return self.visible(self.CARDHOLDER_NAME_FIELD).text

    def enter_card_number(self, value: str):
        self.replace_value(self.CARD_NUMBER_FIELD, value)

    @property
    def card_number(self) -> str:
        return self.visible(self.CARD_NUMBER_FIELD).text

    def enter_expiration_date(self, value: str):
        self.scroll_to(self.EXPIRATION_DATE_FIELD)
        self.replace_value(self.EXPIRATION_DATE_FIELD, value)

    @property
    def expiration_date(self) -> str:
        return self.visible(self.EXPIRATION_DATE_FIELD).text

    def enter_security_code(self, value: str):
        self.replace_value(self.SECURITY_CODE_FIELD, value)

    @property
    def security_code(self) -> str:
        return self.visible(self.SECURITY_CODE_FIELD).text

    def review_order(self):
        self.hide_keyboard()
        self.click(self.REVIEW_ORDER_BUTTON)
