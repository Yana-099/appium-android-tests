import allure
import pytest
from selenium.webdriver.common.by import By

from config.test_data import SYSTEM_NOTIFICATION_TEXT, SYSTEM_NOTIFICATION_TITLE
from pages.product_details_page import ProductDetailsPage
from pages.products_page import ProductsPage
from pages.base_page import BasePage
from utils.android_device import (
    AndroidDeviceCommandError,
    collapse_notification_shade,
    post_test_notification,
)


@pytest.mark.regression
@allure.tag("regression")
@allure.epic("Mobile Demo App")
@allure.feature("Жизненный цикл приложения")
@allure.story("Системное уведомление")
@allure.title("Тестовое уведомление не приводит к крашу приложения")
def test_push_notification_does_not_crash_product_card(driver, device_profile):
    # Выполняем предусловие: закрываем шторку уведомлений.
    with allure.step("Предусловие: закрыть шторку уведомлений"):
        collapse_notification_shade(device_profile.udid)

    # Выполняем предусловие: открываем карточку первого товара.
    with allure.step("Предусловие: открыть карточку первого товара"):
        selected_product = ProductsPage(driver).wait_until_loaded().open_first_product()
        product_page = ProductDetailsPage(driver)
        assert product_page.title == selected_product

    # Отправляем тестовое системное уведомление на эмулятор.
    with allure.step("Отправить тестовое системное уведомление"):
        post_test_notification(
            device_profile.udid,
            SYSTEM_NOTIFICATION_TITLE,
            SYSTEM_NOTIFICATION_TEXT,
        )

    try:
        # Открываем шторку и проверяем полученное уведомление.
        with allure.step("Открыть шторку уведомлений и проверить уведомление"):
            driver.open_notifications()
            notification_shade = BasePage(driver)
            assert notification_shade.visible(
                (By.XPATH, f'//*[@text="{SYSTEM_NOTIFICATION_TITLE}"]')
            ).is_displayed()
            assert notification_shade.visible(
                (By.XPATH, f'//*[@text="{SYSTEM_NOTIFICATION_TEXT}"]')
            ).is_displayed()
    finally:
        # Закрываем шторку, не скрывая результат основной проверки при сбое ADB.
        with allure.step("Закрыть шторку уведомлений после проверки"):
            try:
                collapse_notification_shade(device_profile.udid)
            except AndroidDeviceCommandError as error:
                allure.attach(
                    str(error),
                    name="Не удалось закрыть шторку уведомлений",
                    attachment_type=allure.attachment_type.TEXT,
                )

    # Проверяем состояние приложения после закрытия шторки.
    with allure.step("Проверить карточку товара после закрытия шторки"):
        assert product_page.title == selected_product
        assert product_page.is_add_to_cart_available
