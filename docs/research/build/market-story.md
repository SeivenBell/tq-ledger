# Investor value story for the Q-Day Claim Ledger

## Summary
- **Real money already depends on Q-Day timing, but nobody puts a number on it.** BlackRock's IBIT prospectus spends a whole paragraph on quantum risk and gives no figure. Coinbase, which custodies about 12% of all BTC, set up a board to "respond in real time" to breakthroughs. Aon and Moody's warn insurers about "silent quantum" exposure. In HKMA's July 2026 survey, 73% of Hong Kong banks named the lack of models and tools to quantify quantum risk as a top-three barrier.
- **Estimates move fast and count different things.** I counted at least 9 public quantum-cost estimates for ECC or RSA between March and October 2026, plus a leaderboard that updates every day. ECDSA.Fail cut its own score 86.1% in about 8 weeks. In 2025, Gidney cut the RSA estimate 20×. The figures people quote mix logical and physical qubits, one point addition and the whole attack, and minutes and months.
- **Georgian has stated a thesis this fits.** A Georgian post from May 2026 says "verifiability is what turns comfort from a feeling into evidence" and calls "domain-specific evals" a trust-layer product surface. Deval Pandya has said publicly that independent evaluation is "vital".
- **Evidence against the pitch, which belongs in it:**
  - The Coinbase board calls the timeline debate "largely irrelevant".
  - Ivezic argues the algorithm curve is flattening toward a floor.
  - Bloomberg's James Seyffart calls ETF quantum disclosures "completely standard".
  - No named buyer has committed.
  - Ivezic is a possible competitor and Eigen could build this (see the existing memo).

---

## 1. Who makes money decisions on Q-Day timing

