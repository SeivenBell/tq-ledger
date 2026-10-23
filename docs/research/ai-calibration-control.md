# AI for quantum hardware calibration and control: is it a real pain an outsider can address?

Ticket #5. Research date: 2026-10-22. Read-depth labels: `full`, `partial (sections …)`, `snippet-only`. `[INFERENCE]` marks my own analysis. The sources do not state it.

## 1. Bottom line

1. **The pain is real, frequent, and expensive, but the hardware belongs to the vendors.** Concrete examples: QuEra put 4 specialists on a laser-recovery script for 2–3 weeks. MIT EQuS spends about 1 day per set of fixed-frequency qubits and about 1 week per set of tunable qubits. BAQIS estimates 18–24 expert hours for a 112-qubit bring-up. Rigetti pays $175–200k for gate-calibration engineers. Every successful demonstration in 2026 ran on hardware the authors own. An outsider gets no actuator, only simulators and one public plot dataset.
2. **In 2026 the space filled up with well-funded players.** NVIDIA released an open VLM, a benchmark and an agent blueprint (Ising Calibration, Apr/Jul 2026). Q-CTRL sells Boulder Opal Scale Up. Qruise sells QruiseOS. QuantrolOx, Quantum Machines (QUAlibrate) and Conductor Quantum (YC) also compete. Anthropic's MHS ran with QuEra, and OpenAI ran with MIT EQuS. A "calibration agent" built in 12 hours would be a weaker copy of NVIDIA's free blueprint.
3. **One gap is open and an outsider can reach it: no one publishes a closed-loop, ground-truth benchmark for calibration agents.** QCalEval scores single plots only. The BAQIS authors write that their agent and NVIDIA's model "are not directly comparable on a shared benchmark". QpiAI built a physics-grounded closed-loop environment, but I found no released code. The best-documented way agents fail is **false success**: across models, 60.7% of "suboptimal" plots are called "expected" (QCalEval), and the EQuS agent "(incorrectly) concludes that this measurement is acceptable".
4. **Best wedge: CalArena**, a fault-injected virtual QPU with a harness and leaderboard. It scores any calibration agent on parameter error, false-success rate and measurement budget. It matches Severyn's benchmark and verification profile, it fits the Eon Era (agent testing) prize, and it carries no 1QBit/TopQAD overlap.
5. **Weak point: the user.** The users of a benchmark are a few research teams (NVIDIA Ising, EQuS, BAQIS, QpiAI, Conductor), not buyers. No one has publicly asked for this artifact. NVIDIA owns the adjacent leaderboard and could ship the same thing.
6. **Verdict: calibration is not a top-1 pick unless Severyn lands a named user by Oct 25.** The two candidates are Open Quantum Design (whose `oqd-calibrator` has stalled since Sep 2024) or the NVIDIA Ising team. Rank CalArena below any option that already has a real user. Rank it above a generic "AI calibration agent".

## 2. The pain

