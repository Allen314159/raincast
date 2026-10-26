# Phase 5 real-run evaluation

Date: 2026-10-26

## Run metadata

| Item | Measured value |
|---|---|
| Checkpoint | `encoder_forecaster_77000.pth` |
| Checkpoint size | 50,587,234 bytes |
| `MODEL_VERSION` | `convlstm-77000` |
| Archive | `nhb_2023_05.npz` |
| Archive month | May 2023 |
| Streamed archive windows | 90 |
| Additional event windows | 3 |
| Total evaluated windows | 93 |
| Archive stride | 50 |
| CPU | AMD Ryzen 5 5600H with Radeon Graphics |
| Installed RAM | 16,483,872,768 bytes (15.35 GiB) |
| Peak inference-service working set | 673,443,840 bytes |

The archive evaluator streamed `nhb_2023_05.npz` and added the three local
event files listed below. Counts were summed across windows before calculating
each metric; per-window scores were not averaged. The local event files are
ignored data generated from archive windows for this run and are not committed.

The primary threshold is **D1 / Singapore**:
`Z = 61.75 * R^1.61`, heavy rain is `R >= 10 mm/h`, and the measured
normalised threshold is `0.6286624231` (reported in the project contract as
`0.6287`). Decoding is `dBZ = 70x - 10` (D2).

The reproduction threshold is **HKO**, used only for the reproduction check:
`Z = 58.53 * R^1.56`, with measured normalised threshold `0.6181969320`
(reported as `0.6182`). The archive is the 512 x 512 RainCast pipeline; the
thesis pipeline used 360 x 360 data.

## Real HTTP service

The service was started with the 77000 checkpoint and the local event
directory. `/health` returned HTTP 200 with `modelLoaded: true` and
`modelVersion: convlstm-77000`. Response sizes below are UTF-8 JSON bytes and
exclude no fields from the response; frame contents were not printed.

| Event | Status | HTTP latency (ms) | Response bytes | Service `latencyMs` | ConvLSTM CSI (+10..+60) | Persistence CSI (+10..+60) |
|---|---:|---:|---:|---:|---|---|
| `2023-05-26-0813` | 200 | 2210.563 | 4775298 | 1930 | 0.469926, 0.282630, 0.197191, 0.166734, 0.121506, 0.105800 | 0.396988, 0.269626, 0.214754, 0.180788, 0.136940, 0.134290 |
| `2023-05-26-1703` | 200 | 1854.433 | 2615528 | 1742 | 0.375656, 0.258649, 0.165927, 0.160099, 0.158087, 0.181142 | 0.318922, 0.210974, 0.146701, 0.112353, 0.103008, 0.050403 |
| `2023-05-28-1903` | 200 | 1685.251 | 1889157 | 1621 | 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000 | 0.000000, 0.000000, 0.000000, 0.022727, 0.000000, 0.000000 |

Five warm HTTP runs of `2023-05-26-0813`, after one warm-up call, had a
median latency of 1852.943 ms and a maximum latency of 2066.030 ms. Peak
process RAM was measured from the Windows process working-set peak counter,
not with `tracemalloc`.

## Primary aggregate: D1 / Singapore

| Model | Lead | CSI | POD | FAR | BIAS |
|---|---:|---:|---:|---:|---:|
| ConvLSTM | +10 | 0.375046 | 0.764902 | 0.576089 | 1.804393 |
| ConvLSTM | +20 | 0.254396 | 0.629938 | 0.700905 | 2.106144 |
| ConvLSTM | +30 | 0.195552 | 0.562422 | 0.769357 | 2.438490 |
| ConvLSTM | +40 | 0.171989 | 0.507183 | 0.793502 | 2.456109 |
| ConvLSTM | +50 | 0.143253 | 0.443486 | 0.825351 | 2.539297 |
| ConvLSTM | +60 | 0.119168 | 0.383577 | 0.852605 | 2.602376 |
| Persistence | +10 | 0.327716 | 0.489264 | 0.501877 | 0.982215 |
| Persistence | +20 | 0.190416 | 0.317233 | 0.677356 | 0.983231 |
| Persistence | +30 | 0.129524 | 0.229666 | 0.770982 | 1.002829 |
| Persistence | +40 | 0.092959 | 0.167080 | 0.826760 | 0.964444 |
| Persistence | +50 | 0.062873 | 0.117749 | 0.881128 | 0.990551 |
| Persistence | +60 | 0.046514 | 0.090393 | 0.912559 | 1.033761 |

## Reproduction check: D2 / HKO (`0.6182`)

This table is separate from the primary table and is not the app's primary
threshold.

