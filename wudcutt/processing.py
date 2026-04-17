from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
from PIL import Image, ImageOps

Image.MAX_IMAGE_PIXELS = None


@dataclass(slots=True)
class ThresholdResult:
    threshold: int
    image: Image.Image


def load_image_grayscale(path: str | Path) -> Image.Image:
    img = Image.open(path)
    img = ImageOps.exif_transpose(img)
    return ImageOps.grayscale(img)


def apply_threshold(img: Image.Image, threshold: int) -> Image.Image:
    img_array = np.array(img.convert("L"))
    img_array = np.where(img_array > threshold, 255, 0).astype(np.uint8)
    return Image.fromarray(img_array, mode="L")


def suggest_threshold(img: Image.Image) -> int:
    grayscale = np.array(img.convert("L"), dtype=np.uint8)
    hist, _ = np.histogram(grayscale, bins=256, range=(0, 256))
    total = grayscale.size
    if total == 0:
        raise ValueError("Cannot suggest threshold for empty image")

    sum_total = np.dot(np.arange(256), hist)
    sum_background = 0.0
    weight_background = 0.0
    max_variance = -1.0
    best_threshold = 127

    mean_background_at_best = 0.0
    mean_foreground_at_best = 255.0

    for threshold, count in enumerate(hist):
        weight_background += count
        if weight_background == 0:
            continue
        weight_foreground = total - weight_background
        if weight_foreground == 0:
            break
        sum_background += threshold * count
        mean_background = sum_background / weight_background
        mean_foreground = (sum_total - sum_background) / weight_foreground
        variance_between = weight_background * weight_foreground * (mean_background - mean_foreground) ** 2
        if variance_between > max_variance:
            max_variance = variance_between
            best_threshold = threshold
            mean_background_at_best = mean_background
            mean_foreground_at_best = mean_foreground

    midpoint_threshold = int(round((mean_background_at_best + mean_foreground_at_best) / 2))
    return max(0, min(255, midpoint_threshold))


def generate_threshold_series(img: Image.Image, start: int = 0, stop: int = 255, step: int = 5) -> list[ThresholdResult]:
    if step <= 0:
        raise ValueError("step must be positive")
    return [ThresholdResult(threshold=value, image=apply_threshold(img, value)) for value in range(start, stop, step)]


def create_transparent_image(img: Image.Image) -> Image.Image:
    grayscale = img.convert("L")
    rgba = Image.new("RGBA", grayscale.size)
    grayscale_array = np.array(grayscale, dtype=np.uint8)
    pixels = []
    for value in grayscale_array.flatten().tolist():
        if value >= 250:
            pixels.append((255, 255, 255, 0))
        else:
            pixels.append((0, 0, 0, 255))
    rgba.putdata(pixels)
    return rgba
