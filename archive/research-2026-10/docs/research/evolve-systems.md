# LLM-driven evolutionary program search: what a solo builder can reuse for quantum-circuit discovery

Researched 2026-10-19. Read-depth labels: `full`, `partial (sections …)`, `abstract-only` (abstract-only items are **unverified**). Claims I derived myself rather than read are marked **[INFERENCE]**.

---

## 0. TL;DR

1. **The inspiration paper's stack is mostly reusable.** Gu et al. (arXiv 2610.22367) ran their search with **OpenEvolve** (Apache-2.0) and used **Claude Mythos 5** as the proposer. Their **evaluator, circuit builder, simulator, and all 8 task graders are public** at `andigu/uncompute` (Apache-2.0, created 2026-10-15). The search harness is not public: ideation prompts, OpenEvolve config, agent tools, and per-task specs are missing. The paper also reports **no iteration counts, sample counts, wall-clock time, or dollar cost**. Mythos 5 has *limited availability* and costs $10/$50 per MTok.
2. **OpenEvolve and ShinkaEvolve are both mature, Apache-2.0, and support Claude.** Both use the same evaluator contract: a Python function that scores a program file and returns a metrics dict. Recent evidence on sample counts: ShinkaEvolve beat AlphaEvolve's circle packing in about 150 proposals for about $10–12 of API spend. CodeEvolve needed about 400 Gemini-2.5 calls (about $35) for the same target. FunSearch used about 10⁶ samples. AlphaEvolve says "thousands".
3. **Cost estimate for a small reversible-arithmetic task with a T×Q score** [INFERENCE, derived from the per-call costs above]:
   - About $0.06–0.17 per single-shot proposal on Claude Sonnet 5.5 or 4.6.
   - Smoke test (30–100 calls): $3–15.
   - Meaningful multi-family run (300–1,000 calls): $20–150.
   - Gu-style *agentic* iterations, with multi-turn tool use inside each iteration: $0.5–3 per iteration on Sonnet, so $100–1,500 per task. Multiply by about 5 for Mythos.
   - Caveat: n-bit adders are a solved problem. Gidney's adder uses n−1 Toffolis and ships as a gadget in `uncompute`. A "meaningful" adder run can only rediscover known constructions. Modular adders, comparators against constants, and windowed or fused arithmetic leave more room.

---

## 1. Inspiration paper: Gu, Kemeny, Yelin, Lukin, arXiv 2610.22367 (15 Oct 2026)

**Read depth:** partial. I read the main text, all results sections through the Discussion, the full Methods ("Circuit model and validity", "Validation and statistical guarantees", "Cost model and scoring", "Evolutionary search"), the Extended Data prompt figure, and the results tables. Of the SI I skimmed section headings and the RS/modular-inversion baselines. I did not read all SI derivations.

### What the method actually does
- **Representation.** Each candidate is a *Python program that builds a circuit* through a shared generic circuit-building interface. Functions, loops, and named registers are kept so the LLM can make coordinated algorithmic edits.
- **Circuit model.** The "kickmix" model of Babbush et al. (arXiv 2603.28846):
  - X, CNOT, Toffoli, SWAP;
  - diagonal sign gates Z, CZ, CCZ;
  - destructive X-basis measurement for measurement-based uncomputation (MBU).

  Every allowed op maps a basis state to a basis state up to sign, so the evaluator only tracks one bit string plus a sign per shot.
- **Validity.** On every tested shot:
  - outputs match the reference;
  - inputs are unchanged;
  - every ancilla returns to |0⟩;
  - the global sign is exact;
  - gate operands are distinct.

  Large domains are *sampled*, with a binomial bound P_{k,b}(ε) on the true failure rate. Some tasks allow a "failure budget" (≤10⁻³ or ≤2·10⁻⁴).
