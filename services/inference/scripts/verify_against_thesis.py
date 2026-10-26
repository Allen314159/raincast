import os
import sys
from pathlib import Path

import torch

THESIS_REPO = Path(os.environ["THESIS_REPO"])
MODEL_PATH = Path(os.environ["MODEL_PATH"])
sys.path.insert(0, str(THESIS_REPO))
sys.path.insert(0, str(Path(__file__).parents[1]))

from experiments.net_params import convlstm_encoder_params, convlstm_forecaster_params
from nowcasting.models.encoder import Encoder
from nowcasting.models.forecaster import Forecaster
from nowcasting.models.model import EF

from app.model import build_model


def main() -> None:
    torch.manual_seed(0)
    state_dict = torch.load(MODEL_PATH, map_location="cpu", weights_only=True)

    raincast = build_model().eval()
    raincast.load_state_dict(state_dict, strict=True)
    thesis = EF(
        Encoder(convlstm_encoder_params[0], convlstm_encoder_params[1]),
        Forecaster(convlstm_forecaster_params[0], convlstm_forecaster_params[1]),
    ).eval()
    missing, unexpected = thesis.load_state_dict(state_dict, strict=False)
    print(f"missing keys ({len(missing)}): {missing}")
    print(f"unexpected keys ({len(unexpected)}): {unexpected}")

    inputs = torch.rand(6, 1, 1, 512, 512)
    with torch.no_grad():
        raincast_output = raincast(inputs)
        thesis_output = thesis(inputs)
    difference = (raincast_output - thesis_output).abs()
    print(f"max abs diff: {difference.max().item():.10g}")
    print(f"mean abs diff: {difference.mean().item():.10g}")


if __name__ == "__main__":
    main()
