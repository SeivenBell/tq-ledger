Source: commit 21d086a on branch `research/practitioner-pain`, file `docs/research/practitioner-pain.md` (31,589 characters, pasted in full below in one part).

---

# Practitioner pain: what quantum researchers, developers and hardware engineers say hurts day to day, and where AI could help

Ticket #11. Research date: 2026-10-22. Read-depth labels: **full**, **partial (sections …)**, **snippet-only** (nothing snippet-only carries a conclusion). `[INFERENCE]` marks my own analysis. Sources older than 18 months are flagged **stale**.

Access notes: Reddit, quantumcomputing.stackexchange.com (HTML), riverlane.com and the GitHub API for third-party repos were blocked in this environment. Stack Exchange data came through its public API; GitHub counts came from the rendered web pages; Riverlane's survey came through three news write-ups.

---

## 1. Bottom line

1. **Yes, there is a real, quantified day-to-day pain, but it is mundane.** The most consistent complaint of working quantum software practitioners is SDK churn: 81% of surveyed developers (n=26, all Qiskit users) hit bugs after library updates; 41% of 483 forum-mined hybrid-code issues were configuration or library/platform problems; "incompatible with current stack" blocks 30 to 35% of 698 Unitary Foundation respondents from tools they want. In their words: "when Qiskit was upgraded, everything changed"; "Half the qiskit examples you find are all using deprecated modules."
2. **Practitioners have already moved to LLMs, and the LLMs fail on exactly this pain.** 54% of 807 Unitary Foundation respondents now use GenAI tools for answers (37% a year earlier); Quantum Computing Stack Exchange question volume fell from 2,051 (2023) to 864 (2025) to 227 so far in 2026, with the unanswered share rising from 17% to 40%. But LLM-generated Qiskit breaks across SDK versions ("API drift remains only partly recoverable even with migration guidance"), and IBM's own Qiskit Code Assistant was discontinued in May 2026 after never leaving preview. Generic "chat to circuit" is crowded and unproven; **verified** code repair is not.
3. **Hardware engineers' pain is bigger but unreachable in 12 hours.** Bring-up takes about a day per fixed-frequency chip and a week per tunable chip; drift forces retuning "every six hours or so"; every lab runs home-grown control code. Four vendors (Quantum Machines, Zurich Instruments, Q-CTRL, Qruise) already sell calibration automation, and LLM-agent calibration is already a published research result (MIT and OpenAI, Sep 2026; BAQIS, Jun 2026). Severyn has no lab and no hardware user after Oct 25. Skip.
4. **Fault-tolerant resource-estimation toil is confirmed in practitioners' own words and in hiring**, which supports `field-needs.md`: Qualtran's authors call manual analysis "tedious, consuming months of researcher time and dozens of pages"; IonQ, Xanadu and Alice & Bob postings hire people to *build* estimation methodology and tooling. But PsiQuantum made Construct free and open-access in May 2026, and the physical layer overlaps 1QBit's TopQAD.
5. **Best wedge from this ticket:** a *verified SDK-migration agent*: give it a 2022 to 2024 paper repository or notebook, it rewrites the code to Qiskit 2.x, runs old and new on a simulator, proves circuit equivalence with MQT QCEC, and emits a migration report. Reusable Apache-2.0 and MIT parts exist. Estimated LLM cost under $40. Average score 3.6 of 5; the main failure mode is commoditisation by Claude Code or IBM.
6. **What this ticket does not find:** no practitioner, in any survey, forum or posting, asks for AI to *discover* better circuits or algorithms. That demand is paper-driven (see `quantum-ai-discovery.md`), not practitioner-driven. Any discovery-flavoured project must find its user elsewhere (program evaluators, FT algorithm teams), not among day-to-day developers.

---

## 2. The pain

### 2.1 Software practitioners: SDK churn, dependency hell and silent wrong answers

