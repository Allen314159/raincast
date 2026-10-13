import { NextResponse } from "next/server";
import { z } from "zod";

import { InferenceClientError, predict } from "../../../src/lib/inference-client";
import { prisma } from "../../../src/lib/prisma";
import { forecastRequestSchema, predictResponseSchema } from "../../../src/lib/schemas";

const forecastQuerySchema = z.object({ eventId: z.string().trim().min(1).optional() });

function errorResponse(status: number, code: string, message: string): NextResponse {
  return NextResponse.json({ error: { code, message } }, { status });
}

export async function POST(request: Request): Promise<NextResponse> {
  let body: unknown;
  try {
    body = await request.json();
  } catch {
    return errorResponse(400, "INVALID_REQUEST", "Request body must be valid JSON");
  }

  const requestResult = forecastRequestSchema.safeParse(body);
  if (!requestResult.success) {
    return errorResponse(400, "INVALID_REQUEST", "Request body is invalid");
  }

  const event = await prisma.radarEvent.findUnique({ where: { slug: requestResult.data.eventId } });
  if (!event) {
    return errorResponse(404, "EVENT_NOT_FOUND", "Event not found");
  }

  let prediction;
  try {
    prediction = predictResponseSchema.parse(await predict(event.slug));
  } catch (error: unknown) {
    if (error instanceof InferenceClientError) {
      return errorResponse(error.status, `INFERENCE_${error.status}`, error.message);
    }
    return errorResponse(502, "INFERENCE_502", "Inference service returned an invalid response");
  }

  const forecast = await prisma.forecast.create({
    data: {
      eventId: event.id,
      modelVersion: prediction.modelVersion,
      latencyMs: prediction.latencyMs,
      csiConvlstm: prediction.metrics.convlstm.csi,
      csiPersist: prediction.metrics.persistence.csi,
    },
  });

  return NextResponse.json({ ...prediction, runId: forecast.id });
}

export async function GET(request: Request): Promise<NextResponse> {
  const eventId = new URL(request.url).searchParams.get("eventId") ?? undefined;
  const queryResult = forecastQuerySchema.safeParse({ eventId });
  if (!queryResult.success) {
    return errorResponse(400, "INVALID_QUERY", "Query parameters are invalid");
  }

  const forecasts = await prisma.forecast.findMany({
    where: queryResult.data.eventId ? { eventId: queryResult.data.eventId } : undefined,
    orderBy: { createdAt: "desc" },
  });
  return NextResponse.json(forecasts);
}