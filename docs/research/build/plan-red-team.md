# Q-Day Ledger build plan: red-team report

## Summary

The core idea holds up. The plan around it does not fit the time. The two inputs everything waits on are Severyn's review time and a schema that is not finished, and three of the demo's key moments rest on numbers or rules that the tickets cannot produce as written.

- **Scope.** The Must set (T1–T8) is about 1.5–2× bigger than the "~12 hours" claim. T1, T2, T6 and T7 are each underestimated by about one size. Severyn's own planned hours already add up to about 13–14 h, and that is before any time to review and merge agent pull requests.
- **The schema can't express the 14 labelled pairs.** Cards have one card-level `layer`, but several cards contain both logical and physical numbers. Metrics have no "operating point" (one paper gives two or more alternative designs). Pair 10's headline "34.5 %" is not a Toffoli comparison, and pair 4's label goes against rule G9 as written.
- **Several "verifiable" claims are circular.** "0 unsupported numbers published" and "100 % pass" are true by construction. The engine is scored on the same pairs it was built against. The baseline asks a model with no documents about papers from Sept–Oct 2026, which mostly tests its knowledge cutoff. The gold labels come from the same model family as the extractor.
- **Most likely failure on Sunday night:** the extraction-and-eval chain finishes late. The video and Devpost page then go out with `[RESULT]` gaps, or get recorded late at night against a half-merged site.

**How I read things.**
- Read in full: BRIEFING, PRODUCT, ARCHITECTURE, PLAN, DEMO, DEVPOST, OUTREACH, CONTEXT, issues #15–#26 including comments, `claims-2026.md` and `span-check-feasibility.md`.
- Read in part (searched): `claims-classic.md`, `judge-panel.md`, `build-feasibility.md`.
- Primary sources: arXiv 2505.15917 HTML (§3.2, searched), 2609.09582v2 HTML (searched) and the 2306.08585 abstract.
- I couldn't run the `gh` command; I read the issues through the GitHub issue reader, which gives the same content.
- **No Python tool was available in this session.** I did all arithmetic by hand and checked each result with a second method. Re-run it in Python before anything goes on stage.

## Files

- `docs/build/PLAN.md:13-38` — Friday and Saturday schedule. F4 starts T1, T2 and T3 overnight, which conflicts with T3's approval step.
- `docs/build/PLAN.md:42-57` — ticket table and dependencies.
- `docs/build/PLAN.md:59-67` — cut order.
- `docs/build/ARCHITECTURE.md` §3 — data model: card-level `layer`, `metrics {name: Value}`, `asserted` filled by `headline.parse`.
- `docs/build/ARCHITECTURE.md` §4 — the checks.
- `docs/build/ARCHITECTURE.md` §5 — gates G1–G9 and "the page shows the ratio" only when comparable.
- `docs/build/ARCHITECTURE.md` §8 — eval: "Twelve labelled comparison questions", split, baseline.
- `docs/build/DEMO.md:9-16` — script. 0:25 depends on T9; 0:50 needs a ratio on a caveat verdict; 1:20 needs a web reviewer page.
- `docs/build/DEVPOST.md:11,31-35,41,67` — overclaims (details below).
- `CONTEXT.md` "Comparing claims" — out of date: 6 gates, and a verdict level called "comparable with a stated conversion".
- Issue #17 (T3) — pair table; pairs 4, 5, 7, 10, 12 and 14 are a problem.
- Issue #15 (T1) — 20 cards + 3 headlines, plus the requirement to re-anchor every quote.
- Issue #16 (T2) — number formats and recompute registry entries.
- Issues #20 and #21 (T6, T7) — extraction returns one `DraftCard`; the gold set is `G25-RSA2048, SCHR, GOOG-ZK-PA/FULL`.
- `docs/research/build/claims-2026.md:351,373` — 1.961 B and 34.5 %.
- `docs/research/build/claims-classic.md:473-474` — the G25 typo, plus a second unresolved inconsistency (1,399 vs 1,409 vs 1,537 logical qubits).
- `docs/research/build/span-check-feasibility.md` — only 58 % of quotes in the 2026 corpus match the source text.

## Architecture: what depends on what