| Model | Lead | CSI | POD | FAR | BIAS |
|---|---:|---:|---:|---:|---:|
| ConvLSTM | +10 | 0.386458 | 0.773850 | 0.564339 | 1.776265 |
| ConvLSTM | +20 | 0.267686 | 0.649374 | 0.687087 | 2.075259 |
| ConvLSTM | +30 | 0.205706 | 0.582474 | 0.758716 | 2.414060 |
| ConvLSTM | +40 | 0.178932 | 0.526317 | 0.786721 | 2.467743 |
| ConvLSTM | +50 | 0.148012 | 0.459421 | 0.820774 | 2.563373 |
| ConvLSTM | +60 | 0.123416 | 0.401319 | 0.848734 | 2.653072 |
| Persistence | +10 | 0.340903 | 0.503430 | 0.486392 | 0.980184 |
| Persistence | +20 | 0.202811 | 0.333786 | 0.659257 | 0.979582 |
| Persistence | +30 | 0.141254 | 0.247915 | 0.752831 | 1.003013 |
| Persistence | +40 | 0.103361 | 0.184665 | 0.809871 | 0.971265 |
| Persistence | +50 | 0.073735 | 0.136877 | 0.862188 | 0.993215 |
| Persistence | +60 | 0.053228 | 0.103205 | 0.900966 | 1.042121 |

## Per-event primary tables

The three tables below use D1 / Singapore. Values are in lead order +10, +20,
+30, +40, +50, +60 minutes.

### `2023-05-26-0813`

| Model | CSI | POD | FAR | BIAS |
|---|---|---|---|---|
| ConvLSTM | 0.469926, 0.282630, 0.197191, 0.166734, 0.121506, 0.105800 | 0.660103, 0.380061, 0.284552, 0.243685, 0.191390, 0.177995 | 0.380069, 0.475628, 0.608905, 0.654447, 0.750317, 0.793118 | 1.064800, 0.724793, 0.727576, 0.705203, 0.766532, 0.860369 |
| Persistence | 0.396988, 0.269626, 0.214754, 0.180788, 0.136940, 0.134290 | 0.511456, 0.346887, 0.284661, 0.245412, 0.202137, 0.214115 | 0.360519, 0.452372, 0.533483, 0.592927, 0.701970, 0.735184 | 0.799799, 0.633435, 0.610182, 0.602871, 0.678244, 0.808541 |

### `2023-05-26-1703`

| Model | CSI | POD | FAR | BIAS |
|---|---|---|---|---|
| ConvLSTM | 0.375656, 0.258649, 0.165927, 0.160099, 0.158087, 0.181142 | 0.936047, 0.895222, 0.713287, 0.747126, 0.698387, 0.600636 | 0.614448, 0.733276, 0.822215, 0.830729, 0.830329, 0.794053 | 2.427810, 3.356362, 4.012079, 4.413793, 4.116129, 2.916468 |
| Persistence | 0.318922, 0.210974, 0.146701, 0.112353, 0.103008, 0.050403 | 0.521802, 0.413932, 0.322314, 0.274425, 0.273387, 0.139220 | 0.549372, 0.699163, 0.787866, 0.840167, 0.858159, 0.926778 | 1.157946, 1.375936, 1.519389, 1.716954, 1.927419, 1.901352 |

### `2023-05-28-1903`

| Model | CSI | POD | FAR | BIAS |
|---|---|---|---|---|
| ConvLSTM | 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000 | 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000 | null, null, null, null, null, null | 0.000000, 0.000000, 0.000000, 0.000000, 0.000000, 0.000000 |
| Persistence | 0.000000, 0.000000, 0.000000, 0.022727, 0.000000, 0.000000 | 0.000000, 0.000000, 0.000000, 0.086957, 0.000000, 0.000000 | 1.000000, 1.000000, 1.000000, 0.970149, 1.000000, 1.000000 | 4.466667, 3.045455, 1.218182, 2.913043, 0.632075, 0.250000 |

## GO / NO-GO gate

| Check | Measured value | Result |
|---|---|---|
| No NaN or Inf anywhere | `finite = true` for all 93 evaluated windows and JSON metrics use `null` for zero denominators | GO |
| ConvLSTM CSI above persistence at +30/+40/+50/+60 | D1 differences: +0.066029, +0.079030, +0.080380, +0.072654 | GO |
| Aggregate ConvLSTM CSI decreases with lead | D1: 0.375046 > 0.254396 > 0.195552 > 0.171989 > 0.143253 > 0.119168 | GO |
| HKO CSI is the same order as thesis Table A.2 | HKO +10 ConvLSTM CSI 0.386458 / thesis reference 0.2214 = ratio 1.745520 | GO; this is not called a match |

All four checks passed. No threshold tuning or reprocessing was done to make
the checks pass.

## Thesis reference (checkpoint 89000, different checkpoint, from `outputs/test_metrics.json`)

These are reference values from the thesis evaluator output, not measurements
of checkpoint 77000. The reference checkpoint is 89000 and the thesis
evaluation used a different pipeline.

| Lead | CSI | POD | FAR |
|---|---:|---:|---:|
| +10 | 0.370119 | 0.813344 | 0.595525 |
| +20 | 0.275865 | 0.722222 | 0.691391 |
| +30 | 0.219557 | 0.636712 | 0.749000 |
| +40 | 0.181467 | 0.548415 | 0.786654 |
| +50 | 0.152162 | 0.467047 | 0.815866 |
| +60 | 0.129126 | 0.393302 | 0.838757 |
| Aggregate BIAS | 2.351604 |  |  |

May 2023 membership in the held-out set is documented, but was not verified
for checkpoint 77000. Thesis Table 5.4 persistence (`CSI 0.1595`) used a
360 x 360 pipeline and threshold `0.629`; it is not comparable to the
persistence measured here.
