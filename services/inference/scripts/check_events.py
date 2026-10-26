"""Verify local event files against the committed web event list and manifest."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

ROOT = Path(__file__).parents[3]
EVENTS_DIR = ROOT / "services" / "inference" / "data" / "events"
WEB_EVENTS = ROOT / "apps" / "web" / "prisma" / "events.json"
MANIFEST = EVENTS_DIR / "manifest.json"
EXPECTED_SHAPE = (6, 512, 512)


def load_json(path: Path) -> list[dict[str, object]]:
    with path.open(encoding="utf-8") as file:
        value = json.load(file)
    if not isinstance(value, list):
        raise TypeError(f"{path} must contain a JSON list")
    return value


def check() -> None:
    web_events = load_json(WEB_EVENTS)
    manifest = load_json(MANIFEST)
    web_slugs = {str(event["slug"]) for event in web_events}
    manifest_slugs = {str(event["slug"]) for event in manifest}
    if web_slugs != manifest_slugs:
        raise ValueError("web events and manifest slugs differ")
    files = {path.stem for path in EVENTS_DIR.glob("*.npz")}
    if files != manifest_slugs:
        raise ValueError("event files and manifest slugs differ")
    for slug in sorted(files):
        with np.load(EVENTS_DIR / f"{slug}.npz") as event:
            if set(event.files) != {"input", "target"}:
                raise ValueError(f"{slug}: keys must be input and target")
            for key in event.files:
                values = event[key]
                if values.shape != EXPECTED_SHAPE or values.dtype != np.float32:
                    raise ValueError(f"{slug}: invalid {key} shape or dtype")
                if not np.isfinite(values).all() or np.any(values < 0) or np.any(values > 1):
                    raise ValueError(f"{slug}: invalid {key} range")
    print(f"checked {len(files)} event files")


if __name__ == "__main__":
    check()
