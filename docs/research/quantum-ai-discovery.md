# Quantum-specific LLM/agent discovery papers (2025–2026): landscape around arXiv 2610.22367

Compiled 2026-10-19. Read-depth labels: `full`, `partial (sections …)`, `abstract-only` (unverified). Repo checks used the GitHub API on 2026-10-19. Text marked [INFERENCE] is my own judgement, not something a paper states.

---

## 0. Reference point: 2610.22367, Gu, Kemeny, Yelin, Lukin (Harvard/Anthropic/QuEra), "Discovering state-of-the-art quantum circuits with LLMs"
**Read depth:** partial (abstract, "Design principles", "Discussion and outlook", Table 1, all Methods subsections: circuit model, validation, cost model, evolutionary search; Extended Data task table). I did not read the DQI and modular-inversion sections or the SI.

- **Task:** compile classical functions into reversible circuits, |x⟩|y⟩ → |x⟩|y⊕f(x)⟩. Eight tasks: a Reed–Solomon DQI decoder, a Hermitian-code DQI decoder, the HHL rotation angle, a Coulomb potential, a fixed-point Gaussian, Fe2S2 alias–Select (QROM), a nonabelian lattice-gauge step, and prime-field modular inversion.
- **Method:** OpenEvolve with **Claude Mythos 5**. Each candidate is a Python program that builds the circuit through a generic circuit-building interface. An ideation stage proposes several algorithm families (for example Euclid, Berlekamp–Massey, PGZ). Each family evolves separately, and the best candidates are shared across families from time to time. Archive: MAP-Elites over the (Toffoli count T, qubit count Q) plane. Every iteration starts a fresh agent session. The session can run drafts, query a classical oracle and use subagents. Lineage, short insight notes and failure feedback are carried between sessions. Search starts from a blank program and runs without substantive human intervention.
- **Evaluator:** a "kickmix" circuit model (Babbush et al.). Allowed operations are X/CNOT/Toffoli/swap, Z/CZ/CCZ and destructive X-basis measurement (measurement-based uncomputation). The simulator tracks only a bit string and a sign, so it is classically cheap. Each check verifies the output, that inputs are unchanged, that every ancilla returns to |0⟩, and the **exact phase**. If k random trajectories all pass, then ε ≤ ln(1/δ)/k, and state fidelity ≥ (1−2ε)². Tasks used 10⁵ tests (9·10³ for the numerical tasks, 2·10⁷ for Fe2S2). Some tasks allow a failure budget of ≤10⁻³ or ≤2·10⁻⁴.
- **Metric:** TQ = Toffoli count × peak qubit count. The paper states that this choice is arbitrary: Q^κ·T with κ = 1–3, Toffoli depth or active volume are all reasonable alternatives.
- **Results (Table 1):** RS-DQI decoder (5.1e6 T, 1938 Q) → (4.4e5, 1837), G_TQ = 12. HHL angle G = 32. Coulomb G = 9.9. Gaussian G = 39. Fe2S2 G = 4.1. Lattice gauge G = 7.7. Hermitian DQI: 1.0e8 → 9.3e5 Toffolis, but the baseline is a naïve reversible implementation. Modular inversion: a new divstep architecture at (4.0e6, 935), with no comparable baseline.
- **Compute/cost:** not reported in the sections I read. **Code:** no code-availability statement found in the main text or Methods, and the search found no repo → treat as **not released**.
- **Stated limits:** the objective is hand-chosen. The interface uses a fixed computational basis, so it excludes changes of encoding such as coset representations. Task boundaries and input distributions are fixed by hand.
- **Unstated limits [INFERENCE]:** the evaluator checks correctness only statistically on large domains. The paper offers no human-hour or API-cost comparison and no ablation of the LLM against non-LLM search. The objective ignores routing, connectivity and magic-state factory throughput, although the paper raises this in its discussion.

---

## 1. 2607.25865 OmniQEC: discovering practical QEC codes by an AI scientist (NTU / CityU HK / Foxconn)
**Read depth:** partial (the HTML main text in full: §I–IV including setup, scaling, validation, ablation and cost). The SI (A–D: code families, tool details, p_LER definition, family analysis) is not in the HTML and was not read.

