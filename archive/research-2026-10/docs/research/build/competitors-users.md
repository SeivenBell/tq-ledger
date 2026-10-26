# Who already compares quantum-cryptanalysis resource claims, and who would use the Claim Ledger (research as of 2026-10-23)

## Summary

- **The niche is open, but narrow.** I found no product or site that turns public ECC/RSA cost claims into cited cards with per-field quotes and gates that block unlike comparisons. Three things come close:
  - **Marin Ivezic** does this work by hand, in prose, and sells the expertise.
  - **qdayiscoming.com** publishes sourced, headline-level tables.
  - **Eigen Labs' Yukon** already runs machine-readable claim sheets with "AI review" and per-target comparability labels, but for hash and classical-ECDLP attacks, not for claims in quantum papers.
- **Eigen/Yukon is the likeliest competitor.** It is also the likeliest partner. It already has the method and the community; the only thing missing is this domain.
- **Practitioners do mix up incomparable numbers, and publicly.** Five public trackers I read give different "logical qubits needed" figures (RSA-2048: 1,399 / ~4,000 / 2,314; ECC: <1,200 / 1,673). They also disagree on today's logical-qubit record (8 / 48 / ~96 / ~100). One tracker misquotes the GRI survey. Ivezic contradicts himself on Chevignard (~1,100 vs ~1,193) and publicly corrected a co-author's "25% fewer physical qubits" claim.
- **Disconfirming evidence:**
  - Most public argument is about *timelines* (the 2028 Doom Clock, Vitalik vs Hoskinson), not about *which resource estimate is right*.
  - Ivezic wrote in May that ECC estimates have "converged".
  - Content sites (qLABS, qdayiscoming) already explain logical vs physical well. That shrinks the beginner-education use case.
- **BIP-360 cites no qubit count.** It has one unsourced footnote: "10^8 operations". The ethereum.org roadmap cites only Google's "roughly 1,200 logical qubits". Neither shows a dispute about which estimate is right.

---

## Main table

Overlap: 0 = none, 5 = already builds the Claim Ledger. Read depth and dates are in the per-item notes below.

