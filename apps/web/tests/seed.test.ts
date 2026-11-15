import { describe, expect, it } from "vitest";

import { parseSeedEvents } from "../prisma/seed";

describe("seed manifest", () => {
  it("rejects an event without startTime", () => {
    expect(() =>
      parseSeedEvents([
        {
          slug: "event",
          name: "Event",
          description: null,
        },
      ]),
    ).toThrow();
  });

  it("accepts a dated event", () => {
    expect(
      parseSeedEvents([
        {
          slug: "event",
          name: "Event",
          startTime: "2023-05-26T08:13:00.000Z",
          description: null,
        },
      ]),
    ).toHaveLength(1);
  });
});
