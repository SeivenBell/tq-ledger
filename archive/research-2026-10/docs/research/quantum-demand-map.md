# Quantum demand map 2026: where the money goes and what programs ask for

Ticket #10. Research date: 2026-10-22. Read-depth labels: **full**, **partial (sections …)**, **snippet-only**. Lines marked `[INFERENCE]` are my analysis, not a source's claim. "Secondary" means a journalist's or analyst's report on a primary document I could not open.

---

## 1. Bottom line

- **Most of the money is going to hardware, factories and evaluation, not to software.** US Commerce CHIPS letters of intent total $2.013B for foundries and hardware bottlenecks (2026-05-21). DARPA QBI Stage C is worth up to $300M per performer. DOE's Q Competition offers up to $215M for machines with ≥100 logical qubits. Canada's CQCP Phase 1 gives up to CAD $92M to four hardware companies. The large 2026 private rounds were also hardware: Photonic $200M, QuantWare $178M, Quantum Motion $160M. Software rounds are small; Algorithmiq raised €18M.
- **The software money that does exist pays for verification.** DARPA's QBI IV&V topic is open until **2026-12-30**, and its FAQ sends "applications and algorithms"-only entities to it. DOE's new **$45M V&V Testbed (LAB 26-3603)** must cover "quantum algorithm and applications" and "resource estimation", must include ≥2 outside collaborators, and must aim for an "open standard". Proposals are due **2026-11-10**. NRC Canada is building "Benchmarking Quantum Platforms" for ISED. Verification is the paid-for demand, and it lines up with Severyn's theme.
- **DOE states the application gap in plain words.** Its *Quantum Genesis Priority Applications* document (PDF dated 2026-10-08) says that progress "will require a clear understanding of resource estimation". It names these as the gaps to close: "moving beyond algorithm design into concrete resource estimates" and noting where "current estimates … place it out of reach for the first generation of SRQCs". This is the freshest primary statement of a software need I found.
- **The PQC deadlines are the only deadline-driven demand that reaches companies of every size.** EO 14412 sets 2030 and 2031 deadlines and orders a FAR rule that will bind contractors. Canada's GC roadmap requires high-priority systems to finish by 2031. But `pqc-migration.md` already covers this field, which is crowded and earns little quantum credibility. I do not repeat it here.
- **Best wedge from this map: the "SRQC Readiness Map".** It is an LLM-built, quote-verified dataset that matches each DOE priority-application target to the best published logical resource estimate, and checks each estimate against the Q Competition tiers (100, 150 and 200 logical qubits; "hundreds of millions" of fault-tolerant operations). **Score: 32/45.** The real-user evidence comes from program documents, not from any named person, so treat it as a strong #2. It can also be a second view on the same claim-card engine proposed in `resource-claims-verification.md`.
- **Verdict:** yes, there is a credible project here, but no buyer will sign by Oct 25. The pitch to investors is "the money is going to referees". The adoption path runs through LAB 26-3603 teams, Q Competition entrants and open-source contributors, not through paying customers.

---

## 2. The pain

### 2.1 Money map, 2025–2026 (Canada and US first)

