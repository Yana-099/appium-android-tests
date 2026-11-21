from selenium.webdriver.common.by import By

from config.settings import APP_PACKAGE
from pages.base_page import BasePage
from pages.menu_page import MenuPage

LOGIN_HELP_TEXT = (
    "Select a username and password from the list below, or click on the "
    "username to automatically populate the username and password."
)


class LoginPage(BasePage):
    TITLE = (By.ID, f"{APP_PACKAGE}:id/loginTV")
    HELP_TEXT = (By.ID, f"{APP_PACKAGE}:id/selectTextTV")
    USERNAME_LABEL = (By.ID, f"{APP_PACKAGE}:id/usernameTV")
    PASSWORD_LABEL = (By.ID, f"{APP_PACKAGE}:id/passwordTV")
    USERNAME_FIELD = (By.ID, f"{APP_PACKAGE}:id/nameET")
    PASSWORD_FIELD = (By.ID, f"{APP_PACKAGE}:id/passwordET")
    LOGIN_BUTTON = (By.ID, f"{APP_PACKAGE}:id/loginBtn")
    ERROR_MESSAGE = (By.ID, f"{APP_PACKAGE}:id/errorTV")

    def open(self):
        MenuPage(self.driver).open().open_login()
        self.visible(self.TITLE)
        return self

    @property
    def title(self) -> str:
        return self.visible(self.TITLE).text

    @property
    def is_open(self) -> bool:
        return self.is_displayed(self.TITLE)

    @property
    def help_text(self) -> str:
        return self.visible(self.HELP_TEXT).text

    @property
    def username_label(self) -> str:
        return self.visible(self.USERNAME_LABEL).text

    @property
    def password_label(self) -> str:
        return self.visible(self.PASSWORD_LABEL).text

    @property
    def login_button_text(self) -> str:
        return self.clickable(self.LOGIN_BUTTON).text

    @property
    def is_username_field_enabled(self) -> bool:
        return self.visible(self.USERNAME_FIELD).is_enabled()

    @property
    def is_password_field_enabled(self) -> bool:
        return self.visible(self.PASSWORD_FIELD).is_enabled()

    @property
    def is_login_button_enabled(self) -> bool:
        return self.clickable(self.LOGIN_BUTTON).is_enabled()

    def enter_credentials(self, username: str, password: str):
        self.enter_username(username)
        self.enter_password(password)
        return self

    def enter_username(self, username: str):
        self.fill(self.USERNAME_FIELD, username)
        return self

    def enter_password(self, password: str):
        self.fill(self.PASSWORD_FIELD, password)
        return self

    def submit_login(self):
        self.click(self.LOGIN_BUTTON)

    def login(self, username: str, password: str):
        self.enter_credentials(username, password)
        self.submit_login()

    @property
    def entered_username(self) -> str:
        return self.visible(self.USERNAME_FIELD).get_attribute("text")

    @property
    def entered_password(self) -> str:
        return self.visible(self.PASSWORD_FIELD).get_attribute("text")

    @property
    def error_message(self) -> str:
        error_elements = self.driver.find_elements(*self.ERROR_MESSAGE)
        return error_elements[0].text if error_elements else ""
