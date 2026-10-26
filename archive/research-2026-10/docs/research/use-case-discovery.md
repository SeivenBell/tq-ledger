# Where enterprise quantum adoption stalls, and can AI pick real use cases?

Ticket #7, slug `use-case-discovery`. Research date: 2026-10-22. Read-depth labels: **full**, **partial (sections …)**, **abstract-only**, **snippet-only**. "Secondary" means I read a full analyst or journalist report about a primary source that I could not open. Lines marked `[INFERENCE]` are my own analysis. Sources older than 18 months (before 2025-04-22) are flagged **stale?**.

---

## 1. Bottom line

- **Yes, but only as a mid-ranked option (30/45).** Adoption stalls at one documented step: matching a business problem to a quantum speedup that survives the best classical methods. Google Quantum AI calls this step (its "Stage III") "perhaps the most significant bottleneck in delivering value". It also says this is the step generative AI is suited to: "the agent's task would not be to invent, but to recognize". I found no public, free tool that does this job and answers "not yet" honestly.
- **Demand is real and enterprises pay for it.** BCG puts 2025 enterprise quantum spend at about $550M. More than 60% of surveyed enterprises spend over $1M a year, yet "concrete applications … remain scarce". OECD surveys find "unclear business value" is a top-three barrier. One older survey found 73% of financial firms had not identified any application. **Zapata Quantum launched exactly this product on 2026-09-22 (Quantum Pilot).** That launch validates the job and closes the enterprise lane.
- **The honest answer is usually "not yet", and the evidence base for saying so exists.** Google's Tables 2–4 (CC BY 4.0) list every super-quadratic application with a published resource estimate. Outside simulation and cryptanalysis, most rows have Stage III application "Unknown". DQI's exponential speedup is on OPI, a problem with no known real-world use. On max-XORSAT, a tailored classical solver beats DQI. On the IBM-backed Quantum Advantage Tracker, 33 of 52 submissions are classical-only results that test or push back on quantum claims.
- **Best wedge: "Not Yet", a triage agent for use-case claims with every claim tied to a citation.** The user types a plain-language problem. The agent maps it to a quantum primitive, assigns a Google stage, shows the nearest published resource estimate and compares that with vendor roadmaps, and shows the strongest classical counter-evidence. It ships with a calibration benchmark of labelled cases showing how often raw LLMs overclaim. Quantum-Audit (2026-02) found models accept false quantum premises, scoring below 66% on them.
- **Main weakness: no named person will use it next week.** The people with budget hire consultants or Zapata. The people who would use a free tool (innovation analysts, domain scientists, students) are spread out. Choose it over the peer claim-ledger or SRQC-map wedges (32/45 each) only if Severyn can get two or three named "I'd try it" replies before Saturday.
- **It can converge with peers.** "Not Yet" could be the enterprise-facing front end on the same evidence-card dataset that `quantum-demand-map.md` (SRQC Readiness Map) and `resource-claims-verification.md` (claim ledger) propose. 1QBit/TopQAD overlap is low if it only quotes published estimates and never computes physical resources.

---

## 2. The pain

### 2.1 Where adoption stalls (named organisations, numbers)

