import { PrismaClient } from "@prisma/client";

import events from "./events.json";

const prisma = new PrismaClient();

async function main(): Promise<void> {
  for (const event of events) {
    await prisma.radarEvent.upsert({
      where: { slug: event.slug },
      update: {
        name: event.name,
        startTime: new Date(event.startTime),
        description: event.description,
      },
      create: {
        slug: event.slug,
        name: event.name,
        startTime: new Date(event.startTime),
        description: event.description,
      },
    });
  }
}

main()
  .catch((error: unknown) => {
    console.error(error);
    process.exitCode = 1;
  })
  .finally(async () => {
    await prisma.$disconnect();
  });