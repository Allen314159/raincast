import numpy as np
import pytest

from app.preprocess import normalised_pixel_threshold
from scripts.event_data import build_event_arrays, heavy_target_count


def test_build_event_splits_and_selects_channel() -> None:
    frames = np.zeros((12, 2, 2, 2), dtype=np.float64)
    frames[..., 1] = 0.25
    frames[:6, ..., 0] = 0.1
    frames[6:, ..., 0] = 0.9

    inputs, targets = build_event_arrays(frames, channel=0)

    assert inputs.shape == (6, 2, 2)
    assert targets.shape == (6, 2, 2)
    assert inputs.dtype == np.float32
    np.testing.assert_allclose(inputs, 0.1)
    np.testing.assert_allclose(targets, 0.9)


@pytest.mark.parametrize(
    "frames",
    [
        np.zeros((11, 2, 2, 1)),
        np.zeros((12, 2, 2)),
        np.full((12, 2, 2, 1), np.nan),
        np.full((12, 2, 2, 1), 1.1),
    ],
)
def test_build_event_rejects_invalid_frames(frames: np.ndarray) -> None:
    with pytest.raises(ValueError):
        build_event_arrays(frames)


def test_heavy_count_uses_targets_not_inputs() -> None:
    threshold = normalised_pixel_threshold(10.0)
    input_heavy = np.full((6, 2, 2), threshold)
    target_light = np.zeros((6, 2, 2))
    assert heavy_target_count(np.concatenate((input_heavy, target_light))) == 0

    input_light = np.zeros((6, 2, 2))
    target_heavy = np.full((6, 2, 2), threshold)
    assert heavy_target_count(np.concatenate((input_light, target_heavy))) == 24
