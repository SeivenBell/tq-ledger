# Q-Day Ledger: product spec

Status: build-ready draft, 2026-10-23. Owner: Severyn Balaniuk. Pick recommended by `docs/decision/ranked-memo.md`; final choice is Severyn's ([Choose the project to build](https://github.com/SeivenBell/tq-ledger/issues/14)).

Working name **Q-Day Ledger**. Tagline: *Quantum code-breaking claims, with receipts.*

## 1. The problem, in plain English

Every few weeks a new paper, leaderboard record, or headline says that breaking RSA or Bitcoin's cryptography takes fewer qubits than we thought. The numbers in circulation contradict each other:

- Public trackers say RSA-2048 needs **1,399**, **~2,314**, or **~4,000** logical qubits, and give today's best machines **8**, **48**, **~96**, or **~100** logical qubits (`docs/research/build/competitors-users.md`, table "Evidence that numbers in circulation are incomparable or wrong").
- A co-author announced that a new elliptic-curve circuit "cuts … physical qubits … by 25%". The paper never measured hardware; the field's most careful analyst re-derived "16% at most" for one architecture and "about 28% fewer ions but run longer" for another (Ivezic, postquantum.com, 2026-10-14).
- Litinski's title promises "only 50 million Toffoli gates"; the paper's single-key figure is **109 million**. The 50 million is a many-keys limit the paper never derives (`docs/research/build/claims-classic.md`, card LIT23).
- A widely cited "Bitcoin in one hour needs 317M physical qubits" result is built on a circuit for a NIST curve, not Bitcoin's secp256k1 (card WEB22).

**Why this happens.** Claims count different things: logical vs physical qubits, one subroutine vs a full attack, average vs worst-case gate counts, classical vs coherent inputs, Toffoli vs T vs "Toffoli + T/2", different failure rates, one key vs many keys. Titles and posts round and relabel. Nobody makes the conventions explicit side by side.

**Who pays the cost.**

| Person | What they must decide | What they do today |
|---|---|---|
| PQC risk analyst or advisor (e.g. Marin Ivezic, Applied Quantum; evolutionQ) | Does this new claim change the threat timeline I give clients? | Reads a 30 to 60 page paper and writes a prose comparison by hand. Applied Quantum sells due diligence because "timelines and claims are hard to compare". |
| CISO, crypto custodian, bank risk team | When to migrate, what to disclose to a board or regulator | Relies on trackers and headlines that disagree |
| Standards and policy groups (Quantum Alliance, NIST/CCCS-facing teams) | What evidence a "quantum-safe" or "quantum-threat" claim needs | No shared claim format |
| Journalists and tracker sites | What number to print | Copy headline figures; errors propagate |

Deadlines make this concrete: NSA CNSA 2.0 applies to new National Security System purchases from 2027-01-01; NIST IR 8547 deprecates RSA/ECC by 2030 and disallows them by 2035; Canada's federal roadmap requires high-priority systems migrated by end of 2031 (`docs/research/pqc-migration.md`).

## 2. What the product does

A public ledger of **claim cards**: one card per published claim, every number tied to the exact sentence it came from. On top of the cards:

1. **Compare**: pick two claims; the ledger runs **comparability gates** (same problem, scope, layer, cost statistic, addend interface, failure budget, gate unit, amortization) and either compares them or **refuses**, naming the gate that fails.
2. **Check a headline**: paste a sentence ("New circuit cuts Bitcoin-breaking hardware by 25%"); the ledger maps it to the underlying cards and says what the sources actually support.
3. **Add a claim**: give an arXiv ID; a model drafts a card where every field carries a verbatim quote; code verifies each quote and number; a signed-in reviewer approves field by field.
4. **Recompute**: the ledger re-derives what can be derived from quoted inputs (products, run-time arithmetic, failure-rate intervals) and flags inconsistencies inside a source.

The product's core promise: **an LLM proposes, code verifies, a human approves, and nothing unverified is published.**

### What it deliberately does not do

