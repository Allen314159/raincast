# RainCast — Development Plan (v2)

> Replaces PLAN v1 · Status date: 2026-10-26 · Owner: Lam My Trang
> Order of authority: `docs/RULES.md` (how) > `docs/PROJECT.md` (what) > `docs/DECISIONS.md` (owner choices) > this file (order of work).
> Every phase has: goal, entry gate, a **prompt to paste into the coding agent**, an **owner review checklist**, and an exit gate.

---

## 0. How to work with this plan

**Loop for every phase**

1. Check the **entry gate**. If it is not met, do not start.
2. Open a fresh agent session. Paste the **Standard Preamble** (section 2), then the **phase prompt**.
3. The agent works on the branch named in the prompt and ends with the **report format** from the preamble.
4. You review with the **phase review checklist** and the **generic review protocol** (section 3). Do not merge on the agent's word alone.
5. Merge only when the **exit gate** is true. Then update the status table below and `docs/DECISIONS.md`.
6. If something fails or looks wrong, paste the agent report plus `git diff --stat main...HEAD` to your "brain" chat for a second opinion.

**One phase = one branch = one PR.** Audits (read-only) produce a report instead of a PR; save each report under `docs/audits/`.

### Status table (update after each phase)

| Phase | Name | Status |
|---|---|---|
| 0 | Evidence closure (audits) | A, B, B3, C, D, E done and thesis PDF read; decisions below await your OK; **next: Phase 1** |
| 1 | Baseline and hygiene (docs only) | not started |
| 2 | Model port (thesis network) | not started |
| 3 | Normalisation, threshold, metrics contract | blocked by D + decisions |
| 4 | Event builder and curated events (local data only) | not started |
| 5 | Real-run and evaluation gate | not started |
| 6 | Web/DB hardening | not started |
| 7 | End-to-end smoke test | not started |
| 8A / 8B / 8C | UI: shell + events page / event page / history page | not started |
| 9 | Docker and CI | not started |
| 10 | Release: deployment decision, README, claims audit | not started |
| 11 | Interview readiness | not started |

```
0 ──► 1 ──► 2 ──► 3 ──► 4 ──► 5 (GATE) ──► 6 ──► 7 ──► 8A ──► 8B ──► 8C ──► 9 ──► 10 ──► 11
            └─(2 may start once 1 is merged; 3 needs the answers from 0/D)
```

**Hard gate:** nothing from Phase 6 onward starts until Phase 5 passes (a real event, the real checkpoint, honest scores).

---

## 1. Current state (what is known, what is not)

### Verified by audits (evidence in `docs/audits/`, save the reports there in Phase 1)

