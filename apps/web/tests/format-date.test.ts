import { describe, it, expect } from "vitest";
import { formatEventDate } from "../src/lib/format-date";

describe("formatEventDate", () => {
  it("returns fallback text for null date", () => {
    expect(formatEventDate(null)).toBe("time not verified");
  });

  it("formats an ISO string parsed as Date correctly", () => {
    // 2023-05-26T08:13:00.000Z → "26 May 2023, 08:13 UTC"
    const date = new Date("2023-05-26T08:13:00.000Z");
    expect(formatEventDate(date)).toBe("26 May 2023, 08:13 UTC");
  });

  it("formats midnight UTC correctly", () => {
    const date = new Date("2023-01-01T00:00:00.000Z");
    expect(formatEventDate(date)).toBe("1 Jan 2023, 00:00 UTC");
  });

  it("formats end-of-year date correctly", () => {
    const date = new Date("2023-12-31T23:59:00.000Z");
    expect(formatEventDate(date)).toBe("31 Dec 2023, 23:59 UTC");
  });

  it("pads single-digit hours and minutes", () => {
    const date = new Date("2023-06-05T03:07:00.000Z");
    expect(formatEventDate(date)).toBe("5 Jun 2023, 03:07 UTC");
  });
});
