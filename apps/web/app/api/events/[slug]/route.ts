import { NextResponse } from "next/server";

import { databaseUnavailableResponse, errorResponse } from "../../../../src/lib/api-errors";
import { prisma } from "../../../../src/lib/prisma";
import { eventSlugSchema } from "../../../../src/lib/schemas";

type EventRouteContext = { params: Promise<{ slug: string }> };

export async function GET(_request: Request, context: EventRouteContext): Promise<NextResponse> {
  const { slug } = await context.params;
  const slugResult = eventSlugSchema.safeParse(slug);
  if (!slugResult.success) {
    return errorResponse(400, "INVALID_QUERY", "Event slug is invalid");
  }

  try {
    const event = await prisma.radarEvent.findUnique({ where: { slug: slugResult.data } });
    if (!event) {
      return errorResponse(404, "EVENT_NOT_FOUND", "Event not found");
    }

    return NextResponse.json(event);
  } catch {
    return databaseUnavailableResponse();
  }
}