import os
import sys
from pathlib import Path

import numpy as np

THESIS_REPO = Path(os.environ["THESIS_REPO"])
sys.path.insert(0, str(THESIS_REPO))

from nowcasting.utils import rainfall_to_pixel

from app.preprocess import HKO_EVALUATOR, SINGAPORE, normalised_pixel_threshold

RAIN_RATES = (0.5, 2.0, 5.0, 10.0, 30.0)


def print_table(title: str, thesis_pair: tuple[float, float] | None = None) -> None:
    print(title)
    print("rain_rate_mm_h thesis_x raincast_x")
    for rain_rate in RAIN_RATES:
        if thesis_pair is None:
            thesis_x = rainfall_to_pixel(np.asarray(rain_rate))
        else:
            thesis_x = rainfall_to_pixel(
                np.asarray(rain_rate), a=thesis_pair[0], b=thesis_pair[1]
            )
        raincast_x = normalised_pixel_threshold(
            rain_rate, HKO_EVALUATOR if thesis_pair is None else SINGAPORE
        )
        print(f"{rain_rate:g} {float(thesis_x):.10f} {raincast_x:.10f}")


def main() -> None:
    print_table("Thesis default pair (58.53, 1.56)")
    print_table("Thesis function called with Singapore pair (61.75, 1.61)", SINGAPORE)


if __name__ == "__main__":
    main()
