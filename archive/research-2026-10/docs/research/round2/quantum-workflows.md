# Checking quantum code after a Qiskit upgrade

Researched 2026-10-23. Decision input, not an implementation or an executed smoke. Read `quantum-dev-agents.md`, `practitioner-pain.md`, `build/qref-probe.md`, the research brief, and the original practitioner report in `local://paste-1.md` first. `[INFERENCE]` denotes synthesis. Source dates/read depths are below.

## Bottom line

- Existing tools already compare what quantum circuits do. MQT QCEC checks circuits, including parameterized circuits and measurement results. It does not prove that the surrounding Python code or runtime settings behave the same way. A new tool must show useful checks beyond those existing features. [S4–S6]
- A small contribution to IBM or MQT looks more useful than a separate product. IBM documents its checking limits and requests examples with real agent transcripts. QED-C has a draft CUDA-Q port under review. Neither team agreed to use a new tool. [S3, S7]
- Restoring one old notebook gives a user a clear result: code they can run again, with a record of what changed. Supporting arbitrary paper repositories is not a credible 12-hour promise. The archived textbook provides public examples, but no current maintainer requested their restoration. [S8]
- The previous probe caught five deliberately inserted errors. Its six passing examples and five failing examples show that the exercised checks work. They do not measure errors in real agent migrations or establish user demand. [S0]
- The headline numbers need context. The survey's 81% means 21 of 26 selected respondents encountered bugs at least occasionally after updates. The repair rates of 19-59% and 95-100% describe different model and destination subsets in the same study. [S1, S2]
- [INFERENCE] Build only after the small experiment below and evidence that someone needs its result. Stop the separate product if an ordinary coding agent plus QCEC produces the same useful evidence. If only package installation needs repair, do not present that work as new quantum verification.

Terms used below:

- **Migration** means changing existing code to work with a different software version or framework.
- **Circuit equivalence** means that two quantum circuits perform the same operation under the checker's stated assumptions. It does not establish that two complete programs behave identically.
- **Regression check** means a check for behavior that changed after an edit or upgrade.
- **Parameter binding** means assigning numeric values to a circuit's named parameters.
- **Measurement decoding** means converting measured bitstrings into the program's reported answer.
- **Smoke test** means a small first execution that checks a specific working path. Here, the proposed smoke tests also compare quantum outputs.

## 1. What pain and actual requests are established?

**TOSEM practitioner study, not a representative prevalence estimate.** Methods §§4.1–4.5: a voluntary, uncompensated 63-question, 20–30-minute survey; targeted identification of 1,397 industry/government developers from 71 organizations, plus 75 academic contacts and academic/snowball distribution. Collected May 20–Aug 5, **2024**: 38 completions, 12 excluded for no relevant experience, 26 retained; four opt-in follow-up interviews; 18 PhDs. More than ten invitees declined for confidentiality/security reasons. Quantitative aggregation plus independent qualitative coding/reconciliation was used; no inter-rater statistic was reported because the codebook evolved. These are **stale underlying observations** (>18 months), despite a February 2026 manuscript date. Do not treat the outreach denominator as a response rate: academic redistribution has no known total exposure. [S1]

Results §7.2: ten “occasionally,” eight “frequently,” three “very frequently,” four “rarely,” one “never” after updates. Thus **21/26 = 80.8% at least occasionally; 11/26 = 42.3% frequently/very frequently**. This measures respondents' experience, not the fraction of upgrades that fail, silent semantic defects, or demand for QRef. §8.4 calls for migration/versioning support and output validation; §8.6 emphasizes integration. One interviewee says academic tools “don't fit our workflows.” §9 explicitly acknowledges self-report, selection and small-sample/generalizability limits. There is also an internally inconsistent debugging-difficulty sentence (nine difficult, seventeen neutral, two easy totals 28 for n=26); do not use its “61% neutral” as a precise disconfirmation statistic without the replication data. [S1]