| Who (org, role) | What happens, how often | What they do today | Cost | Source, date, depth |
|---|---|---|---|---|
| **QuEra** (Sergio Cantu, VP Quantum Systems; Takuya Kitagawa, President) | Lasers that address the atoms drift. The complex failures "resisted automation" because they need expert judgement. Every new machine generation has more lasers, sitting at customer sites further from the experts. | Before the pilot: on-site specialists "at any hour", up to 30 min per tuning session, and weeks to commission a new operating point. A hand-written script took 4 specialists 2–3 weeks and covered only the failures its authors listed. | With MHS, Claude wrote a deterministic controller. It recovered in 695/700 trials, in under 6 s for most faults versus 5–10 min for an expert. Quote: "the people driving at 2 am to fix a laser lock". | QuEra press release, 2026-08-27, `full` |
| **MIT EQuS** (Yankelevich, Grover, Oliver) | A new multi-qubit experiment "can require months and thousands of preliminary measurements". Parameters drift, and chips "exhibit stochastic behavior". | Experts calibrate fixed-frequency qubits in about 1 day and tunable qubits in about 1 week. Agents (GPT-5.6 Sol through Codex plus a Jupyter MCP) are now "routinely" used for chip characterisation. Humans stepped in on 4 of 40 measurements. | The tunable qubit needed "significant instruction". The agent wrongly accepted a bad scan. It took "several months of iteration" to find the right context for the agent. | OpenAI/MIT case study, 2026-09-04, `full` |
| **BAQIS / IOP-CAS** (Hai-Feng Yu, Pan Zhang, Lei Wang) | Scaling is "increasingly constrained by calibration complexity". Scripts are "brittle to anomalous signals". | An expert needs an estimated 18–24 h for a 112-qubit campaign. The agent (Claude Code orchestrating a fine-tuned Qwen 35B) did it in 4.7 h, with 108/112 qubits passing. | It agreed with the expert on 14/16 qubits. The agent's median T2R was 7.9 µs against the expert's 14.4 µs because it did not tune to the sweet spot. | arXiv 2606.22376, 2026-06-21, `partial (abstract, §I–VI, Supp. §VII)` |
| **Q-CTRL** customers (QuantWare, Rigetti, IonQ, Atom, Alice & Bob are listed on the page) | "Trained researchers can spend nearly all of their time just trying to find workable operating points on modestly sized devices." | They buy Boulder Opal Scale Up: under 3 h per 5-qubit feedline from a cold start. On a 21-qubit QuantWare device it "resurrected" a qubit the humans had written off. | Commercial licence, price not public. Free 30-day trial for QuantWare customers. | Q-CTRL blog, 2026-09-18, `full`; Q-CTRL blog, 2026-04-14, `full`; product page, undated, `full` |
| **Rigetti** (hiring) | Gate calibration across "hundreds of qubit pairs" with "emphasis on robustness and automation at scale". | A senior Quantum Engineer for gate calibration (PhD required). | $175,000–$200,000 per year. | startup.jobs posting, ~Aug 2026, `full` |
| **Conductor Quantum** (YC, spin qubits) | "Days of expert manual work per device." | Automated tuning of 128 double quantum dots on 64 SemiQon devices, under 1 h per device. | — | Conductor blog, 2026-04-08, `full` |
| **Open Quantum Design** (Waterloo; Roger Melko) | A 2024 roadmap item reads "Design calibration flow, 2024-09, 7M". | `oqd-calibrator` (a DAG framework with a mock device) has had no code commit since 2024-09-18; the only later commit is a licence update on 2025-08-06. A new repository, `ms-gate-design` (created 2026-10-12, updated today), uses AI agents for MS-gate design on the Bloodstone ¹⁷¹Yb⁺ apparatus and lists "calibration effort" as a tracked cost. | Unknown. [INFERENCE] The stalled repository suggests an unmet need, not proven pain. | GitHub repos and commits, checked 2026-10-22, `full` (README, commits), `partial` (roadmap, STATUS.md) |

**Can an outsider access this?** For hardware, no. All of the above ran on the authors' own rigs. MHS is a closed research preview by application. What outsiders can use:
- **QCalEval:** 243 samples (186 simulated, 57 from hardware, contributed by IQM, Conductor/EeroQ, Fermilab, Infleqtion and NPL), licensed CC-BY-4.0.
- **Open simulators:** LeeQ virtual transmons (BSD-3), the qibolab emulator (Apache-2.0), and the mock experiments in NVIDIA's blueprint (Apache-2.0).
- **OQD's open stack.**

## 3. Existing solutions

