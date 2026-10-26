# AI-for-science next to quantum: where verification or automation is the bottleneck

Ticket #12. Researched 2026-10-22. Read-depth labels: `full`, `partial (sections …)`, `abstract-only`, `snippet-only`. Nothing `snippet-only` or `abstract-only` carries a conclusion. `[INFERENCE]` marks my own analysis. `[STALE]` marks sources older than 18 months (before 2025-04-22).

---

## 1. Bottom line

1. **The verification bottleneck is real, documented and recent in one place: checking AI-proposed inorganic materials by powder X-ray diffraction (XRD).** Berkeley's A-Lab (Nature 2023) claimed 41 new compounds. Princeton/UCL showed most were misidentified or were known disordered phases. Nature published an author correction on 2026-01-19 that drops 4 compounds and withdraws the "new to science" claim. On 2026-09-15, Periodic Labs ($300M seed) wrote that "scientists can no longer keep up with analyzing XRD results manually" and that XRD success "cannot be cheaply verified".
2. **Most of it is already being automated by well-resourced players.** Periodic trained a 1T-parameter model (Neon) on its own lab data for this one task. Ceder's group ships Dara (MIT licence, multi-hypothesis Rietveld search). Oak Ridge published RADAR-PD (May 2026). Bruker sells AI-assisted phase ID. Severyn has no data moat and no crystallography expertise here.
3. **The open gap is narrow: a neutral, falsification-first "is this material actually new?" audit.** It would run the two checks that broke A-Lab (known-phase mixtures, and the ordered prediction vs a known disordered phase) and emit an evidence-graded report. All components exist under MIT/CC0 (Dara, pymatgen, MatterGen's `DisorderedStructureMatcher`, COD). No one packages them as a third-party audit. `[INFERENCE]`
4. **Quantum sensing is a poor fit for 12 hours.** The software pain is per-device calibration (NV magnetometers). It is hardware-specific, the data is proprietary, the main buyers are defence navigation (dual-use), and no user can be reached before Oct 25.
5. **AI-scientist report verification (Claude Science, Kosmos) is real but generic and crowded.** Kosmos's "synthesis" statements are only 57.9% accurate. Claude Science already ships a built-in fact-checker. This wedge does nothing for Severyn's quantum credibility.
6. **Verdict: no, this is not the pick for tonight.** The best wedge (W1, the materials novelty audit) scores 26/45. It is weak on Severyn's edge (2/5), adoption path (2/5) and quantum credibility (2/5). Keep it as a backup only. The transferable lesson for the memo: in science, the sellable unit is a falsification check with an explicit cost of being wrong. That supports the quantum-native verification wedges in `field-needs.md`.

---

## 2. The pain

### 2a. Materials: verifying that an AI-proposed compound was made, and is new

| Who | Evidence (observed) | Date | Read depth |
|---|---|---|---|
| **Berkeley A-Lab** (Ceder, Persson, Zeng; LBNL), with Google DeepMind co-authors | Author correction: "concerns were raised about the unambiguous identification of the compound structures using diffraction as well as the original claims of material novelty." After manual re-analysis, 36 of 40 successes were confirmed and 4 are "inconclusive from XRD alone". One compound was "mistakenly included in the training data". Novelty was redefined as "new to the prediction platform, not necessarily new to science". | 2026-01-19 | full (correction notice) |
| **Princeton (Schoop lab) / UCL (Palgrave)**: solid-state chemists acting as external referees | They examined all 43 A-Lab products and found "four common shortfalls". Conclusion: "no new materials have been discovered in that work". "Two thirds of the claimed successful materials … are likely to be known compositionally disordered versions." They ask for "a reliable artificial-intelligence-based tool for Rietveld fitting". Worked examples: Mg₃NiO₄ is an MgO–NiO solid solution (Vegard's law fits the lattice parameter exactly); Sn₂Sb₂Pb₄O₁₃ refines as known Pb₂SnSbO₆.₅ + SnO₂ (the "Naples Yellow" pigment family). | 2024-03-07 `[STALE]`, but re-confirmed by the 2026 correction | partial (abstract, §I–III, §IV.A–D) |
| **Periodic Labs** (CEO Liam Fedus; Menlo Park, Montreal ML office; $300M seed led by a16z/Accel/Khosla with Toronto's Radical Ventures) | "As we scale our autonomous labs, scientists can no longer keep up with analyzing XRD results manually." Hard patterns take "several hours of expert time per pattern" and contain ~5 phases on average. "Science is *falsifiable*, but not easily verifiable." Three PhD experts agree with each other 77.2% of the time. Their LLM-judge ensemble agrees with experts 74.6% of the time and with expert consensus 84%. Neon reaches 55.3% on FrontierXRD (134 hard samples). Periodic's harness is 3.8× Claude Code + COD/MP/BGMN at the same model. | 2026-09-15 (posted 2026-10-01) | full |
| **Periodic, Meissner, FL01** (the latter two are Toronto startups and CDL graduates; Meissner targets superconductors "for quantum computing, nuclear fusion"; $3.6M pre-seed from BDC) | "Firms applying AI to materials science must screen for practicality; otherwise, their models might come up with substances that are perfect in theory but impossible to manufacture." Periodic "charges clients to use its software". | 2026-10-07 | full |
| **Fritz Haber Institute / Imperial** (Jakob, Walsh, Reuter, Margraf) | 47% of ICSD entries are disordered. A classifier predicts **80–84% of GNoME** and 39–47% of MP-only predictions are likely substitutionally disordered. It flags 16 of the 23 A-Lab compounds with known disordered phases, and 9 of the 10 GNoME examples critiqued by Cheetham & Seshadri. | 2025-10-23 | partial (abstract, §1–3, Methods) |
| NIST (Nguyen … Ratcliff) | 82.9% of new ICSD formulas fall into existing structural communities. GNoME, MP-theoretical, JARVIS and Alexandria all "depart" from experimental basins more than MatterGen does. They propose a "historical synthesizability prior for triaging". | 2026-06-29 | abstract-only |
| Cheetham & Seshadri (UCSB), on GNoME | Novelty and practicality critique (e.g. actinium compounds) | 2024-04 `[STALE]` | snippet-only (used only via Jakob's summary) |

**How often and at what cost.** Every autonomous-synthesis run ends in an XRD call. Periodic says hard patterns take hours each and that throughput, not instruments, is the limit. A misidentification that reaches publication costs a Nature correction 26 months later and public reputational damage (A-Lab). `[INFERENCE: no source prices an XRD analyst hour; at expert rates, several hours per hard pattern is the order of $100s per sample.]`

**What people do today.** Search/match against PDF-5/ICSD/COD (Bruker DIFFRAC.EVA, Profex/BGMN), then manual Rietveld refinement with expert judgment. Dara automates the multi-hypothesis search. Periodic built an in-house harness and model.

### 2b. AI-scientist outputs (cross-domain)

- **Kosmos** (Edison Scientific, the FutureHouse spinout): independent scientists judged 79.4% of 102 statements accurate. By type: data analysis 85.5%, literature 82.1%, **synthesis/interpretation 57.9%**. Priced at $200/run at launch. Dates: 2025-11-05 (blog) and arXiv 2511.02824. Read depth: partial (abstract, §1 results, Fig. 1 caption) and full announcement paragraph.
- **Claude Science** (Anthropic, beta on Pro/Max/Team/Enterprise, 2026-06-30): "A separate fact-checker AI then double-checks the citations and calculations before anything goes to publication". TechCrunch's caveat: "it's still the same underlying model checking itself". Every figure carries its "exact code and environment". Read depth: full (TechCrunch). Anthropic's own page returned 404.

### 2c. Quantum sensing

- **SBQuantum** (Sherbrooke, QC; NV diamond magnetometers): $4M USD seed (Quantonation, Quantacet, Investissement Québec), >$15M in R&D contracts incl. ESA and Canada's DND, and a US sister company (Zero Drift) "to serve defense and government contracts". 2026-04-16. Read depth: full. The market is GPS-denied navigation, i.e. **dual-use**.
- NV magnetometry "deployment remains bottlenecked by complex calibration" (Daniel et al., arXiv 2608.19582, 2026-08-20). Read depth: abstract-only.
- Qruise automated bring-up of XeedQ's 5-qubit NV system (2026-05-02). Read depth: full, but the source is a low-trust aggregator (quantumintel.tech); not relied on.
- **Microsoft Majorana 2** (2026-06-02): agents automated the parity measurements that previously took "weeks" and "cut the cycle time by orders of magnitude". An agent also found "an uncalibrated temperature sensor reading". Read depth: full. This is real automation pain, but it sits inside proprietary hardware teams. `[INFERENCE]`

---

## 3. Existing solutions

| Product / tool | What it does | Who uses it | Price / licence | Date | Read depth |
|---|---|---|---|---|---|
| **Dara** (`CederGroupHub/dara`) | Exhaustive tree search over phase combinations in a chemical system. Every hypothesis is validated by BGMN Rietveld refinement. Returns multiple hypotheses when ambiguous. Ships a web server (`dara server`), a filtered COD index (`cod_filtered_info_2024.json.gz`), ~60 real `.xrdml` scans, and auto-downloads BGMN for Linux/macOS/Windows. | A-Lab / Ceder group; 63★, 21 forks | **MIT**; last push 2026-07-31 | Chem. Mater. 38, 1364 (2026) | README + repo tree + abstract |
| **RADAR-PD** (ORNL: Yadav, Cheng, Doucet) | Mismatch-tolerant NN + "physics-constrained Rietveld verification"; X-ray and neutron; beats Dara on RRUFF reference-phase recovery | Research | not checked | 2026-05-12 | abstract-only |
| XMatcher, MatDiffract, PowderLine | Open-source XRD phase-ID frameworks | Research | not checked | 2026-07/08 | snippet-only |
| **Periodic Neon + Periodic Harness** | 1T-param model post-trained with RL on lab XRD; LLM-judge rewards; in-house structure DBs | Periodic labs; clients pay for software | Proprietary | 2026-09-15 | full |
| **Bruker DIFFRAC.EVA / TOPAS + CNN phase ID** (with KIT) | Commercial search/match + Rietveld. On iron-ore QC the CNN gets recall 90 / precision 76 vs Auto-EVA 63 / 100. Bruker frames AI as "complementary … not a replacement". | Industrial QC labs | Commercial licence | 2026 (©2026 app note) | full |
| Profex / BGMN | Free Rietveld GUI and kernel | Academia | Freeware | — | snippet-only |
| **MatterGen evaluation** (`microsoft/mattergen`) | `DisorderedStructureMatcher` decides whether an ordered prediction equals a known disordered structure (`OrderDisorderElementComparator`, radius/electronegativity thresholds). This is exactly Leeman's "error 3" check. | Generative-model novelty metrics | **MIT**; 1,852★; push 2026-08-27 | — | code read (`structure_matcher.py`) |
| pymatgen | StructureMatcher, CIF I/O, XRD simulation | Standard library | **MIT** (LICENSE file read); push 2026-10-20 | — | LICENSE + metadata |
| Disorder classifier (Jakob et al.) | Composition → P(disordered); ROC-AUC 0.96 | Research | Code on MPG GitLab (not verified) | 2025-10 | partial |
| Microsoft Discovery (GA 2026-06) | Enterprise agentic R&D platform; free local app with GitHub Copilot | Syensqo, Microsoft Quantum | Azure pricing | 2026-06-02 | full (news) |
| Claude Science | Workbench; 60+ databases; sub-agents; fact-checker; reproducible figures | Allen Institute, UCSF, Novo Nordisk | Included in Claude plans | 2026-06-30 | full (TechCrunch) |
| Kosmos (Edison) | Autonomous AI scientist with cited reports | Academia/biotech | $200/run at launch | 2025-11 | partial |
| Acceleration Consortium (U of T) | 7 SDL core facilities incl. "SDL for Inorganic Materials". >100 researchers, 50 SDLs at U of T, 30+ staff scientists, 90 partners. Builds open orchestration software and the El Agente agent. Stated aim: "increase trust in automated systems". | Toronto ecosystem | CFREF-funded | Impact report, FY 2025-26 | partial (pp. 1–10) |
| Orbital Industries (formerly Orbital Materials) | Orb MLIP; now sells AI-designed data-centre hardware; $50M Series B | — | Orb models open on GitHub | 2026-05-28 | snippet-only |

---

## 4. The gap

1. **Phase identification is being solved; novelty adjudication is not.** Dara/RADAR-PD answer "which known phases fit this pattern". Leeman's argument is a different question: is the evidence *better* explained by a new compound than by known ones, including disordered aristotypes? Leeman calls the alternative a "positive testing strategy" and rejects it. No tool I found takes (predicted CIF + measured pattern + recipe) and returns a falsification-first verdict. `[INFERENCE from the §3 table]`
2. **The disorder check exists only as an internal metric.** MatterGen's `DisorderedStructureMatcher` is buried in an evaluation module for generated samples. Jakob's classifier is a paper artefact. Neither is applied to *experimental* claims.
3. **Open reference data is incomplete.** MP "contains no compositionally disordered compounds" (Leeman §II). ICSD is paid (FIZ Karlsruhe). COD is CC0 and has disordered entries but is less complete. A free audit therefore misses some known phases, and that weakness is structural.
4. **Why nobody has filled it** `[INFERENCE]`: (a) labs with data (Periodic, A-Lab) solve it in-house for their own throughput, not as a neutral third party; (b) the market for "auditing other people's AI-materials claims" is reviewers, editors and investors, who do not buy tools; (c) it needs real crystallography judgment, so an automated verdict that is wrong is worse than none.

---

## 5. Candidate wedges

### W1. "Is it new?": a falsification-first audit of AI-proposed materials (best of three)

- **User:** the operator of an autonomous inorganic-synthesis line who must decide whether a hit is real before reporting it. Named targets: AC "SDL for Inorganic Materials" (U of T), A-Lab (LBNL), Meissner and FL01 (Toronto). Secondary users: referees of AI-materials papers. `[INFERENCE: no named person was found asking for this tool]`
- **Job:** input a predicted CIF (or MP id), a measured `.xy`/`.xrdml` and precursors. The tool then:
  - (1) pulls known phases in the chemical system from COD/MP;
  - (2) runs Dara to list alternative known-phase explanations with refinement quality;
  - (3) runs `DisorderedStructureMatcher` to test whether the "new" ordered structure is a known disordered phase;
  - (4) checks space-group drift between the predicted and refined structures (Leeman error 2);
  - (5) a Claude agent reasons over the precursors and conditions and writes a verdict: *Supported / Known phase / Known disordered variant / Inconclusive*, with every number linked to the code that produced it.
- **2-minute demo:** replay a Leeman case. Example: predicted ordered Mg₃NiO₄ is flagged as matching a rock-salt Mg/Ni solid solution, with a Vegard's-law check. Then a Dara `.xrdml` binary reaction shows the multi-hypothesis table. End on the Nature correction headline.
- **Reusable components:** Dara (MIT, 2026-07-31), pymatgen (MIT, 2026-10-20), MatterGen evaluation (MIT, 2026-08-27), mp-api (licence NOASSERTION via API; MP data CC-BY 4.0, snippet-only), COD (CC0, snippet-only).
- **Data/compute:** CPU only. BGMN runs on Linux in Docker (Render/Cloud Run). MP API key (free).
- **LLM cost:** ~5–15 calls per audit ≈ $0.3–2 on Sonnet-class pricing (`evolve-systems.md` per-call costs). Under $20 for the build. `[INFERENCE]`
- **Partner-prize fit:** Eon Era (agent testing and benchmarking): ship a 10-case benchmark from Leeman's 43 adjudications. SurrealDB: an audit ledger. Clerk: weak.
- **Main failure mode:** a wrong crystallographic call in front of judges or in public. Second: A-Lab's raw patterns may not be easy to fetch, which would leave the demo running on Dara's sample data rather than a famous case.

### W2. Claim ledger for AI-scientist reports

- **User:** Claude Science / Kosmos users before they publish.
- **Job:** split a report into statements, re-execute code-backed claims in a sandbox, verify citations against the primary text, and score synthesis claims (the 57.9% class).
- **Demo:** a Kosmos-style report goes in; a red/amber/green ledger comes out.
- **Reuse:** `Future-House/paper-qa` (Apache-2.0, push 2026-10-20).
- **Cost:** $1–5 per report. `[INFERENCE]`
- **Prize fit:** Eon Era (strong).
- **Fails because:** Claude Science and Edison already ship built-in checking. It is generic, not quantum, and indistinguishable from the diligence-agent space that was ruled out on 2026-10-21.

### W3. NV-magnetometer calibration copilot

- **User:** NV sensing teams (SBQuantum, university NV labs).
- **Job:** fit ODMR spectra, flag drift, propose recalibration.
- **Demo:** simulated ODMR → agent fit → drift alarm.
- **Reuse:** none verified.
- **Fails because:** no real data or user reachable by Oct 25, the users are defence-adjacent (dual-use), and the work is physics-fitting where the LLM adds little.

---

## 6. Scores: W1 ("Is it new?" materials audit)

| Criterion | Score | Why |
|---|---|---|
| Real user with evidence of pain | 3 | The pain is heavily documented (Nature correction 2026, Periodic 2026, Leeman 2024). No named user has asked for a *third-party* audit, and labs with volume build in-house. |
| AI makes a material difference | 3 | The core checks are deterministic (Rietveld, structure matching). The LLM adds chemical-context reasoning (Periodic: harness + reasoning = 3.8×) and the report, but is not the engine. |
| Severyn's unfair advantage | 2 | Verification ethos (Aquarium) and agent/report infrastructure (Maindframe) fit. He has no crystallography or solid-state synthesis track record, and Periodic has data plus a 1T model. |
| Buildable and demoable in 12 hours | 3 | All parts exist (Dara + BGMN + pymatgen + MatterGen matcher). Risks: BGMN in Docker, COD filtering, and finding one clean famous case with public raw data. |
| Judge appeal (Georgian investors) | 3 | "AI claimed 41 new materials; Nature corrected it; we catch it automatically" is crisp. But it is a science-tooling niche for a B2B growth fund. |
| Adoption path after Oct 25 | 2 | Open-source release to the SDL community (AC, A-Lab) is plausible but there is no buyer. Dara is free and already the default. |
| Competition density (5 = open field) | 3 | Phase ID is crowded (Dara, RADAR-PD, Bruker, Periodic). The specific falsification-first novelty verdict is open. |
| Credibility gain in AI and quantum | 2 | Builds AI-for-science credibility. Quantum only by adjacency (superconductors and magnets for quantum hardware). |
| Risk (5 = low: no dual use, no 1QBit overlap) | 5 | No TopQAD overlap and no dual-use. The residual risk is reputational (a wrong verdict), not legal. |
| **Total** | **26/45** | |

---

## 7. Sources

| # | Source | URL | Date | Read depth |
|---|---|---|---|---|
| 1 | Leeman, Liu, Stiles, Lee, Bhatt, Schoop, Palgrave, "Challenges in High-Throughput Inorganic Materials Prediction and Autonomous Synthesis", PRX Energy 3, 011002 | https://par.nsf.gov/servlets/purl/10532478 | 2024-03-07 `[STALE]` | partial (abstract, §I–III, §IV.A–D) |
| 2 | Szymanski et al., Author Correction, Nature 650, E1 | https://www.nature.com/articles/s41586-025-09992-y | 2026-01-19 | full |
| 3 | Periodic Labs, "Nature Is Our Learning Environment" | https://periodic.com/news/nature-is-our-learning-environment | 2026-09-15 | full |
| 4 | The Logic (Hemmadi), "AI could help invent new materials. First, firms must figure out how to make them" | https://thelogic.co/news/artificial-intelligence-materials-science/ | 2026-10-07 | full |
| 5 | Jakob, Walsh, Reuter, Margraf, "Learning Crystallographic Disorder", Adv. Mater. 38, e14226 | https://pmc.ncbi.nlm.nih.gov/articles/PMC12822528 | 2025-10-23 | partial (abstract, §1–3, Methods) |
| 6 | Nguyen et al., arXiv 2606.30967 | https://arxiv.org/abs/2606.30967 | 2026-06-29 | abstract-only |
| 7 | Cheetham & Seshadri, Chem. Mater. 36, 3490 | https://pubs.acs.org/doi/abs/10.1021/acs.chemmater.4c00643 | 2024-04 `[STALE]` | snippet-only |
| 8 | Fei, McDermott, Rom, Wang, Ceder, Dara, arXiv 2510.19667 / Chem. Mater. 38, 1364 | https://arxiv.org/abs/2510.19667 | 2025-10-22 / 2026 | abstract-only |
| 9 | Dara repo (README, tree, licence, push date via GitHub API) | https://github.com/CederGroupHub/dara | push 2026-07-31 | README + tree |
| 10 | Yadav, Cheng, Doucet, RADAR-PD, arXiv 2605.12478 | https://arxiv.org/abs/2605.12478 | 2026-05-12 | abstract-only |
| 11 | Bruker AXS / KIT, App Note 633, "AI-Assisted Phase Identification from Powder XRD Data" | https://www.bruker.com/en/products-and-solutions/diffractometers-and-x-ray-microscopes/x-ray-diffractometers/diffrac-suite-software/diffrac-eva.html | 2026 | full |
| 12 | MatterGen `structure_matcher.py`; repo metadata | https://github.com/microsoft/mattergen | push 2026-08-27 | code (class definition and `fit` docstring) |
| 13 | pymatgen LICENSE; repo metadata | https://github.com/materialsproject/pymatgen | push 2026-10-20 | LICENSE file |
| 14 | Mitchener et al., Kosmos, arXiv 2511.02824 | https://arxiv.org/html/2511.02824 | 2025-11 | partial (abstract, §1 results, Fig. 1) |
| 15 | Edison Scientific, "Kosmos: An AI Scientist for Autonomous Discovery" (pricing) | https://edisonscientific.com/news/announcing-kosmos | 2025-11-05 | partial (pricing and accuracy paragraphs) |
| 16 | TechCrunch (Bellan), "Anthropic's Claude Science bets on workflow…" | https://techcrunch.com/2026/06/30/anthropics-claude-science-bets-on-workflow-not-a-new-model-to-win-over-scientists | 2026-06-30 | full |
| 17 | Anthropic, Life Sciences Verification Program (model access for vetted biologists; not result verification) | https://www.anthropic.com/news/life-sciences-verification-program | 2026-09-17 | snippet-only |
| 18 | Microsoft Source, "Introducing Majorana 2" | https://news.microsoft.com/source/features/innovation/majorana-2-microsoft-discovery-agentic-ai/ | 2026-06-02 | full |
| 19 | Quantum Computing Report, SBQuantum $4M seed | https://quantumcomputingreport.com/sbquantum-secures-4m-seed-round-and-appoints-new-ceo-to-scale-us-operations/ | 2026-04-16 | full |
| 20 | Daniel et al., NV sim-to-real calibration, arXiv 2608.19582 | https://arxiv.org/abs/2608.19582 | 2026-08-20 | abstract-only |
| 21 | quantumintel.tech, Qruise NV calibration | https://quantumintel.tech/news/qruise-automates-nv-center-qpu-calibration-goethe-university/ | 2026-05-02 | full (low-trust aggregator) |
| 22 | Acceleration Consortium Impact Report FY2025-26 | https://cdn.prod.website-files.com/6935f8052c49ab4956e4b162/6aa1bf22cb7b7ab77b086625_ac_impactreport2026_web_FINAL.pdf | 2026 (covers to 2026-03-31) | partial (pp. 1–10) |
| 23 | Orbital Industries Series B (TNW / Techmeme) | https://thenextweb.com/news/orbital-industries-50m-series-b-data-center-cooling | 2026-05-28 | snippet-only |
| 24 | COD licence (CC0) | https://cod.psdi.ac.uk/ | — | snippet-only |
| 25 | Materials Project data licence (CC-BY 4.0) | https://next-gen.materialsproject.org/api | — | snippet-only |
| 26 | `Future-House/paper-qa` metadata (Apache-2.0) | https://github.com/Future-House/paper-qa | push 2026-10-20 | metadata only |

---

## 8. Open questions

1. **Does Severyn want a materials project at all?** W1's quantum credibility is adjacency only. If (2) "credibility in AI and quantum" must carry quantum, drop this ticket's wedges.
2. **Can a famous A-Lab pattern be obtained in raw form within an hour?** The A-Lab Supplementary Data and Leeman's refinements are the obvious source; not verified this session. If not, the demo runs on Dara's sample scans and loses its hook.
3. **Is there a reachable user before Oct 25?** Candidates: a staff scientist at AC's SDL for Inorganic Materials, Meissner (CEO Olivia Leng), or Robert Palgrave (who publicly critiques AI-materials claims). One reply asking "would you run this on your next claimed hit?" would raise the user score from 3 to 4.
4. **Is COD coverage enough?** How many of Leeman's 43 "known phase" counter-examples exist in COD (CC0) rather than only in ICSD (paid)? This sets the false-negative rate of a free audit.
5. **For the synthesis memo:** Periodic's numbers (human experts agree 77.2% of the time; LLM judge 74.6%) are a clean, citable benchmark for "verification without ground truth". It may strengthen the pitch of whichever quantum-verification wedge is chosen, even though this ticket's wedge is not the pick.