- **Task:** discover qLDPC codes under a fixed **total** physical-qubit budget N (data + ancilla). The objective is circuit-level logical error rate (LER) per round per logical qubit, not [[n,k,d]].
- **Method:** an LLM orchestrator keeps a discovery memory and coordinates two loops:
  - **Fast loop:** a code-search agent writes construction programs (rule + parameters). Each iteration produces 24 programs × 20 seeds, so up to 480 code instances. These are screened by validity (H_X H_Zᵀ = 0), k, d (estimated with BP+LSD/OSD) and Φ = kd²/n.
  - **Slow loop:** syndrome-extraction circuits are scheduled by edge-colouring the Tanner graph and compiled to Stim. A detector error model is sampled and decoded with BP+OSD (BP+LSD and Relay-BP are also integrated) under depolarizing noise at p = 0.005.
  - Run settings: T = 60 iterations; 14 budgets from N = 20 to N = 288; 4 families (BB, trivariate-bicycle, lifted-product, generalized LP).
- **Models:** Claude Opus 4.8, GPT-5.5 and DeepSeek-V4-Pro, each tried as the orchestrator.
- **Baselines:** BB [[72,12,6]] (N = 144) and [[144,12,12]] (N = 288), evaluated with **OmniQEC's own** edge-colouring schedule and decoder ("identical syndrome-extraction and decoding protocols"), not IBM's published hand-optimised circuit.
- **Results:**
  - All three backends beat BB-72 from N = 98. Claude and GPT beat BB-144 at N = 240; DeepSeek never does.
  - Across p ∈ [0.002, 0.01] the best code has an LER 29.2× lower than BB-72 at p = 0.002 and 1.66× lower at p = 0.01.
  - Fitted slope Γ: 5.2–5.6 for the discovered codes ([[48,4,8]] from GPT, [[58,2,7]] from Claude) vs 3.79 for BB-72.
  - **The Φ proxy mis-ranks codes.** At N = 144 the winners have Φ = 2.25, 5.56 and 3.36, while BB-72 has Φ = 6.
- **Ablation (most useful finding):** final top-5 suppression −log₁₀ p_LER:

  | Variant | Claude | GPT | DeepSeek |
  |---|---|---|---|
  | Full workflow | 4.61 | 5.17 | 4.07 |
  | Proxy-only (no slow loop) | 2.14 | 3.20 | 0.84 |
  | No feedback at all | 3.86 | 4.25 | 2.83 |

  **Proxy-only feedback does worse than no feedback**: optimising the cheap proxy actively steers the search toward circuit-level-poor codes.
- **Cost:** token usage and $ appear only in Fig. 4, with no numbers in the text. The paper says Claude has the best cost/performance and DeepSeek is cheapest but weakest. Circuit-level evaluation takes "minutes to hours" per candidate.
- **Code:** **none found** (no statement in the paper; a GitHub search found nothing).
- **Stated limits:** circuit-level evaluation is the bottleneck. Only the orchestrator and search agent are LLMs; the other modules are fixed tools. Results cover memory experiments only. Calibration-aware (per-device) co-design is listed as future work.
- **Unstated limits [INFERENCE]:**
  - Normalising LER per logical qubit favours small-k codes; the winners have k = 2–4 vs k = 12.
  - The BB reference uses a generic edge-colouring schedule, which likely handicaps it relative to its best-known circuit.
  - Search ran at a single p.
  - No variance is reported across repeated campaigns.

## 2. 2602.19387 AI Agents for Variational Quantum Circuit Design (U. Alabama)
**Read depth:** partial (§1–6 in full). Appendices A (tool docstrings) and B (full Claude transcript) were not read.

- **Task:** design the VQC inside a fixed QNN on a toy problem: predicting the position of a 1-D Gaussian peak. Data: 21 points per sample; 150 train, 250 validation and 500 test samples. Three architectures: Simple QNN, Quanvolutional NN and Full-quantum QNN. There is also an external benchmark, a Lie-equivariant quantum GNN for jet tagging.
- **Method:** one agent built on the Orchestral AI framework. It writes PennyLane QNode code into a tool (`TrainCustom…Tool`). The tool trains with AdamW and returns test RMSE, gate count and parameter count. The full history stays in context, and a human intervenes between rounds.
- **Models:** Claude 3.7 Sonnet and Llama 3.3 70B.
- **Results:**
  - Simple QNN: Claude's best RMSE is 0.0326 (9 qubits, data/compute qubit split, star entangler). Llama's best is 0.021 with 48 parameters.
  - Full-quantum: 0.081, but the circuit has depth 1659 and 4189 gates.
  - Quanv: 0.133, with no clear trend.
  - Lie-EQGNN: AUC ≈ 0.734.
- **Baselines:** none. There is no comparison against hand-designed ansätze, random search or classical models, and each setting is a single run.
- **Evaluator:** test RMSE from simulator training. It includes no noise and no hardware.
- **Code:** no repo cited.
- **Stated limits:** invalid code; context loss ("lost in the middle"); exploration collapse; toy task; simulation only.
- **Unstated limits [INFERENCE]:**
  - Human steering confounds the claim of autonomy.
  - Results are single-seed, and there are no baselines.
  - Claude kept dead gates after the measurement: the agent added layers that do not affect the measured qubits and did not notice (the paper states the observation).

