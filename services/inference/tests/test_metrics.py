import numpy as np

from app.metrics import bias, contingency, csi, far, per_lead_metrics, pod


def test_metrics_hand_made_example() -> None:
    forecast = np.array([[1, 1], [0, 0]], dtype=bool)
    observed = np.array([[1, 0], [1, 0]], dtype=bool)

    hits, misses, false_alarms = contingency(forecast, observed)

    assert (hits, misses, false_alarms) == (1, 1, 1)
    assert csi(hits, misses, false_alarms) == 1 / 3
    assert pod(hits, misses) == 0.5
    assert far(hits, false_alarms) == 0.5
    assert bias(hits, misses, false_alarms) == 1.0


def test_contingency_ignores_invalid_pixels() -> None:
    forecast = np.array([[1, 1], [0, 0]], dtype=bool)
    observed = np.array([[1, 0], [1, 1]], dtype=bool)
    valid = np.array([[1, 1], [0, 0]], dtype=bool)

    assert contingency(forecast, observed, valid) == (1, 0, 1)


def test_zero_denominators_return_none() -> None:
    assert csi(0, 0, 0) is None
    assert pod(0, 0) is None
    assert far(0, 0) is None
    assert bias(0, 0, 0) is None


def test_per_lead_metrics_returns_six_values_per_metric() -> None:
    forecast = np.zeros((6, 2, 2), dtype=bool)
    observed = np.zeros((6, 2, 2), dtype=bool)
    forecast[:, 0, 0] = True
    observed[:, 0, 0] = True

    result = per_lead_metrics(forecast, observed)

    assert result == {
        "csi": [1.0] * 6,
        "pod": [1.0] * 6,
        "far": [0.0] * 6,
        "bias": [1.0] * 6,
    }


def test_per_lead_metrics_returns_none_for_all_zero_masks() -> None:
    result = per_lead_metrics(
        np.zeros((6, 2, 2), dtype=bool), np.zeros((6, 2, 2), dtype=bool)
    )

    assert result == {
        "csi": [None] * 6,
        "pod": [None] * 6,
        "far": [None] * 6,
        "bias": [None] * 6,
    }
