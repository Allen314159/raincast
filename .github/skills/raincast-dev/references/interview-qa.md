# RainCast Interview Question Bank

Use these as mock prompts. Answers are templates: replace any personal detail with the owner's verified account, and say `TBD` for unknown measurements.

## Thesis and Model

**Q: What did you personally do?**  
A: I focused on literature review, data collection, and training the ConvLSTM baseline. I describe my partner's work separately rather than claiming the whole thesis as my own.

**Q: Why is ConvLSTM a reasonable baseline?**  
A: It combines convolution for spatial structure with recurrent state for temporal sequences, so it is a simple comparison point for radar-frame forecasting. It is a baseline, not the thesis U-Net + Transformer result.

**Q: What does balanced loss address?**  
A: Heavy-rain pixels are sparse compared with non-heavy pixels. A balanced loss gives the minority class enough influence during training. The exact implementation and weights must be confirmed from the thesis or code before stating them.

**Q: Explain CSI, POD, FAR, and BIAS.**  
A: CSI measures overlap while ignoring correct negatives, POD measures how much observed heavy rain was detected, FAR measures the fraction of predicted events that were false alarms, and BIAS compares predicted event frequency with observed event frequency. Zero denominators are `null`.

**Q: What does CSI 0.291 mean here?**  
A: It is the thesis U-Net + Transformer score and must not be presented as the ConvLSTM baseline score served by RainCast.

## Architecture

**Q: Why separate the inference service?**  
A: FastAPI isolates Python and PyTorch dependencies from the Next.js application, lets the web app remain focused on UI and orchestration, and gives the model a clear HTTP boundary. The exact deployment tradeoffs should be described as design reasoning, not as a measured latency claim.

**Q: Why load the model at startup?**  
A: Loading once avoids repeating expensive checkpoint work on every request. `eval()` selects inference behavior and `torch.no_grad()` prevents unnecessary gradient tracking.

**Q: Why use Zod if TypeScript already has types?**  
A: TypeScript types disappear at runtime. Zod checks untrusted request, query, and service-response data before the application relies on it.

**Q: Why Prisma and PostgreSQL?**  
A: Prisma gives typed database access in server code, while PostgreSQL stores durable relational event and forecast data. The exact schema answer must match the project contract.

**Q: What do Docker and CI provide?**  
A: Docker makes the multi-service environment repeatable. CI runs lint, type-checks, tests, and builds on pushes and pull requests so local assumptions are checked before merge.

## Honest Unknowns

When asked about model layout, exact API fields, NaN preprocessing, a measured latency, ownership details, or open questions Q1-Q6, answer: “I have not verified that yet; I would check the project contract or ask the owner rather than guess.”