```
T1 schema + 20 cards + canonical text (re-anchor every quote)
 ├─► Severyn card review (gold) ──► T3 pairs approval ─► T3 engine ─► T5 compare page ─┐
 ├─► T2 verifier ─► T6 extraction (dev) ─► prompt iteration ─► held-out run ─► T7 page ─┼─► video ─► Devpost
 └─► T4 skeleton ─► T8 deploy ──────────────────────────────────────────────────────────┘
```

**Real critical path:** T1 schema → T2 → T6 → prompt iteration → held-out run → T7 → video. Every step also needs Severyn as reviewer, merger and labeller.

---

## 1. Scope realism

| Ticket | Plan size | Realistic | Why |
|---|---|---|---|
| T1 | M | **L** | 20 cards + 3 headlines (BRIEFING says "17"; PRODUCT says "8 to 12"). The #15 addendum adds: fetch canonical text for 11 sources, re-anchor every quote, add table locators, list misses. The 2026 corpus matched only 58 %, so expect many manual fixes. It also has to settle the schema problems in §2 below. |
| T2 | M | **L** | Tiered exact/fuzzy span check, table locator against `pdftotext -layout`, flattened-exponent parser, a recompute registry, Clopper–Pearson. Each piece is small; together it's a full day for an agent plus review. |
| T3 | M | M | Fine once the schema is fixed. As written, several expected pairs can't pass (§2). |
| T4 | M | M | The Lighthouse ≥ 90 accessibility target is extra polish. |
| T5 | M | M | Doesn't include the draft or review page the demo needs. |
| T6 | M | **L** | Papers make several claims (GOOG-ZK has 2 cards and 4+ operating points; SCHR has 3). `extract()` returns a single `DraftCard`. The nested `{value, quote, location}` structured-output schema for every field is large. |
| T7 | M | **L** | Matching extracted claims to gold cards is unspecified. So are normalisation, scoring of extra fields, and how free-text baseline answers get graded. |
| T8 | S | S/M | uv build on Render. Live extraction would need `pdftotext`, which Render's native runtime probably lacks [INFERENCE]. |
| T9 / T10 / T11 | S / S / M | M / M / L | T10 also has to write approvals somewhere other than Render's disk, which is wiped on restart. T11 depends on a pre-release SDK. |

**Severyn's hours.**
- PLAN says 10–12 focused hours, but its own schedule adds up to 0.75 + (2+2+2+1–2) + (2+1+1.5+1) ≈ **13.25–14.25 h** (hand sum).
- Not budgeted at all: reviewing and merging about 8–10 agent pull requests (≈ 20 min each ≈ 3 h [INFERENCE]), merge conflicts on `pyproject.toml`/`uv.lock`, and debugging the deploy.
- Card review alone: about 20 cards × ~10 fields ≈ 200 field checks, scheduled for a "2 h" morning slot. That's ≈ 36 s per field, without opening the source [INFERENCE].
- The G25 1,399 / 1,409 / 1,537 inconsistency (`claims-classic.md:474`) needs real physics reading before anything can say "1,399".

**Proposed tighter must-have set** (keep the never-cut list from `PLAN.md`):

1. **T1a (Friday): schema only**, merged before any other ticket starts.
2. **T1b: about 12 cards the demo actually needs:** EF-893, EF-BENCH, EF-BENCH-COHERENT, GOOG-ZK-PA (low-qubit and low-gate), GOOG-ZK-FULL, LIT23 title and single-key, GE19, G25, GU-DIV, SCHR, plus headlines PLDD-25 and CD-50. Re-anchor quotes only for these. The rest ship as `machine_extracted` with a visible badge.
3. **T2** as specified.
4. **T3 with 10 development pairs, plus 4 held-back pairs** labelled by Severyn and kept away from the engine agent.
5. **T4 + T5 merged**, plus a read-only `/drafts/{id}` page.
6. **T8 moved to Saturday morning**, right after the skeleton ("deploy first").
7. **T6 + T7 as command-line tools**, with a static `/eval` page built from `results.json`.

Cut T9, T10, T11 and T12 by default. Bring T12 back only after the source-fetching fix in §3.

## 2. Contradictions and gaps between documents

