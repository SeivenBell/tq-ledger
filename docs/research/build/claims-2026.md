# Claim cards: 2026 secp256k1 point-addition / ECDLP resource claims

Compiled 2026-10-23 by EccClaims2026. Sources were fetched live on 2026-10-23. Read depth is stated on each card. Arithmetic marked **[RECOMPUTED]** was done in Python 3 with `scipy.stats.beta`. **[INFERENCE]** marks my own judgement. "not found" means I searched the source and the number is not there.

Location convention: arXiv HTML has no page numbers, so locations are section, table or equation labels taken from the HTML. API records are cited by JSON field, and the note by its Markdown heading.

---

## 0. Recomputation: 893-qubit circuit failure statistics [RECOMPUTED]

Input: k = 111 failures in n = 360,960 shots (40 salts × 9,024). Source: submission 457ccb7a note, "## Population measurements", Checkpoint D table: "salts × shots | 40 × 9,024 = 360,960" … "failing shots | 111".

- Point estimate: p̂ = 111/360,960 = **3.0751×10⁻⁴**, about **1 in 3,252**.
- 95% Clopper–Pearson interval (exact binomial):
  - lower = B⁻¹(0.025; k, n−k+1) = B⁻¹(0.025; 111, 360,850) = **2.530×10⁻⁴**
  - upper = B⁻¹(0.975; k+1, n−k) = B⁻¹(0.975; 112, 360,849) = **3.703×10⁻⁴**
  - B⁻¹ is the inverse regularized incomplete beta function (`scipy.stats.beta.ppf`).
- Probability that one 9,024-input evaluation is clean, (1−p)^9024:
  - at p̂: **0.0623** (6.2%)
  - at the CI lower bound: 0.102
  - at the CI upper bound: 0.035
  - Expected failures per 9,024 run: λ = 9,024·p̂ = **2.775**, which matches the note's "estimated lambda | 2.775". Poisson check: e^−2.775 = 0.0623.
- If p̂ applied independently to each of the 28 windowed additions [INFERENCE: the independence and classical-input model is an extrapolation, as Ivezic also says]: P(≥1 failure) = 1−(1−p̂)^28 = **0.86%**. At the CI upper bound it is 1.03%.
- 874-qubit circuit: 122/360,960 = 3.380×10⁻⁴, and (1−p)^9024 = **0.047**.
- Cross-budget check [RECOMPUTED]:
  - Gu et al.'s modinv-point-add grader allows ≤20 failures per 100,000 (2×10⁻⁴).
  - The 893-qubit circuit's whole 95% interval (2.53–3.70×10⁻⁴) lies **above** that budget. Its expected failure count in a 100k run is ≈31.
  - So the "893 qubits, 2.2M Toffolis" point **would not pass the Gu benchmark's failure budget**, even though it passed ECDSA.Fail's 9,024-input gate.
- Schrottenloher's "failure probability at most 2^−13.3 (succeeding on 10 000 randomly chosen inputs)" [RECOMPUTED]:
  - 2^−13.3 = 9.9×10⁻⁵ ≈ 1/10,000.
  - A circuit with ε = 2^−13.3 passes 10,000 tests with probability (1−ε)^10000 ≈ e^−0.99 ≈ 0.37.
  - So zero failures in 10,000 bounds ε ≤ 2^−13.3 only at ≈63% confidence. The 95% bound is ln(20)/10,000 = **3.0×10⁻⁴ ≈ 2^−11.7**.
  - [INFERENCE] The stated bound is a one-over-n heuristic, not a 95% guarantee.

Other arithmetic checks [RECOMPUTED]:

