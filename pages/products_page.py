import allure
from selenium.webdriver.common.by import By

from config.settings import APP_PACKAGE
from pages.base_page import BasePage


class ProductsPage(BasePage):
    TITLE = (By.ID, f"{APP_PACKAGE}:id/productTV")
    PRODUCT_TITLE = (By.ID, f"{APP_PACKAGE}:id/titleTV")
    PRODUCT_IMAGE = (By.ID, f"{APP_PACKAGE}:id/productIV")
    SORT_BUTTON = (By.ID, f"{APP_PACKAGE}:id/sortIV")
    NAME_DESCENDING = (By.XPATH, "//*[contains(@text, 'Name') and contains(@text, 'Descending')]")

    def wait_until_loaded(self):
        self.visible(self.TITLE)
        return self

    @property
    def is_open(self) -> bool:
        return self.visible(self.TITLE).text == "Products"

    @allure.step("Нажать на карточку первого товара")
    def open_first_product(self) -> str:
        product_titles = self.wait.until(
            lambda driver: driver.find_elements(*self.PRODUCT_TITLE)
        )
        product_name = product_titles[0].text
        assert product_name, "The first product has no name"

        product_images = self.wait.until(
            lambda driver: driver.find_elements(*self.PRODUCT_IMAGE)
        )
        product_images[0].click()
        return product_name

    def sort_by_name_descending(self):
        self.click(self.SORT_BUTTON)
        self.click(self.NAME_DESCENDING)
        return self

    @property
    def product_names(self) -> list[str]:
        return [element.text for element in self.driver.find_elements(*self.PRODUCT_TITLE)]
