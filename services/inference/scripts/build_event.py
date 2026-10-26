"""Build one local event from a streaming Nha Be archive.

The event index convention is start = the first input frame. Input frames are
start..start+5 and target frames are start+6..start+11.
"""

from __future__ import annotations

import argparse
import time
from pathlib import Path

import numpy as np
from event_data import build_event_arrays, stream_radar_frames


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--archive", type=Path, required=True)
    parser.add_argument("--start", type=int, required=True)
    parser.add_argument("--slug", required=True)
    parser.add_argument("--channel", type=int, default=0)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.start < 0:
        raise SystemExit("--start must be non-negative")
    started = time.perf_counter()
    frames: list[np.ndarray] = []
    for index, frame in enumerate(stream_radar_frames(args.archive)):
        if index >= args.start:
            frames.append(frame)
        if len(frames) == 12:
            break
    if len(frames) != 12:
        raise SystemExit("archive does not contain twelve frames at --start")
    input_frames, target_frames = build_event_arrays(
        np.stack(frames), args.channel, expected_grid=(512, 512)
    )
    output = Path(__file__).parents[1] / "data" / "events" / f"{args.slug}.npz"
    output.parent.mkdir(parents=True, exist_ok=True)
    np.savez(output, input=input_frames, target=target_frames)
    elapsed = time.perf_counter() - started
    print(f"{args.slug}\t{output.stat().st_size} bytes\t{elapsed:.3f} seconds")


if __name__ == "__main__":
    main()
