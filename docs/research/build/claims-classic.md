# Claim cards — classic / foundational quantum-cryptanalysis resource estimates

Built 2026-10-23. Every source was downloaded from arXiv as a PDF and converted with `pdftotext`. "pN" means **PDF page N** (form-feed count in the extracted text). Read depth: the resource-estimate, results and assumption sections were read in full for every paper. Proof and arithmetic-construction sections were read only partially, as noted on each card. Quotes are verbatim from the extracted text. Where the extraction broke a superscript (for example `1.26 · 1011` = 1.26·10^11), the card gives the normalized value and the quote stays as extracted. `[INFERENCE]` marks my own reasoning. `[CHECK]` marks a deterministic arithmetic check I ran.

Licenses come from the arXiv abs pages, read 2026-10-23: 1706.06752, 2001.09580, 2306.08585 and 2108.12371 use the arXiv non-exclusive distribution licence (`arxiv.org/licenses/nonexclusive-distrib/1.0`). 1905.09749 and 2505.15917 are CC BY 4.0. That means only the CC BY sources may have long verbatim quotes redistributed freely. For the others, keep quotes short (fair use) [INFERENCE].

---

## Card RNSL17-P256

```yaml
id: RNSL17-P256
source:
  authors: [Martin Roetteler, Michael Naehrig, Krysta M. Svore, Kristin Lauter]
  title: "Quantum Resource Estimates for Computing Elliptic Curve Discrete Logarithms"
  arxiv: 1706.06752v3
  date: 2017-10-31 (v3)
  url: https://arxiv.org/abs/1706.06752
  license: arXiv non-exclusive distribution 1.0
  read_depth: full for Abstract, §1 contributions, §4.2 exceptional cases, §5 Cost and resource estimates (Tables 1–2, Fig. 11), §6 Discussion; partial for §3 arithmetic circuits
target: {problem: "ECDLP P-256 (NIST prime-field curve, n=256)", scope: "full attack (Shor ECDLP circuit = 2n controlled point additions); physical layer absent"}
layer: logical-circuit
metrics:
  - name: logical_qubits
    value: 2330
    unit: logical qubits
    statistic: worst-case (circuit width; deterministic)
    quote: "our simulation of the point addition quantum circuit for the NIST standardized curve P-256 needs 2330 logical qubits"
    location: p4, §1 contributions; also Table 2 row 256 (p21)
  - name: toffoli_count
    value: 1.26e11
    unit: Toffoli gates
    statistic: not stated (deterministic count from a regression fit, not sampled)
    quote: "the full Shor algorithm would need about 1.26 · 1011 Toffoli gates"
    location: p4, §1; Table 2 row "256 2330 1.26 · 1011 1.16 · 1011 3 848" (p21)
  - name: toffoli_depth
    value: 1.16e11
    unit: Toffoli layers
    statistic: worst-case
    quote: "256 2330 1.26 · 1011 1.16 · 1011 3 848"
    location: Table 2, p21 (columns: bits, #Qubits, #Toffoli gates, Toffoli depth, Sim time sec)
  - name: logical_qubits_formula
    value: "9n + 2⌈log2 n⌉ + 10"
    quote: "can be computed on a quantum computer with at most 9n + 2dlog2 (n)e + 10 qubits using a quantum circuit of at most 448n3 log2 (n) + 4090n3 Toffoli gates"
    location: Abstract, p1
  - name: comparison_RSA-3072 (same table)
    value: {qubits: 6146, toffoli: 1.86e13}
    quote: "Shor’s factoring algorithm for a 3072-bit modulus needs 6146 qubits and 1.86 · 1013 Toffoli gates"
    location: p4; Table 2 RSA column is "interpolation from [21]", not simulated by RNSL
assumptions:
  - text: "No physical layer: no error rate, code, cycle time, reaction time, factories or connectivity given."
    quote: not found
    location: not found
  - text: Optimisation priority is qubits first, then Toffoli count
    quote: "our overall emphasis was to minimize first the number of required logical qubits and second the Toffoli gate count"
    location: §5, p18
  - text: Only the generic affine group law (exceptional cases ignored)
    quote: "we follow the approach by Proos and Zalka and only consider the generic group law"
    location: §4.2, p16
failure:
  value: "approximate upper bound n/2^n fraction of invalid scalars from exceptional cases; no logical-error budget"
  quote: "an approximate upper bound for the fraction of invalid scalars among the superposition of all scalars due to exceptional cases in the addition law is 2n/2n+1 = n/2n"
  location: §4.2, p17
counting_conventions:
  - quote: "the controlled point addition is iterated 2n times"
    location: §5, p20
  - quote: "whenever we encounter a CNOT or NOT gate, we do not increase the counter as by our assumption these gates do not contribute to the overall depth as they are Clifford gates"
    location: §5, p20 (depth convention)
  - quote: "we have used the Montgomery approach to report the results of our experiments"
    location: §5, p18–19
  - note: "Counts are Toffoli gates, not T. No windowing and no measurement-based uncomputation. Häner et al. 2020 convert RNSL to T-count using 7 T per Toffoli and add 8 qubits (2330→2338) to reach T-depth 1."
checks:
  - "[CHECK] 9·256 + 2·8 + 10 = 2330 ✓"
  - "[CHECK] formula (448·8 + 4090)·256³ = 1.288e11, not the tabled 1.26e11 (≈2% gap). The table comes from simulation plus regression, and the closed form is an upper-bound fit. Show both; do not treat this gap as an error."
not_comparable_with:
  - "Physical-qubit or runtime claims (Webber, GE19, G25): this card has no physical layer."
  - "T-count claims, unless the Toffoli→T convention (7 T vs 4 T per AND) is fixed."
  - "Litinski 2023 per-key Toffoli counts, which use windowing, measurement-based uncomputation, multi-key amortisation and partial key bits."
```

