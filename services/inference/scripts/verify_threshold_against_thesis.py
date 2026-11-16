"""Compare thesis and RainCast normalised rain-rate thresholds locally."""

from __future__ import annotations

import os
import sys
from pathlib import Path

import numpy as np

INFERENCE_ROOT = Path(__file__).parents[1]
if str(INFERENCE_ROOT) not in sys.path:
    sys.path.insert(0, str(INFERENCE_ROOT))

THESIS_REPO = Path(os.environ["THESIS_REPO"])
sys.path.insert(0, str(THESIS_REPO))

from nowcasting.utils import rainfall_to_pixel

from app.preprocess import HKO_EVALUATOR, SINGAPORE, normalised_pixel_threshold

RAIN_RATES = (0.5, 2.0, 5.0, 10.0, 30.0)
PAIRS = (("HKO", HKO_EVALUATOR), ("Singapore", SINGAPORE))


def thesis_threshold(rain_rate: float, pair: tuple[float, float]) -> float:
    return float(
        rainfall_to_pixel(np.asarray(rain_rate), a=pair[0], b=pair[1])
    )


def print_table() -> None:
    print(
        "rain_rate_mm_h\tthesis_default\tRainCast_HKO\t"
        "diff_HKO\tthesis_singapore\tRainCast_Singapore\tdiff_Singapore"
    )
    for rain_rate in RAIN_RATES:
        thesis_default = float(rainfall_to_pixel(np.asarray(rain_rate)))
        thesis_values = [
            thesis_threshold(rain_rate, pair) for _, pair in PAIRS
        ]
        raincast_values = [
            normalised_pixel_threshold(rain_rate, pair) for _, pair in PAIRS
        ]
        print(
            f"{rain_rate:g}\t{thesis_default:.10f}\t"
            f"{raincast_values[0]:.10f}\t"
            f"{abs(thesis_values[0] - raincast_values[0]):.10g}\t"
            f"{thesis_values[1]:.10f}\t{raincast_values[1]:.10f}\t"
            f"{abs(thesis_values[1] - raincast_values[1]):.10g}"
        )


def main() -> None:
    print_table()


if __name__ == "__main__":
    main()
