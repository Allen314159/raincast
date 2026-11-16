import { describe, expect, it } from "vitest";
import { formatHistoryDate, getCsiAt30 } from "../src/lib/history";

describe("history helpers", () => {
  it("formats a saved run time in UTC", () => {
    expect(formatHistoryDate(new Date("2023-05-26T08:13:00.000Z"))).toBe(
      "26 May 2023, 08:13",
    );
  });

  it("extracts CSI at +30 minutes", () => {
    expect(getCsiAt30([0.4, 0.3, 0.219557, 0.1])).toBe(0.219557);
  });

  it.each([null, undefined, {}, [], [0.4, 0.3], [0.4, 0.3, null], [0.4, 0.3, "0.2"], [0.4, 0.3, Number.NaN]])(
    "returns null for malformed CSI data: %s",
    (value) => {
      expect(getCsiAt30(value)).toBeNull();
    },
  );
});