| # | Where | Contradiction or gap |
|---|---|---|
| C1 | ARCH §3 (`layer` on the card) vs T3 pairs 5 and 7 | G25, GE19, GOOG-ZK-FULL and LIT23 hold both logical and physical numbers (`claims-classic.md:341,423,255`). If G25's layer is `physical_architecture` and GOOG-ZK-FULL's is `logical_algorithm`, pair 5 (logical vs logical) also fails G3. Pair 7 (physical vs physical) fails G3 too. T3 requires the failing-gate set to match exactly, so these tests fail. |
| C2 | ARCH §3 `metrics {name: Value}` vs the data | One card can hold several alternative designs: GOOG-ZK-PA (≤1,175 q / ≤2.7M T and ≤1,425 q / ≤2.1M T), SCHR (space- vs gate-optimised), WEB22 (1 h / 1 day / 10 min), EF-BENCH (cutoff / windowed / low-qubit), G25 (1,399 / 1,409 / 1,537). A pair reference like `GOOG-ZK-PA toffoli` is ambiguous. |
| C3 | T3 pair 10 (metric `toffoli`) vs BRIEFING:49, DEMO:12, ARCH:133 "34.5 %" | 34.5 % is the paper's **retry-adjusted Q×T/p̂ ≈ 1.961 B** (2609.09582v2 §5.1.1: "lowest tabulated Q×T/p̂, at approximately 1.961 B") compared with Google's **low-gate** Q×T bound, 2.9925 B. The paper scores external rows "optimistically with p̂=1". Hand check: 1,162 × 1,684,161 = 1,956,995,082; ÷ 0.99809 ≈ 1.9607 B; 1 − 1.9607/2.9925 = **34.5 %**. Raw Q×T gives 34.6 %. Toffolis alone give 19.8 % (vs 2.1M) or 37.6 % (vs 2.7M). Against the low-qubit bound it's 38.2 %. No card has a Q×T metric, so the engine as specified **can't print 34.5 %**. |
| C4 | ARCH §5 / T5 "ratio only when comparable" vs DEMO:12 | The demo shows "comparable with caveat: 34.5 % below", but the spec hides the ratio on caveat verdicts. |
| C5 | T3 pair 4 (GE19 vs G25 physical qubits = caveat) vs G9 | G9 says a different runtime target means **not comparable**. GE19 runs about 7.4 h; G25 about 5 days (`claims-classic.md:476`). The schema can't tell a runtime constraint (WEB22's deadline) from a runtime result (GE19, G25). |
| C6 | T3 pair 12 vs T1 card list | The pair needs a windowed SCHR (as ECDSA.Fail quotes it) and an unwindowed SCHR (as Gu quotes it). T1 creates one SCHR card, and a third-party quotation fits neither `ClaimCard` nor `Headline`. |
| C7 | T3 pair 14 and DEMO fallback vs ARCH §3 | Headlines are compared through `asserted`, which is "filled by headline.parse" (T9, a Should item and cut #3). Without T9, pair 14 and the demo's fallback (preset pair 14) have no input. |
| C8 | PLAN F4 (start T1, T2, T3 overnight) vs T3 step 1 and BRIEFING §6 | T3 needs Severyn's approval before writing the engine; BRIEFING schedules that approval for midday Saturday, PLAN for the morning. T2 and T3 depend on T1's schema but start in parallel with it. |
| C9 | DEMO 1:20–1:40 vs tickets | No Must ticket builds a web extraction route or a review page. T6 is a command-line script; `/review` exists only in T10 (Should, cut #2). T8 rate-limits an extraction endpoint nobody builds. |
| C10 | DEMO 0:25 vs PRODUCT Should #8 and cut #3 | The strongest 25 seconds of the video depend on a feature that is first in line to be cut. |
| C11 | T6 `extract() -> DraftCard` vs T7 gold `GOOG-ZK-PA/FULL` | Multi-claim papers have no rule for matching extracted claims to gold cards. |
| C12 | Pair count | ARCH §8 says "Twelve"; PRODUCT §7 and PLAN's definition of done say "≥ 12"; T3, DEMO and DEVPOST say 14. |
| C13 | ARCH §2 vs ARCH §8 / DEVPOST | §2 says Haiku for repeated eval runs; §8 and DEVPOST say the baseline uses "the same model". |
| C14 | ARCH §1 "cards live in git" vs T10 | An approval on Render writes to a disk that is wiped on restart (`build-feasibility.md:123`). No ticket gives the server a GitHub token. |
| C15 | T12 "fails if `checks` would change" vs licences | Texts under the default arXiv licence (RNSL17, HJNRS20, WEB22, LIT23, LUO) aren't committed. In CI their span checks come out `not_run`, but locally they pass, so CI goes red. Otherwise DEVPOST's "100 %… run in CI" is false. |
| C16 | CONTEXT vs ARCH | CONTEXT lists 6 gates and a "comparable with a stated conversion" level; ARCH has 9 gates and "caveat". "Reproduced" status is defined but no ticket ever sets it. "Machine-extracted = passed span check" is applied to seed cards before anyone has run a span check. |
| C17 | T2 number formats vs real quotes | GOOG-ZK: "fewer than **half a million** physical qubits". G25: "less than **a million** noisy qubits". Neither form is in the parser list, and both numbers appear in the demo (home-page strip, pair 7). |
| C18 | ARCH §4 example | It says "the single-key card must quote the (44 + 65/k)M formula", but a direct quote exists: "109 million Toffoli gates per key" (§2.1 p10, `claims-classic.md:268`). |
| C19 | DEMO 0:25 "click 893 → … arXiv link" | EF-893's source is an ECDSA.Fail API JSON record (`"qubits": 893`) under a proprietary ToS, not an arXiv paper. |
| C20 | BRIEFING "17 claim cards' worth of **verified** quotes" | The 2026 corpus, which holds the demo's main cards, matched 58 % (`span-check-feasibility.md`). |
| C21 | Pair 10 vs G2 (inclusions), needs Severyn's judgement | Google's point-addition count leaves the lookup out (billed separately as 3·2¹⁶ in Eq. 1). The coherent variant uses a lookup/use/unlookup pattern inside its count (+29.6 % T); [INFERENCE] the lookup cost is probably included. Under strict G2 the pair is not comparable, or at least needs a caveat about the direction of the bias. |

The G25 typo itself checks out against the primary source. arXiv 2505.15917 §3.2 reads "the expected number of shots is 9.2, giving an expected total time of 12.07⋅9.1/24=4.63 days". By hand, 12.07 × 9.1 / 24 = 4.5765 and 12.07 × 9.2 / 24 = 4.6268. That quote is **not** in the corpus with a location, though; only a `[CHECK]` note is (`claims-classic.md:473`). T1 has to anchor it. The arXiv HTML text also doubles MathML tokens ("9.29.2"), so the canonical-text step must strip annotations.

## 3. Verification weaknesses

1. **Tautological metrics.** "0 unsupported numbers reached a published card" and "100 % of published numbers pass" are guaranteed by the publishing gate. The informative measure is how often the verifier wrongly accepts or rejects a number compared with gold.
2. **The number check only tests presence.** Any number found in the quote passes. Swaps inside multi-number quotes pass undetected: Table 5's row "… 33 1280 1.25% 9.2 6.5e+09 1399", or Google's "either ≤1200 … or ≤1450 …". The categorical fields that **drive the gates** (layer, scope, statistic, addend, amortization) are not checked by code at all. "Code verifies every quote and number" is true; "nothing unverified is published" overclaims.
3. **The engine is graded on its own training pairs.** T3's tests are the 14 pairs, so "engine 14/14 vs chatbot X/14" compares a memorised set with a zero-shot one. Freezing the labels first doesn't change that.
4. **The baseline is a strawman.** A model with no documents is asked about EF-893 (2026-10-13), GU-DIV (2026-10-15) and similar. That mostly measures its training cutoff [INFERENCE]. Grading of free-text answers is unspecified. Pandya will notice.
5. **Gold-label circularity.** Claude research agents wrote the corpus, and a Claude model extracts. Agreement partly measures self-consistency. Gold for SCHR and GOOG-ZK was read only partially, so correct extractions outside gold have no scoring rule. Severyn's time-pressed review is the only independent check.
6. **Held-out leakage.**
   - The held-out papers are also published seed cards and pairs in the same repo the agents read.
   - The dev paper EF-BENCH tabulates Google and Schrottenloher rows and their conventions (Table 3).
   - The prompt's checklist comes from CONTEXT, which was written from the full corpus.
   - T11's "recall prior cards… for the same source family" would put gold straight into the prompt.
   - G25 (May 2025) is probably in the model's pretraining data [INFERENCE].
7. **Recompute "discovery" is hand-coded.** The G25 registry entry is keyed by card ID and was written after an agent found the typo. DEVPOST's "The verifier found a real inconsistency" is circular.
8. **Self-reported inputs.** 111/360,960 is the submitter's own test (`claims-2026.md` EF-893). The card must say "self-reported".
9. **Small n.** About 3 papers, 25–40 numeric fields and 14 pairs. Report n and a confidence interval (reuse `failure_stats`), not a bare percentage.
10. **Fuzzy tier vs "verbatim".** DEVPOST says quotes were "found verbatim", but the fuzzy tier allows 15 % character difference. Report the exact and fuzzy rates separately.

## 4. Presentation risks with this panel

- **"Gate" collides with quantum gates.** The narration "Three gates fail" comes in a video that is also counting Toffoli *gates*. Say "checks" or "comparison rules" in the UI, narration and Devpost; keep "gate" internal.
- **The opening list mixes kinds of numbers without saying so.** "one million, twenty-six thousand, eleven hundred, eight hundred ninety-three" (DEMO:9, DEVPOST:11) are physical RSA, physical P-256 atoms, logical point-addition and logical point-addition (`market-story.md:132-135`). Unlabelled, the product commits the error it exists to catch. The 0:00–0:15 segment is also 43 words in 15 s ≈ 170 wpm, which is too fast.
- **"Last week"** would be said on Oct 25 about an Oct 13 post. Precision is the brand; say "On October 13".
- **Second-hand hook.** The X post behind PLDD-25 was never read (`claims-2026.md` PLDD-25), so the 25 % line is Ivezic's report of it. Attribute it ("as reported by…"). Dallaire-Demers is also an outreach target.
- **The 50 % is the paper's own number.** "a headline said fifty percent" leaves out that the ECDSA.Fail abstract itself says "more than 50% below" and then builds the coherent variant. Credit the authors.
- **The Litinski framing reads as a gotcha.** PRODUCT calls 50M a limit "the paper never derives". But the abstract says the per-key reduction comes from "reusing the stored state for multiple keys and spreading the cost… over multiple parallel instances" (2306.08585 abstract).
- **"Who pays?" isn't in the 2:00 video.** BRIEFING:72 says a user → buyer card fixes it, but DEMO has no such segment. The video also shows no per-run cost or latency (`judge-panel.md:46`, Coupez).
- **DEVPOST overclaims:**
  - "verifier found";
  - the pre-written result "mostly by mixing logical and physical counts";
  - "Nothing unverified is published";
  - "Unrelated to the author's employment", which conflicts with the 1QBit/TopQAD overlap in PRODUCT §8;
  - "34.5 % below Google's upper bound" without saying it's the low-gate bound and retry-adjusted.
- **Non-deterministic live step.** "One field marked rejected" (DEMO 1:20) can't be guaranteed, and staging it would count as faking the demo.

## 5. Single most likely failure on Sunday night, and the mitigation

**Failure.** The eval chain finishes late: T1 schema churn → T2 → T6 multi-claim extraction → prompt iteration → held-out run → T7. Severyn is reviewing 200 fields and merging about 10 pull requests at the same time. The Saturday exit gate fails on "held-out eval numbers exist". Sunday turns into fixes, and the video is recorded at about 9–11 PM against a half-merged site, with `[RESULT]` placeholders or numbers from a hurried run. Smaller risk on top of that: the clone lives in `/tmp/tq-work`, which macOS clears on reboot (BRIEFING §9).

**Mitigation.**
1. Merge the schema on Friday, then start the other tickets.
2. Deploy the skeleton Saturday morning and redeploy on every merge.
3. Limit card review to the 12 demo cards.
4. **Run the held-out eval by Saturday 17:00, using whatever prompt exists by then**, as a command-line run that writes `results.json`. Build the eval page afterwards.
5. Fill in the Devpost numbers Saturday night.
6. Record the video Sunday by 13:00 and re-record only if something improves.
7. Push after every merge, or move the clone out of `/tmp`.

---

## Prioritized fix list

### P0 (before Friday kickoff or the Saturday start)

1. **`docs/build/PLAN.md` F4 row.** Change to: "Kick off T1 *schema PR only*; merge before anything else. Then T3 *step 1 only* (draft `pairs.json`, stop for approval). T2 and T4 start after the schema merges." In the Saturday table, move "T8 deploy" from Afternoon to Morning (after T4). Add a Severyn line: "PR review and merge, about 20 min per PR (about 3 h total)". Change "Time available… 10 to 12" to the honest figure, about 14 h.
2. **`ARCHITECTURE.md` §3 and issue #15.**
   - Move `layer` from `ClaimCard` onto `Value`, derived from `unit` (`physical_qubits`/`hours` with hardware assumptions → physical).
   - Replace `metrics {name: Value}` with `operating_points: {<op_id>: {<metric>: Value}}` (e.g. `low_qubit`, `low_gate`, `space_opt`, `1h`).
   - Add `runtime_role: "constraint" | "outcome"` to runtime values.
   - Add derived metrics `qt_score` (Q×T) and `qt_retry_adjusted` (Q×T/p̂, with p̂ = 1 when not measured, labelled as the paper's convention).
   - Add `quantity_source: "own" | "as_quoted_by:<source_id>"` so the SCHR variants in pair 12 can exist.
   - T1 must hand-write `asserted` for PLDD-25, CD-50 and IONQ-PR.
   - Change T1 acceptance from "≥ 19 cards" to "12 demo-critical cards reviewed; others `machine_extracted`".
3. **Issue #17 (T3) table.** Rewrite references as `ID:op:metric`.
   - Pair 10: `EF-BENCH-COHERENT:windowed:qt_retry_adjusted` vs `GOOG-ZK-PA:low_gate:qt_score`, expected verdict caveat (G5 one-sided). Add a G2 note for Severyn on whether the lookup is included (C21).
   - Pair 4: either relabel "not comparable (G9 runtime outcome differs: ≈7.4 h vs ≈5 days)", or change G9 in ARCH §5 so that runtime *outcomes* produce a caveat and only runtime *constraints* produce a fail. Pick one and edit both documents.
   - Pair 12: name the two derived SCHR variants explicitly.
   - Pairs 5 and 7: confirm failing gates under per-value layer.
   - Add "Step 1b: Severyn writes 4 held-back pairs *after* the engine merges; they are not in `tests/test_compare.py`."
4. **`ARCHITECTURE.md` §5 and issue #19.** Replace "ratio only when comparable" with "ratio when comparable; when the only caveat is G5 upper-bound, show 'at least X % below <named bound>'". Require the sentence to name the operating point ("Google's low-gate bound").
5. **`ARCHITECTURE.md` §8 and issue #21 (eval honesty).**
   - Metrics: replace "unsupported-number rate after the verifier must be 0" with "**verifier false-accept rate** (passed span and number checks but wrong against gold) and **false-reject rate**". Keep "0 published" as a design property.
   - Report n and a 95 % confidence interval for every rate. Report exact and fuzzy span tiers separately.
   - Baseline: add **Baseline B**, the same Sonnet model given both cards' quotes, answering in JSON `{verdict ∈ {comparable, caveat, not_comparable}, reasons ⊆ G1..G9}`, graded mechanically. Keep A (no documents) but label it "knowledge-only". Change "Twelve" to "Fourteen". Report engine accuracy on held-back pairs separately from the 10 development pairs.
   - Leakage: run log must assert `memory=off` and no held-out card ID in the prompt; freeze the prompt hash before the run; add a contamination note for G25.
   - Claim alignment: match draft claims to gold by `(target.problem, scope, op_id)`; list extra extracted claims separately.
6. **Issue #20 (T6).** Change `extract(...) -> list[DraftCard]` (several claims per source). Add `--no-memory` as the default for eval.
7. **`docs/build/DEMO.md` 1:20–1:40.** Replace the live web extraction with a read-only `/drafts/{id}` page on the live site. It renders the **actual held-out run** (per-field quote, check tier, verdict) and its run log (model, tokens, cost, latency, date). Narration: "This is the real run from Oct 24." Don't promise a rejection; if none happened, show a field that disagrees with gold. Add the `/drafts/{id}` page to issue #19.
8. **`DEMO.md` 0:25–0:50.** Make the compare-page preset pair 14 the primary path (T9 is optional). In 0:25, click a GOOG-ZK or G25 number (CC BY arXiv) instead of "893 → arXiv link", or say "links to the leaderboard record".
9. **BRIEFING §1 and §6 (first 45 minutes).** Add "Confirm a funded `ANTHROPIC_API_KEY` (extraction and eval need it whether or not the $100 credit arrives)" and "Move the clone out of `/tmp` or push after every merge."
10. **G25 1,399.** Severyn resolves `claims-classic.md:474` before 1,399 goes on the home strip, or the strip shows "1,399 (Table 5)" with the card's inconsistency flag.

### P1 (Saturday, before recording)

11. **`DEMO.md` 0:00–0:15.** Show the four numbers with on-screen labels ("1M physical · RSA", "26,000 atoms · P-256", "1,151 logical · one step", "893 logical · one step"). Cut narration to about 35 words. "Last week" → "On October 13". Add "as reported by Marin Ivezic" for the 25 % line.
12. **`DEMO.md`.** Add an 8-second user → buyer card (take the time from 1:05–1:20). Show the cost and latency of the run on the draft page.
13. **Terminology everywhere** (`DEMO.md`, `DEVPOST.md`, `PRODUCT.md`, UI copy in issue #19): user-facing "gate(s)" → "check(s)" or "comparison rules"; "nine comparability gates" → "nine comparison rules".
14. **`DEVPOST.md`:**
    - :41 "The verifier found a real inconsistency" → "Our recompute check flags a printed-arithmetic slip (formula encoded after reading the paper)…". Add "self-reported" to the 893-circuit failure data.
    - :35 delete "mostly by mixing logical and physical counts"; fill it from data.
    - :20 "Nothing unverified is published" → "No number is published unless its quote is found in the source and a person approves it; categorical labels are human-reviewed."
    - :32 "found verbatim" → "[exact]% exact, [fuzzy]% near-exact".
    - :11 label the four numbers.
    - :67 "Unrelated to the author's employment" → "Built independently of the author's employer; no employer code, data, or methods; logical-layer claims only."
    - Add the 34.5 % qualifier: "retry-adjusted, against Google's low-gate bound, using the paper's own convention".
    - Credit the ECDSA.Fail authors for both the 50 % and the coherent variant.
15. **`CONTEXT.md`.** Verdict levels → comparable / comparable with caveat / not comparable. List all nine gates. Define seed-card status honestly ("drafted from the research corpus"). Remove "Reproduced" or name what earns it.
16. **Issue #16 (T2).**
    - Add parser cases "half a million", "a million", "less than a million", "fewer than half a million".
    - The number check must record the matched token's offset. When a quote holds several candidates of the same unit or magnitude, require a `token_index` or table column, or mark the field `ambiguous`.
    - Add the G25 sentence as a located quote (§3.2) and strip MathML duplicates from canonical text.
17. **Issue #26 (T12) and #16.** Add `make fetch-sources`: download by arXiv ID and version, check `text_sha256`, cache in CI. Sources that aren't on arXiv (Eigen API, X, CoinDesk, Ivezic) record `not_run: not redistributable`, and DEVPOST says so.
18. **`PRODUCT.md` §1.**
    - Litinski bullet → "the title's 50 million is a per-key figure when many keys are computed, as the abstract says; one key needs 109 million". Drop "promises" and "never derives".
    - WEB22 bullet: mark the "NIST curve, not secp256k1" point as the corpus's inference about a small constant-cost difference, not an error.

### P2 (if time allows)

19. **`ARCHITECTURE.md` §5 G7.** Define "exact" and say whether an observed rate is compared with a budget or a budget with a budget.
20. **Issue #24 (T10).** State that approvals on Render produce a downloadable or committed JSON through a pull request, not a write to Render's disk.
21. **Licences.** On EF-893, EF-874 and EF-LEAD, quote only the needed fields and link the record; don't commit the API JSON (Eigen ToS §5). Note the GU-DIV CC BY-NC-SA licence on its card.
22. **Issue #18 (T4).** Drop the Lighthouse ≥ 90 target from acceptance and keep basic accessibility.
23. **EF-LEAD.** Show the baseline mismatch (API 3,962,753 vs paper 3,960,753) as an unexplained difference, not as a fact.

**Checks for the main agent to run:** none were run here; this was read-only. Before stage use, recompute in Python:
- 1,162 × 1,684,161 / 0.99809 / 2.9925e9;
- 1,684,161 / 2.1e6 and 1,684,161 / 2.7e6;
- 12.07 × 9.1 / 24 and 12.07 × 9.2 / 24;
- 1.96074 / 3.1725.