import { prisma } from "../src/lib/prisma";
import EventCard from "./components/EventCard";

export default async function EventsPage() {
  let events;
  let dbError = false;

  try {
    events = await prisma.radarEvent.findMany({
      orderBy: { startTime: "desc" },
    });
  } catch {
    dbError = true;
  }

  if (dbError) {
    return (
      <>
        <h1 className="text-2xl font-bold">Radar Events</h1>
        <div
          role="alert"
          className="mt-6 rounded-lg border border-red-300 bg-red-50 p-6 text-center dark:border-red-700 dark:bg-red-900/30"
        >
          <p className="font-semibold text-red-800 dark:text-red-300">
            Unable to load events
          </p>
          <p className="mt-1 text-sm text-red-700 dark:text-red-400">
            The database is currently unavailable. Please try again later.
          </p>
        </div>
        <AboutSection />
      </>
    );
  }

  return (
    <>
      <h1 className="text-2xl font-bold">Radar Events</h1>

      {events && events.length > 0 ? (
        <div className="mt-6 grid gap-4 sm:grid-cols-2">
          {events.map((event) => (
            <EventCard
              key={event.slug}
              slug={event.slug}
              name={event.name}
              startTime={event.startTime}
              description={event.description}
            />
          ))}
        </div>
      ) : (
        <div className="mt-6 rounded-lg border border-gray-200 bg-gray-50 p-6 text-center dark:border-gray-700 dark:bg-gray-900">
          <p className="font-semibold text-gray-700 dark:text-gray-300">
            No events available
          </p>
          <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
            No radar events have been added yet. Seed the database to get
            started.
          </p>
        </div>
      )}

      <AboutSection />
    </>
  );
}

function AboutSection() {
  return (
    <section className="mt-10" aria-labelledby="about-heading">
      <h2
        id="about-heading"
        className="text-lg font-semibold text-gray-900 dark:text-gray-100"
      >
        About / Limitations
      </h2>
      <ul className="mt-3 list-disc space-y-1 pl-5 text-sm text-gray-700 dark:text-gray-300">
        <li>
          This demo serves only the <strong>ConvLSTM baseline</strong> model.
        </li>
        <li>
          The checkpoint served is <strong>77000</strong>. Thesis numbers refer
          to a different checkpoint (89000) and a different evaluation pipeline;
          they are not directly comparable.
        </li>
        <li>
          Over-prediction of heavy rain is expected: aggregate BIAS measured at
          1.80–2.60 across lead times (see{" "}
          <code className="rounded bg-gray-100 px-1 dark:bg-gray-800">
            docs/RESULTS.md
          </code>
          ).
        </li>
      </ul>
    </section>
  );
}