---

## Card HJNRS20-P256-LowW / LowT / LowD

```yaml
id: HJNRS20-P256
source:
  authors: [Thomas Häner, Samuel Jaques, Michael Naehrig, Martin Roetteler, Mathias Soeken]
  title: "Improved quantum circuits for elliptic curve discrete logarithms"
  arxiv: 2001.09580v1 (only version on arXiv)
  date: 2020-01-27
  url: https://arxiv.org/abs/2001.09580
  license: arXiv non-exclusive distribution 1.0
  read_depth: full for Abstract, §1, §3 (Toffoli/AND conventions), §6 Results (Table 1, asymptotic formulas); partial for §4–5 arithmetic and Appendix D tables
target: {problem: "ECDLP on 256-bit NIST prime curve (P-256; also P-384, P-521)", scope: "full attack (Shor ECDLP); logical only"}
layer: logical-circuit
metrics:   # Table 1, p12, "256-bit modulus" block. The extraction split exponents onto a separate line; values are normalised.
  - name: logical_qubits (Low W)
    value: 2124
    statistic: worst-case
    quote: "For P256, we reduce the number of logical qubits from 2338 to 2124, while reducing the T -depth and T -count by factors of 54 and 119, respectively."
    location: §6, p12
  - name: t_count (Low W, window 19)
    value: "1.72·2^32 ≈ 7.39e9"
    unit: T gates
    statistic: not stated (deterministic Q# resource count, extrapolated for window >18)
    quote: "Low W   19   1.32 · 2 1.76 · 2 1.72 · 2 1.45 · 2 1.98 · 230 1.89 · 232 2124 / 34 26 32 35"
    location: Table 1, p12 (exponents 34/26/32/35 extracted on the following line)
  - name: t_depth (Low W)
    value: "1.98·2^30 ≈ 2.13e9"
    quote: same row
    location: Table 1, p12
  - name: t_count (Low T, window 19)
    value: "1.08·2^31 ≈ 2.32e9"
    unit: T gates
    quote: "Low T   19   1.75 · 233 1.95 · 227 1.08 · 231 1.80 · 234 1.44 · 229 1.85 · 231 2619"
    location: Table 1, p12
  - name: logical_qubits (Low T)
    value: 2619
    quote: same row
    location: Table 1, p12
  - name: t_count / t_depth / qubits (Low D, window 15)
    value: {t_count: "1.34·2^32 ≈ 5.76e9", t_depth: "1.12·2^24 ≈ 1.88e7", qubits: 2871}
    quote: "Low D   15   1.04 · 234 1.61 · 228 1.34 · 232 1.40 · 234 1.12 · 224 1.40 · 227 2871"
    location: Table 1, p12
  - name: RNSL baseline as re-expressed by HJNRS
    value: {t_count: "1.60·2^39 ≈ 8.8e11", t_depth: "1.69·2^36", qubits: 2338}
    quote: "RNSL     –       –          –      1.60 · 239     –      1.69 · 236     –      2338"
    location: Table 1, p12
  - name: asymptotic Low W
    quote: "about 8n + 10.2 blg nc − 1 logical qubits using roughly 436n3 − 1.05 · 226 T -gates at a T -depth of 120n3 − 1.67 · 222"
    location: §6, p12
  - name: asymptotic Low T
    quote: "require about 10n + 7.4 blg nc + 1.3 qubits and need 1115n3 / lg n − 1.08 · 224 T gates"
    location: §6, p12
assumptions:
  - text: "No physical layer."
    quote: not found
    location: not found
  - text: Window sizes above 18 extrapolated, not simulated
    quote: "Window sizes above 18 were too large to simulate, so we extrapolated from the costs for smaller lookup tables."
    location: §6, p11–12
  - text: Uses n (not n+1) windows because NIST curve order < modulus
    quote: "We can use n instead of n + 1 because the order of each NIST curve is less than its modulus"
    location: §6, p12
failure:
  value: "not stated numerically; exceptional cases treated as negligible, following RNSL / Proos–Zalka"
  quote: "Proos and Zalka [25] and RNSL [27] both argue that these exceptional cases only slightly distort the desired quantum state in Shor’s algorithm and their influence is negligible."
  location: §5, p10
counting_conventions:
  - quote: "It uses 4 T gates, while a Toffoli gate uses 7, and the inverse AND† uses no T gates while Toffoli† uses 7."
    location: §3, p4
  - quote: "we assume that with 8 extra qubits (c.f. Section 3) they can use Toffoli gates of T-depth 1"
    location: §6, p12 (this is how RNSL's 2330 becomes 2338)
  - quote: "We multiplied this cost by the number of windows dividing 2n to get the full cost of Shor’s algorithm for ECDLP."
    location: §6, p12 (windowing plus QROM lookups)
checks:
  - "[CHECK] 1.60·2^39 / (1.72·2^32) = 119.1 ✓ (claimed 119×)"
  - "[CHECK] 1.69·2^36 / (1.98·2^30) = 54.6 ✓ (claimed 54×)"
  - "[CHECK] RNSL T-count 8.8e11 / RNSL Toffoli 1.26e11 = 6.98 ≈ 7 T/Toffoli ✓"
not_comparable_with:
  - "Toffoli-count claims (RNSL, Litinski, GE19, G25) unless converted. The T-count mixes AND (4T) and Toffoli (7T) and has no single Toffoli equivalent. Dividing by 4 or 7 gives only bounds [INFERENCE]."
  - "Low W, Low T and Low D are three different circuits: different window, width and depth. Never mix metrics across rows."
```

