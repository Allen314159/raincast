import base64
import io

import numpy as np
from PIL import Image

from app.render import frame_to_png_base64


def test_frame_to_png_base64_decodes_to_512_by_512_png() -> None:
    frame = np.zeros((512, 512), dtype=np.float32)
    frame[160:352, 160:352] = 0.7

    encoded = frame_to_png_base64(frame)
    image = Image.open(io.BytesIO(base64.b64decode(encoded)))

    assert image.format == "PNG"
    assert image.size == (512, 512)