**Current, concrete primary workflow evidence:**

| Owner/work | Observed artifact, not invented demand | Implication |
|---|---|---|
| IBM/Qiskit skills, Jessie Yu (`jyu00`) | Phase 5 says a wrong plausible option default changes results silently and Phase 6 checks paths/types, **not behavior**. Phase 6 deliberately Cliffordizes and drops bound parameters for local option verification; it warns this is not physical-result reproduction. PR #8 (2026-09-29) reports simulator OOM during migration testing. CONTRIBUTING requests end-to-end agent/version/prompts/transcript evidence; internal eval workloads are not public. [S3] | A public original-circuit/observable/parameter regression fixture complements the documented check. Do **not** “fix” Cliffordization by removing an intentional cheap option-path test. Actual acceptance of an added runner is unknown. |
| QED-C/NVIDIA port authors/reviewers | PR **#838**, created 2026-10-07, remains draft: “Merge cudaq-multi-agent-staged into master – DRAFT – for review.” Visible commits include output-analysis rescaling, width overflow, QFT FP32 precision, parameterized CUDA-Q result validation and alignment of noise defaults. [S7] | This is a real review task and evidence that semantics exceed imports. It is not an explicit request for an outside referee. Parent is separately checking the migration paper methods/results/contact; this report does not independently repeat its error-rate or cost claims. |
| MQT QCEC | Current README explicitly invites contributed code, tests, examples, and feedback/use cases. Open-issue API on 10-23 returned only a dependency dashboard, not a named migration feature request. [S4] | A concrete worked adapter/example is a plausible contribution, **not** validated backlog demand. An empty issue search cannot prove no need. |
| Taxonomy-RAG research authors | June 2026 paper §6 explicitly proposes moving beyond synthetic snippets to public projects and adding syntactic/semantic pre/post execution validation. [S9] | An author-stated research direction, not a product/customer request. Their paper already pursues migration automation. |

There is no verified monetary cost, purchase intent, weekly frequency, or confirmed post-hackathon user in these artifacts.

### Reconciling API-drift repair numbers

The July 2026 study uses 50 adapted HumanEval tasks, Qiskit **0.43.3 / 1.3.0 / 2.0.0**, Python 3.10, 17 model configurations, three generated samples per task/version. Sixteen REST configurations have a 1,024-token cap; Codex CLI is a separately reported reference. Repair is **one attempt** using failing code, error trace, migration notes, and original task; only code passing its prompted version and failing a later one qualifies. Harnesses intentionally use structural/type/return-presence assertions, so quantum correctness is not guaranteed. [S2 §§2, 6]

- **19.2–59.1%**: overall repair across *both* destinations for sixteen matched REST models.
- **95–100%**: selected stronger models' repairs **toward v2.0**, not all models or arbitrary notebook migrations. Grok: 19/20; Opus: 14/14 (95% Wilson interval 78.5–100%); GPT-5.4 API: 26/26 (87.1–100%); Codex CLI reference: 19/19 (83.2–100%). Sonnet: 20/22 = 90.9%.
- The same Opus is **20/65 = 30.8% overall**, because v1.3 repairs are 6/51; GPT-5.4 API is 27/97 overall, with 1/71 to v1.3. Both prior summaries were selective, not contradictory. Do not infer that agents either universally solve or universally fail migration. [S2 Tables 4, 10]

The taxonomy-RAG paper's **81 is a count, not 81%**: Table 1 gives Gemini restrictive mode 81 “OK” scenarios out of 110 detected; the unit is expert-rated scenario/suggestion, not fully revived projects. Table 2 has inconsistent counts versus Table 1, and the authors explicitly leave real projects and semantic execution for future work. It cannot establish an end-to-end migration success rate. [S9 §§3–6]

## 2. Existing solutions really do compare semantics