---

## Card WEB22-ECC256-1h / 1day / 10min

```yaml
id: WEB22-ECC256
source:
  authors: [Mark Webber, Vincent Elfving, Sebastian Weidt, Winfried K. Hensinger]
  title: "The Impact of Hardware Specifications on Reaching Quantum Advantage in the Fault Tolerant Regime"
  arxiv: 2108.12371v3
  date: 2021-11-11 (v3). Journal version AVS Quantum Science 2022, not verified in this pass; the arXiv abs page shows no journal-ref.
  url: https://arxiv.org/abs/2108.12371
  license: arXiv non-exclusive distribution 1.0
  read_depth: full for Abstract, §1.2 Breaking Bitcoin's encryption, §2.1–2.2, §3 ECC results (Fig. 2 caption and text p12–14); partial for the FeMoco sections
target: {problem: "ECDLP 256-bit (Bitcoin = secp256k1; the logical inputs are taken from HJNRS20 NIST-curve estimates)", scope: "full attack (one key) at the physical layer"}
layer: physical-architecture (logical inputs inherited from HJNRS20 Low D)
metrics:
  - name: physical_qubits @ 1 hour
    value: 317e6
    statistic: not stated (point estimate from a model)
    quote: "It would require approximately 317 million physical qubits to break the encryption within one hour using the surface code, a code cycle time of 1 µs, a reaction time of 10 µs, and physical gate error of 10−3 ."
    location: Abstract, p1; repeated §3, p13
  - name: physical_qubits @ 1 day
    value: 13e6
    quote: "To break the encryption instead within one day it would require 13 million physical qubits."
    location: Abstract, p1
  - name: physical_qubits @ 10 min
    value: 1.9e9
    quote: "To break it within 10 minutes with the same code cycle time it would require 1.9 billion physical qubits"
    location: §3, p13
  - name: physical_qubits @ 1h, p=1e-4
    value: 33e6
    quote: "this is reduced down to 33 million for a base error of 10−4"
    location: §3, p14
  - name: logical inputs used
    value: {t_count: 5.76e9, logical_qubits: 2871, t_depth: 1.88e7}
    quote: "We use the logical resources of the depth optimized approach provided by Haner et al [48] for 256 bit encryption, which corresponds to 5.76 · 109 T gates, 2871 logical qubits, and a measurement depth (Tdepth ) of 1.88 · 107 ."
    location: §3, p13
assumptions:
  - {text: physical error 1e-3, quote: "physical gate error of 10−3", location: Abstract p1}
  - {text: code cycle 1 µs; reaction time 10 µs, quote: "a code cycle time of 1 µs, a reaction time of 10 µs", location: Abstract p1}
  - text: Reaction time is modelled as depending on the cycle time, so the abstract's "10 µs" is ≈10.25 µs at 1 µs CC [INFERENCE from formula]
    quote: "Assuming the relationship between reaction time (RT) and code cycle time (CC) of RT = CC/4 + 10 µs"
    location: Fig. 2 caption, p12
  - text: Logical error model
    quote: "pL = 0.1(100p)(d+1)/2 . (2)"
    location: §2.2, p4
  - text: Factories are AutoCCZ, with CCZ catalysed to 2 T
    quote: "These trends utilize AutoCCZ factories to trade space for time to reach the desired run time and assume that a CCZ state can be efficiently traded for 2 T gates [58]"
    location: Fig. 2 caption, p12
  - text: Connectivity is surface code with nearest neighbour on a 2D grid (stated generally)
    quote: "the surface code which relies only on nearest neighbour interactions between physical qubits arranged on a 2D grid"
    location: §1, p2
  - text: Physical qubits per logical qubit
    quote: "in the surface code the number of physical qubits per logical qubit scales as 2d2"
    location: §2.2, p4
failure:
  value: "~6% final output error"
  quote: "We use a base physical error rate of 10−3 and a final output error of ∼ 6%."
  location: Fig. 2 caption, p12
counting_conventions:
  - quote: "A Toffoli gate can be decomposed using 4 T gates [57] , whereas the CCZ states normally produced for the Toffoli gate can be efficiently catalyzed into two T states [58] ."
    location: §2.1, p4
  - quote: "These resource estimates are solely a function of algorithm meta information such as total T count, measurement depth, and the number of logical qubits."
    location: p12
checks:
  - "[CHECK] Inputs match HJNRS20 Table 1 Low D: 1.34·2^32 = 5.755e9 ✓; 1.12·2^24 = 1.879e7 ✓; 2871 ✓"
not_comparable_with:
  - "Any estimate without a deadline. This card is runtime-constrained: physical qubits are bought to hit 1 h, 1 day or 10 min. 13M at 1 day vs 317M at 1 h shows a 24× qubit swing for the same problem."
  - "GE19 or G25 physical counts as 'RSA vs ECC'. Different problem, different factory model, and 2d² vs 2(d+1)² qubits per patch."
  - "Litinski 2023: different algorithm (≈50–109M Toffoli vs ~1.4e9 Toffoli-equivalent here [INFERENCE: 5.76e9 T / 4]) and different connectivity."
  - "Applying a 'Bitcoin' label to a NIST-curve circuit is an [INFERENCE] the paper makes implicitly. secp256k1 has a=0, which may change constant costs slightly; no secp256k1-specific circuit is given."
```

