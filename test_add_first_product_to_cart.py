import unittest

from appium import webdriver
from appium.options.android import UiAutomator2Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


APPIUM_SERVER_URL = "http://127.0.0.1:4723"
APP_PACKAGE = "com.saucelabs.mydemoapp.android"
APP_ACTIVITY = ".view.activities.SplashActivity"
WAIT_SECONDS = 15


class TestShoppingCart(unittest.TestCase):
    def setUp(self):
        options = UiAutomator2Options().load_capabilities(
            {
                "platformName": "Android",
                "appium:automationName": "UiAutomator2",
                "appium:udid": "emulator-5554",
                "appium:appPackage": APP_PACKAGE,
                "appium:appActivity": APP_ACTIVITY,
                # Clean application data so an old cart cannot make the test pass.
                "appium:noReset": False,
            }
        )

        self.driver = webdriver.Remote(APPIUM_SERVER_URL, options=options)
        self.wait = WebDriverWait(self.driver, WAIT_SECONDS)

    def tearDown(self):
        if hasattr(self, "driver"):
            self.driver.quit()

    def test_add_first_product_to_cart(self):
        product_titles = self.wait.until(
            EC.presence_of_all_elements_located(
                (By.ID, f"{APP_PACKAGE}:id/titleTV")
            )
        )
        first_product_name = product_titles[0].text
        self.assertTrue(first_product_name, "The first product has no name")

        first_product_images = self.wait.until(
            EC.presence_of_all_elements_located(
                (By.ID, f"{APP_PACKAGE}:id/productIV")
            )
        )
        first_product_images[0].click()

        add_to_cart_button = self.wait.until(
            EC.element_to_be_clickable((By.ID, f"{APP_PACKAGE}:id/cartBt"))
        )
        add_to_cart_button.click()

        cart_button = self.wait.until(
            EC.element_to_be_clickable((By.ID, f"{APP_PACKAGE}:id/cartRL"))
        )
        cart_button.click()

        product_in_cart = self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, f'//*[@text="{first_product_name}"]')
            )
        )
        self.assertTrue(
            product_in_cart.is_displayed(),
            f'Product "{first_product_name}" is not displayed in the cart',
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
