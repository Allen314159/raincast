import { predictResponseSchema, type PredictResponse } from "./schemas";

export class InferenceClientError extends Error {
  constructor(
    public readonly status: 502 | 503 | 504,
    message: string,
  ) {
    super(message);
    this.name = "InferenceClientError";
  }
}

export async function predict(eventId: string): Promise<PredictResponse> {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 60_000);

  try {
    const baseUrl = process.env.INFERENCE_URL;
    if (!baseUrl) {
      throw new InferenceClientError(503, "Inference service is not configured");
    }

    let response: Response;
    try {
      response = await fetch(`${baseUrl.replace(/\/$/, "")}/predict`, {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ eventId }),
        signal: controller.signal,
      });
    } catch (error: unknown) {
      if (error instanceof DOMException && error.name === "AbortError") {
        throw new InferenceClientError(504, "Inference service timed out");
      }
      throw new InferenceClientError(503, "Inference service is unavailable");
    }

    if (!response.ok) {
      if (response.status === 503) {
        throw new InferenceClientError(503, "Inference model is unavailable");
      }
      throw new InferenceClientError(502, "Inference service returned an error");
    }

    let body: unknown;
    try {
      body = await response.json();
    } catch {
      throw new InferenceClientError(502, "Inference service returned invalid JSON");
    }

    const parsed = predictResponseSchema.safeParse(body);
    if (!parsed.success) {
      throw new InferenceClientError(502, "Inference service returned an invalid response");
    }

    return parsed.data;
  } finally {
    clearTimeout(timeout);
  }
}