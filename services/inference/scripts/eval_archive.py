"""Evaluate the ConvLSTM and persistence baseline on streamed archive windows."""

from __future__ import annotations

import argparse
import json
import sys
from collections import deque
from pathlib import Path
from typing import Any

import numpy as np
import torch

INFERENCE_ROOT = Path(__file__).parents[1]
if str(INFERENCE_ROOT) not in sys.path:
    sys.path.insert(0, str(INFERENCE_ROOT))

from app.metrics import bias, contingency, csi, far, pod
from app.model import build_model
from app.preprocess import (
    HKO_EVALUATOR,
    SINGAPORE,
    heavy_rain_mask,
    normalised_pixel_threshold,
)
from scripts.event_data import stream_radar_frames

LEADS = [10, 20, 30, 40, 50, 60]
THRESHOLDS = {
    "primary_d1_singapore": SINGAPORE,
    "reproduction_d2_hko": HKO_EVALUATOR,
}


def empty_counts() -> list[dict[str, int]]:
    return [{"hits": 0, "misses": 0, "falseAlarms": 0} for _ in LEADS]


def add_counts(
    counts: list[dict[str, int]],
    forecast: np.ndarray,
    observed: np.ndarray,
) -> None:
    for index in range(len(LEADS)):
        hits, misses, false_alarms = contingency(forecast[index], observed[index])
        counts[index]["hits"] += hits
        counts[index]["misses"] += misses
        counts[index]["falseAlarms"] += false_alarms


def counts_to_metrics(counts: list[dict[str, int]]) -> dict[str, list[float | None]]:
    return {
        "csi": [
            csi(row["hits"], row["misses"], row["falseAlarms"]) for row in counts
        ],
        "pod": [pod(row["hits"], row["misses"]) for row in counts],
        "far": [far(row["hits"], row["falseAlarms"]) for row in counts],
        "bias": [
            bias(row["hits"], row["misses"], row["falseAlarms"]) for row in counts
        ],
    }


def predict_window(
    model: torch.nn.Module,
    input_frames: np.ndarray,
    target_frames: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, bool]:
    input_tensor = torch.from_numpy(input_frames[:, np.newaxis, np.newaxis, ...])
    with torch.no_grad():
        prediction = model(input_tensor).detach().cpu().numpy()[:, 0]
    prediction = np.clip(prediction, 0.0, 1.0)
    persistence = np.repeat(input_frames[-1][np.newaxis, ...], 6, axis=0)
    return (
        prediction,
        persistence,
        target_frames,
        bool(
            np.isfinite(prediction).all()
            and np.isfinite(input_frames).all()
            and np.isfinite(target_frames).all()
        ),
    )


def add_window_to_counts(
    counts: dict[str, list[dict[str, int]]],
    prediction: np.ndarray,
    persistence: np.ndarray,
    target_frames: np.ndarray,
    z_r_pair: tuple[float, float],
) -> None:
    observed = heavy_rain_mask(target_frames, z_r_pair=z_r_pair)
    add_counts(
        counts["convlstm"],
        heavy_rain_mask(prediction, z_r_pair=z_r_pair),
        observed,
    )
    add_counts(
        counts["persistence"],
        heavy_rain_mask(persistence, z_r_pair=z_r_pair),
        observed,
    )


def metrics_for_window(
    prediction: np.ndarray,
    persistence: np.ndarray,
    target_frames: np.ndarray,
    z_r_pair: tuple[float, float],
) -> dict[str, dict[str, list[float | None]]]:
    local_counts = {"convlstm": empty_counts(), "persistence": empty_counts()}
    add_window_to_counts(
        local_counts, prediction, persistence, target_frames, z_r_pair
    )
    return {
        model_name: counts_to_metrics(model_counts)
        for model_name, model_counts in local_counts.items()
    }


def evaluate(
    archive: Path,
    model_path: Path,
    events_dir: Path | None,
    stride: int,
) -> dict[str, Any]:
    if stride < 1:
        raise ValueError("stride must be positive")
    state_dict = torch.load(model_path, map_location="cpu", weights_only=True)
    model = build_model()
    model.load_state_dict(state_dict)
    model.eval()
    counts = {
        threshold_name: {
            model_name: empty_counts() for model_name in ("convlstm", "persistence")
        }
        for threshold_name in THRESHOLDS
    }
    windows = 0
    finite = True
    buffered: deque[np.ndarray] = deque(maxlen=12)
    for frame_index, frame in enumerate(stream_radar_frames(archive)):
        buffered.append(np.asarray(frame[..., 0], dtype=np.float32))
        if len(buffered) < 12:
            continue
        start = frame_index - 11
        if start % stride != 0:
            continue
        window = np.stack(buffered)
        input_frames, target_frames = window[:6], window[6:]
        prediction, persistence, target, window_finite = predict_window(
            model, input_frames, target_frames
        )
        finite = window_finite and finite
        for threshold_name, z_r_pair in THRESHOLDS.items():
            add_window_to_counts(
                counts[threshold_name], prediction, persistence, target, z_r_pair
            )
        windows += 1

    event_names: list[str] = []
    event_results: dict[str, Any] = {}
    if events_dir and events_dir.is_dir():
        for event_path in sorted(events_dir.glob("*.npz")):
            with np.load(event_path) as event:
                input_frames = np.asarray(event["input"], dtype=np.float32)
                target_frames = np.asarray(event["target"], dtype=np.float32)
            event_names.append(event_path.stem)
            prediction, persistence, target, event_finite = predict_window(
                model, input_frames, target_frames
            )
            finite = event_finite and finite
            event_results[event_path.stem] = {
                threshold_name: metrics_for_window(
                    prediction, persistence, target, z_r_pair
                )
                for threshold_name, z_r_pair in THRESHOLDS.items()
            }
            for threshold_name, z_r_pair in THRESHOLDS.items():
                add_window_to_counts(
                    counts[threshold_name],
                    prediction,
                    persistence,
                    target,
                    z_r_pair,
                )
            windows += 1

    result: dict[str, Any] = {
        "archive": str(archive),
        "archiveMonth": archive.stem.removeprefix("nhb_"),
        "checkpoint": str(model_path),
        "stride": stride,
        "archiveWindows": windows - len(event_names),
        "eventWindows": event_names,
        "events": event_results,
        "windows": windows,
        "thresholds": {
            name: {
                "zR": list(pair),
                "normalisedThreshold": float(
                    normalised_pixel_threshold(10.0, pair)
                ),
                "models": {
                    model_name: {
                        "counts": counts[name][model_name],
                        "metrics": counts_to_metrics(counts[name][model_name]),
                    }
                    for model_name in ("convlstm", "persistence")
                },
            }
            for name, pair in THRESHOLDS.items()
        },
        "finite": finite,
    }
    return result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--archive", type=Path, required=True)
    parser.add_argument("--model", type=Path, required=True)
    parser.add_argument("--events-dir", type=Path)
    parser.add_argument("--stride", type=int, default=50)
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = evaluate(args.archive, args.model, args.events_dir, args.stride)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(args.output), "windows": result["windows"]}))


if __name__ == "__main__":
    main()