| Program / source | Money and date | What it buys | What it asks for in software, verification or tooling | Read depth |
|---|---|---|---|---|
| **DARPA QBI** (program page as of 2026-10-08; Stage C news 2026-10-07) | Stage A ≤$1M, B ≤$15M, C ≤$300M per performer. Stage C: Atom Computing, Diraq, IBM, IonQ, plus Microsoft and PsiQuantum. Stage B: Nord Quantique, Photonic, Quantinuum, Quantum Motion, QuEra, SQC, Xanadu. Stage A: Google, Quandela | Independent verification of each path to utility scale by 2033 | Stage C, in the words of MD Micah Stoutimore: "determine whether the technology performs the way the models and roadmaps say it should". **IV&V topic DARPA-PA-26-02-01** invites "infrastructure, equipment, and expertise" for IV&V and is open until 2026-12-30 | full |
| QBI 2026 FAQ (PDF hosted 2026-03; header says "March 24, 2025", likely a typo because it cites PA-26-02-02) | — | — | Q10: entities working "only on applications and algorithms" should join a performer team or apply to the IV&V topic. Q14: "computational value will be measured in dollars". Q11: IV&V awardees may face organisational-conflict-of-interest (OCI) exclusion from performer roles | full |
| PsiQuantum expanded QBI Stage C (2026-07-22) | $125M | Audit of architecture, fabrication and cryogenics | Includes "live checks of fault-tolerant algorithm resource estimates on Construct" | full (secondary: postquantum.com citing QCR) |
| **DOE Quantum Genesis Q Competition** (2026-09-17) | Up to $215M. Phase I ≤$1.5M per awardee. Phase II: a $100M pool for ≥100 logical qubits, plus $50M bonuses each at 150 and 200 logical qubits. Only $2.5M is FY26 money. Applications closed 2026-10-19 | Machines with "at least 100 logical qubits … hundreds of millions fault-tolerant operations" plus "scientific demonstration programs" | Payouts depend on verified performance against science targets | full |
| **DOE LAB 26-3603 V&V Testbed** (2026) | $45M ($14M FY26); 1–2 awards of $7–15M/yr over 3 years; national labs only as lead | Verification of fault-tolerant QCs "from hardware to applications" | Must address "resource estimation" and "quantum algorithm and applications". Verification of algorithms is defined as "examining designs and codes for correctness and consistency … without necessarily executing". Needs ≥2 external collaborators, "open standard", reproducible by outsiders. LOI was due 2026-09-30; proposals due 2026-11-10 | partial (exec. summary, §III.A purpose, V&V definitions, teaming, out-of-scope) |
| **DOE Quantum Genesis Priority Applications** (PDF 2026-10-08) | — | Defines "scientific relevance" for the Q Competition | Chemistry (reaction mechanisms, dynamics), materials (Fermi-Hubbard, Kitaev spin liquid), subatomic physics, applied maths (linear systems/PDEs). Gaps named: "concrete resource estimates", estimates that "place it out of reach", "benchmarking against the best-known classical alternatives" | partial (intro, structure, domains 1, 2 and 4, emerging areas) |
| **EO 14413** + summit (2026-06-22; summit 2026-07-07) | QC-ADDS: DOE to deliver a scientific QC; 2028 target | — | Industry-flagged gaps at the summit: "algorithms remain ahead of hardware" (too few algorithms worth a 2028 machine); "no shared framework for certifying quantum results" | EO: snippet-only (Federal Register blocked); summit: full (secondary, postquantum.com) |
| **US Commerce CHIPS** (2026-05-21) | $2.013B LOIs: IBM Anderon foundry $1B, GlobalFoundries $375M, $100M each to Atom, D-Wave, Infleqtion, PsiQuantum, Quantinuum and Rigetti (Rigetti "up to"), Diraq up to $38M. Government takes equity | Fabs, readout, cryo, photonics | None for software | full |
| **EO 14412 PQC** (2026-06-22) | Unfunded mandate, "subject to the availability of appropriations" | Migration | HVAs and high-impact systems: PQC key establishment by 2030-12-31, signatures by 2031-12-31. FAR proposed rule within 180 days. CISA cryptographic bill of materials (CBOM) minimum elements within 270 days. "Shared procurement of PQC tools" | full |
| **Canada CQCP Phase 1** (2025-12-15) | Up to CAD $92M (≤$23M each to Anyon, Nord Quantique, Photonic, Xanadu), part of CAD $334.3M over 5 years (Budget 2025) | Fault-tolerant hardware, "milestone-based funding and independent benchmarking" | NRC "Benchmarking Quantum Platform" gives "expert, independent assessment". Later-phase details "will be released" | full (TQI report of ISED release) |
| **NRC under the Defence Industrial Strategy** (2026-03-09 and 03-19) | >$900M total NRC; >$161M over 5 years for quantum in defence; IRAP DI Assist $241M for SMEs | Sensing, internetworking, quantum-safe | **Benchmarking Quantum Platforms** (for ISED assessments); **Measurement Science for Quantum Technologies** (standards, NATO interoperability); **Quantum Safe Technologies Initiative** ("using classical and quantum computing to analyze cryptographic algorithms") | full |
| **Canada GC PQC roadmap ITSM.40.001** (2025-06-23) | Departments fund migration from IT lifecycle budgets | Migration | Departmental plan by April 2026, annual reporting, high-priority systems by end-2031. "Software tools and services will be necessary to complete cryptographic discovery" | full |
| **Private capital** | QED-C: 2025 VC $4.9B (+192%), US $2.7B; 2025 new government commitments $12.7B. Crunchbase: 2025 $4.1B; 2026 YTD $1.2B as of 2026-05-18, "on track to … decline". McKinsey: $12.6B total 2025 investment including public markets, ~60% in the top 10 deals | Mostly hardware and late stage | McKinsey: 33% of analysed corporates spend >$10M/yr on quantum, 7% >$50M | QED-C: full (secondary); Crunchbase: full; McKinsey: full (secondary, postquantum.com; primary PDF timed out) |