- **Score.** TQ = Toffoli count (CCZ counts equally) × peak live qubits. The paper says any computable objective can be substituted.
- **Search.**
  - **Framework:** "We search over these circuit-generating programs with **OpenEvolve** [33], using **Claude Mythos 5** [28] to propose architectures and program rewrites."
  - **Ideation:** from the spec alone, the LLM proposes up to five distinct "algorithm families". Each family seeds a separate population.
  - **Evolution:** families evolve separately. Leading programs are shared across families periodically.
  - **Selection:** **MAP-Elites over the (T, Q) plane**, keeping the lowest-TQ program in each cell.
  - **Each iteration is a fresh *agent session*.** The session receives the spec, the parent program plus its evaluator feedback, alternative archive programs with their costs, short summaries of earlier attempts, and "DISCOVERY:" insight notes. Inside the session the agent can run drafts on test inputs, query a classical oracle, and delegate to subagents. The session ends by submitting one program.
  - The LLM never sees the evaluator beyond its feedback.
- **Results.** 7 of 8 tasks improve both T and Q. Examples: Reed–Solomon DQI decoder (5.1·10⁶, 1,938) → (4.4·10⁵, 1,837), a 12× TQ gain; Gaussian 39×; HHL angle 32×. Modular inversion gets a new divsteps architecture at (4.0·10⁶, 935).

### What is NOT stated (in the sections I read)
- Number of iterations, LLM calls, or tokens per task.
- Wall-clock time, compute, and **$ cost**.
- OpenEvolve configuration: islands, population size, cell grid.
- The agent tool definitions. Only a schematic transcript is shown, e.g. `run_candidate(..., trial_eval=true)`.
- The Gaussian-lineage figure colors points by iteration, but the text gives no totals.

### Code and benchmarks
- **`github.com/andigu/uncompute`** exists (cited as ref [16]). Apache-2.0, 3 stars, commits 2026-10-15 and 2026-10-16. Its README (read in full) and package README (read in full) show it contains:
  - **`uncompute.Builder`.** Allocation uses a LIFO free-list and tracks `peak_qubits`. Gates: x, cx, ccx, ccz, cswap, hmr, and others. `and_compute`/`and_release` implement Gidney temporary ANDs. `checkpoint`/`mirror` emit an exact Bennett inverse. `emit()` writes an op stream.
  - **`uncompute.Simulator`.** Bit-parallel: an arbitrary number of lanes is packed into one Python int per wire, so exhaustive sweeps are cheap. `assert_clean()` checks phase and ancillas, with a strict algebraic MBU check.
  - **Evaluator:** `tools/eval.py`. Usable from Python as `from eval import evaluate`, which returns `valid, tq_cost, toffoli, qubits, fail_reason, phases, …`.
  - **8 task folders**, each with `grader.py`, `reference.py`, `contract.json`, baseline and discovered circuits, and certified op streams.
  - **Lean 4 proofs** for the divsteps and DQI lemmas.
  - **Gadget library**: `gidney_add` (len−1 Toffoli), `cdkm_add_co` (2 Toffoli per bit), `mcx`, `ge_const_flag`, QROM/SelectSwap, GF(2) linear layers, GF tower fields.
- **Not released:** the search harness itself (prompts, OpenEvolve config, agent tools, task specs given to the LLM). The F₂⁴-inversion toy task from the Extended Data prompt figure is not among the 8 repo tasks.

### Reusable for a 20 h build
`uncompute` is a ready evaluator for T×Q with the correct validity semantics (ancilla cleanliness, phase, MBU). The grader/reference pattern lets you add a small task, such as an n-bit modular adder, in about 1 h [INFERENCE]. **Pitfall:** if candidates may import `uncompute.gadgets`, the LLM can call `gidney_add` and trivially hit the known optimum. Restrict imports, or score only novel composition.

---

## 2. AlphaEvolve (Novikov et al., Google DeepMind, arXiv 2506.13131, Jun 2025)

**Read depth:** partial. I read §1 Introduction with Table 1, §2 (2.1 Task spec, 2.2 Prompt sampling, 2.3 Creative generation, 2.4 Evaluation, 2.5 Evolution, 2.6 Distributed pipeline), §3 results text including the math-discovery strategy and §3.3 engineering (scheduling, kernels, TPU circuit, XLA IR), and §4 Ablations. I skipped the appendices.