## 3. 2606.13380 An LLM System for Autonomous VQC Design ("Astronaut", Osaka: Sakka, Mizukami, Mitarai)
**Read depth:** partial (§I–VII; App. A.1–A.3.4). The generated-circuit appendices C and D and analysis B were not read.

- **Tasks:**
  1. Quantum-kernel feature maps for SVM classification. MNIST, reduced by PCA to 80 dimensions, is used during search; Fashion-MNIST and CIFAR-10 are used only for final testing.
  2. Hardware-efficient VQE ansätze with O(N²) gate and parameter scaling for H₂, H₄, H₆, LiH, BeH₂, H₂O and N₂ (STO-3G, Jordan–Wigner, 10 bond lengths each).
- **Method:** seven components:
  - **Exploration:** a deep-research report from o3-deep-research, then seed ideas pruned from 10 to 5 to 2.
  - **Generation:** GPT-5.
  - **Discussion:** critic, domain-expert and advocate roles, using retrieval over 2,785 quant-ph papers embedded with text-embedding-3-small.
  - **Validation:** static checks against 385 LLM-generated PennyLane 0.39 class documents, plus dynamic execution.
  - **Evaluation**, **Review** and **Storage**.
  - Run settings: 15 trials. Validation uses gpt-5-mini; summaries use gpt-5-nano.
- **Evaluator:**
  - Feature maps: exact statevector kernels on lightning.qubit, scored by SVM accuracy.
  - VQE: lightning.gpu with SLSQP, measuring mean |E_exact − E_VQE| against FCI or CASCI. Each evaluation is a single optimisation with one seed.
- **Results:**
  - Feature maps: on MNIST, 0.9772 at 10 qubits and 0.9767 at 14 qubits, vs RBF 0.9765 and YZCX 0.9727. On CIFAR-10 at 14 qubits, 0.5734 vs RBF 0.5669.
  - VQE: mean error 6.4·10⁻³ Ha, which is **above** chemical accuracy (1.6·10⁻³ Ha). The ansatz beats Particle-U1/U2, is worse than GateFabric, and beats UCCSD only at stretched BeH₂, H₂O and N₂.
  - Ablation (5 runs each): Exploration and Discussion help, and the authors call this "preliminary".
- **Compute/cost:** API cost is not quantified.
- **Code:** github.com/Qyusu/astronaut (**MIT**, exists, last push 2026-05-11) and Qyusu/astronaut-artifact (MIT).
- **Stated limits:**
  - Symmetry criteria for particle number and spin were given only as text and were "not consistently satisfied".
  - Results are noiseless only.
  - The authors find the generated circuits hard to interpret.
- **Unstated limits [INFERENCE]:**
  - On MNIST the "beats RBF" margin is 0.0002–0.0007, inside the stated ±; only CIFAR-10 at 14 qubits shows a clear gap.
  - The task is PCA-80 SVM classification, where quantum advantage is not expected.

## 4. 2607.25834 Pasqal: Lowering the implementation barrier of neutral-atom QC with agentic workflows, plus the Neutral-Atom Agentic Toolkit
**Read depth:** full main text, App. A, and App. B rules. Also read: the toolkit landing page (pasqal.com/neutral-atom-agentic-toolkit) and docs.pasqal.com/agentic-toolkit.

- **Task:** take a paper, patent or idea through an experiment spec, a Pulser pulse sequence, MPS emulation, submission to a real QPU (FC1 in Sherbrooke, SA1 in Saudi Arabia) and analysis.
- **Method:** Claude Code (Opus 4.8 and "Fable 5") plus 6 skills: paper_to_spec, spec_to_sequence, validate_emu (emu-mps with the live device noise model), noise_emulate (40 quantum-jump trajectories), qpu_submit (with calibration) and harvest_and_analyze. All skills share one `experiment_spec.json`.
- **Results:**
  1. **Keesling 2019 reproduction:** the agent correctly rejected Z₃ as infeasible (Ω/2π would need to be 0.087 MHz) and ran Z₂ on a 56-atom ring (FC1) and a 96-atom ring (SA1). Correlation length ξ = 4.2 vs the paper's 3.9. Took 3 prompts and less than 1 h to the first QPU job. Switching to a ring register came from the human.
  2. **Triangular-lattice phases (Guo et al.):** feasibility verdicts were correct, but the agent chose the wrong observable (mean magnetisation instead of staggered |m|). It took **43 exchanges** to reach a correct implementation; the 1/3 plateau was observed at N = 49 and N = 100.
  3. **Patent graph colouring (IS peeling):** 75 unit-disk graph instances with N = 15–80. Exact χ at N = 20; mean gap 0.84; gap ≤ 2 everywhere. The agent blamed blockade leakage for violating shots; the true cause was a **qubit-ordering bug**.
  4. **Corpus triage:** 633 Rydberg theory papers screened; 526 classified with a 5-rule decision tree; 258 (49%) judged implementable today. Of the rest, XY interactions (141) and local addressing (87) are the main blockers.
