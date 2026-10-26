"""Streaming and validation helpers for curated radar event windows."""

from __future__ import annotations

import sys
import zipfile
from collections.abc import Iterator, Sequence
from pathlib import Path

import numpy as np

INFERENCE_ROOT = Path(__file__).parents[1]
if str(INFERENCE_ROOT) not in sys.path:
    sys.path.insert(0, str(INFERENCE_ROOT))


def _read_exact(stream: zipfile.ZipExtFile, size: int) -> bytes:
    data = stream.read(size)
    if len(data) != size:
        raise ValueError("radar_sequence.npy ended before the expected data")
    return data


def stream_radar_frames(archive: Path) -> Iterator[np.ndarray]:
    """Yield channel-preserving frames without loading the archive array."""
    with zipfile.ZipFile(archive) as archive_file:
        try:
            member = archive_file.open("radar_sequence.npy")
        except KeyError as error:
            raise ValueError("archive does not contain radar_sequence.npy") from error
        with member:
            version = np.lib.format.read_magic(member)
            if version == (1, 0):
                shape, fortran_order, dtype = np.lib.format.read_array_header_1_0(
                    member
                )
            elif version == (2, 0):
                shape, fortran_order, dtype = np.lib.format.read_array_header_2_0(
                    member
                )
            elif version == (3, 0):
                shape, fortran_order, dtype = np.lib.format.read_array_header_3_0(
                    member
                )
            else:
                raise ValueError(f"unsupported NPY version: {version}")
            if fortran_order or len(shape) != 4:
                raise ValueError("radar_sequence.npy must be a C-order 4D array")
            frame_size = int(np.prod(shape[1:]))
            frame_bytes = frame_size * dtype.itemsize
            for _ in range(shape[0]):
                raw = _read_exact(member, frame_bytes)
                yield np.frombuffer(raw, dtype=dtype).reshape(shape[1:])


def build_event_arrays(
    frames: Sequence[np.ndarray] | np.ndarray,
    channel: int = 0,
    *,
    expected_grid: tuple[int, int] | None = None,
) -> tuple[np.ndarray, np.ndarray]:
    """Validate twelve frames, select a channel, and split input from target."""
    array = np.asarray(frames)
    if array.ndim != 4 or array.shape[0] != 12:
        raise ValueError("an event must contain exactly 12 frames")
    if channel < 0 or channel >= array.shape[3]:
        raise ValueError(f"channel must be in [0, {array.shape[3] - 1}]")
    selected = np.asarray(array[..., channel], dtype=np.float32)
    if expected_grid is not None and selected.shape[1:] != expected_grid:
        raise ValueError(f"frames must have shape {expected_grid}")
    if not np.isfinite(selected).all():
        raise ValueError("event frames must contain only finite values")
    if np.any(selected < 0.0) or np.any(selected > 1.0):
        raise ValueError("event frames must be in the range [0, 1]")
    return selected[:6].copy(), selected[6:].copy()


def heavy_target_count(frames: Sequence[np.ndarray] | np.ndarray) -> int:
    """Count heavy-rain pixels in the six target frames of a twelve-frame window."""
    from app.preprocess import heavy_rain_mask

    array = np.asarray(frames)
    if array.ndim != 3 or array.shape[0] != 12:
        raise ValueError("an event must contain twelve single-channel frames")
    return int(np.count_nonzero(heavy_rain_mask(array[6:])))
