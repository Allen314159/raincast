import os
import time
from contextlib import asynccontextmanager
from pathlib import Path

import numpy as np
import torch
from fastapi import FastAPI, HTTPException

from app.metrics import per_lead_metrics
from app.model import build_model
from app.preprocess import heavy_rain_mask
from app.render import frame_to_png_base64
from app.schemas import (
    LEAD_MINUTES,
    FrameSet,
    HealthResponse,
    Metrics,
    MetricSet,
    PredictRequest,
    PredictResponse,
)

EVENTS_DIR = Path(__file__).parent.parent / "data" / "events"
MODEL_PATH = os.getenv("MODEL_PATH")
MODEL_VERSION = os.getenv("MODEL_VERSION", "convlstm-89000")
model: torch.nn.Module | None = None


def load_model(model_path: str | None) -> torch.nn.Module | None:
    if not model_path or not Path(model_path).is_file():
        return None
    state_dict = torch.load(model_path, map_location="cpu", weights_only=True)
    network = build_model()
    network.load_state_dict(state_dict)
    network.to("cpu")
    network.eval()
    return network


@asynccontextmanager
async def lifespan(_: FastAPI):
    global model
    model = load_model(MODEL_PATH)
    yield
    model = None


app = FastAPI(title="RainCast Inference", lifespan=lifespan)


def event_path(event_id: str) -> Path:
    event_files = {path.stem: path for path in EVENTS_DIR.glob("*.npz")}
    if event_id not in event_files:
        raise HTTPException(status_code=404, detail="Unknown eventId")
    return event_files[event_id]


def load_event(event_id: str) -> tuple[np.ndarray, np.ndarray]:
    with np.load(event_path(event_id)) as event:
        input_frames = np.asarray(event["input"], dtype=np.float32)
        target_frames = np.asarray(event["target"], dtype=np.float32)
    expected_shape = (6, 360, 360)
    if input_frames.shape != expected_shape or target_frames.shape != expected_shape:
        raise HTTPException(status_code=500, detail="Invalid event shape")
    if (
        not np.isfinite(input_frames).all()
        or not np.isfinite(target_frames).all()
        or np.any(input_frames < 0.0)
        or np.any(input_frames > 1.0)
        or np.any(target_frames < 0.0)
        or np.any(target_frames > 1.0)
    ):
        raise HTTPException(status_code=500, detail="Invalid event values")
    return input_frames, target_frames


def metric_model(values: dict[str, list[float | None]]) -> Metrics:
    return Metrics(**values)


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(
        status="ok", modelLoaded=model is not None, modelVersion=MODEL_VERSION
    )


@app.post("/predict", response_model=PredictResponse)
def predict(request: PredictRequest) -> PredictResponse:
    if model is None:
        raise HTTPException(status_code=503, detail="Model is not loaded")

    input_frames, observed = load_event(request.eventId)
    started = time.perf_counter()
    input_tensor = torch.from_numpy(input_frames[:, np.newaxis, ...])
    with torch.no_grad():
        prediction = model(input_tensor).detach().cpu().numpy()
    prediction = np.clip(prediction[:, 0, ...], 0.0, 1.0)
    persistence = np.repeat(input_frames[-1][np.newaxis, ...], 6, axis=0)

    observed_mask = heavy_rain_mask(observed)
    convlstm_metrics = per_lead_metrics(heavy_rain_mask(prediction), observed_mask)
    persistence_metrics = per_lead_metrics(heavy_rain_mask(persistence), observed_mask)

    def render_frames(frames: np.ndarray) -> list[str]:
        return [frame_to_png_base64(frame) for frame in frames]

    rendered_frames = FrameSet(
        observed=render_frames(observed),
        convlstm=render_frames(prediction),
        persistence=render_frames(persistence),
    )
    latency_ms = int((time.perf_counter() - started) * 1000)
    return PredictResponse(
        eventId=request.eventId,
        modelVersion=MODEL_VERSION,
        thresholdMmPerHour=10.0,
        leadMinutes=LEAD_MINUTES,
        frames=rendered_frames,
        metrics=MetricSet(
            convlstm=metric_model(convlstm_metrics),
            persistence=metric_model(persistence_metrics),
        ),
        latencyMs=latency_ms,
    )