| Name | What it does | Who uses it | Price / licence | Read depth |
|---|---|---|---|---|
| NVIDIA Ising Calibration 1 / 1.5 | VLM that reads calibration plots and outputs a status, parameters and next step. Version 1.5 has 31B parameters and an NVFP4 build that runs on a DGX Spark. | Q-CTRL integration, Conductor Control API; trained on partner data from several qubit modalities | OpenMDW licence; NIM container | NVIDIA blog 2026-07-27 `full`; dev page `full` |
| QCalEval | Static VLM benchmark: 6 question types, 22 experiment families. Best zero-shot model scored 72.3. With in-context learning, Opus 4.6 reached 85.1. | NVIDIA leaderboard (updated July 2026) | Data CC-BY-4.0; scripts Apache-2.0 (`nvidia/QCalEval`, last push 2026-07-27) | arXiv 2604.25884 `partial (§1–4.2, availability)`; README `full`; HF card `full` |
| NVIDIA Quantum-Calibration-Agent-Blueprint | LangChain agent with web UI, TUI, DAG workflows and HDF5/SQLite storage. Experiments are **mocks**: seeded parameters with simulated wall-clock time. | 73 stars; issues are mostly from NVIDIA staff | Apache-2.0, last push 2026-09-23 | README `full`; 2 scripts `full` |
| Q-CTRL Boulder Opal Scale Up | Physics-informed state machine for full bring-up, with controller interpreters and a "virtual device" data store. Its vendor explicitly argues *against* "throw a big model at it". | QuantWare, Elevate Quantum Q-PAC | Commercial | `full` (3 pages) |
| Qruise QruiseOS | Automated bring-up with 40+ experiments, dashboard and on-premises install; covers SC, ion, Rydberg, NV and spin platforms | IQCC proof of concept (Apr 2026); Innovate UK testbed | Commercial; demo by booking | product page `full` |
| QuantrolOx | ML-based tuning; 2-qubit gate tuned in 25 min with Qblox and QuantWare | Quantum-Hub@MAHE (Mar 2026); AQSolotl partnership (Jun 2026) | Commercial | `snippet-only` |
| Quantum Machines QUAlibrate | Open calibration-graph framework ("hours to minutes") | OPX customers | `qualibrate-core` BSD-3, last push 2026-01-08 | press release returned 403: `snippet-only`; repo metadata verified |
| Conductor Quantum (Stanza, Coda) | Tune-up routines for spin qubits; hosted Ising agent API | SemiQon | `stanza` licence NOASSERTION, last push 2026-08-03 | docs `full`, blog `full` |
| Anthropic MHS | Standard driver for agents operating devices, with declared bounds and interlocks; MCP, CLI and API access | QuEra, Janelia, Genentech, CMU and others | Closed research preview; open-sourcing planned | `full` |
| Vibe Calibration (BAQIS) | Skills structured as decision trees with quantitative gates (R² > 0.9, ≥10 points per period, SNR ≥ 10 dB) and audit records | In-house | No code found | `partial` |
| QpiAI env (arXiv 2607.03193) | scqubits-based transmon environment with wall-time drift and planted faults; VLM agent scored against hidden truth | In-house | No code link found in the HTML | `partial (abstract + full-text keyword scan)` |
| k-agents / LeeQ (Cao et al.) | Agent state machines on LeeQ; benchmarks cover experiment recall and single-plot inspection | Oxford/NVIDIA | LeeQ BSD-3, last push 2026-09-30; issue #40 says the tutorials are broken | README `full`; arXiv 2412.07978 `snippet-only` (abstract; Dec 2024, **stale > 18 months**) |
| Cleland lab (UChicago) | LLM builds "schema-less tools" from a knowledge base; resonator characterisation and a QND reproduction | In-house | — | arXiv 2603.08801 `snippet-only` (abstract) |
| Qibocal / qibolab, LabOne Q, qiskit-experiments | Classical calibration protocol libraries; qibolab includes an emulator | TII, Zurich Instruments and IBM users | Apache-2.0; last pushes 2026-10-22, 2026-09-25, 2026-09-10 | repo metadata, file tree, issues |

## 4. The gap

1. **No public closed-loop evaluation of calibration agents.**
   - QCalEval is single-step plot QA.
   - The BAQIS paper (Supp. §VII) says its orchestration model and Ising-Cal "address different subtasks … and are not directly comparable on a shared benchmark". It also reports that NVIDIA's blueprint skills hold only "meta-procedures", with an empty Documents layer and mock data only.
   - QpiAI built the closest thing, a drift- and fault-aware simulator scored against hidden truth, but I found no released code.
   - A lab choosing between GPT, Claude, Gemini, Ising-Cal or a fine-tuned Qwen has no shared, reproducible score for the outcome that matters: did the agent leave the device correctly calibrated, and did it say so honestly?
2. **False success is the failure mode that matters, and no one measures it end to end.** The evidence:
   - QCalEval reports "optimistic bias" (60.7%).
   - The EQuS agent accepted a bad scan.
   - QuEra's headline claim is that its controller "never reported success when it had not succeeded".
   - Vibe enforces write-back gates by hand.
   - Qibocal issue (2026-10-13): "Chevron fit results can be applied to the wrong qubit pair".
3. **Why nobody has filled it** [INFERENCE]:
   - The groups with hardware publish wins on their own rigs, and a public benchmark would expose their agents' failure rates.
   - NVIDIA's priority is selling models and GPUs, so a static plot benchmark serves that purpose.
   - Vendors such as Q-CTRL have a commercial reason to argue that LLM agents are unreliable, not to measure that.
   - The closest teams (BAQIS, QpiAI) built private environments for their own papers.

