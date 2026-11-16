"""Compare the RainCast model with the thesis ConvLSTM implementation locally."""

from __future__ import annotations

import os
import sys
from collections.abc import Callable
from pathlib import Path

import numpy as np
import torch

INFERENCE_ROOT = Path(__file__).parents[1]
if str(INFERENCE_ROOT) not in sys.path:
    sys.path.insert(0, str(INFERENCE_ROOT))

THESIS_REPO = Path(os.environ["THESIS_REPO"])
MODEL_PATH = Path(os.environ["MODEL_PATH"])
ARCHIVE_PATH = Path(
    os.getenv(
        "ARCHIVE_PATH",
        r"E:\PrecipitationNowcasting\NhaBe-npz\nhb_2023_05.npz",
    )
)
sys.path.insert(0, str(THESIS_REPO))

from experiments.net_params import (
    convlstm_encoder_params,
    convlstm_forecaster_params,
)
from nowcasting.models.encoder import Encoder
from nowcasting.models.forecaster import Forecaster
from nowcasting.models.model import EF

from app.model import build_model
from scripts.event_data import stream_radar_frames

REAL_START_INDEX = 3647
INPUT_LENGTH = 6
EXPECTED_MISSING_KEYS = 18
LAYER_NAMES = (
    "encoder.stage1",
    "encoder.rnn1",
    "encoder.stage2",
    "encoder.rnn2",
    "encoder.stage3",
    "encoder.rnn3",
    "forecaster.rnn3",
    "forecaster.stage3",
    "forecaster.rnn2",
    "forecaster.stage2",
    "forecaster.rnn1",
    "forecaster.stage1",
)


def build_thesis_model() -> EF:
    return EF(
        Encoder(convlstm_encoder_params[0], convlstm_encoder_params[1]),
        Forecaster(convlstm_forecaster_params[0], convlstm_forecaster_params[1]),
    ).eval()


def load_models() -> tuple[torch.nn.Module, EF]:
    state_dict = torch.load(MODEL_PATH, map_location="cpu", weights_only=True)
    raincast = build_model().eval()
    raincast.load_state_dict(state_dict, strict=True)
    thesis = build_thesis_model()
    missing, unexpected = thesis.load_state_dict(state_dict, strict=False)
    print(f"missing keys ({len(missing)}): {missing}")
    print(f"unexpected keys ({len(unexpected)}): {unexpected}")
    if len(missing) != EXPECTED_MISSING_KEYS or unexpected:
        raise RuntimeError("thesis checkpoint key comparison did not match expectations")
    return raincast, thesis


def compare_outputs(
    raincast_output: torch.Tensor, thesis_output: torch.Tensor
) -> tuple[float, float]:
    difference = (raincast_output - thesis_output).abs()
    return float(difference.max()), float(difference.mean())


def flatten_tensors(value: object) -> list[torch.Tensor]:
    if isinstance(value, torch.Tensor):
        return [value]
    if isinstance(value, (tuple, list)):
        tensors: list[torch.Tensor] = []
        for item in value:
            tensors.extend(flatten_tensors(item))
        return tensors
    return []


def get_module(model: torch.nn.Module, dotted_name: str) -> torch.nn.Module:
    current: object = model
    for part in dotted_name.split("."):
        current = getattr(current, part)
    if not isinstance(current, torch.nn.Module):
        raise TypeError(f"{dotted_name} is not a module")
    return current


def capture_intermediates(
    model: torch.nn.Module,
) -> tuple[dict[str, list[torch.Tensor]], list[torch.utils.hooks.RemovableHandle]]:
    captured: dict[str, list[torch.Tensor]] = {}
    handles = []

    def make_hook(name: str) -> Callable[..., None]:
        def hook(_: torch.nn.Module, __: tuple[object, ...], output: object) -> None:
            captured[name] = flatten_tensors(output)

        return hook

    for name in LAYER_NAMES:
        handles.append(get_module(model, name).register_forward_hook(make_hook(name)))
    return captured, handles


def print_first_divergence(
    raincast: torch.nn.Module, thesis: EF, inputs: torch.Tensor
) -> None:
    raincast_layers, raincast_handles = capture_intermediates(raincast)
    thesis_layers, thesis_handles = capture_intermediates(thesis)
    try:
        with torch.no_grad():
            raincast(inputs)
            thesis(inputs)
    finally:
        for handle in raincast_handles + thesis_handles:
            handle.remove()
    for name in LAYER_NAMES:
        raincast_values = raincast_layers.get(name, [])
        thesis_values = thesis_layers.get(name, [])
        if len(raincast_values) != len(thesis_values):
            print(f"first diverging layer: {name} (tensor count differs)")
            return
        for raincast_value, thesis_value in zip(raincast_values, thesis_values):
            if raincast_value.shape != thesis_value.shape:
                print(f"first diverging layer: {name} (shape differs)")
                return
            maximum, mean = compare_outputs(raincast_value, thesis_value)
            if maximum > 1e-5:
                print(
                    f"first diverging layer: {name}; "
                    f"max abs diff={maximum:.10g}; mean abs diff={mean:.10g}"
                )
                return
    print("first diverging layer: none found in captured layers")


def load_real_window() -> torch.Tensor:
    frames: list[np.ndarray] = []
    for index, frame in enumerate(stream_radar_frames(ARCHIVE_PATH)):
        if index >= REAL_START_INDEX:
            frames.append(frame[..., 0])
        if len(frames) == INPUT_LENGTH:
            break
    if len(frames) != INPUT_LENGTH:
        raise RuntimeError("archive ended before the real input window was read")
    values = np.stack(frames).astype(np.float32, copy=False)
    return torch.from_numpy(values[:, None, None, ...])


def check_input(
    label: str,
    inputs: torch.Tensor,
    raincast: torch.nn.Module,
    thesis: EF,
) -> None:
    with torch.no_grad():
        raincast_output = raincast(inputs)
        thesis_output = thesis(inputs)
    maximum, mean = compare_outputs(raincast_output, thesis_output)
    print(f"{label} max abs diff: {maximum:.10g}")
    print(f"{label} mean abs diff: {mean:.10g}")
    if label == "real":
        print(
            "real RainCast raw output "
            f"min/max/mean: {raincast_output.min().item():.10g}/"
            f"{raincast_output.max().item():.10g}/"
            f"{raincast_output.mean().item():.10g}"
        )
    if maximum > 1e-5:
        print_first_divergence(raincast, thesis, inputs)
        raise RuntimeError(f"{label} model equivalence target failed")


def main() -> None:
    raincast, thesis = load_models()
    torch.manual_seed(0)
    random_input = torch.rand(6, 1, 1, 512, 512)
    check_input("random", random_input, raincast, thesis)
    real_input = load_real_window()
    check_input("real", real_input, raincast, thesis)


if __name__ == "__main__":
    main()
