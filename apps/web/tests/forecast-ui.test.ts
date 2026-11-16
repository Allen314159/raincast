import { describe, expect, it } from "vitest";
import {
  buildChartPath,
  buildChartPoints,
  formatMetric,
  forecastErrorMessage,
} from "../src/lib/forecast-ui";

describe("forecast UI helpers", () => {
  it("formats null metrics as an em dash", () => {
    expect(formatMetric(null)).toBe("—");
  });

  it("formats numeric metrics to three decimals", () => {
    expect(formatMetric(0.375046)).toBe("0.375");
  });

  it("clamps out-of-range chart values", () => {
    const points = buildChartPoints([-1, 0.5, 2]);
    expect(points[0].y).toBe(204);
    expect(points[1].y).toBe(120);
    expect(points[2].y).toBe(36);
  });

  it("leaves null chart points without a y coordinate", () => {
    expect(buildChartPoints([0.5, null])[1].y).toBeNull();
  });

  it("breaks chart paths at null values", () => {
    const points = buildChartPoints([0.2, null, 0.8]);
    expect(buildChartPath(points)).toMatch(/^M .* .* M .* .*$/);
  });

  it.each([
    [404, "This event could not be found."],
    [502, "The inference service returned an invalid response."],
    [503, "The inference service is unavailable."],
    [504, "The inference service timed out."],
    [500, "The forecast could not be generated. Please try again."],
  ])("maps status %s to a human message", (status, message) => {
    expect(forecastErrorMessage(status)).toBe(message);
  });
});
