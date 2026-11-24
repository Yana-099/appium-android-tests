from appium.webdriver.common.appiumby import AppiumBy

from pages.base_page import BasePage


class MenuPage(BasePage):
    MENU_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "View menu")
    LOGIN_ITEM = (AppiumBy.ACCESSIBILITY_ID, "Login Menu Item")
    LOGOUT_ITEM = (AppiumBy.ACCESSIBILITY_ID, "Logout Menu Item")

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
