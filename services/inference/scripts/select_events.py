"""Select archive windows without model predictions.

The index convention is start = the index of the FIRST input frame. Input
frames are start..start+5; target frames are start+6..start+11. The
heavy-rain count is taken on the six TARGET frames only.
"""

from __future__ import annotations

import argparse
from collections import deque
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from event_data import heavy_target_count, stream_radar_frames


@dataclass(frozen=True)
class Window:
    start: int
    heavy_count: int
    pixel_count: int

    @property
    def fraction(self) -> float:
        return self.heavy_count / self.pixel_count


def window_heavy_count(frames: np.ndarray) -> int:
    return heavy_target_count(frames)


def scan_windows(archive: Path, first: int, last: int) -> list[Window]:
    if first < 0 or last < first:
        raise ValueError("invalid archive range")
    windows: list[Window] = []
    frame_window: deque[np.ndarray] = deque(maxlen=12)
    for index, frame in enumerate(stream_radar_frames(archive)):
        frame_window.append(frame[..., 0])
        if len(frame_window) < 12:
            continue
        start = index - 11
        if start < first or start + 11 > last:
            continue
        frames = np.stack(frame_window)
        windows.append(Window(start, window_heavy_count(frames), 6 * frames.shape[1] * frames.shape[2]))
    return windows


def keep_spaced(windows: list[Window], minimum_spacing: int = 24) -> list[Window]:
    """Keep the highest-fraction windows while enforcing a minimum spacing."""
    selected: list[Window] = []
    for window in sorted(windows, key=lambda item: (-item.fraction, item.start)):
        if all(abs(window.start - other.start) >= minimum_spacing for other in selected):
            selected.append(window)
    return sorted(selected, key=lambda item: item.start)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--archive", type=Path, required=True)
    parser.add_argument("--first", type=int, default=3598)
    parser.add_argument("--last", type=int, default=4461)
    parser.add_argument("--minimum-spacing", type=int, default=24)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    windows = scan_windows(args.archive, args.first, args.last)
    for window in keep_spaced(windows, args.minimum_spacing):
        print(f"{window.start}\t{window.heavy_count}\t{window.fraction:.12f}")


if __name__ == "__main__":
    main()
