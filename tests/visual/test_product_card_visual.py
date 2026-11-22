from dataclasses import asdict
from io import BytesIO
import json
from pathlib import Path

import allure
import pytest
from allure_commons.types import AttachmentType
from PIL import Image

from pages.product_details_page import ProductDetailsPage
from pages.products_page import ProductsPage
from utils.visual_comparison import compare_images


BASELINE_PATH = (
    Path(__file__).parent
    / "baselines"
    / "android-emulator-5554"
    / "product_card.png"
)
ARTIFACTS_DIR = Path("artifacts") / "visual"
ACTUAL_PATH = ARTIFACTS_DIR / "product_card_actual.png"
DIFF_PATH = ARTIFACTS_DIR / "product_card_diff.png"
CHANNEL_TOLERANCE = 8
MAX_CHANGED_RATIO = 0.001


def save_region_screenshot(driver, region: tuple[int, int, int, int], path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    with Image.open(BytesIO(driver.get_screenshot_as_png())) as screenshot:
        screenshot.convert("RGB").crop(region).save(path)


@pytest.mark.visual
@allure.tag("visual")
@allure.epic("Mobile Demo App")
@allure.feature("Визуальная регрессия")
@allure.story("Карточка товара")
@allure.title("Карточка первого товара соответствует визуальному эталону")
def test_first_product_card_matches_visual_baseline(driver):
    with allure.step("Открыть карточку первого товара"):
        ProductsPage(driver).wait_until_loaded().open_first_product()
        product_details_page = ProductDetailsPage(driver)

    with allure.step("Сохранить стабильную область карточки товара"):
        save_region_screenshot(driver, product_details_page.visual_region, ACTUAL_PATH)

    if not BASELINE_PATH.exists():
        allure.attach.file(
            str(ACTUAL_PATH),
            name="Фактический результат",
            attachment_type=AttachmentType.PNG,
        )
        pytest.fail(
            "Visual baseline is missing. Review "
            f"{ACTUAL_PATH} and copy it to {BASELINE_PATH}."
        )

    with allure.step("Сравнить карточку товара с визуальным эталоном"):
        allure.attach.file(
            str(BASELINE_PATH),
            name="Визуальный эталон",
            attachment_type=AttachmentType.PNG,
        )
        allure.attach.file(
            str(ACTUAL_PATH),
            name="Фактический результат",
            attachment_type=AttachmentType.PNG,
        )
        DIFF_PATH.unlink(missing_ok=True)
        try:
            result = compare_images(
                BASELINE_PATH,
                ACTUAL_PATH,
                DIFF_PATH,
                channel_tolerance=CHANNEL_TOLERANCE,
                max_changed_ratio=MAX_CHANGED_RATIO,
            )
        except (OSError, ValueError) as error:
            if DIFF_PATH.exists():
                allure.attach.file(
                    str(DIFF_PATH),
                    name="Диагностика несовместимых изображений",
                    attachment_type=AttachmentType.PNG,
                )
            allure.attach(
                json.dumps(
                    {
                        "error_type": type(error).__name__,
                        "message": str(error),
                    },
                    indent=2,
                ),
                name="Ошибка визуального сравнения",
                attachment_type=AttachmentType.JSON,
            )
            raise
        allure.attach.file(
            str(DIFF_PATH),
            name="Визуальная разница",
            attachment_type=AttachmentType.PNG,
        )
        allure.attach(
            json.dumps(asdict(result), indent=2),
            name="Метрики визуального сравнения",
            attachment_type=AttachmentType.JSON,
        )

    assert result.passed, (
        f"Visual difference is {result.changed_ratio:.4%}; "
        f"allowed maximum is {result.max_changed_ratio:.4%} "
        f"with channel tolerance {result.channel_tolerance}."
    )