### Method
- **Loop:** Prompt sampler → LLMs propose SEARCH/REPLACE diffs (or full rewrites) → evaluators → program database.
- **Evaluator contract:** a user-supplied Python `evaluate(...)` that returns a `dict[str, float]` of metrics to maximize. Code regions to evolve are marked `# EVOLVE-BLOCK-START/END`.
- **Evaluator features:**
  - an evaluation cascade with test stages of increasing difficulty;
  - LLM-generated feedback for non-quantified properties;
  - parallel evaluation. "The sample efficiency … makes it feasible to spend on the order of 100 compute-hours to evaluate any new solution."
- **Database:** "inspired by a combination of the MAP-Elites algorithm and island-based population models."
- **Prompts:** multiple prior programs plus scores, explicit context (papers, equations), stochastic formatting, and meta-prompt evolution.
- **Models:** an ensemble of **Gemini 2.0 Flash**, for throughput and idea volume, and **Gemini 2.0 Pro**, for occasional higher-quality breakthroughs.
- **Scale claim (Table 1):** FunSearch used "millions of LLM samples"; AlphaEvolve "thousands of LLM samples suffice". The paper gives no exact per-problem sample count and no $ figure.
- **Ablations** on matmul tensor decomposition and kissing numbers: removing evolution, prompt context, meta-prompts, full-file evolution, or the strong LLM (using a "small base LLM only") each hurts.
- **Math strategy:** evolves *search heuristics* with a fixed time budget (e.g. 1,000 s) that start from the previous best construction. The final constructions came from sequences of specialized heuristics.
- **Hardware relevance:** found a functionally equivalent simplification of a Verilog arithmetic circuit in the TPU matmul unit, which had to pass formal verification. This is the closest AlphaEvolve analogue to circuit discovery.

### Availability
- Closed research code. Discovered math results are published in a Colab at `google-deepmind/alphaevolve_results`.
- **Since 2026-07-09 it is GA as a paid service** on Google Cloud's Gemini Enterprise Agent Platform (source: InfoQ 2026-07-19, *read full*). Evaluators run client-side.
  - Klarna explored about 6,000 candidate programs over 3 weeks.
  - Pricing is not disclosed.
  - It requires Gemini Enterprise licenses and coordination with a GCP account team (from Google docs search snippet, *abstract-only*).
  - **Not practical for a 20 h hackathon.**

---

## 3. FunSearch (Romera-Paredes et al., Nature 625:468, Dec 2023)

**Read depth:** partial. I read the Main, FunSearch (Specification, Pretrained LLM, Evaluation, Programs database, Prompt, Distributed approach), Methods (implementation, prompt building, islands with exact Boltzmann selection, robustness), Code availability, and Extended Data figure captions. I skipped the SI.

- **Loop:** sample k=2 programs from one island, sorted by score into `priority_v0`, `priority_v1`; ask the LLM for `priority_v2`; evaluate; store the result if it is correct.
- **What is evolved:** a single function inside a fixed skeleton (e.g. the priority function of a greedy algorithm), typically 10–20 lines.
- **Evaluator:** `evaluate` scores the outputs on a set of inputs and aggregates them, e.g. by mean. Programs that time out, run out of memory, or produce invalid output are discarded.
- **Islands:** m islands, each seeded with the initial program.
  - **Every 4 h**, the worst m/2 islands are wiped and reseeded with the best program of a random surviving island.
  - Within an island, programs are clustered by *signature* (the tuple of per-input scores).
  - Clusters are sampled with Boltzmann probability P_i ∝ exp(s_i/T_cluster), where T_cluster = T₀(1 − (n mod N)/N).
  - Within a cluster, shorter programs are favoured (∝ exp(ℓ̃/T_program)).
