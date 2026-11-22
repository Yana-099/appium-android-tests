from dataclasses import dataclass
from functools import reduce
from pathlib import Path

from PIL import Image, ImageChops

SIDE_BY_SIDE_GAP = 8


@dataclass(frozen=True)
class VisualComparisonResult:
    changed_pixels: int
    total_pixels: int
    changed_ratio: float
    channel_tolerance: int
    max_changed_ratio: float
    passed: bool


def compare_images(
    baseline_path: Path,
    actual_path: Path,
    diff_path: Path,
    *,
    channel_tolerance: int,
    max_changed_ratio: float,
) -> VisualComparisonResult:
    with Image.open(baseline_path) as baseline_source:
        baseline = baseline_source.convert("RGB")
    with Image.open(actual_path) as actual_source:
        actual = actual_source.convert("RGB")

    if baseline.size != actual.size:
        baseline_width, baseline_height = baseline.size
        actual_width, actual_height = actual.size
        diagnostic = Image.new(
            "RGB",
            (
                baseline_width + SIDE_BY_SIDE_GAP + actual_width,
                max(baseline_height, actual_height),
            ),
            (255, 0, 0),
        )
        diagnostic.paste(baseline, (0, 0))
        diagnostic.paste(actual, (baseline_width + SIDE_BY_SIDE_GAP, 0))
        diff_path.parent.mkdir(parents=True, exist_ok=True)
        diagnostic.save(diff_path)
        raise ValueError(
            "Image sizes differ: "
            f"baseline={baseline_width}x{baseline_height}, "
            f"actual={actual_width}x{actual_height}"
        )

    raw_diff = ImageChops.difference(baseline, actual)
    largest_channel_diff = reduce(ImageChops.lighter, raw_diff.split())
    changed_mask = largest_channel_diff.point(
        lambda value: 255 if value > channel_tolerance else 0
    )

    changed_pixels = changed_mask.histogram()[255]
    total_pixels = baseline.width * baseline.height
    changed_ratio = changed_pixels / total_pixels

    grayscale_actual = actual.convert("L").convert("RGB")
    red_highlight = Image.new("RGB", actual.size, (255, 0, 0))
    visual_diff = Image.composite(red_highlight, grayscale_actual, changed_mask)
    diff_path.parent.mkdir(parents=True, exist_ok=True)
    visual_diff.save(diff_path)

    return VisualComparisonResult(
        changed_pixels=changed_pixels,
        total_pixels=total_pixels,
        changed_ratio=changed_ratio,
        channel_tolerance=channel_tolerance,
        max_changed_ratio=max_changed_ratio,
        passed=changed_ratio <= max_changed_ratio,
    )