---

## Card LIT23-ECC256-AV / LIT23-ECC256-baseline

```yaml
id: LIT23-ECC256
source:
  authors: [Daniel Litinski]
  title: "How to compute a 256-bit elliptic curve private key with only 50 million Toffoli gates"
  arxiv: 2306.08585v1
  date: 2023-06-14
  url: https://arxiv.org/abs/2306.08585
  license: arXiv non-exclusive distribution 1.0
  read_depth: full for Abstract, intro (p1–4), §1 subroutine breakdown incl. algorithmic modifications (p4–10), §2 Resource estimate (p10–12); partial for appendix figures
target: {problem: "ECDLP 256-bit, generic short-Weierstrass curve (no specific curve named; 'not found' for secp256k1/P-256)", scope: "full attack, amortised per key"}
layer: logical-algorithm + physical-architecture (two architectures)
metrics:
  - name: toffoli_count per key (k parallel instances)
    value: "(44 + 65/k)·1e6 → 109e6 at k=1; asymptote 44e6"
    statistic: not stated (deterministic count, amortised)
    quote: "The resulting Toffoli count for k parallel instances is (44k + 65) · 106 Toffoli gates and (2.8k + 3.8) · 109 blocks of active volume. Asymptotically, the cost per key approaches 44 million Toffoli gates and 2.8 billion logical blocks of active volume for large quantum computers. We adjust these costs by a factor of 10/9"
    location: §2, p10–11
  - name: toffoli_count per key (headline)
    value: 50e6
    quote: "How to compute a 256-bit elliptic curve private key with only 50 million Toffoli gates"
    location: Title, p1. The body never derives 50M explicitly. [INFERENCE] 44M × 10/9 ≈ 48.9M ≈ "50 million", i.e. the k→∞ asymptote.
  - name: baseline single-key
    value: {logical_qubits: 6000, toffoli: 109e6}
    quote: "In total, we need 6000 logical qubits and 109 million Toffoli gates per key."
    location: §2.1, p10
  - name: physical_qubits baseline (2D-local, d=28)
    value: 9.4e6
    quote: "Therefore, both require 9.4 million physical qubits. With a 1 µs code cycle, superconducting qubits generate one key every 484 · 28 seconds, or 3.8 hours."
    location: §2.1, p10
  - name: runtime baseline
    value: {"1 µs cycle": "3.8 h/key", "1 ms cycle (ions)": "160 days/key", "10 µs cycle": "38 h/key"}
    quote: "By contrast, a device with strict 2D-local connectivity requires more qubits and produces one key every 38 hours."
    location: Abstract p1 (10 µs case); p10 (1 µs and 1 ms cases)
  - name: physical_qubits active-volume
    value: "6000 × 1152 = 6.9e6 [CHECK: arithmetic mine]"
    quote: "At 10% threshold, assuming a 10-µs code cycle and non-local connections, one key can be generated every 10 minutes using 6000 modules with 1152 physical qubits each."
    location: Abstract, p1
  - name: runtime active-volume
    value: "9.7 min/key (1 key at a time); 1.4 min/key with 4× footprint and 4 keys in parallel"
    quote: "With a 10-µs code cycle, a device with 6000 logical qubit modules can generate one key every 9.7 minutes. A device with four times the footprint that generates four keys in parallel can generate one key every 1.4 minutes"
    location: p4
  - name: active_volume per key
    value: "6.6e9 blocks (1 key); 3.75e9 blocks (4 parallel)"
    quote: "In the first scenario, the active volume per key is 6.6 billion blocks, while in the second scenario, the active volume per key is reduced to 3.75 billion blocks"
    location: §2.2, p11
assumptions:
  - {text: physical error 10% of threshold, quote: "assume a physical error rate at 10% of the surface-code threshold error rate, which is a common assumption in the literature", location: p3}
  - {text: logical error model, quote: "contribute a logical error rate of pL = 10−d/2 at 10% threshold", location: §2.1 p10}
  - {text: code distances 28 (baseline) and 24 (AV), quote: "The source of the footprint reduction is a distance reduction from d = 28 to d = 24 due to the reduced volume of the computation.", location: p4}
  - {text: reaction time 10 µs standard, not optimised, quote: "A standard assumption in the literature is 10 µs, as indicated in Fig. 1, but this is not a physical limit", location: p4}
  - text: connectivity is a logarithmic number of non-local inter-module links (AV) vs 2D-local (baseline)
    quote: "a fault-tolerant surface-code quantum computer consists of modules with a logarithmic number of non-local inter-module connections"
    location: Abstract p1
  - text: Physical qubits per logical are 2d² (circuit-based) vs d² data qubits per module (photonic AV)
    quote: "each distance-d logical qubit consists of 2d2 physical qubits"
    location: §2.1 p10
failure:
  value: "code distance chosen so the expected runtime before a logical error is 10 phase-estimation blocks; baseline ≈20% logical-error probability after 10 blocks at d=28"
  quote: "With d = 28, the probability of a logical error after 10 phase estimation blocks is around 20% in this estimate."
  location: §2.1, p10; rule stated p9: "we will choose the code distance such that the expected runtime before a logical error is 10 phase estimation blocks"
counting_conventions:
  - quote: "Instead of using 16 repetitions of the group-of-16 operation in Fig. 4b, we can use only 13 repetitions to generate 208 of the 256 bits of the rescaled private key ck. This narrows down the list of possible candidates to 248 keys."
    location: p9–10 (partial-key output plus 2^48 classical brute force at "O(106 ) CPU hours")
  - quote: "multiple private keys k1...m of the same elliptic curve can be generated by repeating the second phase estimation m times for different public keys"
    location: p9 (multi-key amortisation; the 10/9 factor)
  - quote: "k numbers can be inverted using 3k − 3 multiplications and a single inversion"
    location: p10 (Montgomery batch inversion across parallel instances)
  - quote: "Note that this gate count is slightly lower than the gate count in Ref. [8] because of the use of Gidneystyle arithmetic circuit [25] with fewer Toffoli gates due to measurement-based uncomputation."
    location: p8
  - quote: "We will apply the cost estimate for the n-controlled Toffolis to Toffoli gates with n controls as well as groups of n standard 2-controlled Toffoli gates."
    location: p4
  - note: "Windowing with a 16-bit window and a 2^16-entry QROM lookup: 'A windows size of 16 was chosen to optimize the resource count for 256-bit keys' (Fig. 4 caption, p5)."
checks:
  - "[CHECK] 6000 × 2·28² = 9,408,000 ≈ 9.4M ✓; 2·24² = 1152 ✓"
  - "[CHECK] 484e6 logical cycles × 28 µs = 13,552 s = 3.76 h ≈ 3.8 h ✓; ×10 for a 10 µs cycle = 37.6 h ≈ 38 h ✓"
not_comparable_with:
  - "Single-key, full-bit estimates (RNSL, HJNRS, Webber). The 50M headline is an asymptotic per-key amortised figure over many keys of the same curve and many parallel instances, with 48 bits recovered classically. The honest single-key, k=1 analogue is 109M."
  - "Physical counts from 2D-local papers (GE19, G25, Webber) against the AV figure (6.9M, 10 min). The connectivity assumption differs."
  - "'10% of threshold' is not the same as 'p = 1e-3' unless the threshold is 1%, which Litinski does not state numerically ('not found')."
```