| Evidence | Who | Finding | Date, depth |
|---|---|---|---|
| Zappin, Stalnaker, Chaparro, Poshyvanyk, "Challenges and Practices in Quantum Software Testing and Debugging: Insights from Practitioners", TOSEM (accepted; dated Feb 2026); data May to Aug 2024 | n=26 valid responses (1,397 invited at 71 organisations incl. IBM, Google, NVIDIA, IonQ, Rigetti; "more than 10" declined citing NDAs); 18 PhDs; all use Qiskit; 4 follow-up interviews | **81%** (21/26) hit bugs after library or platform updates, 42% frequently. **69%** use no dedicated debugging tool (print statements, "run with different inputs"). **62%** use no testing tool; only **31%** use a quantum-specific one. **54%** see flaky tests. **50%** see silent wrong output frequently. Backward-compatibility issues 21/26. Interview: Qiskit 1.0 transition "quite impractical" because "almost the entire API changed"; "You can't always trust the output. Sometimes it looks fine, but it's not what you expect"; "The classical side breaks before the quantum side ever does"; "I want to look at it! And I'm like, no, that doesn't scale!" | 2026-02, **full** (52 pp) |
| Unitary Foundation 2025 Quantum Open Source Software Survey (survey Sep 2 to Oct 5, 2025; results Nov 2025) | 1,400+ respondents; per-question n 600 to 1,149; roles: researcher 50%, developer 37%, student 29%; affiliation academic 41%, enterprise 27%, startup 27%; 38% unpaid | Reasons for not using a wanted tool (n=698): price 45%, **poorly documented 38%** (down from 51% in 2024), **tool does not exist 35%**, **incompatible with stack 30%**. Among software developers: tool does not exist 42%, poorly documented 41%, incompatible 39%. Open text: "The number of tools and libraries that all do the same thing is growing and inflating. We need to group together!"; 2024: "normalizing crappy quantum software." Qiskit used by 69%, PennyLane 31%, Cirq 17%. | 2025-11, **full** (embedded data extracted) |
| Zappin et al., "When Quantum Meets Classical", ICSE 2025 (arXiv 2411.16884; data to Oct 2023) **stale** | 531 issues from PennyLane forum (377) and QC Stack Exchange (154) | Of 483 categorised: developer errors 29%, software faults 25%, **library/platform 24%, configuration 17%**, hardware 5%. 74% manifest as crashes; 70% caused by programmer error; 15 cases of platform updates breaking other libraries; Qiskit Aqua and Ignis deprecation made code and docs obsolete. | 2024-12, **full** |
| Khan et al., "Mining Q&A Platforms for Empirical Evidence on Quantum Software Programming" (arXiv 2503.05240; data Apr 2024) | 6,935 Stack Exchange posts | Data handling and module management 9.8%, file and system configuration 5.9%; hardest topics are classical paradigms applied to quantum (OOP, parameter control, threading); accepted-answer proportion declining over time. | 2025-03, **full** |
| El Aoun et al. (arXiv 2205.03181; data to Mar 2021) **stale** | 3,117 posts, 43,979 GitHub issues from 122 projects | Environment management 15% and dependency management 15% of posts; environment management hardest (61% unanswered). GitHub: API change 11.7% of issues across 81% of projects. | 2022-05, **full** |
| Hacker News, user fastneutron, 2022-07-04 **stale** | self-described applied quantum researcher | "the biggest issue I've have with quantum development isn't the interface per se … but the instability of the underlying APIs. Half the qiskit examples you find are all using deprecated modules, and anything off that beaten path might as well be throwaway code once the corresponding paper is published." | **full** |
| Qiskit repository, 2026-10-22 | — | 7.9k stars, 726 open issues, 121 issues matching "deprecat"; latest 2026-09-24 "deprecate (and remove) qasm3.load_experimental". Qiskit 2.0 removed BackendV1, Pulse, `c_if`, V1 primitives, `classicalfunction`; releases 2.0 to 2.5 in about 18 months; deprecation policy: removals only in yearly majors. | **full** (issue and release pages) |

**Disconfirming evidence.** In the TOSEM survey only 35% rate debugging "difficult"; 61% say "neutral", and the authors concede this is "at odds with other findings". Industry respondents average about five testing methods each and one said academic tools "don't fit our workflows", so the gap may be fit, not absence. In the Unitary Foundation survey 94.5% rate the open-source ecosystem positively, documentation complaints fell 13 points in a year, and price, not tooling, is the top barrier (students 66%). The n=26 study is the only large-signal source on debugging; the 1,400-person survey never asks about it.

