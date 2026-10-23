# AI × quantum error correction: where AI helps, who needs it now, and is there a 12-hour slice?

Ticket #4 · slug `ai-qec` · researched 2026-10-22 · author: research agent (AiQec)
Read-depth labels: `full`, `partial (sections …)`, `abstract-only`, `snippet-only`, `metadata-only`. Repo facts (license, last push, stars) come from the GitHub API, queried on 2026-10-22. `[INFERENCE]` marks my own judgement. Code discovery (OmniQEC 2607.25865, IBM `qcode-discovery` 2606.02418) is already covered in `quantum-ai-discovery.md` §1, §9 and §11-B, so this report does not repeat it.

---

## 1. Bottom line

- **Verdict: no high-leverage QEC project for Severyn this weekend.** Rank this area below the options from the other tickets. AI clearly helps QEC, but in two slices: **neural decoding** and **decoder-weight calibration**. Google DeepMind (AlphaQubit 2), NVIDIA (open Ising Decoding models) and Riverlane (RL decoder calibration on H100s) own both. All three give their work to hardware teams free or through partnerships. A solo 12-hour build adds nothing to either slice that a real user would adopt.
- **Who needs AI-for-QEC now:** hardware makers and labs. NVIDIA names Infleqtion, IQM, SEEQC, Sandia, Quantum Elements, Cornell, UCSB, UChicago, USC, Yonsei and EdenCode as Ising Decoding deployers (2026-04-14). Riverlane works with "over 60%" of quantum-computer companies. These buyers are few, expert, and already supplied.
- **The only open slice is the classical tooling around QEC, not AI inside the decoder.** Riverlane's own report counts about 600–700 QEC specialists worldwide against 5,000–16,000 needed by 2030. StabilizerBench (2026-04-23) shows frontier LLM agents fail at fault-tolerant QEC circuit synthesis: capability score ≤2,830 of 16,340. So an LLM agent that runs QEC experiments only through deterministic Stim/decoder tools, behind verification gates, is defensible. The evidence that users want it is indirect, though, and Riverlane's free Deltakit already serves newcomers.
- **Best wedge if Severyn still wants QEC: "Verified QEC Lab Agent".** It is an MCP server plus a small web UI that turns a plain-language request into a gate-checked Stim memory experiment and a decoder comparison with confidence intervals, and writes a report in which the LLM never produces a number. Score: **29/45**. That is a credible portfolio piece but a weak "real user" story for Georgian judges.
- **The more distinctive but riskier alternative is "Decoder Claim Check".** It re-tests public decoder claims on Google's open hardware data. Hook: on 2026-10-22, Gix Internet put out a press release on Quantum X Labs' decoder result (12.7% fewer errors than PyMatching), saying it "has not independently verified" the result. The tool fits Severyn's verification brand, but it has few repeat users.
- **Employer risk is low** for both wedges. Neither touches magic-state factories, lattice surgery or physical resource estimation. Simulating surface-code memory sits next to TopQAD's Noise Profiler, so keep the tool at the logical-error-rate level and add no physical-qubit estimates.

---

## 2. The pain

