import { NextResponse } from "next/server";

import { prisma } from "../../../src/lib/prisma";

export async function GET(): Promise<NextResponse> {
  const events = await prisma.radarEvent.findMany({ orderBy: { startTime: "desc" } });
  return NextResponse.json(events);
}