- No new attack circuits, no new resource estimates.
- No conversion from logical to physical resources. Physical numbers appear only as quoted from their source, with their hardware assumptions.
- No grading of companies or hardware vendors.
- No live monitoring claims; the demo dataset is frozen and dated.
- No redistribution of full paper text unless the paper's licence allows it (CC BY); otherwise short attributed quotes and character offsets only.

## 3. Users, jobs, and stories

Primary user: **the PQC risk analyst** (writes threat assessments for clients or an employer). Buyer path: analyst firms and in-house risk teams first, then CISOs needing evidence for migration timelines.

| # | Story | Acceptance |
|---|---|---|
| U1 | As an analyst, I see every published ECC-256 and RSA-2048 estimate, grouped so only like-for-like numbers sit together. | Ledger table with filters (problem, scope, layer); each row links to its card. |
| U2 | As an analyst, I click any number and see the exact sentence, its location, and the source link. | Every numeric field opens its quote, location, source version, licence. |
| U3 | As an analyst, I compare two claims and get a verdict with the reason. | Compare page shows a gate table and one of: comparable, comparable with a stated caveat, not comparable. |
| U4 | As a CISO, I paste a headline and learn whether its sources support it. | Headline page returns matched cards and a verdict with quotes. |
| U5 | As a reviewer, I add a new paper and approve or reject each extracted field. | Draft card shows per-field check status; approval records reviewer identity and time. |
| U6 | As a sceptic, I can reproduce every check. | `make verify` re-runs span, number, recompute, gate, and eval checks; results match the site. |

## 4. Why it is useful (value case)