| Who | Pain | How they handle it today | Cost of the pain | Evidence (date, depth) |
|---|---|---|---|---|
| **Hardware teams running QEC: superconducting** (Google Quantum AI, IBM, IQM, SEEQC) | Decoders must be fast (≈1 µs/cycle for superconducting qubits) *and* accurate. MWPM/PyMatching is fast but approximate; near-optimal decoders are slow | In-house neural decoders (Google AQ2) or adopting NVIDIA Ising Decoding as a pre-decoder ahead of PyMatching | AQ2-RT stays real-time only up to surface-code d=11 and colour-code d=9 on Trillium TPUs. FT algorithms need LER ≤10⁻¹⁰ per operation | AQ2 arXiv 2512.07737v2, 2026-03-11, **partial** (abstract, §1–6); NVIDIA Ising PR, 2026-04-14, **full** |
| **Hardware teams: neutral atoms** (Infleqtion Sqale) | Leakage and atom loss break the Pauli-noise assumptions decoders rely on; decoding must keep pace as readout speeds up (path to 60 µs) | Integrating NVIDIA Ising pre-decoder with the `leaky` simulator; erasure-aware decoding planned | Not quantified in the post | Infleqtion blog, 2026-04-14 (modified 2026-10-12), **full** |
| **Hardware teams: drift** (all modalities; Riverlane's customers) | Decoder weights go stale as qubits drift: "When the noise changes and the weights don't, the decoder quietly gets worse" | Periodic re-calibration. Riverlane's RL loop learns weights from experimental data; Google used prior optimisation (Sivak et al., arXiv 2406.02700) in Willow | Learned weights cut LER "from several percent to as much as a factor of two". One epoch takes 3 min on 1 CPU core vs 2.8 s on an H100. Every calibration minute is idle QPU time | Riverlane technical update, 2026-10-14, **full**; Riverlane–NVIDIA blog, 2026-10-14, **full** |
| **The QEC workforce** (whole industry; report based on 25 expert interviews incl. John Martinis) | "Severe talent gap": ≈600–700 QEC specialists today vs 5,000–16,000 needed by 2030; training can take up to 10 years. Real-time decoding is called the "critical bottleneck" | Riverlane open-sourced Deltakit (SDK + textbook, 2025-09). Riverlane and Unitary Foundation fund contributors ($2k–$4k awards; targets: "bounds for error budgeting, threshold computation, ZX graph benchmark library") | Talent scarcity slows every vendor's roadmap (the report's interpretation) | Riverlane QEC Report PR, 2025-11-19, **full** (report PDF not read); Deltakit Community Fund PR, 2026-07-28, **full** |
| **Investors / analysts reading decoder claims** | Vendor claims use different baselines and datasets, so they cannot be compared: QXL "12.7% fewer errors than PyMatching" (d=3, 10k held-out shots, Google public data); NVIDIA "3× more accurate than PyMatching"; AlphaQubit "30% fewer errors than correlated matching" | Nobody re-tests them. Gix states it "has not independently verified the technical test results reported by QXL" | Mispricing risk for retail-listed small caps (Gix: Nasdaq GIXI) `[INFERENCE]` | Gix/QXL PR, 2026-10-22, **full**; AlphaQubit blog, 2024-11-20, **full** (⚠ >18 months old); NVIDIA PR, **full** |
| **AI agents writing QEC circuits** | LLMs produce plausible but non-fault-tolerant circuits | Researchers check by hand or with Stim | StabilizerBench B3 (fault-tolerant synthesis): best capability 2,830/16,340 (Claude Opus 4.6); GPT-5.2 2,220; Gemini 3 Pro 276–1,226. B1 state prep is easy (72–80% perfect solves) | StabilizerBench arXiv 2604.21287, 2026-04-23, **partial** (abstract, §I–II, §IV tables, §VI) |

Observed facts vs. interpretation:
- Riverlane's talent-gap numbers come from a vendor and market-data firm (Resonance) that sells QEC products and intelligence. They show the vendor's framing, not a measured census.
- The drift and idle-time pain is real and recurring, but the people who feel it (QPU operators) are the customers of Riverlane, Google and NVIDIA. They are not reachable by a weekend tool `[INFERENCE]`.

**Frequency** `[INFERENCE]`:
- Decoder calibration happens "once a day" today, and Riverlane aims for "before every experiment".
- Decoder claims appear monthly: QXL announced in 2026-08 and again in 2026-10; NVIDIA in 2026-04; AQ2 in 2026-03; IonQ in 2026-09.

---

## 3. Existing solutions

