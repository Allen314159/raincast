# RainCast — Build Plan with Prompts

> How to use: work **one phase at a time**. For each phase: (1) attach the listed files, (2) paste the **Common header** followed by the phase prompt into your AI agent (Claude Code, Cursor, etc.), (3) run the checks yourself, (4) do the **Review ritual** before moving on.
> Total: about 17–20 working days. Don't skip the reviews: they are what lets you explain the project in an interview.

## Progress tracker

- [ ] Phase 0 — Prepare (answer open questions)
- [ ] Phase 1 — Repo scaffold, lint, CI skeleton
- [ ] Phase 2 — Inference core: preprocessing, metrics, rendering
- [ ] Phase 3 — Model loading and `/predict`
- [ ] Phase 4 — Database, Prisma, web API routes
- [ ] Phase 5 — UI
- [ ] Phase 6 — Docker Compose, tests, full CI
- [ ] Phase 7 — Deploy, README, demo
- [ ] Phase 8 — CV update and interview prep

| Phase | Days | Milestone (PROJECT.md §12) |
|---|---|---|
| 0 | 1–2 | M0 |
| 1 | 1 | — |
| 2 | 2 | M2 (part) |
| 3 | 3 | M1, M2 |
| 4 | 3 | M3 |
| 5 | 3 | M4 |
| 6 | 2 | M5 |
| 7 | 2–3 | M6 |
| 8 | 1–2 | — |

---

## Common header (paste before EVERY phase prompt)

```text
You are working on the RainCast project. First read AGENTS.md, docs/RULES.md and docs/PROJECT.md in the repo (attached) and follow them strictly.

Constraints for this session:
- Do only the phase described below. Do not build features from later phases or anything listed as out of scope.
- Do not guess open questions (PROJECT.md section 4). If a needed answer is missing, ask me.
- Do not invent numbers or results. Run the real commands and report their real output.
- Use learning mode: keep code simple; after finishing, tell me what changed, why, how to verify, 3 interview questions about this change, and a 2-3 line explanation of every new concept you used.
- Work in small steps. List the files you will create/change BEFORE writing code.
```

## Review ritual (after EVERY phase)

1. Run the phase's verification commands yourself and read the output.
2. Read every changed file. Delete anything you cannot explain, or ask the agent to explain it or simplify it.
3. Answer the agent's 3 interview questions out loud, without looking.
4. Commit with a Conventional Commit message on a `feat/...` branch, open a PR, wait for CI, merge.
5. Tick the tracker above and write 3–5 lines in a personal `notes.md`: what you learned, what confused you.

---

## Phase 0 — Prepare (answer open questions)

**Goal:** know exactly how your trained model expects its input, before any code is written. Fill PROJECT.md §4 (Q1–Q6).
**Attach:** your thesis training code for the ConvLSTM (model class, dataset/preprocessing, training script), `AGENTS.md`, `docs/PROJECT.md`.
**Also do yourself:** ask your advisor whether sample radar files may be published (Q5); check the checkpoint size (Q6).

```text
[Common header]

PHASE 0 — Answer the open questions.
I attached my thesis training code for the ConvLSTM baseline (checkpoint encoder_forecaster_89000.pth).
Read it and answer PROJECT.md section 4 questions Q1-Q4 with evidence:
- Q1: exact model class, constructor arguments, and where the class is defined
- Q2: the input tensor layout and dtype the model expects, with an example shape
- Q3: how NaN/invalid pixels are handled before training
- Q4: whether model output is already in [0,1] or raw

For each answer quote the file and line/function it comes from. If the code does not answer something, say "not found" instead of guessing, and tell me what I should check.
Then output a minimal Python snippet (no dependencies except torch/numpy) that loads the checkpoint on CPU and runs one forward pass on a random tensor, and print the output shape. Do not modify the repo files; give me the snippet and the filled-in table for PROJECT.md section 4.
```

**Done when:** Q1–Q4 filled with evidence; the snippet runs on your machine and prints an output shape of 6 frames.
**Learn:** what an encoder–forecaster is, tensor layouts, `map_location`, `state_dict`.

---

## Phase 1 — Repo scaffold, lint, CI skeleton

**Goal:** an empty but correct monorepo where lint, type-check and (empty) tests run in CI from the first commit.
**Attach:** `AGENTS.md`, `docs/PROJECT.md`, `docs/RULES.md`.