### 2.2 Everyone: the Q&A commons is collapsing into LLMs, which are unreliable past the basics

Quantum Computing Stack Exchange (public API, 2026-10-22):

| Year | Questions | Accepted answer (latest 300) | Unanswered (latest 300) |
|---|---|---|---|
| 2021 | 2,065 | 47% | 17% |
| 2023 | 2,051 | 42% | 30% |
| 2025 | 864 | 42% | 26% |
| 2026 (to Oct 22) | 227 | 31% | 40% |

Stack Overflow fell faster over the same period (1.33M questions in 2022 to 109k in 2025), so this is the general LLM shift, not quantum-specific `[INFERENCE]`. The Unitary Foundation survey confirms the destination: GenAI tools as an information source rose from 37.4% (2024, n=602) to **54.3%** (2025, n=807), while Stack Exchange fell from 40.4% to 35.8% and Stack Overflow from 39.5% to 29.1%. Project documentation (81%) and source code (74%) still rank higher.

What practitioners say about the LLMs, verbatim:
- Hacker News, 2026-01-09, self-described quantum computing worker: "I have tried a few different ones, but they all start spouting nonsense about anything that is not super basic … I have tried Sonnet, Opus, various versions of GPT, Deepseek … I can't quite get them to work in quantum computing." (**full**)
- Hacker News, 2026-09-06, "Quantum software engineer here": "I use Claude quite extensively with quantum SDKs like Qiskit and Pennylane. It tends to be very good at scaffolding and architecture, but can spiral or be outright incorrect when it comes to implementing certain algorithms like QAOA … a lot of hand-holding is required." (**full**)
- PennyLane forum, 2026-01-13: AI tools "are helpful for clarification and examples. However, they are not fully reliable as a primary learning source, especially for internal Qiskit design … and up-to-date development workflows." (**full**)

Benchmarks agree on *where* they fail. Qiskit QuantumKatas (IBM Research, arXiv 2605.27210, May 2026; 350 tasks, 16 models; **full**): GPT-5.5 83.1%, Claude Opus 4.7 80.9%; errors are 43% wrong quantum state, 31.6% code-structure, 13.6% Qiskit API; "quantum reasoning, not code syntax, is the primary limitation." API drift benchmark (arXiv 2607.04072, Jul 2026; 17 models, Qiskit 0.43/1.3/2.0; **partial**): pass@1 ranges 0.02 to 0.85 by version; doc-guided repair succeeds only 19 to 59%. Bugs4Q re-validation (arXiv 2607.09007, Jul 2026; **partial**): GPT-5.4 repairs 48.8% at pass@10, all models do best on Qiskit 0.45 and worse after 1.0; deprecated APIs caused 13 to 56% of failures.

### 2.3 Hardware engineers and experimentalists: bring-up, drift, home-grown software

