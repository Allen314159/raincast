# End-to-end smoke test

The smoke script checks the inference health endpoint and the web
events/forecasts routes without printing base64 frame data. It requires Node
18 or newer, because it uses the built-in `fetch`.

With the inference service, PostgreSQL, and web app running, execute from the
repository root:

```powershell
node scripts\smoke-e2e.mjs
```

The URLs default to `http://localhost:3000` and `http://localhost:8000`. Set
`WEB_URL` and `INFERENCE_URL` to override them:

```powershell
$env:WEB_URL = "http://localhost:3000"
$env:INFERENCE_URL = "http://localhost:8000"
node scripts\smoke-e2e.mjs
```

The script exits non-zero if any check fails. It reports only response sizes,
timings, frame counts, and identifiers.

## Manual failure checks

Do not automate stopping services. Keep the web app and database running while
stopping only the inference service, then send a valid forecast request:

```powershell
curl.exe -i -X POST http://localhost:3000/api/forecasts `
  -H "content-type: application/json" `
  --data "{\"eventId\":\"<known-event-slug>\"}"
```

The response must have HTTP status `503` and the standard JSON error shape:
`{ "error": { "code": "INFERENCE_503", "message": "..." } }`.
Restart the inference service before the next check.

To check the database failure path, stop only PostgreSQL while leaving the web
app and inference service running. Then request the event list:

```powershell
curl.exe -i http://localhost:3000/api/events
```

The response must have HTTP status `503` and the standard JSON error shape:
`{ "error": { "code": "database_unavailable", "message": "..." } }`.
Restart PostgreSQL after the check.
