import base64
import io

import numpy as np
import pytest
from PIL import Image

from app.preprocess import normalised_pixel_threshold, normalised_to_dbz
from app.render import frame_to_png_base64


def test_frame_to_png_base64_decodes_to_512_by_512_png() -> None:
    frame = np.zeros((512, 512), dtype=np.float32)
    frame[160:352, 160:352] = 0.7

    encoded = frame_to_png_base64(frame)
    image = Image.open(io.BytesIO(base64.b64decode(encoded)))

    assert image.format == "PNG"
    assert image.size == (512, 512)


def test_heavy_rain_threshold_uses_yellow_colour_bin() -> None:
    threshold = normalised_pixel_threshold(10.0)
    frame = np.array([[threshold]], dtype=np.float32)

    image = Image.open(io.BytesIO(base64.b64decode(frame_to_png_base64(frame))))

    # The documented heavy-rain bin starts at the Singapore 10 mm/h threshold.
    assert image.getpixel((0, 0)) == (254, 234, 0, 255)
    assert normalised_to_dbz(np.asarray(threshold)) == pytest.approx(
        34.0063696, abs=1e-6
    )