| Product / tool | Owner | What it does | Users | Price / license | Read depth |
|---|---|---|---|---|---|
| AlphaQubit 1 (Nature 2024) | Google DeepMind + Quantum AI | Transformer decoder. On Sycamore: 6% fewer errors than tensor network, 30% fewer than correlated matching. Too slow for real time | Google internal | Not released (`google-deepmind/alphaqubit` → 404) | blog **full** (2024-11-20, ⚠ stale) |
| **AlphaQubit 2** (AQ2, AQ2-RT) | Google DeepMind + Quantum AI | Recurrent + transformer streaming decoder for surface and colour codes. 7.3×10⁻¹¹ LER/cycle at surface d=23. Real-time <1 µs/cycle to d=11 (surface) and d=9 (colour) on TPUs. Fine-tuned on Willow data, beats Libra | Google internal | Paper CC BY 4.0; no code found | **partial** (§1–6) |
| **NVIDIA Ising Decoding** | NVIDIA | 3D-CNN pre-decoders (0.9M / 1.8M params) that sparsify syndromes before PyMatching (surface) or Chromobius (colour). Training recipes for any noise model. ONNX/FP8 export to CUDA-Q QEC. Claims "2.5× faster, 3× more accurate" than PyMatching | Infleqtion, IQM, SEEQC, Sandia, Quantum Elements, EdenCode, 6+ universities | Apache-2.0; `NVIDIA/Ising-Decoding` 121★, pushed 2026-10-16; weights on Hugging Face | PR **full**; product page **full**; README **partial**; paper 2604.12841 **abstract-only** |
| NVIDIA Ising Calibration | NVIDIA | 35B VLM for QPU calibration plots, driven by agents. Users include IQM, Q-CTRL, Atom Computing, IonQ, Fermilab | — | Open weights (HF) | product page **full**. *QPU calibration is outside this ticket* (see the AI-calibration report) |
| **CUDA-Q QEC** | NVIDIA | GPU decoders (RelayBP, BP-OSD), real-time decoding, AI-inference hooks, QEC kernels | HPC/QPU integrators; QXL ran its decoder on it | Apache-2.0; `NVIDIA/cudaq-qec` 119★, pushed 2026-10-22 | metadata + PyPI snippet; CUDA-Q Logical PR (2026-09-14) **snippet-only** |
| **Riverlane Deltaflow** | Riverlane | Real-time QEC stack: proprietary decoder chips/FPGA (LCD decoder), integrated with Qblox and Altera | "over 60%" of QC companies (Riverlane's claim) | Commercial | press releases **full** (2025-11-19, 2026-10-14) |
| Riverlane AI decoder calibration | Riverlane + NVIDIA | Multi-agent RL learns decoder priors from experimental data; d=5 "sensor" patches; 65× faster per epoch on H100 | Riverlane customers | Commercial / research | **full** |
| **Deltakit** | Riverlane | Open SDK: code/circuit generation, noisy QPU models, Stim simulation, decoding (PyMatching + proprietary via cloud token), LEP analysis, logical-assembly compiler, textbook | Learners, researchers; unitaryHACK participants | Apache-2.0; `Deltakit/deltakit` 84★, pushed 2026-10-22; cloud features need a token | README **partial** |
| Stim + sinter | Google (Gidney) | Stabilizer simulation, DEMs, Monte Carlo sampling and decoding at scale | De facto standard in every QEC paper | Apache-2.0; `quantumlib/Stim` 836★, pushed 2026-10-20 | metadata |
| PyMatching / Tesseract / Chromobius / ldpc | Higgott; Google; Google; Roffe | MWPM; A*-search near-optimal; colour-code decoder; BP-OSD/BP-LSD | Standard baselines | Apache-2.0 (369★ / 121★ / 45★); MIT (230★). Pushed 2026-05-22 / 10-22 / 10-22 / 06-02 | metadata |
| IonQ real-time decoder | IonQ | Real-time decoding of 408 logical qubits and 31.5M ops on one CPU; 0.02% stretch | IonQ internal | Proprietary | PR **full** (2026-09-22) |
| Quantum X Labs decoder | QXL (Nasdaq-listed parent stake: Gix) | "AI-driven" decoder on CUDA-Q. 12.7% / 12.1% fewer errors than PyMatching at d=3/5 on 10k held-out Google shots | Unknown | Proprietary | PR **full** (2026-10-22) |
| EdenCode | Startup | Extends Ising pre-decoders to general Tanner graphs (qLDPC) | Unknown | Unknown | **snippet-only** (page metadata) |
| **FINAL-Bench Open Quantum Challenge** | VIDRAFT / FINAL-Bench | Public decoder leaderboard: rotated surface d=5, p=0.005 (simulated), Wilson CIs, $1,000 prize, deadline 2027-03-31. Participants are told to paste the guide into Claude Code or Codex | Small (HF Space) | Code MIT per README (no license in API); data CC-BY-NC-4.0 | README **full**; HF blog **full** (2026-10-11) |
| **StabilizerBench** | U. Washington | 192 stabilizer codes, 3 tasks (state prep, optimisation, FT synthesis) with Stim oracles; agents run through the GitHub Copilot SDK | Researchers | **No license** (`uw-math-ai/quantum-ai`, 3★, pushed 2026-09-11), so the code is not reusable | **partial** |
| QECTOR Claude plugin | G. Lessard (qector.store) | 4 MCP servers for QEC in Claude Code/Desktop; proprietary `qector-decoder-v3`; parity check `Hc = s` on every correction | 1★ | NOASSERTION; pushed 2026-08-24 | README **partial** |
| Stab | ifsheldon | Rust rewrite of Stim built "agent-native" with Codex; JSON diagnostics for agents | 0★ | MIT; pushed 2026-09-05 | README **full** |
| OmniQEC; IBM qcode-discovery | NTU; IBM | LLM-driven code discovery | Research | Closed; Apache-2.0 | see `quantum-ai-discovery.md` |

**Disconfirming evidence, collected:**
- **Decoding is well funded and open.** NVIDIA gives away models, training data and recipes. Google has published the AQ2 method, with Willow results ahead of every baseline. A solo build cannot compete on accuracy or speed, and has no GPU for training (Ising training is GPU-only; its CPU path is tests only).
- **Calibration has an owner.** Riverlane says decoder-weight optimisation is "moving from research curiosity to standard practice", with Google, NVIDIA, IBM and academic groups all working on it.
- **Agent-for-QEC tooling already exists**, though it shows no traction: QECTOR has 1 star and Stab has 0. Deltakit is the incumbent free on-ramp.
- **LLMs alone are poor at the hard part.** In StabilizerBench, a minimal prompt beat a detailed one, and more attempts *lowered* the B1 score. Value has to come from tools and verifiers, not from the model.

---

## 4. The gap

1. **No independent, real-hardware decoder comparison.** Each vendor reports against its own chosen baseline:
   - QXL compares with uncorrelated PyMatching.
   - NVIDIA compares with PyMatching and, for its larger model, correlated PyMatching.
   - AQ1 compares with correlated matching and a tensor network.
   - AQ2 compares with Libra.
   - FINAL-Bench scores only *simulated* d=5 data.
   
   Google's public data (Zenodo 13273331, CC-BY-4.0, 2024-08-26; 105-qubit Willow d=3/5/7 zip is 5.7 GB) makes a neutral "baseline ladder" possible. **Why it is unfilled** `[INFERENCE]`: vendors have no incentive, academics publish once, and the market for "decoder audits" is tiny.
2. **No verification-gated agent layer for routine QEC experiments.** Deltakit, Stim and CUDA-Q QEC are libraries. Generic coding agents write Stim code but do not check the result: they do not confirm the circuit has the requested distance, that detectors are deterministic, or that the confidence intervals are honest. StabilizerBench quantifies how often unaided agents get QEC circuits wrong. **Why unfilled** `[INFERENCE]`: experts don't need it, and Riverlane's product strategy runs through its own cloud and textbook rather than an LLM front end.
3. **Neither gap is a business by itself.** Both are open-source infrastructure plays with grant-style funding at best (Deltakit Community Fund awards of $2k–$4k). This is the main reason QEC ranks low for Georgian judges `[INFERENCE]`.

---

## 5. Candidate wedges

### Wedge A (best in this area): "Verified QEC Lab Agent", an MCP server plus web UI

- **User:**
  - Non-specialist engineers now expected to run QEC workloads. Riverlane names "HPC centres and control-system companies" as new owners of QEC compute (e.g. Qblox, Quantum Machines, HPC centres pairing GPUs with QPUs).
  - Grad students in QEC courses. Severyn has IQC ties, which gives a first test group.
  - Deltakit and unitaryHACK newcomers.
- **Job:** "Compare PyMatching, Tesseract and the Ising pre-decoder on a rotated surface code d=3–7 memory experiment under SI1000 noise at p=0.1–0.5%. Give me LER per round with CIs and a threshold estimate." The agent may act only through tools:
  1. Generate the circuit (`stim.Circuit.generated` or Deltakit).
  2. **Gate checks:**
     - DEM decomposes without error.
     - Detectors are deterministic.
     - `shortest_graphlike_error` length equals the requested d.
     - The noise parameters echo the request.
     - The shot count meets a minimum-errors target.
  3. Run sinter with the chosen decoders.
  4. Fit the threshold and compute Wilson intervals.
  5. Write a report in which every number points to a run hash.
  
  The LLM plans and explains; it never writes a number.
- **2-minute demo:**
  1. A typed request leads to a live tool trace.
  2. A deliberately bad hand-written circuit is rejected by the distance gate.
  3. The final plot and report appear.
  4. Close with a mini-eval: raw Claude writing Stim code versus the gated agent on 15 tasks, showing the verified-correct rate. This mirrors StabilizerBench's finding without using its unlicensed code.
- **Reusable components (verified):**
  - Stim + sinter: Apache-2.0, pushed 2026-10-20; sinter lives in `glue/sample`.
  - PyMatching, Apache-2.0.
  - `tesseract-decoder`, Apache-2.0.
  - `ldpc`, MIT.
  - Chromobius, Apache-2.0.
  - Deltakit, Apache-2.0.
  - MCP Python SDK: MIT, pushed 2026-10-17.
  - Optional: Ising-Decoding pre-trained surface model (Apache-2.0); CPU inference only, `[INFERENCE: feasible at d≤7, not timed]`.
- **Data and compute:** simulated only. Laptop CPU for d≤7, plus Render ($50 credit) for hosting. Cap shots per request so the hosted demo stays under about 60 s per job `[INFERENCE]`.
- **LLM cost** `[INFERENCE, assuming Sonnet-class pricing of about $3/M input, $15/M output; 2026 prices not checked]`: about 30k input and 3k output tokens per session ≈ $0.15. With roughly 200 dev and demo sessions plus the eval, the total is $30–45, within the pending $100 Anthropic credit.
- **Partner-prize fit:**
  - **Eon Era**: the mini-eval *is* agent testing against a verifier.
  - **SurrealDB**: store run lineage and the agent's memory of past experiments as a graph.
  - **Clerk**: auth for the hosted tool.
- **Main way it fails:** judges and practitioners see "a chat wrapper on Stim". Experts script this in 20 lines; newcomers already have Deltakit tutorials and Claude Code. No named user has asked for it.

### Wedge B (alternative): "Decoder Claim Check" on Google's public hardware data

- **User:** analysts and investors reading quantum press releases (Georgian's own judges), journalists (The Quantum Insider), and decoder authors who want a neutral real-data baseline.
- **Job:**
  1. Paste a claim, for example the QXL release.
  2. The LLM extracts a structured spec: dataset, d, rounds, baseline, metric, n.
  3. The harness runs a **baseline ladder** on the same public shots: uncorrelated PyMatching → correlated PyMatching → Tesseract → Ising pre-decoder + PyMatching.
  4. It reports paired differences (McNemar test) with intervals and states where the claimed result sits on the ladder.
  5. It labels the claim "reproducible baseline / not testable (decoder unreleased) / baseline mismatch".
- **2-minute demo:**
  - QXL claims 12.7% vs PyMatching, while AQ1 reported 30% vs correlated matching.
  - The tool shows how far correlated PyMatching alone moves the baseline on the same shots.
  - `[INFERENCE: not yet run; the result could go either way]`.
- **Reusable components:** the same decoders as Wedge A, plus Zenodo 13273331 (CC-BY-4.0). Download 5.7 GB once and precompute.
- **LLM cost:** under $5 (claim extraction only).
- **Prize fit:** Best Overall (investor story). Weak Eon Era fit.
- **Main way it fails:**
  - Few repeat users.
  - Most claimed decoders are unreleased, so only the baseline side can be tested.
  - Naming a listed company carries reputational and legal risk.
  - Too close to the "investor diligence" direction ruled out on 2026-10-21.

### Wedge C (do not build): decoder-prior calibration on Willow data

- **What:** an RL or gradient loop that learns PyMatching weights from Willow detection events, after Sivak et al. (2406.02700, ⚠ 2024, not read) and Riverlane.
- **Why not:**
  - The users are QPU operators already served by Riverlane, Google and NVIDIA (Ising includes a noise-learning architecture per its 2604.12841 abstract).
  - Riverlane needed an H100 to make the epochs fast.
  - It is the closest of the three to 1QBit's TopQAD Noise Profiler.

---

## 6. Scores for the best wedge (Wedge A: Verified QEC Lab Agent)

| Criterion | Score | Why |
|---|---|---|
| Real user with evidence of pain | 2 | Talent-gap figures (600–700 vs 5k–16k) and Riverlane's naming of HPC/control-system firms are indirect, vendor-sourced evidence; no named person has asked for an agent |
| AI makes a material difference | 3 | The LLM turns intent into verified tool calls and explanations, but the physics is done by deterministic tools, and StabilizerBench shows unaided LLMs fail at FT circuits |
| Severyn's unfair advantage | 4 | MSc QI (Waterloo/IQC) plus a built agent harness (Maindframe) plus experience productizing research tools; verification is his public theme (Aquarium) |
| Buildable and demoable in 12 hours | 4 | All parts are pip-installable open-source tools; d≤7 simulations run on a laptop; the main risk is UI polish, not science |
| Judge appeal (Georgian investors) | 2 | Open-source dev tooling for a niche workforce; no B2B revenue path a growth-equity fund would recognise |
| Adoption path after Oct 25 | 3 | Publish as an MCP server or Claude Code plugin; pitch threshold-computation features to the Deltakit Community Fund ($2k–$4k awards); trial with IQC students |
| Competition density (5 = open field) | 3 | Deltakit (free, Riverlane-backed), CUDA-Q QEC, QECTOR plugin and generic coding agents; none ships verification-gated agent runs, but the space is not empty |
| Credibility gain in AI and quantum | 4 | Shows agent engineering plus real QEC knowledge (distance checks, DEMs, decoders, CIs); a solid portfolio artifact |
| Risk (5 = low: no dual use, no 1QBit overlap) | 4 | No dual use; low TopQAD overlap if it stays at logical error rates with no physical-qubit or runtime estimates |
| **Total** | **29 / 45** | Credible but weak on criterion (1), the brief's top priority |

---

## 7. Sources

| # | Source | Date | Read depth |
|---|---|---|---|
| 1 | Senior et al., "A scalable and real-time neural decoder for topological quantum codes" (AlphaQubit 2), https://arxiv.org/html/2512.07737v2 | v2 2026-03-11 | partial (abstract, §1–6; Methods not read) |
| 2 | Google, "AlphaQubit tackles one of quantum computing's biggest challenges", https://blog.google/innovation-and-ai/models-and-research/google-deepmind/alphaqubit-quantum-error-correction/ | 2024-11-20 ⚠ >18 months old | full (Nature paper not read) |
| 3 | NVIDIA, "NVIDIA Launches Ising…", https://nvidianews.nvidia.com/news/nvidia-launches-ising-the-worlds-first-open-ai-models-to-accelerate-the-path-to-useful-quantum-computers | 2026-04-14 | full |
| 4 | NVIDIA Ising product page, https://www.nvidia.com/en-gb/solutions/quantum-computing/ising/ | undated, accessed 2026-10-22 | full |
| 5 | `NVIDIA/Ising-Decoding` README and API metadata, https://github.com/NVIDIA/Ising-Decoding | pushed 2026-10-16 | README partial (lines 1–300 + targeted search); metadata full |
| 6 | Chamberland et al., "Fast and accurate AI-based pre-decoders for surface codes", https://arxiv.org/abs/2604.12841 | 2026-04-14 | abstract-only (carries no conclusion) |
| 7 | NVIDIA, "NVIDIA Expands Open Source CUDA-Q Platform…", https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Expands-Open-Source-CUDA-Q-Platform-for-Fault-Tolerant-Quantum-Computing/default.aspx | 2026-09-14 | snippet-only (page metadata) |
| 8 | Riverlane, "Riverlane and NVIDIA explore faster calibration…", https://www.riverlane.com/blog/riverlane-and-nvidia-explores-faster-calibration-for-qec-with-nvidia-accelerated-computing | 2026-10-14 | full |
| 9 | Riverlane, "From Minutes to Seconds: Faster Decoder Recalibration…", https://www.riverlane.com/news/faster-decoder-recalibration-for-quantum-error-correction | 2026-10-14 | full |
| 10 | Riverlane, "Riverlane report reveals scale of the QEC challenge" (QEC Report 2025), https://www.riverlane.com/press-release/riverlane-report-reveals-scale-of-the-quantum-error-correction-challenge | 2025-11-19 | full (press release; the report itself not read) |
| 11 | Riverlane and Unitary Foundation, "Deltakit Community Fund", https://www.riverlane.com/press-release/riverlane-and-unitary-foundation-launch-deltakit-community-fund | 2026-07-28 | full |
| 12 | `Deltakit/deltakit` README, https://github.com/Deltakit/deltakit | pushed 2026-10-22 | partial (README) |
| 13 | Infleqtion, "Bringing AI-Accelerated QEC to Neutral-Atom Logical Qubits", https://infleqtion.com/blog/ai-accelerated-qec/ | 2026-04-14 (modified 2026-10-12) | full |
| 14 | EdenCode, "Scaling AI-Powered QEC with NVIDIA Ising", https://www.edencode.ai/blog-nvidia-ising | undated | snippet-only (meta description) |
| 15 | Gix Internet / Quantum X Labs press release (via Markets Insider), https://markets.businessinsider.com/news/stocks/gix-internet-quantum-x-labs-achieved-key-milestones-with-nvidia-cuda-q-decoder-and-ibm-quantum-hardware-1036654430 | 2026-10-22 | full (GlobeNewswire original returned 403) |
| 16 | IonQ, "IonQ Demonstrates Industry's First End-to-End Real-Time Quantum Error Decoder", https://www.ionq.com/news/ionq-demonstrates-industrys-first-end-to-end-real-time-quantum-error-decoder | 2026-09-22 | full (arXiv 2608.25027 not read) |
| 17 | Paz et al., "StabilizerBench", https://arxiv.org/html/2604.21287v1; repo https://github.com/uw-math-ai/quantum-ai | 2026-04-23; repo pushed 2026-09-11 | partial (abstract, §I–II, §IV results tables, §VI) |
| 18 | FINAL-Bench harness README, https://raw.githubusercontent.com/final-bench/quantum-bench-harness/main/README.md | pushed 2026-10-15 | full |
| 19 | FINAL-Bench, "The Open Quantum Challenge", https://huggingface.co/blog/FINAL-Bench/the-open-quantum-challenge-quantum-simulation-and | 2026-10-11 | full |
| 20 | QECTOR Claude plugin, https://github.com/GuillaumeLessard/qector-claude-plugin | pushed 2026-08-24 | partial (README first half) |
| 21 | Stab, https://github.com/ifsheldon/Stab | pushed 2026-09-05 | full (README) |
| 22 | Google Quantum AI, "Data for 'QEC below the surface code threshold'", https://zenodo.org/records/13273331 | 2024-08-26 ⚠ >18 months (dataset; still current) | metadata-only (file list, license) |
| 23 | GitHub API metadata: quantumlib/Stim, oscarhiggott/PyMatching, quantumlib/tesseract-decoder, quantumlib/chromobius, quantumgizmos/ldpc, NVIDIA/cudaq-qec, modelcontextprotocol/python-sdk, inmzhang/leaky, algorithmicsuperintelligence/openevolve, qiskit-community/qcode-discovery | queried 2026-10-22 | metadata |
| 24 | In-repo: `docs/research/quantum-ai-discovery.md` (OmniQEC, IBM code search), `docs/research/field-needs.md` (TopQAD overlap) | 2026-10-19 | full |

Not found, despite targeted searches on GitHub and the web: any LLM-agent product for QEC with real adoption; any independent real-hardware decoder leaderboard; any released AlphaQubit code.

---

## 8. Open questions

1. **For synthesis:** does any other ticket's best wedge score ≥30/45 with a named user? If so, drop QEC. If not, Wedge A is a safe credibility build, not a winning pitch.
2. **For Severyn:** can he name 2–3 IQC or Waterloo QEC students, or a control-systems engineer, who would try Wedge A on Oct 26–29? Without that, criterion (1) stays at 2.
3. **For Severyn:** would 1QBit see a surface-code memory simulator with decoder comparison as adjacent to TopQAD's Noise Profiler? (Confirmed: no contractual restriction. This is a positioning question only.)
4. **Unverified:**
   - Whether NVIDIA's Ising pre-trained surface model runs acceptably on Apple-silicon CPU.
   - Whether it beats PyMatching on Willow data without fine-tuning; it was trained on simulated depolarizing noise.
   - Both take about one hour to test before committing to either wedge.
5. **Unverified:** which Google dataset QXL used (the "5 rounds, d=3/5, 10,000 held-out" description fits the 72-qubit Sycamore sets better than Willow `[INFERENCE]`). Wedge B depends on matching it exactly.
6. **Not read:** the Riverlane QEC Report 2025 itself. Does it contain survey data on tool needs (e.g. "simulation tooling" or "training") that would firm up Wedge A's user evidence?