- **Model:** Codey (PaLM 2 based, Vertex AI API). A fast, lower-quality model was chosen deliberately. Results were "not too sensitive" to the choice of LLM; a StarCoder comparison is in the SI.
- **Budget:** "**total number of samples on the order of 10⁶**". Typical deployment was **15 samplers + 150 CPU evaluators** (five 32-core CPU servers).
- **Robustness:** cap set n=8 succeeded in only **4 of 140** experiments. Admissible-set runs beat the baseline every time.
- **Code:** `github.com/google-deepmind/funsearch`, Apache-2.0 for code and CC-BY for materials, 1,134 stars. It contains a single-threaded reference implementation (`implementation/*.py`) without an LLM, sandbox, or distributed infrastructure.
- **Takeaway for the build:** the island-reset and signature-clustering ideas are worth copying. The sample-hungry regime (10⁶ calls) is unaffordable with frontier models and unnecessary with them.

---

## 4. Open-source reimplementations and successors

### 4.1 OpenEvolve — `github.com/algorithmicsuperintelligence/openevolve` (formerly `codelion/openevolve`)
**Read depth:** partial. I read the README in full (via the API), the circle-packing example README, the `config_phase_1_anthropic.yaml` config, the minimal `function_minimization/evaluator.py`, and the Claude Code quickstart README.
- **Activity:** Apache-2.0, Python, **7,600 stars**, 1,190 forks, 95 open issues. **Last commit 2026-10-19** ("adapt local AlphaEvolve evaluators for OpenEvolve (#519)"). PyPI package `openevolve`.
- **Evaluator API:**
  - `evaluate(program_path) -> dict` or `EvaluationResult(metrics={...}, artifacts={...})`. Artifacts (stderr, hints) are fed back to the LLM.
  - Optional `evaluate_stage1/2/…` for cascades with `cascade_thresholds`.
  - Extra kwargs via `evaluator_args`.
  - Library form: `run_evolution(initial_program=..., evaluator=lambda path: {...}, iterations=N)`.
- **Search:**
  - MAP-Elites with configurable `feature_dimensions`, which can be custom evaluator metrics. **This matches the paper's (T, Q) grid.**
  - Islands with migration, plus an optional `island_selector`.
  - `PopulationStrategy` hooks: `admit`, `archive`, `evict`, `migrate`, `replace_cell`.
  - Optional embedding novelty filter, LLM feedback, diff or full-rewrite modes, and a visualizer with a MAP-Elites grid view.
- **Model support:**
  - Any OpenAI-compatible API. OpenRouter works through `api_base`; the docs show an OpenRouter embedding endpoint.
  - **Native Anthropic:** the shipped config uses `api_base: https://api.anthropic.com/v1` with `claude-sonnet-4-5` (0.8) and `claude-opus-4-5` (0.2).
  - CLI providers that need no API key: **Claude Code CLI** (`provider: claude_code`, runs `claude -p`, per-call `max_budget_usd`), GitHub Copilot CLI, and Codex.
  - Gemini is the default.
- **Reported cost (README):**

  | Model | Cost per iteration |
  |---|---|
  | o3 | $0.15–0.60 |
  | o3-mini | $0.03–0.12 |
  | Gemini-2.5-Pro | $0.08–0.30 |
  | Gemini-2.5-Flash | $0.01–0.05 |

  The README advises starting with 100–200 iterations.
