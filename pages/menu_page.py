from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class MenuPage(BasePage):
    MENU_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "View menu")
    LOGIN_ITEM = (AppiumBy.ACCESSIBILITY_ID, "Login Menu Item")
    LOGOUT_ITEM = (AppiumBy.ACCESSIBILITY_ID, "Logout Menu Item")
    LOGOUT_DIALOG_TITLE = (
        By.ID,
        "com.saucelabs.mydemoapp.android:id/alertTitle",
    )
    LOGOUT_DIALOG_MESSAGE = (By.ID, "android:id/message")
    CANCEL_LOGOUT_BUTTON = (By.ID, "android:id/button2")
    CONFIRM_LOGOUT_BUTTON = (By.ID, "android:id/button1")

    def open(self):
        self.click(self.MENU_BUTTON)
        self.wait.until(
            lambda driver: driver.find_elements(*self.LOGIN_ITEM)
            or driver.find_elements(*self.LOGOUT_ITEM)
        )
        return self

    @property
    def is_open(self) -> bool:
        return self.is_visible(self.LOGIN_ITEM)

    @property
    def has_logout_item(self) -> bool:
        return self.is_visible(self.LOGOUT_ITEM)

    def open_login(self):
        self.click(self.LOGIN_ITEM)

    def open_logout_dialog(self):
        self.click(self.LOGOUT_ITEM)
        self.visible(self.LOGOUT_DIALOG_TITLE)
        return self

    @property
    def logout_dialog_title(self) -> str:
        return self.visible(self.LOGOUT_DIALOG_TITLE).text

    @property
    def logout_dialog_message(self) -> str:
        return self.visible(self.LOGOUT_DIALOG_MESSAGE).text

    @property
    def cancel_logout_button_text(self) -> str:
        return self.clickable(self.CANCEL_LOGOUT_BUTTON).text

    @property
    def confirm_logout_button_text(self) -> str:
        return self.clickable(self.CONFIRM_LOGOUT_BUTTON).text

    def confirm_logout(self):
        self.click(self.CONFIRM_LOGOUT_BUTTON)