- **Evaluator:** comparison with noiseless and noisy emulation, plus a human expert. There is no automatic correctness signal for "right physics".
- **Code:** github.com/pasqal-io/agent-marketplace (**Apache-2.0**, exists, pushed 2026-10-08). Works with Claude Code, Codex, Cursor, Gemini CLI and others. Each example sequence self-tests against analytically known states. **Two rules are enforced in scripts:** shot-count approval before spending, and refusal to bill a project the user did not name. "Emulate before QPU" is only a prompt instruction.
- **Stated limits:** the agent narrows onto the easiest observable, invents plausible but wrong physical stories, and needs an expert in the loop.
- **Unstated limits [INFERENCE]:**
  - Corpus classifications were not human-audited (only "auditable" citations are stored).
  - Model and cost per experiment are not quantified.

## 5. 2601.10194 Autonomous Quantum Simulation through LLM Agents (Renormalizer, Shuai group)
**Read depth:** partial (Results, Discussion, Methods in full). The SI (prompts, transcripts) was not read.

- **Task:** run tensor-network (MPS: DMRG/TDVP) simulations autonomously on three problems:
  1. 2D transverse-field Ising, 8×8, with open vs periodic boundaries.
  2. The sub-Ohmic spin-boson dynamical phase diagram.
  3. A two-state, 25-mode retinal photoisomerization model, which needs an exponential-DVR basis.
- **Method:** LangChain. A Conductor coordinates 7 agents (Strategist, Guide, Programmer, Executor, Aggregator, Validator, Visualizer). About 43k tokens of curated Renormalizer documentation sit in the prompt. Three configurations were compared: baseline, single agent + docs, and multi-agent + docs.
- **Models:** DeepSeek-V3.2 (with reasoning), Gemini 2.5 Pro and Claude Opus 4.5.
- **Evaluator:** **authors grade each run 0–10** with a rubric. Five runs per task per configuration.
- **Results:**
  - Multi-agent DeepSeek: mean 9.47, 87% perfect runs.
  - Gemini: baseline 0.87 → multi-agent 8.13.
  - Claude's failures are mostly malformed-response errors.
  - Token use: ~10M input tokens per task. Cost: about $2–3 per task for DeepSeek or Gemini, $20–30 for Opus 4.5.
- **Failure modes:** declaring a task finished prematurely, running with bond dimension 1, and unit/sign errors. Without reasoning, the Validator hallucinated that "energy should increase with h".
- **Code:** Renormalizer (Apache-2.0, exists). The agent code and logs will be released "upon publication", so **not yet released**.
- **Unstated limits [INFERENCE]:** human-graded rubric; small n; all three tasks have known reference answers.

## 6. 2604.08318 MCP server for quantum execution in hybrid quantum-HPC (ABCI-Q, AIST)
**Read depth:** full.

- **Task:** take a natural-language prompt, have the LLM write OpenQASM 2.0, and run it through an MCP tool on CUDA-Q (H100 nodes via PBS batch jobs) or the Quantinuum H2-1E emulator (REST API, asynchronous).
- **Model:** local NVIDIA Nemotron 3 Nano (31.6B MoE, 3.6B active, 4-bit, Ollama on CPU). The local model is used for data sovereignty.
- **Results:**
  - 3-qubit GHZ: 6/8 runs succeed; both failures are malformed JSON.
  - QAOA triangle MaxCut at fixed (γ, β): ⟨H⟩ = 0.0299 in 5/5 runs.
  - Latency is about 107–192 s per job and is dominated by PBS scheduling, with a floor of about 42 s.
- **Inconsistency:** the Fig. 2 console shows 1040/960 GHZ counts, but the text reports 996/1004.
- **Code:** the server code is **not released** (only CUDA-Q is cited).
- **Assessment [INFERENCE]:** this is execution plumbing with trivial tasks and no discovery loop. Amazon Braket already ships an MCP server, per the paper.

---

## 7. Other 2025–2026 papers found: triage