**Strongest reason the gap does not matter.** Q-CTRL's position is that calibration needs deterministic, physics-encoded state machines, with AI confined to narrow inference tasks. If buyers agree, a leaderboard of general-purpose agents measures something that no one deploys. A counterpoint from QuEra: the agent's output was a deterministic program, so agents can serve as *authors* of state machines, and that use also needs evaluation.

## 5. Candidate wedges

### A. CalArena: closed-loop, fault-injected benchmark for calibration agents (recommended within this area)

- **User:** teams that choose or build calibration agents.
  - The NVIDIA Ising team (Shuxiang Cao, research scientist; Tom Lubowe, senior PM), who maintain QCalEval and the blueprint.
  - Lab users such as EQuS.
  - The BAQIS and QpiAI authors.
  - Conductor Quantum.
  - Note: no buyer.
- **Job:** "Before I let an agent touch my fridge, tell me which model and harness calibrates correctly, cheaply, and *admits failure*."
- **2-minute demo:**
  - A virtual 4-qubit transmon chip with hidden ground truth.
  - Faults are switched on: resonance outside the scan window, low SNR, a TLS defect that dips T1, a 2-photon peak that looks like f01, an undersampled Rabi scan, a dead qubit, and mid-run drift.
  - Claude and one other model run the same tune-up through MCP-style tools (spectroscopy, Rabi, Ramsey, T1, `write_param`, `declare_done`).
  - A live replay shows the plots each agent saw and each write-back.
  - Leaderboard columns: parameter error versus truth, **false-success rate**, measurements used, and bound violations.
  - Last step: switch on a simple gate (the Vibe-style R² and points-per-period checks) and show the false-success rate fall.
- **Reusable components (verified 2026-10-22):**
  - NVIDIA blueprint mock-experiment pattern (Apache-2.0, 2026-09-23).
  - LeeQ numpy virtual device (BSD-3, 2026-09-30) as the source of physics formulas.
  - QCalEval family definitions and status vocabularies (CC-BY-4.0) for naming fault classes.
  - Severyn's own Gymnasium harness pattern from Maindframe; that code predates build week, so disclose it and rewrite.
- **Data and compute:** all synthetic numpy, CPU only, on a Render web service with a static leaderboard.
- **LLM cost** [INFERENCE]:
  - About 30 tool calls per episode, each carrying one plot image, gives roughly 0.3–0.6M input tokens per episode.
  - At Sonnet-class prices that is about $1–2 per episode.
  - 3 models × 10 scenarios ≈ $30–60, which fits the $100 Anthropic credit only if non-Anthropic models run on their free tiers or the matrix shrinks.
