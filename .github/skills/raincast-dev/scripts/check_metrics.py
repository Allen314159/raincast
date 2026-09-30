"""Check RainCast event metrics on small binary masks without dependencies."""

from __future__ import annotations

from typing import Iterable


def event_counts(observed: Iterable[bool], predicted: Iterable[bool]) -> tuple[int, int, int]:
    """Return hits, misses, and false alarms for paired event masks."""
    pairs = list(zip(observed, predicted, strict=True))
    hits = sum(actual and forecast for actual, forecast in pairs)
    misses = sum(actual and not forecast for actual, forecast in pairs)
    false_alarms = sum(not actual and forecast for actual, forecast in pairs)
    return hits, misses, false_alarms


def ratio(numerator: int, denominator: int) -> float | None:
    """Return a metric ratio, using None for an undefined zero denominator."""
    return None if denominator == 0 else numerator / denominator


def metrics(observed: Iterable[bool], predicted: Iterable[bool]) -> dict[str, float | None]:
    """Calculate CSI, POD, FAR, and BIAS for one lead time."""
    hits, misses, false_alarms = event_counts(observed, predicted)
    return {
        "CSI": ratio(hits, hits + misses + false_alarms),
        "POD": ratio(hits, hits + misses),
        "FAR": ratio(false_alarms, hits + false_alarms),
        "BIAS": ratio(hits + false_alarms, hits + misses),
    }


def self_test() -> None:
    result = metrics(
        [True, True, False, False],
        [True, False, True, False],
    )
    assert result == {"CSI": 1 / 3, "POD": 1 / 2, "FAR": 1 / 2, "BIAS": 1.0}
    assert metrics([False], [False]) == {
        "CSI": None,
        "POD": None,
        "FAR": None,
        "BIAS": None,
    }


if __name__ == "__main__":
    self_test()
    print("check_metrics.py self-test passed")