| Existing solution | Verified features / remaining boundary |
|---|---|
| **MQT QCEC**, MIT, latest checked commit `57802471fd7a6f840b9fea94ee6ed71e1251d29f` (2026-10-23); PyPI **3.11.0** | One-call `verify`/`verify_compilation`; DD and ZX engines; simulation-based falsification; symbolic parameters; layout permutations and measurements; partial equivalence over measured outcomes with ancillary/garbage handling. Partial equivalence is **not enabled by default**. Simulation-only checks do not prove equivalence; timeout/no-information is inconclusive. Does not certify whole Python/runtime behavior. [S4–S6] |
| **IBM `Qiskit/skills`**, Apache-2.0, commit `a5499c7c24f51633cbd0a5e7ea5902841e5b983e` (2026-10-06) | Grounded, version-aware runtime migration; explicitly protects results-changing decisions; local option validation, not just import rewriting. Behavioral gap is acknowledged, not an unknown vendor oversight. Broader Qiskit migration appears on its non-contractual 2027 roadmap. [S3] |
| **flake8-qiskit-migration** | Current README checks removed **imports, methods and arguments** for both 1.0 and 2.0, with notebook integration via nbQA and documented heuristic false positives. The old claim “imports only” is outdated. No execution or semantic comparison is advertised. Repository is **`qiskit-community/flake8-qiskit-migration`**, not `Qiskit/...`. [S10] |
| **QED-C benchmark's own oracle** | Grover README already defines analytic expected output distribution, width/marked-item sweeps and noise-normalized fidelity. This is already a semantic test, not an import smoke. A second report must catch something outside/hidden by that existing metric or reduce actual review labor. [S7, S11] |
| **Plain agent + Aer/Qiskit quantum_info + pytest** | Existing probe demonstrates that small deterministic checks are cheap to construct. [S0] [INFERENCE] This is the strongest simple substitute for a new product. Avoid treating a dashboard around those checks as a moat. |

Search also surfaced *LLM-Powered Quantum Code Transpilation*, arXiv **2507.12480v1**. It is **discovery-only here**: methods/results were not read and parent was asked to route that additional paper read. It cannot support a novelty or performance conclusion. No conclusion in this report rests on “no competitor found.”

## 3. Three genuinely different deliverables

### A. Independent QRef — bounded migration comparison, not certification

**User/job/input/output:** an external port reviewer provides original and ported entry points plus explicit semantic input contract; receives per-input circuit verdict, option differences, decoded output comparison and unsupported/inconclusive surfaces. Original environment is a reference, not a correctness oracle for the science.

**Smallest complete 12-hour artifact [INFERENCE]:** two pinned subprocess environments; exactly one Qiskit static-circuit boundary; parameter/input sweeps; exact classical-bit distributions; deterministic replay through unchanged classical post-processing; JSON plus readable report. No cloud runtime, adaptive optimizers, arbitrary notebook discovery, dynamic-circuit promise, or “signed certificate.” Existing probe code is prior work and must be disclosed if reused.

**AI vs plain coding agent:** AI proposes the port; independently frozen deterministic checks arbitrate. The referee needs no LLM. Extra value must be demonstrated by an unseeded discrepancy or materially lower reviewer work than an agent writing standard tests.

**Data/compute/license:** artifacts below; Qiskit/Aer Apache-2.0, QCEC MIT; CPU only, 4–8 qubits; public source only. Two small model migrations, maximum two repairs each and a hard token/cost cap; monetary estimate requires the selected provider's current price, not the old report's inferred price.

**Adoption:** local CLI/CI evidence attached to a real QED-C review, not a hosted arbitrary-code-upload service. **Reject:** broad semantic core is already QCEC; extraction/pairing/postprocess is brittle; current probe has only planted failures. No independent customer commitment.

### B. End-to-end single-notebook revival — stronger job, weaker differentiation