| Fact | Evidence |
|---|---|
| Checkpoint `encoder_forecaster_77000.pth`: 28 float32 tensors, 50,587,234 bytes, 12,643,945 parameters in total, no peephole tensors (`Wci/Wcf/Wco`), no embedded provenance | audits B, B3, D |
| Model was trained on a cloud VM; checkpoint downloaded to the owner's PC. TensorBoard logs run to step 90,000, so `encoder_forecaster_89000.pth` was probably saved on the VM but is not on this PC | owner statement, audit B3 |
| Thesis network is hard-wired to **512×512** input (states 102/34/17; strides 5,3,2 and 2,3,5); it fails at 360×360 | audits A, B |
| Current RainCast `model.py` has **different strides and a different gate order**, outputs raw mean ≈ −0.96 on real data and gives **CSI 0** | audits B, C |
| A scratch reconstruction with thesis geometry, gate order `i,f,g,o`, zero states and no peepholes gave plausible scores on 93 windows of May 2023 (CSI 0.2159 at ≥10 mm/h under the thesis evaluator's threshold; persistence 0.1453; ConvLSTM above persistence at every lead). **Scratch result, not yet reproduced in the repo** (the other B3 report, "no candidate works", used a buggy screen and is not trusted) | scratch audit, repeated in Phases 2 and 5 |
| Peepholes: the thesis source declares `Wci/Wcf/Wco` as `nn.Parameter(torch.zeros(...)).to(device)`. The checkpoint's 12,643,945 parameters equal the documented total and would be 18,303,721 with the 5,659,776 peephole parameters, so the peepholes were not registered or saved in training. **Probable mechanism (inferred, not reproduced on a GPU):** `.to(device)` on a Parameter returns a plain tensor when it copies, so on the GPU run the peepholes stayed constant zeros and never reached the optimizer. On CPU the same code registers them, which is why strict loading into the thesis classes reports 18 missing keys | audit D §5 |
| The executable thesis conversion is `dBZ = 70x − 10`, `x = clip((dBZ+10)/70, 0, 1)`; the evaluator converts rain-rate thresholds to pixels with Z–R **a=58.53, b=1.56** and no mask (all ones). Normalised threshold for 10 mm/h = **0.6181969**; also 0.5 mm/h → 0.3282531, 2 → 0.4624265, 5 → 0.5511102, 30 → 0.7245268. With the thesis text's Singapore pair 61.75/1.61 it is 0.6286624 (the 0.629 used in the thesis and PROJECT.md). The ConvLSTM repo docs say `x = dBZ/70`, but the final thesis PDF (§3.2.1 d) states `(clip(dBZ,−10,60)+10)/70`, matching the code and audit E: **resolved, the +10 form is right** | audit D §1 |
| Raw data on this PC: PPI NetCDF files for **one day only (2023-05-26)**, 144 files, 10-minute spacing (9.95–10.05 min), no duplicates. Each has a 720×720 grid at 0.3333 km (240 km, range 120 km), `DBZ` (float32, NaN where no data; −16 to 59.5 dBZ in frame 1, up to 75 dBZ across the day; 95.4% NaN in frame 1) and a derived `RAIN_RATE` using Marshall–Palmer Z=200R^1.6 (a third Z–R pair, not used by the thesis evaluator) | audit D §2, §4 |
| Monthly raw products exist only as `.rar` files in `E:\PrecipitationNowcasting\Dataset` (no RAR tool was available to list them); `Dataset-Processed` holds only a shortcut; **no code that converts raw to the 512×512 archive exists locally** | audit D §2, §3 |
| Archive `nhb_2023_05.npz`: one array `(4462, 512, 512, 2)`, float32, values in [0, 1], no NaNs, ~88.8% exact zeros in channel 0, no timestamps, 4462 frames instead of the 4464 a complete month would have. Channel 1 contains only 0.0 or 1.0 (136,874,055 ones of 1,169,686,528 values, 11.7%) and channel 0 is non-zero in about 11.2% of values. **Hypothesis (unverified): channel 1 is a validity mask and NaNs became zeros** | audits C, D |
| The thesis code uses channel 0 only and an all-ones mask | audits A, C, D |
| Audit C's "heavy target pixel" counts are **wrong by a 6-frame shift**: its script computed them on the six INPUT frames. Its count for start 3653 (112,979) equals audit D's HKO-threshold count for start 3647, i.e. the same frames seen as targets. **Do not use audit C's candidate list.** Audit D's frame convention is trusted, but its 112,979 count used the HKO evaluator threshold; Phase 4 uses the authoritative Singapore threshold and recomputes the count | my review of audits C and D; Phase 4 diagnostic |
| **Time alignment (audit E):** raw day 2023-05-26 frame k = archive index **3598 + k** (combined correlation 0.996; next best offset 3597 gives 0.975; both halves of the day pick 3598). The count is self-consistent: 3598 + 144 + 720 = 4462, so the two missing frames lie before 26 May and 27–31 May look complete. Indices 3598–3741 (26 May) are verified; 3742 and up (27–31 May) are dated by this arithmetic only; indices below 3598 can be off by up to 2 frames (about 20 minutes) | audit E §2–4 |
| **Value scale (audit E):** `x = (dBZ+10)/70` fits much better than `x = dBZ/70` (sum of percentile errors 0.104 vs 0.497 with the resize hypothesis; 0.063 vs 0.432 with centre crop, which is a poor spatial match). Decisive point: resizing cannot create values above the raw maximum, yet the archive reaches 1.0 where the raw frame maximum is 63 dBZ (0.90 under dBZ/70). Residual: archive P99 (0.883) is higher than `(dBZ+10)/70` predicts (0.72–0.74), unexplained (different pixel subsets or an extra step) | audit E §5 |
| **Spatial conversion (audit E):** full-frame bilinear resize 720×720 → 512×512, identity orientation, NaN as 0, gives Pearson correlation 0.991 (frame k=45); centre crop gives 0.38; flips and transposes are worse. Implied pixel size ≈ 240 km / 512 ≈ 0.469 km (my arithmetic, assumes the whole 720 × 0.3333 km frame was used). Original script still not found | audit E §6 |
| **Channel 1 (audit E):** P(ch1=1 \| ch0>0) = 1.0; P(ch0>0 \| ch1=1) = 0.968 on day 26 and 0.796 over 300 other frames; correlation with the raw non-NaN mask 0.848. Consistent with a "valid data" mask, not proven. Heavy-rain pixels always lie inside it, so ignoring it does not change heavy-rain hits and misses | audit E §7 |
| Local time is UTC+7 (Vietnam). Window start 3647 = 2023-05-26 08:13 UTC (15:13 local), targets 09:13–10:03 UTC; start 3716 = 19:43 UTC | audit E §4 |
| **Thesis PDF, data pipeline (§3.2.1, §3.2.3):** raw 720×720 (0.333 km) → **360×360 by 2×2 average pooling** (0.667 km); `x = (clip(dBZ, −10, 60) + 10) / 70`; **NaN pixels set to 0.0** (no rain); samples of 12 consecutive frames about 10 minutes apart saved as `.npz` with `input` and `target` of shape (6, 360, 360); chronological 70/20/10 split; test set = May–June 2023; case-study events 26/05/2023 and 29/06/2023 (Figures 5.5–5.9). The thesis never mentions a 512×512 grid | thesis PDF |
| **Thesis PDF, threshold (§4.2.3):** heavy rain = R ≥ 10 mm/h with the **Singapore Z–R 61.75/1.61 → 34.0 dBZ → x ≥ 0.629**; the thesis notes Marshall–Palmer would give 39.0 dBZ | thesis PDF |
| **Thesis PDF, ConvLSTM baseline (App. A.3):** encoder–forecaster, B-MSE + B-MAE loss, Adam 1e-4, StepLR γ 0.7 per 20,000 iterations, converged at iteration 89,000 (`encoder_forecaster_89000.pth`). Reported at ≥ 10 mm/h: CSI 0.2214, POD 0.5968, FAR 0.7462, BIAS 2.3516; per lead CSI 0.3701 / 0.2759 / 0.2196 / 0.1815 / 0.1522 / 0.1291. Table 5.4 puts it next to persistence (CSI 0.1595, BIAS 1.005) and the proposed model (CSI 0.2911, BIAS 1.553) | thesis PDF |
| **Comparability caveat:** audits A–E show the baseline was trained and scored on the 512×512 two-channel archives with the evaluator threshold 0.6182 (HKO pair), while the thesis pipeline is 360×360 with threshold 0.629. If Table 5.4 mixes the two, its ConvLSTM column is not like-for-like with the other columns. Needs a check with your thesis partner or advisor; RainCast therefore never compares its numbers with the proposed model's | audits A–E vs thesis PDF |
| Thesis documents the split train 2021-01..2022-11, valid 2022-12..2023-03, test 2023-05..06 (via environment variables not stored with the checkpoint) | audit C |
| `/predict` currently needs `.npz` files with `input` and `target` of shape (6, H, W); no real event file exists in the repo | repo report |

### Not known yet (do not guess)

- The original preprocessing script that made the 512×512 two-channel archives (interpolation library, order of NaN → 0 and resizing, clipping, how channel 1 was built). The thesis describes only the 360×360 average-pooled pipeline.
- Whether thesis Table 5.4's ConvLSTM column was computed on the same sequences, grid and threshold as the other columns (the evidence says it was not). Ask your thesis partner or advisor.
- Where the two missing frames before 26 May are (timestamps below index 3598 can be off by up to 2 frames); whether 27–31 May are truly gap-free (only arithmetic evidence).
- Monthly raw inventory: the `.rar` files could not be listed (no RAR tool installed).
- Why the archive's 99th percentile is higher than the `(dBZ+10)/70` prediction (residual in audit E).
- Whether May 2023 was truly held out when checkpoint 77000 was trained (the thesis test set is May–June 2023, but the training environment variables were not recorded).
- Whether the advisor allows publishing radar data or derived images (Q5).

### Decision log (`docs/DECISIONS.md`: Phase 1 creates it, you fill the Status column)

| ID | Decision | Options | Recommended | Status |
|---|---|---|---|---|
| D1 | Z–R pair for the project's heavy-rain threshold | Singapore 61.75/1.61 (thesis text and PROJECT.md; 34.0 dBZ; 0.6287 normalised, rounded to 0.629 in the thesis) · HKO 58.53/1.56 (the ConvLSTM repo's evaluator; 0.6182) | **Singapore (thesis text)** for everything the app computes and shows, so RainCast agrees with the thesis and PROJECT.md. Compute the HKO threshold only in a labelled reproduction check against thesis Tables A.2–A.4. The difference is small (0.0105 normalised, 0.74 dBZ; the scratch run gave CSI 0.2159 vs 0.2074) | awaiting your OK |
| D2 | Pixel ↔ dBZ decoding | `dBZ = 70x − 10` · `dBZ = 70x` | **`dBZ = 70x − 10`** (thesis §3.2.1 d, executable code, audit E). With Singapore Z–R, x ≥ 0.6287 = 34.0 dBZ = 10 mm/h | **decided (thesis + audit E)** |
| D3 | Checkpoint to serve | 77000 · 89000 | **Serve 77000 as `convlstm-77000`.** Never attach 89000 thesis numbers to it | **decided by owner (2026-10-26)** |
| D4 | Event time | dated frames only · `startTime` nullable | **Curated events only from archive indices ≥ 3598 (26–31 May 2023)**, so every event has a non-null UTC `startTime` computed as 2023-05-26T00:03:03Z + 10 min × (index − 3598). Day 26 (3598–3741) is raw-verified; 27–31 May are "derived from frame-count consistency" and say so in the description. No schema change | awaiting your OK |
| D5 | Public event identifier | slug · database id | Slug everywhere | awaiting your OK |
| D6 | Deployment track | live inference host · replay mode (precomputed) · demo video | Decide in Phase 10 from Q5 and a real RAM test | TBD |
| D7 | Q5 publishing permission (data and derived images) | yes · no · only some events | Ask the advisor in writing | TBD |
| D8 | Event file format | float32 · uint8 quantised | float32 (local-only files, simplest) | awaiting your OK |
| D9 | Which metrics to persist | CSI only · all four | CSI only (matches PROJECT.md), revisit later | awaiting your OK |
| D10 | Grid and pixel size | 512×512 (model) · 360×360 (thesis dataset) | The served model needs **512×512**: the archive is the full 720×720 raw frame bilinearly resized (audit E, correlation 0.991, about 0.469 km per pixel over about 240 km); no resize/pad/crop of archive data. Say plainly that the thesis dataset is 360×360 (2×2 average pooling) and the baseline pipeline differs | decided by evidence |
| D11 | Valid-pixel mask (PROJECT.md §8 "ignoring invalid pixels") | no mask (thesis used all ones; thesis sets NaN to 0.0) · use channel 1 | **No mask**, channel 0 only; remove the "ignoring invalid pixels" sentence from §8. Heavy-rain pixels always lie inside channel 1, so hits and misses would not change | awaiting your OK |
| D12 | How to present baseline numbers | compare with the proposed model's numbers · show only RainCast-measured numbers plus a labelled thesis reference | **Only RainCast-measured numbers** (in `docs/RESULTS.md`) plus the thesis 89000 numbers in a labelled reference table, never side by side with the proposed model's 0.2911, because the pipelines differ (see comparability caveat) | awaiting your OK |

---

## 2. Standard Preamble (paste before EVERY phase prompt)

