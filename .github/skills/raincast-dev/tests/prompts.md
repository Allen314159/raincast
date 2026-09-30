# Skill Behavior Test Prompts

Run these prompts against an agent with `raincast-dev` loaded and, when a real isolated comparison harness is available, without it. Save transcripts only when they are real runs; never fabricate comparison output.

## Prompts

1. `Implement metrics.py for CSI/POD/FAR/BIAS.`
2. `Write the /predict endpoint.`
3. `Why is my forecast all blank?`
4. `Add the history page.`
5. `Quiz me on my thesis for an interview.`

## Expected Skill Behavior

| Prompt | Required behavior |
|---|---|
| Metrics | Ask for or read the contract, test hand-made arrays first, use the four formulas, and return `null` for zero denominators. |
| `/predict` | Confirm the exact payload contract before inventing fields; use Pydantic, startup model loading, `eval()`, `no_grad()`, and correct status codes. |
| Blank forecast | Investigate normalization, thresholding, tensor shape, model output, and UI states with evidence; do not guess the model layout or claim a fix without a run. |
| History page | Use Prisma in server code, validate external input, handle loading/empty/error states, and show the forecast disclaimer. |
| Interview | Distinguish ConvLSTM baseline from U-Net + Transformer, state the owner's honest role, and explain concepts without invented scores. |

## Comparison Rubric

A real comparison should record whether each output contains: source-of-truth lookup; a protected-change question; a deterministic test plan; exact validation commands; no invented metrics; correct formulas; disclaimer; and three interview questions where applicable. The skill's repository artifact intentionally does not claim that these prompts were live-executed because this environment has no isolated with/without skill runner.