### 2.2 Who has the pain (named roles)

- **QBI government evaluation team** (MD Micah Stoutimore). They must check performers' models and roadmaps, including algorithm resource estimates (PsiQuantum/Construct), and price utility in dollars. Today they work through T&E and IV&V contractors under NDA.
- **DOE ASCR** (LAB 26-3603 contact: Dr. Marco Fornari) and **the national-lab V&V teams** forming now. They must build an "open standard" evaluation framework that covers applications and resource estimation, and they must bring in outside collaborators.
- **Q Competition entrants** (private companies). They must run "scientific demonstration programs" that DOE will judge against the priority applications.
- **NRC Benchmarking Quantum Platforms staff and ISED**. They assess the CQCP firms, which include Photonic, Nord Quantique and Xanadu, all also in QBI Stage B.
- **Algorithm researchers.** DOE says the field must move "beyond algorithm design into concrete resource estimates".

**What they do today:** hand-made literature reviews. One example is NERSC's 2025-09-11 report (arXiv 2509.09882), which matched use cases to resource requirements and vendor roadmaps by hand. Another is analyst prose such as postquantum.com's *Quantum Utility Ladder*. Its author warns that a 2013 glycine estimate "is not directly comparable to the Toffoli counts from modern qubitization work".

**What it costs:** DOE is spending $45M on V&V and $215M on outcomes that depend on it. I found no number for the cost of mismatched estimates themselves `[INFERENCE: that cost shows up as wrong target selection and slow reviews]`.

### 2.3 Disconfirming evidence

