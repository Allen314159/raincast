# RainCast — Project Specification

> Version 0.1 · Owner: Lam My Trang · Status: planning
> Source of truth for *what* we build. Engineering rules are in `RULES.md`; agent instructions are in `../AGENTS.md`.

---

## 1. Purpose

RainCast is a small full-stack web app that lets a user pick a past heavy-rain event over Ho Chi Minh City and compare, side by side:

1. **Observed** radar frames (ground truth),
2. **ConvLSTM** forecasts (the baseline model trained in the owner's undergraduate thesis),
3. **Persistence** forecasts (repeat the last observed frame — the naive baseline).

It exists for two reasons:

- **Portfolio:** demonstrate a complete, tested, containerised, CI-checked and deployed full-stack system (Next.js, TypeScript, Prisma, PostgreSQL, FastAPI, Docker, GitHub Actions).
- **Thesis showcase:** make the thesis model tangible, and show honest evaluation (CSI/POD/FAR) instead of only pictures.

This is a **research demo, not an operational weather service.** The UI must say so.

## 2. Scope

### In scope (MVP)
- List of curated radar events (8–10) stored as sample files.
- Run the ConvLSTM on an event and show 6 forecast frames (t+10 … t+60 min).
- Show Observed | ConvLSTM | Persistence for the selected lead time.
- Compute and show CSI, POD, FAR (and BIAS) at the heavy-rain threshold per lead time.
- Save each forecast run (metadata + metrics) in PostgreSQL; show a history page.
- Unit/API tests, Docker Compose for local run, GitHub Actions CI, public deployment.

### Out of scope (do NOT build)
- User accounts, login, payments.
- Real-time or live radar ingestion; anything that pulls from the station.
- Training or fine-tuning models inside this repo.
- The U-Net + Transformer model (owned by the thesis partner; not part of this project).
- Mobile app, notifications, maps with tiles.

## 3. Background: how this relates to the thesis

| Thesis fact | Value used in this project |
|---|---|
| Data source | Nha Be weather radar, Ho Chi Minh City (10.6596°N, 106.7283°E), scan mode CD2, 120 km range |
| Grid | 360 × 360 pixels, 0.667 km/pixel (240 × 240 km) |
| Time step | ≈ 10 minutes between frames |
| Sample structure | 6 input frames (t−50 … t0) → 6 target frames (t+10 … t+60), stored as `.npz` with arrays `input` and `target`, each `(6, 360, 360)` |
| Normalisation | `x = (clip(dBZ, −10, 60) + 10) / 70`, range [0, 1] |
| uint8 decoding (raw files, not used here) | `dBZ = (uint8 − 64) / 2`; values 0 and 255 are invalid → NaN |
| Z–R relation | Singapore: `Z = 61.75 · R^1.61` → `R = (10^(dBZ/10) / 61.75)^(1/1.61)` |
| Heavy-rain threshold | R ≥ 10 mm/h ≈ 34.0 dBZ ≈ 0.629 normalised |
| Baseline model | ConvLSTM encoder–forecaster, Adam lr 1e-4, StepLR (γ 0.7 / 20k iters), balanced B-MSE + B-MAE loss, checkpoint `encoder_forecaster_89000.pth` |
| Baseline result (test set, >10 mm/h) | CSI 0.2214 · POD 0.5968 · FAR 0.7462 · BIAS 2.3516 |
| Baseline CSI by lead time | t+10 0.3701 · t+20 0.2759 · t+30 0.2196 · t+40 0.1815 · t+50 0.1522 · t+60 0.1291 |

**Only the ConvLSTM baseline is served here.** The thesis's proposed model reached CSI 0.291 (+83% over persistence); never present the baseline's numbers as that model's numbers.

## 4. Open questions (must be answered before/while building — agents must NOT guess)

| # | Question | Where to look | Answer |
|---|---|---|---|
| Q1 | Exact model class and constructor arguments used to train `encoder_forecaster_89000.pth` | owner's training code | The attached training code builds `EF(encoder, forecaster)` from `nowcasting/models/model.py:24` and `experiments/convLSTM_balacned_mse_mae/main.py:112-118`. Its recurrent cells are `ConvLSTM(input_channel, num_filter, b_h_w, kernel_size, stride=1, padding=1)` from `nowcasting/models/convLSTM.py:5`. The configured encoder cells are `8 -> 64`, `192 -> 192`, `192 -> 192`; the forecaster cells are `192 -> 192`, `192 -> 192`, `64 -> 64`, configured in `experiments/net_params.py:88-121`. The attached source was verified, but the requested `89000` checkpoint itself was not found. |
| Q2 | Input tensor layout the model expects (e.g. `[B, T, C, H, W]` vs `[T, B, C, H, W]`) | training code | Dataset tensors are `float32` (`npz_dataset.py:104,113`) and are initially batched as `[B, T, C, H, W]`. Training permutes them at `experiments/convLSTM_balacned_mse_mae/main.py:143` to `[T, B, C, H, W]`, which is the model input layout documented in `nowcasting/models/encoder.py:30`. The attached configuration and smoke test use `T=6`, `C=1`, and `H=W=512`, not RainCast's specified 360x360 grid. |
| Q3 | How NaN pixels were filled before training (0? masked?) | preprocessing code | Not found. `np.nanmax` is used only to inspect the maximum (`npz_dataset.py:108`); `np.clip` does not replace NaNs (`npz_dataset.py:111`). The NPY training path creates an all-ones mask (`experiments/convLSTM_balacned_mse_mae/main.py:148`), so explicit NaN filling or invalid-pixel masking is not evidenced. Do not assume NaNs were filled with zero. |
| Q4 | Is the model output already in [0, 1] (sigmoid/clamp) or raw? | training code | Raw. The final `conv3_3` layer has no sigmoid or clamp (`experiments/net_params.py:112`; activation insertion is in `nowcasting/utils.py:31`). Evaluation clamps the output afterward at `nowcasting/evaluator.py:145`, so the forward output itself is not verified to be in [0, 1]. |
| Q5 | Are the radar sample files allowed to be published? | thesis advisor | _TBD_ — requires confirmation from the thesis advisor. |
| Q6 | Checkpoint file size; where can it be hosted? | file system | `encoder_forecaster_89000.pth` was not found. The only matching file is `outputs/encoder_forecaster_77000.pth`, measured at 50,587,234 bytes (48.24 MiB). A hosting location for the requested checkpoint is _TBD_. |

Record answers here as they are resolved.

## 5. Architecture

```
Browser ──► Next.js (UI + API routes) ──► FastAPI /predict ──► ConvLSTM (PyTorch, CPU)
                 │                                │
                 ▼                                ▼
        Prisma + PostgreSQL               sample .npz event files
   (events, forecast runs, metrics)
```

| Part | Tech | Responsibility |
|---|---|---|
| `apps/web` | Next.js (App Router), TypeScript strict, Tailwind, Prisma, Zod, Vitest | UI, input validation, calling the inference service, persisting runs |
| `services/inference` | FastAPI, Pydantic, PyTorch (CPU), NumPy, pytest | load model once, preprocess, predict, compute metrics, render frames |
| Database | PostgreSQL | events metadata and forecast run metrics |
| Local run | Docker Compose | `web` + `api` + `db` |
| CI | GitHub Actions | lint, type-check, tests, build for both apps |

**Design decisions**
- The ML model lives in its own service so the web app stays light and the model can be replaced independently.
- Event radar files live **with the inference service**; the database only stores event metadata. They share a stable `slug` (e.g. `2023-05-14-heavy-cell`).
- Frames are returned in the HTTP response and **not persisted**; the database stores metrics only. (Keeps DB small; re-run to see frames.)

## 6. Repository layout

```
raincast/
  AGENTS.md
  README.md
  docs/PROJECT.md  docs/RULES.md
  docker-compose.yml
  .env.example
  .github/workflows/ci.yml
  apps/web/
    prisma/schema.prisma  prisma/seed.ts
    src/app/                 # pages + route handlers
    src/lib/                 # zod schemas, api client, small helpers
    src/**/*.test.ts
  services/inference/
    app/main.py              # FastAPI app, routes
    app/model.py             # ConvLSTM architecture (copied from thesis code)
    app/preprocess.py        # dBZ <-> normalised, Z-R
    app/metrics.py           # CSI, POD, FAR, BIAS
    app/render.py            # colormap -> PNG base64
    app/schemas.py           # Pydantic models
    data/events/*.npz        # curated samples (only if publishing is allowed)
    tests/
    requirements.txt
```

## 7. Data contract

### 7.1 Event file (`data/events/<slug>.npz`)
- `input`: float32 `(6, 360, 360)`, normalised [0, 1]
- `target`: float32 `(6, 360, 360)`, normalised [0, 1]
- Optional: store as uint8 (`round(x*255)`) to shrink files; if so, dequantise on load and verify CSI changes by < 0.01.

### 7.2 Inference API (FastAPI)

`GET /health` → `{ "status": "ok", "modelLoaded": true, "modelVersion": "convlstm-89000" }`

`POST /predict`
```jsonc
// request
{ "eventId": "2023-05-14-heavy-cell" }

// response 200
{
  "eventId": "2023-05-14-heavy-cell",
  "modelVersion": "convlstm-89000",
  "thresholdMmPerHour": 10,
  "leadMinutes": [10, 20, 30, 40, 50, 60],
  "frames": {                       // base64 PNG, 360x360, colour-mapped dBZ
    "observed":    ["<b64>", "..."],   // 6 items (target frames)
    "convlstm":    ["<b64>", "..."],   // 6 items
    "persistence": ["<b64>", "..."]    // 6 items
  },
  "metrics": {
    "convlstm":    { "csi": [..6], "pod": [..6], "far": [..6], "bias": [..6] },
    "persistence": { "csi": [..6], "pod": [..6], "far": [..6], "bias": [..6] }
  },
  "latencyMs": 2340
}
// errors: 404 unknown eventId · 422 invalid body · 503 model not loaded
```
A metric is `null` when its denominator is 0 (e.g. no heavy rain in a frame). Never return NaN.

### 7.3 Web API (Next.js route handlers)

| Route | Body / Params | Result |
|---|---|---|
| `GET /api/events` | — | list of `RadarEvent` |
| `GET /api/events/:slug` | — | one event |
| `POST /api/forecasts` | `{ eventId }` (Zod) | calls FastAPI, saves run, returns frames + metrics + run id |
| `GET /api/forecasts?eventId=` | optional filter | saved runs (metrics only), newest first |

Errors use a single JSON shape: `{ "error": { "code": "string", "message": "string" } }`.

### 7.4 Database (Prisma)

```prisma
model RadarEvent {
  id          String     @id @default(cuid())
  slug        String     @unique
  name        String
  startTime   DateTime
  description String?
  forecasts   Forecast[]
}

model Forecast {
  id           String     @id @default(cuid())
  eventId      String
  event        RadarEvent @relation(fields: [eventId], references: [id], onDelete: Cascade)
  modelVersion String
  latencyMs    Int
  csiConvlstm  Json       // number|null [6]
  csiPersist   Json       // number|null [6]
  createdAt    DateTime   @default(now())

  @@index([eventId, createdAt])
}
```
Events are seeded from `prisma/seed.ts` using a manifest of slugs, names, start times.

## 8. Metric definitions

Applied per lead time on the 360×360 grid, ignoring invalid pixels. Convert normalised → dBZ → R (Z–R Singapore), then binarise with **R ≥ 10 mm/h**.

- `hits H` = forecast yes & observed yes · `misses M` = forecast no & observed yes · `false alarms F` = forecast yes & observed no
- **CSI** = H / (H + M + F) · **POD** = H / (H + M) · **FAR** = F / (H + F) · **BIAS** = (H + F) / (H + M)

## 9. UI requirements

1. **Events page:** cards with name, date, description.
2. **Event page:** "Run forecast" button; loading state (inference can take seconds); slider t+10…t+60; three panels (Observed / ConvLSTM / Persistence) with a colour legend; CSI-vs-lead-time line chart for both models; visible disclaimer "Research demo".
3. **History page:** table of saved runs (event, time, latency, CSI at t+30).
4. Responsive, keyboard-accessible slider, clear error and empty states.

## 10. Testing strategy

| Layer | Tool | What is tested |
|---|---|---|
| Web unit | Vitest | Zod schemas, metric formatting helpers, route handlers with FastAPI mocked |
| API unit | pytest | dBZ round-trip, Z–R conversion, CSI/POD/FAR on hand-made arrays, `/predict` shape and status codes |
| Model smoke | pytest | tiny **randomly initialised** model with the real architecture: output shape `(6, 360, 360)` and range |
| Manual/local | real checkpoint | reproduce plausible CSI behaviour (see acceptance below) |

CI never needs the real checkpoint or real radar data.

## 11. CI and deployment

- **CI (GitHub Actions), on every push and PR:** job `web` (install, lint, `tsc --noEmit`, Vitest, `next build`) and job `api` (install, ruff, pytest).
- **Local:** `docker compose up` starts web, api, db.
- **Deploy:** web on Vercel, database on Neon, inference on a host with enough RAM for PyTorch on CPU (e.g. a Docker-based host; verify current free-tier limits). If no host works, do not claim "deployed" — publish a demo video instead.

## 12. Milestones and acceptance criteria

| # | Milestone | Done when |
|---|---|---|
| M0 | Answer open questions Q1–Q6 | table in §4 filled |
| M1 | Inference service | `/predict` returns valid output for one event with the real checkpoint; pytest green |
| M2 | Metrics correct | hand-made metric tests pass; on sample events CSI generally decreases with lead time; if the thesis test set is available locally, aggregate CSI is close to the thesis values in §3 |
| M3 | Web + DB | events listed; run saved to PostgreSQL; history page works |
| M4 | UI | slider, three panels, chart, disclaimer |
| M5 | Quality | tests for both apps, Docker Compose works from a clean clone, CI green |
| M6 | Release | deployed (or demo video), README with architecture diagram and screenshots |

## 13. Risks

| Risk | Mitigation |
|---|---|
| Not allowed to publish radar data | publish precomputed outputs for a few events, or keep the demo private |
| Checkpoint too large / no free RAM for PyTorch | quantise/prune only if metrics are re-verified; otherwise demo video |
| Preprocessing mismatch → wrong forecasts | tests for §3 formulas; answer Q3/Q4 first |
| Scope creep | §2 "Out of scope" is binding |
| Owner cannot explain the code in interviews | learning-mode rules in `AGENTS.md` |

## 14. Glossary

- **Nowcasting:** very short-range forecast (here 0–60 min).
- **dBZ:** radar reflectivity in decibels.
- **Z–R relation:** formula converting reflectivity to rain rate.
- **CSI / POD / FAR / BIAS:** categorical forecast scores (see §8).
- **Persistence:** baseline that assumes the last observation stays unchanged.
- **Lead time:** how far ahead the forecast is (t+10 … t+60 min).