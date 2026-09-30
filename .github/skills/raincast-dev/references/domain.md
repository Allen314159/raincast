# RainCast Domain Facts

## System

RainCast is a portfolio full-stack app for heavy-rain nowcasting over Ho Chi Minh City. The production target described by the project is a ConvLSTM baseline trained from Nha Be radar data on a 360x360 grid. It consumes 6 input frames and produces 6 forecast frames at +10, +20, +30, +40, +50, and +60 minutes. A persistence baseline repeats the last input frame for each forecast lead time.

Do not claim that the repository contains live ingestion, training, or the thesis U-Net + Transformer model. The thesis score `CSI 0.291` belongs to that U-Net + Transformer model, not the ConvLSTM baseline served here.

## Preprocessing

Normalisation:

`x = (clip(dBZ, -10, 60) + 10) / 70`

Inverse:

`dBZ = 70 * x - 10`

Singapore Z-R relation:

`R = (10^(dBZ/10) / 61.75)^(1/1.61)`

Heavy rain is `R >= 10 mm/h`, approximately `34 dBZ`, approximately `0.629` on the normalised scale. Treat the approximation as a documented threshold, not as permission to silently change the formula.

## Metrics

At each lead time, classify pixels using the agreed heavy-rain threshold and count:

- `H`: observed heavy rain and predicted heavy rain
- `M`: observed heavy rain and predicted non-heavy rain
- `F`: observed non-heavy rain and predicted heavy rain

Then calculate:

- `CSI = H / (H + M + F)`
- `POD = H / (H + M)`
- `FAR = F / (H + F)`
- `BIAS = (H + F) / (H + M)`

If a denominator is zero, return `null`. JSON must never contain `NaN` or infinity. Metrics must be reported per lead time, not collapsed into an invented aggregate.

## Evidence Rules

Only report values from a real run. Unknown metrics, test counts, latency, coverage, and deployment state are `TBD`. The limitations section must preserve the documented baseline limitation: over-prediction of heavy rain, `BIAS 2.35` on the thesis test set, and blur at long lead times. Do not transfer any thesis number to a different model or dataset.