```text
You are working on RainCast (E:\Project\raincast, Windows/PowerShell). Python interpreter: e:/Project/raincast/.venv/Scripts/python.exe. Before acting, read docs/RULES.md, docs/PROJECT.md, docs/DECISIONS.md and the phase you were given in docs/PLAN.md.

HARD RULES
- Work on the branch named in the task, created from up-to-date main. Never commit to main.
- Never commit radar data (.npz/.npy/.nc), checkpoints (.pth), .env files or secrets. Check `git status` before every commit.
- No new dependency without a one-line justification in the commit message AND in your report.
- Never invent numbers. Every metric, count, size or latency written into code, docs, commits or your report must come from a command you ran; paste the output. If you did not measure it, write TBD.
- Do not guess open questions. If docs/DECISIONS.md marks something TBD that your task needs, STOP and ask me.
- Do not weaken, skip or delete a test/lint/type check to get green. Do not edit a test to match wrong behaviour; explain the conflict instead.
- Stay in scope. List extra findings under "Out of scope findings"; do not fix them.
- Keep code simple and conventional; I must be able to explain every line. Comments explain why, not what.
- Conventional Commits, small commits.

REPORT FORMAT (end every task with exactly these sections)
1. Summary (max 5 lines)
2. Commits (hash + subject)
3. Files changed (output of `git diff --stat main...HEAD`)
4. Commands run with real output (test counts, lint, type-check, build)
5. What you did NOT do and assumptions you made
6. Out-of-scope findings
7. Questions for the owner
```

---

## 3. Generic review protocol (use in every phase)

Do these in order. It takes 15–30 minutes.

1. **Read the report first.** Does it follow the 7 sections? Does every number have pasted command output next to it?
2. **Look at the size of the change.** `git diff --stat main...HEAD`. Is it only the files the phase should touch? A large unexpected diff means scope creep.
3. **Run the checks yourself** (never trust the pasted output alone):
   ```powershell
   cd E:\Project\raincast
   git status --short --branch
   cd apps\web; npm test; npm run lint; npm run typecheck; npm run build; cd ..\..
   & 'e:/Project/raincast/.venv/Scripts/python.exe' -m ruff check services\inference
   & 'e:/Project/raincast/.venv/Scripts/python.exe' -m pytest services\inference
   ```
4. **Safety scan.**
   ```powershell
   git diff --name-only main...HEAD | Select-String -Pattern '\.(npz|npy|nc|pth)$|(^|/)\.env$'
   git diff main...HEAD | Select-String -Pattern 'TODO|FIXME|console\.log|# type: ignore|@ts-ignore|skip\(|xit\(|\.only\('
   ```
   The first must print nothing. The second needs an explanation for every hit.
5. **Tests are the contract.** Open the new tests. Would they fail if the code were wrong? A test that only checks "no exception" is weak. Look for hand-computed expected values.
6. **Ask the agent to explain.** Pick one core file and ask: "Explain this file line by line as if I must present it in an interview. What breaks if line X changes?" If you cannot follow the answer, the code is too clever.
7. **Claims check.** Every number in docs/README/PR text must trace to a command output. Search for numbers you did not see measured.
8. **Decide:** merge, ask for fixes (list them), or reject and re-run with a sharper prompt.

**Universal red flags:** tests edited to fit the code · skipped or loosened checks · numbers without commands · data/checkpoint staged · a "fix" that changes preprocessing formulas without a decision · the agent says "should work" instead of showing output · a diff much larger than the phase.

---

## 4. Phases

---

### Phase 0 — Evidence closure (COMPLETE)

**Goal (reached):** settle what the data is, how it relates to the thesis code, and which frames have which time. Audits A, B, B3, C, D and E are done. Their reports go to `docs/audits/` in Phase 1 (with a README that says which report is trustworthy and which has known errors).

**What the audits settled**

| Question | Result |
|---|---|
| Model | Thesis geometry at 512×512, gate order `i,f,g,o`, no peepholes (constant zeros during training, mechanism inferred); current RainCast `model.py` is wrong |
| Threshold | Thesis text: Singapore 61.75/1.61 → 34.0 dBZ → 0.6287 (0.629). ConvLSTM repo evaluator code: HKO 58.53/1.56 → 0.6182. RainCast uses the thesis text (D1) and shows the other only in a reproduction check |
| Value scale | `x = (dBZ+10)/70`: thesis §3.2.1 d and audit E agree (D2 decided) |
| Grid | Archive = full raw 720×720 frame bilinearly resized to 512×512 (≈ 0.469 km per pixel), NaN → 0 |
| Channel 1 | Probably a validity mask; not used by the thesis; ignored by RainCast (D11) |
| Time | Archive index 3598 + k = raw frame k of 2023-05-26 (verified); 27–31 May by arithmetic; before 26 May ±2 frames |
| Events | Take them from indices ≥ 3598. Audit D's frame convention is start = first input frame and counts the six target frames, but its 112,979 reference used the HKO threshold. Phase 4 recomputes the Singapore-threshold ranking inside indices 3598 to 4461. Audit C's ranking is wrong (it counted input frames) |

**Optional owner actions (do not block Phase 1):**

1. Look on the cloud VM and bucket for `encoder_forecaster_89000.pth`, the training code folder, the shell history with the `NPZ_*_GLOB` variables and the notebook or script that built the 512×512 archives. Copy what you find to your PC (never into git). If you find 89000 or the preprocessing script, tell your brain chat: D2, D3 and D10 may change.
2. Install 7-Zip so the monthly `.rar` files in `E:\PrecipitationNowcasting\Dataset` can be listed. Not required: events come from the archive and only day 26 is verified against raw frames.

**Exit gate:** you approve the "awaiting your OK" rows of the decision log (or change them); the reports are saved. Then Phase 1.

---

### Phase 1 — Baseline and hygiene (docs only, no code changes)

**Goal:** make the repo describe reality: current state of `main`, audit reports saved, decisions recorded, missing project files restored.

**Entry gate:** you copied the audit reports (A, B, B3, C, D) into `docs/audits/` as `.md` files (save the chat text). They contain no radar data.

**Branch:** `docs/baseline`

**Prompt:**

```text
TASK: Phase 1 baseline and hygiene. DOCS ONLY: change no source code, tests, schema or config except .gitignore (if a data pattern is missing).

1. STATE OF MAIN. Report `git status`, `git log --oneline -15`, and whether the web API work (events, forecasts routes, Prisma schema, seed, schemas, inference client) is on main. Run the full checks (web: npm test, lint, typecheck, build; inference: ruff, pytest) and paste counts.
2. KNOWN ISSUES TABLE. Create docs/audits/main-state.md with one row per issue below: status FIXED / OPEN / NOT APPLICABLE, with file:line evidence.
   H1 no usable .npz event; H2 MODEL_VERSION default convlstm-89000 vs local 77000 checkpoint; M1 POST uses slug but GET /api/forecasts filters by database id; M2 invalid-pixel handling vs docs; M3 per_lead_metrics truncates silently with zip; M4 DB errors not mapped to the standard error shape; M5 no check that the inference response eventId equals the requested event; L1 placeholder events in prisma/events.json; L2 unused helpers in model.py; L3 stale README; L4 AGENTS.md missing; plus: Prisma migrations missing, docker-compose.yml missing, UI only a placeholder.
2b. Create docs/audits/README.md: a table of every report in docs/audits (name, what it checked, trust level, known errors). Mark: audit C = heavy-rain counts computed on the six INPUT frames, shifted by 6 frames, do not use its candidate list; first B3 report ('no candidate works') = candidate screen used a faulty decoder sequence, superseded; second B3 report (scratch Candidate B) = plausible but not reproduced in the repo until Phase 2 and Phase 5; audit D and audit E = trusted, with the unknowns they list.
3. Create docs/DECISIONS.md: a table with columns ID, Decision, Options, Recommended, Status, Evidence. Copy rows D1..D11 from section 1 of docs/PLAN.md exactly (including the Status column as written there; D3 is decided: serve checkpoint 77000, version string convlstm-77000). Add the owner's decisions only if I wrote them in the task message below.
4. Create AGENTS.md at the repo root (max 60 lines): what the project is; source-of-truth order (RULES > PROJECT > DECISIONS > PLAN); the hard rules from the Standard Preamble; "learning mode" (explain code on request, simple code, owner must be able to explain every line); where audits live.
5. Update docs/PROJECT.md:
   a. section 4 (open questions): fill Q1..Q6 with the audit evidence (Q1 thesis geometry and gate order from audits B/B3 plus the caveat that provenance is unproven; Q2 layout [T,B,C,512,512]; Q3 the thesis sets NaN pixels to 0.0 (no rain, thesis §3.2.1 d); the archive has no NaNs and shows raw no-data as 0; training used an all-ones mask and ignored channel 1 (binary, probably a validity mask, unverified); Q4 raw output is not bounded, clamp to [0,1]; Q5 TBD; Q6 77000 is the checkpoint we have, 50,587,234 bytes, hosting TBD). Cite docs/audits files.
   b. section 6: fix the repository layout to the real one (app/ not src/app, etc.).
   c. Leave the normalisation text (section 3), the Z-R pair, the threshold, the 360x360 grid and the 0.667 km/pixel claim EXACTLY as they are but add a visible note "UNDER REVIEW - see docs/DECISIONS.md D1/D2/D10". Do not change them yet.
6. Rewrite README.md "Status" so it states only what exists and works today (verified by commands you ran) and what does not (UI, Docker, migrations, real events, deployment). No metrics, no claims about performance.
7. Replace docs/PLAN.md with the file I provide (do not edit it). If I did not provide it, stop and ask.
8. Do not add the thesis PDF to the repo; cite its sections by number in docs (for example "thesis §4.2.3").
```