**User/job/input/output:** instructor/researcher has a specific legacy notebook and wants to rerun its local experiment. Input is immutable notebook snapshot and declared cells; output is a runnable migrated notebook, exact lock/environment, visible patch, original-vs-modern distributions/observable summary, and unresolved behavioral decisions. This completes a user's task rather than asking them to supply both ports.

**Smallest complete 12-hour artifact [INFERENCE]:** fully revive the QAOA notebook below including its plotting and optimizer cells, while separately checking fixed input/parameter points. Preserve every scientific change as an explicit decision: do not silently repair an apparent old shots typo while calling it migration preservation. Report optimizer-path divergence separately rather than equating a changed optimum to a bug. Retain license/attribution. No arbitrary repository URL promise.

**AI vs plain agent:** documents-guided patching plus environment diagnosis; ordinary Claude/Codex can already do it. Quantum-specific checks add protection at angle/bitstring/objective boundaries, not better package installation.

**Data/compute:** same CPU/pins as below, modest small-circuit simulation. **Adoption:** deliver a requested notebook patch to its current instructor/author and integrate checks into that repository. The archived textbook has no shown active recipient; using it for the demo does not establish adoption. **Reject:** most measured value may be a generic Python environment fix; archived examples may not be worth updating; restoring full notebook UI/runtime support can consume the build.

### C. IBM/MQT contribution — preferred, conditional on recipient

**User/job/input/output:** skill reviewer receives a real agent transcript and a bounded regression fixture: source/target versions, circuit + observable + parameter values + measurement map + options, with independent output evidence. IBM's cheap Cliffordized verification remains; the added local fixture exercises the **unmodified small scientific circuit** and classical decoder instead.

**Smallest complete 12-hour artifact [INFERENCE]:** one runnable migration example with pinned before/after environments, report generation, and an end-to-end agent transcript, shaped as a draft contribution; reuse QCEC rather than implementing an equivalence engine. Either (i) IBM runtime local observable/parameter regression **if a maintainer supplies/accepts a public compatible case**, or (ii) an MQT worked migration-boundary example using QAOA. These are alternatives, not a promise to implement both. A textbook-only core Qiskit migration is **not** falsely described as testing IBM's runtime skill.

**Evidence/adoption:** IBM CONTRIBUTING explicitly requests this form of evidence, with issue-first discussion and a CLA; MQT invites examples. QED-C can consume an independent check as a port review artifact. None guarantees merge or recurring usage. **AI contribution:** agent migration is the system under evaluation; bounded transcripts make its behavior reviewable. **Data/compute:** Apache/MIT fixtures, CPU, no credentials/hardware or proprietary internal evals. **Reject:** maintainer may prefer a tiny example or correction over a new runner, or internal validation may already cover the case. If so, contribute the tiny useful thing, not a new brand.

## 4. Clean public smoke inputs and exact proposed pins

This source investigation did not execute the proposed smoke. The parent subsequently ran the QAOA helper experiment: [actual results and limits](workflow-checks.md). The environment pins below have been corrected to match that run; the Grover control remains unexercised.

### Artifact 1 — real legacy QAOA notebook (best first experiment)

