import { notFound } from "next/navigation";
import { prisma } from "../../../src/lib/prisma";

interface EventPageProps {
  params: Promise<{ slug: string }>;
}

export default async function EventPage({ params }: EventPageProps) {
  const { slug } = await params;

  let event;
  try {
    event = await prisma.radarEvent.findUnique({ where: { slug } });
  } catch {
    return (
      <div
        role="alert"
        className="rounded-lg border border-red-300 bg-red-50 p-6 text-center dark:border-red-700 dark:bg-red-900/30"
      >
        <p className="font-semibold text-red-800 dark:text-red-300">
          Unable to load event
        </p>
        <p className="mt-1 text-sm text-red-700 dark:text-red-400">
          The database is currently unavailable. Please try again later.
        </p>
      </div>
    );
  }

  if (!event) {
    notFound();
  }

  return (
    <>
      <h1 className="text-2xl font-bold">{event.name}</h1>
      <p className="mt-2 text-gray-600 dark:text-gray-400">
        Event detail page — forecast view coming in Phase 8B.
      </p>
    </>
  );
}