| arXiv | What | Relevance | Depth |
|---|---|---|---|
| **2603.29894** LLM-guided evolutionary search for algebraic T-count optimisation (VarTODD + GigaEvo) | LLM evolves the *tuner/policy* around a fixed, verified algebraic core | High: same "LLM + independent verifier" pattern, applied to a FT compiler pass | **deep-read, §8** |
| **2606.02418** IBM: evolutionary discovery of bivariate-bicycle codes with LLM-guided search | OpenEvolve over generator ansätze; MILP-certified distance | High: open code; quantifies how proxies fail | **deep-read, §9** |
| 2606.13811 IBM: Aligning quantum operators with LLMs | Maps unitaries into the LLM latent space; trained model for Clifford+T synthesis; language-conditioned constraints | Medium (needs training) | abstract-only (unverified) |
| 2610.10490 Nasir & Ahmad: standard estimators cannot represent FT workloads at measured error rates | Not LLM. Propagates evidence-based priors through 5 surface-code cost models (RSA-2048, ECC-256, AES-256, Hubbard); argues single-number resource estimates are invalid | High for the resource-estimation niche | abstract-only (unverified) |
| 2609.20258 Protocol-guided LLM agent for quantum program synthesis and execution | YAML protocol plus evaluator-guided repair; VQE-H₂, QAOA and kernel tasks; 240 trials; completion 80% → 99.2% | Low–medium (NISQ codegen) | abstract-only (unverified) |
| 2602.03466 Test-time learning circuit generation | Memory-augmented LLM optimiser maximising the Meyer–Wallach entanglement of 20–25-qubit circuits | Low (toy objective) | abstract-only (unverified) |
| 2604.08570 QuanBench+ / 2609.35581 QC-Stark | LLM quantum-codegen benchmarks: 42 tasks across Qiskit/PennyLane/Cirq (best Pass@1 59.5%); 11 tasks × 10 models with IRT | Medium: shows benchmarks are codegen-only, not discovery | abstract-only (unverified) |
| 2601.21629 Quantinuum: RL composes pytket passes | RL, not LLM | Low | abstract-only (unverified) |
| 2609.25947 Bridge of Ψ's (Schrödinger-bridge circuit optimiser) | Generative model; 2.46× gate reduction on 8q × 64-depth Clifford+T | Low (needs training) | abstract-only (unverified) |
| Bloq Maya (Bloq Quantum, launched 2026-10-13/14) | Commercial NISQ algorithm-development agent with hardware execution | Competitor signal, not FT | news headline only |
| US 2026/0300121 A1 (Dell) "LLM-based process for quantum resource estimates" | Patent application published 2026-10-01 | Possible prior art for an LLM resource-estimation agent | title only; the PDF text would not extract |

Not found despite targeted searches: any LLM/agent paper on syndrome-extraction scheduling, lattice-surgery or magic-state-factory layout, or decoders; any LLM agent paper producing **fault-tolerant resource estimates** (Qualtran or Azure Resource Estimator); any released code for 2610.22367 or OmniQEC.

## 8. 2603.29894 LLM-Guided Evolutionary Search for Algebraic T-Count Optimization
**Read depth:** partial (§I–VI, Tables 1–2). Appendices A–C were not read.

- **Task:** minimise T-count of CNOT+T phase polynomials, i.e. the number of columns of the parity matrix P, subject to an unchanged signature tensor S(P).
- **Method:**
  - VarTODD exposes the heuristic choices of FastTODD/TOHPE as a policy θ: budget split, top-k pools, a scoring function, schedules over the T-count, and beam width.
  - GigaEvo evolves **tuner programs** that define how θ is parameterised and searched, including restarts.
  - Three levels: GigaEvo → tuner → VarTODD descent. The archive is a 3-island MAP-Elites archive (ab-initio, mid-margin restart, near-end restart).
