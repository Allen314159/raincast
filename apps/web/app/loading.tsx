export default function Loading() {
  return (
    <>
      <h1 className="text-2xl font-bold">Radar Events</h1>
      <div className="mt-6 grid gap-4 sm:grid-cols-2">
        {[1, 2, 3].map((i) => (
          <div
            key={i}
            className="animate-pulse rounded-lg border border-gray-200 bg-white p-4 dark:border-gray-700 dark:bg-gray-900"
          >
            <div className="h-5 w-3/4 rounded bg-gray-200 dark:bg-gray-700" />
            <div className="mt-2 h-4 w-1/2 rounded bg-gray-200 dark:bg-gray-700" />
            <div className="mt-3 h-4 w-full rounded bg-gray-200 dark:bg-gray-700" />
          </div>
        ))}
      </div>
    </>
  );
}