**Owner review**

- `docs/audits/main-state.md`: spot-check 3 rows by opening the cited files yourself.
- `AGENTS.md`: read all of it; it is the rule file future agents obey.
- `docs/PROJECT.md` diff: only §4, §6 and "UNDER REVIEW" notes should change. No formula may be altered.
- README: no numbers except commands you can reproduce.
- Run the generic safety scan: no data or checkpoint.

**Exit gate:** PR merged; `main` has `AGENTS.md`, `docs/DECISIONS.md`, `docs/audits/*`, honest README.

**If it fails:** if the agent edits code, reject the PR; this phase is docs only.

---

### Phase 2 — Model port (the thesis network)

**Goal:** replace `services/inference/app/model.py` with a faithful port of the thesis geometry and control flow so the 77000 checkpoint produces meaningful forecasts. Input becomes 512×512.

**Entry gate:** Phase 1 merged (so `AGENTS.md` and `DECISIONS.md` exist). Audit D's peephole evidence is in (checkpoint has 12,643,945 parameters, none of them peepholes). If you find on the VM that training code registered peepholes as trainable (or the VM run used a different model file), stop and consult your brain chat.

**Branch:** `fix/model-port`

**Prompt:**

```text
TASK: Phase 2 model port.

BACKGROUND (verified by audits in docs/audits/): services/inference/app/model.py does not match the network that produced encoder_forecaster_77000.pth (real data gave CSI 0). The checkpoint has 28 tensors and no Wci/Wcf/Wco. An independent scratch run with thesis geometry, gate order i,f,g,o, zero initial states and no peepholes produced plausible scores. The thesis network requires [T,B,C,H,W] = [6,B,1,512,512].

1. READ, DO NOT CHANGE, these thesis files: nowcasting/models/convLSTM.py, encoder.py, forecaster.py, model.py, experiments/net_params.py (path: E:\PrecipitationNowcasting\ConvLSMT). Port exactly: layers, kernel/stride/padding/output_padding, LeakyReLU slope, how encoder states feed the forecaster (order and any reversal), the forecaster's input at each step, how six outputs are produced. Use gate chunk order i, f, g, o. Omit peepholes ONLY if the evidence shows they were constant zeros. Evidence so far (docs/audits/D-data-contract.md): the thesis declares Wci/Wcf/Wco as nn.Parameter(torch.zeros(...)).to(cfg.GLOBAL.DEVICE); the checkpoint's 12,643,945 parameters equal the documented total and exclude the 5,659,776 peephole parameters. Add a 5-line CPU demonstration to your report that `nn.Parameter(torch.zeros(1)).to(torch.float64)` is NOT an nn.Parameter (a copying .to() returns a plain tensor; expected output False, run it and paste the result), and label the GPU explanation as 'inferred mechanism, not reproduced on a GPU'. If anything in the thesis code contradicts constant-zero peepholes, stop and report.
2. Rewrite services/inference/app/model.py. State-dict key names must equal the 28 checkpoint keys (strict=True must load). Input must be [6,B,1,512,512]; any other spatial size raises ValueError with a clear message. Remove make_layers/activation/Predictor only after proving nothing imports them.
3. Update main.py and schemas: events are float32 (6,512,512) with finite values in [0,1]; keep 404/422/503 behaviour and the whitelist of existing .npz files. Make MODEL_VERSION required whenever MODEL_PATH is set (no default); update .env.example (example value convlstm-77000) and /health accordingly. Keep clamping predictions to [0,1] after the forward pass.
4. per_lead_metrics must raise on mismatched lengths/shapes instead of silently truncating (use strict checks, not zip).
5. TESTS (CI must not need the real checkpoint or real data): (a) the recurrent cell against a hand-computed tiny example proving gate order i,f,g,o; (b) a randomly initialised model on [6,1,1,512,512] returns (6,1,1,512,512) finite values; (c) wrong spatial size raises ValueError; (d) the model's state_dict keys and shapes equal the hard-coded expected list of the 28 checkpoint keys; (e) update /predict tests and helpers to 512x512 stub events; (f) per_lead_metrics raises on mismatch.
6. LOCAL GOLDEN CHECK (not in CI): services/inference/scripts/verify_against_thesis.py; reads THESIS_REPO and MODEL_PATH from the environment. It loads the checkpoint into the new RainCast model and into the thesis classes (on CPU the thesis classes register the peepholes as Parameters, so load with strict=False and print the missing keys: 18 are expected; the peepholes stay at their zero initial value), runs one fixed-seed random [6,1,1,512,512] input through both, and prints max and mean absolute difference. Run it and paste the output. Target max abs diff < 1e-5. If larger, locate the first diverging layer by comparing intermediates; do not hack around it.
7. Run ruff, pytest and the web checks; paste counts. In docs/PROJECT.md update only the model description, the 512x512 model-input note and MODEL_VERSION. Leave normalisation/Z-R/threshold as UNDER REVIEW.
8. If the checkpoint and one real test window are available locally (E:\PrecipitationNowcasting\...), run one real forward pass and report the raw output min/max/mean and wall time. State which window.
```

**Owner review**

- Run the golden check yourself: `verify_against_thesis.py` with `THESIS_REPO` and `MODEL_PATH` set. You want `max abs diff < 1e-5`. Anything bigger is a failed phase.
- Open `model.py` next to the thesis `convLSTM.py`, `encoder.py`, `forecaster.py`. Check by eye: gate order, strides (5,3,2 / 2,3,5), `output_padding=2`, activation slope, state handoff.
- Ask the agent: "Explain how the six forecast frames are produced, step by step, and why zero initial states are correct here."
- The gate-order test must fail if you swap two chunks. Try it: swap two names in `model.py` and run the test, then undo it.
- Real forward pass: raw output should now be near [0, 1], not −0.96 on average.

**Exit gate:** golden diff < 1e-5; strict load passes; ruff/pytest/web checks green; no data or checkpoint committed.

**If it fails:** if the golden check diverges, paste the report to your brain chat with the first differing layer. Do not accept "close enough".

---

### Phase 3 — Normalisation, threshold and metrics contract

**Goal:** one place in the code defines how a pixel becomes dBZ and rain rate, and which pixel value counts as "heavy rain"; renderer and metrics use it; docs match.

**Entry gate:** Phase 2 merged; D1 and D2 filled in `docs/DECISIONS.md`.

**Branch:** `fix/preprocess-contract`

**Prompt:**

