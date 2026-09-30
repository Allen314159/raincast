# RainCast

RainCast is a research-demo monorepo scaffold for a Next.js web app and a FastAPI inference service. The Phase 1 scaffold contains only a placeholder web page and a health endpoint; model inference, radar data, persistence, and database features are not implemented yet.

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

The service currently exposes only `GET /health`.