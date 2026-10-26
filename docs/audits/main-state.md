# Main state audit

This audit records the state of `main` and the known Phase 1 issues. Evidence
paths and line numbers refer to the branch state checked for this phase.

| ID | Status | Evidence | Finding |
|---|---|---|---|
| H1 | OPEN | `services/inference/app/main.py:52-75`; `services/inference/data/events/` | The loader expects `.npz` events, but no usable event file is present in the repository. |
| H2 | OPEN | `services/inference/app/main.py:26`; `services/inference/tests/test_health.py:13` | The default model version is `convlstm-89000`, while the local checkpoint is 77000. |
| M1 | OPEN | `apps/web/app/api/forecasts/route.ts:27,63` | POST resolves a slug to a database ID; GET uses the query value directly as the database `eventId`. |
| M2 | OPEN | `services/inference/app/metrics.py:10-13`; `services/inference/app/main.py:102-104` | Metrics default to an all-ones validity mask; the documented invalid-pixel contract is not implemented. |
| M3 | OPEN | `services/inference/app/metrics.py:47-58` | `zip` truncates mismatched forecast and observed sequences without reporting the mismatch. |
| M4 | OPEN | `apps/web/app/api/forecasts/route.ts:42-52,62-67` | Database create and read failures are not mapped to the standard error shape. |
| M5 | OPEN | `apps/web/app/api/forecasts/route.ts:34-39,115-117`; `apps/web/src/lib/schemas.ts` | The response event ID is parsed and returned, but is not checked against the requested event. |
| L1 | OPEN | `apps/web/prisma/events.json:2-18` | Seed data contains three placeholder events and fake descriptions. |
| L2 | OPEN | `services/inference/app/model.py:58-76,221-235` | The `activation` and `Predictor` helpers are not used by `build_model` or the service path. |
| L3 | OPEN | `README.md:3-29` | README status describes only the initial scaffold and does not document the current repository surfaces. |
| L4 | OPEN | `AGENTS.md` | Agent instructions were missing before this Phase 1 change. |
| P1 | OPEN | `apps/web/prisma/schema.prisma`; no `apps/web/prisma/migrations/` directory | Prisma migrations are missing. |
| P2 | OPEN | repository root; no `docker-compose.yml` | Docker Compose is missing. |
| P3 | OPEN | `apps/web/app/page.tsx:1-7` | The UI is still a placeholder page. |
