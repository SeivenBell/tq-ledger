# Q-Day Ledger: domain glossary

The language of the project. Terms only; no implementation detail.

## Claims and sources

- **Source**: a dated, versioned public document that states quantum resource numbers: a paper (with its arXiv version), a benchmark leaderboard entry, a blog post, or an article. A source has an author, a date, a URL, and a licence.
- **Claim**: one statement in a source that a cryptanalytic computation needs a stated amount of quantum resources. One source can make several claims.
- **Headline**: a third-party restatement of a claim, for example a news sentence or a social post. A headline is not a source; it points (correctly or not) at one or more claims.
- **Claim card**: the structured record of one claim. Every field on a card is grounded in a quoted span of its source, or is marked *not stated*.
- **Quoted span**: the exact text in the source that supports one field, with its location (section, table, page, or character range).

## What a claim is about

- **Target problem**: the cryptographic problem the computation attacks: the elliptic-curve discrete logarithm on a named curve (secp256k1, P-256), or factoring a named RSA modulus size (RSA-2048).
- **Scope**: how much of the attack the claim covers.
  - **Subroutine**: one building block, for example a single elliptic-curve point addition or a modular inversion.
  - **Full attack**: the complete computation that recovers a private key or a factor.
- **Layer**: what kind of resource the numbers count.
  - **Logical circuit**: gates and qubits of an error-free circuit for a subroutine.
  - **Logical algorithm**: total logical resources for a full attack (logical qubits, Toffoli or T gates), before error correction.
  - **Physical architecture**: physical qubits and runtime under stated hardware assumptions (error rate, code, cycle time).
- **Cost statistic**: how a gate count is summarised: **worst-case** (gates in the fixed circuit), **average executed** (mean over inputs when some gates are skipped), or **expected**.
- **Addend interface**: for point addition, whether the point being added is **classical** (known in advance) or **coherent** (held in qubits). Classical addends are cheaper and are not interchangeable with coherent ones.
- **Counting convention**: a stated rule for counting, for example "a CCZ counts as one Toffoli", "table lookups are excluded", or "measurement-based uncomputation is used".
- **Hardware assumption**: a physical parameter a physical-architecture claim depends on: physical error rate, error-correcting code, code cycle time, reaction time, number of magic-state factories, connectivity.

## Correctness of a claimed circuit

- **Failure budget**: the probability of a wrong result that the authors allow.
- **Observed failures**: wrong results found in testing, reported as failures out of tests (for example 111 out of 360,960).
- **Test support**: the inputs a circuit was tested on (a fixed public set, a hash-seeded set, held-out inputs).
- **Independent verification**: a check of the claim by someone other than its authors, with who did it and how.

## Comparing claims

- **Comparability gate**: a rule that must hold before two numbers can be compared: same target problem, same scope, same layer, same cost statistic, same addend interface, and compatible failure budgets.
- **Verdict**: the outcome of comparing two claims on one metric.
  - **Comparable**: every gate holds.
  - **Comparable with a stated conversion**: gates hold after a conversion the ledger names (for example a unit change).
  - **Not comparable**: at least one gate fails; the verdict names the gate.
- **Misleading headline**: a headline that compares or restates claims across a failed gate, for example presenting logical qubits of one subroutine as physical qubits for a full attack.

## Trust status of a card

- **Machine-extracted**: fields proposed by a model, each with a quoted span that passed the span check.
- **Human-reviewed**: a named reviewer confirmed every field against its source.
- **Reproduced**: the card's checkable numbers were recomputed from public artefacts.
- **Span check**: the quoted span occurs verbatim in the source.
- **Number check**: the field's value can be read from its quoted span.
