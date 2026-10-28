import { beforeEach, describe, expect, it, vi } from "vitest";

const { prismaMock, inferenceMock } = vi.hoisted(() => ({
  prismaMock: {
    radarEvent: {
      findMany: vi.fn(),
      findUnique: vi.fn(),
    },
    forecast: {
      create: vi.fn(),
      findMany: vi.fn(),
    },
  },
  inferenceMock: vi.fn(),
}));

vi.mock("../src/lib/prisma", () => ({ prisma: prismaMock }));
vi.mock("../src/lib/inference-client", () => ({
  InferenceClientError: class InferenceClientError extends Error {
    status: 502 | 503 | 504;

    constructor(status: 502 | 503 | 504, message: string) {
      super(message);
      this.status = status;
    }
  },
  predict: inferenceMock,
}));

import { GET as getEvents } from "../app/api/events/route";
import { GET as getEvent } from "../app/api/events/[slug]/route";
import { GET as getForecasts, POST as postForecast } from "../app/api/forecasts/route";
import { InferenceClientError } from "../src/lib/inference-client";

const event = {
  id: "event-1",
  slug: "2023-05-14-heavy-cell",
  name: "Heavy cell",
  startTime: new Date("2023-05-14T00:00:00.000Z"),
  description: "Placeholder event description.",
};

const prediction = {
  eventId: event.slug,
  modelVersion: "convlstm-77000",
  thresholdMmPerHour: 10,
  leadMinutes: [10, 20, 30, 40, 50, 60],
  frames: {
    observed: ["a", "b", "c", "d", "e", "f"],
    convlstm: ["a", "b", "c", "d", "e", "f"],
    persistence: ["a", "b", "c", "d", "e", "f"],
  },
  metrics: {
    convlstm: { csi: [0, 0, 0, 0, 0, 0], pod: [0, 0, 0, 0, 0, 0], far: [0, 0, 0, 0, 0, 0], bias: [0, 0, 0, 0, 0, 0] },
    persistence: { csi: [0, 0, 0, 0, 0, 0], pod: [0, 0, 0, 0, 0, 0], far: [0, 0, 0, 0, 0, 0], bias: [0, 0, 0, 0, 0, 0] },
  },
  latencyMs: 123,
};

beforeEach(() => {
  vi.clearAllMocks();
});

describe("event routes", () => {
  it("lists events", async () => {
    prismaMock.radarEvent.findMany.mockResolvedValue([event]);

    const response = await getEvents();

    expect(response.status).toBe(200);
    expect(await response.json()).toEqual([{ ...event, startTime: event.startTime.toISOString() }]);
  });

  it("returns one event by slug", async () => {
    prismaMock.radarEvent.findUnique.mockResolvedValue(event);

    const response = await getEvent(new Request("http://localhost/api/events/heavy"), {
      params: Promise.resolve({ slug: event.slug }),
    });

    expect(response.status).toBe(200);
    expect(await response.json()).toEqual({ ...event, startTime: event.startTime.toISOString() });
  });

  it("returns 404 for an unknown event", async () => {
    prismaMock.radarEvent.findUnique.mockResolvedValue(null);

    const response = await getEvent(new Request("http://localhost/api/events/missing"), {
      params: Promise.resolve({ slug: "missing" }),
    });

    expect(response.status).toBe(404);
  });

  it("maps one-event database failures to 503", async () => {
    prismaMock.radarEvent.findUnique.mockRejectedValue(new Error("database failure"));

    const response = await getEvent(new Request("http://localhost/api/events/event"), {
      params: Promise.resolve({ slug: event.slug }),
    });

    expect(response.status).toBe(503);
    expect(await response.json()).toEqual({
      error: { code: "database_unavailable", message: "Database unavailable" },
    });
  });

  it("maps event database failures to 503", async () => {
    prismaMock.radarEvent.findMany.mockRejectedValue(new Error("connection string should not leak"));

    const response = await getEvents();

    expect(response.status).toBe(503);
    expect(await response.json()).toEqual({
      error: { code: "database_unavailable", message: "Database unavailable" },
    });
  });
});

