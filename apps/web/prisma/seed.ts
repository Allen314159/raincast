import { PrismaClient } from "@prisma/client";
import { pathToFileURL } from "node:url";
import { z } from "zod";

import events from "./events.json";

const prisma = new PrismaClient();

const seedEventSchema = z.object({
  slug: z.string().trim().min(1),
  name: z.string().trim().min(1),
  startTime: z.string().datetime(),
  description: z.string().nullable().optional(),
});

export function parseSeedEvents(input: unknown): z.infer<typeof seedEventSchema>[] {
  return z.array(seedEventSchema).parse(input);
}

async function main(): Promise<void> {
  for (const event of parseSeedEvents(events)) {
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

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  main()
    .catch((error: unknown) => {
      console.error(error);
      process.exitCode = 1;
    })
    .finally(async () => {
      await prisma.$disconnect();
    });
}