| Evidence | Finding | Date, depth |
|---|---|---|
| Yankelevich, Zhang, DeCaro, Grover, Oliver (MIT EQuS) with OpenAI, "Case Study: Agentic Calibration of Superconducting Qubits" | "Calibrating a novel multi-qubit experiment can require months and thousands of preliminary measurements." Fixed-frequency qubit set ≈ 1 day; tunable set ≈ 1 week. "A measurement that worked one day fails the next … revisiting measurements completed dozens of steps earlier." Agent (GPT-5.6 via a Jupyter MCP) tuned 4 fixed-frequency qubits with 4 of 40 interventions; tunable qubits "required significant instruction"; "agents take longer than experienced researchers"; infrastructure took "several months". Data on a Dropbox-synced Windows lab PC. | 2026-09-04, **full** (co-branded with the model vendor) |
| Xu et al. (BAQIS), "Vibe Calibration", arXiv 2606.22376 | Expert manual: 14.3 min per qubit (3.8 h for 16); 18 to 24 h estimated for 112 qubits; agent did 108/112 in 4.7 h. "Sustained attention over long calibration runs ultimately gives way to fatigue and error." | 2026-06, **partial** |
| Pack, Machnes (Qruise), Wilhelm, arXiv 2509.08555 | Manual calibration "often on the order of hours to weeks"; 50+ qubits "weeks or months"; "does not deliver new scientific insights." | 2026-04 v4, **partial** |
| IEEE Quantum Week 2026 roundup (Quantum Zeitgeist) | Retune "every six hours or so" (Quantum Machines); machines "offline for about an hour two to four times a day" (NVIDIA); reporter's caveat: most loop times from emulated qubits. | 2026-10-20, **full** |
| IBM Quantum docs, calibration jobs | Monitoring jobs "approximately once an hour"; Heron calibrations "under two hours per day"; no drift indicator or calibration history exposed to users, only `last_update_date` and per-property timestamps. | **full** |
| Stack Exchange #46297 (2026-06-05), #46449 (2026-09-30), #46462 (2026-10-13), **full** via API | Cloud users hit drift and opacity: same 12-qubit GHZ on ibm_fez gave F=0.692 then 0.503 four hours apart, "roughly 30 to 100× larger than shot noise"; "Does IBM Quantum expose any calibration timestamp or drift indicator?" (unanswered). Co-hosting GHZ compartments in one job on IQM Garnet collapsed fidelity from 94% to 46% (unanswered). Shot ordering undocumented ("I also submitted this to the Support Center … I don't expect a reply"). | 2026, **full** |
| Hacker News, 2022-06-01 **stale**; 2026-09-09 | PhD student rewrote LabVIEW lab control in Python; "my supervisors … did not see any value in software development." Counterpoint 2026: "I had qubit bring up and calibration fully automated with Python in 2011 … not sure if AI is really needed there, curve fitting and some data logging is enough." | **full** |

### 2.4 Fault-tolerant algorithm and QEC researchers: toil, non-comparable estimates, training gap

- Harrigan et al. (Google), Qualtran paper, arXiv 2409.04643 (Sep 2024, **partial**: intro): "a manual analysis is tedious, consuming months of researcher time and dozens of pages in a publication" (16 pages in one reference, 41 in another); "imprecise, requiring a researcher to approximate in an ad hoc way"; "inaccessible, yielding numerical figures that are hard for a reader to reproduce or extend." Nasir and Ahmad, arXiv 2610.10490 (Oct 2026, abstract **full**): estimates "almost always reported as single numbers, even though they rest on uncertain hardware parameters"; five cost models "disagree by a stable factor of two."
- Job postings (2026, all **full** unless noted): IonQ Senior Staff Scientist, FTQC algorithms ($193k to $253k): "Define, develop, and drive adoption of industry-leading benchmarking and resource estimation methodologies, metrics, and tools." Xanadu Quantum Scientist, Algorithms: "Collaborate with PennyLane software developers to create state-of-the-art tools for quantum algorithms research"; "constant-factor resource estimation" listed as a scarce skill. Alice & Bob Quantum Compilation Scientist: "Improve the resource estimator to integrate our newest architectural improvement … make it usable by external users." IBM Dublin Research Scientist: "Produce qubit/T-count/depth estimates under plausible error-correction assumptions." Quandela Resource Estimation Scientist re-listed Jul and Aug 2026 (snippet-only). Across 12 postings, Stim, Qualtran and Azure QRE appear in zero; Python is universal, C++ or Rust in 8.
- Riverlane 2025 QEC Survey (Aug 2025; 300+ professionals from academia, industry, national labs; read via The Quantum Insider and Quantum Computing Report, **full**): top barriers to QEC adoption are **limited training and knowledge 41%**, lack of best practices or guidelines 28%, difficulty securing resources 28%; 96% expect to need external support; 88% can build circuits, 62% have built a surface-code circuit. Unitary Foundation 2025: for QEC tools specifically, "tool does not exist" 35%, poorly documented 32% (n=752); 32% use QEC software (Stim 39% of those, PyMatching 21%, Deltakit 15%).
- Workforce (QED-C "Connecting the Dots", Apr 2025, **full**; a 32-participant workshop report, not a survey): bottleneck is hands-on experience, mentorship and career clarity, "particularly at the associate degree and technician levels". No developer-tooling content.

---

## 3. Existing solutions

