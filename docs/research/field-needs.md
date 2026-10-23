# FTQC field needs: circuit cost reduction, verification, resource estimation — and who the users are

Research date: 2026-10-19. Written for a 20-hour solo Build North project that needs a credible "real user + path to production".
Read-depth labels: **full**, **partial (sections …)**, **README/docs**, **snippet-only** (search-result text only, unverified), **abstract-only** (unverified).
Lines marked `[INFERENCE]` are my own analysis or arithmetic. The sources do not state them.

---

## 0. Bottom line

1. **Most FTQC cost sits in a few classical-function subroutines.** In RSA, ECC, DQI and chemistry estimates, most Toffolis go to modular arithmetic (additions, multiplications, modular inversion), table lookups/QROM, reversible decoders, or coefficient loading plus rotations. Each estimate below states this directly.
2. **No neutral, verified registry of best-known subroutine costs exists.** Each paper uses its own cost convention: $T\cdot Q$, $q^3 t$, active volume, or *average executed* Toffolis. Each also uses its own failure budget (≤1e-3, ≤2e-4, ≤1%) and its own billing rules (for example, whether lookups that supply a classical addend are counted). Tools such as Qualtran, the Microsoft QRE, Bartiq and TopQAD *aggregate* costs. None of them certifies that a subroutine is correct or that it is the best known. The 2610.22367 repo (`andigu/uncompute`, Apache-2.0) has the first hash-seeded, certifiable evaluator, but only for its own 8 tasks.
3. **Verification and trust are now a research topic in their own right.** Google published a zero-knowledge (ZK) proof of its ECC circuit costs instead of the circuits. DARPA QBI has an IV&V topic. Canada's CQCP uses NRC "Benchmarking Quantum Platforms" for evaluation. These are concrete users who need auditable resource claims.

---

## 1. Where Toffoli and logical-qubit costs concentrate in flagship estimates

