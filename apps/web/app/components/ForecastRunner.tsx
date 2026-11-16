"use client";

import { useState } from "react";
import {
  buildChartPath,
  buildChartPoints,
  formatMetric,
  forecastErrorMessage,
} from "../../src/lib/forecast-ui";
import {
  errorResponseSchema,
  forecastResponseSchema,
  type ForecastResponse,
} from "../../src/lib/schemas";

interface ForecastRunnerProps {
  slug: string;
}

type RunnerState =
  | { status: "idle" }
  | { status: "loading" }
  | { status: "success"; forecast: ForecastResponse }
  | { status: "error"; message: string };

const COLOR_STOPS = [
  { dbz: -10, color: "#000000" },
  { dbz: 5, color: "#2850a0" },
  { dbz: 15, color: "#00aadc" },
  { dbz: 25, color: "#00be50" },
  { dbz: 34.0063696, color: "#ffeb00" },
  { dbz: 45, color: "#ff6400" },
  { dbz: 60, color: "#b40000" },
] as const; // must match services/inference/app/render.py

const CHART_WIDTH = 600;
const CHART_HEIGHT = 240;

export default function ForecastRunner({ slug }: ForecastRunnerProps) {
  const [state, setState] = useState<RunnerState>({ status: "idle" });
  const [leadIndex, setLeadIndex] = useState(2);

  async function runForecast() {
    setState({ status: "loading" });

    try {
      const response = await fetch("/api/forecasts", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ eventId: slug }),
      });
      const body: unknown = await response.json();

      if (!response.ok) {
        const parsedError = errorResponseSchema.safeParse(body);
        setState({
          status: "error",
          message: parsedError.success
            ? parsedError.data.error.message
            : forecastErrorMessage(response.status),
        });
        return;
      }

      const parsedForecast = forecastResponseSchema.safeParse(body);
      if (!parsedForecast.success) {
        setState({ status: "error", message: forecastErrorMessage(502) });
        return;
      }

      setState({ status: "success", forecast: parsedForecast.data });
    } catch {
      setState({ status: "error", message: forecastErrorMessage(503) });
    }
  }

  return (
    <section className="mt-8" aria-labelledby="forecast-heading">
      <div className="flex flex-wrap items-center justify-between gap-3">
        <h2 id="forecast-heading" className="text-xl font-semibold">
          Forecast
        </h2>
        <button
          type="button"
          onClick={runForecast}
          disabled={state.status === "loading"}
          className="rounded-md bg-blue-700 px-4 py-2 font-semibold text-white hover:bg-blue-800 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-blue-700 disabled:cursor-not-allowed disabled:opacity-60 dark:bg-blue-600 dark:hover:bg-blue-500"
        >
          {state.status === "loading" ? "Running forecast…" : "Run forecast"}
        </button>
      </div>

      {state.status === "idle" && (
        <p className="mt-3 text-gray-700 dark:text-gray-300">
          Run the ConvLSTM forecast to compare six lead times. Inference can
          take several seconds.
        </p>
      )}

      {state.status === "loading" && (
        <div className="mt-4 flex items-center gap-3" role="status">
          <span
            className="size-5 animate-spin rounded-full border-2 border-blue-700 border-t-transparent dark:border-blue-400 dark:border-t-transparent"
            aria-hidden="true"
          />
          <p>Inference can take several seconds. Please wait.</p>
        </div>
      )}

      {state.status === "error" && (
        <div
          className="mt-4 rounded-lg border border-red-300 bg-red-50 p-4 dark:border-red-700 dark:bg-red-900/30"
          role="alert"
        >
          <p className="font-semibold text-red-800 dark:text-red-200">
            {state.message}
          </p>
          <button
            type="button"
            onClick={runForecast}
            className="mt-3 rounded-md border border-red-700 px-3 py-1.5 font-semibold text-red-800 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-red-700 dark:border-red-300 dark:text-red-200"
          >
            Retry
          </button>
        </div>
      )}

      {state.status === "success" && (
        <ForecastResult
          forecast={state.forecast}
          leadIndex={leadIndex}
          onLeadIndexChange={setLeadIndex}
        />
      )}
    </section>
  );
}

function ForecastResult({
  forecast,
  leadIndex,
  onLeadIndexChange,
}: {
  forecast: ForecastResponse;
  leadIndex: number;
  onLeadIndexChange: (index: number) => void;
}) {
  const lead = forecast.leadMinutes[leadIndex];
  const panels = [
    ["Observed", forecast.frames.observed[leadIndex]],
    ["ConvLSTM", forecast.frames.convlstm[leadIndex]],
    ["Persistence", forecast.frames.persistence[leadIndex]],
  ] as const;

  return (
    <div className="mt-6">
      <div className="rounded-lg border border-gray-200 p-4 dark:border-gray-700">
        <label htmlFor="lead-time" className="font-semibold">
          Lead time: <span>+{lead} min</span>
        </label>
        <input
          id="lead-time"
          type="range"
          min={10}
          max={60}
          step={10}
          value={lead}
          onChange={(event) =>
            onLeadIndexChange(Number(event.target.value) / 10 - 1)
          }
          aria-valuetext={`+${lead} minutes`}
          className="mt-3 w-full accent-blue-700"
        />
        <div className="mt-1 flex justify-between text-xs text-gray-600 dark:text-gray-400">
          {forecast.leadMinutes.map((minutes) => (
            <span key={minutes}>+{minutes}</span>
          ))}
        </div>
      </div>

      <div className="mt-6 grid gap-4 md:grid-cols-3">
        {panels.map(([title, frame]) => (
          <figure
            key={title}
            className="rounded-lg border border-gray-200 bg-white p-3 dark:border-gray-700 dark:bg-gray-900"
          >
            <figcaption className="font-semibold">{title}</figcaption>
            <img
              src={`data:image/png;base64,${frame}`}
              alt={`${title} radar frame at +${lead} minutes`}
              className="mt-2 aspect-square w-full object-contain"
            />
          </figure>
        ))}
      </div>

      <div className="mt-6 rounded-lg border border-gray-200 p-4 dark:border-gray-700">
        <h3 className="font-semibold">Colour legend (dBZ)</h3>
        <div
          className="mt-3 h-4 rounded"
          style={{
            background: `linear-gradient(to right, ${COLOR_STOPS.map(
              ({ dbz, color }) => `${color} ${((dbz + 10) / 70) * 100}%`,
            ).join(", ")})`,
          }}
          aria-label="Radar reflectivity colour scale from minus 10 to 60 dBZ"
        />
        <div className="mt-1 flex justify-between text-xs text-gray-600 dark:text-gray-400">
          <span>-10 dBZ</span>
          <span>60 dBZ</span>
        </div>
      </div>

      <MetricsTable forecast={forecast} leadIndex={leadIndex} />
      <CsiChart forecast={forecast} />

      <p className="mt-4 text-sm text-gray-600 dark:text-gray-400">
        Run ID: <code>{forecast.runId}</code> · Inference latency:{" "}
        {forecast.latencyMs} ms
      </p>
    </div>
  );
}