---

## Card GE19-RSA2048

```yaml
id: GE19-RSA2048
source:
  authors: [Craig Gidney, Martin Ekerå]
  title: "How to factor 2048 bit RSA integers in 8 hours using 20 million noisy qubits"
  arxiv: 1905.09749v3
  date: 2021-04-13 (v3; published Quantum 5, 433 (2021) per arXiv journal-ref)
  url: https://arxiv.org/abs/1905.09749
  license: CC BY 4.0
  read_depth: full for Abstract, §1 (Tables 1–2), §2.8–2.14 (Toffoli/runtime/error/physical counts), §3.1–3.2 (Table 3); partial for §3.3 DLP and appendices
target: {problem: "RSA-2048 (via Ekerå–Håstad short DLP)", scope: "full attack"}
layer: physical-architecture (+ logical-circuit formulas)
metrics:
  - name: physical_qubits
    value: 20e6
    unit: physical qubits
    quote: "2048                      15   27    4     5     5     1024   31%        4.1        5.9     20           5.1"
    location: Table 3, p16 (columns n, d1, d2, δoff, cmul, cexp, csep, Retry Risk, Volume per run, Volume expected, Qubits megaqubits, Runtime hours per run)
  - name: runtime per run
    value: 5.1
    unit: hours
    statistic: per run (single attempt)
    quote: same Table 3 row
    location: Table 3, p16
  - name: runtime expected
    value: "0.31 days ≈ 7.4 h (title '8 hours')"
    statistic: expected (includes retries)
    quote: "Expected runtime (days) 410 10 1.1 3.7 1 6 0.36 0.31"
    location: Table 2, p3 (last column = "(ours)")
  - name: spacetime volume expected
    value: 5.9
    unit: megaqubitdays
    quote: Table 3 row above; also Table 2 "Expected volume (megaqubitdays) ... 6.6 5.9"
    location: p16, p3
  - name: toffoli_count (Toffoli+T/2)
    value: 2.7e9
    statistic: approximate upper bound
    quote: "(ours) 2019 3n + 0.002n lg n 500n2 + n2 lg n 0.3n3 + 0.0005n3 lg n 0.4 2.7 9.9"
    location: Table 1, p3 (column "Toffoli+T/2 Count (billions)", n = 1024/2048/3072)
  - name: logical qubits (abstract circuit)
    value: "3n + 0.002n lg n ≈ 6189 at n=2048 [CHECK: arithmetic mine]"
    quote: "our construction uses 3n + 0.002n lg n logical qubits, 0.3n3 + 0.0005n3 lg n Toffolis, and 500n2 + n2 lg n measurement depth"
    location: Abstract, p1
  - name: RNSL ECC-256 cross-reference
    value: "130 billion Toffoli+T/2; 83 megaqubitdays min volume"
    quote: "Roetteler et al. 2017 [74] 9n + O(lg n) 448n3 lg n + 4090n3 448n3 lg n + 4090n3 30 84 130 13 52 83"
    location: Table 1, p3
assumptions:
  - quote: "a planar grid of qubits with nearest-neighbor connectivity, a characteristic physical gate error rate of 10−3 , a surface code cycle time of 1 microsecond, and a reaction time of 10 microseconds"
    location: Abstract, p1
  - quote: "We assume distance-d logical qubits are stored using square patches of 2(d + 1)2 physical qubits"
    location: §1, p2
  - text: CCZ factories with two-level distillation (d1=15, d2=27 at n=2048)
    quote: "using a level 1 code distance 17 and a level 2 code distance of 27, this corresponds to a total distillation error of 6.4%"
    location: §2.12, p13 (worked example; Table 3 uses d1 = 15)
failure:
  value: "Retry risk 31% at n=2048 (Table 3); worked example ~27% topological error at d=27 → ~1.4 runs; ≥99% classical post-processing success per correct run"
  quotes:
    - {quote: "the probability of a topological error arising is approximately 10−d27/2+1e · 226 · 63 · 0.75 · 25 · 109 ≈ 27%", location: §2.13, p13}
    - {quote: "a single correct run of this quantum algorithm suffices for the RSA integer to be factored with at least 99% success probability in the classical post-processing", location: §3.2, p16}
counting_conventions:
  - quote: "Toffoli+T/2 Count"
    location: Table 1 header, p3
  - quote: "Using measurement-based uncomputation (appendix C of [8]), uncomputing each table lookup has a Toffoli count and measurement depth of 2^√(cexp+cmul) which is negligible"
    location: §2.5, p7 (extraction garbles the exponent)
  - quote: "These approximate upper bounds, with ne set to 1.5n, are the formulae we report in the abstract and in Table 1"
    location: §2.8, p9
  - note: "Optimises a 'skewed expected spacetime volume' s^1.2 · t/(1−ε) (§3.1, p16). The reported point is a deliberate space/time trade-off, not min-qubits."
checks:
  - "[CHECK] 5.1 h / (1 − 0.31) = 7.39 h ≈ 0.31 day ✓ → title '8 hours' is a rounded-up expected time"
  - "[CHECK] 0.3·2048³ + 0.0005·2048³·11 = 2.62e9 ≈ 2.7e9 ✓"
  - "Hand estimate in §2.14 disagrees with the title, and the paper says so: 'approximately 23 million qubits. Attentive readers will note that this number disagrees with the estimate in the title of the paper.' (p13). The script 'estimate costs.py' is authoritative."
not_comparable_with:
  - "ECC cards: different problem. Only compare via an explicit 'equivalent classical security' mapping, which GE19 itself does in Table 1."
  - "G25: same physical assumptions, but G25 counts expected Toffolis per factoring over ~9 shots, while GE19 counts one run plus a retry factor."
  - "Webber's 'Bitcoin is comparable to RSA-2048' line (p3) is Webber's framing, not GE19's."
```