| # | Entity | What it does (2026) | Overlap (0–5) | Role for the Ledger | Contact surface |
|---|---|---|---|---|---|
| 1 | **ECDSA.Fail** (Eigen Labs) | Public leaderboard for verified secp256k1 point-addition circuits. Score is Q × average executed Toffolis; there is a Pareto chart. | 2 | **Data source** (the circuits are the subjects of the cards) and **distribution channel** (its Telegram, GitHub PRs and roughly 147 accounts). Competitor only if it adds cross-paper cards. | Gautham Anant: X `@bbuddha_xyz`, LinkedIn `/in/gautham-anant` (search snippets). Jieyi Long: X `@jieyilong`. Org: X `@eigenlabs` |
| 2 | **Yukon** (Eigen's platform: HashSmash, CurveSmash and others) | Hosts open "autoresearch" challenges. HashSmash and CurveSmash take claim sheets and publish "Accepted by AI review" versus "Accepted by human review". | 3 on method, 1 on domain | **Most likely competitor or absorber**, and a possible host or partner | Same as above; "Create a challenge" at yukon.org/create |
| 3 | **HashSmash design doc** | Machine-readable YAML claim sheet, an LLM triage and review harness, and a rule to compare only within the same target profile and attack class | 3 on method | Proof the method is already being designed elsewhere. Same team as #1–2. | Oversight board listed as "Zooko (Shielded Labs), JP, Sreeram (Eigen), Justin (Ethereum Foundation)" |
| 4 | **Marin Ivezic**: postquantum.com, Applied Quantum, Quantum Academy | Q-Day Estimator (demand-side presets picked from papers), CRQC Scorecard, capability framework, and frequent hand-written comparisons of new claims | Tools: 2. Hand-written analysis: 4 | **Strongest potential user** and a **distribution channel**. Also a competitor in effect, because manual analysis is what he sells (consulting and training). | X `@infosec`; LinkedIn `linkedin.com/in/marinivezic`; email `marin@ivezic.com` (byline in a search snippet; obfuscated on the page); Telegram `t.me/infosec` |
| 5 | **Project Eleven** | Bitcoin Risq List (BTC exposure, last updated 10/12/2026), the 1 BTC Q-Day Prize (awarded 2026-04-24), a 110-page 2026 report with a Q-Day model, yellowpages (a PQ proof-of-ownership registry), Strongpoint custody | 1 | **Data source** (report, Risq List). Possible **user**, since their report synthesizes estimates. Its Q-Day model mixes RSA demand with ECC risk, which makes it a card candidate. | Alex Pruden X `@apruden08`, LinkedIn `/in/alex-pruden`; Conor Deegan X `@conordeegan`, LinkedIn `/in/conor-deegan-587513189`; X `@projecteleven` |
| 6 | **GRI / evolutionQ Quantum Threat Timeline 2025** (published 2026-03-09) | Annual opinion survey of 26 experts; evolutionQ also runs Quantum Briefings and paid risk-assessment services | 1 | **Data source** (forecast cards) and a **local potential user** (Waterloo) | evolutionQ: X `@evolutionQinc`, LinkedIn company/evolutionq, contact form. Personal handles for Mosca and Piani: not found. |
| 7 | **Pauli Group** (Calgary; Dallaire-Demers) | "We publish resource estimates, track hardware roadmaps…". Also Brace for Impact (arXiv 2508.14011), the Proof of Quantum challenge, Anchor Wallet. | 2 | **Potential user** and **subject**: Dallaire-Demers' 25% claim is the demo case. He co-authored the ECDSA.Fail paper. | `contact@pauli.group`; X `@pauli_group`; Dallaire-Demers X `@dallairedemers` |
| 8 | **Quantum Doom Clock** (Postquant Labs; Quantum Alliance contributors) | Exponential regression on physical-qubit counts, giving Q-Day = 08 Mar 2028 | 1 | **A claim to card** (its 1,673 logical qubits for crypto conflicts with Google's <1,200) | Richard Carback LinkedIn `/in/richard-carback`, carback.us; postquant.xyz |
| 9 | **Quantum Alliance** (launched 2026-10-16) | Open standards body that will "set the criteria for judging quantum-resistance claims" (about *readiness* claims, not attack-cost claims) | 1 | **Distribution channel** (it wants open test criteria) | Media: `wahid@input.global` |
| 10 | **qdayiscoming.com** (owner unknown) | Sourced explainer tables of estimates vs hardware: "Every number sourced"; leaves out unverified vendor claims | 3 (closest editorial analog) | Competitor on content; **potential user** | Not found |
| 11 | **qdaycountdown.com** (Secria) | Q-Day clock set to 2035-01-01, plus trackers: predictions, deadlines, qubits-to-break-RSA | 2 | Potential user or channel | Not found (site credits "Secria") |
| 12 | **BlueQubit "Road to Q-Day"** | Timeline plus a "Qubits: Have vs Need" chart | 2 | Potential user; **contains a misquote** (see evidence) | Not found |
| 13 | **Qoronex "Q-Day Intelligence"** | Countdown, milestones scored 1–10 "after human review", paid API | 2 | Competitor in paid data; **contains contestable figures** | Not found |
| 14 | **The Quantum Insider** (Toronto) | News plus paid market intelligence ("analyst-verified" means provenance, per `competitors-intelplatforms.md`) | 1 | **Distribution channel** (Canadian, local) | `hello@thequantuminsider.com`; X `@QuantumDaily` |
| 15 | **Quantum Computing Report / GQI** | News plus paid analysis | 1 | Channel | Not checked |
| 16 | **qLABS** | Explainers ("How many qubits to break Bitcoin?") and an L1 vulnerability index | 1 | Potential user; quoted as evidence of confusion | Site contact form |
| 17 | **Quantum Horizon** (arXiv 2606.14484, 2026-06-12) | Monte-Carlo CRQC forecast; "Reproducible models accompany every quantitative claim" | 2 | Data source and card subject (wide 1,200–2,330 logical range) | Gershteyn and Alber (no handles checked) |
| 18 | **BIP-360 (P2MR)** and **ethereum.org PQ roadmap** | Protocol proposals and roadmap | 0 | Neither a user nor a source of disputes; each cites one number | — |

---

## Per-item evidence

### 1–3. Eigen Labs: ECDSA.Fail, Yukon, HashSmash, CurveSmash

**ECDSA.Fail story blog** (2026-09-10; read in full), by Jieyi Long:
> "Because the interfaces and accounting conventions differ, this is a numerical comparison rather than a claim of formal dominance."

The same post describes the coherent-addend variant: "1,162 qubits, just 11 more than the original, and about 30% more Toffoli gates." It adds that "A complete Shor implementation, which chains 28 calls to this kernel, remains future work."

**Yukon launch post** (2026-08-12; full):
> "The score itself is calculated by the Yukon evaluation harness, never by the solver. A candidate is promoted only after it clears a defined improvement threshold."

**yukon.org** (read 2026-10-23; full, JS-rendered):
- 11 challenges, among them HashSmash, CurveSmash and sig.golf.
- Project Eleven, the Ethereum Foundation and zkSecurity are listed as collaborators.
- "ECDSA.fail's record is 69.4% below Google Quantum AI's bound."

**HashSmash design doc** (undated; read in full, 743 lines). Overlapping passages, verbatim:
- "LLM-assisted validation of the method, cost estimates, implementation, etc. With multiple LLMs cross-checking their observations. **Exact harness TBD**."
- "Submissions are compared only within the same target profile and attack class."
- "Claim sheet, machine-readable", followed by a YAML manifest with `time_log2`, `memory_log2_bytes`, `success_probability`, `restrictions` and `baseline_improved`.
- "Models should use a structured output format, cite exact pages, equations, code locations, or manifest fields."
- Prompt 5: "Do not compare attacks with different collision notions, message restrictions, preprocessing models, or success probabilities without displaying those differences."
- Principles: "**Every number needs a model.** A complexity exponent without a unit, memory model, success probability, and preprocessing convention is decorative mathematics."

**HashSmash live page** (read 2026-10-23; partial, first 229 of 304 lines). Results are labelled "Accepted by AI review." or "Accepted by human review." with a frontier column. [INFERENCE] Some form of the "TBD" harness is now in production.

**CurveSmash live page** (read 2026-10-23; full). It covers *classical* ECDLP and pairing-inversion bounds, not quantum:
- "Full-production targets. Scores use each target's own reference operation and are not directly comparable."
- "Acceptance after exploratory AI review is not mathematical proof."
- "Acceptance means plausible, not refuted; it is not a proof or practical break."
- Record: 127.08 log₂(T), Oct 23 2026, 13 results from 8 solvers. Judges include Antonio Sanso (EF) and Youssef El Housni (Consensys).

**What exactly overlaps.** The method is the same: a machine-readable claim sheet, LLM review that cites locations, comparison only within the same profile, and explicit "not directly comparable" labels. Severyn's deterministic comparability gates are the same idea.

**What does not overlap:**
- Yukon scores *submissions to its own verifier*. It does not extract claims from published papers such as Google, Oratomic, IonQ or Gidney.
- It has no quantum logical-vs-physical layer gate.
- ECDSA.Fail ranks Q×T only. Per `resource-claims-verification.md` (repo), failure rates appear only in free-text notes.

[INFERENCE] Eigen could add a "claims" track in days. Show it to them as a contribution, not as a rival.

### 4. Marin Ivezic / postquantum.com / Applied Quantum

**Q-Day Estimator** (published 2025-08-10, modified 2026-04-11; page read in full, tool not run):
> "select a published resource estimation paper — such as Gidney 2025 for RSA‑2048 or Google's 2026 estimate for ECC‑256 — which sets the LQC (logical qubits), LOB (logical operations budget), and QOT (logical ops/sec) targets"

Disclaimer on the same page: "for education and scenario exploration only." It is a one-paper-at-a-time preset. It has no cross-claim comparability or per-field citations.

**"Sub-900-Qubit secp256k1 Circuit Within Google's Bound"** (2026-10-14, modified 10-17; full). This is the Ledger's exact job, done by hand:
- "The comparison with Google is closer to like-for-like than most comparisons of resource estimates."
- On Dallaire-Demers' 25% physical-qubit claim, he rescales each vendor's architecture: Oratomic "16% at most", IonQ "about 28% fewer ions but run longer".
- "Dallaire-Demers called the result a breakthrough. I would hold that word until a windowed version of the circuit and an independent estimate of a full attack exist."
- "Anyone comparing leaderboard entries should read 'passed all 9,024 inputs' as an approximate circuit with a chosen test set, and look for the failure rate in the notes."

**"How Close Is the Quantum Threat? Resource Estimates"** (2026-05-12, modified 05-27; full):
- It contains a hand-made comparison table mixing RSA and ECC rows across logical qubits, Toffolis, physical qubits and runtime.
- Disconfirming: "Resource estimates for breaking ECC-256 have converged … to a consistent range of 1,200-1,450 logical qubits and 70-90 million Toffoli gates."
- Inconsistency: the table gives Chevignard et al. "~1,100" logical qubits. His **June 23** article ("The Floor Beneath…", full) says the same EUROCRYPT 2026 construction "reaches about 1,193 qubits."

**Review of Project Eleven's report** (2026-05-07; full). He flags an incomparability:
> "Appendix E's demand side is anchored to RSA-2048 via Shor's algorithm even though the blockchain threat profile is primarily ECC-256."

**Does he sell services?** Yes. The appliedquantum.com homepage (modified 2026-03-16; partial, 300 of 382 lines) offers consulting across strategy, PQC and risk, systems integration and due diligence:
> "Funds, asset managers and sovereign investors are flooded with 'quantum' pitches … but timelines and claims are hard to compare. We provide independent technical and market due diligence"

His author bio also names Quantum Academy (training and certification). I found no sale of a data or claims product.

### 5. Project Eleven

- **Bitcoin Risq List** (search snippet; "LAST UPDATED: 10/12/2026"): "7,105,958 BTC" at risk. This counts exposure, not attack cost.
- **Q-Day Prize**: awarded 2026-04-24 to Giancarlo Lelli for a 15-bit ECC key (PRNewswire snippet). It is about hardware demonstrations.
- **yellowpages** (2025-06-10 blog; snippet only): a "cryptographic registry that lets Bitcoin holders prove ownership in a post-quantum world". No overlap.
- **2026 report**: summarized from Ivezic's review above; the report itself was not read.
- **"Q-Day Clock"**: appears in search ("20x reduction in requirements for Shor's algorithm"), but `/q-day-clock` now redirects to the homepage. Treat as snippet only.

### 6. GRI / evolutionQ

**GRI page** (2026-03-09; full):
> "answered by 26 experts … CRQC quite possible (28-49%) within the next 10 years, and likely (51-70%) in the next 15."

**The report PDF** (keyword grep only). It frames estimates around Gidney 2025 (RSA). Blais (p. ~26):
> "some of the most sophisticated resource estimates we have, like (Gidney 2025) … focus on a relatively specific (type of) platform and choice of error correction, and may lead us to underestimate the potential of other platforms"

**evolutionQ Quantum Briefing June 2026** (published 2026-07-24; landing page full, briefing not read). It "examines the technical basis for the new resource estimates". Services include paid Quantum Risk Assessment and an Executive Workshop.

### 7. Pauli Group

pauli.group (undated; full):
> "We publish resource estimates, track hardware roadmaps, and translate them into actionable timelines. All our tools are open-source."

Projects: Proof of Quantum (a hardware challenge), Brace for Impact ("2029–2031" window), Anchor Wallet. It has no claim-card tool.

### 8–9. Quantum Doom Clock and Quantum Alliance

**quantumdoomclock.com** (read 2026-10-23; full text extract):
- "Cryptocurrency ~2028 1,673 logical qubits".
- "Banking & Web ~2029 2,314 logical qubits".
- "Using exponential regression on physical qubit counts over time".

**Quantum Alliance press release** (2026-10-16; full):
> "an open standards body that will set the criteria for judging quantum-resistance claims in blockchain … A network can call itself 'quantum-resistant' today with no shared understanding of which parts of its system the claim covers or what evidence should support it."

It cites the Doom Clock as a contributor model.

**cryptoticker** (2026-10-21; partial) adds: "March 2028 comes out of a model run by two parties who make their living from the subject."

### 10–13. Q-Day tracker sites

**qdayiscoming.com, RSA article** (2026-09-25; full):
> "Companies have announced higher logical-qubit counts. We leave those out of this comparison until we have checked them against a primary source."

**qdayiscoming.com, Bitcoin article** (2026-10-20; full): "fewer than 1,200 error-corrected 'logical' qubits" and "roughly 8 logical qubits measured against about 1,200 needed."

**qdaycountdown.com / Secria** (reviewed 2026-10-21; full): it separates trend lines, migration targets and deadlines, and links "Q-Day predictions tracker" and "qubits-to-break-rsa" trackers (not opened).

**BlueQubit** (read 2026-10-23; full):
- "Note that the estimates assume very different architectures, error rates and runtimes; hover the points for context."
- It cites GRI as "(32 experts, 2025 edition) … 19–34% by ~2035". **The GRI primary page says 26 experts and 28–49% within 10 years.** [INFERENCE] BlueQubit likely mislabels an earlier edition's figures.

**Qoronex** (read 2026-10-23; full):
- "Roughly ~4,000 fault-tolerant logical qubits are needed to threaten RSA-2048."
- "Current best: ~100 logical qubits (Quantinuum/Microsoft, Q1 2026)".
- "Full API access requires an approved subscription."

### 14–16. Media and explainer sites

**TQI "Q-Day Just Got Closer"** (2026-03-31; full):
- "Quantinuum's Helios processor has achieved 48 logical qubits from 98 physical qubits".
- It reports Toronto as TQI's address in its schema.

**qLABS** (2026-07-27; full). The most direct statement of practitioner confusion:
> "Most estimates come in two forms, and mixing them up causes most of the confusion here."
>
> "Quote a qubit count without its runtime, and you've quoted half the number."
>
> (On the Iceberg RSA figure used for Bitcoin) "Quoting it as Bitcoin's number is quoting the wrong paper."

### 18. BIP-360 and Ethereum

**BIP-360** (raw mediawiki v0.12.1; partial, first 300 of 456 lines; retitled to P2MR):
- The only number is footnote-level: "Shor's algorithm is believed to need 10^8 operations to break a 256-bit elliptic curve public key." It has no citation and no qubit count.
- Its motivation leans on CNSA 2.0 and NIST IR 8547 dates, not on estimates.

**ethereum.org PQ page** (current; full): "could require roughly 1,200 logical qubits … Current quantum hardware is far from this scale, operating with a few thousand noisy physical qubits."

**Delving Bitcoin BIP-360 threads**: snippet only. I saw no evidence there of arguments over which estimate is right.

**Vitalik vs Hoskinson** (cryptoticker 2026-10-10; full): the argument is about AI breaking lattices, not about qubit estimates. Hoskinson calls the key-size suggestion "numerology".

---

## Evidence that numbers in circulation are incomparable or wrong (2026)

| Quantity | Claim A | Claim B | Claim C |
|---|---|---|---|
| RSA-2048 logical qubits needed | 1,399 (Gidney 2025, via qdayiscoming, 2026-09-25) | "~4,000" (Qoronex, live) | 2,314 for "Banking & Web" (Doom Clock, live) |
| ECC-256 logical qubits needed | <1,200 (Google, via qdayiscoming and ethereum.org) | 1,673 (Doom Clock) | "1,200–2,330 logical, 0.5–320 million physical" (Quantum Horizon, PDF snippet) |
| Best logical qubits today | 8 measured (Sandia benchmark, via qdayiscoming) | 48 on Helios (TQI 2026-03-31) | ~96 QuEra (Ivezic 06-23) / ~100 (Qoronex) |
| Chevignard ECC width | ~1,100 (Ivezic 05-12) | ~1,193 (Ivezic 06-23) | — |
| GRI 2025 survey | 26 experts, 28–49% within 10 years (GRI) | 32 experts, 19–34% by 2035 (BlueQubit) | — |
| 893-qubit circuit, physical saving | "cuts … physical qubits … by 25%" (Dallaire-Demers on X, as reported by Ivezic) | Oratomic ≤16%, IonQ 27–29% fewer ions but longer runtime (Ivezic 10-14) | — |

Some rows mix the definition of "best today" (measured vs announced). That ambiguity is exactly what the Ledger's layer gate is for.

---

## Verdict

**Is the "cited, comparable claim card" niche open? Yes, but narrow, and the window is short.**

- No one publishes per-field, quote-anchored cards with deterministic gates (layer, statistic, addend interface, scope, failure budget).
- The closest analogs each miss half the job:
  - Ivezic: right analysis, prose only, not reusable.
  - qdayiscoming: sourced, but headline-level, with no convention fields.
  - Yukon: right machinery, wrong domain.
- The demand signals are real but not paid. Applied Quantum sells "claims are hard to compare" due diligence. The Quantum Alliance wants claim criteria, but for readiness. Six trackers publish conflicting figures.
- [INFERENCE] The biggest risk is that Eigen adds a "claims" lane to Yukon. Pitch it as a contribution or integration, and keep scope to cross-paper cards, which Yukon does not do.

**The 5 best people to show it to this weekend:**

1. **Marin Ivezic.** He did the 893-qubit analysis by hand on Oct 14; the demo reproduces it. X `@infosec`, LinkedIn `/in/marinivezic`, `marin@ivezic.com`.
2. **Gautham Anant, Eigen Labs.** He built the ECDSA.Fail benchmark and owns the AI-review pipeline. He is the partner or absorber, so ask about hosting or linking. X `@bbuddha_xyz`, LinkedIn `/in/gautham-anant`.
3. **Jieyi Long, Theta Labs.** He is first author of the ECDSA.Fail paper, author of the 893/874 circuits, and wrote the "numerical comparison rather than formal dominance" caveat. X `@jieyilong`.
4. **Pierre-Luc Dallaire-Demers, Pauli Group.** He co-authored the ECDSA.Fail paper and his org publishes resource estimates. His 25% claim is a demo card, so frame it neutrally and ask for corrections. X `@dallairedemers`, `contact@pauli.group`.
5. **Marco Piani / Michele Mosca, evolutionQ and GRI (Waterloo).** They author the Threat Timeline and the June briefing on new estimates. Being local and Canadian helps with the Georgian judges. Reach them through the evolutionQ contact form or X `@evolutionQinc`; I found no personal handles.

Alternates: Conor Deegan (`@conordeegan`; report author, cryptographer), Justin Drake (`@drakefjustin`; co-author of both the Google and ECDSA.Fail papers, but less likely to reply), and the TQI newsroom (`hello@thequantuminsider.com`) as a channel.

---

## Sources

| Source | Date | Depth |
|---|---|---|
| raw.githubusercontent.com/Layr-Labs/hash-smash-pareto/master/docs/HashSmash.md | undated | full |
| eigenlabs.org/blog/introducing-yukon | 2026-08-12 | full |
| eigenlabs.org/blog/open-autoresearch-the-ecdsa-fail-story | 2026-09-10 | full |
| yukon.org; yukon.org/curvesmash | read 2026-10-23 | full |
| yukon.org/hashsmash | read 2026-10-23 | partial (229 of 304 lines) |
| ecdsa.fail | read 2026-10-23 | partial (JS shell) |
| postquantum.com Q-Day Estimator | mod. 2026-04-11 | full page, tool not run |
| postquantum.com "How Close Is the Quantum Threat?" | 2026-05-12 | full |
| postquantum.com "The Floor Beneath…" | 2026-06-23 | full |
| postquantum.com "Sub-900-Qubit…" | 2026-10-14 | full |
| postquantum.com Project Eleven review | 2026-05-07 | full |
| appliedquantum.com | mod. 2026-03-16 | partial |
| Project Eleven homepage | current | full |
| Risq List, Q-Day Prize, yellowpages, Q-Day clock | various | snippet-only |
| GRI QTT 2025 page | 2026-03-09 | full |
| GRI QTT 2025 PDF | — | keyword grep only |
| evolutionQ briefing landing page | 2026-07-24 | full (briefing not read) |
| pauli.group | undated | full |
| quantumdoomclock.com | read 2026-10-23 | full (text extract) |
| Quantum Alliance press release | 2026-10-16 | full |
| cryptoticker Quantum Alliance article | 2026-10-21 | partial |
| cryptoticker Vitalik/Hoskinson article | 2026-10-10 | full |
| qday.bluequbit.io | read 2026-10-23 | full |
| qdayiscoming RSA article | 2026-09-25 | full |
| qdayiscoming Bitcoin article | 2026-10-20 | full |
| qdaycountdown.com/when-is-q-day | reviewed 2026-10-21 | full |
| qday.qoronex.co.uk | read 2026-10-23 | full |
| qlabs.tech "How many qubits…" | 2026-07-27 | full |
| TQI "Three Papers" | 2026-03-31 | full |
| arXiv 2606.14484 | 2026-06-12 | abstract full; PDF figures snippet-only |
| BIP-360 mediawiki | v0.12.1 | partial (300 of 456 lines) |
| ethereum.org quantum-resistance page | current | full |
| Delving Bitcoin threads, Quantum Computing Report, JoS QUANTUM, quantum-qanary, migration.fail | — | snippet-only or not read |
| Repo: `docs/research/resource-claims-verification.md`, `docs/decision/ranked-memo.md` | — | read for prior findings (sections) |

Contact handles marked "search snippet" were not confirmed on a profile page.