| Who | Evidence | Source, date, read depth |
|---|---|---|
| **Google Quantum AI** (Babbush, King, Boixo, Huggins, Khattar, Low, McClean, O'Brien, Rubin) | Five-stage framework. "Two central stages, identifying concrete problem instances … and connecting such problems to real-world use cases, represent essential and currently under-resourced challenges." Stage V (deployment) is "entirely prospective". "Problem-first" discovery ("ask a domain expert or customer for their hardest problem") "is rarely fruitful because quantum speedups tend to require exceptional mathematical structure". HHL has ">4k citations" but "we are not aware of any paper identifying a promising real-world instantiation". It describes a "classic collective action problem … systemic under-investment" in application work, and investors who assume "if we build it, apps will come". Google is building a "Compendium of Super-Quadratic Quantum Advantage" for domain experts and has "early success" with "an internal Google tool based on Gemini". | arXiv 2511.09124 v2 (2025-11-13), PRX Quantum 7, 020101 (2026). **partial** (abstract, intro, five stages, Stage I–III sections, Tables 2–4, economics, outlook) |
| **BCG** (Langione, Bobier et al.) | 2025 enterprise spend ≈ **$550M**, and enterprises now provide more than half of all quantum spending. About 100 enterprises ran about **150 POCs** by end-2024. **>60%** spend >$1M/yr. Algorithm/software share of spend rose from 21% to 40% (2022→2024). "Concrete applications that can be deployed against complex, real world problems remain scarce … many enterprises are stuck in the early stage of exploration." Its advice to CEOs: "identify three to five high-value use cases" and "translate business constraints into quantum-ready problems". | "Quantum Is Getting Real. CEOs Need to Shape Where It Creates Value", 2026-06-04 (mod. 2026-08-07). **full** |
| **OECD** (16 support organisations interviewed; survey synthesis) | Four barriers: immaturity, **unclear use cases and business implications**, cost, and talent. QuEra 2024 survey of users: unclear business value 39.6%, high cost 39.6%, skills 40.6%, immature algorithms 28.1%. ISED 2024 survey of Canadian quantum developers: main end-user barrier is "use cases still being proven" (21.4%). "Most of the examples of potential applications … originate from technology providers, particularly start-ups." Interviewees named PQC as the "first conversation" that opens the door. | "Building business readiness for quantum computing", OECD DEP No. 383, 2026-03-23. **partial** (§1–3.2, Tables 1–4) |
| Financial services (Moody's survey of 200 leaders, via OECD) | 87% see quantum as an opportunity. **73% had not identified any application** with a real commercial advantage. 87% have no dedicated budget. | 2023, via OECD. **stale?** |
| UK executives (EY/NQCC, 501 respondents, via OECD) | 97% expect disruption and only one-third have begun planning. **More than 1,000 executives declined** to take the survey, citing unfamiliarity. | 2022, via OECD. **stale?** |
| **McKinsey** Quantum Technology Monitor | More than 300 companies (Airbus, Boehringer Ingelheim, E.ON, JPMorgan, Liberty Mutual) work with quantum vendors. 33% of analysed companies spend >$10M/yr, 7% >$50M, and the largest budget is $200M. Quantum companies had >$1B revenue in 2025. Ivezic's critique: the value numbers compare 2035 quantum against 2026 classical baselines, and most applications remain "experimental or hybrid". | 2026-04-28. Primary page and PDF timed out: **snippet-only**. PostQuantum critique 2026-04-20 (mod. 2026-07-16): **full (secondary)** |
| **XPRIZE Quantum Applications** judges ($5M, Google/GESDA) | Where non-advancing submissions fell short: "applying existing quantum methods without sufficiently demonstrating an advantage over strong classical baselines"; "broadly appealing problems without clearly explaining why classical approaches are insufficient"; "quantum primitives without a convincing connection to real-world use". | xprize.org, 2026-01-21. **full** |
| **Zapata Quantum** (CEO Sumit Kapur) | "The process, in order to connect use cases to algorithms, is extraordinarily complex." Mark Hill, CDIO at CSL Behring and a Zapata adviser: "the harder question enterprises keep avoiding: which applications are worth building now". | Next Platform 2026-03-12, **full**. TQI 2026-09-22, **full** |

### 2.2 What they do today and what it costs

- **Consultants and vendor advisory.** BCG, McKinsey, Accenture and Applied Quantum sell this work. OECD lists Microsoft, Pasqal and QURECA as providers of readiness assessments. Engagement prices are undisclosed. BCG's >$1M/yr spending figure gives the scale.
- **Consortia and challenges.** QED-C sector workshops (for example oil and gas with SPE, 2026), QUTAC's QC Monitor, Q-STAR, and the BMW/Airbus challenges run with AWS. BMW is described as an outlier that built an expert team almost ten years ago (BCG).
- **Do-it-yourself reading** of papers and of free analyst pieces such as Ivezic's Utility Ladder.
- **Frequency** `[INFERENCE]`: each enterprise CoE re-screens its 3–5 use cases whenever a big algorithm or hardware result lands. Recent examples are Gidney 2025 (20× fewer RSA resources) and IBM's July 2026 "advantage era" claims. Ivezic had to fact-check the IBM claims paper by paper.

### 2.3 Why "not yet" is usually correct (the evidence a tool would rely on)

- **The quadratic barrier.** Babbush et al. 2021 (via PostQuantum, **stale?** but foundational) found that quadratic speedups (Grover, amplitude estimation, quantum-accelerated annealing) are uncompetitive at surface-code clock rates. One example: about 1 day on about 1M physical qubits to match 4 CPU-minutes of simulated annealing. Dalzell et al. found per-iteration T-counts of 10²²–10²⁴ for portfolio optimization (QIPM), which is "not practically advantageous" (PostQuantum Utility Ladder, upd. 2026-10, **partial**).
- **DQI, a showcase case.** Jordan et al. (Nature 646, 2025-10-22, **partial**: abstract, main text through OPI) show a superpolynomial speedup for OPI. On their max-XORSAT instance, "a tailored classical solver can outperform DQI". Google's Table 3 gives DQI-for-OPI 1,900 logical qubits, 6×10⁶ Toffolis and ~1 h on 8×10⁵ physical qubits, with **no Stage III application listed**. Kramer et al. (arXiv 2610.02145, 2026-10-01, **abstract-only**) prove an oracle-setting gap for folded OPI (DQI ≈0.85 vs classical threshold 0.65). It is still abstract, with no business problem attached.
- **Classical methods push back fast.** The Quantum Advantage Tracker (IBM, Algorithmiq, Flatiron, BlueQubit) holds 52 submissions (15 CVP, 20 OE, 17 VP). Only 19 include a quantum run; the rest are classical challenges. BlueQubit's peaked-circuit lead was overturned within months, with classical runtimes falling "to mere seconds" (IBM blog 2026-02-23, **full**; repo data JSON **full**, counted 2026-10-22). IBM's three July 2026 "advantage era" papers are still "active candidates" on the tracker, and none shows "a commercially useful speedup" (PostQuantum 2026-08-01, **full**).
- **Chemistry is real but narrower.** Lee et al. 2023 (**stale?**) found no evidence of generic exponential advantage in ground-state chemistry. Google's Table 4 places FeMoco at 1,500 LQ / 10⁹ Toffolis / 5×10⁶ physical / 9 h, and P450 at 1,200 LQ / 5×10⁸. Compare IBM's Starling target of 200 LQ × 10⁸ gates for 2029 (via PostQuantum).

---

## 3. Existing solutions

| Product / tool | What it does | Users | Price / license | Read depth |
|---|---|---|---|---|
| **Zapata Quantum Pilot** (Zapata Quantum, OTCQB: ZPTA) | Hardware-agnostic platform: "Quantum Graph" (knowledge layer of applications, algorithms and roadmaps), "Quantum Engine" (agents for algorithm selection and resource estimation, built with NVIDIA), "Quantum Assurance" (formal methods with UMD plus expert review). "Every quantum hypothesis compared with the strongest practical classical approach." A "dynamic application portfolio" | "Select enterprise and government customers", early access | Proprietary, demo on request, price undisclosed | TQI press 2026-09-22 **full**; product page **full** (undated) |
| **Quantum Links AI** | Problem and workflow assessment → choice of classical, ML or quantum route → real-QPU feasibility and cost → "evidence for next step" | Energy, logistics, life sciences (claimed) | Consulting, contact form | home page (mod. 2026-09-10) **full** |
| Consultancies (BCG, McKinsey, Accenture, Applied Quantum) and vendor advisory (Microsoft, Pasqal, QURECA) | Use-case workshops, readiness assessments, roadmaps | Large enterprises | Undisclosed | BCG **full**; OECD **partial** |
| GQI, The Quantum Insider | Market intelligence, scorecards | Investors, vendors | Paid | see `competitors-intelplatforms.md` |
| **PostQuantum Quantum Utility Ladder** (Marin Ivezic) | Hand-written catalogue mapping fault-tolerant algorithms to LQ, T-count, runtime and evidence strength, with a candid "finance won't be saved" section | CISOs, executives | Free article, copyrighted (link only) | upd. 2026-10, **partial** (~60%) |
| **Google Grand Challenge Tables 2–4** | About 30 Stage II–IV rows with logical qubits, Toffolis, physical qubits, time and advantage-assessment status | Researchers | **CC BY 4.0** (arXiv) | **partial** |
| Google "Compendium of Super-Quadratic Quantum Advantage" and internal Gemini tool | Plain-language catalogue for domain experts, plus an AI tool that matches problems to speedups | Internal | Not public; no release found (search 2026-10-22) | described in 2511.09124 |
| **Quantum Advantage Tracker** | Open submissions of quantum vs classical results on canonical instances | IBM, Algorithmiq, Flatiron, BlueQubit, Caltech, LANL | **Apache-2.0**, 126★, last commit 2026-10-22 ("submission from issue #250") | README, CONTEXT.md, data **full** |
| Quantum Algorithm Zoo (Stephen Jordan) | Catalogue of more than 500 references by speedup type | Researchers | Repo `stephenjordan/stephenjordan.github.io` has **no license**, last commit 2026-10-07 (link, don't copy) | **partial** |
| metriq-gym / QED-C App-Oriented Benchmarks | Hardware benchmarks, not use-case triage | Vendors | Apache-2.0; pushed 2026-10-22 and 2026-10-23 | README / metadata |
| Quantum-Audit benchmark | 2,700 quantum-concept questions for LLMs, including 350 false-premise questions | AI evaluation | arXiv 2602.10092 (2026-02-10) | **abstract-only** |

---

## 4. The gap

**Unsolved:** no **open, free, citation-locked** tool that does all of the following:
- takes a plain-language business or science problem;
- maps it to a known primitive, or says that none exists;
- places it on Google's stage scale;
- shows the nearest published end-to-end estimate next to vendor roadmaps;
- surfaces the strongest classical counter-evidence (tracker, dequantization, tailored heuristics);
- is itself **measured** for overclaiming.

Zapata does most of this behind an enterprise early-access wall, with human experts. The Ivezic ladder and the Google tables hold the evidence but cannot be queried. They also cannot map "our fleet-charging scheduling" to "this is quadratic-search territory".

**Why nobody has filled it:**
1. **Incentives.** Google calls it a collective-action problem: vendors put their resources into hardware. Consultants and Zapata monetize the answer, and "not yet" does not sell POCs `[INFERENCE]`.
2. **Staleness.** Stage IV is "a moving target". Estimates fell five orders of magnitude for FeMoco. A static catalogue rots, which suits an agent with dated, versioned evidence.
3. **LLMs alone are unsafe for this job.** Quantum-Audit found models "frequently accepted and reinforced false premises". A raw chatbot asked "can quantum optimize our logistics?" is the hype machine that OECD and Google warn about.
4. **Zapata's history shows the business is hard.** Zapata (founded 2017 as a Harvard spin-out) shut down in Oct 2024. Its AI-focused SPAC "brought in effectively zero of equity capital … and $20-plus millions of liability". The pivot to "quantum-inspired AI" left it "mispivoted". The company re-emerged in Sep 2025, restructured $18.7M of debt, and returned to this exact use-case-to-algorithm job. Kapur: "we were a little bit ahead of our time" (Next Platform 2026-03-12 **full**; TQI 2024-10-12 **full**; SEC EDGAR filing index **partial**). The lesson `[INFERENCE]`: selling use-case answers before hardware could run them did not sustain a company on its own. A hackathon tool should be free infrastructure, not a SaaS bet.

---

## 5. Candidate wedges

### Wedge A (best): **Not Yet**, a triage agent for quantum use-case claims

- **User.** First-pass screeners who must answer "should we spend on quantum for X?":
  - enterprise innovation and CoE analysts at the long tail of firms that cannot buy Zapata or BCG (OECD's "awareness concentrated in just a few individuals");
  - domain scientists, who are the audience Google's compendium targets;
  - quantum-startup BD staff who need credible "not yet" answers to keep customer trust.

  Named targets for outreach (none confirmed): Mark Hill (CSL Behring, who publicly framed this exact question); QED-C working-group members; Waterloo and Toronto innovation leads.
- **Job.** Given a problem statement (and optionally a vendor pitch or press release), return a **verdict card**:
  - (i) the matched primitive, or "no known super-quadratic route";
  - (ii) the Google stage reached;
  - (iii) the nearest published estimate (LQ, Toffolis, physical qubits, time), with citation;
  - (iv) the gap against vendor roadmaps (IBM Starling 200 LQ / 10⁸ gates 2029; Blue Jay 2,000 LQ / 10⁹ gates 2033+; QuEra 2028; IonQ 2029 claims);
  - (v) the strongest classical counter-evidence;
  - (vi) the verdict: *Now / plausible in 2029–2033 hardware / beyond published roadmaps / no known advantage*.

  Deterministic code computes (iv) and (vi) from the evidence table. The LLM only maps the problem and writes the explanation, and every number must quote a row.
- **2-minute demo.**
  1. "Logistics firm: can quantum optimize vehicle routing?" The answer is **no known super-quadratic route**. The card cites the quadratic barrier and the QAOA-for-8-SAT row: 28,000 LQ, 5×10¹¹ Toffolis, 7×10⁷ physical qubits.
  2. "Battery R&D: cathode degradation spectra." The card shows a Stage III/IV row (Li₂MnO₃ dynamic structure factor, 100 LQ, 9×10¹¹ Toffolis) that lies beyond Starling's gate budget, so "watch; not before post-2029 hardware".
  3. Paste IBM's July 2026 "advantage era" press line. The card shows "Stage II candidates, tracker status active, no commercial workload".
  4. A benchmark slide: raw model vs Not Yet, overclaim rate on 60–100 labelled cases.
- **Reusable components (verified 2026-10-22).**
  - Google 2511.09124 Tables 2–4 (CC BY 4.0, attribute): hand-transcribe about 35 rows.
  - `quantum-advantage-tracker/quantum-advantage-tracker.github.io` (Apache-2.0, last commit 2026-10-22): ingest `data/*/submissions.json` for live classical-pushback status.
  - Quantum Algorithm Zoo: link only, no license.
  - Optional: `quantumlib/Qualtran` (Apache-2.0, pushed 2026-10-22) for cross-checking logical counts. **Do not** use physical QRE, to avoid TopQAD overlap.
- **Data and compute.** About 35 Google rows, about 10 roadmap rows, about 15 "no-go" rows (quadratic barrier, QIPM, dequantized QML, DQI max-XORSAT), 52 tracker rows, and 60–100 labelled benchmark prompts. Roughly 3 of the 12 hours go to curation. CPU only. SurrealDB holds the evidence graph (case → row → source → date).
- **LLM cost** `[INFERENCE]`: about 2 calls of ~6k tokens per query, so cents per query. The benchmark (100 cases × 3 models × 2 conditions ≈ 600 calls) costs about $20–40, within the $100 Anthropic credit.
- **Partner-prize fit.** Eon Era (agent testing and benchmarking: the overclaim benchmark is the core deliverable) is strong. SurrealDB Agent Memory (versioned evidence graph, verdict history as estimates fall) is good. Clerk (saved portfolios) is weak.
- **Main way it fails.** Judges see "a chatbot over a table", and users stop coming back because the answer is almost always "no". Mitigation: lead with the measured overclaim benchmark and the "verdict changed when estimate X dropped" history view. A second risk is a mis-mapped problem. Mitigation: show the matched primitive's preconditions (sparsity, condition number, data loading) and ask the user to confirm them.

### Wedge B: **Hype-Check**, an open use-case overclaim benchmark for LLMs

- **User.** AI-evaluation teams and anyone deploying LLM assistants for technology scouting.
- **Job.** 150 enterprise-style prompts with ground-truth verdicts drawn from the evidence table. It scores overclaim rate, citation accuracy and false-premise correction across frontier models, with and without retrieval.
- **Demo.** A leaderboard, plus side-by-side transcripts where a model invents advantage for portfolio optimization.
- **Components.** Same evidence table. Quantum-Audit is the closest prior work (concept questions, not use-case verdicts). It is abstract-only here, so check whether its data is released.
- **Cost.** About $30–60. **Prize fit:** Eon Era is strong.
- **Fails because** the "user" is diffuse and the real-world-impact story is weak for Georgian. It works best as Wedge A's eval harness, not as a separate project.

### Wedge C: **Advantage-claim docket**, an evidence card per new claim

- **User.** Analysts and journalists who fact-check claims such as IBM's July 2026 papers, plus tracker participants.
- **Job.** Turn an arXiv or press claim into a card: stage, verifiability (classical, quantum or none), tracker status, classical rebuttals, evidentiary level.
- **Fails because** it overlaps the ruled-out diligence/intel space and the peer claim ledger. Ivezic already does it by hand, with high quality. Skip it unless merged with the peer claim-ledger wedge.

---

## 6. Scores: Wedge A (Not Yet)

| Criterion | Score | Why |
|---|---|---|
| Real user with evidence of pain | 3 | Pain is documented by BCG (2026), OECD (2026), Google, XPRIZE judges, and a vendor product launched for it (Zapata, 2026-09-22). No named individual has committed to using a free tool. |
| AI makes a material difference | 4 | Google names recognition across terminology as GenAI's Stage III strength. Raw LLMs overclaim (Quantum-Audit <66% on false premises). The tool's value is LLM mapping plus deterministic verdicts. |
| Severyn's unfair advantage | 4 | MSc in quantum information, runs a resource-estimation demo, has a verification and open-benchmark track record (Aquarium), and can judge the mappings himself. |
| Buildable and demoable in 12 hours | 4 | About 3 h curation, 4 h agent and verdict logic, 3 h UI, 2 h benchmark. All data public, CPU only. |
| Judge appeal (Georgian investors) | 3 | The B2B line "stops $1M POCs that can't work" lands. Quantum is niche for a growth fund, and judges will ask "vs Zapata?" |
| Adoption path after Oct 25 | 2 | A free tool with diffuse users and no distribution channel. Possible routes: the tracker community, QED-C, a contribution to Google's compendium effort. Zapata owns the enterprise buyer. |
| Competition density (5 = open field) | 2 | Zapata Quantum Pilot, Quantum Links AI, consultancies, Ivezic's ladder, and Google's internal Gemini tool all target the job. The open, measured version is the only gap left. |
| Credibility gain in AI and quantum | 4 | Evidence-graded verdicts citing primary FT estimates, plus a published LLM calibration benchmark. Matches Severyn's "evidence whichever way it lands" brand. |
| Risk (5 = low: no dual use, no 1QBit overlap) | 4 | Quotes only published estimates and computes no physical resources, so TopQAD overlap is low. Crypto rows are public numbers. Small positioning risk if 1QBit still sells applications consulting (unverified). |
| **Total** | **30 / 45** | |

---

## 7. Sources

| # | Source | Date | Read depth |
|---|---|---|---|
| 1 | Babbush et al., "The Grand Challenge of Quantum Applications", https://arxiv.org/html/2511.09124v2 (PRX Quantum 7, 020101, https://link.aps.org/doi/10.1103/6r9l-lynr) | v2 2025-11-13; PRX 2026 | partial (abstract, intro, Stages I–III, Tables 2–4, economics, outlook) |
| 2 | BCG, "Quantum Is Getting Real. CEOs Need to Shape Where It Creates Value", https://www.bcg.com/publications/2026/ceos-need-to-shape-where-quantum-creates-value | 2026-06-04 (mod. 08-07) | full |
| 3 | OECD, "Building business readiness for quantum computing", DEP No. 383, https://www.oecd.org/en/publications/building-business-readiness-for-quantum-computing_ee847e5f-en/full-report/component-4.html | 2026-03-23 | partial (§1–3.2) |
| 4 | McKinsey Quantum Technology Monitor 2026, https://www.mckinsey.com/capabilities/mckinsey-technology/our-insights/mckinsey-quantum-technology-monitor-2026-a-commercial-tipping-point | 2026-04-28 | snippet-only (timed out) |
| 5 | Ivezic, "McKinsey Quantum Monitor 2026: Tipping Point?", https://postquantum.com/industry-news/mckinsey-quantum-monitor-2026/ | 2026-04-20, mod. 07-16 | full (secondary) |
| 6 | TQI, "Zapata Launches Platform to Help Companies Assess Quantum Use Cases", https://thequantuminsider.com/2026/09/22/zapata-launches-platform-to-help-companies-assess-quantum-use-cases/ | 2026-09-22 | full |
| 7 | Zapata Quantum Pilot page, https://zapataquantum.com/quantum-pilot | undated (2026) | full |
| 8 | Burt, "Four Months Into Its Comeback, Zapata…", Next Platform, https://www.nextplatform.com/compute/2026/03/12/four-months-into-its-comeback-zapata-stakes-its-claim-in-quantum-software/5209179 | 2026-03-12 | full |
| 9 | TQI, "Zapata Computing Holdings Inc. Ceases Operations", https://thequantuminsider.com/2024/10/12/zapata-computing-holdings-inc-ceases-operations/ | 2024-10-12 **stale?** (historical fact) | full |
| 10 | SEC EDGAR, Zapata Quantum filing index, https://www.sec.gov/Archives/edgar/data/1843714/000095017024114391/ck0001843714-20241007.htm | to 2026-10-20 | partial (index only) |
| 11 | Quantum Links AI, https://www.quantumlinks.ai/ | mod. 2026-09-10 | full |
| 12 | IBM, "Quantum Advantage Tracker: the race to advantage", https://www.ibm.com/quantum/blog/quantum-advantage-tracker | 2026-02-23 | full |
| 13 | Quantum Advantage Tracker repo, https://github.com/quantum-advantage-tracker/quantum-advantage-tracker.github.io (Apache-2.0; data JSON) | last commit 2026-10-22 | README, CONTEXT.md, data full |
| 14 | Ivezic, "IBM's Three Quantum Advantage Claims, Fact-Checked", https://postquantum.com/industry-news/ibm-three-quantum-advantage-papers/ | 2026-08-01 | full |
| 15 | Ivezic, "Quantum Utility Ladder for Fault-Tolerant Algorithms", https://postquantum.com/quantum-utility-map/quantum-utility-ladder-fault-tolerant-algorithms/ | upd. 2026-10 | partial (~60%) |
| 16 | Ivezic, "The Five Stages from Idea to Impact", https://postquantum.com/industry-news/google-framework-quantum-applications/ | 2025-11-13 | full (secondary) |
| 17 | Jordan et al., "Optimization by decoded quantum interferometry", Nature 646:831, https://pmc.ncbi.nlm.nih.gov/articles/PMC12545177/ | 2025-10-22 | partial (abstract, main through OPI definition) |
| 18 | Kramer et al., arXiv 2610.02145, https://arxiv.org/abs/2610.02145 | 2026-10-01 | abstract-only |
| 19 | XPRIZE, "From Promise to Proof…", https://www.xprize.org/news/from-promise-to-proof-what-qualified-the-2025-xprize-quantum-applications-phase-i-finalists | 2026-01-21 | full |
| 20 | XPRIZE 2026 Finalist Teams Book page, https://www.xprize.org/news/2026-finalist-teams-book-xprize-quantum-applications | 2026-05-10 | full (page; PDF not read) |
| 21 | Afane et al., "Quantum-Audit", arXiv 2602.10092, https://arxiv.org/abs/2602.10092 | 2026-02-10 | abstract-only |
| 22 | Eisert & Preskill, "Mind the gaps", arXiv 2510.19928, https://arxiv.org/abs/2510.19928 | 2025-10-22 | abstract-only (no conclusion rests on it) |
| 23 | Quantum Algorithm Zoo, https://quantumalgorithmzoo.org/ (repo stephenjordan/stephenjordan.github.io, no license) | last commit 2026-10-07 | partial |
| 24 | GitHub API metadata: Qualtran (Apache-2.0, 2026-10-22), microsoft/qdk (MIT, 2026-10-22), metriq-gym (Apache-2.0, 2026-10-22), metriq-app (archived, moved to monorepo), SRI QC-App-Oriented-Benchmarks (Apache-2.0, 2026-10-23), zapatacomputing/benchq (Apache-2.0, 2025-03-06 **stale?**) | queried 2026-10-22 | metadata |
| 25 | QED-C 2026 reports (market forecast; government-industry workshop; SPE oil and gas), https://quantumconsortium.org/publications/reports/ | 2026-04 to 2026-10 | snippet-only |

---

## 8. Open questions

1. **A named user before Saturday?** Can Severyn get 2–3 people (an enterprise innovation lead, a QED-C member, a startup BD lead, or Mark Hill) to say "I'd run my use case through this"? Without that, Wedge A should rank below the peer wedges that have named users (claim ledger, SRQC map).
2. **Merge or compete?** Should synthesis build one evidence-card engine with three views: crypto claim ledger (`resource-claims-verification`), DOE/SRQC target map (`quantum-demand-map`), and enterprise "Not Yet" (this report)? The data model is the same: claim → estimate → source → date. The users differ.
3. **Zapata positioning.** Judges will ask "why not Zapata?" The answer would be "open, free, measured, says no". Is that enough for Georgian, or does it read as a weaker clone?
4. **Google's compendium.** If it is released this month, it becomes the canonical data source, or it makes the tool redundant. A quick email to Robbie King or Ryan Babbush might settle this and could even produce a user.
5. **Licensing.** The arXiv HTML is CC BY 4.0. Confirm the PRX Quantum version's license before redistributing the transcribed tables. Ivezic's ladder and the Algorithm Zoo are link-only.
6. **1QBit.** Does 1QBit currently sell enterprise use-case consulting (its historical business)? If so, positioning risk rises from low to medium. This was not verified this session.
7. **Scope of "no".** Should the benchmark include crypto rows, which are public but sensitive, or leave cryptanalysis to the PQC peer report and keep "Not Yet" to chemistry, materials, optimization, finance and ML?