function MetricsTable({
  forecast,
  leadIndex,
}: {
  forecast: ForecastResponse;
  leadIndex: number;
}) {
  const rows = [
    [
      "CSI",
      forecast.metrics.convlstm.csi[leadIndex],
      forecast.metrics.persistence.csi[leadIndex],
    ],
    [
      "POD",
      forecast.metrics.convlstm.pod[leadIndex],
      forecast.metrics.persistence.pod[leadIndex],
    ],
    [
      "FAR",
      forecast.metrics.convlstm.far[leadIndex],
      forecast.metrics.persistence.far[leadIndex],
    ],
    [
      "BIAS",
      forecast.metrics.convlstm.bias[leadIndex],
      forecast.metrics.persistence.bias[leadIndex],
    ],
  ] as const;

  return (
    <div className="mt-6 overflow-x-auto">
      <table className="w-full min-w-[22rem] border-collapse text-left text-sm">
        <caption className="mb-2 text-left font-semibold">
          Metrics at +{forecast.leadMinutes[leadIndex]} minutes
        </caption>
        <thead>
          <tr className="border-b border-gray-300 dark:border-gray-700">
            <th scope="col" className="px-3 py-2">
              Metric
            </th>
            <th scope="col" className="px-3 py-2">
              ConvLSTM
            </th>
            <th scope="col" className="px-3 py-2">
              Persistence
            </th>
          </tr>
        </thead>
        <tbody>
          {rows.map(([name, convlstm, persistence]) => (
            <tr
              key={name}
              className="border-b border-gray-200 dark:border-gray-800"
            >
              <th scope="row" className="px-3 py-2 font-medium">
                {name}
              </th>
              <td className="px-3 py-2">{metricValue(convlstm)}</td>
              <td className="px-3 py-2">{metricValue(persistence)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function metricValue(value: number | null) {
  if (value === null) {
    return (
      <span title="no heavy rain in this frame or no forecast heavy rain (undefined)">
        —
      </span>
    );
  }
  return formatMetric(value);
}

function CsiChart({ forecast }: { forecast: ForecastResponse }) {
  const convlstmPoints = buildChartPoints(forecast.metrics.convlstm.csi);
  const persistencePoints = buildChartPoints(forecast.metrics.persistence.csi);
  const convlstmPath = buildChartPath(convlstmPoints);
  const persistencePath = buildChartPath(persistencePoints);

  return (
    <section className="mt-8" aria-labelledby="csi-chart-heading">
      <h3 id="csi-chart-heading" className="font-semibold">
        CSI by lead time
      </h3>
      <svg
        viewBox={`0 0 ${CHART_WIDTH} ${CHART_HEIGHT}`}
        className="mt-3 h-auto w-full"
        role="img"
        aria-labelledby="csi-chart-title csi-chart-description"
      >
        <title id="csi-chart-title">CSI by lead time for both models</title>
        <desc id="csi-chart-description">
          Lines show CSI from zero to one across the six forecast lead times.
        </desc>
        <line x1="36" y1="36" x2="36" y2="204" stroke="currentColor" />
        <line x1="36" y1="204" x2="564" y2="204" stroke="currentColor" />
        <text x="8" y="40" className="fill-current text-xs">
          1.0
        </text>
        <text x="12" y="208" className="fill-current text-xs">
          0.0
        </text>
        <path d={convlstmPath} fill="none" stroke="#2563eb" strokeWidth="3" />
        <path
          d={persistencePath}
          fill="none"
          stroke="#d97706"
          strokeWidth="3"
        />
        {forecast.leadMinutes.map((minutes, index) => (
          <text
            key={minutes}
            x={convlstmPoints[index].x}
            y="224"
            textAnchor="middle"
            className="fill-current text-xs"
          >
            +{minutes}
          </text>
        ))}
      </svg>
      <p className="text-sm text-gray-700 dark:text-gray-300">
        <span className="font-semibold text-blue-700 dark:text-blue-400">
          Blue
        </span>{" "}
        ConvLSTM ·{" "}
        <span className="font-semibold text-amber-700 dark:text-amber-400">
          Amber
        </span>{" "}
        Persistence
      </p>
    </section>
  );
}
