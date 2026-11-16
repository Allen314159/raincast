/**
 * Format a date for display on event cards.
 * Returns a human-readable UTC date string, or a fallback if the date is null.
 */
export function formatEventDate(date: Date | null): string {
  if (date === null) {
    return "time not verified";
  }

  // Format as "26 May 2023, 08:13 UTC"
  const day = date.getUTCDate();
  const month = MONTHS[date.getUTCMonth()];
  const year = date.getUTCFullYear();
  const hours = String(date.getUTCHours()).padStart(2, "0");
  const minutes = String(date.getUTCMinutes()).padStart(2, "0");

  return `${day} ${month} ${year}, ${hours}:${minutes} UTC`;
}

const MONTHS = [
  "Jan", "Feb", "Mar", "Apr", "May", "Jun",
  "Jul", "Aug", "Sep", "Oct", "Nov", "Dec",
] as const;
