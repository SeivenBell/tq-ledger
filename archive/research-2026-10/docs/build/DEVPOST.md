# Devpost preparation — UNPUBLISHED DRAFT

Archived, unpublished copy for the unbuilt Ledger proposal. The [current decision memo](../decision/ranked-memo.md) supersedes that recommendation. This is not submission-ready text. Use it only if Ledger is explicitly selected; describe only functionality and results that were actually demonstrated.

## Proposed title

Q-Day Ledger: quantum code-breaking claims, with receipts

## Inspiration — source-grounded draft

Quantum cost numbers can describe a logical subroutine, a logical full attack or a physical architecture under hardware assumptions. Comparing their headline counts directly can mislead. The proposed tool makes the distinctions and supporting quotes visible, rather than estimating a new attack or predicting Q-Day.

HKMA's July 2026 survey says 73% of respondents ranked a lack of established models, tools or industry-standard frameworks for quantifying quantum-related risk among their top three concerns. This is a ranked concern, not objective proof that banks lack tools, and not evidence that they want this product. Intended early users are PQC analysts, resource-estimate reviewers and security writers; a possible buyer is their research/security team. **Demand and willingness to pay are unvalidated.**

The free [PostQuantumSecurity.org tracker](https://www.postquantumsecurity.org/trackers/qubit-estimates.html), launched October 21, already provides sourced RSA/ECC estimates, assumptions and a downloadable CSV. ECDSA.Fail, Jaques's Quantum Landscape and Ivezic's analysis cover adjacent jobs. Do not claim a first, unique or validated market. The hypothesis to test is whether quote-level evidence and a reasoned refusal save expert review work.

## Intended build — replace with actual shipped behavior

- Static source-linked cards and a deterministic comparison view. Recommend six human-reviewed operating-point cards: EF-893 logical point addition; GOOG-ZK-PA low-qubit and low-gate separately; LIT23 single-key and amortized k=11 separately; G25 physical full attack. Distinguish G25 Table 5 counts from layout qubits; never combine them as one operating point.
- Comparison outcomes: comparable, caveat, not comparable, or insufficient evidence. Unknown required evidence must not silently pass. Suppress ratios for incompatible scopes, resource layers or inclusions; show the reasons and sources.
- Source-grounded CLI extraction returns a **list of draft cards**, followed by strict span and unambiguous number checks, human categorical review and local review/export. Static draft/run evidence can be deployed; a live writable reviewer is not promised.
- A model proposes; code checks literal evidence; a human reviews semantics. A quote's existence does not prove the field's meaning, scientific validity or circuit correctness. Fuzzy matching cannot certify support.

Authentication, memory, headline parsing and sophisticated CI are optional, not submission claims. Describe the actual implementation and model only after inspecting the shipped artifacts; do not name a speculative model version or partner integration.

## Scientific copy constraints

- EF-893 is 893 **logical** qubits for one point addition with a classical addend; 111 failures in 360,960 wider tests are **submitter-reported**. Link the [submission record](https://api.ecdsa.fail/api/submissions/457ccb7a-4436-4e8c-8e8c-f7d22c3c81b5), not an arXiv paper for that number. Do not equate nonce-filtered tests with an independent correctness proof.
- [Litinski](https://arxiv.org/abs/2306.08585) gives (44 + 65/k) million Toffolis per key: 109M at k=1 and approximately 49.9M at k=11. The asymptote is 44M, not 50M. The title's 50M is amortized, not a single-key cost or a misleading claim by itself.
- The ECDSA.Fail authors' abstract states “more than 50% below” for its stated Q×T comparison. The approximately 34.5% figure is a limited, retry-adjusted Q×T calculation against Google's **low-gate upper bound**, not a headline result, physical-resource reduction or proof of like-for-like superiority. Interface/lookup inclusions and the paper's optimistic external-row success convention constrain interpretation; leave it out of the core pitch.
- If a pre-identified printed arithmetic slip is encoded as a recompute check, describe it as a check of a known example, not autonomous discovery. Do not imply an unaffected conclusion was invalidated.

## Evidence required before writing “how it works” or results

- [ ] Record actual implemented architecture, dependency/model versions, deployment URL, code revision and video URL. Confirm each claimed feature works; remove others.
- [ ] Review all six cards against pinned/versioned sources; record reviewer, date, source hashes, locations, licensing and unresolved fields. Do not label a draft human-reviewed.
- [ ] Save real CLI extraction inputs, list-of-drafts output, strict check outcomes, ambiguities, human corrections and review/export artifact. Attach raw run evidence, not a staged rejection or fabricated UI.
- [ ] Record three development comparison examples separately from three held-back pairs independently labelled by a human. Freeze held-back labels before scoring and exclude them from prompt/engine tuning. Report counts and disagreements, not a statistically strong benchmark or broad accuracy claim.
- [ ] If extraction is evaluated, state source/claim/field denominators, human gold procedure, false accepts and false rejects, and missing/extra drafts. “All published fields pass checks” is a publishing property, not independent accuracy evidence.
- [ ] If a funded key exists, run an LLM baseline on the same tasks with the same source access; preserve raw answers and grading rules. Otherwise say not run, without a baseline superiority claim.
- [ ] Include model cost/latency only if measured; give units, run boundary, date and n. No invented throughput, savings, customer quotes or success odds.
- [ ] Replace this checklist with evidence-backed prose; do not turn unfilled items into asserted placeholder results. If extraction was not run, say so explicitly.

## Security, licensing and independence — verify before publication

Use public published claims only: no new attack estimates, circuit construction or logical-to-physical conversion. Pin licensed sources; show licence and provenance. Do not redistribute full source texts or proprietary API records without permission. A source fetch or text hash does not verify scientific truth. Report inaccessible or unchecked evidence explicitly.

Keep any API key server-side/local and out of static exports. The core is read-only hosting with locally reviewed/versioned exports; Render filesystem writes are not durable approvals. Claim authentication, spend controls or ingestion restrictions only if implemented.

Build independently, with no employer data or code. No employer-specific restrictions, permission or endorsement are presumed. Before submission, describe actual authorship, dates, prior work and AI assistance from the repository history; do not assert that all work was written during Build Week without evidence. List only dependencies/platforms genuinely used and distinguish research assistance from human source review.

## Research depth

[practitioner-pain.md §7](../research/practitioner-pain.md#7-sources) distinguishes full/partial readings, secondary evidence and competition. [competitors-users.md](../research/build/competitors-users.md) and [market-story.md](../research/build/market-story.md) supply leads, not validated demand; use the corrected HKMA wording above over their older pitch copy. The [classic](../research/build/claims-classic.md) and [2026](../research/build/claims-2026.md) corpora supply draft evidence; [span-check-feasibility.md](../research/build/span-check-feasibility.md) explains why quotes must be re-anchored. None constitutes independent circuit reproduction.

Repository: https://github.com/SeivenBell/tq-ledger. No live/video link is asserted until an actual deployed build and recording exist. Outreach status must be taken from actual sent/reply records; drafts are not contact or adoption evidence.

Acceptance boundary: absent a funded key, extraction is `not_run` and the full AI-workflow acceptance criterion remains unmet. An honest static demo is not evidence that extraction worked. Core ratios require fully comparable, exact, unbounded values; caveats/bounds receive no ratio.
