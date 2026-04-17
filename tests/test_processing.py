from pathlib import Path

import numpy as np
from PIL import Image

from wudcutt.processing import (
    apply_threshold,
    create_transparent_image,
    generate_threshold_series,
    load_image_grayscale,
    suggest_threshold,
)


def test_apply_threshold_returns_binary_image():
    img = Image.fromarray(np.array([[0, 120], [200, 255]], dtype=np.uint8), mode="L")

    result = apply_threshold(img, 150)

    assert result.mode == "L"
    assert list(np.array(result).flatten()) == [0, 0, 255, 255]


def test_generate_threshold_series_creates_expected_thresholds():
    img = Image.fromarray(np.array([[10, 20], [30, 40]], dtype=np.uint8), mode="L")

    series = generate_threshold_series(img, start=0, stop=10, step=5)

    assert [item.threshold for item in series] == [0, 5]
    assert all(item.image.mode == "L" for item in series)


def test_create_transparent_image_makes_white_pixels_transparent():
    img = Image.fromarray(np.array([[0, 255], [255, 0]], dtype=np.uint8), mode="L")

    result = create_transparent_image(img)

    assert result.mode == "RGBA"
    pixels = [tuple(pixel) for pixel in np.array(result).reshape(-1, 4)]
    assert pixels[0] == (0, 0, 0, 255)
    assert pixels[1] == (255, 255, 255, 0)


def test_load_image_grayscale_respects_file_path(tmp_path):
    path = tmp_path / "source.png"
    Image.new("RGB", (4, 4), color=(255, 0, 0)).save(path)

    loaded = load_image_grayscale(path)

    assert loaded.mode == "L"
    assert loaded.size == (4, 4)


def test_suggest_threshold_finds_midpoint_for_bimodal_image():
    img = Image.fromarray(
        np.array(
            [
                [20, 20, 20, 20],
                [20, 20, 20, 20],
                [220, 220, 220, 220],
                [220, 220, 220, 220],
            ],
            dtype=np.uint8,
        ),
        mode="L",
    )

    threshold = suggest_threshold(img)

    assert 60 <= threshold <= 180
