# Is there demand for verifying quantum resource claims and circuit costs?

Ticket #8, `wayfinder:research`. Researched 2026-10-22. This report builds on `field-needs.md` (2026-10-19) and does not repeat it. Read depth is given for every source. `[INFERENCE]` marks my own analysis.

---

## 1. Bottom line

- **Yes, but the demand is narrower than the "circuit registry" idea.** The strong, public, recurring demand for independent checks of resource claims sits in one place: **quantum-cryptanalysis cost claims** (ECC-256, RSA-2048). Researchers, a crowd of AI-agent users, and PQC risk analysts argue there every week about whose numbers are comparable.
- **Verifying the circuits themselves is already done for the hottest target.** Eigen Labs' **ECDSA.Fail** runs a hash-seeded evaluator with 9,024 inputs, adapted from Google's ZK verifier. By 2026-10-17 it had **1,589 submissions from 147 accounts**. Google's ZK proof and Trail of Bits' TrailMix also exist. Another verifier or leaderboard for ECC point addition would duplicate them.
- **What nobody has solved is comparing claims across sources.** Every primary source (the ECDSA.Fail paper, Google's ZK claims, TrailMix, postquantum.com) says "interfaces and accounting conventions differ" and then normalizes the numbers by hand. The leaderboard ranks only Q×T. It rejected the 893-qubit Pareto point with "score did not improve current best". Failure rates exist only in free-text submission notes.
- **Program evaluators are real buyers, but not by Oct 25.** DARPA's QBI IV&V topic (open to **2026-12-30**) explicitly invites algorithm-only entities. NRC's Benchmarking Quantum Platform assesses CQCP companies. Both evaluate whole-machine concepts under NDA and conflict-of-interest rules, so neither is a hackathon user.
- **Best wedge: a "quantum cryptanalysis claim ledger".** An LLM extracts each claim into a card with citations. Deterministic code re-checks the arithmetic and statistics, flags which claims are comparable, and plots an honest Pareto chart. Its users are PQC risk analysts and the ECDSA.Fail community. It fits in 12 hours and scores **32/45**.
- **Skip the general non-crypto subroutine registry.** I found no evidence of demand: `uncompute` has 3★ and Bartiq's issues contain no verification requests. Eigen Labs is also already generalizing open leaderboards (HashSmash).

---

## 2. The pain

### 2.1 Who has it, how often, and what they do today

| Who (named) | Pain, observed | What they do today | Cost to them | Source (date, depth) |
|---|---|---|---|---|
| **Marin Ivezic**, founder of Applied Quantum, author of postquantum.com (former Fortune Global 500 CISO) | Each new claim has to be checked by hand against Google, Oratomic and IonQ. For example, the 2026-10-13 claim that an 893-qubit circuit "cuts physical qubits by 25%". | Hand analysis. He reads submission notes to find the failure rate (111 of 360,960 additions) and computes that a run of the 9,024-input check "would come out clean about 6% of the time". He rescales block counts in each vendor's architecture (12–16% for Oratomic, 27–29% for IonQ). His advice: "read 'passed all 9,024 inputs' as an approximate circuit with a chosen test set." | A multi-hour article per claim `[INFERENCE]`. His own words: "The field is moving faster than anyone can keep scorecards updated." | [postquantum ECDSA.Fail article](https://postquantum.com/security-pqc/ecdsa-fail-low-qubit-circuit/), 2026-10-14, mod. 10-17, **full**. [CRQC Scorecard](https://postquantum.com/post-quantum/crqc-scorecard-how-close/), upd. 2026-06-04, **partial** (first half) |
| **ECDSA.Fail authors**: Jieyi Long (CTO, Theta Labs), Eigen Labs (Gajesh Naik, Gautham Anant, Soubhik Deb), Justin Drake (Ethereum Foundation), Pierre-Luc Dallaire-Demers (Pauli Group, Calgary) | Their own paper says: "differing interfaces, accounting conventions, and validation scope preclude formal dominance." The score "is an empirical cost over finite, submission-selected support rather than a certified bound". Nonce re-rolling makes up **4.8%** of scored commits. A `DUMMY_TOFFOLIS` padding mechanism also appears in the archive. | A hand-built comparison table (Table 3) and a hand-curated reconstruction package. That package uses a "public-note-parser sensitivity rule" to pull metrics out of note text. | 62-page paper, 35 authors. The Pareto analysis needed three different admission rules. | [arXiv 2609.09582v2](https://arxiv.org/abs/2609.09582), 2026-09-19, **partial** (abstract, §1, §3.3, §5.1, §5.5, §6 in full); [reconstruction README](https://github.com/jieyilong/ecdsafail-supplemental-materials/tree/d6cdcd4be0204b8df7b6d6c486ccd5702da0b7bd/frontier_reconstruction), **full** |
| **ECDSA.Fail participants** (147 accounts; e.g. Matt Zweil / Mochimo Foundation, jackylee0424, gnuchev) | No official error-rate rule exists, so the community made its own: a "limiting contract" capping **λ ≤ 19.5 failing shots per 9,024**, "raised from 18 after discussions with the ECDSA.fail Telegram community". Participants also run paired fresh holdouts, deliberate-fault controls, and "independent agent" reviews by hand inside each PR. | Free-text audit sections in every PR, for example PR #936 (λ = 18.23 on 248 inputs) | Thousands of words of audit text per submission `[INFERENCE: from PR bodies read]` | PRs [#936](https://github.com/Layr-Labs/ecdsafail-challenge/pull/936) and [#937](https://github.com/Layr-Labs/ecdsafail-challenge/pull/937), 2026-10-23 UTC, **full** (2 PR bodies); [submission 457ccb7a](https://api.ecdsa.fail/api/submissions/457ccb7a-4436-4e8c-8e8c-f7d22c3c81b5), 2026-10-13, **full** |
| **Trail of Bits** (Keegan Ryan; Joe Doyle's crypto team) | Forged a Google ZK proof claiming **0 Toffolis / 1,164 qubits** by exploiting unsafe Rust deserialization and register aliasing. Their conclusion: ZK proofs "redistribute trust ... to programming languages, compilers, proof systems". | Manual security audit. Google patched its proof (arXiv 2603.28846v2). | Shows that a cost claim can be wrong even when the proof verifies | [ToB blog](https://blog.trailofbits.com/2026/04/17/we-beat-googles-zero-knowledge-proof-of-quantum-cryptanalysis/), 2026-04-17, **full** |
| **Qualtran users and maintainers** (Google: Fionn Malone, Matt Harrigan, Bill Huggins) | A user's THC/QPE run gave **1,300 trillion Toffolis vs 33 billion in the paper** (#1591, open since 2025-03-10). The cause traced to missing QROAM costing and random coefficients. A 7-T vs 4-T CSwap convention caused inconsistent T counts (#1463, fixed 2025-05-08). | GitHub issue threads | Months to resolve | [#1591](https://github.com/quantumlib/Qualtran/issues/1591) (2025-03-10 to 2025-07-14), **full**; [#1463](https://github.com/quantumlib/Qualtran/issues/1463) (2024-10, **possibly stale**), **full** |
| **GRI / evolutionQ** (Michele Mosca, Waterloo; Marco Piani) | Their annual survey of 26 experts lags new resource estimates. Ivezic notes that four landscape-reshaping papers landed weeks after the survey closed. | Annual opinion survey | Lagging indicator for CISOs and boards | [postquantum review of the GRI report](https://postquantum.com/security-pqc/quantum-threat-timeline-report-2025/), 2026-04-05, **full** (GRI PDF itself not read) |

**Frequency.** On ECDSA.Fail, several submissions arrive per day: two PRs merged or closed within 1 hour on 2026-10-23 UTC. The literature also moves fast: Google 2603.28846 (Mar), Luo 2604.02311 (Apr), Schrottenloher 2606.02235 (Jun), IonQ 2609.05625 and ECDSA.Fail 2609.09582 (Sep), Jo & Lee ePrint 2026/2014 (Sep), Gu 2610.22367 (Oct). That is **at least 7 ECC-cost papers in 7 months**, each with its own conventions (counted from sources cited above).

### 2.2 Additions and corrections to `field-needs.md` §4 (personas)

- **P4 (PQC and crypto-risk analysts) is the strongest persona. In `field-needs` it was the weakest.** It now has named people: Ivezic, Dallaire-Demers, and the Ethereum Foundation through Justin Drake. It also has observable weekly work, listed above. evolutionQ/GRI are confirmed as the Waterloo-based authors of the Threat Timeline.
- **P2 (program evaluators) is confirmed, but with limits.** The DARPA QBI FAQ, item 10, says entities "interested in working only on applications and algorithms" may submit to the **IV&V topic DARPA-PA-26-02-01**. That topic was published 2025-11-17 with a **deadline of 2026-12-30**, not the 2026-10-15 stated in `field-needs`. FAQ item 11 warns that an IV&V award may exclude the awardee from being a QBI performer because of organizational conflict of interest. Foreign participants are allowed, subject to export controls (item 13). NRC's "Benchmarking Quantum Platform ... assess[es] each company's technical progress" on the *underlying quantum technologies*, not algorithm costs ([Canada.ca](https://www.canada.ca/en/innovation-science-economic-development/news/2025/12/minister-solomon-announces-major-new-quantum-initiative.html), 2025-12-15, **full**). The QBI Stage B list, current as of 2026-10-08, now has **7** companies, still including Nord Quantique, Photonic and Xanadu ([DARPA QBI](https://www.darpa.mil/research/programs/quantum-benchmarking-initiative), **full**).
- **P2 also gains a second buyer: DOE ASCR LAB 26-3603, "Quantum HPC Validation and Verification Testbed".** Issued 2026-09-17, it offers **$45 M** for 1–2 awards of $7–15 M per year over 3 years. Only DOE national labs may lead. Letters of intent closed 2026-09-30 and proposals are due **2026-11-10**. The call:
  - requires V&V across hardware, logical architecture, **"quantum algorithm design, and resource estimation"**;
  - asks for "well-defined performance measures ... reproducible by members of the research community outside of the framework development team";
  - requires a plan for "an **open standard** for a quantum validation and verification framework";
  - requires **≥2 external collaborators**, one with expertise in "interoperability, and dissemination" of V&V tools;
  - excludes single-modality proposals.

  An open claim-card schema could be a deliverable for a lab team after the hackathon. That only works as a subaward to a team that already filed an LOI, so it is not an Oct 25 user ([LAB 26-3603](https://science.osti.gov/-/media/grants/pdf/lab-announcements/2026/LAB-26-3603.pdf), **partial**, pp. 1–12; lead from peer DemandMap, verified).

  DOE's ["Quantum Genesis Priority Applications"](https://www.energy.gov/documents/quantum-genesis-priority-applications) (11 pp., PDF created 2026-10-08, **full**) says progress "will require a clear understanding of resource estimation and optimization ... and performance benchmarking against the best-known classical alternatives". It also lists as a knowledge gap "moving beyond algorithm design into concrete resource estimates", and warns that "current estimates of required quantum resources may place it out of reach for the first generation of SRQCs". This is demand for *having* trustworthy estimates for chemistry, materials, lattice gauge theory and linear algebra, not an explicit call to audit them. `[INFERENCE]` The same claim-card engine could cover a DOE-target view, which peer DemandMap proposes; its crypto-ledger users would differ.
- **P5 (tool maintainers) is weak.** Bartiq's 25 open issues contain no request for verified costs; the newest, #303 (2026-10-10), is a roll-up inconsistency. Qualtran's evidence is about mismatches, not a request for a registry.
- **New persona: open-autoresearch platform operators.** Eigen Labs runs ECDSA.Fail and HashSmash, with an oversight board that includes Zooko and Justin Drake. The HashSmash design doc plans "LLM-assisted validation of the method, cost estimates ... **Exact harness TBD**" and a machine-readable claim sheet ([HashSmash.md](https://github.com/Layr-Labs/hash-smash-pareto/blob/master/docs/HashSmash.md), undated, **partial** lines 1–300). This is a potential partner or customer, and also the most likely competitor.

---

## 3. Existing solutions

| Product / tool | What it does | Who uses it | Price / license | Read depth |
|---|---|---|---|---|
| **ECDSA.Fail** (Eigen Labs) | Public leaderboard for secp256k1 point addition. Evaluator checks classical output, ancillas, phase and forward∘reverse identity on 9,024 SHAKE256-hash-seeded inputs. Score is Q × average executed T. Also has low-Q and low-T tracks. | 147 accounts, 1,589 submissions (2026-10-17); many use Claude Code and Codex | Free. Repo: GitHub API reports **no license file**; the ToS says repo contents are **MIT** and promoted submissions are **Apache-2.0**. Hosted API and leaderboard are **proprietary**, licensed "solely to participate in challenges". 92★, last push **2026-10-23T01:37Z** | README **full**; ToS (eff. 2026-10-07) **full**; homepage **partial** (JS-rendered) |
| **Google ZK attestation** (Babbush et al., SP1 zkVM + Groth16) | Proves bounds on Q and T for an undisclosed circuit | Google Quantum AI; reused as the ECDSA.Fail harness | Zenodo 19597130 (license **unverified**: HTTP 403) | via ToB (full) and `field-needs` |
| **TrailMix** (Trail of Bits) | Rust toolchain for kickmix circuits: 64-shot simulator, abstract-interpretation phase gate, time-travel debugger, 5 open EC-add circuits (e.g. 1,169 q / 2.09 M T) | ToB; ECDSA.Fail participants built on it | 27★, 7 commits; **no license shown**; last-commit date **unverified** (API 403) | README **partial** (first 300 lines) |
| **postquantum.com CRQC Scorecard + Q-Day Estimator** (Ivezic) | Demand-side presets from papers (LQC, LOB, QOT) vs supply-side modality growth, giving a projected Q-Day | CISOs, risk committees | Free web tool; no license or data export seen | Estimator page **full** (tool not exercised); Scorecard **partial** |
| **quantumresourceestimator.com** | Browser surface-code calculator with Gidney-Ekerå, FeMoco and Grover presets | Education, planning | Free, open methodology; owner unknown | **full** page |
| **GRI/evolutionQ Quantum Threat Timeline** | Annual expert survey (26 experts in 2025) | CISOs, regulators | Free PDF | via postquantum review (**full**); PDF not read |
| **`andigu/uncompute`** | 8 non-crypto kickmix tasks with graders and certified results | Gu et al. | Apache-2.0, 3★, pushed 2026-10-16 (verified 2026-10-19 in `field-needs`; not re-checked) | from `field-needs` |
| **Qualtran, Bartiq/QREF, MS QRE, TopQAD** | Aggregate and estimate costs; do not certify (see `field-needs` §2) | FT researchers, vendors | Various | from `field-needs` |
| **GQI, The Quantum Insider** | Market intelligence; "analyst-verified" means provenance only | Investors, governments | $2,999–5,999 datasets (TQI) | from `competitors-intelplatforms.md` |
| **Papa 2025** (Google, arXiv 2506.03318) | Unit-test validation that found **4 uncomputation errors** in the then state-of-the-art ECC point-addition circuit | Research | arXiv | **snippet-only** (abstract); supporting evidence only |

---

## 4. The gap

1. **No cross-source, machine-readable record of what each claim counts.** For ECC point addition alone, sources mix:
   - Toffoli counts that are average executed, emitted, or worst-case;
   - a classical addend vs a coherent windowed lookup (the ECDSA.Fail paper measured the windowed overhead at **+11 qubits and +29.6% T**);
   - validation corpora that are hash-selected Fiat-Shamir or independent (FS 9,024; 10,000 tests; 100,000 random; 360,960 trials);
   - attestation by ZK proof, open source, or bounds only;
   - scope that is one point addition or a full attack (×28 windowed additions).

   Ivezic, the ECDSA.Fail authors and TrailMix each rebuild this mapping by hand (§2).
2. **Leaderboards rank one scalar.** ECDSA.Fail promotes only Q×T improvements, so Pareto-relevant low-width circuits are recorded as "rejected", and their failure rates live only in notes.
3. **Evidence quality is not graded.** A circuit "passing 9,024" may still fail at roughly 1 in 3,250. A ZK proof can be forged (ToB). A library can return a cost 4 orders of magnitude off the paper (Qualtran #1591).

**Why nobody has filled it** `[INFERENCE]`:
- Researchers are rewarded for new circuits, not for bookkeeping.
- Eigen Labs optimizes its own leaderboard.
- Ivezic sells consulting and writes articles, so manual analysis is his product.
- The field became fast-moving only in 2026, when the Google, Oratomic and ECDSA.Fail results landed in Mar–Oct.
- Extracting conventions from 60-page papers was impractical before capable LLMs.

**Strongest reason it fails.** The people with the pain are few: perhaps dozens of analysts and a few hundred leaderboard participants. They already do the work themselves, and Eigen Labs could add a claim sheet plus LLM review to ECDSA.Fail, as it is already designing for HashSmash.

---

## 5. Candidate wedges

### Wedge A: Quantum Cryptanalysis Claim Ledger (recommended)

- **User.** PQC risk analysts writing threat assessments: Ivezic/Applied Quantum, evolutionQ in Waterloo, Pauli Group, Ethereum Foundation PQ researchers. Second user: ECDSA.Fail participants comparing against external papers.
- **Job.** Turn any ECC or RSA resource claim (arXiv paper, ePrint, ECDSA.Fail submission ID) into a **claim card** in about 60 seconds. Each card holds:
  - fields: target; scope; interface; Q; T and what kind of T; ops; failure evidence (k / N, corpus type); attestation; physical assumptions;
  - for every field, the **page, table or equation citation** it came from;
  - deterministic re-checks:
    - Q×T;
    - Clopper–Pearson interval on the failure rate;
    - P(clean 9,024 run);
    - full-attack extrapolation (×28, + windowed-lookup overhead) **labelled as an extrapolation**;
  - comparability flags against every other card.

  Output: a Pareto chart where non-comparable edges are visibly marked, plus a "what changed this week" feed.
- **2-minute demo.**
  1. Paste the 2026-10-13 submission ID 457ccb7a. A card appears with cited fields.
  2. The ledger flags "average executed T, classical addend, FS-selected support". It shows "111/360,960 failures → P(clean 9,024 run) ≈ 6%" and "not comparable to IonQ's 1.4 M/addition, which includes the lookup". These reproduce Ivezic's hand analysis automatically.
  3. Paste arXiv 2606.02235. The Pareto chart updates.
  4. Close on the eval panel: extractor field accuracy on 10 hand-labelled claims, with ground truth from ECDSA.Fail Table 3 and Ivezic's numbers.
- **Reusable components.**
  - arXiv HTML, which is CC BY 4.0 for 2609.09582.
  - The ECDSA.Fail frozen API snapshot (831 rows) in `jieyilong/ecdsafail-supplemental-materials`; license **not checked**.
  - Public ECDSA.Fail PR bodies on GitHub.
  - Clopper–Pearson from `scipy` (BSD).
  - Do **not** depend on the hosted ECDSA.Fail API without Eigen Labs' permission (ToS §5).
- **Data and compute.** About 20 seed claims: Litinski 2023; Google ×2; Schrottenloher; Luo; TrailMix ×5; ECDSA.Fail paper points; Long 893 and 874; current 1,234 q / 761 k leader; Gu divsteps; IonQ; Oratomic; Gidney RSA 2025; Chevignard; Jo & Lee (flagged "no concrete count"). Laptop plus Render, no GPU.
- **LLM cost.** About 20 documents × 40–80 k tokens in, plus structured output and a second-pass checker, comes to **≈ $10–30** of the $100 credit `[INFERENCE]`.
- **Partner prizes.**
  - **Eon Era**: the extractor-accuracy harness is agent testing and benchmarking.
  - **SurrealDB Agent Memory**: the claim graph links sources, cards and lineage (`builds_on`, `supersedes`, which ECDSA.Fail notes already declare).
  - Clerk: analyst annotations; weak fit.
- **Main way it fails.** Extraction errors on dense papers erode trust. Mitigations: show the citation for every field, require a human "approve" step, and publish the accuracy score. Adoption is the second risk, because analysts may keep doing it by hand. Mitigation: ask Ivezic, Dallaire-Demers and Gautham Anant for a "would use" reply before Oct 25.

### Wedge B: fresh-corpus re-certifier for kickmix circuits

- **User.** ECDSA.Fail participants and maintainers.
- **Job.** Rebuild a submission commit, then:
  - evaluate it on a **circuit-independent** corpus of 100 k inputs;
  - report the failure rate with a confidence interval;
  - diff its operation stream against the parent to flag nonce re-rolls and padding;
  - emit a signed certificate in JSON.
- **Demo.** Re-certify the 893-qubit circuit and show λ, the interval, and the "verifier-search only" flag.
- **Reuse.** The ECDSA.Fail harness (MIT per the ToS; Rust) and `uncompute` (Apache-2.0) for the non-crypto tasks.
- **Compute.** One CPU-heavy run per circuit: about 27 M ops × 100 k shots on a 64-shot bit-parallel simulator, taking minutes to hours `[INFERENCE]`.
- **LLM cost.** Under $5.
- **Prize fit.** Eon Era (weak).
- **Fails because:**
  - participants already do paired fresh holdouts by hand (PR #936);
  - Eigen Labs can add this in a day;
  - AI adds little;
  - the tool sits inside the attack-circuit optimization loop, which is a dual-use optics problem for the Security and Ethics criterion.

### Wedge C: open registry for non-crypto FT subroutines

- **User.** FT algorithm researchers: Gu et al., QuEra, chemistry teams.
- **Job.** Run the `uncompute` 8-task graders as a submission service with hash-seeded tests plus hold-out certification and a Pareto view over (T, Q, ε).
- **Reuse.** `uncompute` (Apache-2.0) and OpenEvolve (Apache-2.0).
- **Cost.** Under $10.
- **Fails because** no demand was observed: 3★, no community, and Bartiq/Qualtran maintainers are not asking for it. Eigen Labs' Yukon platform is already generalizing leaderboards (ECDSA.Fail → HashSmash).

---

## 6. Scores: Wedge A (Claim Ledger)

| Criterion | Score | Why |
|---|---|---|
| Real user with evidence of pain | 4 | Named analysts and the ECDSA.Fail authors do this normalization by hand, publicly and weekly (Ivezic 2026-10-14; paper §6; PR #936). Nobody has yet asked for a tool. |
| AI makes a material difference | 3 | The bottleneck is LLM extraction of conventions from 60-page papers and 10 k-word notes. The trust layer (statistics, comparability) must stay deterministic. |
| Severyn's unfair advantage | 4 | MSc in quantum information, a resource-estimation demo built at 1QBit, verification-first Aquarium lab, and Waterloo proximity to evolutionQ/GRI. |
| Buildable and demoable in 12 hours | 4 | About 20 seed claims, a schema, extractor, checker, Pareto UI and eval panel. No GPU and no circuit execution needed. |
| Judge appeal (Georgian investors) | 3 | Q-Day risk for banks, custodians and crypto is salient, and "AI that audits AI-generated science" is a clear story. Still niche, with no paying buyer shown. |
| Adoption path after Oct 25 | 3 | Free and open source, with reachable named users (postquantum.com, Pauli Group, Eigen Labs). Funded V&V programs exist that want "open standards": DARPA IV&V (deadline 2026-12-30) and DOE LAB 26-3603 (labs-led, due 2026-11-10). No user or program has confirmed interest. |
| Competition density (5 = open field) | 3 | Ivezic's estimator and scorecard work at headline level only. ECDSA.Fail covers its own track. Eigen's HashSmash plans LLM claim review. No one offers cross-source claim cards. |
| Credibility gain in AI and quantum | 4 | Shows command of FT cost accounting and a measured LLM extraction eval, in the hottest FT-cost topic of 2026. |
| Risk (5 = low: no dual use, no 1QBit overlap) | 4 | It aggregates public claims and produces no circuits. 1QBit overlap stays low **if the physical-qubit projection is excluded** or limited to quoting published numbers. |
| **Total** | **32 / 45** | |

---

## 7. Sources

| # | Source | Date | Read depth |
|---|---|---|---|
| 1 | Ivezic, "Sub-900-Qubit secp256k1 Circuit Within Google's Bound", https://postquantum.com/security-pqc/ecdsa-fail-low-qubit-circuit/ | 2026-10-14 (mod. 10-17) | full |
| 2 | Ryan (Trail of Bits), "We beat Google's zero-knowledge proof...", https://blog.trailofbits.com/2026/04/17/we-beat-googles-zero-knowledge-proof-of-quantum-cryptanalysis/ | 2026-04-17 | full |
| 3 | Long et al., "ECDSA.Fail: Open Autoresearch...", https://arxiv.org/abs/2609.09582 (HTML v2) | 2026-09-19 | partial (abstract, §1, §3.3 headings and text, §5.1, §5.5, §6 full) |
| 4 | ECDSA.Fail README, https://github.com/Layr-Labs/ecdsafail-challenge | repo pushed 2026-10-23T01:37Z | full; repo metadata via GitHub API 2026-10-22 |
| 5 | ECDSA.Fail PRs #936, #937 | 2026-10-23 UTC | full (bodies) |
| 6 | ECDSA.Fail submission 457ccb7a, https://api.ecdsa.fail/api/submissions/457ccb7a-4436-4e8c-8e8c-f7d22c3c81b5 | 2026-10-13 | full |
| 7 | ECDSA.Fail Terms, https://ecdsa.fail/terms | effective 2026-10-07 | full |
| 8 | ECDSA.Fail homepage, https://ecdsa.fail | undated | partial (JS-rendered) |
| 9 | Frontier reconstruction README, jieyilong/ecdsafail-supplemental-materials | 2026 (commit d6cdcd4) | full |
| 10 | HashSmash design doc, https://github.com/Layr-Labs/hash-smash-pareto/blob/master/docs/HashSmash.md | undated | partial (lines 1–300) |
| 11 | TrailMix README, https://github.com/trailofbits/trailmix | ~2026-06 (per ToB post on X, snippet) | partial (first 300 lines) |
| 12 | DARPA QBI IV&V topic, https://www.darpa.mil/work-with-us/opportunities/darpa-pa-26-02-01 | published 2025-11-17 | full (short page); SAM.gov solicitation not read |
| 13 | DARPA QBI program page, https://www.darpa.mil/research/programs/quantum-benchmarking-initiative | current as of 2026-10-08 | full |
| 14 | DARPA QBI Stage A FAQ, https://www.darpa.mil/sites/default/files/attachment/2026-03/darpa-qbi-q-a-2026.pdf | 2026-03 (file path) | full |
| 15 | DARPA QB (completed program) page, https://www.darpa.mil/research/programs/quantum-benchmarking | 2024 content, **possibly stale** | full |
| 16 | ISED, CQCP Phase 1 announcement, https://www.canada.ca/en/innovation-science-economic-development/news/2025/12/minister-solomon-announces-major-new-quantum-initiative.html | 2025-12-15 | full |
| 17 | Ivezic, GRI Threat Timeline review, https://postquantum.com/security-pqc/quantum-threat-timeline-report-2025/ | 2026-04-05 | full |
| 18 | Ivezic, CRQC Readiness Benchmark / Q-Day Estimator, https://postquantum.com/crqc-readiness-benchmark-q-day-estimator/ | mod. 2026-04-11 | full (tool not exercised) |
| 19 | Ivezic, CRQC Scorecard, https://postquantum.com/post-quantum/crqc-scorecard-how-close/ | upd. 2026-06-04 | partial (first half) |
| 20 | quantumresourceestimator.com | undated | full |
| 21 | Qualtran issue #1591 | 2025-03-10 to 2025-07-14 | full |
| 22 | Qualtran issue #1463 | 2024-10-10 to 2025-05-08, **possibly stale** | full |
| 23 | Bartiq open issues list, https://github.com/PsiQ/bartiq/issues | as of 2026-10-22 | full (titles only) |
| 24 | Papa, arXiv 2506.03318 | 2025-06-03 (v2 2025-07-14) | snippet-only (abstract) |
| 25 | Jo & Lee, IACR ePrint 2026/2014 | 2026-09 | snippet-only (abstract) |
| 26 | Zenodo 19597130 (Google ZK code); HPCwire CQCP article | — | **not read** (HTTP 403) |
| 26b | DOE ASCR LAB 26-3603, Quantum HPC V&V Testbed, https://science.osti.gov/-/media/grants/pdf/lab-announcements/2026/LAB-26-3603.pdf | 2026-09-17 | partial (pp. 1–12: summary, funding, eligibility, purpose, teaming, scope) |
| 26c | DOE, Quantum Genesis Priority Applications, https://www.energy.gov/documents/quantum-genesis-priority-applications | 2026-10-08 (pdfinfo CreationDate) | full (pdftotext, 11 pp.) |
| 27 | `field-needs.md`, `competitors-intelplatforms.md`, `evolve-systems.md`, `quantum-ai-discovery.md` (this repo) | 2026-10-19 to 10-21 | skimmed (field-needs full) |

---

## 8. Open questions

1. **Outreach before choosing.** Will Severyn message Ivezic (postquantum.com contact page), Dallaire-Demers (pierre-luc@pauli.group, per arXiv 2603.25519) and Gautham Anant (Eigen Labs) tonight and ask, "Would you use a cited claim card for each new ECC cost claim?" One "yes" turns adoption from 3 into 4.
2. **Data rights.** The hosted ECDSA.Fail API is licensed "solely to participate in challenges". Can the ledger use submission data via public GitHub PR text and the frozen snapshot, or should Severyn ask Eigen Labs first?
3. **Ethics framing.** Is a cryptanalysis-adjacent topic acceptable for the Security and Ethics criterion and for 1QBit positioning? My recommendation: frame it as defensive PQC migration intelligence, show no circuit internals, and keep physical-qubit projections out to stay clear of TopQAD.
4. **Scope.** ECC only, or ECC plus RSA-2048? ECC has the live community; RSA has the GRI and CISO audience. I recommend ECC-first with 3 RSA cards.
5. **Synthesis.** How does 32/45 compare with the other tickets' best wedges? This wedge has the clearest named users doing the job by hand today. Its weakness is market size and judge appeal, not evidence.
6. **DOE LAB 26-3603.** Does Severyn have a contact at a DOE lab team that filed an LOI (Sep 30) and still needs an external collaborator on "interoperability and dissemination"? If so, the claim ledger's open schema becomes a concrete post-hackathon path.
