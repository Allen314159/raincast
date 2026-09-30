import base64
import io

import numpy as np
from PIL import Image

from app.render import frame_to_png_base64


def test_frame_to_png_base64_decodes_to_360_by_360_png() -> None:
    frame = np.zeros((360, 360), dtype=np.float32)
    frame[120:240, 120:240] = 0.7

    encoded = frame_to_png_base64(frame)
    image = Image.open(io.BytesIO(base64.b64decode(encoded)))

    assert image.format == "PNG"
    assert image.size == (360, 360)
