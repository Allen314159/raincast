# AGENTS.md — RainCast

Instructions for AI coding agents (Claude Code, Cursor, Codex, Copilot, etc.). Read this file first, every session.

## What this project is

RainCast is a small full-stack app that shows heavy-rain forecasts (10–60 min) over Ho Chi Minh City from radar data. It serves a **ConvLSTM baseline model** trained in the owner's undergraduate thesis (Nha Be radar, 360×360 grid, 6 input frames → 6 forecast frames) and compares it with a persistence baseline.

- Owner: Lam My Trang (fresher; this repo is a portfolio project used in job interviews).
- Full spec: `docs/PROJECT.md` · Rules: `docs/RULES.md`. **Read both before non-trivial work.**

## Stack and layout

| Path | Tech |
|---|---|
| `apps/web` | Next.js (App Router), TypeScript strict, Tailwind, Prisma, Zod, Vitest |
| `services/inference` | FastAPI, Pydantic, PyTorch (CPU), NumPy, pytest, ruff |
| Database | PostgreSQL (Prisma) |
| Infra | Docker Compose, GitHub Actions |

## Commands (update if scripts change)

```bash
# web
cd apps/web
npm ci
npm run lint && npx tsc --noEmit
npm test                 # Vitest
npx prisma migrate dev   # apply migrations
npx prisma db seed       # seed events
npm run dev

# inference
cd services/inference
pip install -r requirements.txt
ruff check . && ruff format --check .
pytest
uvicorn app.main:app --reload --port 8000

# whole stack
docker compose up --build
```

Before saying a task is done, run the lint, type-check and test commands for every part you touched, and report the real results.

## Boundaries

### Always
- Follow `docs/RULES.md` and match the contracts in `docs/PROJECT.md` (§7 API, schema, metrics).
- Write or update tests with the code.
- Use env vars for paths/URLs (`MODEL_PATH`, `INFERENCE_URL`, `DATABASE_URL`).
- Keep changes small and on topic. One milestone slice per PR.
- Say clearly when something is unverified or unknown.

### Ask the owner first
- Adding a dependency or changing the stack.
- Changing the API contract, DB schema, preprocessing formulas, or metric definitions.
- Anything touching model architecture/weights.
- Adding any radar data file to the repo.
- Anything in `docs/PROJECT.md` §4 (Open questions) — do **not** guess Q1–Q6.

### Never
- Invent metrics, latencies, test counts, or results. Write "TBD" instead.
- Attribute the thesis U-Net + Transformer results (CSI 0.291) to this ConvLSTM baseline.
- Commit secrets, `.env`, the `.pth` checkpoint, or raw radar data.
- Build features listed as out of scope (auth, live ingestion, training, payments).
- Disable, skip, or weaken tests/lint/CI to make something pass.
- Use `any`, `@ts-ignore` without justification, or raw file paths from user input.
- Rewrite unrelated files or reformat the whole repo.

## Domain facts you must get right

- Normalisation: `x = (clip(dBZ, −10, 60) + 10) / 70`. Inverse: `dBZ = 70·x − 10`.
- Z–R (Singapore): `R = (10^(dBZ/10) / 61.75)^(1/1.61)`.
- Heavy rain: R ≥ 10 mm/h ≈ 34.0 dBZ ≈ 0.629 normalised.
- Lead times: 10, 20, 30, 40, 50, 60 minutes (6 frames).
- Metrics per lead time: CSI = H/(H+M+F), POD = H/(H+M), FAR = F/(H+F), BIAS = (H+F)/(H+M). Zero denominator → `null`, never NaN.
- Persistence = repeat the last input frame (t0) for all 6 lead times.
- Every forecast UI shows: "Research demo — not an operational weather forecast."

## Learning mode (important)

The owner must be able to explain **every line** in an interview. Therefore:

1. Prefer simple, conventional code. No clever abstractions, no heavy libraries for small jobs.
2. After each change, reply with:
   - **What changed** (files, in plain language)
   - **Why** (the reasoning, one short paragraph)
   - **How to verify** (exact commands) and the real result
   - **3 interview questions** the owner should be able to answer about this change
3. When you introduce a concept (Server Components, Zod, Prisma relations, `torch.no_grad`, async FastAPI, Docker layers, CI jobs), add a 2–3 line explanation in your reply.
4. If a request is ambiguous, ask one focused question instead of guessing.
5. Do not generate large amounts of code in one step. Work milestone by milestone (`docs/PROJECT.md` §12) so the owner can review and learn.

## Workflow

1. Restate the task and the milestone it belongs to.
2. List the files you will touch.
3. Write tests first for logic (metrics, preprocessing, schemas).
4. Implement the smallest change that satisfies the spec.
5. Run lint, type-check, tests; fix failures properly.
6. Update `docs/PROJECT.md` if a contract changed.
7. Summarise using the learning-mode format above.

## Commit style

Conventional Commits, e.g. `feat(api): add /predict endpoint`, `test(api): cover CSI zero-denominator`, `docs: fill open question Q2`.