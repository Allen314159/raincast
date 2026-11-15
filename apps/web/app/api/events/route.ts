import { NextResponse } from "next/server";

import { databaseUnavailableResponse } from "../../../src/lib/api-errors";
import { prisma } from "../../../src/lib/prisma";

export async function GET(): Promise<NextResponse> {
  try {
    const events = await prisma.radarEvent.findMany({ orderBy: { startTime: "desc" } });
    return NextResponse.json(events);
  } catch {
    return databaseUnavailableResponse();
  }
}