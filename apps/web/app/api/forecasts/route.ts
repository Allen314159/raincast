import { NextResponse } from "next/server";
import { z } from "zod";

import { databaseUnavailableResponse, errorResponse } from "../../../src/lib/api-errors";
import { InferenceClientError, predict } from "../../../src/lib/inference-client";
import { prisma } from "../../../src/lib/prisma";
import { forecastRequestSchema, predictResponseSchema } from "../../../src/lib/schemas";

const forecastQuerySchema = z.object({ eventId: z.string().trim().min(1).optional() });
const MAX_BODY_BYTES = 1_048_576;

export async function POST(request: Request): Promise<NextResponse> {
  let body: unknown;
  try {
    const contentLength = request.headers.get("content-length");
    if (contentLength && Number(contentLength) > MAX_BODY_BYTES) {
      return errorResponse(413, "payload_too_large", "Request body is too large");
    }

    const bytes = await request.arrayBuffer();
    if (bytes.byteLength > MAX_BODY_BYTES) {
      return errorResponse(413, "payload_too_large", "Request body is too large");
    }
    body = JSON.parse(new TextDecoder().decode(bytes)) as unknown;
  } catch {
    return errorResponse(400, "INVALID_REQUEST", "Request body must be valid JSON");
  }

  const requestResult = forecastRequestSchema.safeParse(body);
  if (!requestResult.success) {
    return errorResponse(400, "INVALID_REQUEST", "Request body is invalid");
  }

  let event;
  try {
    event = await prisma.radarEvent.findUnique({ where: { slug: requestResult.data.eventId } });
  } catch {
    return databaseUnavailableResponse();
  }
  if (!event) {
    return errorResponse(404, "EVENT_NOT_FOUND", "Event not found");
  }

  let prediction;
  try {
    const predictionResult = predictResponseSchema.safeParse(await predict(event.slug));
    if (!predictionResult.success) {
      return errorResponse(502, "inference_bad_response", "Inference response is invalid");
    }
    if (predictionResult.data.eventId !== event.slug) {
      return errorResponse(502, "inference_bad_response", "Inference response identity is invalid");
    }
    prediction = predictionResult.data;
  } catch (error: unknown) {
    if (error instanceof InferenceClientError) {
      return errorResponse(error.status, `INFERENCE_${error.status}`, error.message);
    }
    return errorResponse(502, "inference_bad_response", "Inference service returned an invalid response");
  }

  let forecast;
  try {
    forecast = await prisma.forecast.create({
      data: {
        eventId: event.id,
        modelVersion: prediction.modelVersion,
        latencyMs: prediction.latencyMs,
        csiConvlstm: prediction.metrics.convlstm.csi,
        csiPersist: prediction.metrics.persistence.csi,
      },
    });
  } catch {
    return databaseUnavailableResponse();
  }

  return NextResponse.json({ ...prediction, runId: forecast.id });
}

export async function GET(request: Request): Promise<NextResponse> {
  const eventId = new URL(request.url).searchParams.get("eventId") ?? undefined;
  const queryResult = forecastQuerySchema.safeParse({ eventId });
  if (!queryResult.success) {
    return errorResponse(400, "INVALID_QUERY", "Query parameters are invalid");
  }

  try {
    let eventId: string | undefined;
    if (queryResult.data.eventId) {
      const event = await prisma.radarEvent.findUnique({
        where: { slug: queryResult.data.eventId },
      });
      if (!event) {
        return errorResponse(404, "EVENT_NOT_FOUND", "Event not found");
      }
      eventId = event.id;
    }

    const forecasts = await prisma.forecast.findMany({
      where: eventId ? { eventId } : undefined,
      orderBy: { createdAt: "desc" },
    });
    return NextResponse.json(forecasts);
  } catch {
    return databaseUnavailableResponse();
  }
}