---
name: raincast-dev
description: "Use this skill whenever a task touches RainCast or related radar nowcasting, ConvLSTM checkpoints, /predict, CSI/POD/FAR/BIAS, dBZ normalisation, Z-R rainfall conversion, Prisma events or forecasts, Next.js forecast UI, Docker Compose, GitHub Actions, FastAPI, or interview preparation about the project or thesis. Trigger proactively even when the user does not say RainCast; keep implementation, evidence, and interview claims honest."
argument-hint: "Describe the RainCast task, affected area, and expected behavior."
user-invocable: true
---

# RainCast Development

Build, test, debug, review, and explain RainCast one small milestone slice at a time. The owner is a fresher preparing for interviews, so every decision must be simple enough to explain and every claim must be backed by evidence.

## Source of Truth

1. Read `AGENTS.md`, `docs/PROJECT.md`, and `docs/RULES.md` before non-trivial work. If a file is missing, say so and ask the owner before filling its contract from memory.
2. Treat the repository's current code and those documents as authoritative. Use [domain facts](./references/domain.md), [API notes](./references/api-contract.md), and [checklists](./references/checklists.md) as quick references, not permission to override the project contract.
3. Identify the milestone, files to touch, one local hypothesis, and one cheap check that could disconfirm it before editing.

## Protected Decisions

Ask the owner first when a change affects an API contract, Prisma schema, preprocessing formula, metric definition, model architecture or weights, raw radar data, sample-event permission, or open questions Q1-Q6. The reason is reproducibility: a plausible guess can silently change scientific results or break the web-service contract.

Do not add `.env` files, secrets, `.pth` checkpoints, raw radar data, arbitrary uploads, authentication, live ingestion, training, or payments. These boundaries keep the portfolio demo reproducible and prevent sensitive or oversized artifacts from entering Git.

## Domain Invariants

Use the exact formulas in [domain.md](./references/domain.md):

- `x = (clip(dBZ, -10, 60) + 10) / 70`
- `R = (10^(dBZ/10) / 61.75)^(1/1.61)`
- Heavy rain is `R >= 10 mm/h`, approximately `34 dBZ` or `0.629` normalised.
- Lead times are 10, 20, 30, 40, 50, and 60 minutes.
- `CSI = H / (H + M + F)`
- `POD = H / (H + M)`
- `FAR = F / (H + F)`
- `BIAS = (H + F) / (H + M)`
- A zero denominator is `null`, never `NaN`.
- Persistence repeats the last input frame at every lead time.

The app serves the ConvLSTM baseline. Never attribute the thesis U-Net + Transformer score `CSI 0.291` to it. Never invent metrics, latency, coverage, test counts, deployment status, or model results; use `TBD` or run the check.

## Implementation Workflow

1. Restate the behavior and milestone. List the files likely to change.
2. Read the nearest implementation, caller, test, and applicable contract section.
3. For metric, preprocessing, schema, or parsing logic, write a deterministic regression test first using hand-made arrays or a tiny model. Tests must not require the real checkpoint or radar data.
4. Make the smallest conventional edit. Use environment variables `MODEL_PATH`, `INFERENCE_URL`, and `DATABASE_URL`; validate external input with Zod or Pydantic; keep database access in server code through Prisma.
5. Validate the touched slice immediately. Then run all required checks for every touched stack area. Report the actual command and result; name unavailable checks rather than claiming success.
6. Update `docs/PROJECT.md` in the same change if an API, schema, or scope contract changed.
7. Finish using [the definition-of-done checklist](./references/checklists.md) and the learning-mode response below.

For inference code, load the model once at startup, call `model.eval()`, and use `torch.no_grad()` because request-time model loading is slow and inference should not build training graphs. For web code, prefer Server Components and use `"use client"` only for interaction; use Zod at external boundaries because TypeScript types do not validate runtime data.

## Learning Mode

After every code or configuration change, reply with:

1. **What changed:** files and behavior in plain language.
2. **Why:** the shortest defensible reason.
3. **How to verify:** exact commands and their real output or an explicit unverified blocker.
4. **Concept notes:** explain each new concept in two or three lines.
5. **Three interview questions:** questions the owner should be able to answer about this change.

## Interview Prep Mode

When the user asks for interview preparation, use [the question bank](./references/interview-qa.md). Generate mock questions and honest model answers about the thesis, ConvLSTM baseline, balanced loss, CSI/POD/FAR, division of work, separate inference service, Prisma/PostgreSQL, Zod, FastAPI, Docker, and CI.

Keep the owner's role precise: literature review, data collection, and ConvLSTM baseline training. Do not claim ownership of work the owner has not stated. Clearly distinguish thesis facts, repository facts, and unknowns that require the owner's answer.

## UI, API, and Operations Guardrails

Every forecast view must show exactly: `Research demo - not an operational weather forecast.` Use the hyphen in generated text when the product contract requires ASCII; preserve an existing typographic dash only when matching existing UI copy.

Validate `eventId` against known slugs and never build file paths from raw input. Set web-to-inference timeouts and return clear 503/504 errors. FastAPI request and response models use Pydantic; web route bodies, query parameters, and inference responses use Zod. Keep loading, empty, and error states in data-fetching UI.

For Docker and CI, pin base images, use the required multi-stage web build, keep `.env.example` usable from a clean clone, and run web lint, type-check, tests, and build plus API lint and tests. Never disable or skip a failing check to make CI green.

## Test Prompts

Use the realistic prompts in `tests/prompts.md` to review whether this skill changes agent behavior. The expected guardrails and comparison rubric are in that file. The skill package contains no fabricated model transcripts: this environment cannot invoke an isolated skill with and without loading it, so record any live comparison only when the platform provides that harness.

## Progressive References

- [domain.md](./references/domain.md): formulas, thresholds, lead times, baselines, and evidence boundaries.
- [api-contract.md](./references/api-contract.md): known service boundaries and unresolved contract questions.
- [interview-qa.md](./references/interview-qa.md): honest question-and-answer bank.
- [checklists.md](./references/checklists.md): implementation, definition-of-done, and pre-deploy checks.
- [check_metrics.py](./scripts/check_metrics.py): small standard-library helper with self-tests for metric math.
