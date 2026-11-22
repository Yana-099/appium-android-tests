from pathlib import Path

import pytest
from PIL import Image

from utils.visual_comparison import compare_images


def save_image(path: Path, color: tuple[int, int, int], size: tuple[int, int] = (2, 2)):
    Image.new("RGB", size, color).save(path)


def test_identical_images_pass_without_changed_pixels(tmp_path):
    baseline = tmp_path / "baseline.png"
    actual = tmp_path / "actual.png"
    diff = tmp_path / "diff.png"
    save_image(baseline, (10, 20, 30))
    save_image(actual, (10, 20, 30))

    result = compare_images(
        baseline,
        actual,
        diff,
        channel_tolerance=0,
        max_changed_ratio=0.0,
    )

    assert result.passed is True
    assert result.changed_pixels == 0
    assert result.total_pixels == 4
    assert result.changed_ratio == 0.0
    assert diff.exists()


def test_color_difference_at_tolerance_is_ignored(tmp_path):
    baseline = tmp_path / "baseline.png"
    actual = tmp_path / "actual.png"
    diff = tmp_path / "diff.png"
    save_image(baseline, (10, 20, 30))
    save_image(actual, (15, 20, 30))

    result = compare_images(
        baseline,
        actual,
        diff,
        channel_tolerance=5,
        max_changed_ratio=0.0,
    )

    assert result.passed is True
    assert result.changed_pixels == 0


def test_changed_ratio_at_limit_passes_and_larger_ratio_fails(tmp_path):
    baseline = tmp_path / "baseline.png"
    actual = tmp_path / "actual.png"
    passing_diff = tmp_path / "passing-diff.png"
    failing_diff = tmp_path / "failing-diff.png"
    save_image(baseline, (0, 0, 0))
    save_image(actual, (0, 0, 0))
    with Image.open(actual) as image:
        image.putpixel((0, 0), (255, 255, 255))
        image.save(actual)

    passing_result = compare_images(
        baseline,
        actual,
        passing_diff,
        channel_tolerance=0,
        max_changed_ratio=0.25,
    )
    failing_result = compare_images(
        baseline,
        actual,
        failing_diff,
        channel_tolerance=0,
        max_changed_ratio=0.24,
    )

    assert passing_result.passed is True
    assert failing_result.passed is False
    assert failing_result.changed_pixels == 1
    assert failing_result.changed_ratio == 0.25


def test_different_image_sizes_raise_diagnostic_error(tmp_path):
    baseline = tmp_path / "baseline.png"
    actual = tmp_path / "actual.png"
    diff = tmp_path / "diff.png"
    save_image(baseline, (0, 0, 0), size=(2, 2))
    save_image(actual, (0, 0, 0), size=(3, 2))

    with pytest.raises(ValueError, match=r"baseline=2x2, actual=3x2"):
        compare_images(
            baseline,
            actual,
            diff,
            channel_tolerance=0,
            max_changed_ratio=0.0,
        )

    with Image.open(diff) as diagnostic:
        assert diagnostic.size == (13, 2)
        assert diagnostic.convert("RGB").getpixel((5, 0)) == (255, 0, 0)


def test_diff_marks_changed_pixels_in_red(tmp_path):
    baseline = tmp_path / "baseline.png"
    actual = tmp_path / "actual.png"
    diff = tmp_path / "diff.png"
    save_image(baseline, (0, 0, 0))
    save_image(actual, (0, 0, 0))
    with Image.open(actual) as image:
        image.putpixel((1, 0), (255, 255, 255))
        image.save(actual)

    compare_images(
        baseline,
        actual,
        diff,
        channel_tolerance=0,
        max_changed_ratio=1.0,
    )

    with Image.open(diff) as diff_image:
        assert diff_image.convert("RGB").getpixel((1, 0)) == (255, 0, 0)
