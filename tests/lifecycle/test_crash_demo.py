import allure
import pytest

from config.settings import APP_PACKAGE
from pages.product_details_page import ProductDetailsPage
from pages.products_page import ProductsPage
from utils.android_device import crash_application


@pytest.mark.crash_demo
@pytest.mark.negative
@allure.tag("negative", "crash_demo")
@allure.epic("Mobile Demo App")
@allure.feature("Жизненный цикл приложения")
@allure.story("Аварийное завершение")
@allure.title("Демонстрация Android logcat после аварийного завершения приложения")
def test_crash_demo_attaches_android_logcat(driver):
    # Выполняем предусловие: открываем карточку первого товара.
    with allure.step("Предусловие: открыть карточку первого товара"):
        selected_product = ProductsPage(driver).wait_until_loaded().open_first_product()
        product_page = ProductDetailsPage(driver)
        assert product_page.title == selected_product

    # Имитируем аварийное завершение процесса приложения через ADB.
    with allure.step("Принудительно аварийно завершить приложение через ADB"):
        crash_application(APP_PACKAGE)

    # Завершаем demo-кейс понятной ошибкой для формирования вложений Allure.
    with allure.step("Зафиксировать аварийное завершение в отчёте"):
        pytest.fail(
            "Демонстрация: приложение было принудительно аварийно завершено. "
            "Откройте вложение «Android logcat: причина аварийного завершения»."
        )
