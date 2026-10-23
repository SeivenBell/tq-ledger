# Devpost page draft

Fill `[RESULT]`, `[URL]`, and `[VIDEO]` after the build. Keep every claim true on submission day; anything not built gets deleted, not softened.

---

## Q-Day Ledger: quantum code-breaking claims, with receipts

### Inspiration

Every few weeks a new paper, leaderboard record, or headline says that breaking RSA or Bitcoin's cryptography takes fewer qubits: one million, 26,000, 1,151, 893. Banks are told to "monitor these breakthroughs and adjust their timelines" (HKMA, July 2026), and 73 % of surveyed Hong Kong banks say they lack the tools to quantify this risk. But the numbers count different things: logical vs physical qubits, one step vs the whole attack, average vs worst-case gate counts, one key vs many. Even careful readers get caught: a co-author announced that a new circuit "cuts the physical qubits by 25 %", from a paper that never measured hardware. Analysts sort this out by hand, one article at a time.

### What it does

Q-Day Ledger turns each public claim into a **claim card** where every number links to the exact sentence it came from.

- **Compare** two claims: the ledger checks nine comparability gates (problem, scope, layer, gate unit, statistic, input type, failure budget, amortization, hardware assumptions). It compares them, or **refuses and names the gate**.
- **Check a headline**: paste a sentence; see what the sources actually support.
- **Recompute**: failure-rate intervals, totals, and arithmetic re-derived from quoted inputs; inconsistencies inside sources are flagged.
- **Add a paper**: a model drafts the card; code verifies every quote and number; a reviewer approves field by field. Nothing unverified is published.

### How we built it

FastAPI + Jinja + HTMX on Render; cards as versioned JSON in Git; Claude Sonnet 5.5 with structured outputs for extraction and headline parsing; a deterministic verifier (span check, number parser, recompute registry, Clopper–Pearson intervals with SciPy); a deterministic comparability engine. [If built: Clerk for reviewer sign-in and audit trail; SurrealDB Agent Memory for the source → claim → assumption provenance graph and for recalling counting conventions before each extraction.]

**Trust boundary**: the model proposes, code verifies, a human approves.

### How we know it works

- [RESULT] human-reviewed cards from [RESULT] sources (2017 to 2026); 100 % of published numbers pass the span and number checks (`make verify`, run in CI).
- 14 labelled comparison pairs, labels frozen before the engine was written: the engine matches [RESULT] / 14.
- Extraction on 3 papers held out from development: [RESULT] of numeric fields correct; [RESULT] of quotes found verbatim; 0 unsupported numbers reached a published card. Every disagreement is listed on the eval page.
- Baseline: the same model without the ledger answered the 14 comparison questions; it got [RESULT] wrong, mostly by mixing logical and physical counts.

### Challenges

Counting conventions are buried in prose and footnotes; the same paper can state three different qubit counts; titles round (a "50 million" in one title is a many-keys limit; the single-key figure is 109 million). Citations and structured outputs can't be combined in one API call, so we verify quotes in our own code, which turned out to be the product's core.

### Accomplishments

The verifier found a real inconsistency in a well-known paper (a printed 12.07 · 9.1 / 24 = 4.63; the product is 4.58, and 4.63 corresponds to the 9.2 runs stated in the same sentence) and showed that a much-shared 893-qubit circuit's failure rate sits above another benchmark's budget.

### What's next (path to production)

1. More sources, including hardware claims (logical-qubit records), with change alerts when a new paper supersedes a card in the same comparable class.
2. Evidence packs for CISOs, custodians, and insurers who must justify migration timelines to boards and regulators.
3. A read-only API and claim-sheet export for trackers, standards groups, and benchmark operators.

Target users we contacted: [list replies honestly, or "outreach sent; no reply yet"].

### Security and ethics

- Public, published claims only. No circuits, no new attack estimates, no logical-to-physical conversion.
- Every card shows its review status; nothing is labelled independently verified unless it is.
- API keys server-side; extraction requires sign-in and has a daily spend cap; ingestion only from an allowlist.
- Short attributed quotes; full text stored only for CC BY papers; the licence is shown on every card.
- Aimed at defenders planning post-quantum migration.

### Partner platforms

[Only list what is genuinely used. Clerk: reviewer sign-in; every approval records the reviewer. SurrealDB Agent Memory: provenance graph and recall of counting conventions before extraction. Render: hosting.]

### Prior work and AI tools (disclosure)

All code was written during Build Week (Oct 16 to 25, 2026). Research notes in `docs/research/` were produced with AI research agents and reviewed by Severyn. Code was written with Claude Code. Open-source dependencies: FastAPI (MIT), SciPy (BSD-3), Jinja2 (BSD-3), HTMX (BSD-2), Anthropic SDK (MIT) [update to the final list]. Quoted sources are credited on each card. Not affiliated with any company whose claims appear in the ledger. Unrelated to the author's employment.

### Built with

python, fastapi, htmx, claude, anthropic, scipy, render [, clerk, surrealdb]

### Links

Live: [URL] · Code: https://github.com/SeivenBell/tq-ledger · Video: [VIDEO]
