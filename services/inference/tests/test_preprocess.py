import numpy as np

from app.preprocess import dbz_to_rain_rate, denormalise, heavy_rain_mask, normalise


def test_normalise_and_denormalise_round_trip_inside_supported_range() -> None:
    dbz = np.array([-10.0, 0.0, 34.0, 60.0])

    np.testing.assert_allclose(denormalise(normalise(dbz)), dbz)


def test_normalise_clips_values_outside_supported_range() -> None:
    dbz = np.array([-20.0, -10.0, 60.0, 70.0])

    np.testing.assert_allclose(normalise(dbz), np.array([0.0, 0.0, 1.0, 1.0]))


def test_dbz_to_rain_rate_at_34_dbz() -> None:
    assert abs(float(dbz_to_rain_rate(np.array(34.0))) - 10.0) < 0.1


def test_heavy_rain_mask_uses_10_mm_per_hour_threshold() -> None:
    x_normalised = np.array([0.628, 0.629, 0.7])

    np.testing.assert_array_equal(
        heavy_rain_mask(x_normalised), np.array([False, True, True])
    )
