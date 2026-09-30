import os
import sys
from pathlib import Path

import numpy as np
import torch

sys.path.insert(0, str(Path(__file__).parents[1]))

from app.main import load_event, load_model
from app.metrics import per_lead_metrics
from app.preprocess import heavy_rain_mask


def main() -> None:
    model_path = os.getenv("MODEL_PATH")
    event_id = os.getenv("EVENT_ID")
    if not model_path:
        raise SystemExit("Set MODEL_PATH to the real checkpoint path.")
    if not event_id:
        raise SystemExit("Set EVENT_ID to a .npz event filename without its extension.")

    model = load_model(model_path)
    if model is None:
        raise SystemExit(f"Checkpoint was not found: {model_path}")
    input_frames, observed = load_event(event_id)
    input_tensor = torch.from_numpy(input_frames[:, np.newaxis, ...])
    with torch.no_grad():
        prediction = model(input_tensor).cpu().numpy()[:, 0]
    prediction = np.clip(prediction, 0.0, 1.0)
    persistence = np.repeat(input_frames[-1][np.newaxis, ...], 6, axis=0)

    observed_mask = heavy_rain_mask(observed)
    convlstm = per_lead_metrics(heavy_rain_mask(prediction), observed_mask)
    persistence_metrics = per_lead_metrics(heavy_rain_mask(persistence), observed_mask)
    for lead, convlstm_csi, persistence_csi in zip(
        (10, 20, 30, 40, 50, 60), convlstm["csi"], persistence_metrics["csi"]
    ):
        print(
            f"t+{lead} min: ConvLSTM CSI={convlstm_csi!r}, "
            f"persistence CSI={persistence_csi!r}"
        )


if __name__ == "__main__":
    main()
