# Outreach drafts (send Friday evening; follow up Sunday with the live link)

Goal: one honest reply from a target user before submission ("useful / not useful / this is wrong"). Never present anyone as a customer. Log replies on [Choose the project to build](https://github.com/SeivenBell/tq-ledger/issues/14).

Contact details come from `docs/research/build/competitors-users.md`; handles marked there as search-snippet only should be checked on the profile before sending.

## Sample card to paste (plain text, until the site is live)

```
Claim: 893-qubit secp256k1 point-addition circuit (ECDSA.Fail submission 457ccb7a, 2026-10-13)
Counts: 893 logical qubits; 2,218,127 average executed Toffolis; one point addition; classical addend
Tests: passed 9,024 hash-seeded inputs after nonce filtering; 111 failures in 360,960 in the submitter's own test
Recomputed: p = 3.08e-4, 95% CI [2.53e-4, 3.70e-4] (assumes independent trials)
Not comparable with: physical-qubit counts, full-attack totals, coherent-addend circuits
Comparable with caveat: Gu et al. 2026 modinv-point-add (their failure budget is 2e-4; this interval is above it)
Every number links to the sentence it came from.
```

## 1. Marin Ivezic (postquantum.com) · LinkedIn `/in/marinivezic` or `marin@ivezic.com`

> Hi Marin, your Oct 14 piece on the 893-qubit circuit is the clearest comparison I've read, especially reading "passed all 9,024 inputs" next to the failure rate in the notes. I'm building a small open tool that does the bookkeeping part of that: one card per published claim, every number linked to its sentence, and a rule set that refuses to compare logical with physical, one step with the full attack, or classical with coherent addends. Sample card below. Would a ledger like this be useful in your workflow, and what's the first thing you'd fix? Live version by Sunday. — Severyn (Waterloo, MSc quantum information)

## 2. Gautham Anant (Eigen Labs, ECDSA.Fail) · X `@bbuddha_xyz`, LinkedIn `/in/gautham-anant`

> Hi Gautham, I've been reading ECDSA.Fail and the HashSmash design doc. I'm building something complementary for the published-paper side: claim cards for ECC and RSA cost estimates (Google, Schrottenloher, Gu et al., Litinski, Gidney), each field quoted, with gates that refuse cross-convention comparisons. It doesn't verify circuits; it links to your records. Would you want the cards in your claim-sheet format, and is there anything in how I describe leaderboard entries that you'd correct? Sample below.

## 3. Jieyi Long (ECDSA.Fail paper, first author) · X `@jieyilong`

> Hi Jieyi, your paper's line that "differing interfaces, accounting conventions, and validation scope preclude formal dominance" is the rule my open tool encodes: it puts each published ECC claim on a card with quotes and refuses comparisons across those conventions. I've modelled the benchmark and the coherent-addend variant; could you sanity-check how I describe them (sample below)?

## 4. Pierre-Luc Dallaire-Demers (Pauli Group) · X `@dallairedemers`, `contact@pauli.group`

Neutral tone: his 25 % post is one of the demo cards.

> Hi Pierre-Luc, I'm building an open ledger of published quantum cost claims for ECC and RSA, where each number links to its source and the tool states which comparisons are like for like. The 893-qubit result and the discussion of physical-qubit savings around it are in it. I want to represent your position accurately: is there a write-up of the 25 % physical-qubit estimate and its assumptions that I should cite? Corrections very welcome.

## 5. evolutionQ / Global Risk Institute (Waterloo) · contact form, X `@evolutionQinc`

> Hello, I'm a Waterloo quantum-information graduate building an open, cited ledger of quantum cryptanalysis cost claims (one card per published estimate, with rules that block comparisons across logical/physical, subroutine/full attack, and other conventions). Your June briefing on the new resource estimates is exactly the kind of reader I'm building for. Would your team be open to a 10-minute look next week? Happy to share the live link Sunday.

## Follow-up (Sunday, with link)

> Thanks again. It's live: [URL]. The card for [their item] is here: [link]. Anything wrong, I'll fix it before judging on Monday.