```text
[Common header]

PHASE 1 — Repository scaffold.
Create the monorepo layout from PROJECT.md section 6:
- apps/web: Next.js (App Router) + TypeScript strict + Tailwind + ESLint + Vitest configured, one trivial passing test, one placeholder home page.
- services/inference: FastAPI app with GET /health only (returns status ok, modelLoaded false for now), requirements.txt, ruff config, pytest with one passing test for /health using TestClient.
- Root: .gitignore (must exclude .env, *.pth, node_modules, __pycache__, data files except placeholders), .env.example (DATABASE_URL, INFERENCE_URL, MODEL_PATH), README.md (title + one paragraph + how to run each part; no invented claims).
- .github/workflows/ci.yml with two jobs: web (npm ci, lint, tsc --noEmit, vitest, next build) and api (pip install, ruff, pytest). Run on push and pull_request.

Do NOT add Prisma, Docker, or any feature yet. Use the newest stable versions but tell me which versions you chose. Then run every lint/type-check/test command and paste real output.
```

**Verify:** `npm test`, `npx tsc --noEmit`, `pytest`, `ruff check .`; push a branch and see both CI jobs green.
**Learn:** monorepo, what each CI step does, `pytest` `TestClient`, why `strict` TypeScript.

---

## Phase 2 — Inference core: preprocessing, metrics, rendering

**Goal:** pure, fully tested functions. No model yet. This is where correctness lives.
**Attach:** `AGENTS.md`, `docs/PROJECT.md` (§3, §8), `docs/RULES.md`, the answers to Q3/Q4.

```text
[Common header]

PHASE 2 — Pure functions in services/inference/app.
Implement with type hints and pytest tests (write tests first):

1. preprocess.py
   - normalise(dbz) : x = (clip(dbz, -10, 60) + 10) / 70
   - denormalise(x) : dbz = 70*x - 10
   - dbz_to_rain_rate(dbz) : R = (10**(dbz/10) / 61.75) ** (1/1.61)   (Singapore Z-R)
   - heavy_rain_mask(x_normalised, threshold_mm_h=10) : boolean array
   Tests: round-trip on values inside [-10,60]; clipping outside; R at 34 dBZ is about 10 mm/h (tolerance 0.1); threshold 0.629 normalised corresponds to 10 mm/h.

2. metrics.py
   - contingency(forecast_mask, observed_mask, valid_mask=None) -> hits, misses, false_alarms
   - csi, pod, far, bias -> float or None (None when denominator is 0; never NaN)
   - per_lead_metrics(forecast[6,H,W], observed[6,H,W]) -> dict with lists of 6 values each
   Hand-made test: forecast [[1,1],[0,0]], observed [[1,0],[1,0]] => hits=1, misses=1, false_alarms=1, CSI=1/3, POD=0.5, FAR=0.5, BIAS=1. Also test all-zero masks => None.

3. render.py
   - frame_to_png_base64(x_normalised[H,W]) -> base64 PNG string using a standard radar-like colour map on dBZ, transparent/neutral for very low values. Test: output decodes to a 360x360 PNG.

Rules: functions are pure (no I/O, no globals). Use NumPy only (plus Pillow for PNG if needed; justify it). Explain each formula in a docstring in one line. Run ruff and pytest and paste the real output.
```

**Verify:** `pytest -v` shows the hand-made metric test and the Z–R test passing.
**Learn:** contingency table, CSI/POD/FAR/BIAS meaning, why zero denominators return `None`, dBZ vs rain rate.

---

## Phase 3 — Model loading and `/predict`

**Goal:** the real checkpoint produces forecasts through an HTTP endpoint. Tests use a tiny random model.
**Attach:** `AGENTS.md`, `docs/PROJECT.md`, `docs/RULES.md`, the model class file (from Q1), Q1–Q4 answers. Have 1–2 sample `.npz` events ready locally (do **not** commit them).

```text
[Common header]

PHASE 3 — Model loading and /predict in services/inference.
Inputs I provide: the model class (app/model.py, copied from my thesis code), and the answers to Q1-Q4 in PROJECT.md section 4.

Implement:
1. Model loading once at startup (FastAPI lifespan) from MODEL_PATH, on CPU, model.eval(). /health reports modelLoaded and modelVersion. If MODEL_PATH is missing, the service still starts and /predict returns 503.
2. An event loader: read data/events/<slug>.npz (arrays 'input' and 'target', each (6,360,360), normalised). Validate eventId against the list of files that exist (whitelist). Never build a path from raw input. Unknown id => 404.
3. POST /predict as specified in PROJECT.md section 7.2: run inference with torch.no_grad(); compute persistence (repeat last input frame 6 times); compute metrics for both with the Phase 2 functions; render frames for observed/convlstm/persistence; measure latencyMs. Pydantic request/response models in schemas.py. No NaN in JSON.
4. Tests (pytest): use a tiny randomly initialised model that has the SAME class but small channel sizes if possible, or monkeypatch the model with a stub returning the right shape. Tests must not need the real checkpoint or real data: generate small synthetic npz files in a temp dir. Cover 200 shape, 404, 422, 503.
5. A manual script scripts/try_real.py (not a test) that loads my real checkpoint and one real event and prints per-lead CSI for ConvLSTM and persistence. Do NOT hard-code any expected numbers.

Do not add the database or the web app. Run ruff and pytest and paste real output. Tell me exactly what to run for the manual check.
```

