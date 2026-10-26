# RainCast

RainCast is a research-demo monorepo for a Next.js web app and a FastAPI
inference service. It is not an operational weather forecast.

## Status

The repository currently has a buildable Next.js app with a placeholder home
page, API route code and Prisma schema, plus a FastAPI service with a health
endpoint and unit-tested inference helpers. The web checks (tests, lint,
type-check and production build) and inference checks (ruff and pytest) pass in
the current local environment.

The following are not available yet: a finished UI, usable real event files,
Prisma migrations, Docker Compose, deployment, and a verified end-to-end run
with a real event and checkpoint. The seeded event manifest still contains
placeholders. See [docs/PROJECT.md](docs/PROJECT.md) and
[docs/audits/main-state.md](docs/audits/main-state.md) for the scope and
evidence.

## Run the web app

```bash
cd apps/web
npm ci
npm run dev
```

Run its checks with:

```bash
npm run lint
npm run typecheck
npm test
npm run build
```

## Run the inference service

```bash
cd services/inference
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Run its checks with:

```bash
ruff check .
pytest
```