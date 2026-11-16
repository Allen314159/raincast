import Link from "next/link";
import { formatEventDate } from "../../src/lib/format-date";

interface EventCardProps {
  slug: string;
  name: string;
  startTime: Date | null;
  description: string | null;
}

export default function EventCard({
  slug,
  name,
  startTime,
  description,
}: EventCardProps) {
  return (
    <Link
      href={`/events/${slug}`}
      className="block rounded-lg border border-gray-200 bg-white p-4 shadow-sm transition-shadow hover:shadow-md focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-blue-600 dark:border-gray-700 dark:bg-gray-900"
    >
      <h2 className="text-lg font-semibold text-gray-900 dark:text-gray-100">
        {name}
      </h2>
      <p className="mt-1 text-sm text-gray-600 dark:text-gray-400">
        {formatEventDate(startTime)}
      </p>
      {description && (
        <p className="mt-2 text-sm text-gray-700 dark:text-gray-300">
          {description}
        </p>
      )}
    </Link>
  );
}
