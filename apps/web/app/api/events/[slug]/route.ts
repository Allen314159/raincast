import { NextResponse } from "next/server";

import { prisma } from "../../../../src/lib/prisma";

type EventRouteContext = { params: Promise<{ slug: string }> };

export async function GET(_request: Request, context: EventRouteContext): Promise<NextResponse> {
  const { slug } = await context.params;
  const event = await prisma.radarEvent.findUnique({ where: { slug } });

  if (!event) {
    return NextResponse.json(
      { error: { code: "EVENT_NOT_FOUND", message: "Event not found" } },
      { status: 404 },
    );
  }

  return NextResponse.json(event);
}