| Value | Evidence | Strength |
|---|---|---|
| Prevents repeating wrong or incomparable numbers | Conflicting tracker figures; the 25% physical-qubit claim; Litinski title vs body; Webber curve label; a GRI survey misquote on a tracker (`competitors-users.md`) | Strong, documented |
| Saves analyst time per new claim | Ivezic's 2026-10-14 article is exactly this job done by hand. Time per comparison is not published. [INFERENCE] a few hours manually vs minutes plus a review with the ledger | Plausible, unmeasured; do not quote a number |
| Gives decision-makers a citation trail | Deadlines (CNSA 2.0, NIST IR 8547, Canada 2031) force migration decisions that boards and regulators review | Strong need; buyer not yet confirmed |
| Catches inconsistencies inside sources | Gidney 2025 prints "12.07 · 9.1/24 = 4.63 days"; the product is 4.58 (the 4.63 matches Table 5's 9.2 runs, so likely a typo with no effect on the conclusion) (`claims-classic.md`) | Strong demo; frame respectfully |
| Fits a funded direction | DARPA QBI IV&V topic open to 2026-12-30; DOE $45M V&V testbed (LAB 26-3603) includes resource estimation (`quantum-demand-map.md`) | Context for the path to production, not a hackathon user |

Honest weaknesses: no user has committed yet; the paying market is small today; Eigen Labs (Yukon) could add a claims lane. Mitigations are in section 8.

## 5. How usable it is (design principles)

- **Zero friction to read.** No login for the ledger, cards, compare, and headline check. Every card has a permalink.
- **Receipts on click.** Numbers are links. The quote panel highlights the cited sentence and shows section/page, arXiv version, and licence.
- **Plain-English verdicts.** "Not comparable: one counts logical qubits for a single point addition; the other counts physical qubits for a full key recovery."
- **Jargon behind tooltips.** Logical vs physical, Toffoli, addend interface, average vs worst case, each with a one-line explanation.
- **Visible trust status.** Badges: machine-extracted, human-reviewed, reproduced; observed vs derived values in different colours; "not independently verified" where true.
- **Exportable.** JSON per card, CSV for the table, a read-only JSON API.
- **Corrections welcome.** Each card links to a prefilled GitHub issue.

## 6. Scope

**Must (the demo depends on it)**
1. Card schema and 8 to 12 human-reviewed seed cards (ECC and RSA, 2017 to 2026).
2. Verifier: span check, number check, recompute checks, failure-rate statistics.
3. Comparability engine with named gates and labelled test pairs.
4. Web app: ledger table, card page with quote panel, compare page, method page with "what we do not do".
5. Extraction pipeline: arXiv text to a draft card with per-field quotes, verified by code.
6. Evaluation: held-out extraction accuracy and a plain-LLM baseline on labelled comparison questions; results page.
7. Deployed on Render (always-on instance), public repo, README, Devpost page, video of 2 minutes or less.

**Should (add in this order if time allows)**
8. Headline check.
9. Clerk sign-in for reviewers; approvals record the Clerk user ID.
10. SurrealDB Agent Memory: provenance graph (source, claim, assumption), "current best estimate" per comparable class via supersession, recall of prior cards and counting conventions before each extraction.

**Won't (this week)**
Physical estimation or logical-to-physical conversion; new circuits; live feeds; company grading; Eon Era and Expo integrations (no honest fit, see `docs/research/build/build-feasibility.md` §5).

## 7. Success metrics

**By submission (Oct 25, 11:59 PM ET)**

| Metric | Target | How measured |
|---|---|---|
| Live URL works logged-out on a cold browser | Yes, page under 2 s | Manual check from another network on Oct 25 and Oct 26 |
| Human-reviewed cards | ≥ 8, spanning ≥ 6 sources | `data/cards/*.json` with `review.status = human-reviewed` |
| Published numeric fields that pass span and number checks | 100 % | `make verify` |
| Labelled comparison pairs where the engine's verdict matches the label | 100 % on ≥ 12 pairs, labels frozen before coding | `tests/test_compare.py` |
| Held-out extraction accuracy (numeric fields, after normalisation) | Report the true figure; target ≥ 80 %; zero unsupported numbers reach a published card | `scripts/run_eval.py` → `data/eval/results.json` |
| Plain-LLM baseline on the same comparison questions | Report how many it gets wrong | Same harness, model without the ledger |
| External reply from a target user | ≥ 1 (stretch) | Outreach log |

**30 days after**: 25+ cards; 3 external corrections or pull requests; one analyst using it weekly; a conversation with Eigen Labs about linking or hosting.

## 8. Risks and mitigations

| Risk | Mitigation |
|---|---|
| A wrong physics statement on a card destroys credibility | Every published card human-reviewed by Severyn; derived values labelled; correction link; neutral wording |
| "Niche, who pays?" | Show user → buyer path: analyst firms (already sell this as manual due diligence) → CISOs and custodians needing evidence packs → API for trackers and standards groups |
| Eigen Labs (Yukon) adds a claims lane | Position as complementary: Yukon verifies submitted circuits; the ledger reads published papers and posts. Offer cards in Yukon's claim-sheet format |
| Build overruns | Deterministic core first; cut order in `docs/build/PLAN.md` |
| Demo fails during online judging (Oct 26) | Paid always-on Render instance, frozen data, smoke test, video recorded against the live URL |
| Licensing of paper text | CC BY papers for full-text demos; short attributed quotes and offsets for others; licence shown on every card |
| Read as an attack tool or as fear-mongering | Only public claims, no circuits, defensive framing (migration planning), "what we do not do" box |
| Overlap with Severyn's employer (1QBit, TopQAD) | Logical-layer only; no physical resource estimation, magic-state factories, or compilation. This is also the product's thesis (refuse logical-to-physical conversion) |

## 9. Positioning against what exists

| Alternative | What it lacks |
|---|---|
| Ivezic's analyses (postquantum.com) | Prose; not reusable; one claim at a time |
| Tracker sites (qdayiscoming, Quantum Doom Clock, BlueQubit, Qoronex) | Headline numbers without conventions; documented inconsistencies |
| Eigen Labs ECDSA.Fail and Yukon | Verify circuits submitted to their own checker; no cards for published papers; no logical-vs-physical gate |
| Asking a chatbot | No per-number receipts; conflates layers (measured by the baseline eval) |