| Product or tool | What it does | Who uses it | Price or licence | Depth |
|---|---|---|---|---|
| IBM Qiskit Code Assistant | Fine-tuned Qiskit models (mistral-small-3.2-24b-qiskit, granite-3.3-8b-qiskit) with VS Code and JupyterLab extensions | Premium Plan preview since Oct 2024. **Hosted service discontinued 29 May 2026**; the Qiskit MCP repo removed its server "because the underlying Qiskit Code Assistant service has been discontinued by IBM Quantum" | Models Apache-2.0 on Hugging Face; 52 and 229 downloads last month | **full** (docs, HF cards, mcp-servers README); sunset notice snippet-only |
| Qiskit/mcp-servers (IBM) | MCP servers for Qiskit core, IBM Runtime, AI transpiler, docs search | 41 stars; pushed 2026-10-08; PyPI `qiskit-mcp-server` 1,552 downloads last month | Apache-2.0 | **full** |
| flake8-qiskit-migration (qiskit-community) | Linter flagging deprecated or removed imports, methods and arguments for Qiskit 1.0 and 2.0 | 2 stars; last commit 2026-02-24 | Apache-2.0 | **full** |
| LLM Qiskit refactoring (arXiv 2506.14535; 2606.20173) | Taxonomy-guided LLM migration to Qiskit 0.46; RAG variant with Gemini Flash 2.5 | Academic; no code found | CC BY-SA paper | **partial** |
| MQT QCEC (TUM) | Equivalence checking of two circuits (Qiskit `QuantumCircuit` or OpenQASM); proves equivalence or finds counterexamples | 120 stars | MIT | **full** |
| Classiq Quantum Agent | Natural language to Classiq functional model to synthesised circuit | Launched 2026-04-23; platform customers Rolls-Royce, BMW, Comcast; 20% of UF respondents used the Classiq library | Not stated | **full** (press release) |
| Bloq Maya | Conversational agent for circuits, QUBOs and code on IBM and Braket | Launched 2026-10-13; 1 to 10 staff; no usage numbers | Not stated | **full** (news) |
| Pasqal agent-marketplace | Claude Code / Codex skills: paper to spec to Pulser sequence to QPU | 6 stars; pushed 2026-10-08 | Apache-2.0 | **full** |
| PennyLane (Xanadu) | Largest non-IBM SDK | No first-party AI assistant, MCP or agent found | Apache-2.0 | **full** (site search) |
| Quantum Machines QUAlibrate | Calibration-graph automation for OPX controllers | Source moved private 2026-03-18; PyPI 1.3+ ships a proprietary EULA ("Alpha/Beta … not for production") | Was BSD-3; now proprietary | **full** (repo, wheels) |
| Zurich Instruments LabOne Q | DAG calibration framework; 26 of 28 qubits characterised in 3 to 3.5 h vs "days of operator time" | ZI hardware | Apache-2.0; 58 stars; v26.7.0 Jul 2026 | **full** |
| Q-CTRL Boulder Opal Scale Up | "Fully autonomous quantum computer bootup"; cold-start calibration 90 min | QuantWare and others | SaaS, quote | **full** (marketing) |
| Qruise OS / ML; Conductor Quantum | Multi-vendor automated tune-up; ML tune-up for spin qubits | Jülich; SemiQon, LBNL | Quote | **full** (marketing) |
| I-QMapper (arXiv 2606.27508) | Jupyter tool: IBM calibration heatmaps, 7/14/30-day drift views, layout score | PyPI `i-qmapper` | Open-source (licence not confirmed) | **partial** |
| PsiQuantum Construct | Visual circuit designer, Resource Analyzer, 100+ FTQC subroutines, Bartiq, QREF | Public free access since 2026-05-28; Brookhaven partnership | Free; Bartiq Apache-2.0 | **full** |
| Qualtran, Bartiq, MS QRE, TopQAD | See `field-needs.md` §2 | | | |

---

## 4. The gap

