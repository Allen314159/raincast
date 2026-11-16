import type { Metadata } from "next";
import Link from "next/link";

import { prisma } from "../../src/lib/prisma";
import { eventSlugSchema } from "../../src/lib/schemas";
import { formatHistoryDate, getCsiAt30 } from "../../src/lib/history";

export const metadata: Metadata = {
  title: "Forecast History | RainCast",
  description: "Saved RainCast forecast runs.",
};

const HISTORY_LIMIT = 50;

interface HistoryPageProps {
  searchParams: Promise<{ event?: string | string[] }>;
}

interface HistoryRun {
  id: string;
  createdAt: Date;
  latencyMs: number;
  modelVersion: string;
  csiConvlstm: unknown;
  csiPersist: unknown;
  event: { name: string; slug: string };
}

export default async function HistoryPage({
  searchParams,
}: HistoryPageProps) {
  return <HistoryData searchParams={searchParams} />;
}

async function HistoryData({
  searchParams,
}: HistoryPageProps): Promise<React.ReactElement> {
  const rawEvent = (await searchParams).event;
  const parsedEvent = eventSlugSchema.safeParse(
    typeof rawEvent === "string" ? rawEvent : undefined,
  );
  const invalidFilter = rawEvent !== undefined && !parsedEvent.success;
  const eventSlug = parsedEvent.success ? parsedEvent.data : undefined;
  let filterEvent: { id: string; name: string; slug: string } | null = null;
  let runs: HistoryRun[] = [];

  try {
    filterEvent = eventSlug
      ? await prisma.radarEvent.findUnique({ where: { slug: eventSlug } })
      : null;

    runs = filterEvent || !eventSlug
      ? await prisma.forecast.findMany({
          where: filterEvent ? { eventId: filterEvent.id } : undefined,
          include: {
            event: { select: { name: true, slug: true } },
          },
          orderBy: { createdAt: "desc" },
          take: HISTORY_LIMIT,
        })
      : [];
  } catch {
    return <DatabaseError />;
  }

  return (
    <>
      <h1 className="text-2xl font-bold">Forecast History</h1>
      <p className="mt-2 text-gray-700 dark:text-gray-300">
        Showing up to {HISTORY_LIMIT} most recent forecast runs.
      </p>
      {invalidFilter && (
        <p
          role="status"
          className="mt-3 rounded-md border border-amber-300 bg-amber-50 p-3 text-sm text-amber-900 dark:border-amber-700 dark:bg-amber-900/30 dark:text-amber-200"
        >
          The event filter was invalid and was ignored.
        </p>
      )}
      {eventSlug && filterEvent && (
        <p className="mt-3 text-sm text-gray-700 dark:text-gray-300">
          Filtered by event: <strong>{filterEvent.name}</strong>{" "}
          <Link
            href="/history"
            className="font-semibold text-blue-700 underline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-blue-700 dark:text-blue-400"
          >
            Clear filter
          </Link>
        </p>
      )}
      {eventSlug && !filterEvent ? (
        <EmptyState message={`No runs found for event "${eventSlug}".`} />
      ) : runs.length === 0 ? (
        <EmptyState message="No runs yet" />
      ) : (
        <HistoryTable runs={runs} />
      )}
    </>
  );
}

function DatabaseError() {
  return (
    <>
      <h1 className="text-2xl font-bold">Forecast History</h1>
      <div
        role="alert"
        className="mt-6 rounded-lg border border-red-300 bg-red-50 p-6 text-center dark:border-red-700 dark:bg-red-900/30"
      >
        <p className="font-semibold text-red-800 dark:text-red-300">
          Unable to load forecast history
        </p>
        <p className="mt-1 text-sm text-red-700 dark:text-red-400">
          The database is currently unavailable. Please try again later.
        </p>
      </div>
    </>
  );
}

function EmptyState({ message }: { message: string }) {
  return (
    <div className="mt-6 rounded-lg border border-gray-200 bg-gray-50 p-6 text-center dark:border-gray-700 dark:bg-gray-900">
      <p className="font-semibold text-gray-800 dark:text-gray-200">{message}</p>
      <p className="mt-2 text-sm text-gray-600 dark:text-gray-400">
        <Link
          href="/"
          className="font-semibold text-blue-700 underline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-blue-700 dark:text-blue-400"
        >
          Browse events
        </Link>{" "}
        to run a forecast.
      </p>
    </div>
  );
}

function HistoryTable({
  runs,
}: {
  runs: HistoryRun[];
}) {
  return (
    <div className="mt-6 overflow-x-auto rounded-lg border border-gray-200 dark:border-gray-700">
      <table className="w-full min-w-[46rem] border-collapse text-left text-sm">
        <caption className="sr-only">
          Forecast runs, newest first
        </caption>
        <thead className="bg-gray-100 dark:bg-gray-800">
          <tr>
            <th scope="col" className="px-4 py-3 font-semibold">Event</th>
            <th scope="col" className="px-4 py-3 font-semibold">Created</th>
            <th scope="col" className="px-4 py-3 font-semibold">Latency (ms)</th>
            <th scope="col" className="px-4 py-3 font-semibold">Model version</th>
            <th scope="col" className="px-4 py-3 font-semibold">CSI +30 ConvLSTM</th>
            <th scope="col" className="px-4 py-3 font-semibold">CSI +30 Persistence</th>
          </tr>
        </thead>
        <tbody>
          {runs.map((run) => (
            <tr
              key={run.id}
              className="border-t border-gray-200 dark:border-gray-700"
            >
              <th scope="row" className="px-4 py-3 font-medium">
                <Link
                  href={`/events/${run.event.slug}`}
                  className="text-blue-700 underline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-blue-700 dark:text-blue-400"
                >
                  {run.event.name}
                </Link>
              </th>
              <td className="px-4 py-3">
                <time dateTime={run.createdAt.toISOString()}>
                  {formatHistoryDate(run.createdAt)}
                </time>
              </td>
              <td className="px-4 py-3">{run.latencyMs}</td>
              <td className="px-4 py-3">{run.modelVersion}</td>
              <td className="px-4 py-3">{formatCsi(run.csiConvlstm)}</td>
              <td className="px-4 py-3">{formatCsi(run.csiPersist)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function formatCsi(value: unknown): string {
  const csi = getCsiAt30(value);
  return csi === null ? "—" : csi.toFixed(3);
}
