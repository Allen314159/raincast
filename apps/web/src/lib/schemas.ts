import { z } from "zod";

const sixNumbersSchema = z.array(z.number().finite().nullable()).length(6);
const sixFramesSchema = z.array(z.string().min(1)).length(6);

const modelMetricsSchema = z.object({
  csi: sixNumbersSchema,
  pod: sixNumbersSchema,
  far: sixNumbersSchema,
  bias: sixNumbersSchema,
});

export const forecastRequestSchema = z.object({
  eventId: z.string().trim().min(1),
});

export const predictResponseSchema = z.object({
  eventId: z.string().min(1),
  modelVersion: z.string().min(1),
  thresholdMmPerHour: z.number().finite(),
  leadMinutes: z.tuple([
    z.literal(10),
    z.literal(20),
    z.literal(30),
    z.literal(40),
    z.literal(50),
    z.literal(60),
  ]),
  frames: z.object({
    observed: sixFramesSchema,
    convlstm: sixFramesSchema,
    persistence: sixFramesSchema,
  }),
  metrics: z.object({
    convlstm: modelMetricsSchema,
    persistence: modelMetricsSchema,
  }),
  latencyMs: z.number().int().nonnegative(),
});

export const errorResponseSchema = z.object({
  error: z.object({
    code: z.string().min(1),
    message: z.string().min(1),
  }),
});

export type PredictResponse = z.infer<typeof predictResponseSchema>;