```text
TASK: Phase 3 preprocessing contract. Implement what docs/DECISIONS.md D1 (Z-R pair) and D2 (pixel<->dBZ decoding) say. If either is TBD, STOP and ask.

1. In services/inference/app/preprocess.py define named constants (MAX_DBZ, DBZ_OFFSET or equivalent for D2, two named Z-R pairs SINGAPORE=(61.75, 1.61), used by the app per D1, and HKO_EVALUATOR=(58.53, 1.56), used only for the reproduction check against thesis numbers, and HEAVY_RAIN_MM_H=10) and small pure functions: normalised->dBZ, dBZ->rain rate, heavy_rain_mask (rain >= threshold), and the normalised pixel threshold for a given rain rate. One definition only; render.py and metrics.py must use these, no duplicated numbers.
2. TESTS with hand-computed values (write the arithmetic in the test comment): round trip pixel->dBZ->pixel; the heavy-rain pixel threshold with the +10 decoding: for SINGAPORE 10 mm/h -> dBZ 34.0063696 -> x 0.6286624231 (from audit D, which also gave 0.4858 for the wrong dBZ/70 decoding; do not use it); for HKO_EVALUATOR (values measured by audit D from the thesis code) 0.5 mm/h 0.3282531044, 2 mm/h 0.4624264739, 5 mm/h 0.5511102473, 10 mm/h 0.6181969320, 30 mm/h 0.7245268116; use tolerance 1e-6 and write the formula x = (10 b log10(R) + 10 log10(a) + 10) / 70 and one hand calculation in the test comment; thresholds for 0.5, 2, 5, 30 mm/h; values just below/above the threshold; array shapes preserved; no NaN produced. Update existing tests that encoded the old 0.629 value only if D1/D2 change it, and say so explicitly in the report.
3. render.py must decode with the same constants (colour scale in dBZ). Add a test that a pixel at the threshold maps to the colour bin you document.
4. LOCAL VERIFY (not CI): services/inference/scripts/verify_threshold_against_thesis.py imports only the thesis nowcasting/utils.py conversion functions (from THESIS_REPO) and prints a table: rain rate (0.5, 2, 5, 10, 30) -> thesis normalised threshold vs RainCast normalised threshold, once with the thesis default pair (58.53, 1.56) and once calling the thesis function with a=61.75, b=1.61 (it accepts a and b). If the thesis import fails because of missing packages, report it and stop; do not edit the thesis repo. Run it and paste the table.
5. Update docs/PROJECT.md sections 3 and 8: replace the "UNDER REVIEW" notes with the decided formulas, the decided Z-R pair, the exact threshold value, and the statement that thesis numbers belong to checkpoint 89000 and a different checkpoint (77000) is served. Also state that the thesis ConvLSTM numbers come from the 512x512 archive pipeline scored at threshold 0.6182, while the thesis' own pipeline is 360x360 with threshold 0.629, so they are not like-for-like with the proposed model's numbers. Replace the 360x360 and 0.667 km/pixel claims with: model grid 512x512; the archive is the full raw 720x720 frame bilinearly resized to 512x512 (audit E, correlation 0.991, about 0.469 km per pixel over about 240 km), original preprocessing script not found. State the decoding dBZ = 70x - 10 as supported by audit E. In section 8 delete the sentence about ignoring invalid pixels (D11: no mask, as in the thesis evaluator).
6. Do not change /predict's response shape in this phase.
```

**Owner review**

- Open the verify table: RainCast and thesis normalised thresholds should be identical (or the difference must be explained and approved by you).
- Check there is exactly one definition of each constant: `git grep -n "58.53\|61.75\|1.56\|1.61\|70.0\|10.0" services/inference/app`.
- Read the hand-computed comments in the tests. Check one calculation yourself with a calculator.
- `PROJECT.md` §3 and §8 must say the same thing as the code.

**Exit gate:** thresholds identical to the thesis evaluator's (or an approved documented difference); all checks green.

**If it fails:** if thresholds differ and D1/D2 seem wrong, stop and revisit audit D.

---

### Phase 4 — Event builder and curated events (local data only)

**Goal:** turn the 9 GB monthly archive into a small set of valid event files, selected without looking at model results.

**Entry gate:** Phase 3 merged; D4 and D8 decided; audit D has the candidate ranking and (if verified) timestamps.

**Branch:** `feat/event-builder`

**Prompt:**

```text
TASK: Phase 4 event builder. Data files stay LOCAL and git-ignored. Env var NHB_ARCHIVE_DIR points to E:\PrecipitationNowcasting\NhaBe-npz.

1. services/inference/scripts/build_event.py: CLI args: --archive <path to nhb_YYYY_MM.npz> --start <frame index> --slug <slug> [--channel 0]. It streams the zip member radar_sequence.npy frame by frame (never loads the whole array; RAM is about 2 GB), reads 12 consecutive frames, takes the channel, asserts finite, range [0,1], shape (512,512), splits into input (first 6) and target (last 6), and writes services/inference/data/events/<slug>.npz with float32 arrays input and target of shape (6,512,512) (per D8). Put the pure logic in a function that takes already-read frames, so it can be unit-tested with tiny arrays; the CLI enforces 512.
2. services/inference/scripts/select_events.py: scans the archive (stride 1, streaming) and prints candidate windows with their heavy-rain fraction in the six target frames (threshold from preprocess.py), keeping windows at least 24 frames apart. Selection must NOT use model predictions. Index convention (write it in the script docstring): start = index of the FIRST input frame; input frames are start..start+5; target frames are start+6..start+11; the heavy-rain count is taken on the six TARGET frames only. Add a regression test with a hand-made array where the input frames are heavy and the target frames are not (count must be 0) and the reverse, because a previous audit counted the wrong frames. Sanity target: with the D1/D2 Singapore threshold the best window should be start 3647 with 98,718 heavy target pixels. If the result differs, investigate the calculation before choosing events.
3. Per D4, consider only windows whose 12 frames all lie in archive indices 3598..4461 (26-31 May 2023). Choose 8-10 events by heavy-rain-fraction quantiles of that range: 3 high, 3 medium, 2-3 low but non-zero, at least 2 of them inside day 26 (indices 3598..3741, raw-verified). Time of an event = 2023-05-26T00:03:03Z + 10 min x (start index - 3598), start index = first input frame; round to the minute and keep UTC. Print the table of chosen events (slug, start index, UTC time, local time UTC+7, heavy fraction, time basis: "raw-verified" for 3598..3741, "derived from frame-count consistency" above). For events inside day 26 also cross-check the computed time against the raw file names in E:\PrecipitationNowcasting\ConvLSMT\nha-be-dataset\20230526 and report the difference in seconds. Slug format: YYYY-MM-DD-hhmm in UTC (for example 2023-05-26-0813). The heaviest day-26 window must be included: 26 May 2023 is also the thesis case-study date (thesis Figures 5.5-5.8, test set); do not claim your frames equal the thesis figure unless the owner confirms the figure's timestamp.
4. Write services/inference/data/events/manifest.json (git-ignored) AND generate apps/web/prisma/events.json (committed) from the same chosen list: slug, name (neutral, e.g. "Nha Be radar, May 2023, window w3653"), startTime (ISO UTC, never null), description (factual only: radar product, UTC and local time, archive start index, time basis, measured heavy-rain fraction; no invented place names). Remove the three placeholder events.
5. services/inference/scripts/check_events.py: verifies every slug in apps/web/prisma/events.json has a valid .npz with the right keys/shape/dtype/range and every .npz has a manifest entry; exits non-zero on mismatch.
6. Tests for the pure logic (shape/range/NaN failures, correct split, heavy-fraction computation on a hand-made array). CI must not need archives.
7. Confirm with `git status` that no .npz/.npy is staged; the .gitignore must cover services/inference/data/.
8. Report: the events table, file sizes of the built events (measured), build time per event, and the output of check_events.py.
```

**Owner review**

- Run `check_events.py` yourself. Open one event in Python:
  ```powershell
  & 'e:/Project/raincast/.venv/Scripts/python.exe' -c "import numpy as np; z=np.load('services/inference/data/events/<slug>.npz'); print({k:(z[k].shape,z[k].dtype,float(z[k].min()),float(z[k].max())) for k in z.files})"
  ```
- Look at the images: render two events with `render.py` (or ask the agent) and check they look like rain fields, not noise or blank.
- Check the selection was by heavy-rain quantiles, not by "model does well". This stops cherry-picking.
- `events.json`: no invented dates, no place names the data does not support.
- `git status` must show zero data files.

