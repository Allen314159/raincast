import numpy as np
import torch
from fastapi.testclient import TestClient

from app import main


class StubModel(torch.nn.Module):
    def forward(self, input_sequence: torch.Tensor) -> torch.Tensor:
        return torch.zeros((6, 1, 360, 360), dtype=input_sequence.dtype)


def make_event(events_dir: str) -> None:
    frames = np.full((6, 360, 360), 0.8, dtype=np.float32)
    np.savez(f"{events_dir}/synthetic.npz", input=frames, target=frames)


def test_predict_returns_six_frames_and_metrics(tmp_path, monkeypatch) -> None:
    make_event(str(tmp_path))
    monkeypatch.setattr(main, "EVENTS_DIR", tmp_path)
    monkeypatch.setattr(main, "model", StubModel())

    response = TestClient(main.app).post("/predict", json={"eventId": "synthetic"})

    body = response.json()
    assert response.status_code == 200
    assert body["leadMinutes"] == [10, 20, 30, 40, 50, 60]
    assert len(body["frames"]["observed"]) == 6
    assert len(body["frames"]["convlstm"]) == 6
    assert len(body["frames"]["persistence"]) == 6
    assert len(body["metrics"]["convlstm"]["csi"]) == 6
    assert body["latencyMs"] >= 0


def test_predict_unknown_event_returns_404(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(main, "EVENTS_DIR", tmp_path)
    monkeypatch.setattr(main, "model", StubModel())

    response = TestClient(main.app).post("/predict", json={"eventId": "missing"})

    assert response.status_code == 404


def test_predict_invalid_body_returns_422(monkeypatch) -> None:
    monkeypatch.setattr(main, "model", StubModel())

    response = TestClient(main.app).post("/predict", json={})

    assert response.status_code == 422


def test_predict_without_model_returns_503(monkeypatch) -> None:
    monkeypatch.setattr(main, "model", None)

    response = TestClient(main.app).post("/predict", json={"eventId": "synthetic"})

    assert response.status_code == 503
