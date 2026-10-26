import numpy as np
import pytest

from app.preprocess import (
    HKO_EVALUATOR,
    SINGAPORE,
    dbz_to_rain_rate,
    heavy_rain_mask,
    normalise,
    normalised_pixel_threshold,
    normalised_to_dbz,
)


def test_normalise_and_denormalise_round_trip_inside_supported_range() -> None:
    dbz = np.array([-10.0, 0.0, 34.0, 60.0])

    np.testing.assert_allclose(normalised_to_dbz(normalise(dbz)), dbz)


def test_normalise_clips_values_outside_supported_range() -> None:
    dbz = np.array([-20.0, -10.0, 60.0, 70.0])

    np.testing.assert_allclose(normalise(dbz), np.array([0.0, 0.0, 1.0, 1.0]))


def test_dbz_to_rain_rate_at_34_dbz() -> None:
    assert abs(float(dbz_to_rain_rate(np.array(34.0), SINGAPORE)) - 10.0) < 0.1


def test_heavy_rain_mask_uses_10_mm_per_hour_threshold() -> None:
    threshold = normalised_pixel_threshold(10.0)
    x_normalised = np.array([threshold - 1e-6, threshold, threshold + 1e-6])

    np.testing.assert_array_equal(
        heavy_rain_mask(x_normalised), np.array([False, True, True])
    )


def test_singapore_threshold_uses_plus_ten_decoding() -> None:
    # x = (10*b*log10(R) + 10*log10(a) + 10) / 70
    # For R=10, a=61.75, b=1.61: x=(10*1.61*log10(10) + 10*log10(61.75) + 10)/70=0.6286624231.
    assert normalised_pixel_threshold(10.0, SINGAPORE) == pytest.approx(
        0.6286624231, abs=1e-6
    )


@pytest.mark.parametrize(
    ("rain_rate", "expected"),
    [
        (0.5, 0.3282531044),
        (2.0, 0.4624264739),
        (5.0, 0.5511102473),
        (10.0, 0.6181969320),
        (30.0, 0.7245268116),
    ],
)
def test_hko_evaluator_thresholds(rain_rate: float, expected: float) -> None:
    assert normalised_pixel_threshold(rain_rate, HKO_EVALUATOR) == pytest.approx(
        expected, abs=1e-6
    )


@pytest.mark.parametrize("rain_rate", [0.5, 2.0, 5.0, 30.0])
def test_hko_threshold_boundary_classifies_values_around_threshold(
    rain_rate: float,
) -> None:
    threshold = normalised_pixel_threshold(rain_rate, HKO_EVALUATOR)
    pixels = np.array([threshold - 1e-6, threshold, threshold + 1e-6])

    np.testing.assert_array_equal(
        heavy_rain_mask(pixels, rain_rate, HKO_EVALUATOR),
        np.array([False, True, True]),
    )


def test_preprocess_preserves_shapes_and_produces_no_nan() -> None:
    pixels = np.array([[0.0, 0.5], [0.6286624231, 1.0]])

    decoded = normalised_to_dbz(pixels)
    rain_rate = dbz_to_rain_rate(decoded)
    threshold = normalised_pixel_threshold(10.0)

    assert decoded.shape == pixels.shape
    assert rain_rate.shape == pixels.shape
    assert not np.isnan(decoded).any()
    assert not np.isnan(rain_rate).any()
    assert threshold == pytest.approx(0.6286624231, abs=1e-6)
