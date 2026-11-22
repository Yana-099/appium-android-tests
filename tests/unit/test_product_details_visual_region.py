from pages.product_details_page import ProductDetailsPage


class FakeElement:
    def __init__(self, *, y: int, height: int):
        self.rect = {"y": y, "height": height}


class FakeDriver:
    @staticmethod
    def get_window_size():
        return {"width": 1080, "height": 2400}


def test_visual_region_excludes_right_edge_scrollbar():
    elements = {
        ProductDetailsPage.PRODUCT_IMAGE: FakeElement(y=100, height=1000),
        ProductDetailsPage.TITLE: FakeElement(y=1100, height=100),
        ProductDetailsPage.PRICE: FakeElement(y=1200, height=100),
        ProductDetailsPage.ADD_TO_CART_BUTTON: FakeElement(y=1800, height=100),
    }
    page = object.__new__(ProductDetailsPage)
    page.driver = FakeDriver()
    page.visible = elements.__getitem__

    assert page.visual_region == (0, 100, 1064, 1900)
