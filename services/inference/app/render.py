import base64
import io

import numpy as np
from PIL import Image

from app.preprocess import (
    MAX_DBZ,
    MIN_DBZ,
    normalised_pixel_threshold,
    normalised_to_dbz,
)


def frame_to_png_base64(x_normalised: np.ndarray) -> str:
    """Render normalised dBZ data as a transparent low-value radar-like PNG."""
    dbz = np.asarray(normalised_to_dbz(x_normalised), dtype=float)
    clipped = np.clip(dbz, MIN_DBZ, MAX_DBZ)

    stops = np.array(
        [
            MIN_DBZ,
            5.0,
            15.0,
            25.0,
            normalised_to_dbz(
                np.asarray(normalised_pixel_threshold(10.0))
            ),
            45.0,
            MAX_DBZ,
        ]
    )
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
    alpha = np.where(dbz <= MIN_DBZ, 0, 255).astype(np.uint8)[..., np.newaxis]
    rgba = np.concatenate((rgb, alpha), axis=-1)

    buffer = io.BytesIO()
    Image.fromarray(rgba, mode="RGBA").save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode("ascii")