| Check | Result |
|---|---|
| 893 × 2,218,127 | 1,980,787,411 (= `officialScore`) ✓ |
| 1,234 × 742,470 | 916,207,980 (= `currentBestScore`) ✓ |
| Google low-qubit bound 1,175 × 2.7M | 3.1725 B |
| Google low-gate bound 1,425 × 2.1M | 2.9925 B (ECDSA.Fail rounds these to "≈3.17 B" and "≈2.99 B") |
| Google Eq. (1), w = 16 (low-qubit) | 28 × (2.7M + 3·2¹⁶) = 81.1M ≤ "90 million" ✓ |
| Google Eq. (1), w = 16 (low-gate) | 28 × (2.1M + 3·2¹⁶) = 64.3M ≤ "70 million" ✓ |
| Schrottenloher 2^20.83 | 1.864M |
| Schrottenloher 2^21.19 | 2.392M; + 3·2¹⁶ = 2.589M (this matches ECDSA.Fail Table 3's "2.59 M†" for Schrottenloher, i.e. the *windowed* figure) |
| 893 vs 1,175 | −24.0%; 2,218,127 vs 2.7M = −17.8% (matches Ivezic's "24% fewer … 18% fewer") ✓ |
| Luo per controlled point addition, leading term | 976·n²·log₂n at n = 256 = 5.12×10⁸ Toffolis (lower-order terms ignored) |

---

## 1. Card table (summary)

| id | claim (as stated) | layer | scope | addend | T statistic | failure evidence | independent check |
|---|---|---|---|---|---|---|---|
| EF-BENCH | ECDSA.Fail score S = Q×T; best 1,151 q / 1,299,453 T at the 2026-07-26 cutoff; windowed 1,162 / 1,684,161 | logical-circuit | subroutine (point add) | classical (benchmark); coherent (windowed variant) | average executed | 0/9,024 FS; 0.192% on 100k | evaluator public (MIT); the paper is by the operators |
| EF-893 | 893 q, 2,218,127 T (2026-10-13) | logical-circuit | subroutine | classical | average executed (9,024 shots) | 0/9,024 FS after nonce filter; 111/360,960 own test | official evaluator re-run Q, T; failure test self-reported |
| EF-874 | 874 q, 2,398,215 T (2026-10-14) | logical-circuit | subroutine | classical | average executed | 0/9,024 FS; 122/360,960 own test | as EF-893 |
| EF-LEAD | current best 1,234 q, 742,470 T, S = 916,207,980 | logical-circuit | subroutine | classical | average executed | 0/9,024 FS | official evaluator |
| PQ-IVEZIC | 893 within Google bound; "25% physical" fails under vendor scalings (Oratomic ≤16%, IonQ ~28% but slower) | commentary on logical + physical | subroutine → architecture | n/a | n/a | restates 111/360,960 | hand analysis |
| PLDD-25 | "cuts the physical qubits … by 25%" | physical-architecture (claimed) | full attack (implied) | — | — | none | none; source tweet not read |
| GU-DIV | 4.0M T, 935 q; certified 4,006,673 / 935 | logical-circuit | subroutine (point add) | classical | executed (statistic not stated as average or worst) | budget ≤20/100,000; union bound 1.599×10⁻⁴ | hash-seeded evaluator public (Apache-2.0) |
| SCHR | 1,192 q / 2^21.19 T; 1,446 q / 2^20.83 T (excludes window) | logical-circuit | subroutine; Eq. 1 extends to full | coherent window excluded (+16 q, +3·2¹⁶ T) | not stated | ≤2^−13.3; 0/10,000 | not found |
| GOOG-ZK | PA ≤1,175 q / ≤2.7M T and ≤1,425 q / ≤2.1M T; full ECDLP ≤1,200 q / ≤90M T, ≤1,450 q / ≤70M T; <500k physical | logical-circuit (ZK) + logical-algorithm + physical | subroutine + full | window-indexed per ECDSA.Fail; lookup billed separately per Eq. 1 | average executed over 9,024 | 0/9,024 FS (proved in ZK) | Groth16/SP1 proof; Trail of Bits forged v1 proof (patched in v2) |
| LUO | full ECDLP 1,333 q; 5n+4⌊log₂n⌋+O(1) q; 976n³ T | logical-algorithm | full attack | controlled affine add | asymptotic / leading-order | "exactly correct" (claimed) | Gu reconstruction: 69,529,757 T / 838 q |
| CD-50 | "cut Bitcoin and Ethereum quantum attack estimate by 50%" | press | headline implies full attack; body says a subroutine | — | — | — | none |
| IONQ-PR | "20,000-physical-qubit … break secp256k1 … in just under 26 days" | physical-architecture | full attack | coherent lookups included (per Ivezic) | — | not read | none found |

---

## 2. Cards

### EF-BENCH — ECDSA.Fail benchmark definition and paper operating points
- **source**
  - authors: Long et al. (35 authors per prior notes), incl. P.-L. Dallaire-Demers
  - title: "ECDSA.Fail: Open Autoresearch for Optimizing Elliptic-Curve Point Addition in Shor's Algorithm"
  - id: arXiv 2609.09582**v2**
  - date: v1 submitted 9 Sep 2026; v2 2026-09-19 per prior notes; the abs page lists [v1], [v2]
  - url: https://arxiv.org/html/2609.09582v2
  - license: **CC BY 4.0** (abs page license link)
  - read depth: **partial**. Read: abstract, §2.1 benchmark-cost text, Test points / Approximation and nonce hunting paragraphs, §5.1.1–5.1.2, Table 2 header rows, Table 3 in full, Figure 1/7 captions, §5.2.1 opening. Not read: Supplemental Notes A–F.
- **target**: reversible secp256k1 *mixed point addition*. scope = **subroutine**.
- **layer**: logical-circuit.
- **metrics**

  | name | value | unit | statistic | quote | location |
  |---|---|---|---|---|---|
  | Q definition | — | logical qubits | peak | "Peak qubits Q: the maximum number of logical qubits simultaneously live at any point in the circuit." | §2.1/§3 benchmark cost list |
  | T definition | — | Toffoli-equivalents | **mean over test inputs** | "Average executed Toffoli T: the expected number of executed Toffoli-equivalent …"; "Each executed CCX or CCZ counts as one Toffoli-equivalent operation." | same |
  | score | S = Q×T | — | — | "the challenge defines S=Q×T. (1)" | Eq. (1) |
  | test set | 9,024 | curve points | Fiat–Shamir | "seeding SHAKE256 with the serialized submitted circuit and expanding its output into 9,024 curve points" | "Test points." paragraph |
  | baseline | Q = 2,715, T = 3,960,753 | | | "the 10.75B baseline (Q=2,715, T=3,960,753)" | §1 |
  | cutoff best | Q = 1,151, T = 1,299,453, S = 1,495,670,403 | | avg | "Q=1,151, T=1,299,453, and Q×T=1,495,670,403" | §5.2.1 |
  | cutoff date | 26 Jul 2026 09:21:55 UTC | | | "We place the cutoff date at 26 July 2026, 09:21:55 UTC" | §5.2.1 |
  | windowed variant | Q = 1,162, T = 1,684,161, p̂ = 0.99809 (100,000 inputs) | | avg | "It uses Q=1,162 and T=1,684,161; on 100,000 random inputs, its empirical success probability was p̂=0.99809" | Abstract |
  | low-Q point | Q = 825, T = 489,161,900 | | avg | "b6f2b0a 825 489,161,900 Admitted Lowest observed width." | Table 2 |
  | post-cutoff | 1.259 B; 813 q | | | "the Q×T score was further reduced to 1.259B, while a separate low-width circuit reached 813 qubits" | Abstract |
  | windows per attack | 28 | point-add calls | | "boundary optimizations reduce the estimate used in this paper to 28 point-addition calls" | Figure (windowed Shor) caption |

- **assumptions**: T is "a useful but architecture-dependent work proxy rather than a literal time axis". Q "lower-bounds the required logical storage without by itself determining the physical machine size" (§2.1).
- **failure**
  - Approximation is allowed: "Exactness is not required … Submissions can therefore trade accuracy for lower Q×T by truncating comparisons, narrowing carries, or removing rarely executed gates."
  - Nonce hunting: "Submitters can search these nonces for an error-free test set, or clean validation island."
  - Landability: "approximately (1−ϵ)^9024 under the random-oracle model" ("Approximation and nonce hunting" paragraph).
  - Table 3 row 8e9c9a2: "0/9,024 FS; 0.192% on 100,000 independent cases".
- **addend_interface**: **classical** for the benchmark ("the benchmark supplies one addend classically, whereas windowed Shor selects it coherently", §1). The 1,162-qubit variant is **coherent / window-indexed**.
- **counting_conventions**: average executed CCX+CCZ over the 9,024 FS inputs; peak live logical qubits; classically controlled gates count only when executed; measurement-based uncomputation allowed.
- **independent_verification**: the evaluator code is public (MIT, per ToS §5). The Pareto analysis is by the operators and contributors themselves. Not found: any third-party audit of Table 3.
- **non-comparability notes (author-stated)**: "These comparisons are contextual rather than claims of formal dominance because interfaces, correctness assumptions, and accounting conventions differ" (§1). "External rows without common-corpus measurements are evaluated optimistically with p̂=1" (§5.1.2).

### EF-893 — Lilypad-G 893-qubit circuit (submission 457ccb7a, 2026-10-13)
- **source**
  - author: jieyilong (Jieyi Long); "Model: GPT-5 / Harness: Codex"; design attributed to "Claude Code Opus 5.5"
  - title: "Lilypad-G Layers: 893 qubits and 2.218M Toffolis"
  - id: submission `457ccb7a-4436-4e8c-8e8c-f7d22c3c81b5`, commit `98b17b89…`
  - date: `createdAt` 2026-10-13T17:40:07Z
  - url: https://api.ecdsa.fail/api/submissions/457ccb7a-4436-4e8c-8e8c-f7d22c3c81b5
  - license: hosted API is Eigen Labs proprietary (ToS §5). Notes are public under ToS §6. No data license found.
  - read depth: **full** (the whole JSON record and note)
- **target**: secp256k1 mixed point addition. scope = subroutine.
- **layer**: logical-circuit.
- **metrics**

  | name | value | unit | statistic | quote | location |
  |---|---|---|---|---|---|
  | Q | 893 | logical qubits | peak | `"officialMetrics": {"qubits": 893, …}` | JSON |
  | T | 2,218,127 | Toffolis | mean, integer | `"toffoli": 2218127`; note: "**2,218,126.971 measured mean executed Toffolis**; benchmark integer metric **2,218,127**" | JSON; note "## Result" |
  | S | 1,980,787,411 | | | `"officialScore": 1980787411` | JSON |
  | ops | 27,124,416 | operations | | "**27,124,416 emitted operations**" | note "## Result" |
  | status | rejected | | | `"rejectionReason": "score did not improve current best"` | JSON |

- **failure**
  - Official gate: "0 classical / 0 phase / 0 ancilla failures across all 9,024 shots" (note "## Result").
  - Own population test: "salts × shots | 40 × 9,024 = 360,960 … failing shots | 111 … estimated lambda | 2.775 … standard error | 0.263391" (note "## Population measurements", Checkpoint D).
  - Selection: "Nonce `128` was the first candidate sent to the trusted evaluator. It returned 0/0/0 over all 9,024 shots." The GPU filter "scanned 4,096 nonces … and returned 196 candidates" (note "## L40S nonce hunt and final validation").
  - Recomputed in §0: p̂ = 3.08×10⁻⁴ [2.53, 3.70]×10⁻⁴; P(clean run) = 6.2%.
- **addend_interface**: classical ("adds a quantum elliptic curve point to a classical elliptic curve point", benchmark `description`).
- **counting_conventions**: ECDSA.Fail average executed T over 9,024 FS inputs. Population mean T 2,218,113.31 vs official 2,218,126.971 (different inputs).
- **independent_verification**: Eigen Labs' trusted evaluator re-measured Q and T (official = claimed). The 360,960-shot failure test is **self-reported** by the submitter. Not found: an independent re-run.
- **non-comparability**: the note itself says "It is a low-qubit/low-Toffoli Pareto architecture result, not a claim to beat the current global scalar-product leader." No windowed/coherent version exists: Ivezic says "Nobody has published that version of the sub-900 circuits yet."

### EF-874 — submission ae537372 (2026-10-14)
- **source**: jieyilong. https://api.ecdsa.fail/api/submissions/ae537372-a846-424e-b613-9c4038a0a46e. `createdAt` 2026-10-14T11:02:18Z. Read depth: **partial** (officialMetrics and the population-measurement section of the note).
- **metrics**
  - Q = 874: `"qubits": 874`.
  - T = 2,398,215: `"toffoli": 2398215`.
  - status "rejected".
- **failure**: "shots 360,960 / failing shots 122 / lambda_hat 3.050 / standard error 0.276" (note "## Population measurement"). Selection: "scanned nonces `[0,4096)` and produced 200 conservative candidates. The trusted evaluator found nonces 20, 21, and 23 fully clean." Recomputed: P(clean) = 4.7%.
- **addend_interface**: classical.
- Other fields: as EF-893.

### EF-LEAD — live leaderboard state (fetched 2026-10-23)
- **source**: Eigen Labs, `GET https://api.ecdsa.fail/api/benchmarks`, benchmark `1ffb695a-309b-46b6-a728-2f97d8c7be74` (`gpsanant/ecdsafail-challenge`, status "open"). Read depth: **full** for this record's fields.
- **metrics**
  - `"currentBestMetrics": {"qubits": 1234, "toffoli": 742470}`
  - `"currentBestScore": 916207980`
  - `"baselineMetrics": {"qubits": 2715, "toffoli": 3962753}`
  - `"openedAt": "2026-05-30T07:19:21.482Z"`
  - Note: the baseline Toffoli count differs from the paper's 3,960,753 by 2,000 [not explained in any source read].
- **scoring**: `"description": "Optimize the qubit-toffoli product for a reversible circuit that adds a quantum elliptic curve point to a classical elliptic curve point."` The board ranks a single scalar, so the 893-qubit and 874-qubit Pareto points were rejected.
- **Homepage claim**: "68.5% ahead of Google's classified circuit". This is from a **search-result snippet only**; the page is JS-rendered and my fetch did not return the figure. Recomputed: 916,207,980 / 2,992,500,000 = 0.306, i.e. **69.4%** below Google's low-gate bound now. The 68.5–68.6% figure matches the earlier 1,234 × 761,096 leader (Ivezic: "The leaderboard puts its score 68.6% below that of Google's low-gate bound").
- **Terms** (https://ecdsa.fail/terms, "Effective: October 7, 2026", **partial**, §§2, 3, 5, 6 read):
  - Code license: "made available to you under the MIT License … It does not license the hosted Platform, including the website, the API, the evaluation and scoring service, and the leaderboard, which remain Eigen Labs' proprietary property" (§5).
  - Platform license: "limited, non-exclusive, non-transferable, revocable license to access and use the Platform solely to participate in challenges" (§5).
  - Leaderboard: "The leaderboard is public" (§6).
  - No explicit scraping clause found.
  - [INFERENCE] Bulk-mirroring the API for a product is outside the granted license. Cite and link individual records instead.

### PQ-IVEZIC — Marin Ivezic, postquantum.com
- **source**
  - author: Marin Ivezic
  - title: "Sub-900-Qubit secp256k1 Circuit Within Google's Bound" (share title: "A Key Step of a Quantum Attack on Bitcoin and Ethereum Now Fits in Under 900 Logical Qubits Within Google's Gate Budget")
  - datePublished 2026-10-14T17:58:31+02:00; dateModified 2026-10-17T17:58:56+02:00 (JSON-LD)
  - url: https://postquantum.com/security-pqc/ecdsa-fail-low-qubit-circuit/
  - license: © 2026 Marin Ivezic (`copyrightHolder`); no open license
  - read depth: **full**
- **target**: commentary on EF-893 and EF-874. Translates them to physical machines.
- **layer**: logical-circuit numbers plus his own physical-architecture scalings.
- **metrics (all his statements)**

  | value | quote | location |
  |---|---|---|
  | 893 q / 2,218,127 T | "It uses 893 logical qubits and an average of 2,218,127 Toffoli gates" | para 1 |
  | 111 / 360,960 | "111 of 360,960 additions failed" | para 1 |
  | ≈1/3,250 | "about one in 3,250" | §"The 893-Qubit Circuit Fails…" |
  | 6% clean | "would hit 2.8 failures on average and come out clean about 6% of the time" | same (recomputed 6.2% ✓) |
  | Google bounds | "at most 1,175 logical qubits and 2.7 million Toffolis per addition" | para 2 |
  | Google physical | "fewer than 500,000 superconducting qubits. Scaling that by width alone gives about 380,000" | §Checking the 25%… |
  | Oratomic | "would save roughly 1,200 to 1,600 atoms, 12% to 16% of the machine" | same |
  | IonQ | "would save about 5,200 to 5,600 ions, 27% to 29% of the machine" | same |
  | IonQ per add | "IonQ's 39 million Toffolis, spread over 28 windowed additions, average about 1.4 million per addition with the lookups included. Long's circuit uses 2.2 million before any lookup is added, about 1.6 times as much." | same |
  | coherent penalty | "When the ECDSA.Fail authors added that lookup to their 1,151-qubit circuit, it cost 11 more qubits and about 30% more Toffolis." | same (recomputed 1,684,161/1,299,453 = 1.296 ✓; 1,162−1,151 = 11 ✓) |
  | 28-addition attack | "arithmetic errors would make under 1% of attack runs fail" | §Fails… (recomputed 0.86% ✓) |

- **assumptions**: his physical scalings assume memory shrinks with logical width while factories and routing do not. These are rescalings of published vendor layouts, not recompilations ("None of the three companies has redone its estimate with these circuits").
- **failure**: restates the submitter's numbers. Not an independent test.
- **addend_interface**: explicitly flags the classical vs coherent gap.
- **independent_verification**: hand analysis only. The Oratomic/IonQ inputs (9,739 atoms; 19,397 ions) were **not checked by me** against arXiv 2603.28627 / 2609.05625.
- **notes**: this is the best existing human version of what the ledger automates. Every check he does by hand is a gate in the tool.

### PLDD-25 — "25% fewer physical qubits"
- **source**: Pierre-Luc Dallaire-Demers (Pauli Group; ECDSA.Fail co-author), X post https://x.com/dallairedemers/status/2110068442330234929, 2026-10-13. **Not read** (X not fetchable). Captured **second-hand** from Ivezic: "On October 13 he called the result a breakthrough on X and wrote that it cuts the physical qubits required by recent attack proposals from IonQ, Oratomic and Google by 25%."
- **layer**: physical-architecture (claimed), derived from a logical-circuit change.
- **basis**: not found. [INFERENCE] It matches 1 − 893/1,175 = 24.0%, a one-for-one logical-to-physical scaling.
- **failure / independent verification**: none. Ivezic's check gives Google ≈24% only "if every component shrank with width", Oratomic ≤16%, IonQ ≈28% fewer ions but longer runs.
- **non-comparability**:
  - logical→physical layer jump
  - subroutine→full-attack jump
  - classical-addend circuit applied to coherent-lookup architectures
  - average-T approximate circuit (p̂ = 3.1×10⁻⁴) vs vendors' failure budgets
  - No full-attack estimate exists ("No full Shor's-algorithm estimate built on the new circuit has been published", Ivezic).

### GU-DIV — Gu, Kemeny, Yelin, Lukin, modinv-point-add
- **source**
  - title: "Discovering state-of-the-art quantum circuits with large language models"
  - id: arXiv 2610.22367 (v1, submitted 15 Oct 2026)
  - url: https://arxiv.org/html/2610.22367
  - license: **CC BY-NC-SA 4.0**
  - repo: https://github.com/andigu/uncompute `tasks/modinv-point-add` (Apache-2.0 per prior notes)
  - read depth: **partial**. Read: Table 1, Extended Data Table 1 row, Methods "Validation and statistical guarantees" and "Cost model and scoring", SI II intro and Table S3, divstep stack paragraph. Repo README sections 1, 3.1, 5, 6 and results.jsonl read **full**.
- **target**: secp256k1 point addition (y² = x³+7, p = 2²⁵⁶−2³²−977), benchmarking modular inversion. scope = subroutine.
- **layer**: logical-circuit.
- **metrics**

  | name | value | statistic | quote | location |
  |---|---|---|---|---|
  | T, Q | 4.0×10⁶, 935 | executed | "A complete benchmark circuit built on this inversion (SI II) uses 4.0 million Toffolis and 935 qubits." | main text, "Reversible modular inversion" end |
  | certified | 4,006,673 T; 935 q; TQ 3,746,239,255 | executed | `{"source": "circuits/divsteps/circuit.py", … "toffoli": 4006673, "qubits": 935, "tq_cost": 3746239255}` | results.jsonl row 1 |
  | 893-q variant | 7,866,779 T; 893 q | executed | `"circuits/divsteps/j9.py" … "toffoli": 7866779, "qubits": 893` | results.jsonl |
  | specialized Euclidean | 2.1×10⁷ T, 843 q; certified 20,521,949 / 843 | | "Specialized Euclidean, SI II.2 Specialized packed walk 2.1⋅10⁷ 843 1.7⋅10¹⁰" | Table S3; results.jsonl |
  | Luo reconstruction | 7.0×10⁷ T, 838 q; certified 69,529,757 / 838 | | "Luo et al. [40] Packed Euclidean walk 7.0⋅10⁷ 838 5.8⋅10¹⁰" | Table S3; results.jsonl |
  | Schrottenloher (cited) | 1.9×10⁶ T, 1,446 q | | "Schrottenloher [38] Binary gcd and dialog trick 1.9⋅10⁶ 1,446 2.7⋅10⁹" | Table S3 |
  | cost share | 63% | | README: "These walks use 63% of the Toffolis." | README §4 |

- **failure**
  - Budget: "Failure budget ≤ 2⋅10⁻⁴ … 10⁵" (Extended Data Table 1).
  - README: "A run passes with at most 20 failed tests out of 100,000, a failure rate of 2×10⁻⁴" (§6).
  - Union bound: "The paper's union bound on the failure probability is 1.599×10⁻⁴ per point addition."
  - Euclidean: "about 8×10⁻⁵ per point addition" (README §4).
  - Statistics: (1−ε)^k certificate and P_{k,b}(ε) (Methods Eqs. 20–21).
  - Observed failures for the 935-qubit run: not found (results.jsonl gives only `"verdict": "OK"`).
- **addend_interface**: **classical**. "counts include reversible cleanup but exclude application-specific storage or lookup used to supply the classical addend" (Table S3 caption). "The two `offset` registers are classical bit inputs with fresh values on every test … A circuit may compute any classical function of Q at no cost" (README §3.1).
- **counting_conventions**: "T counts Toffoli and CCZ gates equally and Q is the largest number of logical qubits allocated at once" (Eq. 22). "a bit-conditioned CX counts as a Toffoli. Classical bit wires do not count toward peak qubits" (README). Whether T is a mean over tests or a fixed count: **not found** (README says "executed Toffoli count"). Tests: 10⁵ hash-seeded, vs ECDSA.Fail's 9,024.
- **independent_verification**: certified by the authors' public evaluator (re-runnable). Not found: any third-party run.
- **non-comparability**:
  - Different test count (10⁵ vs 9,024).
  - Different failure gate (≤20/10⁵ vs 0/9,024 after nonce selection).
  - Possibly a different T statistic.
  - Different evaluator from ECDSA.Fail. Gu's evaluator counts bit-conditioned CX as a Toffoli; ECDSA.Fail's convention on this is not checked.
  - At equal Q = 893, Gu j9 needs 7.87M T vs Long's 2.22M. These cannot be ranked without a common evaluator, and Long's circuit would fail Gu's failure budget (§0).

### SCHR — Schrottenloher 2026
- **source**
  - author: André Schrottenloher
  - title: "Optimized Point Addition Circuits for Elliptic Curve Discrete Logarithms"
  - id: arXiv 2606.02235**v1** (submitted 1 Jun 2026)
  - url: https://arxiv.org/html/2606.02235
  - license: **CC BY 4.0**
  - read depth: **partial**. Read: abstract, Table 1 and caption, Eq. (1), the full-attack table, §4 iteration-count text.
- **target**: secp256k1 (plus a generic-prime variant). Point addition; full-attack Toffolis via Eq. (1).
- **layer**: logical-circuit; Eq. (1) gives logical-algorithm totals.
- **metrics**

  | name | value | quote | location |
  |---|---|---|---|
  | space-opt | 1,192 q; 2^21.19 T (= 2.39M) | "Space-optimized for secp256k1 1192 2^21.19 ≃2^24 Ours" | Table 1 |
  | gate-opt | 1,446 q; 2^20.83 T (= 1.86M) | "Gate-optimized for secp256k1 1446 2^20.83 ≃2^24 Ours" | Table 1 |
  | full attack, space-opt | 1,208 q; 2^26.11 T | "Space-optimized for secp256k1 1208 28×(2^21.19+3⋅2^16)=2^26.11 Ours" | full-attack table |
  | full attack, gate-opt | 1,462 q; 2^25.78 T | "…1462 28×(2^20.83+3⋅2^16)=2^25.78 Ours" | same |
  | vs Google | +1.5% q; −6.5–10% T | "a slightly higher number of qubits (around 1.5% increase) and a slightly smaller Toffoli gate count (between 6.5% and 10% reduction)" | Abstract |

- **failure**: "All circuits have a failure probability at most 2^−13.3 (succeeding on 10 000 randomly chosen inputs)" (Table 1 caption). Recomputed in §0: this holds at ≈63% confidence, and the 95% bound is ≈2^−11.7.
- **addend_interface**: point-add numbers **exclude** the window: "do not account for the small window of size w=16: it costs 16 qubits more and 3×2^w Toffoli gates to run the actual 'windowed point addition'" (Table 1 caption). The full-attack rows are coherent / window-indexed.
- **counting_conventions**: "The 'Toffolis' column counts together CCX, CCZ as well as And gates" (Table 1 caption). Average vs worst case: **not found**.
- **independent_verification**: not found. Code release: not found in the sections read.
- **non-comparability**: two sources quote different Schrottenloher numbers.
  - Gu Table S3 uses 1.9M / 1,446 (unwindowed).
  - ECDSA.Fail Table 3 uses 2.06M† / 1,462† and 2.59M† / 1,208† (windowed: +16 q and +3·2¹⁶ T).
  - Both are faithful, but they sit in **different interface columns**. Placing them on one Pareto chart without the flag misplaces the point by ≈0.2M T and 16 q.

### GOOG-ZK — Babbush et al., Google Quantum AI
- **source**
  - title: "Securing Elliptic Curve Cryptocurrencies against Quantum Vulnerabilities: Resource Estimates and Mitigations"
  - id: arXiv 2603.28846 (v1 submitted 30 Mar 2026; v2 exists; v2 patched the proof after the Trail of Bits forgery, per prior notes)
  - url: https://arxiv.org/html/2603.28846
  - license: **CC BY 4.0**
  - ZK artefact: https://zenodo.org/records/19597130 (not opened)
  - read depth: **partial**. Read: abstract, §II.2 resource sentences, Appendix A.1–A.3 statements, the zkVM description, Eq. (1).
- **target**: secp256k1 ECDLP. Both a point-addition subroutine (ZK-attested) and a full attack (derived).
- **layer**: logical-circuit (ZK statements), logical-algorithm (Eq. 1), physical-architecture (<500k).
- **metrics**

  | name | value | statistic | quote | location |
  |---|---|---|---|---|
  | PA low-qubit | ≤2,700,000 T; ≤1,175 q; ≤17,000,000 ops | average executed | "with resource counts of at most: • 2,700,000 non-Clifford gates (CCX + CCZ) • 1,175 logical qubits • 17,000,000 total operations" | App. A.1, Statement 1 |
  | PA low-gate | ≤2,100,000 T; ≤1,425 q | avg | "• 2,100,000 non-Clifford gates (CCX + CCZ) • 1,425 logical qubits" | App. A.2, Statement 2 |
  | full ECDLP | ≤1,200 q / ≤90M T; or ≤1,450 q / ≤70M T | — | "either ≤1200 logical qubits and ≤90 million Toffoli gates or ≤1450 logical qubits and ≤70 million Toffoli gates" | Abstract |
  | physical | <500,000 | physical qubits | "On superconducting architectures with 10⁻³ physical error rates and planar connectivity, those circuits can execute in minutes using fewer than half a million physical qubits." | Abstract |
  | T statistic | — | mean | "we report the average executed Toffoli count as measured across the 9024 evaluated test cases" | App. A.3 |
  | full-attack formula | (PA + 3×2^w)×(2n/w − 4) | — | "ECDLP_Toff^n = (PA_Toff^n + 3×2^w)×(2n/w − 4) (1)" | App. A.3, Eq. (1) |

- **what the ZK proof attests**
  - The SP1 guest "computes a SHA-256 hash of the input circuit and commits it as a public output, along with the demanded resource counts … uses the SHAKE256 … to generate 9024 test inputs via the Fiat-Shamir transform … simulates the parsed circuit using the kickmix simulator on the 9024 Fiat-Shamir derived test cases … asserts that the input private circuit satisfies the demanded resource counts" (App. A.3, zkVM paragraph).
  - Statement: the circuit "correctly computes point addition on the elliptic curve secp256k1 across all 9,024 pseudo-random inputs deterministically derived from the circuit's own hash" (A.1).
- **what is hidden**
  - The circuits themselves; only the hashes are public (low-qubit `0x5373e67c…`, low-gate `0x04f17175…`).
  - The exact Q and T: only upper bounds are proved.
  - Any failure rate beyond 0/9,024. Nonce-style selection is not excluded by the statement [INFERENCE].
  - The full-attack 90M/70M totals and the <500k physical figure are **not** in the proof. They are derived via Eq. (1) and a surface-code compilation.
- **addend_interface**
  - The operation is "Q ← Q + P[k] where P is a (classically) pre-computed table … k is a w-qubit quantum register" (A.3).
  - The lookup is billed separately as "3×2^w" in Eq. (1). [RECOMPUTED] 28×(2.7M + 196,608) = 81.1M ≤ 90M ✓.
  - ECDSA.Fail labels Google "Window-indexed" (Table 3).
  - [INFERENCE] Whether the 2.7M includes any index-handling cost that the classical-addend benchmark omits is not determinable from the hidden circuit.
- **counting_conventions**: CCX+CCZ, average executed over the 9,024 FS inputs. This is the same evaluator lineage as ECDSA.Fail (Ivezic: Anant "recorded in April that it uses the same 9,024-input test procedure and instruction set").
- **independent_verification**: proof verifiable with the published key. Trail of Bits forged a v1 proof claiming 0 Toffolis / 1,164 qubits (blog 2026-04-17, per prior notes; not re-read here).
- **non-comparability**: bounds (≤) vs measured values. Full attack vs subroutine. The physical figure is architecture-specific (superconducting, 10⁻³, planar).

### LUO — Luo, Yang, Wang, Su, Li
- **source**
  - title: "Space-Efficient Quantum Algorithm for Elliptic Curve Discrete Logarithms with Resource Estimation"
  - id: arXiv 2604.02311**v2** (v1 2 Apr 2026; v2 18 Apr 2026)
  - url: https://arxiv.org/abs/2604.02311
  - license: arXiv non-exclusive distribution license (not CC)
  - read depth: **partial**. Read: abstract, §1, Tables 1–2, §5.4 equations, via PDF. The HTML is truncated by a conversion error.
- **target**: full ECDLP on a 256-bit prime-field curve. scope = **full attack**.
- **layer**: logical-algorithm (asymptotic + leading-order).
- **metrics**

  | value | quote | location |
  |---|---|---|
  | 1,333 q at n = 256 | "our estimate reduces the logical-qubit count to 1333, compared with 2124 in the previous low-width implementation of Häner et al." | Abstract; Table 2 |
  | qubits formula | "5n + 4⌊log₂n⌋ + O(1) qubits" | Abstract |
  | Toffolis per add | "a single controlled affine point addition requires (4·204 + 4·32 + 32)n² log₂ n + O(n²) = 976n² log₂ n + O(n²)" | §5.4 |
  | total | "976n³ + O(n³/log n) Toffoli gates in total" | §1 Contributions |
  | 835 q | **not found** in v2 | — |

- **failure**: claims exactness: "remaining exactly correct, in contrast to the fidelity loss incurred in [PZ03]" (§1).
- **addend_interface**: controlled affine point addition (textbook, not windowed).
- **counting_conventions**: leading-order formulas from the RNSL17 resource table. No concrete T at n = 256 in the text (only Figure 1). [RECOMPUTED] The leading term is 5.1×10⁸ per addition.
- **independent_verification**: Gu et al. reconstructed it as 69,529,757 T at 838 q (certified, classical addend). That is ≈7× below the leading-order formula; the two do not reconcile without the O(n²) terms and the control/addend differences.
- **non-comparability**: ECDSA.Fail cites "Luo et al.'s recent 835-qubit result [41]" (§1.1). The paper's own headline is 1,333 for full Shor, and I did not find 835 in v2. Treat 835 and 838 as *third-party point-add reconstructions*, not Luo's claim.

### CD-50 — CoinDesk, 2026-09-10
- **source**: Shaurya Malwa, "Crypto researchers cut Bitcoin and Ethereum quantum attack estimate by 50%", CoinDesk, Sep 10 2026 9:00 a.m. EDT, https://www.coindesk.com/tech/2026/09/10/crypto-researchers-cut-bitcoin-and-ethereum-quantum-attack-estimate-by-50. © CoinDesk. Read depth: **partial** (first ~60% of the body).
- **claim**: headline: "cut Bitcoin and Ethereum quantum attack estimate by 50%".
- **body**: "The estimated work needed for a key step in a future quantum attack … has fallen by more than half". "The new circuit scores about 1.5 billion, more than 50% below the roughly 3 billion score reported by Google". "The paper cautioned that the comparison is not perfectly like-for-like".
- **matches source?**
  - **Headline: no.** The source is a subroutine Q×T proxy with a classical addend, not an attack estimate.
  - The body is accurate.
  - The paper's own coherent variant is 1.961 B, which is 34.5% below 2.9925 B, not 50% [RECOMPUTED].
  - The 50% compares 1.496 B with 2.993 B, the low-gate bound. Against the low-qubit bound (3.17 B) it would be 52.8%.

### IONQ-PR — IonQ press release (Sep 2026)
- **source**: IonQ, "IonQ Publishes World's First Fully Compiled, End-to-End Blueprint for Breaking 256-Bit Elliptic-Curve Signatures", investors.ionq.com, Sep 2026 (exact day not shown in the fetched meta). Paper arXiv 2609.05625 **not read**. Read depth: **snippet-only** (meta description).
- **claim**: "This work concludes that a 20,000-physical-qubit IonQ quantum computer is expected to break secp256k1 … in just under 26 days."
- **matches source?** Partly verified second-hand. Ivezic cites "19,397 ions" and "runtime of 25.7 days per attempt". "Per attempt" is dropped in the press line [INFERENCE: success probability per attempt not checked].
- **layer**: physical-architecture, full attack, coherent lookups included ("about 1.4 million per addition with the lookups included", Ivezic).

---

## 3. The three most misleading comparisons found

1. **"893 logical qubits ⇒ 25% fewer physical qubits for Google/IonQ/Oratomic attacks"** (PLDD-25, 2026-10-13 X post, relayed by Ivezic). It crosses three gates at once:
   - logical→physical layer
   - subroutine→full attack
   - classical→coherent addend

   The paper's own data shows coherent selection costs "11 more qubits and about 30% more Toffolis" (+11 q, ×1.296 T recomputed from 1,151/1,299,453 → 1,162/1,684,161). Ivezic's architecture rescalings give "16% at most" for Oratomic, and ~28% for IonQ only with a longer run, because "Long's circuit uses 2.2 million before any lookup … about 1.6 times as much". The basis of the 25% is not found [INFERENCE: 1 − 893/1,175 = 24%].
2. **Headline: "Crypto researchers cut Bitcoin and Ethereum quantum attack estimate by 50%"** (CoinDesk, 2026-09-10), echoed by the leaderboard's "68.5% ahead of Google's classified circuit" (homepage, snippet-only). Problems:
   - It compares a *measured average* Q×T of a **classical-addend** kernel (1.496 B) with the *upper bounds* of Google's **window-indexed** circuit (2.99 B).
   - It labels that a cut to the "attack estimate".
   - The paper's like-for-like coherent variant is 1.961 B (−34.5%).
   - The paper itself says "contextual rather than claims of formal dominance".
   - The leaderboard percentage is already stale: 69.4% on 2026-10-23 [RECOMPUTED].
3. **"893 qubits, 2.2M Toffolis, passed all 9,024 inputs" placed next to Gu et al.'s "4.0M Toffolis, 935 qubits" (and Gu's own 893-qubit j9 at 7.87M) as if on one frontier.**
   - The failure gates differ. ECDSA.Fail requires 0/9,024 on a hash-seeded set that the submitter can re-roll: "Submitters can search these nonces for an error-free test set". Long's GPU filter returned 196 candidates in 4,096 nonces.
   - Long's own 360,960-shot test gives p̂ = 3.08×10⁻⁴, 95% CP [2.53, 3.70]×10⁻⁴. That **exceeds** Gu's grader budget of "at most 20 failed tests out of 100,000" (2×10⁻⁴).
   - So the lower-T circuit is not admissible under the other benchmark's rule. Ivezic: read "passed all 9,024 inputs" as "an approximate circuit with a chosen test set".
   - Runner-up: Schrottenloher's "≤2^−13.3" from 0/10,000 holds only at ≈63% confidence (95%: ≈2^−11.7). His numbers also appear unwindowed in Gu (1.9M / 1,446) and windowed in ECDSA.Fail (2.59M / 1,208; 2.06M / 1,462).

## 4. Gaps / not done
- X post (PLDD-25) and the Zenodo ZK record were not opened.
- IonQ arXiv 2609.05625 and Oratomic 2603.28627 were not read; their numbers are second-hand via Ivezic.
- ECDSA.Fail Supplemental Notes and the GitHub repo NOTICE file were not read.
- The ECDSA.Fail homepage figure is snippet-only.
- Luo's "835" was not located.
- Gu's T statistic (mean vs fixed) was not found.
