export function formatHistoryDate(date: Date): string {
  return new Intl.DateTimeFormat("en-GB", {
    dateStyle: "medium",
    timeStyle: "short",
    timeZone: "UTC",
  }).format(date);
}

export function getCsiAt30(value: unknown): number | null {
  if (!Array.isArray(value)) {
    return null;
  }

  const csi = value[2];
  return typeof csi === "number" && Number.isFinite(csi) ? csi : null;
}
