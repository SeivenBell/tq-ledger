Reading the committed file so I paste it exactly as written.

Source: commit `071a72e` on branch `research/ai-circuit-discovery`, file `docs/research/ai-circuit-discovery.md`. The complete report follows, verbatim.

---

# Is AI-driven algorithm and circuit discovery open to an outsider in 12 hours?

Ticket #3. Researched 2026-10-22. Read-depth labels: `full`, `partial (sections …)`, `snippet-only` (carries no conclusion). My own judgement is marked `[INFERENCE]`. Evidence already in `docs/research/` is referenced, not repeated.

**Correction to prior evidence.** `quantum-ai-discovery.md` (§0, §10, §11 Niche A) states that 2610.22367 released no code and that "no public evaluator, task suite or code" exists. That is wrong: `andigu/uncompute` (Apache-2.0) has been public since 2026-10-15 and holds the evaluator, all 8 graders, baselines and discovered circuits. `evolve-systems.md` and `field-needs.md` have it right. Niche A ("TQ Arena") was built on the false premise and on the absence of ECDSA.fail from that report.

---

## 1. Bottom line

- **Yes, the field is open to outsiders, and that is already proven: so a search demo is not a product.** Five days after the paper's release, a solo person with "no physics degree, no lab", working from "a chat window and a C compiler" with Claude and Codex coding agents, beat all 8 published TQ results on the unmodified grader (−0.08% to −64.9%). On ECDSA.fail, 147 accounts and 1,589 submissions (as of 2026-10-17) cut the point-addition score 86% in eight weeks using generally available models (Opus 4.8, Opus 5.5, GPT-5, Grok, Kimi) through Claude Code and Codex. Mythos 5 is verification-gated, but nobody needed it.
- **An arena or benchmark is the wrong build.** It exists twice: `uncompute` is the canonical 8-task evaluator (4 stars, 0 forks), and Eigen Labs runs a live leaderboard (ECDSA.fail, since 2026-05-30) now generalised into Yukon, a 13-challenge platform with CLI, sandbox and a "propose a problem, we build the checker with you" intake. A third copy built in 12 hours would be less trusted than either. The right move for the 7 non-crypto tasks is to propose them to Yukon, not to host them.
- **The real, documented pain is verification rigour, not leaderboards.** Sampled graders are being gamed and are leaking wrong circuits: a one-CX-removed circuit passes the stock `hhl-angle` grader; the ECDSA.fail paper admits 4.8% of commits were pure "verifier search" and half of audited commits rerolled the test seed; the 2026-10-13 record circuit fails 111 of 360,960 off-sample inputs; one solver found 46,286 gates that never fire under the 9,024-shot test set. Five issues and PRs asking for stricter checks (four on ECDSA.fail since August, one on `uncompute`) sit open with no maintainer reply. The only Craig Gidney comment found on the Anthropic result was about approximation accounting.
- **Best wedge: an independent re-grading and certification service** ("second opinion" for reversible-circuit claims): fresh-seed off-sample re-grade with a Clopper–Pearson failure-rate interval, dead-gate census, boundary sweeps, retry-adjusted score, and a signed receipt, for `uncompute` op streams first. It fits Severyn's verification theme exactly, has no 1QBit overlap, needs almost no LLM spend, and the evaluator runs in 0.7 to 3 seconds per circuit on this container. Its weakness: the user base today is a few dozen solvers and two maintainer teams, and the AI content is thin.
- **Press claims are inflated and disputed within hours, which is a second demand signal.** Quantum Computing Report's "up to 9,100x" is the paper's own naive reversible baseline (the paper prints "—†" for that row; its largest gain against a published baseline is 39×). On TQ the paper's point adder (3.7e9) is behind Schrottenloher (2.7e9) and behind the ECDSA.fail leader (0.94e9 under different billing). Eigen Labs' Soubhik Deb publicly disputed the Pareto-frontier claim the day of the post.
- **Score for the best wedge: 28/45.** Strong on advantage, credibility, competition and risk; weak on judge appeal and on "AI makes a material difference". It is a credible, honest project, not a venture story. If the map needs a judge-facing B2B story, this opportunity area does not supply one.

---

