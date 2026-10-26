import numpy as np

MAX_DBZ = 60.0
MIN_DBZ = -10.0
DBZ_OFFSET = 10.0
DBZ_RANGE = 70.0
SINGAPORE = (61.75, 1.61)
HKO_EVALUATOR = (58.53, 1.56)
HEAVY_RAIN_MM_H = 10.0


def normalise(dbz: np.ndarray) -> np.ndarray:
    """Map clipped dBZ values from [-10, 60] to the normalised range [0, 1]."""
    return (np.clip(dbz, MIN_DBZ, MAX_DBZ) + DBZ_OFFSET) / DBZ_RANGE


def normalised_to_dbz(x: np.ndarray) -> np.ndarray:
    """Map normalised values back to dBZ with dBZ = 70*x - 10."""
    return DBZ_RANGE * x - DBZ_OFFSET


def denormalise(x: np.ndarray) -> np.ndarray:
    """Backward-compatible name for normalised_to_dbz."""
    return normalised_to_dbz(x)


def dbz_to_rain_rate(
    dbz: np.ndarray, z_r_pair: tuple[float, float] = SINGAPORE
) -> np.ndarray:
    """Convert dBZ to rain rate using a Z-R pair (a, b)."""
    a, b = z_r_pair
    return (10.0 ** (dbz / 10.0) / a) ** (1.0 / b)


def normalised_pixel_threshold(
    rain_rate_mm_h: float, z_r_pair: tuple[float, float] = SINGAPORE
) -> float:
    """Convert a rain-rate threshold to the normalised pixel scale."""
    a, b = z_r_pair
    return float(
        (10.0 * b * np.log10(rain_rate_mm_h) + 10.0 * np.log10(a) + DBZ_OFFSET)
        / DBZ_RANGE
    )


def heavy_rain_mask(
    x_normalised: np.ndarray,
    threshold_mm_h: float = HEAVY_RAIN_MM_H,
    z_r_pair: tuple[float, float] = SINGAPORE,
) -> np.ndarray:
    """Return pixels whose Z-R rain rate is at least the threshold in mm/h."""
    return (
        dbz_to_rain_rate(normalised_to_dbz(x_normalised), z_r_pair)
        >= threshold_mm_h
    )