| Actor | Primary evidence (verbatim, location) | Date | Read depth |
|---|---|---|---|
| **ETF issuer: BlackRock IBIT** | "developments in mathematics and/or technology, including advances in digital computing, algebraic geometry and quantum computing, could result in such cryptography becoming ineffective… there is no guarantee that new quantum-proof architectures will be built and appropriate transitions will be implemented across the network at scale in a timely manner" (Prospectus, Risk Factors, p.24). NAV "$74,198,915,391" as of June 27, 2025 (p.20). [Prospectus](https://www.ishares.com/us/literature/prospectus/p-ishares-bitcoin-trust-12-31.pdf) | Prospectus 2025-07-31, Supplement No.1 2025-11-21 | partial (cover, pp.18–24) |
| ETF disclosure, **disconfirming** | Seyffart (Bloomberg): "These are just basic risk disclosures… It's completely standard." Cited in [TQI](https://thequantuminsider.com/2025/05/13/blockrock-updates-bitcoin-etf-with-broadened-warning-about-quantum-computing/). Morgan Stanley's MSBT S-1 (2026-03-17) also flags quantum, per [CCN](https://www.ccn.com/education/crypto/morgan-stanley-bitcoin-etf-msbt-quantum-computing-risk-launch/). I could not grep the primary S-1. | 2025-05-13; 2026-04-03 | full (secondary) |
| **Exchange/custodian: Coinbase** | The board will "**Respond in real time** to major quantum computing breakthroughs with independent analysis and practical guidance." Members: Aaronson, Boneh, Drake, Kannan, Lindell, Malkhi. [Coinbase blog](https://www.coinbase.com/blog/coinbase-establishes-independent-advisory-board-on-quantum-computing-and-blockchain). Coinbase "holds about 12% of all bitcoin… for its clients"; CoinDesk corrected Coinbase's own 5% figure. [CoinDesk](https://www.coindesk.com/tech/2026/10/14/coinbase-which-holds-5-of-all-bitcoin-wants-the-quantum-fix-started-now) | 2026-01-21; 2026-10-14 (upd. 10-19) | full |
| Coinbase board, **disconfirming** | "we believe that this debate on timelines is largely irrelevant (beyond that it is not imminent) since migrations should be planned for and prepared now", quoted by [Ivezic](https://postquantum.com/security-pqc/coinbase-quantum-blockchain-paper-analysis), who adds the paper is "surprisingly vague" on qubit numbers | 2026-04-21 | partial |
| **Banks: HKMA survey (KPMG analysis)** | "lack of established models, tools, or industry-standard frameworks to systematically quantify and evaluate quantum-related risks, cited by 73%"; "rapid evolution of the quantum computing landscape was cited by 47%"; "these PQC transition timelines are constantly being revised due to new scientific and technological breakthroughs. As a result, AIs should continue to monitor these breakthroughs and adjust their timelines accordingly." Only "5%" have quantum-risk monitoring "embedded within ongoing risk reporting". [HKMA PDF](https://www.hkma.gov.hk/media/eng/doc/key-information/press-release/2026/20260727e3a1.pdf) | July 2026 | partial (grep: exec summary, §2.1.2, §3.2) |
| **FS-ISAC** | Explains "why **consensus is currently limited** around the target dates"; "the period 2030-2031 represents a key milestone, when algorithms like RSA-2048 will be deprecated". [PDF](https://www.fsisac.com/hubfs/Knowledge/PQC/PQC%20Timelines.pdf?hsLang=en) | date not found | partial (grep) |
| **Europol QSFF** | Threat "expected to be available within the next 10 to 15 years, though this timeline could accelerate" (Introduction, p.4). **Disconfirming:** "There is no need for additional legislation" (Recommendation 3). [PDF](https://europol.europa.eu/cms/sites/default/files/documents/Quantum-safe-financial-forum-2025.pdf) | 2025-02-07 | partial (grep) |
| **BIS Project Leap Phase 2** | Bank of Italy, Bank of France, Bundesbank, Nexi-Colt and Swift tested PQC signatures in a live payment system. The report cites Gidney: "under a week by a quantum computer with fewer than a million noisy qubits (Gidney (2025))". It also quotes the Hudson estimate that a Fedwire attack means "USD 2 and USD 3.3 trillion" GDP at risk. [Page](https://www.bis.org/publ/othp107.htm), [PDF](https://www.bis.org/publications/project-leap-phase-2-quantum-proofing-payment-systems.pdf) | 2025-12-11 | page full; PDF partial (grep) |
| **US Treasury** | Quantum-Readiness Task Force, with three workstreams that include "**Digital Assets and Emerging Technology Risk**". [Release](https://home.treasury.gov/news/press-releases/sb0615) | 2026-08-24 | full |
| **Insurers: Aon + Moody's** | "The cyber re/insurance market is, to our knowledge, yet to meaningfully comprehend this source of risk… generating a potential '**silent quantum**' exposure, yet to be assessed, priced, or otherwise risk-managed" (Foreword). "the first insurers that explicitly exclude attacks from quantum machines would be sure to begin a market debate" (Conclusion). [PDF](https://www.moodys.com/web/en/us/site-assets/demystifying_quantum-risk.pdf) | Aug 2026 | full |
| **OSFI (Canada)** | "These guidelines generally recommend achieving quantum readiness across all systems by 2035." "rapid progress towards error-corrected quantum processors… have amplified the risk." These are best practices, not an OSFI deadline. [Bulletin](https://www.osfi-bsif.gc.ca/en/risks/technology-cyber-risk-management/technology-risk-bulletin/quantum-readiness-phases-timelines) | dated Mar 2026; issued 2026-07-03; mod. 2026-10-19 | partial (grep) |
| **NIST IR 8547 (ipd)** | Table: RSA, ECDSA, EdDSA and ECDH are "**Deprecated** after 2030" at 112-bit security and "**Disallowed** after 2035". [PDF](https://nvlpubs.nist.gov/nistpubs/ir/2024/NIST.IR.8547.ipd.pdf). This is the initial public draft; I did not check whether a final version exists. | 2024-11 | partial (grep §4) |
| **EO 14412 / OMB M-26-15** | High-value assets: PQC key establishment by **2030-12-31**, signatures by **2031-12-31**; FAR rule binds contractors by 2030-12-31. Source: `docs/research/pqc-migration.md:20-21`, read in full in an earlier session. | 2026-06-22 | full (prior session) |
| **NSA CNSA 2.0** | New NSS acquisitions compliant from **2027-01-01**; all NSS quantum-resistant by 2035. Taken from Aon-Moody's p.11 and Keyfactor because the NSA PDF was unreadable (403 earlier; this session's grep returned nothing). | 2024-12 FAQ | secondary only |
| **Google (deadline-setter)** | "We're setting a timeline for post-quantum cryptography migration to 2029… in light of progress on… **quantum factoring resource estimates**." [Blog](https://blog.google/innovation-and-ai/technology/safety-security/cryptography-migration-timeline/) | 2026-03-25 | full |
| **GAO, report to Congress** | "development estimates vary widely due to several factors, such as uncertainty in the rate of growth for qubits and how many qubits will be needed". It anchors on the GRI **Dec 2024** survey and a RAND 2023 figure of "10 million physical qubits" (footnote 26). [GAO-27-108740](https://files.gao.gov/reports/GAO-27-108740/index.html) | 2026-10-06 (rev. 10-14) | partial (grep) |

---

## 2. How often estimates appeared in 2025–2026, and how far they moved

| Date | Claim | What is counted | Source (read depth) |
|---|---|---|---|
| 2025-05-21 | RSA-2048 "in less than a week by a quantum computer with less than a million noisy qubits"; Google's blog calls it "a **20-fold decrease** in the number of qubits" from 20M (2019) | physical qubits; runtime grew from 8 h to under a week | [arXiv 2505.15917](https://arxiv.org/abs/2505.15917) abstract full; [Google blog](https://security.googleblog.com/2025/05/tracking-cost-of-quantum-factori.html) full |
| ~2026-02/03 | Iceberg "Pinnacle": ~100,000 qubits for RSA-2048 | physical, qLDPC | via [Ivezic](https://postquantum.com/post-quantum/pinnacle-architecture-break-rsa-2048-critical) — snippet only |
| 2026-03-30 | ECDLP-256 with "<1200 logical qubits and <90 million Toffoli gates"; "minutes using fewer than half a million physical qubits" | logical and physical, full attack, ZK-attested | [arXiv 2603.28846](https://arxiv.org/abs/2603.28846) abstract full |
| 2026-03-30 | "as few as 10,000 reconfigurable atomic qubits"; P-256 "a few days for a system with 26,000 physical qubits" | physical, neutral atoms | [arXiv 2603.28627](https://arxiv.org/abs/2603.28627) abstract full |
| 2026-06 | Schrottenloher's open reproduction (~1,192 / 1,446 logical) | logical | via [Ivezic](https://postquantum.com/post-quantum/quantum-attack-ecc-circuit-floor/) full; repo cites 2606.02235 |
| 2026-05 → 07-26 | ECDSA.Fail: "Participants reduced S by **86.1%**", from 10.75B to 1.496B (Q=1,151, T=1,299,453). "Over approximately **eight weeks**, more than one hundred participants… produced over four hundred promoted submissions." Later 1.259B and 813 qubits. | Q×T for **one point addition**; average executed Toffolis. Baseline is the challenge's own start circuit, not Google's | [arXiv 2609.09582v2](https://arxiv.org/abs/2609.09582v2) abstract full plus grep of §1, §3, §5 |
| 2026-09-04 | IonQ: "about 1450 qubits and 40·10⁶ Toffoli"; "25.7 days using 19,397 physical qubits with an estimated success probability of 63%" | logical, physical and success probability, full attack | [arXiv 2609.05625](https://arxiv.org/abs/2609.05625) abstract full |
| 2026-09/10 | Jo & Lee ePrint 2026/2014; Gu 2610.22367; a 893-qubit low-width circuit (2026-10-13) | various | `docs/research/resource-claims-verification.md:31`, `ranked-memo.md:46` |

**Count:** at least 9 distinct public estimate events between March and October 2026, plus a leaderboard that updates daily. The existing repo counted "at least 7 ECC-cost papers in 7 months"; the extra events counted here are the Cain RSA/P-256 paper and the Iceberg RSA estimate.

**Headline drift you can show on stage:**
- **Rounding.** Google's own blog rounds "less than a million… less than a week" to "1 million noisy qubits running for one week". Aon-Moody's then repeats "one million qubits running for a week" (p.6).
- **Unscoped headline.** Stratsec's subtitle says "The estimated resources to break RSA and ECC have dropped tenfold in four months" without saying which quantity ([2026-05-01](https://intelligence.stratsec.com/p/the-quantum-threat-to-your-cryptography), subtitle only).
- **Authors' own caveat.** ECDSA.Fail: "differing interfaces, accounting conventions, and validation scope preclude formal dominance."
- **Ivezic** ([2026-06-23](https://postquantum.com/post-quantum/quantum-attack-ecc-circuit-floor/), full): "Anyone reading the leaderboard as a simple qubit countdown is missing that contestants can move in either direction on the qubit axis" and "A 500-qubit circuit is the same attack as an 1,100-qubit one, folded into a narrower and longer shape."
- **Institutions lag** [INFERENCE from citations]. The August 2026 Aon-Moody's paper cites only the GRI 2024 survey and Gidney 2025. The October 2026 GAO report anchors on the December 2024 survey. GRI/evolutionQ issued an out-of-cycle June 2026 briefing calling the Cain and Babbush papers "bombshells" (quoting Aaronson) ([PDF](https://globalriskinstitute.org/mp-files/pdf-quantum-briefing-recent-quantum-computing-progress-and-implications-for-cybersecurity.pdf), pp.1–5).

**Disconfirming:** Ivezic argues the algorithm curve is "flattening as it nears its floor… The uncertainty in Q-Day for ECC now sits almost entirely on the other curve" (hardware).

---

## 3. Market size signals and comparable companies

| Signal | Figure (verbatim where possible) | Source, date, depth |
|---|---|---|
| PQC market | "USD 0.42 billion in 2025 to USD 2.84 billion by 2030… CAGR of 46.2%"; "BFSI segment will account for the largest market share" | [MarketsandMarkets PR](https://www.prnewswire.com/news-releases/post-quantum-cryptography-pqc-market-worth-2-84-billion-by-2030--marketsandmarkets-302572135.html), 2025-10-01, partial. This is a vendor-marketing grade source; treat as directional. |
| Advisory / assessment spend | Assessment-and-planning services "expected to reach US$255 million globally by the end of the year"; point solutions "CAGR of 63%" | [ABI Research](https://www.abiresearch.com/press/new-algorithmic-standards-and-migration-policy-timelines-propel-post-quantum-cryptography-toward-billion-dollar-market-by-2030), 2025-04-29, full |
| US federal migration cost | "approximately $7.1 billion" to migrate priority systems (ONCD/OMB) | GAO footnote 63, partial |
| **Project Eleven** (closest comparable) | $6M seed at $30M post (June 2025), then $20M Series A at **$120M post** (2026-01-14), led by Castle Island with Coinbase Ventures participating. "recognized revenue through grants"; aims to be a "'Palantir' for digital asset migrations" | [The Block](https://www.theblock.co/post/385583/project-eleven-series-a-funding-crypto-quantum-threats), full |
| SandboxAQ | Series E "over $450 million"; "raised over $950 million" since 2022 | [Release](https://www.sandboxaq.com/press/sandboxaq-closes-450m-series-e-round-with-expanded-investor-base), 2025-04-04, full. The ">$5.6B valuation" figure is a search-result title only. |
| Keyfactor | $100M+ ARR, ~$1.3B valuation; acquired InfoSec Global (Toronto) | `pqc-migration.md:42`, full in a prior session |
| QuSecure | Series A totals $28M (Two Bear, Accenture) | 2025-02, snippet only |
| evolutionQ (Waterloo) | US$5.5M Series A (Quantonation). Sells "Quantum Risk Assessment", "Executive Workshop", "Roadmap & Strategy" services; authors GRI's threat reports | [Release](https://www.evolutionq.com/news-releases/evolutionq-seriesa-funding-announcement) (2022), full |
| Paid quantum intelligence | TQI datasets "$2,999 named-user / $5,999 corporate"; GQI annual membership, price undisclosed | `competitors-intelplatforms.md:12,23` |
| Vendor "Quantum Threat Intelligence Reports" | QNu Labs and enQase publish BFSI reports as lead generation ("Book a 30-Minute Quantum Readiness Assessment") | snippet only |
| A dedicated "quantum risk intelligence subscription" with claim verification | **not found** | searched 2026-10-23 |

---

## 4. Georgian and the judges

| Who | What I found (verbatim) | Source, date, depth | What they will probe [INFERENCE] |
|---|---|---|---|
| **Georgian (firm)** | "investing in market-leading B2B software companies across the AI technology stack"; "Six deals a year"; "Initial investments targeting $25M+"; AUM "$5.8B". Portfolio filters include Cybersecurity, Financial Services and Insurance, and **Quantum Computing**. Cyber companies include Cyera, Island and Sublime Security. | [georgian.io](https://georgian.io/), [portfolio](https://georgian.io/portfolio), full | A growth-stage firm; the prize is an "investor pitch session + warm fund intro" to an early-stage fund ([Luma](https://luma.com/build-north), full). Pitch a path to a company, not traction. |
| **Georgian house view** (Ben Wilde, not a judge) | "verifiability is what turns comfort from a feeling into evidence"; "the trust layer becomes a product surface. That could include… **domain-specific evals**… insurance"; "learn faster by verifying faster" | [Trust Becomes the Moat](https://georgian.io/posts/trust-becomes-the-moat), 2026-05-13, full | Present the Ledger as a domain-specific verifier. |
| **Margaret Wu** (Partner / Lead Investor) | Has led Supabase, Dominion Dynamics, You.com, Darrow, Ambience, Oyster, Tenstorrent, Generalist and Replit. Waterloo Chemistry/Business grad. Spoke at **IQT Vancouver 2024** (a quantum conference) on VC in quantum. "we look for companies that have a differentiated wedge that gives them defensibility"; buyers should "look out for security posturing in the product". Dominion memo praises "demonstrating technical capability directly to operators before pursuing contracts, earning trust incrementally". | [bio](https://georgian.io/team/margaret-wu) full; [IQT](https://www.insidequantumtechnology.com/news-archive/margaret-wu-lead-investigator-at-georgian-is-an-iqt-vancouver-pacific-rim-2024-speaker) full; [Unleash](https://www.unleash.ai/hr-technology/vc-voices-hr-should-look-for-platforms-that-can-grow-with-their-organizations-says-georgians-margaret-wu) partial (metadata dated 2026-05-20); [Dominion memo](https://georgian.io/posts/why-georgian-invested-in-dominion-dynamics-again) partial, 2026-06-30 | Wedge, defensibility against Ivezic and Eigen, first operator-user. A Canadian sovereignty angle via OSFI and the Waterloo hub may land. |
| **Madalin Mihailescu** (CTO, AI Lab) | "focuses on supporting Georgian's portfolio companies to bring AI products to market"; PhD in distributed data storage and analytics | [bio](https://georgian.io/team/madalin-mihailescu), full. No public statement on verification found this session. | Architecture: what the LLM does versus the deterministic checker; data model; evals. |
| **Julien Coupez** (Google CE for Startups) | "I help startups succeed by providing hands-on technical guidance… cloud architecture, AI/ML, implementation, and optimization"; former founder and CTO of Nexboo | LinkedIn and Luma, snippet only | Tech & Deployment. Google is also the source of the key estimates; its blog says it is "important the size and performance of a future quantum computer… is carefully characterized". |
| **Deval Pandya** (CEO Autoinference, ex-VP AI Eng Vector) | "Independent, objective evaluation of this kind is vital to understanding how models perform in terms of accuracy, reliability, and fairness" ([Vector](https://vectorinstitute.ai/vector-institute-unveils-comprehensive-evaluation-of-leading-ai-models), 2025-04-10, full). MLOps "is the bridge from [Trustworthy AI] principles to practice"; "One key additional part for MLOps is continuous monitoring and testing" ([Vector/CIBC](https://vectorinstitute.ai/cibc-analytics-day-recap-understanding-and-operationalizing-trustworthy-ai), 2022-06-01, partial). Talk: "Responsible and Trustworthy AI – from Principles to Practice" (WASP 2023, full). | as cited | A measured extractor eval (span-match rate, field precision on labelled cards) and continuous re-checking as new claims arrive. |

---

## 5. Five pitch lines

1. **"A $74-billion Bitcoin ETF warns that quantum computing 'could result in such cryptography becoming ineffective' — and gives investors no number to watch."** Source: IBIT prospectus p.24; NAV $74.2B at 2025-06-27, p.20.
2. **"The estimates move too fast to follow: an open leaderboard cut its headline cost 86% in about eight weeks, and Google cut RSA-2048's qubit estimate 20× in 2025."** Sources: ECDSA.Fail arXiv 2609.09582v2; Google Security Blog 2025-05-23.
3. **"The numbers don't measure the same thing: 1,151 logical qubits for one step, 19,397 physical qubits for 26 days, 26,000 atoms for 'a few days', under 500,000 physical qubits for 'minutes'. The authors say their conventions 'preclude formal dominance.'"** Sources: arXiv 2609.09582, 2609.05625, 2603.28627, 2603.28846.
4. **"Banks are asking for this tool: 73% of Hong Kong banks lack 'models, tools, or industry-standard frameworks to systematically quantify' quantum risk, and their regulator tells them to 'monitor these breakthroughs and adjust their timelines.'"** Source: HKMA/KPMG, July 2026.
5. **"Money is already moving on these claims. Google pulled its migration deadline forward to 2029, citing resource estimates. Coinbase, custodian of about 12% of all BTC, set up a board to 'respond in real time'. Aon and Moody's warn of 'silent quantum' insurance exposure. Project Eleven raised at $120M."** Sources: Google blog 2026-03-25; Coinbase 2026-01-21 and CoinDesk 2026-10-14; Aon-Moody's Aug 2026; The Block 2026-01-14.

*Optional closer for Georgian, using their own words:* "Georgian wrote that 'verifiability is what turns comfort from a feeling into evidence.' We built that verifier for the one risk every bank now has to plan for."

---

## 6. Investor objections and answers

| Objection | Best evidence-based answer | Residual risk (be honest) |
|---|---|---|
| **"It's niche: who cares about qubit counts?"** | The holders of crypto and bank risk do. Coinbase's board has a real-time breakthrough-response mandate. IBIT carries a long quantum risk factor. Treasury's task force has a digital-assets workstream. Insurers face unpriced "silent quantum" exposure. 73% of HK banks lack quantification tools. The ECC wedge is narrow on purpose, and the same card schema covers RSA and hardware claims. | Seyffart: ETF disclosures are "completely standard" boilerplate. Do not claim BlackRock is a buyer. |
| **"Who pays?"** | Money is already spent on this analysis: ABI puts assessment and planning services at $255M (2025); TQI sells datasets at $3–6k; evolutionQ and Applied Quantum sell risk-assessment services; Project Eleven earns grant revenue at a $120M valuation. Sequence: a free public ledger (credibility), then paid alerts, an API, and "evidence packs" for board and regulator memos sold to custodians, insurers' cyber-analytics teams and PQC consultancies. [INFERENCE] | No committed buyer (`ranked-memo.md:38`). Validate with 3–5 outreach replies before Demo Day. |
| **"Why not Ivezic?"** | He is the benchmark human analyst, and his own warning ("simple qubit countdown… is missing…") is the Ledger's comparability rule. His output is copyrighted prose, written by hand for each article (he read submission notes to find 111/360,960 failures). The Ledger makes that analysis reproducible, cited, machine-readable and continuously re-checked. Position him as a user, partner or distribution channel. | He could productise this (he already has a CRQC Scorecard and a Q-Day Estimator). |
| **"Why not Eigen / ECDSA.Fail?"** | Eigen ranks one number (Q×T) for one primitive on the supply side, and it rejected the 893-qubit Pareto point as "score did not improve current best" (`resource-claims-verification.md:11`). Its paper admits its figures do not compare formally with Google's or Schrottenloher's. The Ledger works across sources, for the people who use the numbers rather than produce them, and refuses to compare unlike quantities. It complements the leaderboard rather than replacing it. | HashSmash plans machine-readable claim sheets ("Exact harness TBD"). Eigen is the most likely builder of a competitor. |
| **"Timing is irrelevant — just migrate now."** (Coinbase board) | Sequencing and pricing still depend on timing. Google moved its own deadline because of resource estimates. HKMA tells banks to "adjust their timelines". Babbush's fast-clock versus slow-clock distinction changes which Bitcoin outputs (on-spend versus at-rest) need priority. Insurers must decide on exclusions. Ivezic calls the paper "surprisingly vague" on numbers. | Partly true for enterprises with 2030–2035 mandates. Lead with crypto custody and insurers, where timing drives money. |
| **"Estimates are converging on a floor, so the problem disappears."** | Ivezic says the uncertainty moves to hardware. The same card schema then applies to hardware claims (e.g. "about 96" verified logical qubits by QuEra, per Ivezic). Even near the floor, a 500-qubit and an 1,100-qubit circuit are "the same attack", which shows layer gates still matter. | Paper cadence for ECC may slow after 2026. |
| **"An LLM in a trust product will hallucinate."** | The LLM only proposes fields. Deterministic code checks each verbatim span and does the arithmetic, a "refuse to compare" gate blocks mismatched quantities, and a human reviews. This matches Pandya's "continuous monitoring and testing" and Georgian's "verifiability". Show a measured span-match rate. | It needs a real labelled eval, even a small one (6–10 examples per `ranked-memo.md:50`). |
| **"Market too small for venture scale."** | PQC: $0.42B to $2.84B by 2030 (M&M), BFSI the largest segment. Project Eleven reached a $120M valuation on digital-asset quantum readiness alone. The Ledger is the intelligence layer on top of migration spend. [INFERENCE] | Analyst market reports are low-quality evidence. A Georgian-scale ($25M+) company would need to expand into wider quantum and AI-claim verification. |
| **"Dual use: does it help attackers?"** | It indexes only published numbers. It runs no circuit optimisation and does not model physical resources (`ranked-memo.md:48`). | Cite and license sources carefully (arXiv CC BY 4.0). |

---

## 7. Recommended 20-second problem statement

> "Every few weeks a new paper says breaking Bitcoin or RSA takes fewer qubits: one million, 26,000, 1,151, 893. Banks, custodians and insurers are told to 'monitor these breakthroughs and adjust their timelines.' But those numbers count different things: logical versus physical, one step versus the whole attack. Q-Day Ledger turns each claim into a cited card and refuses to compare unlike numbers."

That is about 60 words, roughly 20–22 seconds spoken. What the four figures are:

| Figure | What it measures | Source |
|---|---|---|
| 1 million | physical qubits, RSA | Gidney 2025 |
| 26,000 | physical qubits, P-256 | Cain 2026 |
| 1,151 | logical qubits, one point addition | ECDSA.Fail |
| 893 | logical qubits, low-width point addition | 2026-10-13 claim |

---

## Files and sources (read depth)

- `docs/decision/ranked-memo.md` — risks, data and licensing, cost, demo (lines 3, 30, 38, 44–50).
- `docs/research/resource-claims-verification.md` — personas, frequency count, Eigen and Ivezic evidence (lines 9–31, 56–80).
- `docs/research/pqc-migration.md` — EO 14412, OMB, OSFI, Keyfactor, evolutionQ (lines 7–47).
- `docs/research/competitors-intelplatforms.md` — TQI and GQI pricing (lines 11–23).
- Not readable this session: NSA CNSA 2.0 PDF (no grep hits), the Morgan Stanley S-1 and the IBIT POSAM on SEC.gov (no grep hits), the SandboxAQ valuation page (404), and Julien Coupez's posts (LinkedIn snippet only).