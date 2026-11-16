import Link from "next/link";

export default function Header() {
  return (
    <header className="border-b border-gray-200 bg-white dark:border-gray-700 dark:bg-gray-900">
      <div className="mx-auto flex max-w-5xl items-center justify-between px-4 py-3">
        <Link
          href="/"
          className="text-xl font-bold text-gray-900 dark:text-gray-100"
        >
          RainCast
        </Link>

        <nav aria-label="Main navigation">
          <ul className="flex gap-6">
            <li>
              <Link
                href="/"
                className="text-gray-700 hover:text-gray-900 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-blue-600 dark:text-gray-300 dark:hover:text-gray-100"
              >
                Events
              </Link>
            </li>
            <li>
              <Link
                href="/history"
                className="text-gray-700 hover:text-gray-900 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-blue-600 dark:text-gray-300 dark:hover:text-gray-100"
              >
                History
              </Link>
            </li>
          </ul>
        </nav>
      </div>
    </header>
  );
}
