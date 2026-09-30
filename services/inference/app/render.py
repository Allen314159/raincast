import base64
import io

import numpy as np
from PIL import Image


def frame_to_png_base64(x_normalised: np.ndarray) -> str:
    """Render normalised dBZ data as a transparent low-value radar-like PNG."""
    dbz = np.asarray(70.0 * x_normalised - 10.0, dtype=float)
    clipped = np.clip(dbz, -10.0, 60.0)

    stops = np.array([-10.0, 5.0, 15.0, 25.0, 34.0, 45.0, 60.0])
    colours = np.array(
        [
            [0, 0, 0],
            [40, 80, 160],
            [0, 170, 220],
            [0, 190, 80],
            [255, 235, 0],
            [255, 100, 0],
            [180, 0, 0],
        ],
        dtype=float,
    )
    rgb = np.stack(
        [np.interp(clipped, stops, colours[:, channel]) for channel in range(3)],
        axis=-1,
    ).astype(np.uint8)
    alpha = np.where(dbz <= -10.0, 0, 255).astype(np.uint8)[..., np.newaxis]
    rgba = np.concatenate((rgb, alpha), axis=-1)

    buffer = io.BytesIO()
    Image.fromarray(rgba, mode="RGBA").save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode("ascii")