**Exit gate:** 8–10 events built locally; `check_events.py` passes; only the manifest JSON and scripts committed.

**If it fails:** if streaming is too slow or memory-heavy, ask for a one-time conversion to an uncompressed `.npy` in a scratch folder (outside git).

---

### Phase 5 — Real-run and evaluation gate (GO / NO-GO)

**Goal:** prove with real data that the app's inference path gives honest, plausible results, and record measured numbers.

**Entry gate:** Phase 4 merged; the checkpoint and events exist locally.

**Branch:** `feat/eval-real`

**Prompt:**

```text
TASK: Phase 5 real-run evaluation. Local only; nothing in CI may need the checkpoint or data.

1. Start the inference service for real: MODEL_PATH=<77000 checkpoint>, MODEL_VERSION=convlstm-77000, events dir with the Phase 4 events. Call GET /health and POST /predict for 3 chosen events through the real HTTP service (not TestClient). Report status, latencyMs, response size in bytes, and the 6 CSI values per model for each (convlstm, persistence). Never print base64 frames.
2. Write services/inference/scripts/eval_archive.py: streams nhb_2023_05.npz, takes windows with a fixed stride (default 50) plus the Phase 4 events, runs ConvLSTM (the app's model code, same preprocess and metrics modules as the service) and persistence, and aggregates counts over all windows (sum hits/misses/false alarms per lead, then compute CSI/POD/FAR/BIAS; do not average per-window scores). Compute every metric at BOTH heavy-rain thresholds: the primary one (D1, Singapore, 0.6287) and the thesis-evaluator one (HKO, 0.6182) used only for the reproduction check. Output JSON to a git-ignored path.
3. Create docs/RESULTS.md from that JSON. It must contain: date, checkpoint filename and size, MODEL_VERSION, archive month, number of windows and stride, threshold definition (D1/D2), CPU model and RAM (measured), per-lead CSI/POD/FAR/BIAS for ConvLSTM and persistence, and the three per-event tables. Also a separate, clearly labelled table "Thesis reference (checkpoint 89000, different checkpoint, from outputs/test_metrics.json)". State that May 2023 membership in the held-out set is documented but not verified for checkpoint 77000. State that thesis Table 5.4's persistence (CSI 0.1595, 360x360 pipeline, threshold 0.629) is not comparable to persistence measured here, and show the reproduction-check table (threshold 0.6182) separately from the primary table.
4. Latency: median and max of 5 warm runs of one /predict call (after one warm-up call), plus peak process RAM measured with an OS-level tool (not tracemalloc, which does not see PyTorch tensors).
5. GO/NO-GO checks, printed as a table with measured values: (a) no NaN or Inf anywhere; (b) ConvLSTM CSI above persistence at +30, +40, +50, +60 min in the aggregate; (c) aggregate CSI decreasing with lead time; (d) at the thesis-evaluator threshold the aggregate ConvLSTM CSI is within the same order as thesis Table A.2 (0.2214; state the ratio; do not call it matching; those numbers come from checkpoint 89000). If any check fails, say so plainly and stop; DO NOT tune, change thresholds or reprocess data to make it pass.
6. Do not edit the README or PROJECT.md metrics in this phase; RESULTS.md is the only place for numbers.
```

**Owner review**

- Re-run `eval_archive.py` yourself (it takes a while) and compare with `RESULTS.md`: numbers must match exactly.
- The GO/NO-GO table must contain measured values, not words.
- Compare with the scratch result from the earlier audit (CSI 0.2159 at ≥10 mm/h under thesis threshold; persistence 0.1453). Small differences are fine if the threshold or windows differ, but the agent must explain them.
- Check the thesis table is labelled as a different checkpoint.
- RAM and latency: these decide whether Phase 10 can use a hosted CPU instance.

**Exit gate (GO):** all checks pass, `RESULTS.md` merged. **Hard gate for Phase 6.**

**If it fails (NO-GO):** do not continue. Paste the report to your brain chat. Likely causes to investigate, in order: normalisation scale (D2), channel (D3 audit), event window shape, model port diff.

---

### Phase 6 — Web/DB hardening

**Goal:** make the API contract consistent, safe and reproducible, and real against PostgreSQL.

**Entry gate:** Phase 5 GO; PostgreSQL available locally (installed, or `docker run postgres` if Docker works) and a `DATABASE_URL` in `.env`.

**Branch:** `fix/web-api-contract`

**Prompt:**

```text
TASK: Phase 6 web/DB hardening in apps/web. Follow docs/RULES.md section 3 (strict TS, Zod on all external input, Prisma server-side only).

1. Identifier (D5 = slug): POST /api/forecasts takes { eventId: <slug> }. GET /api/forecasts?eventId=<slug> must resolve the slug to the event, then filter by its database id. Unknown slug -> 404 with the standard error shape. Update schemas and tests; add a regression test for the old mismatch first.
2. Response identity: after calling the inference service, verify the response eventId equals the requested slug; if not return 502 with code "inference_bad_response" and DO NOT save a run. Also verify modelVersion is a non-empty string.
3. Error mapping: Prisma errors in all routes (events, events/[slug], forecasts) return 503 { error: { code: "database_unavailable", message } } without leaking connection strings; log a short server-side message (never secrets, never request bodies).
4. Payload limits: reject POST bodies over a small limit (state the number you chose and why) with 413 in the standard error shape.
5. startTime stays required (D4: curated events are all dated). Do not change the schema for it; add a test that the seed rejects an event without startTime.
6. Seed: prisma/seed.ts reads apps/web/prisma/events.json (Phase 4). Remove any remaining placeholder logic.
7. Migrations: create the initial migration (`npx prisma migrate dev --name init`) against my local PostgreSQL and commit the prisma/migrations folder. Run the seed. Show the counts with `npx prisma studio` alternative: a small script or psql query showing row counts per table.
8. Tests (Vitest, mocks for Prisma and the inference client as today): slug resolution, unknown slug 404, identity mismatch 502 and nothing saved, DB error 503, oversized body 413, startTime null handling if applicable. Optional DB integration test only when DATABASE_URL_TEST is set; skipped otherwise, so CI does not need a database.
9. Update docs/PROJECT.md sections 7.3 and 7.4 to match exactly (error codes, identifier, nullable fields). Add the new error codes to a short table.
```

**Owner review**

- Run the tests plus, once, the DB integration test with your local PostgreSQL.
- Open `forecasts/route.ts` and trace one POST by hand: validate → find event → call inference → check identity → save → return. Ask the agent to explain each early-return and its status code.
- Check the 404/502/503/413 test cases really assert the standard error JSON shape.
- Check the migration folder is committed and `schema.prisma` is unchanged except where D4 says.
- The error message must never contain `DATABASE_URL`: `git grep -n "DATABASE_URL" apps/web/app`.

**Exit gate:** all web checks green; migration committed; seed produces your real events; PROJECT.md §7 matches.

**If it fails:** if migrations fail on your PostgreSQL version, paste the exact error; do not let the agent switch to `db push` silently.

---

### Phase 7 — End-to-end smoke test

**Goal:** show web → inference → database works together on one real event and that failure paths behave.

**Entry gate:** Phase 6 merged; inference service runs with the real checkpoint; PostgreSQL seeded.

**Branch:** `chore/e2e-smoke`

**Prompt:**

```text
TASK: Phase 7 end-to-end smoke test. No new dependencies (use Node 18+ fetch).

1. scripts/smoke-e2e.mjs at the repo root. Inputs from env (WEB_URL default http://localhost:3000, INFERENCE_URL default http://localhost:8000). Steps with PASS/FAIL lines: (a) inference GET /health has modelLoaded true and a non-empty modelVersion; (b) GET /api/events returns at least one event; (c) POST /api/forecasts for the first event returns 200 with 6 observed/convlstm/persistence frames, leadMinutes [10..60], six metric values per series (null allowed, never NaN), a runId, and latencyMs; (d) GET /api/forecasts?eventId=<slug> contains that runId; (e) unknown slug -> 404 with the standard error shape; (f) invalid JSON body -> 400. Never print base64 frames; print sizes and timings only. Exit code non-zero if any step fails.
2. Failure-mode instructions in docs/ (a short "docs/SMOKE.md"): how to run the script, and how to manually verify inference-down (expect 503) and database-down (expect 503) by stopping the services; do not automate stopping them.
3. Run it with all three services up and paste the full output. Run the manual failure checks and paste statuses.
4. Report measured end-to-end time and response size.
```

