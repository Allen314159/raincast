# RainCast Checklists

## Before Editing

- [ ] Restate behavior and milestone.
- [ ] Read `AGENTS.md`, `docs/PROJECT.md`, and `docs/RULES.md`, or record which is unavailable.
- [ ] List files to touch and identify the controlling code path.
- [ ] Ask before changing a protected contract or open question.
- [ ] Confirm no secret, checkpoint, raw radar data, or `.env` will be added.

## Definition of Done

- [ ] Behavior matches `docs/PROJECT.md`.
- [ ] Every new logic function has a deterministic test; bug fixes have a regression test.
- [ ] Metric tests use hand-computed examples, including zero-denominator `null` cases.
- [ ] Web input and inference responses use Zod; FastAPI input and output use Pydantic.
- [ ] Forecast pages show `Research demo - not an operational weather forecast.`
- [ ] Model is loaded once, in eval mode, under `torch.no_grad()` for inference.
- [ ] Lint, formatting, type-check, tests, and build checks were actually run for touched areas.
- [ ] No claims of deployment, CI success, metrics, coverage, or latency lack evidence.
- [ ] `docs/PROJECT.md` changed with the code if an API, schema, or scope contract changed.
- [ ] The owner can explain every changed line.

## Pre-Deploy

- [ ] `.env.example` supports a clean clone; real secrets remain outside Git.
- [ ] Docker base images are pinned and the web image uses the required multi-stage build.
- [ ] `docker compose up` was tested when the environment permits it; otherwise report the blocker.
- [ ] CI runs web lint, `tsc --noEmit`, Vitest, `next build`, API Ruff checks, and pytest.
- [ ] Event identifiers are validated against known slugs; no raw user input becomes a file path.
- [ ] Payload sizes and request timeouts are bounded.
- [ ] Loading, empty, error, 404, 422, and 503/504 states are handled where applicable.
- [ ] Research-demo disclaimer appears on every forecast view.