1. **No tool closes the loop from "my quantum code broke after an SDK update" to "it runs again and provably does the same thing."** The linter only flags imports; the LLM papers stop at Qiskit 0.46 and release no code; general LLMs recover API drift only 19 to 59% of the time; IBM's assistant is gone. Nobody combines rewrite, execution and circuit-equivalence proof. Why unfilled `[INFERENCE]`: IBM's incentive is to push users forward, not to maintain old code; academics publish taxonomies, not tools; the market is researchers who do not pay.
2. **No practitioner-facing trust layer for LLM output.** Practitioners use LLMs at 54% and distrust them past the basics; benchmarks show the dominant error is a wrong quantum state, which prints fine and runs fine. The TOSEM wish list asks for tools that "automatically validate output against known expectations" and "differentiate between classical and quantum sources of failure."
3. **Cloud-QPU reproducibility.** Users see 0.19 fidelity swings in four hours and get no drift indicator, no calibration history and no answer. I-QMapper is the only tool found, and it is a layout tool first.
4. **FT estimation and QEC onboarding** remain toil and training problems (41% cite training), but Construct, Deltakit and the vendors are moving fast here, and the physical layer is TopQAD's turf.
5. **Hardware calibration** is not a gap for Severyn: well funded vendors, closed-source drift, no reachable user.

---

## 5. Candidate wedges

### Wedge A (recommended): "Still Runs", a verified SDK-migration agent for quantum research code

