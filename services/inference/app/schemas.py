from pydantic import BaseModel, Field

LEAD_MINUTES = [10, 20, 30, 40, 50, 60]


class PredictRequest(BaseModel):
    eventId: str = Field(min_length=1)


class FrameSet(BaseModel):
    observed: list[str] = Field(min_length=6, max_length=6)
    convlstm: list[str] = Field(min_length=6, max_length=6)
    persistence: list[str] = Field(min_length=6, max_length=6)


class Metrics(BaseModel):
    csi: list[float | None] = Field(min_length=6, max_length=6)
    pod: list[float | None] = Field(min_length=6, max_length=6)
    far: list[float | None] = Field(min_length=6, max_length=6)
    bias: list[float | None] = Field(min_length=6, max_length=6)


class MetricSet(BaseModel):
    convlstm: Metrics
    persistence: Metrics


class PredictResponse(BaseModel):
    eventId: str
    modelVersion: str
    thresholdMmPerHour: float
    leadMinutes: list[int]
    frames: FrameSet
    metrics: MetricSet
    latencyMs: int


class HealthResponse(BaseModel):
    status: str
    modelLoaded: bool
    modelVersion: str
