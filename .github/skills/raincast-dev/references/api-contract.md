# RainCast API and Data Boundaries

This reference records only contracts supplied by the repository rules and task brief. The authoritative route payloads and Prisma schema belong in `docs/PROJECT.md`; if that document is unavailable, ask the owner rather than inventing fields.

## Service Boundary

- Web: Next.js with TypeScript strict, Prisma, Zod, and PostgreSQL.
- Inference: FastAPI with Pydantic, PyTorch, NumPy, and CPU inference.
- Web-to-inference URL comes from `INFERENCE_URL`.
- Model location comes from `MODEL_PATH`.
- Database URL comes from `DATABASE_URL`.
- The inference model loads once at startup, uses `model.eval()`, and runs inference under `torch.no_grad()`.

## `/predict`

The project identifies `/predict` as the inference endpoint. Do not invent its exact request or response shape. Confirm the route, six-frame tensor layout, event identifier, error payload, and forecast serialization in `docs/PROJECT.md` or the implementation before editing.

Expected operational behavior from the rules:

- Validate request and response data with Pydantic at the FastAPI boundary.
- Return 422 for invalid input, 404 for an unknown event, and 503 when the model is unavailable. A web timeout should surface as a clear 504/503 response.
- Do not return NaN in JSON; represent undefined metric values as `null`.

## Web and Persistence

The Next.js forecast UI must handle loading, empty, and error states and display `Research demo - not an operational weather forecast.` Database access stays in server code through Prisma. External request bodies, query parameters, and inference responses are validated with Zod.

The task brief mentions Prisma entities for events and forecasts, but does not provide their columns, relations, indexes, or migration names. Ask before changing the schema. Do not use raw SQL unless the project contract explicitly justifies it.

## Unknowns

Do not guess model layout, NaN handling beyond the JSON rule, event file permissions, exact route payloads, or open questions Q1-Q6. Record the question and pause the protected change until the owner answers.
