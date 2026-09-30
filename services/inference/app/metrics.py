import numpy as np


def contingency(
    forecast_mask: np.ndarray,
    observed_mask: np.ndarray,
    valid_mask: np.ndarray | None = None,
) -> tuple[int, int, int]:
    """Count hits, misses, and false alarms for two boolean masks."""
    if valid_mask is None:
        valid = np.ones(forecast_mask.shape, dtype=bool)
    else:
        valid = valid_mask.astype(bool)

    forecast = forecast_mask.astype(bool) & valid
    observed = observed_mask.astype(bool) & valid
    hits = int(np.count_nonzero(forecast & observed))
    misses = int(np.count_nonzero(~forecast & observed & valid))
    false_alarms = int(np.count_nonzero(forecast & ~observed & valid))
    return hits, misses, false_alarms


def csi(hits: int, misses: int, false_alarms: int) -> float | None:
    """Compute CSI = H / (H + M + F), or None for a zero denominator."""
    denominator = hits + misses + false_alarms
    return None if denominator == 0 else hits / denominator


def pod(hits: int, misses: int) -> float | None:
    """Compute POD = H / (H + M), or None for a zero denominator."""
    denominator = hits + misses
    return None if denominator == 0 else hits / denominator


def far(hits: int, false_alarms: int) -> float | None:
    """Compute FAR = F / (H + F), or None for a zero denominator."""
    denominator = hits + false_alarms
    return None if denominator == 0 else false_alarms / denominator


def bias(hits: int, misses: int, false_alarms: int) -> float | None:
    """Compute BIAS = (H + F) / (H + M), or None for a zero denominator."""
    denominator = hits + misses
    return None if denominator == 0 else (hits + false_alarms) / denominator


def per_lead_metrics(
    forecast: np.ndarray, observed: np.ndarray
) -> dict[str, list[float | None]]:
    """Compute CSI, POD, FAR, and BIAS for each of six lead-time frames."""
    metrics: dict[str, list[float | None]] = {
        "csi": [],
        "pod": [],
        "far": [],
        "bias": [],
    }
    for forecast_frame, observed_frame in zip(forecast, observed):
        hits, misses, false_alarms = contingency(forecast_frame, observed_frame)
        metrics["csi"].append(csi(hits, misses, false_alarms))
        metrics["pod"].append(pod(hits, misses))
        metrics["far"].append(far(hits, false_alarms))
        metrics["bias"].append(bias(hits, misses, false_alarms))
    return metrics
