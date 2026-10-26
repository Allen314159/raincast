# Audit index

| Report | What it checked | Trust level | Known errors or limits |
|---|---|---|---|
| [A.md](./A.md) | Thesis model and data-contract evidence | Trusted for the source excerpts it records | Does not prove provenance of the local checkpoint. |
| [B.md](./B.md) | Checkpoint compatibility and model geometry | Trusted for measured checkpoint and geometry findings | Scratch reconstruction was not a repository reproduction. |
| [B3.md](./B3.md) | Candidate model screening and checkpoint provenance | Split trust: the second report is plausible; the first is superseded | The first B3 report ("no candidate works") used a faulty decoder sequence. The second B3 report (scratch Candidate B) is plausible but was not reproduced in the repo until Phase 2 and Phase 5. |
| [C.md](./C.md) | Heavy-rain candidate screening | Limited | Heavy-rain counts were computed on the six INPUT frames, shifted by six frames. Do not use its candidate list. |
| [D.md](./D.md) | Raw/archive inventory, checkpoint and preprocessing evidence | Trusted for its measured findings | It lists unresolved provenance, archive conversion, and publishing-permission unknowns. |
| Audit E (referenced, report not present) | Archive/raw time alignment, value scale, and spatial conversion | Trusted as referenced by the plan | The report file is not currently present in `docs/audits/`; its listed residual scale and pre-26-May alignment unknowns remain open. |

Audit reports are evidence, not permission to change protected model, data, or
metric decisions without updating `docs/DECISIONS.md`.
