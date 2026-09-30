import numpy as np


def normalise(dbz: np.ndarray) -> np.ndarray:
    """Map clipped dBZ values from [-10, 60] to the normalised range [0, 1]."""
    return (np.clip(dbz, -10.0, 60.0) + 10.0) / 70.0


def denormalise(x: np.ndarray) -> np.ndarray:
    """Map normalised values back to dBZ with dBZ = 70*x - 10."""
    return 70.0 * x - 10.0


def dbz_to_rain_rate(dbz: np.ndarray) -> np.ndarray:
    """Convert dBZ using Singapore Z-R: R = (10^(dBZ/10) / 61.75)^(1/1.61)."""
    return (10.0 ** (dbz / 10.0) / 61.75) ** (1.0 / 1.61)


def heavy_rain_mask(
    x_normalised: np.ndarray, threshold_mm_h: float = 10.0
) -> np.ndarray:
    """Return pixels whose Z-R rain rate is at least the threshold in mm/h."""
    return dbz_to_rain_rate(denormalise(x_normalised)) >= threshold_mm_h