- **User:** researchers and students whose 2022 to 2024 Qiskit repositories or notebooks no longer run (TOSEM 81%; Zappin 24% library/platform; the 2022 "throwaway code once the paper is published" complaint); maintainers of ecosystem packages (Mitiq hit this with `qiskit.execute()`); reviewers and reproducers (Severyn's Aquarium theme).
- **Job:** point it at a repo. It inventories deprecated calls (flake8-qiskit-migration plus the Qiskit release notes via the Qiskit Docs MCP server), rewrites with an LLM, pins an environment, runs the old code under Qiskit 1.4 and the new code under 2.5 on Aer, checks every emitted circuit for equivalence with MQT QCEC and compares output distributions, then writes a migration report with a pass or fail per circuit and a diff. The LLM never asserts correctness; QCEC and execution do.
- **Two-minute demo:** three public paper repositories from 2022 to 2023 fail on import; the agent fixes them live; the report shows "14 circuits, 14 proven equivalent, 1 behavioural change flagged (measurement order)"; a leaderboard of which model needed fewest repair rounds.
- **Reusable components (verified):** flake8-qiskit-migration (Apache-2.0, last commit 2026-02-24); MQT QCEC (MIT, 120 stars, Qiskit input); Qiskit/mcp-servers docs server (Apache-2.0, pushed 2026-10-08); Qiskit 2.0 release notes (public); qiskit-aer (Apache-2.0).
- **Data and compute:** no QPU needed; CPU simulation of small circuits. Test corpus: public repos, chosen by Severyn.
- **LLM cost:** about 5 to 20 files per repo, 1 to 3 repair rounds each, roughly $0.10 to $0.50 per file on Sonnet-class models; **$20 to $40** for the demo corpus `[INFERENCE from per-call costs in evolve-systems.md §6]`.
- **Partner-prize fit:** Eon Era (agent testing and benchmarking: the repo corpus is a benchmark, and the equivalence check is the grader); SurrealDB (store the API-change graph and migration memory); Clerk (sign-in for a hosted GitHub-Action-style service). Judge criteria: clear user, verifiable value, path to production as a GitHub Action.
- **Main way it fails:** Claude Code or Copilot already do most of the rewrite; the differentiator is only the verification layer and the migration knowledge base. Demand decays as Qiskit 2.x stabilises (until the 3.0 break). Circuit equivalence does not cover runtime semantics (primitives, options), so some "fixes" cannot be proven. Credibility gain in *quantum* is modest: this is devtools.

### Wedge B: "Drift Ledger", calibration provenance for cloud-QPU experiments

- **User:** researchers running on IBM Open or Premium plans and on IQM, Braket; the three unanswered Stack Exchange askers are the archetype.
- **Job:** a wrapper around Sampler and Estimator jobs that snapshots `backend.properties()` with timestamps, computes a drift score for the qubits used since the last calibration, flags unstable windows, stores a signed provenance record per job, and lets an LLM explain anomalies ("fidelity drop coincides with a 2× rise in readout error on q7 at 14:02"). Export a reproducibility appendix for the paper.
- **Demo:** replay the 0.692 to 0.503 GHZ case with recorded properties; show the drift flag firing.
- **Components:** qiskit-ibm-runtime (Apache-2.0); I-QMapper for heatmaps (open-source, licence unconfirmed); SurrealDB for the ledger.
- **Cost:** QPU time on the free Open plan plus about $5 of LLM.
- **Fails:** IBM could expose drift history any day; small user base; needs real QPU runs during build week; weaker AI story (the AI is an explainer, not the core).

### Wedge C: "Estimate Audit", an evidence-carrying FT resource-estimation agent

Already specified as Niche C in `quantum-ai-discovery.md` §11 and supported here by the Qualtran "months of researcher time" quote and three 2026 postings that hire people to build estimation tooling. New information from this ticket: PsiQuantum's Construct has been free since May 2026 with 100+ subroutines and a Resource Analyzer, so the wedge must be the *audit and interval* layer over Qualtran, Bartiq and Construct outputs, not another estimator. Risk remains the TopQAD overlap flagged in `field-needs.md` §5.

---

## 6. Scores for Wedge A

| Criterion | Score | Why |
|---|---|---|
| Real user with evidence of pain | 4 | 81% (n=26), 24% + 17% of 483 issues, 30 to 39% of 698 UF respondents, verbatim quotes; users exist but do not pay |
| AI makes a material difference | 4 | Rewriting across API generations needs an LLM; the moat is deterministic verification around it; benchmarks show unverified LLM repair fails 41 to 81% |
| Severyn's unfair advantage | 3 | Verification-first ethos (Aquarium) and Qiskit/Cirq fluency; not domain-unique |
| Buildable and demoable in 12 hours | 4 | Linter, QCEC, Aer and MCP docs server exist; the agent loop is glue; risk is flaky repo environments |
| Judge appeal (Georgian investors) | 3 | Clear user and production path (GitHub Action); small market; "devtools for a niche" |
| Adoption path after Oct 25 | 3 | Publish as a CLI and Action; Qiskit community and Unitary Foundation channels; demand episodic |
| Competition density (5 = open field) | 3 | Generic coding agents do the rewrite; IBM paper has no code; linter is import-only; nobody verifies |
| Credibility gain in AI and quantum | 3 | Strong on agent verification; weak on quantum depth |
| Risk (5 = low: no dual use, no 1QBit overlap) | 5 | No cryptanalysis, no physical-layer estimation, no employer overlap |

Average 3.6.

---

## 7. Sources

Surveys and studies
- Unitary Foundation, 2025 Quantum Open Source Software Survey results, Nov 2025, https://unitaryfoundation.github.io/survey-2025/ and https://unitary.foundation/posts/2025_survey_results/ (**full**, embedded data); 2024 results https://unitaryfoundation.github.io/survey-2024/ (**full**).
- Zappin, Stalnaker, Chaparro, Poshyvanyk, TOSEM (2026), https://ojcchar.github.io/files/42-tosem25-quantum-test-debug.pdf (**full**); replication https://github.com/jakezappin/Quantum_Survey_Results/.
- Zappin et al., arXiv 2411.16884 v2, Dec 2024 (**full**, stale data).
- Khan et al., arXiv 2503.05240, Mar 2025 (**full**).
- El Aoun et al., arXiv 2205.03181, May 2022 (**full**, stale).
- Heikkinen, Núñez-Corrales, Stirbu, arXiv 2607.15135, Jul 2026 (**full**; conceptual, no practitioner data, not used for conclusions).
- Riverlane 2025 QEC Survey via The Quantum Insider 2025-08-11 and Quantum Computing Report 2025-08-07 (**full**, secondary; riverlane.com blocked).
- QED-C, "Connecting the Dots", Apr 2025, https://quantumconsortium.org/publication/connecting-the-dots-quantum-learning-through-experiential-activities-and-practice/ (**full**).
- Quantum Computing Stack Exchange API, questions per year, tags, accepted and unanswered rates, question bodies #46297, #46449, #46462, #46474, queried 2026-10-22 (**full**).
- Hacker News via Algolia API: items 31976571 (2022), 46561107 and 46562980 (2026-01), 49585611 (2026-09), 31578849 (2022), 49623073 (2026-09) (**full**).
- PennyLane forum thread 9189 (2026-01-13) (**full**).

LLM tools and benchmarks
- IBM Qiskit Code Assistant docs https://quantum.cloud.ibm.com/docs/en/guides/qiskit-code-assistant (**full**); sunset announcement 2026-04-28 (**snippet-only**, 404 on fetch); Qiskit/mcp-servers README (**full**); Hugging Face cards Qiskit/granite-3.3-8b-qiskit and Qiskit/mistral-small-3.2-24b-qiskit (**full**).
- Cruz-Benito, Faro, arXiv 2605.27210, May 2026 (**full**); QuanBench arXiv 2510.16779 (**full**); QHackBench arXiv 2506.20008 (**full**); API drift arXiv 2607.04072 (**partial**); Bugs4Q arXiv 2607.09007 (**partial**); Suárez et al. arXiv 2506.14535, Jun 2025 (**abstract**); arXiv 2606.20173 (**partial**).
- Classiq press release 2026-04-23 (**full**); Bloq Maya coverage 2026-10-13/14 (**full**); pasqal-io/agent-marketplace (**full**); GitHub MCP search results (**full** metadata).
- flake8-qiskit-migration repo and commits (**full**); munich-quantum-toolkit/qcec (**full**); Qiskit 2.0 release notes and DEPRECATION.md (**full**); Qiskit, PennyLane, Cirq issue pages (**full**).

Hardware
- Yankelevich et al. (MIT, OpenAI) case study PDF, 2026-09-04 (**full**); Xu et al. arXiv 2606.22376 (**partial**); Pack, Machnes, Wilhelm arXiv 2509.08555 (**partial**); Quantum Machines calibration guide, Mar 2026 (**full** via reader proxy); APS March Meeting 2026 S07.13 (**snippet-only**); Zurich Instruments blog 2026-01-15 and laboneq repo (**full**); qua-platform/qualibrate repo and PyPI wheels (**full**); Q-CTRL Boulder Opal pages and 2025-05 release (**full**); Qruise and Conductor Quantum sites (**full**, marketing); Quantum Zeitgeist IEEE QCE26 roundup 2026-10-20 (**full**); IBM calibration-jobs guide (**full**); I-QMapper arXiv 2606.27508 and PyPI (**partial**).

Fault tolerance
- Harrigan et al., Qualtran, arXiv 2409.04643, Sep 2024 (**partial**: abstract, introduction); Nasir, Ahmad, arXiv 2610.10490, Oct 2026 (**abstract**); Ye, Palsberg, arXiv 2602.04921 (**abstract**); FTPrimitiveBench arXiv 2605.04049 (**abstract**); PsiQuantum Construct docs and 2026-05-28 announcement (**full**); job postings: IonQ, Xanadu, Alice & Bob, Quantinuum, Riverlane (5), Google Quantum AI, PsiQuantum intern, IBM Dublin (**full**); IBM Peekskill and Quandela (**snippet-only**).

---

## 8. Open questions

1. Does Wedge A survive a 30-minute test with Claude Code alone on one broken 2023 repo? If plain Claude Code fixes it and the circuits match, the only product is the verification report and the benchmark, and the pitch must say so.
2. Who is the *paying* user? Candidates: ecosystem maintainers (Mitiq, PennyLane plugins), course instructors, the Unitary Foundation (grants), IBM developer relations. None is confirmed.
3. How many public Qiskit paper repositories from 2022 to 2024 are actually broken today? A quick census of 30 repos would turn the 81% survey figure into a demo-ready number.
4. Can QCEC handle the circuit sizes in typical paper repos (tens of qubits, parameterised)? QCEC supports parameterised circuits, but scaling was not tested here.
5. For Wedge C, does Construct's Resource Analyzer already output intervals or provenance? If so, the audit layer shrinks further.
6. Reddit and the Qiskit Slack were not reachable; a 20-minute manual read by Severyn could add or remove first-person evidence, especially on debugging pain, where the only large signal is n=26.

---

End of report. This is the complete file as committed in 21d086a, pasted without revision.