---

## Card G25-RSA2048

```yaml
id: G25-RSA2048
source:
  authors: [Craig Gidney]
  title: "How to factor 2048 bit RSA integers with less than a million noisy qubits"
  arxiv: 2505.15917v1 (PDF internally dated June 9, 2025)
  date: 2025-05-21
  url: https://arxiv.org/abs/2505.15917
  license: CC BY 4.0
  read_depth: full for Abstract, §1, §2.2 masking/failure, §3.1 logical costs (Table 5), §3.2 physical costs; partial for §2.1, §2.3–2.4, Appendix A
target: {problem: "RSA-2048 (approximate residue arithmetic, Ekerå–Håstad, s=8)", scope: "full attack (expected over shots)"}
layer: physical-architecture (+ logical Table 5)
metrics:
  - name: physical_qubits
    value: "897,864 computed; reported as <1M"
    quote: "The total number of physical qubits is 897864. For slack, I report the physical qubit count as one million instead of 900 thousand."
    location: §3.2, p19
  - name: runtime
    value: "4.96 days computed; reported as < 1 week"
    statistic: expected
    quote: "Dividing 4.63 days by 93.3% gives the actual time estimate per factoring: 4.96 days. Which I round up to a week for slack."
    location: §3.2, p20
  - name: runtime per shot
    value: 12.07
    unit: hours
    quote: "produces an estimate of 12.07 hours per shot"
    location: §3.2, p20
  - name: toffoli_count
    value: 6.5e9
    statistic: expected per factoring (not per shot)
    quote: "2048    8    21    6      3      5      33    1280       1.25%         9.2         6.5e+09        1399"
    location: Table 5, p18 (columns n, s, ℓ, w1, w3, w4, f, m, Pdeviant, E(shots), Toffolis, Qubits); caption: "The Toffolis column is expected Toffolis per factoring (not per shot)."
  - name: logical_qubits
    value: "1399 (Table 5); 1409 active peak (text); 1537 incl. idle hot patches and factory region"
    quote: "the maximum logical qubit count occurs during loop4 when there are m + 3f + 2ℓ + len m = 1409 logical qubits active" / "The total number of logical qubits, including idle hot patches, is 1280 + 131 + 7 · 18 = 1537 < 1600"
    location: §3.2, p18–19
assumptions:
  - quote: "a square grid of qubits with nearest neighbor connections, a uniform gate error rate of 0.1%, a surface code cycle time of 1 microsecond, and a control system reaction time of 10 microseconds"
    location: Abstract, p1
  - quote: "use magic state cultivation [GSJ24] followed by 8T-to-CCZ distillation [Jon13] to power Toffoli gates"
    location: §3.2, p18
  - quote: "a distance of 25 is sufficient for normal surface code patches to reach a per-patch per-round logical error rate of 10−15 . So my hot patches will use 2·(25+1)2 = 1352 physical qubits per logical qubit."
    location: §3.2, p18
  - quote: "yoking with a 2D parity check code reaches a logical error rate of 10−15 when using 430 physical qubits per logical qubit"
    location: §3.2, p18 (cold storage; the paper flags this as future work: "I leave detailed analysis and simulations of cold storage, under various workloads, as future work.", p19)
  - text: six CCZ factories; 150 rounds per CCZ (rounded up from 114.7)
    quote: "In total this amounts to 114.7 rounds per CCZ state, which I round up to 150 rounds for slack."
    location: §3.2, p20
failure:
  value: "per-shot no-logical-error rate 93.3%; Pdeviant 1.25% per shot (masking/approximation); E(shots)=9.2 incl. /0.99 post-processing"
  quotes:
    - {quote: "Choosing a target logical error rate of 10−15 per logical qubit round will thus result in a no-logical-error shot rate of (1 − 10−15 )6.9·10 13 ≈ 93.3%", location: §3.2, p18}
    - {quote: "E(shots) is the expected number of shots, equal to (s + 1)/(1 − Pdeviant )/0.99 (the /0.99 accounts for the chance of postprocessing failure [Eke20])", location: Table 5 caption, p18}
counting_conventions:
  - quote: "The Toffolis column is expected Toffolis per factoring (not per shot)."
    location: Table 5 caption, p18
  - note: "Cost is counted as additions, lookups and phaseups (Table 3). Lookups follow [Bab+18]: 'These lookups need at least 26 − 6 − 1 = 57 CCZ states' (p20; read 2^6 − 6 − 1)."
checks:
  - "[CHECK] 550400 + 177112 + 170352 = 897864 ✓; 1280·430 = 550400 ✓; 131·1352 = 177112 ✓"
  - "[CHECK] E(shots) = 9/(1−0.0125)/0.99 = 9.206 ✓ (9.2)"
  - "[CHECK] exp(−1e-15 · 6.9e13) = 0.933 ✓"
  - "[CHECK] DISCREPANCY: the text says '12.07 · 9.1/24 = 4.63 days', but 12.07·9.1/24 = 4.577. 4.63 matches E(shots)=9.2 (12.07·9.2/24 = 4.627). Typo '9.1'; the conclusion is unaffected."
  - "[CHECK] DISCREPANCY: '3f + 2ℓ + len m = 131' with f=33 and ℓ=21 gives 3f+2ℓ = 141 > 131 before adding len m. Also 1280 + 131 = 1411 ≠ 1409, and Table 5 says 1399. The definition of 'len m' (Table 2) was not resolved in this pass, so the 131 / 1409 / 1399 values are not reproducible from quoted parameters. Flag for human review."
not_comparable_with:
  - "GE19 runtime: G25 is ~5 days vs GE19 ~7.4 h expected. The qubit reduction is bought with time, Toffolis and newer assumptions (yoked codes, cultivation) that GE19 did not use."
  - "ECC cards: different problem."
```

