const webUrl = (process.env.WEB_URL ?? "http://localhost:3000").replace(/\/+$/, "");
const inferenceUrl = (process.env.INFERENCE_URL ?? "http://localhost:8000").replace(
  /\/+$/,
  "",
);

const leadMinutes = [10, 20, 30, 40, 50, 60];
const failures = [];

function pass(name, details) {
  console.log(`PASS ${name}${details ? ` - ${details}` : ""}`);
}

function fail(name, error) {
  const message = error instanceof Error ? error.message : String(error);
  failures.push(name);
  console.log(`FAIL ${name} - ${message}`);
}

function formatBytes(bytes) {
  return `${bytes} bytes`;
}

function formatMs(milliseconds) {
  return `${milliseconds.toFixed(0)} ms`;
}

async function request(url, options) {
  const started = performance.now();
  const response = await fetch(url, options);
  const body = await response.text();
  return {
    response,
    body,
    elapsedMs: performance.now() - started,
    sizeBytes: Buffer.byteLength(body, "utf8"),
  };
}

function parseJson(body, label) {
  try {
    return JSON.parse(body);
  } catch {
    throw new Error(`${label} did not return JSON`);
  }
}

function assertErrorShape(value, code) {
  if (
    !value ||
    typeof value !== "object" ||
    !value.error ||
    typeof value.error !== "object" ||
    typeof value.error.code !== "string" ||
    typeof value.error.message !== "string" ||
    value.error.code !== code
  ) {
    throw new Error(`expected standard error shape with code ${code}`);
  }
}

function assertMetricSeries(metrics, seriesName) {
  const series = metrics?.[seriesName];
  if (!series || typeof series !== "object") {
    throw new Error(`missing ${seriesName} metrics`);
  }
  for (const metricName of ["csi", "pod", "far", "bias"]) {
    const values = series[metricName];
    if (
      !Array.isArray(values) ||
      values.length !== 6 ||
      values.some((value) => value !== null && (typeof value !== "number" || !Number.isFinite(value)))
    ) {
      throw new Error(`${seriesName}.${metricName} must contain six finite numbers or null`);
    }
  }
}

async function main() {
  const started = performance.now();
  let health;
  try {
    const result = await request(`${inferenceUrl}/health`);
    health = parseJson(result.body, "inference health");
    if (
      result.response.status !== 200 ||
      health.modelLoaded !== true ||
      typeof health.modelVersion !== "string" ||
      health.modelVersion.trim() === ""
    ) {
      throw new Error(`status ${result.response.status}, modelLoaded=${health.modelLoaded}`);
    }
    pass(
      "inference health",
      `${formatBytes(result.sizeBytes)} in ${formatMs(result.elapsedMs)}; modelVersion=${health.modelVersion}`,
    );
  } catch (error) {
    fail("inference health", error);
  }

  let event;
  try {
    const result = await request(`${webUrl}/api/events`);
    const events = parseJson(result.body, "events");
    if (result.response.status !== 200 || !Array.isArray(events) || events.length < 1) {
      throw new Error(`status ${result.response.status}; expected at least one event`);
    }
    event = events[0];
    if (!event || typeof event.slug !== "string" || event.slug.trim() === "") {
      throw new Error("first event has no non-empty slug");
    }
    pass(
      "list events",
      `${events.length} event(s), ${formatBytes(result.sizeBytes)} in ${formatMs(result.elapsedMs)}`,
    );
  } catch (error) {
    fail("list events", error);
  }

  let runId;
  if (event) {
    try {
      const result = await request(`${webUrl}/api/forecasts`, {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ eventId: event.slug }),
      });
      const forecast = parseJson(result.body, "forecast");
      if (
        result.response.status !== 200 ||
        forecast.eventId !== event.slug ||
        typeof forecast.runId !== "string" ||
        forecast.runId.trim() === "" ||
        typeof forecast.latencyMs !== "number" ||
        !Number.isFinite(forecast.latencyMs) ||
        JSON.stringify(forecast.leadMinutes) !== JSON.stringify(leadMinutes)
      ) {
        throw new Error(`status ${result.response.status}; forecast metadata is invalid`);
      }
      for (const frameName of ["observed", "convlstm", "persistence"]) {
        if (
          !Array.isArray(forecast.frames?.[frameName]) ||
          forecast.frames[frameName].length !== 6 ||
          forecast.frames[frameName].some(
            (frame) => typeof frame !== "string" || frame.length === 0,
          )
        ) {
          throw new Error(`${frameName} must contain six non-empty frames`);
        }
      }
      assertMetricSeries(forecast.metrics, "convlstm");
      assertMetricSeries(forecast.metrics, "persistence");
      runId = forecast.runId;
      pass(
        "create forecast",
        `${formatBytes(result.sizeBytes)} in ${formatMs(result.elapsedMs)}; frame counts=6/6/6; latencyMs=${forecast.latencyMs}`,
      );
    } catch (error) {
      fail("create forecast", error);
    }

    if (runId) {
      try {
        const result = await request(
          `${webUrl}/api/forecasts?eventId=${encodeURIComponent(event.slug)}`,
        );
        const forecasts = parseJson(result.body, "forecast history");
        if (
          result.response.status !== 200 ||
          !Array.isArray(forecasts) ||
          !forecasts.some((forecast) => forecast.id === runId)
        ) {
          throw new Error(`status ${result.response.status}; runId not found`);
        }
        pass(
          "forecast history",
          `${formatBytes(result.sizeBytes)} in ${formatMs(result.elapsedMs)}; runId found`,
        );
      } catch (error) {
        fail("forecast history", error);
      }
    }

    try {
      const unknownSlug = `${event.slug}-unknown`;
      const result = await request(
        `${webUrl}/api/forecasts?eventId=${encodeURIComponent(unknownSlug)}`,
      );
      const errorBody = parseJson(result.body, "unknown event");
      if (result.response.status !== 404) {
        throw new Error(`expected status 404, received ${result.response.status}`);
      }
      assertErrorShape(errorBody, "EVENT_NOT_FOUND");
      pass(
        "unknown event",
        `${formatBytes(result.sizeBytes)} in ${formatMs(result.elapsedMs)}; status=404`,
      );
    } catch (error) {
      fail("unknown event", error);
    }

    try {
      const result = await request(`${webUrl}/api/forecasts`, {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: '{"eventId":',
      });
      const errorBody = parseJson(result.body, "invalid JSON");
      if (result.response.status !== 400) {
        throw new Error(`expected status 400, received ${result.response.status}`);
      }
      assertErrorShape(errorBody, "INVALID_REQUEST");
      pass(
        "invalid JSON body",
        `${formatBytes(result.sizeBytes)} in ${formatMs(result.elapsedMs)}; status=400`,
      );
    } catch (error) {
      fail("invalid JSON body", error);
    }
  } else {
    for (const name of [
      "create forecast",
      "forecast history",
      "unknown event",
      "invalid JSON body",
    ]) {
      fail(name, "skipped because events could not be loaded");
    }
  }

  if (failures.length > 0) {
    console.error(`Smoke test failed: ${failures.join(", ")}`);
    process.exitCode = 1;
  } else {
    console.log(`Smoke test passed - total ${formatMs(performance.now() - started)}`);
  }
}

main().catch((error) => {
  fail("smoke test", error);
  process.exitCode = 1;
});