**Owner review**

- Start the three services in three terminals yourself and run `node scripts/smoke-e2e.mjs`.
- Stop the inference service and repeat the POST: you must see 503 in the standard error shape. Do the same with the database.
- Open the database and check the saved run row has `modelVersion = convlstm-77000` and CSI arrays of length 6.
- The script must not print or log frames.

**Exit gate:** all PASS lines yourself; failure modes verified; `docs/SMOKE.md` merged.

**If it fails:** the first failing line says which layer; do not move on to UI.

---

### Phase 8A — UI shell and events page

**Goal:** app layout, the mandatory disclaimer, and the events page with loading/empty/error states.

**Entry gate:** Phase 7 merged. Take a screenshot of the current placeholder page for comparison.

**Branch:** `feat/ui-events`

**Prompt:**

```text
TASK: Phase 8A UI shell and events page (apps/web). Server Components by default; "use client" only where interaction needs it (RULES section 3). Tailwind only; no UI library; no new dependencies.

1. Layout: header with the project name, nav links Events and History, and a footer. A visible banner component on every page that shows forecasts or links to them with exactly this text: "Research demo — not an operational weather forecast." Add a short "About / Limitations" section on the events page: baseline ConvLSTM only, checkpoint served is 77000, thesis numbers are for a different checkpoint, over-prediction of heavy rain expected (state only what docs/RESULTS.md measured; if it is not measured write nothing).
2. Events page (/): fetch events on the server from the database through Prisma (not by calling your own HTTP API). Cards show name, date (if startTime is null show "time not verified"), description, and a link to /events/<slug>. Handle: empty list (clear message), database error (clear error state, no stack traces), loading (use loading.tsx).
3. Keyboard accessibility: cards are links with visible focus rings; correct heading levels; colour contrast OK in light and dark mode.
4. Pure helper(s) for date display with Vitest tests (null date, ISO string). Component tests only if existing dependencies allow; otherwise list manual test steps.
5. Provide screenshots (desktop width and a 375px mobile width) of: populated page, empty state (temporarily with an empty database in your local environment, then restore), error state. Save them to docs/screenshots/ only if each is under 300 KB; otherwise report sizes and ask.
```

**Owner review**

- Open the site yourself at desktop and phone width (browser dev tools).
- Test the empty and error states by stopping the DB or truncating the table, then restore.
- Tab through the page with the keyboard only.
- Check the disclaimer text is exactly the required sentence.
- Check the page reads from Prisma on the server, not by `fetch("/api/events")` from the browser.

**Exit gate:** checks green; screenshots show all three states; disclaimer present.

**If it fails:** if the agent adds a UI library or chart dependency, reject; use plain Tailwind.

---

### Phase 8B — Event page (the core feature)

**Goal:** run a forecast, show three panels, a lead-time slider, metrics and a CSI chart.

**Entry gate:** Phase 8A merged.

**Branch:** `feat/ui-event-page`

**Prompt:**

```text
TASK: Phase 8B event page /events/[slug] (apps/web). No new dependencies; draw the chart with inline SVG.

1. Server part: load the event by slug (Prisma); unknown slug -> notFound(). Client part (small, separated): a "Run forecast" button that POSTs to /api/forecasts with { eventId: slug }.
2. States: idle, loading (explain inference can take seconds; the button is disabled; spinner with text), success, and error (show the standard error message and a retry button). Map 404/503/504/502 to human messages.
3. Success view: lead-time slider (native <input type=range>, steps +10..+60, with a visible label "+30 min" and aria-valuetext) controlling three panels side by side (stack on mobile): Observed | ConvLSTM | Persistence. Frames are base64 PNGs shown with <img> and alt text. A colour legend (dBZ colour stops copied from services/inference/app/render.py into a small typed constant with a comment "must match render.py"; no invented numbers). Show CSI/POD/FAR/BIAS for the selected lead for both models; null prints "—" with a tooltip "no heavy rain in this frame or no forecast heavy rain (undefined)". Show latency and run id.
4. CSI-vs-lead line chart (both models, 6 points, null points break the line; axes labelled; accessible title/desc; works at 375px width).
5. Disclaimer banner from 8A is visible; limitations text links to docs/RESULTS.md values only if they were measured.
6. Pure helpers (metric formatting, chart point building, error mapping) in src/lib with Vitest tests including nulls and out-of-range input. Route handlers need no change; if you think they must change, stop and ask.
7. Provide screenshots: idle, loading (artificially slowed), success at two lead times, error (inference service stopped), desktop and 375px. Report total response size and time to first render after clicking.
```

**Owner review**

- Run the three services and click through: run, slide to each lead time, check CSI numbers against the chart and against the smoke script output for the same run.
- Stop the inference service and click "Run forecast": a friendly error and retry button appear.
- Keyboard only: Tab to the slider, use arrow keys; a screen-reader label like "+30 min" exists (inspect aria attributes).
- Legend colours must match `render.py`: compare visually on a dense-rain event.
- Every panel needs the same lead time at the same time; check observed vs persistence at +10 are visually similar (persistence at +10 should be close to the last input).
- Chart: check one point against the numbers shown in the metrics table.

**Exit gate:** checks green; manual flow works; screenshots for all states.

**If it fails:** a frozen UI during inference or panels that do not change with the slider are blockers.

---

### Phase 8C — History page and polish

**Goal:** a table of saved runs, final accessibility and responsive pass.

**Entry gate:** Phase 8B merged; several saved runs exist in your database.

**Branch:** `feat/ui-history`

**Prompt:**

```text
TASK: Phase 8C history page /history (apps/web). Server Component reading from Prisma; no new dependencies.

1. Table of saved runs, newest first: event name (link), created time, latency (ms), model version, CSI at +30 min for ConvLSTM and persistence (null as "—"). Optional filter by event via query param ?event=<slug> validated with Zod (invalid -> ignored with a visible note, unknown slug -> empty state message).
2. Pagination or a hard limit (state the number) so the page stays fast.
3. States: empty ("No runs yet" with a link to the events page), database error. Responsive: the table scrolls inside its own overflow container on mobile.
4. Accessibility: semantic table (caption, th scope), sortable controls are NOT required. Contrast and focus visible.
5. Tests for any helper (time formatting, CSI-at-+30 extraction from the stored JSON, tolerant of null and malformed JSON arrays).
6. Final polish pass across all pages: heading hierarchy, page titles/metadata, no console errors in the browser, Lighthouse accessibility score reported if you can run it (paste the score; do not claim one you did not measure).
7. Screenshots: populated, empty, filtered, mobile.
```

**Owner review**

- Run three forecasts, open `/history`, check values match what the event page showed for the same runs.
- Query a bad `?event=` value; the page must not crash.
- Open the browser console on every page: it should have no errors.
- Resize to 375px: no horizontal scroll of the whole page.

**Exit gate:** all UI states verified by you; checks green.

**If it fails:** history showing the wrong CSI column (e.g., the +10 value) is the classic bug; compare against the database row.

---

### Phase 9 — Docker and CI

**Goal:** `docker compose up` brings up web, API, database from a clean clone; CI covers both apps and the Docker files.

**Entry gate:** Phase 8C merged. Docker Desktop works on your PC (`docker --version`; `docker run hello-world`).

**Branch:** `chore/docker-ci`

**Prompt:**