---

## Comparability commentary

1. **Layer mismatch.** RNSL17 and HJNRS20 are logical-circuit counts with no hardware. Webber, GE19, G25 and Litinski give physical numbers, each with its own cost model. A ledger must never place "2,124 logical qubits" next to "317 M physical qubits".
2. **Gate-unit mismatch.** RNSL counts Toffoli. HJNRS counts T, with AND = 4T and Toffoli = 7T mixed. Webber takes HJNRS T counts and models CCZ as 2T. GE19 reports "Toffoli+T/2". Litinski and G25 count Toffoli or CCZ with measurement-based uncomputation. There is no lossless conversion: T → Toffoli via ÷4 or ÷7 gives only bounds.
3. **Statistic mismatch.**
   - GE19 headline "8 hours" is an *expected* time over retries: 5.1 h per run, 31 % retry risk.
   - G25 "< 1 week" is an *expected* time over ~9.2 shots, rounded up from 4.96 days.
   - Litinski "50 M Toffoli" is an *asymptotic amortised per-key* figure over many keys and parallel instances, with 48 bits recovered by classical brute force. The single-key figure is 109 M.
   - Webber numbers are *deadline-constrained* physical counts.
   - RNSL and HJNRS are deterministic circuit counts with no failure budget beyond exceptional-case arguments.
