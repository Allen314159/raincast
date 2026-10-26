# RainCast agent instructions

RainCast is a research-demo monorepo for comparing a ConvLSTM radar nowcast with
observations and a persistence baseline. The web app is Next.js/TypeScript and
the inference service is FastAPI/PyTorch.

## Source of truth

Use these files in order:

1. `docs/RULES.md` — engineering and safety rules
2. `docs/PROJECT.md` — product and scientific contract
3. `docs/DECISIONS.md` — owner-approved choices
4. `docs/PLAN.md` — phase order and prompts

## Hard rules

- Never invent metrics, counts, sizes, latency, model results, or status claims.
- Do not commit radar data, checkpoints, `.env` files, secrets, or the thesis PDF.
- Never confuse the ConvLSTM baseline with the thesis U-Net + Transformer model.
- Do not guess open questions; stop and ask the owner.
- Keep changes in scope and do not weaken, skip, or delete checks.
- Use conventional commits and never commit directly to `main`.
- Add no dependency without a one-line justification in the commit and report.
- Preserve validation, error handling, timeouts, and the documented API contract.
- Every forecast view must show: "Research demo - not an operational weather forecast."

## Learning mode

Explain code when requested. Prefer simple, conventional code. The owner must
be able to explain every line that is added or changed.

## Audits

Evidence reports live in `docs/audits/`. Treat them as evidence with the trust
and limitations recorded in `docs/audits/README.md`; do not promote hypotheses
to facts without owner approval.