```text
TASK: Phase 9 Docker and CI.

1. apps/web/Dockerfile: multi-stage, pinned base image tag, non-root user, runs prisma migrate deploy on start (or via an entrypoint) then next start. services/inference/Dockerfile: pinned base image, CPU-only PyTorch (use the CPU wheel index in requirements/Docker command, with a one-line justification), non-root user, uvicorn. Add .dockerignore files (exclude node_modules, .venv, data, checkpoints, .env, .git).
2. docker-compose.yml: services web, api, db (postgres, pinned tag, named volume, healthcheck). The checkpoint and event files are NEVER baked into images; mount them read-only from host paths given in .env (MODEL_HOST_DIR, EVENTS_HOST_DIR). api reads MODEL_PATH, MODEL_VERSION; web reads DATABASE_URL, INFERENCE_URL (service name, not localhost). Use healthchecks and depends_on conditions.
3. .env.example updated so that `copy .env.example .env` then `docker compose up --build` starts all three even when no checkpoint/data is mounted: the web app lists events, /health shows modelLoaded false, and POST /api/forecasts returns the standard 503. Document this behaviour.
4. CI (.github/workflows/ci.yml): keep web and api jobs; add a job that runs `docker compose config -q` and builds both images (no push). CI must not need the checkpoint or data. Do not disable or skip any check.
5. README: a "Run with Docker" section with the exact commands, how to mount the checkpoint and events, and expected output of the smoke script against the compose stack.
6. Run it for real: from a clean clone of the repo in a temporary folder, `docker compose up --build`, then run scripts/smoke-e2e.mjs against it (with checkpoint and events mounted). Paste the steps, the output, image sizes (docker images) and cold-start time. Report anything that failed.
```

**Owner review**

- Clone the repo fresh into another folder, copy `.env.example` to `.env`, run `docker compose up --build`. This is the real test.
- Run the smoke script against the compose stack with and without the mounts.
- `docker images`: note the sizes; PyTorch images are large, which matters for hosting.
- Check `docker history` / `docker run --rm <image> ls /app` to prove no checkpoint or `.env` is inside an image.
- Push the branch and look at the GitHub Actions run: all jobs green.

**Exit gate:** clean-clone compose works as documented; CI green on the PR.

**If it fails:** do not accept "works on my machine"; it must work from the fresh clone.

---

### Phase 10 — Release: deployment decision, README, claims audit

**Goal:** decide honestly how the demo is shown, and make every public statement traceable.

**Entry gate:** Phase 9 merged; advisor answer on Q5 (D7) received in writing, even if "no".

**Branch:** `docs/release` (plus `feat/replay-mode` only if track B is chosen)

**Decision tree (you decide; write it into D6):**

| Track | Condition | What you do |
|---|---|---|
| A. Live inference | Q5 allows, and a hosted CPU instance with enough RAM actually runs `/predict` (measured with the real checkpoint) | Deploy web (Vercel), database (Neon), inference (Docker host). Check free-tier limits yourself on the day. |
| B. Replay mode | Q5 allows derived images/metrics for a few events, but no suitable host | Precompute outputs for the curated events locally; the public app serves stored results; label it "replay of precomputed results". |
| C. Demo video | Q5 says no, or no host works | Local-only app plus a recorded video and screenshots; do not claim "deployed". |

**Prompt (docs part, all tracks):**

```text
TASK: Phase 10 README and claims audit.

1. README.md: what it is; screenshots from docs/screenshots (only those the owner approved); an architecture diagram (mermaid, accurate to the code); how to run with Docker and without; how to test (exact commands and the test counts from a run you perform today); a Limitations section: baseline model only, thesis U-Net+Transformer is not part of this repo, checkpoint 77000 served (not 89000), thesis numbers belong to 89000, over-prediction of heavy rain (cite the measured BIAS from docs/RESULTS.md, and the thesis BIAS 2.35 labelled as the thesis test set / checkpoint 89000); the baseline was trained and scored on a 512x512 archive pipeline that the thesis text does not describe (the thesis pipeline is 360x360 average-pooled with threshold 0.629), so its numbers are not like-for-like with the thesis proposed-model numbers; say so plainly, blurring at long leads (only if visible/measured), data permission status, what is replay vs live.
2. Create docs/CLAIMS.md: a table of every claim you make anywhere (README, CV bullets, LinkedIn text, interview notes): Claim | Evidence file or command | Verified date. Include candidate CV sentences as TBD until evidence exists. Rules: no deployment claim without a working URL tested today; "CI passing" only with a green run link; metrics only from docs/RESULTS.md.
3. Search the repo for numbers in README/docs that do not trace to RESULTS.md or a command, and list them. Do not fix them silently; report them.
```

**Prompt for track B only (replay mode, only if D7 allows derived data):**

```text
TASK: Phase 10B replay mode. Allowed only if docs/DECISIONS.md D7 says derived frames/metrics may be published for the listed events.

1. services/inference/scripts/export_replay.py: for each curated event call the app's prediction code locally and write a replay bundle (metrics JSON + the 18 PNG frames) to apps/web/replay/<slug>/ ; include modelVersion, threshold definition, generation date and a clear field "replay": true.
2. The web app shows replay results through the same UI; the POST route is disabled in replay deployments (env REPLAY_MODE=true) and the UI labels results "Precomputed replay, not a live run". The database history page is hidden or relabelled in replay mode.
3. Only events listed in D7 are exported; list them in your report. Tests for the REPLAY_MODE route behaviour and for the labelling helpers. Report bundle sizes measured on disk.
```

**Owner review**

- Read the README as a stranger: can they run it? Follow it on a fresh clone.
- Every number in README → open `docs/RESULTS.md` and find it.
- `docs/CLAIMS.md`: for each row, open the evidence yourself.
- Check the Limitations section says "checkpoint 77000", "baseline only", and does not borrow thesis numbers for this checkpoint.
- Track B: open the replay bundle, confirm only the permitted events are present, and the UI says it is a replay.
- Track A: open the public URL on your phone today; test an actual forecast.

**Exit gate:** README, CLAIMS and (if applicable) the live URL or video verified by you.

**If it fails:** if you cannot verify "deployed", write "local demo + video" instead.

---

### Phase 11 — Interview readiness (learning mode)

**Goal:** you can explain every part of the system and the honest story of how you got there.

**Entry gate:** Phase 10 merged.

**Branch:** `docs/interview`

**Prompt:**

```text
TASK: Phase 11 interview notes. Write docs/INTERVIEW.md (max 4 pages) from the actual code and docs/audits, in plain English that a graduate can say out loud. No new claims. Sections:
1. 60-second pitch and 3-minute walkthrough of the architecture (browser, Next.js, Prisma/PostgreSQL, FastAPI, ConvLSTM).
2. Model explained simply: why ConvLSTM, encoder-forecaster, 6 frames in/6 out, 10-minute steps, persistence baseline, CSI/POD/FAR/BIAS (formulas and what a low CSI with high BIAS means), why heavy rain >= 10 mm/h.
3. The honest engineering story: the initial model definition did not match the checkpoint (CSI 0), how it was found (cite docs/audits), how the golden check and the real evaluation fixed it. Use measured numbers from docs/RESULTS.md only.
4. 15 likely questions with short answers, each pointing to a file/line: e.g. why a separate inference service; why model is loaded once; how path traversal is prevented; why no frames are stored; how null metrics are handled; why the served baseline is 512x512 while the thesis dataset is 360x360 and what that means for comparing numbers; what you would do next.
5. Limitations and what is NOT claimed.
Then write 10 quiz questions about the codebase (answers hidden at the end) for the owner to self-test.
```

**Owner review**

- Read it aloud; mark every sentence you could not defend, and ask the agent to simplify it or explain it.
- Pick three questions from section 4 and answer without notes; open the code to check yourself.
- Verify section 3 matches `docs/audits/` and `docs/RESULTS.md` exactly.

**Exit gate:** you can answer the self-test without notes.

---

## 5. Quick reference

**Branch names:** `docs/baseline`, `fix/model-port`, `fix/preprocess-contract`, `feat/event-builder`, `feat/eval-real`, `fix/web-api-contract`, `chore/e2e-smoke`, `feat/ui-events`, `feat/ui-event-page`, `feat/ui-history`, `chore/docker-ci`, `docs/release`, `docs/interview`.

**Where numbers live:** measured scores only in `docs/RESULTS.md`; decisions only in `docs/DECISIONS.md`; evidence in `docs/audits/`; public claims in `docs/CLAIMS.md`.

**Never commit:** `.npz`, `.npy`, `.nc`, `.pth`, `.env`, secrets.

**When blocked:** save the agent report and `git diff --stat main...HEAD`, paste to your "brain" chat, and say which phase and which checklist item failed.