- **Partner-prize fit:** Eon Era (agent testing and benchmarking) is a direct fit. SurrealDB works for episode traces and "device notes" memory (QpiAI's reflector idea). Clerk can gate leaderboard submissions.
- **Main way it fails:**
  - The fault models look naive to experimentalists, which would make the benchmark easy to dismiss.
  - No external team submits an agent.
  - NVIDIA ships "QCalEval-Agent" first.

### B. Reviving OQD's calibrator: an agent-driven calibration DAG for a trapped-ion testbed

- **User:** Open Quantum Design (Waterloo), specifically the Bloodstone ¹⁷¹Yb⁺ team and Roger Melko, whose group already works with AI agents in `ms-gate-design`.
- **Job:** finish what `oqd-calibrator` started (DAG of parameters, a mock device with Brownian drift, a DB). Add an agent that plans, runs and gates each node, plus an audit log.
- **Demo:** DAG view in which nodes turn green as the agent calibrates a mock ion chain; drift is injected and the agent re-runs only the nodes that depend on it.
- **Reuse:** `oqd-calibrator` (Apache-2.0, last push 2025-08-06) and `oqd-core`/`oqd-trical` (Apache-2.0, pushed 2026-10).
- **Cost:** under $20 of LLM spend [INFERENCE].
- **Prize fit:** SurrealDB, as a calibration-state graph.
- **Main way it fails:**
  - No evidence that OQD wants this now (the repository is stalled, and no issue asks for it).
  - No remote hardware access.
  - Physically credible ion-calibration mocks would take Severyn most of the 12 hours.
- **Upside:** Severyn's ex-OQD relationship gives the only route in this whole area to a *named* user in 72 hours.

### C. Guarded write-back layer for calibration agents

- **User:** people running NVIDIA's blueprint or any MCP calibration agent.
- **Job:** an MCP server that sits between the agent and the device config store. It enforces declared bounds, fit-quality gates (R², points per period, SNR), physics consistency checks (T2 ≤ 2T1, Rabi period ratio, f01 within the design band) and an append-only audit trail. This mirrors MHS "declared bounds" and Vibe's gates.
- **Demo:** the same agent with and without the guard, using QCalEval plots and blueprint mocks; bad write-backs are blocked and logged.
- **Reuse:** blueprint (Apache-2.0) and QCalEval (CC-BY-4.0).
- **Prize fit:** strong on the Security and Ethics criterion.
- **Main way it fails:** Q-CTRL and Anthropic MHS already ship this concept inside their stacks. The real write-back happens inside each lab's own orchestration software, which no outsider can reach.

## 6. Scores for the best wedge (A: CalArena)

| Criterion | Score | Why |
|---|---|---|
| Real user with evidence of pain | 2 | Calibration pain is well evidenced. Pain about the *missing benchmark* is inferred from BAQIS's "not comparable" remark and the false-success evidence; no team has asked for it, and the blueprint has few external users. |
| AI makes a material difference | 3 | The project evaluates AI agents and does not depend on AI itself. The headline output (false-success rates of frontier models) only exists because agents are now operating hardware. |
| Severyn's unfair advantage | 4 | Background: Gymnasium agent harness, multi-agent anomaly benchmark, Aquarium's verification ethos, an MSc in quantum information, ML work on OQD ion images. Not a superconducting experimentalist, so the fidelity of the fault models is the exposed flank. |
| Buildable and demoable in 12 hours | 4 | Numpy device with 6 experiments and 7 fault types, an MCP-style tool harness, scoring and a static leaderboard are all plain Python and web work. The risk is wall-clock time for agent runs. |
| Judge appeal (Georgian investors) | 3 | "Who audits the AI running a $10M machine?" lands with Deval Pandya (Vector) and the CTO. A benchmark is not a B2B business, which costs it with Margaret Wu. |
| Adoption path after Oct 25 | 2 | Open-source it, propose it to NVIDIA as a closed-loop extension of QCalEval, invite the BAQIS and QpiAI authors. Every step depends on others choosing to engage. |
| Competition density (5 = open field) | 3 | No public closed-loop benchmark was found, but NVIDIA, QpiAI and BAQIS each hold most of the parts and could publish quickly. |
| Credibility gain in AI and quantum | 4 | Puts Severyn at the 2026 intersection of NVIDIA, Anthropic and OpenAI with a measurable, citable artifact in his verification niche. |
| Risk (5 = low: no dual use, no 1QBit overlap) | 5 | Simulation only, no hardware control, no overlap with TopQAD (FT resource estimation). |

Total 30/45. [INFERENCE] This is competitive only if another ticket fails to produce an option with a named user.

## 7. Sources

| Source | URL | Date | Read depth |
|---|---|---|---|
| QuEra press release, AI automates laser subsystem | https://www.quera.com/press-releases/quera-computing-uses-ai-to-automate-a-critical-quantum-computer-subsystem-enabling-the-acceleration-of-commercial-grade-quantum-computing-deployments-from-quera | 2026-08-27 | full |
| Anthropic, Previewing the Model Hardware Standard | https://www.anthropic.com/news/model-hardware-standard-research-preview | 2026-08-27 (mod. 2026-10-13) | full |
| OpenAI/MIT EQuS case study | https://cdn.openai.com/pdf/case-study-agentic-calibration-of-superconducting-qubits.pdf | 2026-09-04 | full |
| QCalEval paper, arXiv 2604.25884 | https://arxiv.org/html/2604.25884 | 2026-04-28 | partial (abstract, §1–4.2, limitations, availability) |
| QCalEval scripts README | https://github.com/nvidia/QCalEval | last push 2026-07-27 | full (README) |
| QCalEval dataset card | https://huggingface.co/datasets/nvidia/QCalEval | 2026-04-08 | full |
| NVIDIA Ising developer page | https://developer.nvidia.com/ising | accessed 2026-10-22 | full |
| NVIDIA blog, Ising Calibration 1.5 | https://developer.nvidia.com/blog/nvidia-ising-enables-fully-automated-quantum-computer-calibration-with-enhanced-in-context-learning/ | 2026-07-27 | full |
| NVIDIA Quantum-Calibration-Agent-Blueprint | https://github.com/NVIDIA/Quantum-Calibration-Agent-Blueprint | last push 2026-09-23 | partial (README, `scripts/rabi_oscillation.py`, `scripts/qubit_params.py`, tree, issues) |
| Vibe Calibration, arXiv 2606.22376 | https://arxiv.org/html/2606.22376v1 | 2026-06-21 | partial (abstract, §I–VI, Supp. §VII) |
| QpiAI, arXiv 2607.03193 | https://arxiv.org/abs/2607.03193 | 2026-07-03 | partial (abstract; keyword scan of HTML) |
| k-agents, arXiv 2412.07978 | https://arxiv.org/abs/2412.07978 | 2024-12-10 (**stale**) | snippet-only (abstract) |
| Cleland lab, arXiv 2603.08801 | https://arxiv.org/abs/2603.08801 | 2026-03-09 | snippet-only (abstract) |
| Q-CTRL autocalibration page | https://q-ctrl.com/technology/quantum-computer-autocalibration | undated | full |
| Q-CTRL blog, calibration autonomous | https://q-ctrl.com/blog/making-quantum-computer-calibration-autonomous-informative-and-easy | 2026-09-18 | full |
| Q-CTRL blog, physics-informed AI and NVIDIA Ising | https://q-ctrl.com/blog/scaling-quantum-autonomy-with-nvidia-ising | 2026-04-14 | full |
| QruiseOS product page | https://www.qruise.com/products/qruise-os | undated | full |
| QuantrolOx news | https://quantrolox.com/news-aqsolotl-and-quantrolox-partner-to-automate-quantum-control-targeting-scalable-production-ready-systems | 2026-06-24 | snippet-only |
| QUAlibrate press release | https://www.quantum-machines.co/press-release/quantum-machines-launches-qualibrate-an-open-source-framework-that-cuts-quantum-computer-calibration-from-hours-to-minutes/ | 2025-05-19 | snippet-only (403) |
| Conductor Quantum agents docs | https://docs.conductorquantum.com/control/agents/nvidia-ising-calibration.md | undated | full |
| Conductor Quantum blog, 64 devices | https://blog.conductorquantum.com/p/128-double-quantum-dots | 2026-04-08 | full |
| Rigetti Senior Quantum Engineer, Gate Calibration | https://startup.jobs/senior-quantum-engineer-gate-calibration-rigetti-8996995 | ~2026-08 | full |
| OQD `oqd-calibrator` | https://github.com/OpenQuantumDesign/oqd-calibrator | last code 2024-09-18; last push 2025-08-06 | full (README, commits, tree) |
| OQD roadmap | https://github.com/OpenQuantumDesign/roadmap | 2024-07 (**stale**) | partial |
| OQD `ms-gate-design` | https://github.com/OpenQuantumDesign/ms-gate-design | 2026-10-22 | partial (README, STATUS.md) |
| LeeQ | https://github.com/ShuxiangCao/LeeQ | last push 2026-09-30 | full (README), issue #40 |
| Qibocal issues | https://github.com/qiboteam/qibocal/issues | 2026-10 | partial (titles) |
| Repo metadata via GitHub API (licence, last push): qibolab, laboneq, qiskit-experiments, qualibrate-core, conductorquantum/stanza | github.com | checked 2026-10-22 | metadata only |
| Existing reports: `field-needs.md`, `quantum-ai-discovery.md` | this repo | 2026-10-19+ | partial (keyword scan) |

## 8. Open questions

1. **Can Severyn get a yes from a named user by Oct 25?** Either Roger Melko or the OQD Bloodstone team for wedge B, or Shuxiang Cao or Tom Lubowe (NVIDIA Ising) for "would you link or adopt a closed-loop QCalEval extension?" for wedge A. Without one, this area loses to any option that has a user.
2. **Will QpiAI release its 2607.03193 environment?** If it is or will be public, wedge A becomes a thin wrapper. An email to the authors would settle it.
3. **Fault-model credibility:** can Severyn get 30 minutes from an IQC superconducting or ion experimentalist to sanity-check the 7 fault classes before the demo?
4. **Positioning:** does a benchmark showing "frontier agents falsely claim success X% of the time" conflict with Severyn's use of Anthropic credits or partner relationships? I think not, since it is model-neutral [INFERENCE].
5. **Synthesis:** does another ticket (for example AI-for-QEC or resource claims) offer a verification artifact with a more direct user? If so, reuse CalArena's "false-success audit" framing there instead of building it here.