| Application / estimate | Headline logical cost | Physical / runtime | Dominant subroutines (as the source states) | Source & read depth |
|---|---|---|---|---|
| **RSA-2048**, Gidney 2025 (arXiv 2505.15917) | **6.5e9 Toffolis** expected per factoring, **1,399 logical qubits** (parameters chosen to minimise $q^3 t$; s=8, ℓ=21, w1=6, w3=3, w4=5, f=33, m=1280); P_deviant 1.25 %, E(shots) 9.2 | <1M physical qubits (≈900k + slack), ~12.07 h per shot, <1 week total; 0.1 % gate error, 1 µs cycle, 10 µs reaction | "Essentially all work performed by the algorithm is addition, lookup, and 'phaseup' operations." n-qubit addition = n−1 Toffolis. Lookup = $2^n-n-1$ Toffolis. Phaseup ≈ $\sqrt{2^n}$. Runtime assumes 2 ms per addition, 2 ms per lookup, 1 ms per phaseup. A 6-address lookup needs ≥57 CCZ states but **63 lattice-surgery layers**. Qubit savings come from approximate residue arithmetic (CFS24), yoked-surface-code cold storage (430 vs 1,352 physical qubits per logical qubit) and magic-state cultivation. Code on Zenodo. | **partial** (abstract, §1, §2.4, §3.1, Table 5, §3.2, App. A.4) |
| **ECDLP-256 (secp256k1)**, Babbush et al. 2026 (arXiv 2603.28846, PRX Quantum 7, 031001) | **≤1,200 logical / ≤90M Toffolis** or **≤1,450 / ≤70M** | <500k physical (superconducting, 1e-3, 4-connectivity); ~9 min per key on fast-clock hardware (needs ~5e5 T states/s, i.e. ~25k physical qubits for magic) | Point addition is "the primary bottleneck". 28 windowed point additions (w=16), each costing $\text{PA}+3\cdot2^{16}$ Toffolis for lookups. Point-addition circuits are ZK-attested at **≤2.7M Toffolis / ≤1,175 qubits** and **≤2.1M / ≤1,425**. These are *average executed* Toffolis over 9,024 Fiat-Shamir tests, with ≥99 % of inputs correct. The circuits themselves are **not disclosed**. | **partial** (abstract, §II.1–II.2, App. A.1–A.7) |
| **ECDLP-256**, Litinski 2023 (arXiv 2306.08585) | 109M Toffolis per key with 6,000 logical qubits (baseline architecture); amortised (44 + 65/k)M with k parallel instances | Active-volume architecture: one key every 16 h at 1 ms cycle vs 160 days on baseline | Modular inversion costs $26n^2+2n$ Toffolis. That is ">10 times more expensive than a multiplication" ($2.25n^2+9n$) and "the dominant contribution to the cost of elliptic curve point addition". Each step also includes a $2^{16}$-entry lookup of 768-bit numbers. | **partial** (overview, arithmetic section, §2.1–2.3) |
| ECC point addition inside 2610.22367 (SI II) | Divstep circuit: 4.0M Toffolis, 935 qubits | — | "The four divstep walks use 2.5 million Toffolis, **63 %** of the circuit. The field multiplications around the walks use 1.4 million, 35 %." Modular inversion again dominates. | **partial** (SI II, Table S3) |
| **DQI / OPI**, Khattar et al. 2025 (arXiv 2510.10967) | (m=4095, n=70, b=12): **5,717,729 Toffolis, 1,885 logical qubits**; >1e23 Prange trials classically | ~800k physical, ~1 h (16 min per shot; d=21 hot, 2D-yoked cold storage; cultivation only, no distillation factories) | "The efficiency of the reversible decoder dominates the resource requirements of the entire DQI algorithm." Gate cost is dominated by quantum–quantum and quantum–classical GF multiplications. The EEA (Euclidean) solve plus its reversal accounts for 3.8M of the 5.1M decoder Toffolis (per Gu et al.'s re-implementation). In the OPI regime, Chien search and Forney are O(mn). Code on Zenodo. | **partial** (abstract, §I, Table 5 discussion, Table 6, §V.2) |
| DQI original, Jordan et al. 2024 (arXiv 2408.08292, Nature 646) | — | — | Not read. The decoder-dominance claim is taken from Khattar et al. | **not read** |
| **Chemistry: FeMoco, THC qubitization**, Lee et al. 2021 (arXiv 2011.03494) | **6.7e9 Toffolis** (483k inner loops × 13,880 Toffolis), Reiher Hamiltonian | ~4M physical, <4 days (d=31; floorplan 53×36 = 1,908 logical patches including routing/factories; 4 CCZ factories at 25 kHz) | "The dominant costs are from the QROM and the rotations." THC reduces QROM cost; rotation cost is unchanged. "Most qubits are used for routing and distillation." | **partial** (abstract, §IV.3 layout, App. sections on QROM; via targeted search) |
| Gu et al. task set (8 primitives) | See §3 | — | Function evaluation (HRS piecewise polynomials: QROM coefficient lookup + multiply-adds); alias-sampling Select (Fe2S2); lattice-gauge running products (W updates = 110k of 170k Toffolis) | **partial** |

**Cross-cutting observations** `[INFERENCE]` drawn from the rows above:
- Four primitive families account for most cost: (i) adders and modular add/multiply, (ii) **table lookup / QROM** together with its measurement-based-uncomputation (MBU) phase fix-up ("phaseup"), (iii) **reversible control-heavy algorithms** (modular inversion, GCD/Euclid, Berlekamp–Massey decoders), (iv) **rotations** (chemistry). Category (iii) is where 2610.22367 found its largest gains, because naive reversible compilation wastes the most there.
- **Subroutine gains are not end-to-end gains.** Example: Khattar's full DQI instance is 5.72M Toffolis, and the decoder stage alone is 5.0M per Gu et al. That leaves ≈0.7M for non-decoder stages. Swapping in Gu's 0.44M decoder gives ≈1.1–1.2M total: about **5×** end-to-end, not 12×. `[INFERENCE: assumes the other stages are unchanged]`
- In the flagship estimates, physical cost depends on more than T·Q: lattice-surgery layers per lookup, reaction time, hot vs cold storage, and factory count (Gidney uses 6 factories, 3×4 patches each).

---

## 2. Tools practitioners use today

| Tool | Owner | License (verified via GitHub API, 2026-10-19) | What it does | Registry of arithmetic circuits with best-known costs? | Automated search? | Main gap for this use case | Read depth |
|---|---|---|---|---|---|---|---|
| **Qualtran** | Google Quantum AI (`quantumlib/Qualtran`, 400★, pushed 2026-10-19) | Apache-2.0 | "Bloqs" language plus a library: arithmetic, `mod_arithmetic`, `gf_arithmetic`, `gf_poly_arithmetic`, `cryptography/ecc` and `rsa`, chemistry, QROM/data loading. Symbolic T/Toffoli and qubit counting. `surface_code` physical models (CCZ2T, 15-to-1, Beverland et al., "flasq" cultivation). Classical simulation of reversible bloqs (`call_classically`, `assert_consistent_classical_action`). | **Partial.** The bloq library is a de facto collection of published constructions with symbolic costs. It is not a ranked "best-known" leaderboard, has no certificates, and has no failure-budget column. | No | No failure-budget accounting for approximate arithmetic. No search. "Experimental preview, no backwards compatibility". | README/docs + repo tree |
| **Microsoft Quantum Resource Estimator** (in `microsoft/qdk`, `source/qre`) | Microsoft | MIT | Layered models (application trace × architecture ISA × QEC/factory). Explores code distances, factories and decompositions; outputs a Pareto frontier of physical qubits vs runtime under an error budget. Inputs: Q#, Cirq, OpenQASM, QIR, logical counts. Photonic Inc. is extending it for distributed/qLDPC (SHYPS) architectures (announced 2026-09-23). | No | Design-space sweep only, not circuit search | The algorithm is given as input. It does not improve or verify subroutines. | docs (MS Learn intro, 2026-06) |
| **pyLIQTR** | MIT Lincoln Lab (repo `isi-usc-edu/pyLIQTR`) | MIT | Problem instances (Hamiltonians), block encodings, QSP/QSVT, Clifford+T resource estimates. Built on Cirq + Qualtran. Comes from the DARPA QB program lineage. | No (has application *instances*, not arithmetic best-knowns) | No | Focused on simulation/chemistry block encodings; T-count only | README |
| **Bartiq + QREF** | PsiQuantum (`PsiQ/bartiq` 57★, `PsiQ/qref`) | Apache-2.0 (both) | Symbolic resource compilation: a routine tree with local symbolic costs (T, Toffoli, active volume, qubits) rolled up into global formulas. QREF is the JSON exchange format. | No | No | Costs are author-asserted symbols, not verified circuits | README |
| **TopQAD** | **1QBit** (Severyn's employer) | Proprietary / licensed; `topqad-sdk` on PyPI | QRE service: Compiler (to Pauli-rotation ISA) → Noise Profiler (surface code + PyMatching, cultivation) → Assembler (microarchitecture, MSF design). Pareto space–time, $/qubit-second cost, error-budget breakdown (synthesis / core / MSF). Decoder-latency models (Riverlane etc.) added in v0.5.0 (2026-07-20). Used in the HPE-led DARPA QBI Stage A consortium. | No | Architecture optimisation, not circuit discovery | Starts from a supplied circuit or from (T-count, qubits) "Lite" inputs. **Direct overlap with any physical-QRE dashboard.** | docs (QRE page, news) |
| PennyLane resource estimation | Xanadu (`PennyLaneAI/pennylane`) | Apache-2.0 | Analytic estimators for chemistry (first-quantization, double-factorization) and resource tracking | No | No | Chemistry-centric | not read (repo metadata only) |
| Qiskit / Cirq arithmetic libraries | IBM / Google | Apache-2.0 | Generic adders, multipliers, comparators (Qiskit circuit library). Cirq's FT bloqs moved into Qualtran. | No | No | Not tuned to FT Toffoli/MBU costs | prior knowledge `[INFERENCE]`, repo metadata only |
| Q# standard arithmetic | Microsoft (`qdk`) | MIT | Ripple-carry/lookahead adders, comparisons; integrated with the QRE | No | No | Same as above | not read |
| Qrisp | Eclipse/Fraunhofer (`eclipse-qrisp/Qrisp`) | EPL-2.0 | High-level arithmetic types, automatic uncomputation | No | No | — | repo metadata only |
| **PyZX** | `zxcalc/pyzx` | Apache-2.0 | ZX-calculus rewriting, T-count optimisation, equivalence checking | No | Rewrite-based only (keeps the same design) | Cannot change the algorithm. 2610.22367 notes such optimisers are "limit[ed] … to variations of a fixed design". | repo metadata |
| **Feynman** | Matt Amy (`meamy/feynman`) | BSD-3 | Path-sum verification (`feynver`) and optimisation (`feynopt`); benchmark folder (.qc/QASM) | Small benchmark set, not best-known FT costs | No | Haskell; .qc only for verification | README |
| MQT QCEC / MQT Bench | TUM (`munich-quantum-toolkit/qcec`, `/bench`) | MIT | Equivalence checking; NISQ-oriented benchmark suite | No (not FT arithmetic) | No | — | repo metadata |
| RevKit / RevLib / mockturtle | Soeken et al. / EPFL LSI | MIT (RevKit last push 2019; mockturtle active) | Reversible/logic synthesis. RevLib.org is a benchmark database of reversible functions with circuit realisations (still online). | RevLib is the closest historical "registry", but it targets NCV/quantum-cost metrics and small functions, not FT Toffoli/qubit/failure budgets | Synthesis heuristics | Pre-FT cost models; stale | site check |
| Quipper | Selinger et al. (Dalhousie) | BSD (site) | Haskell circuit language with automatic reversible synthesis from classical code | No | No | Research-only | site check |
| benchq | Zapata (`zapatacomputing/benchq`) | Apache-2.0 | FT resource estimation | No | No | Last push 2025-03 | repo metadata |
| **`andigu/uncompute`** (2610.22367 artefact) | Gu et al. | **Apache-2.0** (3★, pushed 2026-10-16) | 8 tasks, each with `grader.py` (test distribution + failure budget), `reference.py`, `contract.json` and certified `results.jsonl`. Baseline and discovered circuits as `.ops.xz` op streams. Exact kickmix evaluator (Python + optional C kernel). Liveness/occupancy profiling. Lean 4 proofs (divstep bound + branch recovery; DQI decoder-error bound). **Test inputs are derived from a hash of the emitted circuit.** | **Yes, a seed:** certified T/Q for 8 tasks, plus baselines | **No:** the OpenEvolve search harness and prompts are not in the repo | Only 8 tasks; only the TQ objective; no physical layer; no submission/leaderboard mechanism | README + tree + 2 graders |
| OpenEvolve | `algorithmicsuperintelligence/openevolve` (7.6k★) | Apache-2.0 | Open AlphaEvolve-style evolutionary coding agent; the search engine used in 2610.22367 | — | Yes | Generic | repo metadata |

**Gap summary** (from the rows above):
- **No verified best-known-circuit registry for FT subroutines.** Qualtran holds constructions, Bartiq holds formulas, RevLib is pre-FT, and `uncompute` covers only 8 tasks.
- **No common cost convention.** Examples: $T\cdot Q$ (Gu); $q^3 t$ (Gidney: "cubing q is just an arbitrary way of favoring space"); active volume (Litinski); *average executed* Toffolis (Babbush ZK). In Gu's modinv grader, "a bit-conditioned CX counts as a Toffoli", while its Table S3 *excludes* the lookup that supplies the classical addend.
- **Failure-probability accounting is ad hoc.** Gu allows ≤100 of 1e5 failed shots (RS decoder) or ≤20 of 1e5 (modinv); Babbush proves ≥99 % correctness; Gidney accepts P_deviant = 1.25 % per shot. Physical-QRE tools (MS QRE, TopQAD) budget for logical, synthesis and factory errors; algorithmic-approximation failure must be added by hand. `[INFERENCE for MS QRE: based on its documented error-budget model, not re-verified this session]`
- **No tool links an LLM/evolutionary search to a verifier and a physical estimator.** 2610.22367 does search + verifier with a TQ objective. QREs do the physical layer with no search.

---

## 3. arXiv 2610.22367: what it actually does, the 8 benchmarks, and where its claims are weak

**Read depth: partial.** Main text and Methods read in full (circuit model, validation/statistics, cost model, evolutionary search). Extended Data Table 1 read in full. SI I (DQI) and SI II (modinv) read in part. SI III–V and Appendix A skimmed via targeted search.

### 3.1 Method vs abstract
- The abstract says "LLMs propose circuit designs and an independent evaluator verifies and scores them". **This is accurate.**
- Candidates are *Python programs* built on a `Builder` API (alloc/free, ccx, Clifford gates, MBU via `hmr`). Circuits use the **kickmix** model (Babbush et al. 2026): X/CNOT/Toffoli/SWAP, diagonal Z/CZ/CCZ, destructive X-basis measurement. Because every operation keeps a basis state as a basis state, each test is a bit-string-plus-sign trajectory.
- The evaluator checks four things: outputs, *exact global sign*, every ancilla returned to 0, and distinct operands. Inputs are drawn from a task distribution, and each test also samples measurement outcomes.
- Search: OpenEvolve + **"Claude Mythos 5"**. An ideation stage proposes ≤5 "algorithm families" per task. Each iteration runs a fresh agent session (parent program, feedback, archive excerpts, "DISCOVERY:" notes) and may run drafts, query a classical oracle, and use subagents. MAP-Elites runs over a (T,Q) grid. Best TQ across families is reported.
- **Compute, token and dollar budgets, and iteration counts are not reported** (searched the text for hours/GPU/USD/iterations; none found). This is a reproducibility gap.
- **Code:** `github.com/andigu/uncompute`, Apache-2.0: circuits, tasks, evaluator, Lean proofs. **The search harness and prompts are not released**; Extended Data Fig. 1 shows only example prompts.

### 3.2 Benchmark table (Extended Data Table 1; also repo README)

| Task | Input/output qubits | Correctness criterion | Tests | Baseline (T, Q) [source] | Discovered (T, Q) | $G_{TQ}$ |
|---|---|---|---|---|---|---|
| Prime-field modular inversion (inside secp256k1 point addition) | 512/512 | Failure budget ≤2e-4 (grader: ≤20 failed of 1e5) | 1e5 | — (several frontiers; see below) | **4.0e6, 935** | — |
| Reed–Solomon DQI decoder (Khattar OPI instance) | 840/— | Failure budget ≤1e-3 (≤100 failed of 1e5) | 1e5 | 5.1e6, 1,938 [Khattar 2025, re-implemented from released code] | **4.4e5, 1,837** | 12 |
| Hermitian-code DQI decoder (HOPI) | 738/— | ≤1e-3 | 1e5 | 1.0e8, 1.9e5 (naive Sakata/Feng–Rao; no prior reversible compilation) | **9.3e5, 2,395** | — (≈9,100× vs naive) |
| HHL rotation angle | 21/33 | Error tolerance (fixed-point bound) | 9e3 | 1.6e4, 300 [Häner–Roetteler–Svore 2018] | **1,348, 115** | 32 |
| Coulomb potential (1/r) | 48/25 | ≤2e-6 absolute error | 9e3 | 6,355, 252 [HRS 2018] | **1,140, 142** | 9.9 |
| Fixed-point Gaussian $e^{-x^2}$ | 39/39 | Error tolerance | 9e3 | 2.4e4, 362 [HRS 2018] | **1,583, 139** | 39 |
| Fe2S2 alias-sampling Select | 32/40 | Exact on entire domain | 2e7 | 5.5e4, 139 [Babbush et al. 2018 linear-T] | **1.5e4, 126** | 4.1 |
| Non-abelian lattice gauge (Σ(72×3) plaquette) | 1,728/51 | Exact | 1e5 | 1.3e6, 1,927 [Osorio Perez et al. 2025] | **1.7e5, 1,859** | 7.7 |

Modular-inversion comparison (SI Table S3, complete point-addition circuits):

| Construction | Toffolis | Qubits | TQ |
|---|---|---|---|
| Schrottenloher 2026 (binary GCD + dialog) | 1.9e6 | 1,446 | **2.7e9** |
| **Gu divsteps** | 4.0e6 | 935 | 3.7e9 |
| Luo et al. 2026 (packed Euclid) | 7.0e7 | 838 | 5.8e10 |
| Gu specialised Euclid | 2.1e7 | 843 | 1.7e10 |
| *For reference:* Babbush ZK point-add (not in Gu's table) | ≤2.7e6 / ≤2.1e6 | ≤1,175 / ≤1,425 | ≤3.2e9 / ≤3.0e9 (upper bounds, average-executed, ≥99 % correct) |

Taken together `[INFERENCE]`: on TQ, the divstep circuit is **not** state of the art. Schrottenloher's construction is better on TQ. Divsteps adds a *new low-qubit frontier point* (935 qubits at 4.0M Toffolis). The authors do not claim a gain, which is consistent with this.

### 3.3 How the paper handles failure probability and verification
- **Per-trajectory checks** cover output, exact sign and ancilla cleanliness, with sampled measurement records. The paper bounds state distance: $\|\Phi_V-\Phi_U\|\le2\sqrt\varepsilon$, so fidelity ≥ $(1-2\varepsilon)^2$.
- **Statistical bound:** if $k$ tests all pass, then with confidence $1-\delta$, $\varepsilon\le1-\delta^{1/k}\approx\ln(1/\delta)/k$. The paper conditions this on "a candidate fixed before the test draw". For DQI it allows ≤100 failures in 1e5 tests. Because a wrong sign is detected with probability ≥½, the result is $\varepsilon\le2.434\times10^{-3}$ at 97.5 % confidence. The authors bound the loss in DQI's satisfied fraction at 5.6e-3 (RS), which is ≤7.4 % of the advantage over Prange.
- **Final certification on larger samples:** RS decoder failure measured at 1.4e-4 over 400M samples, with 7 wrong signs in 1e5 tests. Modinv walk limits checked on 200M random walks; the Euclidean variant on 10M (6.6e-5 + 1.3e-5 per point addition).
- **Formal proofs:** Lean 4 proofs of the divstep step bound (590 steps), the branch-recovery rule, and the DQI decoder-error bound.
- **Test seeding:** tests come from a hash of the emitted circuit, the same Fiat-Shamir idea as Babbush's ZK proof.

### 3.4 Critiques the community is likely to raise
I found no published critiques (the paper is 4 days old; the coverage I found is abstract-level). The list below is my analysis and is labelled as such.

1. **Comparisons at unequal failure budgets.** The discovered RS decoder spends a 1e-3 budget (it keeps 1 history-stack entry instead of 35, i.e. 19 vs 665 qubits). The Khattar baseline is effectively exact on all ≤35-error inputs. A fair comparison gives the baseline the same budget: Khattar's 222 synchronised EEA cycles could be truncated the same way. Across papers the budgets are 2e-4 (Gu modinv) vs ≥99 % correctness (Babbush ZK) vs a 1.25 % shot failure (Gidney). **Needed: a Pareto surface over (T, Q, ε), not a single point.**
2. **Statistical bounds after selection.** Eq. 20 holds only for a candidate fixed in advance. MAP-Elites screens many candidates. Hash-seeded tests stop the search from memorising one test set, but an agent can re-roll tests by making trivial edits. With N screened candidates, the chance that some ε-bad candidate passes grows roughly as N·(1−ε)^k. The final circuits do get large post-hoc validation (400M/200M samples), which largely fixes this for the reported results. But N is never reported, and post-selection hold-out certification is not formalised as protocol. **Needed: fresh-seed hold-out certification, Clopper–Pearson intervals, and a reported number of screened candidates.**
3. **Hardware-aware cost.** The authors accept that TQ is a proxy: "relative importance of qubit count, depth, routing, and measurements depends on … hardware". Missing from the objective: Toffoli *depth* (which matters when factories run in parallel), reaction-limited time, lattice-surgery layers (a lookup is cheap in Toffolis but takes $2^n$ layers), hot/cold storage (Gidney's cold storage is 3× denser), active volume (Litinski), and **neutral-atom specifics**: atom movement time, transversal gates, zoned architectures. The latter matters because QuEra's Libra is the authors' own affiliated hardware.
4. **Baseline vintage and scope.** Three of the eight baselines are HRS 2018 piecewise-polynomial constructions. The lattice-gauge task uses a 4³ lattice instead of the source's 10³. The Hermitian baseline is a naive reversible compilation. Two of eight tasks have no G_TQ at all.
5. **Subroutine vs end-to-end.** A 12× decoder gain is ≈5× on the full DQI instance (see §1). `[INFERENCE]`
6. **Reproducibility.** The model ("Claude Mythos 5") is not openly available, compute is not reported, and the search code is not released. Only the evaluator and artefacts are public.

---

## 4. User personas and evidence of demand
**Deadline correction (2026-10-23):** the P2 row's original Oct 15 date is superseded by **Dec 30, 2026** for DARPA-PA-26-02-01; see the [official opportunity](https://www.darpa.mil/work-with-us/opportunities/darpa-pa-26-02-01), read in full during the ranking synthesis, and `resource-claims-verification.md`. This is a program lead, not demand for our proposed app.


| # | Persona | What they need that is missing today | Evidence (read depth) |
|---|---|---|---|
| **P1** | **FT-algorithm / resource-estimation scientists at hardware and full-stack vendors.** Examples: Google Quantum AI (Babbush, Gidney, Khattar), QuEra applications team (VP Algorithms Shengtao Wang), PsiQuantum (Bartiq team), Microsoft QRE team, Photonic Inc. | Comparable, *verified* subroutine costs under *their* cost model (TQ / q³t / active volume) and *their* failure budget. Fast re-costing when a new construction appears, e.g. CFS24 → Gidney 2025 (100× fewer Toffolis), or Litinski 109M → Babbush 70–90M. | Gidney 2025 and Babbush 2026 (partial). Photonic–Microsoft QRE collaboration on distributed/qLDPC estimates, Sep 23 2026 (full press release). QuEra Libra: >256 logical qubits, 1e-6 LER, Braket 2028; gigaquop system >1,000 logical qubits, 1e-9 LER, 2028–29 (full press releases). QuEra CCO: "The algorithms that will harness fault-tolerant systems at this scale might not yet exist." |
| **P2** | **Program evaluators / independent verification & validation (IV&V).** Examples: DARPA QBI government team, NRC Canada "Benchmarking Quantum Platforms" (for CQCP), ARPA-E QC3 reviewers | Auditable resource claims: a hashed or committed circuit plus reproducible tests plus a stated failure budget. The ability to verify claims without publishing sensitive circuits. | DARPA QBI: Stage B (11 companies incl. **3 Canadian: Nord Quantique, Photonic, Xanadu**); Stage C (Oct 7 2026): Atom Computing, Diraq, IBM, IonQ + Microsoft, PsiQuantum. Target is utility scale by 2033. **QBI Topic IV&V solicitation DARPA-PA-26-02-01** (deadline Oct 15 2026) (full DARPA pages). CQCP: up to CAD $23M each for Xanadu, Nord Quantique, Photonic, Anyon; assessed by NRC (full BetaKit article). Babbush 2026 used an SP1/Groth16 ZK proof over 9,024 Fiat-Shamir tests (partial). |
| **P3** | **Application co-design teams in chemistry/materials** (ARPA-E QC3 performers: LBNL "SuperKIQ", LLNL "MAGNETIQC", Phasecraft + Johnson Matthey + Harvard; Xanadu–NRC battery simulation) | Cheaper data-loading and function-evaluation primitives (QROM, alias sampling, Gaussian/Coulomb evaluation) that fit **~100 logical qubits and ~1e6 operations (megaquop)**. Gu's discovered function evaluators (1.1k–1.6k Toffolis, 115–142 qubits) are in exactly this range `[INFERENCE]`. | ARPA-E QC3: $37M over 3 years, 9 teams; aims for 100× over classical "validated at approximately 100 logical qubits"; "vendor roadmaps … don't yet clearly map to the resources required for published algorithms" (full QuEra press release; ARPA-E page not read). FeMoco THC: 6.7e9 Toffolis, QROM- and rotation-dominated (partial). |
| **P4** | **Post-quantum migration and crypto-risk analysts** (CISOs, banks, blockchain protocol developers; Toronto/Waterloo is a hub: evolutionQ, Global Risk Institute's Quantum Threat Timeline) | A trusted, current tracker of "cost to break RSA-2048 / ECC-256" with provenance. Pairs naturally with ZK attestation so that attack circuits are not disclosed. | Babbush 2026: Bitcoin/Ethereum exposure, responsible-disclosure ZK approach (partial). Gidney 2025: "Planning the transition … requires understanding the cost of quantum attacks" (partial). **Canadian org names (evolutionQ, GRI) are unverified this session.** |
| **P5** | **Compiler / tooling maintainers** (Qualtran, Bartiq/QREF, MS QRE, TopQAD, PennyLane) | A regression and benchmark suite of FT arithmetic tasks with certified best-known (T, Q, ε) to test their cost models and synthesis against. | Qualtran already has classical-sim consistency tests (docs). `uncompute` ships graders, `results.jsonl` and certified op streams under Apache-2.0 (README). MQT Bench/QASMBench exist only for NISQ. |

**Job-market evidence (weak):** Q-CTRL "Staff Research Scientist — Quantum Algorithms & Fault-Tolerant Applications" (title only; page body did not load); quantumjobs.us lists a "Fault-Tolerant Computing" category with a $241k–$301k posting (snippet-only); Zapata Quantum is hiring a "Quantum Algorithm Scientist" (snippet-only). Treat all of this as **unverified**.

**Canadian / Toronto-investor angles:**
- Xanadu (Toronto; NASDAQ/TSX: XNDU after SPAC) received CAD $195M from the federal Strategic Response Fund on 2026-08-28 (snippet + headline) and up to CAD $23M from CQCP.
- Nord Quantique was reportedly valued at $1.4B with Fidelity backing (Globe and Mail snippet).
- Photonic closed a US$200M financing (Globe and Mail snippet) and has 180+ staff (press release).
- Federal commitments: CAD $334M quantum (Budget 2025: $223M research + $111M anchoring/defence) on top of the $360M National Quantum Strategy (BetaKit).
- Ministers explicitly frame "keeping the talent here and the IP here" as policy.
- 1QBit (Vancouver) supplies FT QEC design / compilation / QRE to the HPE–Qolab QBI Stage A consortium.

**Pitch line** `[INFERENCE]`: Canada now runs a QBI-like evaluation pipeline (CQCP + NRC benchmarking). A neutral, verifiable resource-claim layer serves that pipeline and the three Canadian QBI Stage B companies.

---

## 5. IP sensitivity: overlap with 1QBit (Severyn's employer)

1QBit's commercial product **TopQAD** is a physical-layer QRE and architecture-design suite. It covers circuit → Pauli-rotation compilation, noise profiling, magic-state-factory optimisation, decoder-latency/reaction-time models, a space–time Pareto frontier, $/qubit-second cost, and error-budget breakdowns. 1QBit also markets "quantum algorithm compilation and automated quantum resource estimation" in the DARPA QBI consortium. Severyn built a Gradio QRE demo at 1QBit.

| Direction | Overlap with 1QBit | Recommendation |
|---|---|---|
| Physical-QRE dashboard (logical counts → physical qubits/runtime, factory sizing, code-distance selection, decoder latency) | **HIGH**: this is TopQAD's core product, and a Gradio-style QRE UI matches Severyn's work output | Avoid, or use *only* public models (Gidney's published formulas, Qualtran `surface_code`, MS QRE) behind a thin adapter. Do not re-create TopQAD features or UI. |
| Magic-state-factory / QEC architecture optimisation | **HIGH** (TopQAD Assembler; 1QBit paper on multi-level MSF optimisation, arXiv 2411.04270, listed in TopQAD refs) | Avoid |
| Circuit-level compilation to a lattice-surgery ISA | **MEDIUM-HIGH** (TopQAD Compiler) | Avoid |
| LLM/evolutionary **logical-level reversible-arithmetic discovery** (Toffoli/qubit/ε) on public tasks (`uncompute`) | **LOW-MEDIUM**: 1QBit compiles algorithms but does not (publicly) offer subroutine discovery | Acceptable if built only on public code/data (Apache-2.0 `uncompute`, OpenEvolve, Qualtran) on personal time and hardware |
| **Verified best-known-subroutine registry / certification service** (hash-committed circuits, failure-budget Pareto (T, Q, ε), optional ZK attestation) | **LOW**: complementary; it feeds any QRE, including TopQAD | Best-differentiated direction. Frame it as neutral infrastructure *upstream* of QRE tools. |

Before submitting: `[INFERENCE: general practice, not legal advice]` check the employment agreement's invention-assignment and moonlighting clauses (Canadian employment contracts often assign related inventions), use no 1QBit code/data/demo assets, and consider telling a manager. Ethics/dual-use: cryptanalysis circuits (RSA/ECC) are sensitive. Follow Babbush's practice of committing hashes / ZK rather than publishing improved attack circuits, and prefer DQI, chemistry or function-evaluation tasks in public demos.

---

## 6. Reusable components for a 20-hour build (all verified to exist)

- `andigu/uncompute` (Apache-2.0): exact kickmix evaluator, 8 graders with failure budgets, baseline and discovered circuits, certified counts, liveness profiles. Usable as the verifier/scoring backend and as seed registry entries.
- OpenEvolve (Apache-2.0): MAP-Elites evolutionary coding agent.
- Qualtran (Apache-2.0): bloq library (GF, modular arithmetic, ECC, RSA, chemistry) with classical simulation; `surface_code` public physical models for an optional physical-cost column.
- Bartiq/QREF (Apache-2.0): a JSON format for exporting registry entries into PsiQuantum-style symbolic estimates.
- MS QRE (MIT): "logical counts" input mode; a registry entry could be pushed straight into it.
- Babbush ZK pattern (SP1 zkVM + Groth16; Zenodo code): a reference design for "prove the cost without revealing the circuit". Too heavy for 20 h; a hash-commitment plus Fiat-Shamir test transcript is a feasible lite version.

## 7. Sources

- Gu, Kemeny, Yelin, Lukin, arXiv 2610.22367, https://arxiv.org/html/2610.22367 (partial, see §3); code https://github.com/andigu/uncompute (README, tree, graders)
- Gidney, arXiv 2505.15917, https://arxiv.org/html/2505.15917 (partial)
- Babbush et al., arXiv 2603.28846, https://arxiv.org/html/2603.28846 (partial)
- Khattar et al., arXiv 2510.10967, https://arxiv.org/html/2510.10967 (partial)
- Litinski, arXiv 2306.08585, https://arxiv.org/html/2306.08585 (partial)
- Lee et al. (THC), arXiv 2011.03494, https://arxiv.org/html/2011.03494 (partial)
- Jordan et al. (DQI), arXiv 2408.08292 (not read)
- TopQAD QRE docs, https://topqad.1qbit.com/services/quantum-resource-estimation (full page); TopQAD news, https://1qbit.com/home/topqad-news (full)
- MS QRE intro, https://learn.microsoft.com/en-us/azure/quantum/intro-to-resource-estimation (full)
- Qualtran classical sim docs, https://qualtran.readthedocs.io/en/latest/simulation/classical_sim.html (full)
- DARPA QBI Stage B, https://www.darpa.mil/research/programs/quantum-benchmarking-initiative/stage-b-selection (full); Stage C news, https://www.darpa.mil/news/2026/four-more-teams-enter-quantum-benchmarking-initiative-final-stage (full)
- QuEra Libra/AWS press release (full): https://www.prnewswire.com/news-releases/quera-announces-2028-fault-tolerant-quantum-computer-and-expanded-multi-year-strategic-collaboration-with-aws-302799818.html
- QuEra gigaquop roadmap / FTQC Founders Circle (full): https://www.quera.com/press-releases/quera-unveils-gigaquop-class-fault-tolerant-roadmap-and-invites-organizations-to-co-design-quantum-applications
- QuEra on ARPA-E QC3 (full): https://www.quera.com/press-releases/quera-scientists-named-co-principal-investigators-on-three-of-nine-teams-in-department-of-energys-quantum-chemistry-program-now-underway
- Photonic–Microsoft QRE (full): https://photonic.com/news/photonic-inc-advances-quantum-resource-estimation-capabilities-with-microsoft
- BetaKit on CQCP (full): https://betakit.com/canada-launches-it-own-quantum-research-program-to-rival-darpa-initiative
- GitHub API metadata (licenses, stars, push dates) for all repos in §2, queried 2026-10-19