## 2. The pain

### 2.1 Sampled verifiers accept wrong circuits, and solvers exploit it

| Who | What happened | Source, date, depth |
|---|---|---|
| Gu, Kemeny, Yelin, Lukin (Harvard/Anthropic/QuEra), maintainers of `uncompute` | `hhl-angle` grader draws ≈8,742 uniform-k shots. Two one-edit variants of the authors' own circuit (one CX removed; one add truncated at bit 30) pass with 0 failures but are wrong on 609 and 1,221 (X,k) lanes. The reporter suspects `coulomb-potential`, `gaussian`, `lattice-gauge` share the weakness (same uniform-k accumulator). Patch supplied. No maintainer reply as of 2026-10-22. | `andigu/uncompute` issue #1, 2026-10-20, `full`; Zenodo 10.5281/zenodo.23486661 white paper, 2026-10-19, `full` (pdftotext) |
| ECDSA.fail organisers (Eigen Labs: Naik, Anant, Deb; Justin Drake, EF) | Paper admits: "The score is sampled and can be optimized through support selection"; 19 of 400 audited commits (4.8%) were pure verifier search; "approximately half of the audited commits include a reroll alongside a circuit modification". Failure budget is 0 of 9,024 ≈ 2^-13.3. | arXiv 2609.09582 v2, 2026-09-19, `full` (PDF pp. 1–3, 16–31, 40–62) |
| Jieyi Long (Theta Labs), record holder | 893-qubit circuit (2026-10-13) passed 9,024/9,024 but failed 111 of 360,960 off-sample additions (≈3e-4). | postquantum.com, 2026-10-14/17, `full` (secondary) |
| Austin Amissah, high-school intern, solo on a ThinkPad | Built a 9.2× faster checker and a classical pre-filter with Claude Code; measured per-draw failure rate λ ≈ 20.6 (CI 18–23) for the then-leader, so P(clean seed) ≈ 1.2e-9: "the search cost the score does not count". PR #27: 46,286 gates never fire on the 9,024-shot set. Issue #23, PR #27, PR #28 open, zero replies. | `austinamissah/ecdsa-circuit-optimization`, Jul–Aug 2026, `full` README + issue/PRs |
| willzeng (ECDSA.fail issue #1, 2026-06-03); bulengerk (#239, 2026-09-08) | Asked for inputs independent of the op stream or many more inputs (closed by maintainer as acceptable at a 99% target); off-sample counterexample with a request for regression fixtures and error-budget disclosure (open). | `Layr-Labs/ecdsafail-challenge` issues, `full` |
| Anonymous `ecdlp-contest` | Forked a "hard mode": 102,400 shots, server-side private seed, zero failures; claims "every replayed public ECDSA.fail row is invalid under the current validation gate". 0 stars. | `ecdlp-contest/ecdlp-point-add`, updated 2026-10-21, `full` README |
| Craig Gidney (Google), HN | Only comment on the Anthropic post: "99.99999% vs 100% accurate can be a factor of 10 in cost." | HN item 50121939, 2026-10-16, 174 points / 39 comments, `full` |

`[INFERENCE]` Two independent benchmark communities hit the same failure in the same quarter. The fix each applied (patch one grader, fork one contest) is local and unmaintained. Nobody offers an independent re-grade as a service.

### 2.2 Claims are not comparable, and the press repeats the wrong number

- The paper never says "up to 9,100x". The figure appears once, in SI I.2, against "our reversible implementation of this baseline" (100M Toffolis, 190k qubits); Table I prints "—†: Naïve reversible implementation; no prior reversible compilation exists". Largest gain against a published baseline: 39× (Gaussian). (arXiv 2610.22367 v1, 2026-10-15, `full` main text + Methods + ED tables; SI `partial`.)
- Quantum Computing Report (Global Quantum Intelligence, 2026-10-17, `full`): "by 4.1x to over 9,100x relative to hand-crafted baselines". It does not say the 9,100× baseline is naive. The Quantum Insider (2026-10-17, `full` by subagent) did flag it.
- Anthropic's post (2026-10-16, `full`) claims a point-addition design that "expanded the Pareto frontier". Soubhik Deb (Eigen Labs) disputed it the same day, citing the ECDSA.fail frontier (X post, `snippet-only`; his authorship of the ECDSA.fail paper confirmed from its author list). The white paper's Table (§7) lists six point adders with an "Accounting" column because each bills differently: per-shot vs average Toffolis, nonce-chosen vs hashed inputs, 0 vs 20-in-100k failures.
- ECDSA.fail paper on Google's ZK-attested circuit: "numerical context rather than … formal dominance".

### 2.3 What practitioners do today and what it costs

Solvers build private instruments (Amissah's checker; Brown's `ucverify`, "compiler and search tools not released"), then publish circuits with a self-graded receipt. Readers must re-run a 1.5k-commit Rust harness or a Python evaluator at a pinned commit to check anything. Cost signals: Amissah's 199 re-runs × 110 s; Brown's point adder re-graded on 100k held-out inputs; Theta's 360,960-input off-sample run. None of this is visible on either leaderboard.

---

## 3. Existing solutions

| Thing | What it does | Who uses it | Price / licence | Depth |
|---|---|---|---|---|
| `andigu/uncompute` | Exact kickmix evaluator, 8 graders with failure budgets, baselines, discovered circuits, Lean 4 proofs. Tests hashed from the circuit. `evaluate()` returns `valid, tq_cost, toffoli, qubits, avg_toffoli, fail_reason`. No search harness, prompts, leaderboard or submission path. 2 commits (2026-10-15), 4★, 0 forks, 1 issue. Verified here: `uv sync` + `make kernel` work; certified-stream re-grade 0.7 s, build-and-grade 3.0 s (coulomb), 1.8 s (hhl baseline). | Gu et al.; Brown | Apache-2.0 | `full` README, tree, 2 graders, `eval.py`, `task.py`; ran it |
| ECDSA.fail (Eigen Labs) + `Layr-Labs/ecdsafail-challenge` | Live leaderboard, S = peak qubits × average executed Toffolis, 9,024 SHAKE256 inputs, Rust harness, CLI `ecdsafail run/submit`. Launched 2026-05-30. 831 rows by 2026-07-27; 1,589 submissions / 147 accounts by 2026-10-17. 92★, 48 forks, 1,541 commits, 13 open issues. No prizes. | Theta Labs, EF, Starknet, StarkWare, Brevis, Trail of Bits, Pauli Group, Stanford FSL, many independents | Paper CC BY 4.0; harness licence not shown | paper `full`; README `full`; blog `full` |
| Yukon (yukon.org, Eigen Labs) | Multi-domain "open autoresearch" platform: 13 challenges (crypto, ML, ZK, biology), deterministic checker, sandbox, `yukon submit`. Only ECDSA.fail is quantum. Intake: "If we shortlist yours, we email you to design the checker together." | Agents and their operators | Free, no prizes shown | `full` (thin pages) |
| `ecdlp-contest/ecdlp-point-add` | Stricter fork: 102,400 shots, server-side seed, different metric (Q × √(avg Toffoli × avg depth)). Anonymous, 0★. | Nobody visible | MIT | `full` README |
| `austinamissah/ecdsa-circuit-optimization` | 9.2× faster checker, classical pre-filter, λ measurement, dead-gate certification. Single-task, Rust. | Author | not stated | `full` |
| `HereLiesRepo/Here-Lies-Space-Time` | `ucverify` C verifier (exhaustive sweeps for 3 small tasks, exact sign tracking, no failure budgets), hhl-angle reproducers and patch, 8 streams with receipts. 0★. | Author | CC BY 4.0 / MIT | `full` README + white paper |
| `trailofbits/trailmix` | Rust reversible-circuit IR, 64-shot simulator, phase checker, EC-add for several curves. 27★. | Trail of Bits | not checked | `full` README (subagent) |
| FTCircuitBench (arXiv 2601.03185, PNNL et al.) | Library of pre-compiled Clifford+T logical benchmark circuits. Not LLM, no leaderboard. | Compiler researchers | open | abstract `full` |
| Classiq Quantum Circuit Challenge | Depth/CX metric, 387 participants, $2k × 5 prizes, 2026-08-28 to 09-30. NISQ. | Students, hobbyists | free | secondary `full` |
| QCircuitBench, QuanBench+, QC-Stark, QHackBench, Qiskit HumanEval, QEncodeBench | LLM code-correctness benchmarks (Pass@k). Not resource-optimal discovery. | ML researchers | open | abstracts |
| OpenEvolve / ShinkaEvolve / GigaEvo / CodeEvolve | Evolutionary coding frameworks (see `evolve-systems.md`). No quantum example in any `examples/`; OpenEvolve issue search "quantum": 0. OpenEvolve's `claude_code` provider is single-shot `claude -p`, not the agentic session of Gu et al. GigaEvo 1.0.0 (2026-08-17, MIT, 128★) has a Claude Code `harness` backend. | Researchers | Apache-2.0 / MIT | `full` README + `claude_code.py` |
| VarTODD (`DanilkaFish/VarTodd`, MIT, 3★, last commit 2026-09-22) + `gigaevo-core-vartodd` | T-count tuner evolution. ~$1–2 LLM per run (Fig. 4 axes), 12 CPU cores, up to 3 h per candidate. Needs C++23, CMake, Redis, OpenRouter key. The 404 name in the prior report was a mis-remembered repo. | Authors | MIT | paper `full`; repos `partial` |
| AlphaEvolve (Google Cloud, GA 2026-07-09) | Requires a Gemini Enterprise licence via a sales rep and account-team provisioning; no public price. | Enterprises (Klarna) | undisclosed | docs `full` |
| Claude Mythos 5 / 5.1 | "available only to organizations verified through Anthropic's verification programs"; $10/$50 per MTok. Fable 5.1 is GA at the same price. | Verified orgs | gated | docs `full` |

---

## 4. The gap

1. **No independent, off-sample certification exists for either benchmark.** Both graders seed tests from the circuit itself (Fiat–Shamir), which stops memorisation but not support selection or nonce rerolls (ECDSA.fail) and not low-probability boundary bugs (`uncompute` hhl-angle). The paper's own statistical bound (ε ≤ ln(1/δ)/k) assumes a candidate fixed before the draw; neither leaderboard records how many candidates were screened. Nobody publishes Clopper–Pearson intervals, retry-adjusted scores (Q×T/p̂, which the ECDSA.fail paper computes once in an appendix), or dead-gate censuses as a standard receipt.
2. **Why unfilled:** maintainers are a two-to-four-person volunteer effort per benchmark and have been silent since August (ECDSA.fail) or for two days (uncompute, which is brand new). The three people who built instruments (Brown, Amissah, the `ecdlp-contest` author) each kept them single-task and unmaintained. `[INFERENCE]` The work is unglamorous and does not move a leaderboard, so solvers do not do it and operators do not fund it.
3. **Cross-benchmark comparability** is unsolved by design: three billing rules for a Toffoli under a classical condition, two input-selection rules, four failure budgets. The white paper's "Accounting" column is the only attempt I found.
4. **Not a gap:** hosting tasks. Yukon will build a checker with any proposer. The 7 non-crypto `uncompute` tasks are ready-made proposals.
5. **Not a gap:** showing that GA models can do this. Brown (Claude + Codex), Theta (Opus 5.5 + GPT-5 Codex), the Yukon sample (Opus 4.8) and IBM's $15 Gemini-Flash campaign already show it. What is missing is the cost and iteration accounting the paper omitted (no iterations, tokens, dollars; ED Fig. 2 colourbar tops at iteration 94 for Gaussian), which is a blog post, not a product.

---

## 5. Candidate wedges

### Wedge A (recommended): "Second Opinion", an independent re-grade and certification receipt for reversible-circuit claims

- **User:** (1) solvers on `uncompute` tasks and ECDSA.fail who want to know whether their circuit is actually correct before claiming a record (Brown ran 100k held-out inputs by hand; Theta did 360,960); (2) the two maintainer teams, who are not answering verification issues; (3) analysts and journalists repeating claims (QCR, postquantum.com).
- **Job:** upload an OPSTRM01 op stream (the `uncompute` format) and a task name. Return in under a minute: stock-grader verdict at the pinned commit; a fresh-seed off-sample re-grade (N ≥ 10× the stock shot count, seeds independent of the stream) with a Clopper–Pearson 95% interval on the failure rate; dead-gate census (ops that never fire under the test distribution, Amissah's PR #27 idea); task-aware boundary sweeps (accumulator carry boundaries, domain edges, exhaustive sub-slices, generalising Brown's hhl-angle patch to the three other uniform-k tasks); retry-adjusted TQ = T×Q/p̂; a signed JSON receipt with the stream hash. Publish a "verifier scorecard" for all 8 stock graders.
- **Demo in 2 minutes:** run Brown's `coverage-gap-blip` reproducer: stock grader says OK; Second Opinion says FAIL with 609 wrong lanes and the exact (X,k). Then grade the paper's discovered `hhl-angle` and Brown's stream side by side with intervals. Then the 8-task scorecard with the three suspect graders flagged.
- **Reusable components (verified):** `andigu/uncompute` (Apache-2.0; evaluator, graders, certified streams as fixtures); Brown's reproducers and patch (patch Apache-2.0, streams CC BY 4.0); `ucverify` (MIT) for an independent C cross-check on 3 tasks. Deploy as FastAPI + a small UI on Render ($50 credit). SurrealDB can hold receipts and lineage (weak but real partner fit).
- **Data and compute:** none beyond CPU. Measured here: 0.7 s per certified re-grade, ≈3 s build-and-grade for small tasks; the DQI and modinv tasks take "minutes to hours" per the README, so cache or background those.
- **LLM cost:** ≈$0 for the core. Optional: an LLM reads `reference.py` and proposes adversarial input families for the boundary sweep (Fable 5.1 or Sonnet, a few dollars). Keep every verdict deterministic.
- **Partner-prize fit:** Eon Era is enterprise-agent simulation (Salesforce, Jira, Slack), not a fit. SurrealDB: receipts store, marginal. Clerk: API keys for submitters, marginal.
- **Main way it fails:** the universe is 8 tasks and ~150 ECDSA.fail accounts, and the ECDSA.fail format is a Rust `build()` function, not an op stream, so day-one coverage is `uncompute` only (two active users). Also my probe shows the hard part is domain-aware: 14 of 14 random single-gate-drop mutants of two certified circuits were caught by the stock grader (and 6 Toffoli-drop mutants crashed the Builder's own mirror journal). Random mutation testing proves nothing; the value is in boundary families per task, which needs understanding each grader.

### Wedge B: "Frontier Ledger", a normalised claims board with accounting columns and re-grade receipts

- **User:** anyone comparing point-addition or primitive costs across papers and leaderboards: PQC risk analysts, journalists (QCR), the Eigen team (Deb's dispute), Gu et al. (Table S3).
- **Job:** one Pareto chart per task with every public claim, labelled by accounting rule (per-shot vs average billing, failure budget, input selection), source, date, and whether a receipt exists. Where a stream is public, re-grade it under the `uncompute` rules and attach the receipt. Show the "9,100×" row with its naive baseline flagged.
- **Demo:** the point-addition chart with Schrottenloher, Gu divsteps, Brown ×2, ECDSA.fail July/Oct, Google's bound, IonQ, record-and-replay, each with its accounting badge; click one to see the receipt.
- **Reuse:** `uncompute` evaluator; the white paper's §7 table and `CREDITS.md`; ECDSA.fail `results.tsv` and API snapshot; `ecdlp.ai` entries.
- **Cost:** ≈$0 LLM. 12 h is enough for the chart and 8 to 12 receipts; converting ECDSA.fail Rust circuits to op streams is not (Brown did it privately).
- **Fails if:** it is read as a content site, not a tool; and the point-addition emphasis is cryptanalysis-adjacent (see risk).

### Wedge C (the "participate" option): run the search with GA models and publish the cost accounting the paper omitted

- **What:** OpenEvolve or GigaEvo with Fable 5.1 or Sonnet 5.5 on one small `uncompute` task (hhl-angle, 1,348 Toffolis) or a 9th task, 100 to 300 iterations, publishing $/iteration, valid-rate, and TQ trajectory; file results as an `uncompute` issue and propose the 7 non-crypto tasks to Yukon.
- **User:** none next week. It is a credibility artefact (Aquarium-style replication) and a Yukon proposal.
- **Cost:** $20–150 (per `evolve-systems.md` §6; IBM's Flash campaign was $15; VarTODD runs were $1–2).
- **Fails if:** judged as a product. It should be the blog post attached to Wedge A, not the submission.

**Do not build:** another leaderboard (Yukon and `uncompute` exist; Aqora's hosting offer on ECDSA.fail issue #5 went unanswered, which says the operators are not looking for hosts); a VQC/NISQ ansatz agent (see `quantum-ai-discovery.md` §10).

---

## 6. Scores for Wedge A

| Criterion | Score | Why |
|---|---|---|
| Real user with evidence of pain | 3 | Pain is documented in 7 primary artefacts (issue #1, PRs #23/27/28, issues #1/#239, the paper's own audit), but the people with the pain built private tools and the maintainers ignore fixes; nobody asked for a service. |
| AI makes a material difference | 2 | The product is deterministic verification of AI-discovered circuits. The AI is upstream; an LLM adversarial-input proposer is optional. |
| Severyn's unfair advantage | 4 | Verification and open-benchmark theme (Aquarium), harness and RL-env experience, FastAPI/Cloud Run deployment; already runs an evaluator demo at work. |
| Buildable and demoable in 12 hours | 3 | Evaluator installs and grades in seconds (verified); fixtures and a known gap exist. Task-aware boundary families for 4 tasks and the UI are the 12 hours; DQI/modinv tasks are too slow for live demo. |
| Judge appeal (Georgian investors) | 2 | No buyer, no market size. The narrative "trust layer for AI-generated science claims" may land with Deval Pandya; it will not read as a B2B company. |
| Adoption path after Oct 25 | 3 | Concrete: PR the sweeps into `uncompute` and the ECDSA.fail harness; offer receipts to Yukon; Brown and Amissah are obvious first users. Ceiling is low. |
| Competition density (5 = open field) | 4 | Three single-task, single-person instruments; none offered as a service; no company. |
| Credibility gain in AI and quantum | 4 | Public, checkable, upstream of two visible communities; a found grader gap is a citable result. |
| Risk (5 = low) | 4 | No 1QBit overlap (upstream of QRE). Dual use is low (verification, not attack construction), but demo on non-crypto tasks and leave point addition to the ledger. |

Total 28/45.

---

## 7. Sources

Primary, read 2026-10-22 unless dated otherwise.

- Gu, Kemeny, Yelin, Lukin, arXiv 2610.22367 v1 (2026-10-15), https://arxiv.org/abs/2610.22367 — `full` main text, Methods, ED Fig. 1–2, ED Table 1; SI `partial` (I.2 Hermitian, II Table S3) via subagent.
- `andigu/uncompute` (2 commits, 2026-10-15), https://github.com/andigu/uncompute — `full` README, file tree, `coulomb-potential/grader.py`, `contract.json`, `hhl-angle/grader.py` header, `evalcore/task.py`, `tools/eval.py` header and `evaluate()`, `ops.py` docstring, gaussian discovered README; cloned and executed.
- Issue #1 on `andigu/uncompute` (HereLiesRepo, 2026-10-20), https://github.com/andigu/uncompute/issues/1 — `full`.
- Brown, "I Did Not Read the README…", Zenodo 10.5281/zenodo.23486661 (2026-10-19/20), https://zenodo.org/records/23486661 — `full` (pdftotext); repo https://github.com/HereLiesRepo/Here-Lies-Space-Time — `full` README, verifier README.
- Anthropic, "Designing more efficient quantum circuits with Claude" (2026-10-16), https://www.anthropic.com/research/designing-efficient-quantum-circuits — `full`.
- Quantum Computing Report (2026-10-17), https://quantumcomputingreport.com/harvard-anthropic-and-quera-use-llms-to-discover-quantum-circuits-with-up-to-9100x-lower-resource-costs/ — `full`.
- HN thread on the Anthropic post (2026-10-16), https://news.ycombinator.com/item?id=50121939 — `full` via subagent.
- Long et al., "ECDSA.Fail: Open Autoresearch…", arXiv 2609.09582 v2 (2026-09-19), https://arxiv.org/abs/2609.09582 — `full` (PDF pp. 1–3, 16–31, 40–62; HTML to 200k chars).
- Eigen Labs blog, "From a Hidden Quantum Circuit to Open Autoresearch" (2026-09-10), https://www.eigenlabs.org/blog/open-autoresearch-the-ecdsa-fail-story/ — `full`.
- `Layr-Labs/ecdsafail-challenge`, https://github.com/Layr-Labs/ecdsafail-challenge — `full` README; issues #1, #2, #5, #8, #23, #27, #28, #239.
- ecdsa.fail, https://ecdsa.fail — `full` (landing only); yukon.org and /create — `full` (thin pages; /challenges is 404).
- `ecdlp-contest/ecdlp-point-add` (updated 2026-10-21), https://github.com/ecdlp-contest/ecdlp-point-add — `full` README.
- `austinamissah/ecdsa-circuit-optimization` and amissah.net project page (Jul–Aug 2026) — `full`.
- postquantum.com, "Sub-900-Qubit secp256k1 Circuit…" (2026-10-14, upd. 10-17) — `full` (secondary). quentir.ai (2026-09-11) — `full` (secondary).
- Soubhik Deb dispute, X (2026-10-16) — `snippet-only` (no conclusion drawn beyond "disputed").
- Fisher et al., arXiv 2603.29894 v2 (2026-08-18) — `full` (Fig. 4 axes decoded); `DanilkaFish/VarTodd` (MIT, last commit 2026-09-22), `DanilkaFish/gigaevo-core-vartodd` (MIT, 2026-08-10), `FusionBrainLab/gigaevo-core` (MIT, 1.0.0 2026-08-17) — `partial` (rendered pages, READMEs).
- Cruz-Benito et al., arXiv 2606.02418 and `qiskit-community/qcode-discovery` README — `full`.
- OpenEvolve `openevolve/llm/claude_code.py` and `examples/` — `full`; ShinkaEvolve README — `full`.
- Google Cloud AlphaEvolve GA blog (2026-07-09) and access docs (updated 2026-10-20) — `full`.
- platform.claude.com model pages (Mythos 5, Fable 5) — `full`.
- Eon Era launch post (updated 2026-10-08), https://www.eon.io/blog/era-build-and-test-ai-agents — `full`.
- Classiq challenge coverage (quantumzeitgeist, 2026-10-06) — `full` (secondary); classiq.io/challenge returned 401.
- `trailofbits/trailmix` README; FTCircuitBench arXiv 2601.03185 abstract — `full`.
- Local experiment: 20 single-gate-drop mutants of the certified `coulomb-potential` and `hhl-angle` circuits run through the stock grader (script in session scratchpad, not committed): 14 valid mutants all FAIL (13 `verdict/classical`, 1 `verdict/phase`); 6 `ccx` drops crashed in `Builder.mirror()` journal verification.

Nothing older than 18 months was relied on.

---

## 8. Open questions

1. Will Severyn accept a project whose honest judge-appeal score is 2? Wedge A is a credibility build; the map's criteria (1) and (2) favour it, (3) does not.
2. Can ECDSA.fail circuits be ingested in 12 hours? The harness takes Rust `build()` code, not streams. Brown converted "exactly" but privately. Without this, day-one users are the `uncompute` community of two.
3. Would Eigen Labs' Yukon team adopt the 7 non-crypto `uncompute` tasks if proposed this week, and would they accept external receipts? One email to the Yukon intake form would settle both before Saturday.
4. Is Brown's hhl-angle gap real on the other three suspected tasks? Reproducing one of them during the build would be the strongest demo and a citable finding; failing to reproduce is also publishable.
5. Dual-use positioning: the loudest community is cryptanalysis (secp256k1). Does the pick restrict the public demo to the five non-crypto tasks, as `field-needs.md` §5 recommends?
6. Should `quantum-ai-discovery.md` §0/§11 be corrected in the synthesis memo so Niche A is not carried forward on a false premise?

---

End of report. This is the complete file as committed in `071a72e`, pasted in one part.