- **Reported samples:** circle packing n=26 reached 2.634 in about 800 generations with default config (issue #117). It exceeded AlphaEvolve (2.63598) at **iteration 206 of a 450-iteration multi-phase run** (issue #156).
- **Minimal example:** `initial_program.py` + `evaluator.py` + `config.yaml`. The library API needs about 5 lines plus an evaluator lambda.
- **Fit:** **Highest.** It is the exact framework the paper used. Caveats:
  - Islands all start from the same initial program, so Gu-style "families" need either an ideation pre-step that seeds one run per family or custom population hooks [INFERENCE].
  - The stock `claude_code` provider is `claude -p`. Whether it grants tool use, i.e. the paper's in-session draft runs and oracle queries, is unverified.

### 4.2 ShinkaEvolve — `github.com/SakanaAI/ShinkaEvolve` (paper arXiv 2509.19349; ICLR 2026)
**Read depth:** partial. I read the arXiv v1 HTML §1–4 and the hyperparameter tables in App. B, the ICLR 2026 camera-ready §1–6 including the Fig. 4 cost axis, the README (via the API), and `docs/getting_started.md`.
- **Activity:** Apache-2.0, Python, **1,469 stars**, 289 forks, 8 open issues. Last commit 2026-10-05 (merge of #195). PyPI package `shinka-evolve`.
  - Mar 2026: unified `ShinkaEvolveRunner`.
  - Feb 2026: Claude Code / Codex agent skills.
  - May 2026: `headless/claude` subscription-backed mutation.
- **Method:**
  - Islands with protected per-island elites.
  - Parent selection by power-law or "weighted" sampling (sigmoid fitness × 1/(1+offspring)).
  - Three mutation types: diff, full rewrite, crossover.
  - **Novelty rejection sampling:** embeddings with a cosine threshold of 0.95, plus an optional LLM novelty judge.
  - **UCB1 bandit over the LLM ensemble**, rewarding relative improvement.
  - A meta-scratchpad every T generations.
- **Evaluator API:**
  - The task directory contains `evaluate.py` + `initial.<ext>`.
  - `evaluate.py` defines `main(program_path, results_dir)` and calls `run_shinka_eval(...)`, which returns `(metrics, correct, error_msg)`.
  - Supports text feedback and multi-objective "public metrics".
  - Runs locally, on SLURM, or on SLURM + Docker.
- **Model support:**
  - Native OpenAI, **Anthropic** (`ANTHROPIC_API_KEY`), Gemini, DeepSeek, Azure.
  - **OpenRouter** (`openrouter/<model>`).
  - Local OpenAI-compatible servers.
  - `headless/claude` (subscription).
  - Live per-model pricing from models.dev, with **`max_api_costs` as a hard USD cap**.
  - A WebUI for monitoring.
- **Reported samples and cost:**
  - Circle packing SOTA "using only **150 samples**".
  - ICLR Fig. 4 plots cumulative API cost on an axis reaching **about $10–12 at about 150–160 proposals**. I read this off the axis; the text gives no number.
  - Circle-packing ensemble: claude-sonnet-4, gpt-4.1, o4-mini, gemini-2.5-flash, and others. Novelty and meta judging by gpt-5-nano. Embeddings by text-embedding-3-small.
  - AIME scaffold: 75 generations. ALE-Bench: 50 generations, about +2.3%. MoE loss: 30 iterations.
- **Fit:** **High.** The cost cap and WebUI suit a demo, and Anthropic/OpenRouter work out of the box. The 150-sample efficiency claim is the best-documented in the field. The circuit domain is untested.

### 4.3 CodeEvolve — `github.com/inter-co/science-codeevolve` (arXiv 2510.14150 v6, 27 Aug 2026)
**Read depth:** partial. I read §1–5.3 and Appendices B.4–B.6 and C.1–C.2 (costs, other LLMs, configs). I did not read the ablation details.
- Apache-2.0, 152 stars, v0.3.1.
- **Method:** islands, a per-island CVT-MAP-Elites archive, inspiration-based crossover, meta-prompting (co-evolving prompts), and depth exploitation with ancestor context. The plateau scheduler sets the exploration rate.
- **Evaluator:** a problem directory holding `input/evaluate.py` and `input/src/init_program.py`, plus a YAML config. It works with any OpenAI-compatible API, including vLLM, Ollama, and Together.
- **Results:**
  - Matches or beats reported AlphaEvolve results on 5 of 9 math benchmarks.
  - Beats **OpenEvolve and ShinkaEvolve on 6 of 9 under matched configs** (Qwen3-Coder-30B, 10 islands, 60 s timeout, 3 runs).
  - **Claude Sonnet 4.5** beat AlphaEvolve's circle-packing n=32 result under the default budget (5 islands × 200 epochs), with a mean of 2.93856 and a best of 2.93957.
- **Hard cost numbers:**
  - CirclePackingSquare n=26: Qwen3-Coder-30B surpassed AlphaEvolve after **about 900 calls / about $6**; **Gemini-2.5 Flash/Pro after about 400 calls / about $35**.
  - Full best runs (Table 10): Gemini-2.5 **$17–77** per run (6–19 h); Qwen3 $2–27.
  - Defaults: 5 islands / 200 epochs for closed models; 10 islands / 250 epochs for open models.
- **Fit:** medium-high. Strong defaults and transparent costs, but a smaller community, and Anthropic support goes only through OpenAI-compatible endpoints [INFERENCE: e.g. via OpenRouter].

### 4.4 GigaEvo + VarTODD (Fisher et al., arXiv 2603.29894 v2, Aug 2026): quantum T-count via LLM evolution
**Read depth:** partial. I read §I–III and §IV's budget text, plus the App. C run snapshot.
- **What it does:** it does *not* evolve circuits. It evolves **tuner programs** that steer the FastTODD/TOHPE parity-matrix optimizer. An external validator checks signature-tensor equality.
- **Models:** a mix of DeepSeek V4 Flash and GPT-5 mini.
- **Archive:** three islands.
- **Compute:** evaluations on 12 CPU cores, with up to 3 h per program for GF(2⁶⁴).
- **Snapshot:** 368 tuner programs across 14 generations; 286 of 357 evaluations were valid.
- **Results:** matches or beats the best reference T-count on all instances, with a mean 7.0% reduction on GF(2ⁿ) multipliers.
- **Cost:** shown only as a figure (incumbent T-count vs. cumulative API cost). No number in the text.
- **GigaEvo repo:** not verified (unverified).
- **Relevance:** a second, independent quantum-compilation example of the pattern: a heuristic search kept honest by an algebraic validator.

### 4.5 Others (lead-only)
- **DeepEvolve** (`liugangcode/deepevolve`; deep research combined with AlphaEvolve) — *search-snippet only, unverified*.
- **ThetaEvolve** (RL plus open models; cited by CodeEvolve) — *not read, unverified*.
- **LoongFlow** (Baidu, arXiv 2512.24077) — *search-snippet only, unverified*.
- **LLM4AD / EoH** — cited by Shinka and CodeEvolve; *not read*.

---

## 5. Comparison table

| System | Open source? | License | Evaluator API | Model support | Reported cost / samples | Fit for 20 h build | Read depth |
|---|---|---|---|---|---|---|---|
| **FunSearch** (DeepMind 2023) | Partial: reference single-thread impl, no LLM, sandbox, or distributed infra | Apache-2.0 (code), CC-BY (materials) | `evaluate()` → score per input, aggregated; evolves one function in a skeleton | Codey/PaLM2 (any LLM pluggable) | **~10⁶ samples**; 15 samplers + 150 CPU evaluators; cap-set n=8 succeeded in 4/140 runs | Low (sample-hungry; DIY infra) | partial |
| **AlphaEvolve** (DeepMind 2025; GA on GCP Jul 2026) | No (paid GCP service) | Proprietary | `evaluate()` → `dict[str,float]`; EVOLVE-BLOCK markers; cascades; client-side evaluator in GA | Gemini 2.0 Flash + Pro (paper); Gemini (service) | "Thousands of samples"; ≤~100 compute-h per eval feasible; Klarna ~6,000 candidates / 3 weeks; price undisclosed | Very low (enterprise onboarding) | partial (paper), full (InfoQ GA article) |
| **OpenEvolve** | Yes, 7.6k★, last commit 2026-10-19 | Apache-2.0 | `evaluate(path)` → dict or `EvaluationResult(metrics, artifacts)`; staged cascade; custom MAP-Elites dims | OpenAI-compatible (OpenRouter), **native Anthropic api_base**, Claude Code CLI, Copilot CLI, Codex, local | README: $0.01–0.60/iteration by model; circle packing beat AlphaEvolve at iter 206 of a 450-iteration run (~800 gens default) | **Highest** (paper's framework; (T,Q) MAP-Elites native) | partial |
| **ShinkaEvolve** | Yes, 1.47k★, last commit 2026-10-05 | Apache-2.0 | `evaluate.py: main(program_path, results_dir)` → `run_shinka_eval` → (metrics, correct, err) + text feedback | Native OpenAI, **Anthropic**, Gemini, DeepSeek, Azure, **OpenRouter**, local, `headless/claude`; bandit ensemble; `max_api_costs` cap | **150 samples** to circle-packing SOTA; ~$10–12 cumulative (ICLR Fig. 4 axis) | **High** (cost cap, WebUI, sample-efficient) | partial |
| **CodeEvolve** | Yes, 152★ | Apache-2.0 | `evaluate.py` + `init_program.py` + YAML | OpenAI-compatible (vLLM, Ollama, Together; Claude via compatible endpoint) | Beat AlphaEvolve circle packing: ~400 Gemini-2.5 calls / ~$35, or ~900 Qwen3-30B calls / ~$6; full runs $17–77 (Gemini) | Medium-high | partial |
| **GigaEvo + VarTODD** (quantum T-count) | Paper; repo unverified | Unverified | External signature-tensor validator; evolves tuner programs | DeepSeek V4 Flash + GPT-5 mini | 368 programs / 14 gens (one run); $ only in figure | Low as framework; useful as precedent | partial |
| **Gu et al. harness** (2610.22367) | **Evaluator yes** (`andigu/uncompute`); search harness **no** | Apache-2.0 (uncompute) | Circuit program → op stream → `tools/eval.py evaluate()` → {valid, tq_cost, toffoli, qubits, fail_reason} | OpenEvolve + **Claude Mythos 5** (limited availability; $10/$50 per MTok) | **Not reported** (no iterations, samples, $, or time) | Evaluator: **very high**; harness: rebuild needed | partial |

---

## 6. Cost estimate: small reversible-arithmetic task (T×Q score)

### 6.1 Pricing (official Claude pricing page, read in full, 2026-10-19)

| Model | Input $/MTok | Output $/MTok | Notes |
|---|---|---|---|
| Claude Sonnet 5.5 | 2 | 10 | cache hit $0.10 |
| Claude Sonnet 5 | 2 | 10 | promo price became standard |
| Claude Sonnet 4.6 / 4.5 | 3 | 15 | |
| Claude Opus 5.5 | 4 | 20 | |
| Claude Mythos 5 | 10 | 50 | limited availability |
| Claude Haiku 5.5 (≤100k-token prompts) | 0.10 | 0.50 | |

The Batch API halves prices but is asynchronous, so it suits only non-interactive steps such as ideation.

### 6.2 Per-call cost [INFERENCE]
Single-shot OpenEvolve/Shinka proposal:
- **Input, about 8–20k tokens:** system and task spec 1–2k; parent circuit program 1–3k (Builder code is about 50–200 lines); 3 top + 2 diverse programs 5–15k; evaluator feedback 0.5–1k.
- **Output:** 1.5–4k tokens for a full rewrite, plus 0–8k if extended thinking is on.

Results:
- **Sonnet 5.5:** 15k × $2/M + 3k × $10/M ≈ **$0.06**. With 5k thinking ≈ **$0.11**.
- **Sonnet 4.6:** ≈ **$0.09**, or **$0.17** with thinking.

Cross-checks from the sources:
- CodeEvolve Gemini-2.5: $35 / 400 calls ≈ **$0.09/call**.
- ShinkaEvolve: about $11 / 150 ≈ **$0.07/proposal**.
- OpenEvolve README, Gemini-2.5-Pro: **$0.08–0.30/iteration**.

These are consistent. Evaluation cost is negligible: `uncompute.Simulator` packs all lanes into one Python int per wire, so an exhaustive check of a 2×8-bit adder (65,536 inputs) costs a few big-int operations per gate [INFERENCE from the README design description].

### 6.3 Calls needed, by ambition [INFERENCE, anchored on §2–4 evidence]

| Run type | What it shows | Calls | $ (Sonnet 5.5–4.6) | Wall-clock (4–8 parallel proposals, ~30–60 s/call) |
|---|---|---|---|---|
| Smoke test: n-bit adder or comparator from blank program | Loop works; LLM rediscovers Cuccaro (2 Toffoli/bit) or Gidney (n−1 Toffolis, temp-AND + MBU) | 30–100 | **$3–15** | 10–30 min |
| Meaningful: 3–5 ideation families × MAP-Elites on (T,Q); modular adder, comparator against a constant, or a small finite-field op | Matches literature-best TQ, ideally beats a naive or textbook baseline by a clear factor | 300–1,000 (same order as Shinka 150, OpenEvolve 206–800, CodeEvolve ~400 to beat AlphaEvolve on packing) | **$20–150** | 1–4 h |
| Gu-style agentic iterations (multi-turn session per iteration: draft runs, oracle queries, subagents) | Closest to the paper's harness | 100–500 iterations × 10–30 turns each | **$0.5–3/iteration → $50–1,500**; Mythos 5 about 5× | several hours to a day |

### 6.4 Caveats
- **Adders are solved territory.** `uncompute.gadgets.arith` already ships `gidney_add` (len−1 Toffolis) and `cdkm_add_co`. With the import available, the LLM gets the optimum for free. A meaningful demo needs either:
  - a task with a less-settled frontier: constant modular adder, comparator against a constant, small GF(2ᵐ) inversion like the paper's F₂⁴ example, windowed/QROM-based lookups, or one of the 8 repo tasks at reduced size; or
  - a framing of the run as *reproducing a known optimum autonomously*, which is a verification story rather than a discovery story.
- The paper gives no sample counts, so it cannot calibrate the circuit domain directly. The estimates above transfer numbers from math and packing benchmarks; circuit programs may need more calls because validity (ancilla cleanliness, phase) fails more often than packing feasibility.

---

## 7. Reusable components for a 20 h solo build (concrete)

1. **Evaluator.** `andigu/uncompute`, Apache-2.0: `Builder` + `Simulator` + `tools/eval.py evaluate()`. Write `grader.py` and `reference.py` for one or two small tasks. Return `{combined_score: 1/TQ or −log TQ, toffoli, qubits}` and `fail_reason` as artifacts or text feedback.
2. **Search.**
   - **OpenEvolve**, the paper's framework: set `feature_dimensions: [toffoli, qubits]` for paper-faithful (T,Q) MAP-Elites, and pass `fail_reason` via artifacts.
   - **ShinkaEvolve** if you want `max_api_costs` and its WebUI: set an `ANTHROPIC_API_KEY` or use OpenRouter.
3. **Families.** One ideation call that asks for 3–5 architectures; seed one island or run per family. This is roughly 50–100 lines of glue [INFERENCE].
4. **Models.** Sonnet 5.5 as the main proposer; optionally Haiku 5.5 for cheap exploration or a novelty judge, as in Shinka's ensemble pattern.
5. **Sources of validity evidence.** Exhaustive simulation for small n; `assert_clean()` strict MBU checks. This gives "independently verified" claims for the Security & Ethics and Real-World Impact narrative.

## 8. Gaps and risks
- The paper's harness, prompts, and per-task specs are unreleased, and so are its cost and sample numbers. A faithful replication budget is unknown.
- The paper's proposer (Mythos 5) is limited-availability. Results with Sonnet-class models in the circuit domain are untested in any source I read.
- No source reports LLM-evolution results specifically on n-bit adders or modular adders with a T×Q objective.
- Reward hacking: the evaluator must recompute T and Q from the op stream, as `uncompute` does, never trusting candidate-reported values. OpenEvolve fixed a similar trust bug in its function-minimization example (issue #514).