- **Models:** a mixture of **DeepSeek V4 Flash and GPT-5 mini** (cheap models).
- **Evaluator:** independently recomputes S(P_final) = S(P₀). Generated code cannot bypass this check.
- **Baselines:** FastTODD (Vandaele's Rust implementation), AlphaTensor-Quantum values, Khoruzhii et al.
- **Results:**
  - GF(2ⁿ) multipliers: 12 of 16 instances strictly beat every listed reference, the rest match, and the mean reduction is 7.0%. Examples: GF(2¹⁶) 423 → 383; GF(2³²) 1275 → 1177; GF(2⁶⁴) 3815 → 3729; GF(2⁵) 49 vs AlphaTensor-Q 59.
  - Ham15-high 639 → 631, Ham15-medium 137 → 135; the other 20+ benchmarks tie.
  - Seven seeds on GF(2¹⁶) ended at 383/383/383/383/385/385/387.
- **Compute:** 12 CPU cores; up to 3 h per tuner program for GF(2⁶⁴). API cost is plotted (Fig. 4) but no total is given in the text.
- **Code:**
  - `FusionBrainLab/gigaevo-core`: MIT, exists, 128★.
  - `DanilkaFish/gigaevo-core-vartodd`: MIT, exists.
  - `DanilkaFish/VarToddSource`: **404 on 2026-10-19** (cited in the paper as the main code and results repo).
- **Stated limits:** T-count is not total cost; Toffoli/CCZ synthesis may be cheaper. Each instance needs its own search.
- **Unstated limits [INFERENCE]:** gains are single-digit percentages over a strong baseline; one run per instance except GF(2¹⁶).
- **Takeaway:** cheap models are enough when the LLM tunes **search heuristics around a trusted core** instead of writing circuits.

## 9. 2606.02418 Evolutionary Discovery of Bivariate Bicycle Codes with LLM-Guided Search (IBM: Cruz-Benito, Cross, Kremer, Faro)
**Read depth:** partial (Abstract, §I, §IV method, §V verification, §VI.6 ablation, §VII discussion and limitations, data availability, campaign cost table). §VI.1–VI.5 and the Supplemental Material were not read.

- **Task:** find BB and non-CSS "perturbed BB" qLDPC codes at n ≤ 360. Fitness ranks codes by FOM = kd²/n.
- **Method:**
  - OpenEvolve with MAP-Elites. The LLM proposes diffs to a generator ansatz G(ℓ, m) → polynomial pairs, so one program covers many lattices. 4–6 islands.
  - Evaluation cascade:
    1. k from GF(2) rank on 2 small lattices (~2 s).
    2. BP-OSD distance on 8 lattices (30–60 s).
    3. MILP distance in the loop (campaigns 4–5).
  - Post-campaign checks: BLISS Tanner-graph deduplication, decomposability, local-Clifford equivalence.
- **Models:** Gemini 3 Flash Preview, then an ensemble of Claude Opus 4.6, GPT-5.2/5.3-Codex and Gemini 3/3.1 Pro.
- **Scale and cost:** 5 campaigns, ~1,650 iterations, ~2×10⁵ candidates, ~140 h. LLM spend was about **$400 total**: $15 (campaign 1, Flash, 100 iterations, 5 h), $25, $50, $47 and $100.
- **Hardware:** campaigns 1–3 ran on one Apple M4 Max (36 GB); later campaigns used a 64-core server.
- **Results:**
  - 465 distinct codes: 97 CSS and 368 non-CSS.
  - New CSS [[288,16,12]], with d = 12 exact and indecomposable.
  - k up to 54; the earlier weight-6 maximum was 16, but the high-k codes have d ≤ 4.
  - A non-CSS [[144,12,12]] that matches the gross code's FOM but does not beat it.
  - The [[288,24,12]] turned out to be a direct sum of two gross codes, caught by the decomposability check.
- **Verification findings:**
  - BP-OSD **overestimates distance up to 12×** for high-rate codes; 147 of 154 bounds were tightened.
  - Every A = B code has d = 2 (proved). BP-OSD missed this even with 1.5×10⁶ trials; MILP finds it in under 1 s.
  - Deep MILP corrected 22% of non-CSS distances downward.
- **Ablation:**
  - A GA on the same ansatz representation reached Σk = 1037 vs the LLM's 704, but every GA code has d ≤ 2.
  - At the lattices where the LLM fails, an exponent GA reached FOM ≤ 4 vs the LLM's 12.
  - The authors note the ablation is confounded by budget (213k LLM evaluations vs 14k GA evaluations).
- **Code:** `qiskit-community/qcode-discovery`, **Apache-2.0**, exists, 27★, pushed 2026-10-07. It contains prompts, diffs, MILP and BLISS tooling, and the catalogs. It depends on Infleqtion/qLDPC (Apache-2.0), quantumgizmos/ldpc (MIT) and OpenEvolve (Apache-2.0).
- **Stated limits:**
  - No circuit-level simulation; FOM is combinatorial (code-capacity simulations only).
  - The screening lattices require 3 | ℓ, which biases the search.
  - Campaign 3 saturated after about 225 iterations.

---

## 10. Landscape map

| Problem area | Who has done it (2025–26) | Evaluator quality | Open gap |
|---|---|---|---|
| VQC / QML ansatz and feature-map design | 2602.19387 (Alabama); 2606.13380 Astronaut (Osaka); 2609.20258; plus earlier QAS/RL work | Weak: noiseless simulation, single seeds, toy datasets, margins within ±σ | **Crowded, low value.** Nobody shows hardware-relevant gains |
| VQE ansatz generation | 2606.13380 (above chemical accuracy at 6.4 mHa); Severyn's own RL-VQE work | Medium: FCI/CASCI reference, but noiseless | Symmetry constraints not enforced. Low novelty for a hackathon |
| Reversible / arithmetic primitive synthesis for FT (Toffoli × qubits) | **2610.22367** (Harvard/Anthropic/QuEra) | **Strong:** kickmix bit+phase simulator, exact phase and ancilla checks, statistical ε bound | **No public evaluator, task suite or code.** TQ objective admitted to be arbitrary; no hardware-weighted objectives; no LLM-vs-GA ablation; no cost reporting |
| T-count / phase-polynomial optimisation | 2603.29894 VarTODD+GigaEvo; AlphaTensor-Quantum (RL); 2606.13811 (trained LLM) | Strong (signature tensor) | Gains of a few % over FastTODD; main repo currently 404; not linked to Toffoli/CCZ or end-to-end resource cost |
| QEC code discovery, code-level (n, k, d) | IBM 2606.02418 (open); refs in OmniQEC: RL, Bayesian optimisation, earlier LLM program search | Medium–strong once MILP is added; BP-OSD alone is misleading (12× overestimate) | Circuit-level performance is missing (IBM says so) |
| QEC code–circuit–decoder co-design (circuit-level LER) | **OmniQEC** 2607.25865 (closed) | Strong in principle (Stim + BP+OSD), but expensive and the baseline schedule is non-optimised | **No open implementation.** No calibration- or device-aware variant (listed as future work). Proxy-only optimisation is shown to be harmful |
| Syndrome-extraction scheduling, lattice surgery, magic-state factories via LLM | **Nobody found** (only classical/human papers, e.g. 2602.09099, 2609.26736) | Stim makes it checkable | Unoccupied, but needs deep QEC know-how and slow evaluation |
| FT resource estimation | No LLM paper found; 2610.10490 (non-LLM uncertainty framework); Dell patent (title only); Qualtran and Azure RE exist | Deterministic tools exist | **No agent that produces evidence-carrying, interval-valued estimates from a paper or algorithm spec** |
| Literature → experiment on hardware | Pasqal 2607.25834 + open toolkit (neutral atoms) | Emulator + human; wrong-observable failure documented | Done well for analog Rydberg; nothing equivalent for gate-model FT design |
| Agent-run numerical simulation | 2601.10194 (tensor networks) | Human rubric | Code unreleased; automatic correctness checks missing |
| Execution plumbing (MCP / HPC / cloud) | 2604.08318 (ABCI-Q); Amazon Braket MCP; Bloq Maya (commercial) | n/a | Commodity, so a poor differentiator |
| Quantum codegen benchmarks | QuanBench+, QC-Stark, QCircuitBench | Execution tests | Benchmarks score code correctness, **not discovery quality under resource objectives** |

**Cross-cutting evidence:**
- (a) Proxy objectives mislead the search:
  - OmniQEC: proxy-only feedback scored *below* no feedback.
  - IBM: BP-OSD overestimated distance up to 12×, and the A = B trap went undetected.
- (b) Cheap models suffice when the evaluator is trustworthy: VarTODD used DeepSeek V4 Flash + GPT-5 mini; IBM's $15 Gemini-Flash campaign found 9 codes.
- (c) Agent failures are "plausible but wrong":
  - Pasqal: wrong observable, and a misdiagnosed qubit-ordering bug.
  - 2601.10194: premature completion, and running at bond dimension 1.
  - 2604.08318: figure and text disagree.
  
  Deterministic verification is the moat.

---

## 11. Three niches a solo 20-hour build could credibly own

### Niche A: "TQ Arena", an open, verified benchmark and discovery service for reversible FT primitives with pluggable hardware objectives
- **What:**
  - Re-implement the kickmix evaluator described in 2610.22367 Methods: bit string + sign tracking; X/CNOT/Toffoli/swap, Z/CZ/CCZ, X-measurement with measurement-based uncomputation; exact checks on output, inputs, ancillas and phase; the ε ≤ ln(1/δ)/k certificate.
  - Ship 5–8 small tasks with known baselines: n-bit adder, comparator, controlled add, the paper's own GF(2⁴) inversion example (|x⟩|h⟩ → |x⟩|h⊕x⁻¹⟩, p(X) = X⁴+X+1), a small QROM, a fixed-point square.
  - Run an OpenEvolve loop (Apache-2.0) with cheap models through OpenRouter.
  - **Differentiator:** let the user choose the objective (TQ, Q^κ·T with κ ∈ {1, 2, 3}, Toffoli depth) and show how the Pareto frontier and the winning circuit change. 2610.22367 itself says TQ is arbitrary and that κ = 1–3 is used in factoring estimates.
  - Leaderboard: model × task × objective × $ spent.
- **Evidence it is open:**
  - No code or evaluator was released for 2610.22367.
  - Existing quantum LLM benchmarks (QuanBench+, QC-Stark) test codegen correctness, not resource-optimal discovery.
  - IBM's ablation shows the LLM-vs-GA question is unresolved and budget-confounded, so the arena can run a matched-budget GA arm.
- **Feasibility:** the simulator is a few hundred lines of Python. Tasks are small enough for 10³–10⁴ tests per candidate in seconds. Budget: IBM got results for $15/campaign; VarTODD used Flash/mini-class models.
- **Fit for Severyn:** it is his RL-env and harness skill set, turned into a deployable product.
- **Hackathon fit:**
  - Eon Era (agent benchmarking) is the natural partner prize.
  - SurrealDB can hold program lineage, a MAP-Elites archive as graph + documents, and insight notes as vectors. This mirrors the paper's cross-session notes.
  - Clerk for API keys and submissions.
- **Risk:** on tiny tasks, the best-known baselines (e.g. Gidney's adder) may be hard to beat. Frame the demo around *verified reproduction* plus objective-dependent trade-offs, not new state of the art.

### Niche B: "Proxy-honest QEC triage", a verification-first evaluator service (MCP + UI) for LLM code-discovery agents
- **What:** submit H_X/H_Z or a BB polynomial pair. The service returns:
  1. An exact k.
  2. A **certified distance or a labelled upper bound**, using MILP via HiGHS, following IBM's formulation. It flags the known traps: A = B ⇒ d = 2, decomposable codes, and BP-OSD-only claims.
  3. A circuit-level LER from Stim + ldpc BP-OSD for small n (≤ 72–144) under a user-chosen p and connectivity.
  4. A "proxy disagreement" badge when the Φ = kd²/n ranking and the LER ranking disagree.
  
  Expose it as an MCP tool so any agent (Claude Code, Codex) can call it, which follows the Pasqal skills pattern.
- **Evidence it is open:**
  - OmniQEC, the only circuit-level LLM QEC system, has no code.
  - Its ablation shows proxy-only feedback scoring below no feedback.
  - IBM explicitly lacks circuit-level simulation, found BP-OSD overestimates up to 12×, and found 22% of non-CSS distances needed downward correction.
- **Reusable parts:** qcode-discovery (Apache-2.0) for the MILP, distance pipeline and catalog of 465 codes, which serves as seed data; Infleqtion qLDPC (Apache-2.0); Stim (Apache-2.0); ldpc (MIT).
- **Risk:**
  - Circuit-level sampling at n = 144 takes minutes to hours (OmniQEC's own figure), so a live demo needs small n or cached results.
  - Less of a match for Severyn's VQE/RL background than A.

### Niche C: "Evidence-carrying FT resource estimates", an auditor agent from paper or algorithm spec to Qualtran/Azure-RE estimates with intervals and provenance
- **What:**
  - The user names an algorithm or pastes a paper's claimed estimate (e.g. "Fe-S cluster QPE, X Toffolis, Y logical qubits").
  - The agent maps it to Qualtran bloqs or Azure RE inputs, and only deterministic tools produce the numbers.
  - It propagates hardware-parameter uncertainty (error rate, code distance, factory model) into **intervals**, as 2610.10490 argues.
  - It diffs the result against the paper's claim, writing every assumption into a reviewable spec file. This copies Pasqal's `experiment_spec.json` and "open_questions" pattern, with approval gates.
- **Evidence it is open:**
  - The targeted searches found no LLM/agent paper for FT resource estimation; only a Dell patent title (unverified) and Bloq Maya, which is NISQ.
  - 2610.10490 argues that single-number estimates are invalid.
  - Pasqal shows the literature-to-spec-to-tool-to-verdict pattern works and scales to triage: 526 papers classified.
  - 2601.10194 and Pasqal show agents fabricate plausible numbers, so the product's selling point is that the LLM never produces numbers itself.
- **Specific user:** application or strategy teams (e.g. 1QBit consultants, pharma or finance quantum leads) who must judge "when is algorithm X feasible on hardware Y".
- **Path to production:** a corpus-scale "estimate audit" of published FT resource claims, the analog of Pasqal's 526-paper triage.
- **Risk:** the hardest of the three to make *correct* in 20 h. Coverage must be limited to 5–10 algorithms already in Qualtran's bloq library, otherwise the agent will hallucinate mappings.

**Avoid:** VQC/QML ansatz agents (three papers already; weak evaluators; no credible impact story) and generic MCP execution wrappers (commodity: ABCI-Q, Braket MCP, Bloq Maya, Pasqal toolkit).
