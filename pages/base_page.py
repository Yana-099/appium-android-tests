from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

from config.settings import WAIT_SECONDS


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(
            driver,
            WAIT_SECONDS,
            ignored_exceptions=(StaleElementReferenceException,),
        )

    def visible(self, locator):
        return self.wait.until(expected_conditions.visibility_of_element_located(locator))

    def clickable(self, locator):
        return self.wait.until(expected_conditions.element_to_be_clickable(locator))

    def click(self, locator):
        self.clickable(locator).click()

    def fill(self, locator, value: str):
        field = self.visible(locator)
        field.clear()
        field.send_keys(value)

    def replace_value(self, locator, value: str):
        field = self.visible(locator)
        self.driver.execute_script(
            "mobile: replaceElementValue",
            {"elementId": field.id, "text": value},
        )

    def scroll_down(self):
        window_size = self.driver.get_window_size()
        self.driver.execute_script(
            "mobile: scrollGesture",
            {
                "left": 0,
                "top": int(window_size["height"] * 0.25),
                "width": window_size["width"],
                "height": int(window_size["height"] * 0.6),
                "direction": "down",
                "percent": 0.8,
            },
        )

    def scroll_to(self, locator, max_attempts: int = 4):
        for _ in range(max_attempts):
            if self.is_displayed(locator):
                return
            self.scroll_down()
        self.visible(locator)

    def hide_keyboard(self):
        try:
            if self.driver.is_keyboard_shown():
                self.driver.hide_keyboard()
        except Exception:
            pass

    def is_visible(self, locator) -> bool:
        try:
            return self.visible(locator).is_displayed()
        except Exception:
            return False

    def is_displayed(self, locator) -> bool:
        try:
            return any(element.is_displayed() for element in self.driver.find_elements(*locator))
        except Exception:
            return False

    @staticmethod
    def accessibility_id(value: str):
        return AppiumBy.ACCESSIBILITY_ID, value
