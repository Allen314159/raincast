export type MetricValue = number | null;

export interface ChartPoint {
  x: number;
  y: number | null;
  value: MetricValue;
}

export function formatMetric(value: MetricValue): string {
  return value === null ? "—" : value.toFixed(3);
}

export function buildChartPoints(
  values: readonly MetricValue[],
  width = 600,
  height = 240,
): ChartPoint[] {
  const padding = 36;
  const usableWidth = Math.max(width - padding * 2, 1);
  const usableHeight = Math.max(height - padding * 2, 1);
  const step = values.length > 1 ? usableWidth / (values.length - 1) : 0;

  return values.map((value, index) => ({
    x: padding + step * index,
    y:
      value === null
        ? null
        : padding + (1 - Math.min(Math.max(value, 0), 1)) * usableHeight,
    value,
  }));
}

export function buildChartPath(points: readonly ChartPoint[]): string {
  let path = "";
  let segmentOpen = false;

  for (const point of points) {
    if (point.y === null) {
      segmentOpen = false;
      continue;
    }

    path += `${segmentOpen ? "L" : "M"} ${point.x} ${point.y} `;
    segmentOpen = true;
  }

  return path.trim();
}

export function forecastErrorMessage(status: number): string {
  switch (status) {
    case 404:
      return "This event could not be found.";
    case 502:
      return "The inference service returned an invalid response.";
    case 503:
      return "The inference service is unavailable.";
    case 504:
      return "The inference service timed out.";
    default:
      return "The forecast could not be generated. Please try again.";
  }
}
