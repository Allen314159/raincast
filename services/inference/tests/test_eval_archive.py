import numpy as np

from scripts.eval_archive import add_counts, counts_to_metrics, empty_counts


def test_archive_counts_are_aggregated_before_metrics() -> None:
    counts = empty_counts()
    add_counts(
        counts,
        np.repeat(np.array([[[1, 0]]], dtype=bool), 6, axis=0),
        np.repeat(np.array([[[1, 1]]], dtype=bool), 6, axis=0),
    )
    add_counts(
        counts,
        np.repeat(np.array([[[0, 1]]], dtype=bool), 6, axis=0),
        np.repeat(np.array([[[1, 0]]], dtype=bool), 6, axis=0),
    )

    metrics = counts_to_metrics(counts)

    assert metrics["csi"] == [0.25] * 6
    assert metrics["pod"] == [1 / 3] * 6
    assert metrics["far"] == [0.5] * 6
    assert metrics["bias"] == [2 / 3] * 6


def test_archive_zero_denominators_are_null() -> None:
    metrics = counts_to_metrics(empty_counts())

    assert metrics == {
        "csi": [None] * 6,
        "pod": [None] * 6,
        "far": [None] * 6,
        "bias": [None] * 6,
    }