4. **Failure-budget mismatch.** Budgets differ across papers: Webber ~6 % output error; GE19 31 % retry risk; Litinski ~20 % logical error after 10 blocks; G25 93.3 % per-shot success times Pdeviant 1.25 %; RNSL n/2^n invalid scalars. Normalising to expected cost needs the retry model each paper states.
5. **Physical-model mismatch.** Qubits per patch: 2d² (Webber, Litinski circuit-based) vs 2(d+1)² (GE19, G25 hot storage) vs 430/logical (G25 yoked cold storage). Error rate: 1e-3 (GE19, G25, Webber) vs "10 % of threshold" (Litinski; threshold not stated). Connectivity: 2D nearest neighbour vs active-volume non-local.
6. **Problem-scope mismatch.** Curves differ: NIST P-256 (RNSL, HJNRS), a "Bitcoin" label on a P-256-derived circuit (Webber), and a generic curve (Litinski). No source here gives a secp256k1-specific circuit.

## Surprises worth surfacing in the demo
- **G25 internal arithmetic slip:** "12.07 · 9.1/24 = 4.63 days" evaluates to 4.58. The deterministic checker catches it; 4.63 is right if 9.2 shots are used. A second unresolved inconsistency: 131 / 1409 / 1399 logical qubits.
- **GE19's own hand estimate (23 M) disagrees with its title (20 M).** The paper admits this; the script is authoritative.
- **Litinski's "50 M" appears only in the title.** The body gives (44 + 65/k) M × 10/9, plus a 13/16 truncation with a 2^48 classical search.
- **HJNRS re-baselined RNSL from 2330 to 2338 qubits** (+8 for T-depth-1 Toffolis), so "2338" and "2330" are the same circuit under different conventions.
- **Webber's logical inputs reproduce HJNRS Low D exactly** (5.755e9 T, 2871 qubits, 1.879e7 T-depth). Good provenance chain. Its reaction time is actually CC/4 + 10 µs, not a flat 10 µs.