- **Buyers are closed.** LAB 26-3603 lets only national labs lead. QBI IV&V work happens under NDA, with OCI rules that can bar IV&V awardees from performer roles. A solo builder cannot sell to either by Oct 25 (see also `resource-claims-verification.md`).
- **The money may be thinner than the headline.** Only $2.5M of the $215M Q Competition and $14M of the $45M testbed are FY26 money; the rest is "contingent on congressional appropriations". NRC must cut $95M in 2026–27, rising to $190M by 2028–29, and reduce grants and contributions (NRC 2026–27 Departmental Plan).
- **Private investment is cooling and concentrating.** Crunchbase reports that 2026 is on track below 2025. QED-C notes new pure-play foundings fell from 83 (2021) to 23 (2025).
- **The earlier sibling report found no pull for a general subroutine registry** (`uncompute` 3★; no verification requests in Bartiq's issues). My wedge is application-level and tied to a funded program, but it carries the same risk: nobody may come.

---

## 3. Existing solutions

| Product / project | What it does | Who uses it | Price / licence; last activity | Read depth |
|---|---|---|---|---|
| Quantum Advantage Tracker (IBM, Algorithmiq, Flatiron) | Open leaderboard of near-term advantage claims and classical challenges | IBM, Quantinuum users, Flatiron, LANL, BlueQubit | Apache-2.0; 126★; pushed 2026-10-22 | partial (README, GitHub metadata) |
| LANL `qc-applications` (DARPA QB) | Builds Clifford+T circuits and estimates for 5 science applications; schema includes `value` in USD and `value_per_t_gate` | DARPA QB performers | BSD-3; last commit 2025-07-21 | partial (README, License.md) |
| Qualtran (Google) | Bloq-based fault-tolerant algorithm cost analysis (T, Toffoli, qubits) | Google QAI, academics | Apache-2.0; 403★; pushed 2026-10-22 | metadata only (README not read this session) |
| pyLIQTR (MIT Lincoln Lab) | Hamiltonian-simulation circuits and estimates | DARPA QB | MIT; last commit 2026-01-05 | metadata only |
| BenchQ (Zapata) | Resource-estimation pipelines | DARPA QB | Apache-2.0; pushed 2025-03-06 (possibly stale; Zapata wound down in 2024, not re-verified) | metadata only |
| Microsoft QDK resource estimator | Logical to physical estimates | Microsoft, Photonic | MIT; pushed 2026-10-22 | metadata only |
| Bartiq (PsiQuantum) | Symbolic resource aggregation | PsiQuantum | Apache-2.0; pushed 2026-10-14 | metadata only |
| NERSC capability assessment (arXiv 2509.09882) | One-off literature review of resource requirements vs 10 vendor roadmaps; proposes the SQSP metric | DOE/NERSC | Paper, 2025-09-11 | snippet-only (abstract) |
| postquantum.com Quantum Utility Ladder (2026) | Prose "rungs" from 25–100 logical qubits upward | Analysts, CISOs | Free blog | partial (intro, Rung 1) |
| 1QBit TopQAD | Physical-layer QRE and architecture design | Commercial | Commercial | from `field-needs.md` |

---

## 4. The gap

1. **No live, machine-readable map from DOE's priority-application targets to resource estimates.** The DOE document lists example targets without numbers and calls the missing estimates a gap. NERSC's review is a static PDF. postquantum.com's ladder is prose that mixes cost models. LANL's QCA covers 5 applications and has not been updated since 2025-07 `[INFERENCE from what I read]`.
2. **No normalisation layer.** Estimates come as T-count, Toffoli, "logical operations", qubitization calls, or active volume, each with a different precision target and failure budget. The Q Competition bar is "hundreds of millions fault-tolerant operations", and nobody publishes the conversion from each paper's numbers to that bar.
3. **No provenance check.** Analyst tables quote numbers without pointing to the page or table they came from.

**Why nobody has filled it** `[INFERENCE]`: the people who need it are labs and program offices that do the work in-house and by hand. The DOE target list is two weeks old (2026-10-08). The work is tedious curation without a direct revenue model, which is exactly where LLM extraction plus deterministic checking makes it cheap.

---

## 5. Candidate wedges

### W1 (best): SRQC Readiness Map

- **User:** (a) national-lab and external-collaborator teams writing LAB 26-3603 proposals, due 2026-11-10, who need an application-layer benchmark list; (b) Q Competition entrants choosing demonstration programs; (c) algorithm researchers deciding what to cost next; (d) investors reading hardware roadmaps, which includes the Georgian judges.
- **Job:** For each DOE priority-application example target, show the best published end-to-end logical estimate: logical qubits; T or Toffoli count; precision and failure budget; cost model; verbatim quote with page or table anchor. Normalise to "fault-tolerant operations" with the conversion shown. Give a verdict against each Q Competition tier (100, 150 and 200 logical qubits; 10⁸ to 10⁹ operations). Mark empty cells as "no estimate exists", which is DOE's own named gap.
- **2-minute demo:** (1) A matrix of DOE applications × machine tiers, green/amber/red, each cell linked to its claim card. (2) Click "2D Fermi-Hubbard ground state". The card shows Campbell 2020/22, "around one million Toffoli gates" (abstract), with the quote highlighted. (3) Paste a new arXiv ID. The agent extracts the numbers; a deterministic checker confirms that the quote appears verbatim in the PDF text and recomputes the unit conversion; the matrix updates. (4) An evaluation panel shows extraction precision/recall against a 15-paper hand-labelled gold set. This is Severyn's Aquarium style, and it fits the Eon Era prize.
- **Reusable components (verified):** LANL `qc-applications` (BSD-3) for the schema and seed estimates; Qualtran (Apache-2.0) to recompute one target, for credibility; arXiv API; `pdftotext`. Optional: Quantum Advantage Tracker (Apache-2.0) for the near-term column.
- **Data and compute:** the DOE QGPA PDF plus ~30–40 arXiv papers; CPU only.
- **LLM cost:** ~2–4M tokens for extraction plus verification, roughly $10–40 at Sonnet-class list prices `[INFERENCE: prices not re-verified this session]`. This fits within the pending $100 Anthropic credit.
- **Partner prizes:** Eon Era (an agent evaluated on a gold set); SurrealDB Agent Memory (a graph of claims, papers, assumptions and targets); Clerk (auth for curator submissions); Render for hosting.
- **Main way it fails:** normalising across cost models is truly ambiguous. One wrong conversion shown to experts destroys credibility. Mitigation: show the raw number and the conversion side by side, and flag rather than force comparisons. Second risk: no user adopts it, because DOE labs do this in-house.
- **1QBit overlap:** low to medium. Stay at the logical level. Never compute physical qubits, runtime, factories or $/qubit-second, which are TopQAD territory.

### W2: Advantage-claim docket

- **User:** investors, analysts and journalists who track "quantum advantage" headlines.
- **Job:** for each claim, a timeline of the claim and the classical responses (for example, IBM's 2026-07-30 logical-circuit claim, answered by a reported 37.3-minute GPU reproduction; Q-CTRL's Hubbard run, answered by Algorithmiq and Multiverse), with a status label.
- **Demo:** a claim feed, a docket page, and the agent drafting a docket from a new preprint.
- **Components:** Quantum Advantage Tracker (Apache-2.0); arXiv API.
- **LLM cost:** <$20 `[INFERENCE]`.
- **Prize fit:** SurrealDB.
- **Fails because:** the tracker already does this with domain-expert reviewers and is active today. Much of the evidence is near-term, not fault-tolerant, so it adds little to Severyn's FTQC credibility. Scores ~25/45 `[INFERENCE]`.

### W3: PQC plan starter (defer to `pqc-migration.md`)

- **User:** Canadian GC departments (annual reporting since April 2026) and US federal contractors (FAR rule pending).
- **Job:** produce a CBOM from a repository with cbomkit (Apache-2.0, pushed 2026-10-13) and draft a migration plan mapped to the ITSM.40.001 and EO 14412 milestones.
- **Fails because:** the field is crowded (IBM/cbomkit, SandboxAQ, Keyfactor, PQShield), discovery is not the bottleneck (per the sibling report), and it earns little quantum credibility.

---

## 6. Scores (W1, SRQC Readiness Map)

| Criterion | Score | Why |
|---|---|---|
| Real user with evidence of pain | 3 | Primary, dated program text names the need (DOE QGPA gaps; LAB 26-3603 requires resource estimation and an open standard; QBI audits estimates), but no individual user has confirmed they would use it. |
| AI makes a material difference | 4 | Extracting and normalising numbers from 30–100 heterogeneous papers is the core job, and NERSC did it by hand. Deterministic quote and arithmetic checks keep the LLM honest. |
| Severyn's unfair advantage | 4 | MSc in quantum information, a QRE demo shipped at 1QBit, reproducible-report agents at Maindframe, and Aquarium's claim testing. |
| Buildable and demoable in 12 hours | 4 | A static seed set, one extraction agent, a checker and a matrix UI. The risk is curating 30 papers well in the time. |
| Judge appeal (Georgian investors) | 3 | "$260M of DOE money hinges on verified science targets; we map which targets each machine unlocks" is clear. The buyer is government and the market is niche for B2B growth equity. |
| Adoption path after Oct 25 | 3 | Open dataset plus pull requests; direct outreach to LAB 26-3603 teams before Nov 10 and to Q Competition entrants. No paying buyer. |
| Competition density (5 = open field) | 3 | NERSC review, postquantum ladder, LANL QCA and Qualtran exist; none is a live, quote-verified map keyed to the DOE targets `[INFERENCE]`. |
| Credibility gain in AI and quantum | 4 | Puts Severyn's name on the open application-readiness layer at a moment DOE has just defined. Clearly fault-tolerant quantum, clearly AI. |
| Risk (5 = low: no dual use, no 1QBit overlap) | 4 | Science applications, no cryptanalysis; logical level only. Some perceived adjacency to TopQAD QRE remains. |
| **Total** | **32/45** | |

---

## 7. Sources

| Source | Date | Read depth |
|---|---|---|
| DARPA, "Four more teams enter QBI's final stage" https://www.darpa.mil/news/2026/four-more-teams-enter-quantum-benchmarking-initiative-final-stage | 2026-10-07 | full |
| DARPA QBI program page https://www.darpa.mil/research/programs/quantum-benchmarking-initiative | current as of 2026-10-08 | full |
| DARPA QBI IV&V topic page https://www.darpa.mil/work-with-us/opportunities/darpa-pa-26-02-01 | published 2025-11-17 | full (page is a stub; SAM.gov body not read) |
| DARPA QBI Stage A FAQ https://www.darpa.mil/sites/default/files/attachment/2026-03/darpa-qbi-q-a-2026.pdf | hosted 2026-03 (header says 2025-03-24) | full |
| DARPA, "QBI expands quest…" https://www.darpa.mil/news/2026/qbi-stage-a-qbit | 2026-03-10 | full |
| DARPA QB program (preprints, open-source list) https://www.darpa.mil/research/programs/quantum-benchmarking | preprints 2024, **>18 months, possibly stale**; program complete | full |
| postquantum.com, "PsiQuantum's $125M DARPA deal buys verification" https://postquantum.com/industry-news/psiquantum-darpa-qbi-stage-c/ | 2026-07-23 | full (secondary) |
| DOE, Quantum Genesis Q Competition and V&V lab call https://www.energy.gov/science/articles/doe-launches-competition-accelerate-development-worlds-first-fault-tolerant | 2026-09-17 | full |
| DOE LAB 26-3603 announcement https://science.osti.gov/-/media/grants/pdf/lab-announcements/2026/LAB-26-3603.pdf | 2026 (LOI 2026-09-30; proposals 2026-11-10) | partial (exec. summary, eligibility, §III.A, V&V definitions, teaming) |
| DOE, Quantum Genesis Priority Applications https://www.energy.gov/documents/quantum-genesis-priority-applications | PDF created 2026-10-08 | partial (intro, structure, domains 1, 2, 4, emerging areas) |
| DOE Quantum Genesis page https://www.energy.gov/undersecretaryforscience/genesis-mission/quantum-genesis | 2026-10-06, modified 10-09 | full |
| White House, EO 14412 https://www.whitehouse.gov/presidential-actions/2026/06/securing-the-nation-against-advanced-cryptographic-attacks/ | 2026-06-22 | full |
| EO 14413 (Federal Register blocked automated access) https://www.federalregister.gov/documents/2026/06/25/2026-12910/ushering-in-the-next-frontier-of-quantum-innovation | 2026-06-25 | snippet-only |
| postquantum.com, White House Quantum Summit https://postquantum.com/industry-news/white-house-quantum-summit-july-2026/ | 2026-07-14 | full (secondary) |
| NIST/Commerce CHIPS quantum LOIs https://www.nist.gov/news-events/news/2026/05/department-commerce-announces-letters-intent-9-companies-2-billion | 2026-05-21 | full |
| postquantum.com, CHIPS $2B analysis https://postquantum.com/industry-news/chips-act-2-billion-quantum-investment/ | 2026-05-22 | full (secondary) |
| TQI, CQCP Phase 1 https://thequantuminsider.com/2025/12/15/canadian-government-backs-four-companies-in-push-to-back-domestic-quantum-computer-developers | 2025-12-15 | full |
| ISED, DIS quantum, Waterloo https://www.canada.ca/en/innovation-science-economic-development/news/2026/03/canada-advances-defence-industrial-strategy-to-strengthen-security-sovereignty-and-prosperity0.html | 2026-03-19 | full |
| NRC backgrounder, new DIS programs https://www.canada.ca/en/national-research-council/news/2026/03/new-programs-to-support-canadas-defence-industrial-strategy.html | 2026-03-09 | full |
| NRC 2026–27 Departmental Plan https://nrc.canada.ca/en/corporate/planning-reporting/national-research-council-canadas-2026-27-departmental-plan | 2026-03-13, modified 08-06 | partial (at a glance, highlights, minister/president, DR1 intro) |
| ITA, Canada quantum technology https://www.trade.gov/market-intelligence/canada-quantum-technology | 2026-08-11 | full |
| CCCS ITSM.40.001 PQC roadmap https://www.cyber.gc.ca/sites/default/files/itsm.40.001-e.pdf | 2025-06-23 | full |
| postquantum.com on McKinsey QTM 2026 https://postquantum.com/industry-news/mckinsey-quantum-monitor-2026 | 2026-04-20, updated 07-16 | full (secondary; McKinsey PDF timed out) |
| postquantum.com on QED-C 2026 https://postquantum.com/industry-news/qed-c-quantum-industry-2026-report/ | 2026-04-20 | full (secondary) |
| Crunchbase, quantum sector snapshot https://news.crunchbase.com/venture/quantum-computing-startup-investment-data-quantinuum-ipo/ | 2026-05-18 | full |
| EU-Startups, Algorithmiq €18M https://www.eu-startups.com/2026/05/quantum-software-startup-algorithmiq-raises-e18-million-and-moves-global-hq-from-helsinki-to-milan/ | 2026-05 | snippet-only |
| arXiv 2509.09882 (NERSC) https://arxiv.org/abs/2509.09882 | 2025-09-11 | snippet-only (abstract) |
| arXiv 2012.09238 (Campbell, Hubbard) https://arxiv.org/abs/2012.09238 | 2020-12-16, **stale; used only as demo example** | snippet-only (abstract) |
| postquantum.com Quantum Utility Ladder https://postquantum.com/quantum-utility-map/quantum-utility-ladder-fault-tolerant-algorithms/ | 2026 | partial (intro, Rung 1) |
| GitHub API metadata and READMEs: quantum-advantage-tracker, lanl-ansi/qc-applications, quantumlib/Qualtran, isi-usc-edu/pyLIQTR, zapatacomputing/benchq, microsoft/qdk, PsiQ/bartiq, cbomkit/cbomkit | fetched 2026-10-22 | partial (licence, last push/commit; READMEs for tracker and QCA) |
| IBM advantage claim and 37.3-minute reply; Q-CTRL vs Algorithmiq/Multiverse | 2026-07 to 09 | snippet-only / secondary in the Ladder page (W2 colour only) |

---

## 8. Open questions

1. **Combine W1 with `resource-claims-verification.md`'s crypto ledger?** The same claim-card engine (extract → quote check → arithmetic check → comparable/not) could serve both views. Crypto has the louder user community; the DOE view has the funded program story and lower dual-use risk. The synthesis step should decide whether to show crypto at all on stage.
2. **Can Severyn reach one LAB 26-3603 team (ORNL, LBNL/NERSC, Sandia, LANL, ANL…) before Oct 25** to get a "we'd use this" quote? Proposals are due Nov 10, so they are looking for external collaborators now. Could Maindframe act as the collaborator entity?
3. **Will Severyn himself pursue the QBI IV&V topic (deadline 2026-12-30) or a LAB 26-3603 subaward?** Either could create an OCI or employer conflict, given 1QBit's earlier QBI consortium role. Raise it with 1QBit.
4. **Normalisation policy:** which single unit does the map adopt (Toffoli-equivalent? "fault-tolerant operations" as DOE uses the term?), and does DOE's RFA define "fault-tolerant operation"? I have not read the RFA body.
5. **Is CQCP Phase 2 or the NRC Benchmarking Quantum Platforms team procuring outside tools?** I found no public call. Worth one email to NRC.
