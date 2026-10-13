import { describe, expect, it } from "vitest";

import {
  errorResponseSchema,
  forecastRequestSchema,
  predictResponseSchema,
} from "../src/lib/schemas";

describe("forecast schemas", () => {
  it("accepts a valid forecast request", () => {
    expect(forecastRequestSchema.safeParse({ eventId: "2023-05-14-heavy-cell" }).success).toBe(
      true,
    );
  });

  it("rejects a request without an event id", () => {
    expect(forecastRequestSchema.safeParse({}).success).toBe(false);
  });

  it("accepts the FastAPI prediction response", () => {
    const metricValues = [null, 0.2, 0.3, 0.4, 0.5, 0.6];
    const frameValues = ["frame-1", "frame-2", "frame-3", "frame-4", "frame-5", "frame-6"];

    expect(
      predictResponseSchema.safeParse({
        eventId: "2023-05-14-heavy-cell",
        modelVersion: "convlstm-89000",
        thresholdMmPerHour: 10,
        leadMinutes: [10, 20, 30, 40, 50, 60],
        frames: {
          observed: frameValues,
          convlstm: frameValues,
          persistence: frameValues,
        },
        metrics: {
          convlstm: { csi: metricValues, pod: metricValues, far: metricValues, bias: metricValues },
          persistence: {
            csi: metricValues,
            pod: metricValues,
            far: metricValues,
            bias: metricValues,
          },
        },
        latencyMs: 2340,
      }).success,
    ).toBe(true);
  });

  it("rejects a prediction response with the wrong frame count", () => {
    expect(
      predictResponseSchema.safeParse({
        eventId: "2023-05-14-heavy-cell",
        modelVersion: "convlstm-89000",
        thresholdMmPerHour: 10,
        leadMinutes: [10, 20, 30, 40, 50, 60],
        frames: { observed: [], convlstm: [], persistence: [] },
        metrics: {
          convlstm: { csi: [], pod: [], far: [], bias: [] },
          persistence: { csi: [], pod: [], far: [], bias: [] },
        },
        latencyMs: 2340,
      }).success,
    ).toBe(false);
  });

  it("accepts the standard error response", () => {
    expect(errorResponseSchema.safeParse({ error: { code: "TIMEOUT", message: "Timed out" } }).success).toBe(
      true,
    );
  });
});