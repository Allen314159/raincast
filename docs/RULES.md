# RainCast — Engineering Rules

> These rules apply to humans and AI agents alike. If a rule blocks you, ask the owner instead of working around it.

## 1. Honesty and evidence (highest priority)

1. **Never invent numbers.** Metrics, latency, test counts, coverage, and model scores in code, README, CV, or UI must come from a real run. If unknown, write "TBD".
2. **Never confuse models.** This project serves the **ConvLSTM baseline**. The thesis U-Net + Transformer model (CSI 0.291) is not part of this repo. Do not attach its numbers to the baseline.
3. **Never claim what is not true.** "Deployed", "tested", "CI passing" are only written after they are verified.
4. **Do not guess unknowns.** Model layout, NaN handling and similar details are listed as open questions in `docs/PROJECT.md` §4. Ask; do not assume.
5. Every page showing forecasts must display: *"Research demo — not an operational weather forecast."*

## 2. Data, model and licensing

1. Do not commit raw radar data, the `.pth` checkpoint, `.env` files, or secrets. Use `.gitignore`.
2. Sample event files may be added to the repo **only** after the owner confirms permission (PROJECT.md Q5), and only the curated events, never bulk data.
3. Model path and inference URL come from environment variables (`MODEL_PATH`, `INFERENCE_URL`). No hard-coded paths.
4. Preprocessing formulas must match the thesis exactly (PROJECT.md §3). Changing them requires a test and the owner's approval.
5. Load the model **once at startup**, not per request. Use `model.eval()` and `torch.no_grad()` for inference.

## 3. Code style

### TypeScript / Next.js (`apps/web`)
- `strict: true`. No `any` (use `unknown` and narrow). No `@ts-ignore` without a comment explaining why.
- Validate **all** external input with Zod (request bodies, query params, and the FastAPI response).
- Prefer Server Components; use `"use client"` only when interactivity requires it.
- Database access only through Prisma, only in server code. No raw SQL unless justified in a comment.
- Files: `kebab-case.ts`; components `PascalCase.tsx`; one main export per file.
- Handle loading, empty and error states in every data-fetching UI.

### Python / FastAPI (`services/inference`)
- Type hints on all functions. Pydantic models for every request and response.
- Format and lint with `ruff`. Keep functions small and pure where possible (`preprocess`, `metrics`, `render` have no I/O).
- No global mutable state except the loaded model.
- Return proper HTTP status codes (404, 422, 503). Never return NaN in JSON — use `null`.

### General
- Prefer simple, conventional code over clever code. The owner must be able to explain every line.
- No new dependency without a one-line justification in the PR/commit message.
- No dead code, no commented-out blocks, no TODOs without an issue or owner note.
- Comments explain **why**, not what.

## 4. Testing rules

1. Every new function with logic gets a test. Bug fixes get a regression test first.
2. Tests must be deterministic and fast. CI must not need the real checkpoint or real radar data — use a tiny randomly initialised model and hand-made arrays.
3. Metric functions are tested with hand-computed examples (including zero-denominator cases → `null`).
4. Web route handlers are tested with the FastAPI service mocked.
5. A change is not "done" if tests, lint, or type-check fail.

## 5. Git and review

- Branches: `feat/…`, `fix/…`, `docs/…`, `chore/…`. Never commit directly to `main`.
- Conventional Commits: `feat(web): add lead-time slider`, `fix(api): handle empty heavy-rain mask`.
- Small, focused PRs (one milestone slice). PR description: what, why, how tested, screenshots for UI.
- CI must be green before merge.

## 6. Security and reliability

- Never log secrets or full request bodies. No secrets in client code (`NEXT_PUBLIC_*` is public).
- Set request timeouts on the web → API call and return a clear error (`504`/`503`).
- Validate `eventId` against known slugs; never build file paths from raw user input (prevent path traversal).
- Limit payload sizes; no arbitrary file upload in the MVP.

## 7. Docker and CI

- One Dockerfile per app; pin base image versions; use multi-stage builds for the web app.
- `docker compose up` must work from a clean clone using `.env.example`.
- CI runs on every push and PR: web (lint, `tsc --noEmit`, Vitest, `next build`) and api (ruff, pytest).
- Do not disable or skip failing checks to get green.

## 8. Documentation

- README: what it is, architecture diagram, screenshots, how to run (Docker and without), how to test, limitations.
- Keep `docs/PROJECT.md` updated when the API, schema, or scope changes — in the same PR as the code.
- Limitations section is mandatory (baseline model only, over-prediction of heavy rain: BIAS 2.35 on the thesis test set, forecasts blur at long lead times).

## 9. Definition of Done (per task)

- [ ] Behaviour matches `docs/PROJECT.md`
- [ ] Tests added/updated and passing locally
- [ ] Lint and type-check pass
- [ ] No secrets, data, or checkpoint committed
- [ ] Docs updated if contract/scope changed
- [ ] No invented numbers or unverified claims
- [ ] Owner can explain the change (see learning mode in `AGENTS.md`)