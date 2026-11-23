import allure
from selenium.webdriver.common.by import By

from config.settings import APP_PACKAGE
from pages.base_page import BasePage


class CheckoutShippingPage(BasePage):
    TITLE = (By.ID, f"{APP_PACKAGE}:id/checkoutTitleTV")
    FULL_NAME_FIELD = (By.ID, f"{APP_PACKAGE}:id/fullNameET")
    ADDRESS_LINE_1_FIELD = (By.ID, f"{APP_PACKAGE}:id/address1ET")
    ADDRESS_LINE_2_FIELD = (By.ID, f"{APP_PACKAGE}:id/address2ET")
    CITY_FIELD = (By.ID, f"{APP_PACKAGE}:id/cityET")
    STATE_FIELD = (By.ID, f"{APP_PACKAGE}:id/stateET")
    ZIP_CODE_FIELD = (By.ID, f"{APP_PACKAGE}:id/zipET")
    COUNTRY_FIELD = (By.ID, f"{APP_PACKAGE}:id/countryET")
    FULL_NAME_LABEL = (By.ID, f"{APP_PACKAGE}:id/fullNameTV")
    ADDRESS_LINE_1_LABEL = (By.ID, f"{APP_PACKAGE}:id/address1TV")
    CITY_LABEL = (By.ID, f"{APP_PACKAGE}:id/cityTV")
    ZIP_CODE_LABEL = (By.ID, f"{APP_PACKAGE}:id/zipTV")
    COUNTRY_LABEL = (By.ID, f"{APP_PACKAGE}:id/countryTV")
    TO_PAYMENT_BUTTON = (By.ID, f"{APP_PACKAGE}:id/paymentBtn")
    FULL_NAME_ERROR = (By.ID, f"{APP_PACKAGE}:id/fullNameErrorTV")
    ADDRESS_LINE_1_ERROR = (By.ID, f"{APP_PACKAGE}:id/address1ErrorTV")
    CITY_ERROR = (By.ID, f"{APP_PACKAGE}:id/cityErrorTV")
    ZIP_CODE_ERROR = (By.ID, f"{APP_PACKAGE}:id/zipErrorTV")
    COUNTRY_ERROR = (By.ID, f"{APP_PACKAGE}:id/countryErrorTV")

    @property
    def title(self) -> str:
        return self.visible(self.TITLE).text

    @property
    def full_name_label(self) -> str:
        return self.visible(self.FULL_NAME_LABEL).text

    @property
    def address_line_1_label(self) -> str:
        return self.visible(self.ADDRESS_LINE_1_LABEL).text

    @property
    def city_label(self) -> str:
        return self.visible(self.CITY_LABEL).text

    @property
    def zip_code_label(self) -> str:
        return self.visible(self.ZIP_CODE_LABEL).text

    @property
    def country_label(self) -> str:
        return self.visible(self.COUNTRY_LABEL).text

    @property
    def is_to_payment_available(self) -> bool:
        return self.clickable(self.TO_PAYMENT_BUTTON).is_enabled()

    @allure.step("Нажать кнопку To Payment")
    def go_to_payment(self):
        self.click(self.TO_PAYMENT_BUTTON)

    def enter_full_name(self, value: str):
        self.replace_value(self.FULL_NAME_FIELD, value)

    @property
    def full_name(self) -> str:
        return self.visible(self.FULL_NAME_FIELD).text

    def enter_address_line_1(self, value: str):
        self.replace_value(self.ADDRESS_LINE_1_FIELD, value)

    @property
    def address_line_1(self) -> str:
        return self.visible(self.ADDRESS_LINE_1_FIELD).text

    def enter_address_line_2(self, value: str):
        self.replace_value(self.ADDRESS_LINE_2_FIELD, value)

    @property
    def address_line_2(self) -> str:
        return self.visible(self.ADDRESS_LINE_2_FIELD).text

    def enter_city(self, value: str):
        self.scroll_to(self.CITY_FIELD)
        self.replace_value(self.CITY_FIELD, value)

    @property
    def city(self) -> str:
        return self.visible(self.CITY_FIELD).text

    def enter_state(self, value: str):
        self.replace_value(self.STATE_FIELD, value)

    @property
    def state(self) -> str:
        return self.visible(self.STATE_FIELD).text

    def enter_zip_code(self, value: str):
        self.replace_value(self.ZIP_CODE_FIELD, value)

    @property
    def zip_code(self) -> str:
        return self.visible(self.ZIP_CODE_FIELD).text

    def enter_country(self, value: str):
        self.scroll_to(self.COUNTRY_FIELD)
        self.replace_value(self.COUNTRY_FIELD, value)

    @property
    def country(self) -> str:
        return self.visible(self.COUNTRY_FIELD).text

    @property
    def full_name_error(self) -> str:
        return self.visible(self.FULL_NAME_ERROR).text

    @property
    def address_line_1_error(self) -> str:
        return self.visible(self.ADDRESS_LINE_1_ERROR).text

    @property
    def city_error(self) -> str:
        return self.visible(self.CITY_ERROR).text

    @property
    def zip_code_error(self) -> str:
        return self.visible(self.ZIP_CODE_ERROR).text

    @property
    def country_error(self) -> str:
        return self.visible(self.COUNTRY_ERROR).text

    @property
    def has_validation_errors(self) -> bool:
        return any(
            self.is_displayed(locator)
            for locator in (
                self.FULL_NAME_ERROR,
                self.ADDRESS_LINE_1_ERROR,
                self.CITY_ERROR,
                self.ZIP_CODE_ERROR,
                self.COUNTRY_ERROR,
            )
        )