**Verify:** `pytest`; then run `scripts/try_real.py` on a real event. Sanity: ConvLSTM CSI usually falls as lead time grows; values are within [0,1]. If the output looks like noise, the usual cause is a preprocessing/layout mismatch (recheck Q2–Q4).
**Learn:** FastAPI lifespan, Pydantic, `torch.no_grad`, why load the model once, path-traversal risk.

---

## Phase 4 — Database, Prisma, web API routes

**Goal:** the web app can list events, call the inference service, and save runs.
**Attach:** `AGENTS.md`, `docs/PROJECT.md` (§5, §7), `docs/RULES.md`.

```text
[Common header]

PHASE 4 — Database and web API in apps/web.
1. Prisma with PostgreSQL: implement the schema from PROJECT.md section 7.4 (RadarEvent, Forecast). Create the first migration. Add prisma/seed.ts that seeds events from a small events manifest JSON (slug, name, startTime, description); use 3 placeholder events with obviously fake descriptions that I will replace.
2. src/lib/schemas.ts: Zod schemas for (a) the POST /api/forecasts body, (b) the FastAPI /predict response (validate it before using it), (c) the standard error shape { error: { code, message } }.
3. src/lib/inference-client.ts: function that calls INFERENCE_URL/predict with a timeout (e.g. 60 s), maps failures to clear errors (503 model unavailable, 504 timeout, 502 bad response).
4. Route handlers:
   - GET /api/events
   - GET /api/events/[slug]
   - POST /api/forecasts: validate body, find event by slug, call the inference client, save a Forecast row (modelVersion, latencyMs, csiConvlstm, csiPersist), return frames + metrics + run id.
   - GET /api/forecasts?eventId= : saved runs newest first.
5. Vitest tests: Zod schemas (valid/invalid), and each route handler with the inference client and Prisma mocked. Test the 400/404/502/503/504 paths.

Do NOT build UI pages yet (only what is needed to test the API). Explain how Prisma migrations, relations and indexes work as you go. Run lint, tsc, vitest and the migration against a local Postgres; paste real output.
```

**Verify:** local Postgres running; `npx prisma migrate dev`, `npx prisma db seed`, `npm test`; then call the routes with `curl` while the FastAPI service is running.
**Learn:** Prisma schema/migrations/seed, one-to-many relation, index purpose, Zod at trust boundaries, timeouts and error mapping.

---

## Phase 5 — UI

**Goal:** the user experience in PROJECT.md §9.
**Attach:** `AGENTS.md`, `docs/PROJECT.md` (§9), `docs/RULES.md`.

```text
[Common header]

PHASE 5 — UI in apps/web.
Build the pages from PROJECT.md section 9 using Tailwind, keeping the design clean and simple:
1. /  (events list): cards with name, date, description; link to /events/[slug].
2. /events/[slug]: "Run forecast" button that calls POST /api/forecasts; loading state (inference takes seconds); error state; a slider (native input type=range, keyboard accessible) for t+10..t+60; three panels Observed | ConvLSTM | Persistence showing the base64 PNG frames for the selected lead time, with a colour legend and metric values for that lead time; a line chart of CSI vs lead time for both models (use a small chart library or plain SVG - tell me which and why); the visible disclaimer "Research demo - not an operational weather forecast."
3. /history: table of saved runs (event, created time, latency, CSI at t+30), empty state.
Use Server Components where possible and "use client" only for the interactive parts; explain each "use client" choice. Do not add auth, extra pages, or animation libraries.
Add component/logic tests with Vitest for the pure helpers (formatting, null metric display "n/a"). Run lint, tsc, tests, next build; paste real output. Tell me how to manually check each page.
```

**Verify:** run both services locally, click through the three pages, check keyboard use of the slider, check null metrics show "n/a".
**Learn:** Server vs Client Components, data fetching, state in React, accessibility basics.

---

## Phase 6 — Docker Compose, tests, full CI

**Goal:** `docker compose up` works from a clean clone; CI covers everything.
**Attach:** `AGENTS.md`, `docs/PROJECT.md` (§10, §11), `docs/RULES.md`.