describe("forecast routes", () => {
  it("rejects an invalid request with 400", async () => {
    const response = await postForecast(
      new Request("http://localhost/api/forecasts", { method: "POST", body: "{}" }),
    );

    expect(response.status).toBe(400);
  });

  it("returns 404 when the event does not exist", async () => {
    prismaMock.radarEvent.findUnique.mockResolvedValue(null);

    const response = await postForecast(
      new Request("http://localhost/api/forecasts", {
        method: "POST",
        body: JSON.stringify({ eventId: event.slug }),
      }),
    );

    expect(response.status).toBe(404);
  });

  it("saves and returns a forecast run", async () => {
    prismaMock.radarEvent.findUnique.mockResolvedValue(event);
    inferenceMock.mockResolvedValue(prediction);
    prismaMock.forecast.create.mockResolvedValue({ id: "run-1" });

    const response = await postForecast(
      new Request("http://localhost/api/forecasts", {
        method: "POST",
        body: JSON.stringify({ eventId: event.slug }),
      }),
    );

    expect(response.status).toBe(200);
    expect(await response.json()).toEqual({ ...prediction, runId: "run-1" });
    expect(prismaMock.forecast.create).toHaveBeenCalledWith({
      data: {
        eventId: event.id,
        modelVersion: prediction.modelVersion,
        latencyMs: prediction.latencyMs,
        csiConvlstm: prediction.metrics.convlstm.csi,
        csiPersist: prediction.metrics.persistence.csi,
      },
    });
  });

  it("rejects a response for a different event without saving", async () => {
      prismaMock.radarEvent.findUnique.mockResolvedValue(event);
      inferenceMock.mockResolvedValue({ ...prediction, eventId: "different-event" });

      const response = await postForecast(
        new Request("http://localhost/api/forecasts", {
          method: "POST",
          body: JSON.stringify({ eventId: event.slug }),
        }),
      );

      expect(response.status).toBe(502);
      expect(await response.json()).toEqual({
        error: { code: "inference_bad_response", message: "Inference response identity is invalid" },
      });
      expect(prismaMock.forecast.create).not.toHaveBeenCalled();
  });

  it("rejects a response without a non-empty model version", async () => {
      prismaMock.radarEvent.findUnique.mockResolvedValue(event);
      inferenceMock.mockResolvedValue({ ...prediction, modelVersion: " " });

      const response = await postForecast(
        new Request("http://localhost/api/forecasts", {
          method: "POST",
          body: JSON.stringify({ eventId: event.slug }),
        }),
      );

      expect(response.status).toBe(502);
      expect(await response.json()).toEqual({
        error: { code: "inference_bad_response", message: "Inference response is invalid" },
      });
      expect(prismaMock.forecast.create).not.toHaveBeenCalled();
  });

  it("rejects an oversized request body", async () => {
    const response = await postForecast(
      new Request("http://localhost/api/forecasts", {
        method: "POST",
        body: `{"eventId":"${"x".repeat(4097)}"}`,
      }),
    );

    expect(response.status).toBe(413);
    expect(await response.json()).toEqual({
      error: { code: "payload_too_large", message: "Request body is too large" },
    });
  });

  it("accepts a small valid request body", async () => {
    prismaMock.radarEvent.findUnique.mockResolvedValue(event);
    inferenceMock.mockResolvedValue(prediction);
    prismaMock.forecast.create.mockResolvedValue({ id: "run-2" });

    const response = await postForecast(
      new Request("http://localhost/api/forecasts", {
        method: "POST",
        body: JSON.stringify({ eventId: event.slug }),
      }),
    );

    expect(response.status).toBe(200);
    expect(await response.json()).toMatchObject({ runId: "run-2", eventId: event.slug });
  });

  it.each([
    [502, "Bad inference response"],
    [503, "Inference unavailable"],
    [504, "Inference timed out"],
  ] as const)("maps inference error %s", async (status, message) => {
    prismaMock.radarEvent.findUnique.mockResolvedValue(event);
    inferenceMock.mockRejectedValue(new InferenceClientError(status, message));

    const response = await postForecast(
      new Request("http://localhost/api/forecasts", {
        method: "POST",
        body: JSON.stringify({ eventId: event.slug }),
      }),
    );

    expect(response.status).toBe(status);
    expect(await response.json()).toEqual({ error: { code: `INFERENCE_${status}`, message } });
  });

  it("resolves a slug before listing saved forecasts newest first", async () => {
    prismaMock.radarEvent.findUnique.mockResolvedValue(event);
    prismaMock.forecast.findMany.mockResolvedValue([{ id: "run-1" }]);

    const response = await getForecasts(
      new Request(`http://localhost/api/forecasts?eventId=${event.slug}`),
    );

    expect(response.status).toBe(200);
    expect(await response.json()).toEqual([{ id: "run-1" }]);
    expect(prismaMock.forecast.findMany).toHaveBeenCalledWith({
      where: { eventId: event.id },
      orderBy: { createdAt: "desc" },
    });
    expect(prismaMock.radarEvent.findUnique).toHaveBeenCalledWith({ where: { slug: event.slug } });
  });

  it("returns 404 for an unknown forecast event slug", async () => {
    prismaMock.radarEvent.findUnique.mockResolvedValue(null);

    const response = await getForecasts(
      new Request("http://localhost/api/forecasts?eventId=missing"),
    );

    expect(response.status).toBe(404);
    expect(await response.json()).toEqual({
      error: { code: "EVENT_NOT_FOUND", message: "Event not found" },
    });
    expect(prismaMock.forecast.findMany).not.toHaveBeenCalled();
  });

  it("maps forecast database failures to 503", async () => {
    prismaMock.radarEvent.findUnique.mockRejectedValue(new Error("database URL should not leak"));

    const response = await postForecast(
      new Request("http://localhost/api/forecasts", {
        method: "POST",
        body: JSON.stringify({ eventId: event.slug }),
      }),
    );

    expect(response.status).toBe(503);
    expect(await response.json()).toEqual({
      error: { code: "database_unavailable", message: "Database unavailable" },
    });
  });

  it("maps forecast-list database failures to 503", async () => {
    prismaMock.forecast.findMany.mockRejectedValue(new Error("database failure"));

    const response = await getForecasts(new Request("http://localhost/api/forecasts"));

    expect(response.status).toBe(503);
    expect(await response.json()).toEqual({
      error: { code: "database_unavailable", message: "Database unavailable" },
    });
  });

  it("rejects an invalid forecast filter with 400", async () => {
    const response = await getForecasts(
      new Request("http://localhost/api/forecasts?eventId="),
    );

    expect(response.status).toBe(400);
  });
});