Snapshot: [`qiskit-community/qiskit-textbook@0ae905083ec3872d7ddc6bb4001d5468f476d93f/content/ch-applications/qaoa.ipynb`](https://github.com/qiskit-community/qiskit-textbook/blob/0ae905083ec3872d7ddc6bb4001d5468f476d93f/content/ch-applications/qaoa.ipynb). All code cells read. Last main commit is **2023-05-30**; repository pushed **2024-11-05**, archived. Do not call the push date the source's last commit. Root `LICENSE.txt` is Apache-2.0; `content/LICENSE.md` is actually zero bytes, not an additional license. The unpinned requirements are not a reproducibility lock. [S8]

Real surfaces: `from qiskit import Aer, execute`, `create_qaoa_circ(G,theta)` splitting beta/gamma by position, `compute_expectation` reversing bitstrings, Aer execution, COBYLA and plots. Existing graph is a four-cycle; no seeded bug. Cell 18 sets `backend.shots` and passes `nshots=512` rather than `shots`. The parent measured 1,024 completed shots in the old runtime, regardless of requested 512 or 17; the port honors the requested setting. Its model notes disclosed that intended correction. Only the helper functions were run, not the full notebook.

Exercised helper environments: **Python 3.11.12; networkx 2.8.8; scipy 1.17.1**. Source: **qiskit 0.46.3; qiskit-aer 0.14.2; numpy 1.26.4**. Target: **qiskit 2.6.1; qiskit-aer 0.18.0; numpy 2.4.6; mqt.qcec 3.11.0**. The proposed shared NumPy 1.26.4 pin failed because Qiskit 2.6.1 requires NumPy 2. Use isolated environments and the [recorded exact dependencies](https://github.com/SeivenBell/tq-ledger/tree/research/round2-qaoa-probe/prototypes/round2-qaoa), not the earlier untested full-notebook package proposal.

Freeze the notebook's original four-cycle as an exact provenance case. Additional **declared** contract inputs (not defects): 4-node asymmetric edges `[(0,1),(1,2),(2,3),(0,2)]`, and a 5-node graph. Sweep p=1 and p=2 with parameter lists `[0.17,0.63]`, `[0.81,0.29]`, `[0.17,0.63,0.41,0.92]`. These inputs exercise positional angle binding and endian-sensitive objective decoding without modifying original code. Do not call newly chosen inputs hidden author tests.

### Artifact 2 — maintained QED-C Grover kernel (clean circuit-semantic control)

Snapshot: [`SRI-International/QC-App-Oriented-Benchmarks@21dfc331ce61a2170b06f88259aa19f901c021bc/qedcbench/grovers/qiskit/grovers_kernel.py`](https://github.com/SRI-International/QC-App-Oriented-Benchmarks/blob/21dfc331ce61a2170b06f88259aa19f901c021bc/qedcbench/grovers/qiskit/grovers_kernel.py). Full kernel and algorithm README read; repo API reports Apache-2.0; last main commit **2026-10-07**, last repository push **2026-10-23**. `GroversSearch(num_qubits, marked_item, n_iterations, use_mcx_shim)` returns a measured circuit and explicitly reverses marked-item bits. Existing native-vs-shim MCX implementations supply a naturally different, intended-equivalent pair; neither was planted for this demo. [S11]

Use the **target environment above** for both native and shim; this is a control/integration input, **not a broken legacy notebook**. Widths 3,4,5; non-palindromic marked values 1,2,5; iterations 1,2; both shim settings. Compare against its analytic expected distribution, and against QCEC after appropriate decomposition. A correct pass is valuable evidence that the checker tolerates implementation changes, but not a migration-error showcase. Avoid pretending this verifies the CUDA-Q branch: that needs a separate adapter/environment and agreed port contract.

## 5. Deciding experiment and honest quantum-specific acceptance

Parent should exercise one short, bounded experiment **before committing the build**, not run a broad migration census:

1. Freeze source bytes, pins, supported input contract and limits; run original QAOA locally and record emitted bound circuits, effective shots, full measurement map and decoded objective. If source cannot run, classify environment/API failure separately; never invent a baseline.
2. Ask the normal coding agent to port it without changing the frozen inputs/reference harness. Preserve the real agent transcript, output diff and all unsupported decisions. Maximum two repair rounds.
3. **Circuit level:** compare corresponding bound circuits with QCEC (retain exact status/options); independently compute exact probabilities on these small noiseless circuits with the declared classical-bit map. TVD tolerance 1e-9 is a proposed numeric threshold, not universal scientific equivalence. A zero-initial-state distribution match does not prove the same operation on arbitrary input states.
4. **Hybrid level:** feed the same deterministic counts/probabilities through each version's unchanged decoder, compare expected MaxCut objective, and log angle/parameter assignment and effective-shot defaults. Pair circuits by declared graph/parameter/input keys, not submission order. Matching printed numbers alone is inadequate.
5. **Nontrivial positive control:** native and shim QED-C Grover should agree despite different gate structure. Compare to its existing analytic oracle. This distinguishes useful quantum semantics from an import/container smoke, and exposes redundant new tests.
6. Report **PASS on this declared scope / FAIL with counterexample / INCONCLUSIVE or unsupported**, never “runtime/program equivalent.” Dynamic feed-forward, noise and cloud-service options are explicitly unexercised. No planted mutation counts enter the unseeded result.

**Keep** only if a practitioner identifies a case/review they would actually use, and the new boundary report supplies a specific check absent from their current workflow or demonstrably saves review work. **Kill/redirect criteria:**

- All useful differences are already explained by QCEC/analytic expected-distribution checks; upstream the wrapper/example, not a competing checker.
- Ordinary agent migration plus a small existing pytest/Aer test produces the same evidence with no additional review burden removed.
- No honest semantic/default/postprocessing discrepancy and no reviewer values a clean positive report: do not manufacture a red demo.
- No runnable old baseline, or corpus requires hardware, secrets, proprietary artifacts or arbitrary adaptive notebook interception: reject that corpus rather than expanding scope.
- More than the single bounded static workflow is required for a credible user outcome: reject a 12-hour universal revival promise.

## 6. Verified contact and inquiry draft

**Public official contact:** Dr. Lukas Burgholzer, MQT QCEC author, **lukas.burgholzer@tum.de**, shown on his [TUM chair page](https://www.cda.cit.tum.de/team/burgholzer/); current QCEC package also names him. Official role currently “Postdoc.” No email was inferred from a naming convention. IBM contact lead is Jessie Yu (`jyu00`) via [skills PR #8](https://github.com/Qiskit/skills/pull/8); her public GitHub profile has **no email**. [S13, S3]

No one may send this draft without new authorization.

Subject: Checking an old Qiskit notebook after an upgrade

> Hi Lukas,
>
> I'm considering a small open-source contribution to help check old Qiskit notebooks after an upgrade. QCEC already compares quantum circuits. I would check the surrounding code too, such as how it assigns parameter values and converts measurement results into an answer.
>
> Can you point me to one public notebook upgrade where those checks would help?
>
> I can use an Apache-licensed example and provide the exact software versions and a reproducible comparison.
>
> Thanks,
> Severyn

## Source register

All accessed 2026-10-23. `Full` refers to the named artifact, not its outgoing references. No abstract-only paper supports the recommendation.

| ID | Primary source / date | Read depth |
|---|---|---|
| S0 | Local `docs/research/build/qref-probe.md`, compiled 2026-10-23; previous research reports dated 10-22/23 | Full assigned reports; original practitioner report targeted sections. Prior probe results are attributed, not rerun. |
| S1 | [Zappin et al., practitioner manuscript](https://ojcchar.github.io/files/42-tosem25-quantum-test-debug.pdf), manuscript February 2026, observations May–Aug 2024 (**stale data**) | Partial: study design §§4.1–4.5; testing/debugging selected results §§5–6; §7.2; implications §§8.3–8.6; threats §9. Author manuscript displays placeholder DOI; do not claim a verified final TOSEM issue/date. |
| S2 | [API drift paper 2607.04072v1](https://arxiv.org/html/2607.04072v1), 2026-07-05 | Partial: all methodology §2; repair results §3.5, Tables4/10; §6 limitations. |
| S3 | [IBM skill](https://github.com/Qiskit/skills/blob/a5499c7c24f51633cbd0a5e7ea5902841e5b983e/skills/migrate-qiskit-ibm-runtime/SKILL.md), [README](https://github.com/Qiskit/skills), [CONTRIBUTING](https://github.com/Qiskit/skills/blob/main/CONTRIBUTING.md), [PR8](https://github.com/Qiskit/skills/pull/8), [PR4](https://github.com/Qiskit/skills/pull/4); latest commit 2026-10-06; PRs Sept25/29 | Skill partial (Phases1–6); README and contribution guide full; PR/API bodies full; repo/license/commit metadata. |
| S4 | [QCEC README](https://github.com/munich-quantum-toolkit/qcec), main commit 2026-10-23; [issues API](https://api.github.com/repos/munich-quantum-toolkit/qcec/issues?state=open&per_page=30) queried10-23 | README full; API open issue list and repository/license/commit metadata. |
| S5 | [QCEC equivalence guide](https://mqt.readthedocs.io/projects/qcec/en/stable/equivalence_checking.html), live undated, read10-23 | Full. Documentation API/features may differ from older installed releases; pin and exercise before using. |
| S6 | [Partial equivalence](https://mqt.readthedocs.io/projects/qcec/en/stable/partial_equivalence.html), [compilation verification](https://mqt.readthedocs.io/projects/qcec/en/stable/compilation_flow_verification.html), live undated | Full both. |
| S7 | [QED-C PR838](https://github.com/SRI-International/QC-App-Oriented-Benchmarks/pull/838), 2026-10-07; [PR812](https://github.com/SRI-International/QC-App-Oriented-Benchmarks/pull/812), 2026-04-19 | Partial: draft/review status, visible commit titles; PR812 API body describing ideal-distribution comparison. No independent source-code verification of every CUDA-Q repair. |
| S8 | [QAOA notebook](https://github.com/qiskit-community/qiskit-textbook/blob/0ae905083ec3872d7ddc6bb4001d5468f476d93f/content/ch-applications/qaoa.ipynb), [root license](https://github.com/qiskit-community/qiskit-textbook/blob/0ae905083ec3872d7ddc6bb4001d5468f476d93f/LICENSE.txt), [requirements](https://github.com/qiskit-community/qiskit-textbook/blob/0ae905083ec3872d7ddc6bb4001d5468f476d93f/requirements.txt), source commit2023-05-30 (**stale deliberately**) | All QAOA code cells and metadata; full license/requirements; repo/commit/tree metadata. Also inspected teleportation/Grover code cells as rejected higher-environment-complexity alternatives (credentials/old providers). |
| S9 | [Qiskit Code Migration with LLMs 2606.20173v1](https://arxiv.org/html/2606.20173v1), 2026-06-18 | Main text §§1–6 full, including methods/results; references not exhaustively followed. |
| S10 | [Migration linter README](https://github.com/qiskit-community/flake8-qiskit-migration), live undated read10-23 | Full README. Not proposed as a pinned build dependency; latest commit/license were not independently rechecked here. |
| S11 | [Grover kernel](https://github.com/SRI-International/QC-App-Oriented-Benchmarks/blob/21dfc331ce61a2170b06f88259aa19f901c021bc/qedcbench/grovers/qiskit/grovers_kernel.py), [algorithm README](https://github.com/SRI-International/QC-App-Oriented-Benchmarks/blob/21dfc331ce61a2170b06f88259aa19f901c021bc/qedcbench/grovers/README.md); main commit2026-10-07 | Full both; repo Apache-2.0/license and main commit verified via GitHub API. |
| S12 | [QCEC PyPI JSON](https://pypi.org/pypi/mqt.qcec/json), current release3.11.0, queried10-23 | Partial: package version, Python/dependency/license/author metadata, not historical release file inventory. |
| S13 | [Official TUM Burgholzer profile](https://www.cda.cit.tum.de/team/burgholzer/), live undated read10-23; [Jessie Yu GitHub profile API](https://api.github.com/users/jyu00), queried10-23 | Profile partial: role/contact; GitHub name/email fields. |

No builds, tests, formatters, migrations, commits, pushes, or external messages were performed. Parent owns the deciding smoke and synthesis.