```text
[Common header]

PHASE 6 — Containers and CI hardening.
1. apps/web/Dockerfile (multi-stage, Next.js standalone output, non-root user) and services/inference/Dockerfile (pinned python slim, CPU-only PyTorch, installs from requirements.txt, non-root user). Add .dockerignore files.
2. docker-compose.yml: services db (postgres, healthcheck, named volume), api (mounts MODEL_PATH and data/events as read-only volumes, does NOT bake the checkpoint into the image), web (depends on db healthy, runs prisma migrate deploy on start or via a one-shot job - choose and explain). Everything configured through .env (copy of .env.example).
3. Review the test suites: list what is covered and what is not; add only the missing high-value tests. Report real test counts.
4. CI: keep the two jobs; add caching for npm and pip; add a job that builds both Docker images (no push). Do not require the real checkpoint or data in CI.
5. Update README with the exact run commands.

Do not deploy anything yet. Verify from a clean clone in a temp directory: cp .env.example .env, docker compose up --build, then hit /health and /api/events. Paste real output and any issues found.
```

**Verify:** a fresh clone starts with one command; CI green including the Docker build job.
**Learn:** image vs container, layers and caching, volumes, healthchecks, `depends_on`, why secrets are not baked into images.

---

## Phase 7 — Deploy, README, demo

**Goal:** a public link (or an honest demo video) and a README that sells the project.
**Attach:** `AGENTS.md`, `docs/PROJECT.md` (§11, §13), `docs/RULES.md`.
**Do yourself first:** confirm data permission (Q5); check the current free-tier limits of your chosen hosts.

```text
[Common header]

PHASE 7 — Deployment and documentation.
I want to deploy: web on Vercel, database on Neon, inference service on a host that can run PyTorch on CPU. Before writing any config:
1. Search current documentation for the free-tier RAM/CPU/disk limits of the inference host options and tell me which of them can realistically run my model (I will tell you the checkpoint size: <SIZE MB>) and image. If none can, say so and propose the fallback (local Docker + demo video) instead of pretending.
2. Then produce a step-by-step deployment guide for the option we choose: environment variables for each service, how the model file gets to the host WITHOUT committing it to git, how to run prisma migrate deploy on Neon, and CORS/URL settings between web and inference. I will do the clicking; you write the configs/commands and explain each step.
3. Improve README.md: one-paragraph pitch, architecture diagram (Mermaid), screenshots placeholders, live demo link placeholder, how to run (Docker and local), how to test, tech stack, and an honest Limitations section (baseline model only; heavy rain over-prediction, BIAS 2.35 on the thesis test set; forecasts blur at longer lead times; research demo). No invented metrics; only numbers I confirm from real runs.
Do not change application logic.
```

**Verify:** open the live URL on your phone; run a forecast; check the history page after a run.
**Learn:** env vars per environment, migrations in production, CORS, cold starts.

---

## Phase 8 — CV update and interview prep

**Goal:** the CV matches reality, and you can explain everything.
**Attach:** final `LamMyTrang_CV.tex`, README, your notes.md, the thesis PDF (or your summary of your part).

```text
[Common header — but skip the "do only this phase" parts about code; this phase is documentation and coaching only.]

PHASE 8 — CV and interview prep.
1. Update the RainCast entry in my CV (Jake's format LaTeX attached) using ONLY verified facts. Here are the real values: test counts web=<N>, api=<N>; CI green=<yes/no>; inference latency median=<X> s measured on <host>; live URL=<url>; repo=<url>. Remove any bullet I cannot back up. Keep the CV on one page.
2. Write 12 interview questions with model answers for each area: (a) my thesis (problem, ConvLSTM, balanced loss, CSI/POD/FAR, my role vs my partner's), (b) RainCast architecture (why a separate inference service, why store metrics not frames), (c) Prisma/PostgreSQL, (d) Zod and TypeScript, (e) FastAPI/PyTorch inference, (f) Docker and CI. Answers must be honest: my role in the thesis was literature review, data collection and ConvLSTM baseline training.
3. Then run a mock interview: ask me one question at a time, wait for my answer, give feedback and a better version. Start with the thesis.
```

**Done when:** CV facts are all verifiable; you can answer the thesis questions in under 2 minutes each without notes.

---

## If you get stuck

- **Forecasts look like noise:** re-verify Q2–Q4 (layout, NaN fill, output range) and the normalisation formula.
- **Agent proposes something out of scope:** paste "This violates RULES.md/PROJECT.md §2, remove it."
- **Agent output too large to review:** say "Split this into smaller steps; do only step 1."
- **You don't understand a file:** ask "Explain this file line by line, then simplify it if possible." Delete what you can't justify.