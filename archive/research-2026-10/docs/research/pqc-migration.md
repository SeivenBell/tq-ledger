# Can an AI agent that finds quantum-vulnerable cryptography in code win users now?

Ticket #9 · slug `pqc-migration` · researched 2026-10-22

## 1. Bottom line

- **No, not as Severyn's top pick. It works as a B2B fallback only if the scope is narrow.** The deadlines are real and dated: CNSA 2.0 applies to new NSS acquisitions from 2027-01-01, EO 14412 sets 2030 for key establishment and 2031 for signatures, Canada's GC requires high-priority systems by end of 2031, and OSFI wants readiness across all systems by 2035. Buyers are already sending vendors questionnaires. But "find quantum-vulnerable crypto in code" is a commodity. IBM, Keyfactor, SandboxAQ, Sectigo, Arqit and others sell it, and at least 10 open-source scanners exist. Most have 0 to 21 GitHub stars, which suggests weak bottom-up pull from developers.
- **Discovery is not the bottleneck.** DigiCert's May 2026 survey (n=1,001) found that only 3% of organisations name "where to start" as their top barrier. Legacy complexity (26%), performance (19%) and budget (19%) lead. Marin Ivezic, a practitioner, estimates that AI-compressible technical work is about 15–20% of programme effort. Calendar time goes to governance, access, vendors and change control.
- **Where AI clearly adds value over static scanners:** (a) triaging findings by context, for example MD5 in a UUID versus MD5 in a password hasher; (b) drafting migration patches; (c) turning scan evidence into the answers buyers ask for. Static rules cannot do (c).
- **The underserved spot:** a 10–200-person B2B software vendor that receives a PQC vendor questionnaire and has "nothing to hand them" (IDC, 2026-09-08). Fewer than 10% of vendors can produce evidence. AusCERT's questionnaire tells buyers to "halt new contract expansions" with red-scored vendors. **Best wedge: a PQC evidence pack (W2).**
- **Credibility cost:** PQC is classical cryptography engineering. It earns little credibility in quantum and plays only partly to Severyn's MSc in quantum information. Verifying agent-written migrations (W1/W3) fits his "verification and open benchmarks" brand better, but its user evidence is weaker.
- **Risk is low.** The work is defensive, and there is no overlap with TopQAD unless the project adds Shor resource estimates ("when does RSA break"). Avoid that.

## 2. The pain

**Who must migrate, and by when (observed, primary sources):**

| Who | Obligation | Source (date, read depth) |
|---|---|---|
| US federal agencies | Agencies name a PQC lead within 30 days. HVAs and high-impact systems move to PQC key establishment by **2030-12-31** and to PQC signatures by **2031-12-31**. The FAR rule requires covered **contractors** to comply with PQC FIPS by 2030-12-31. CISA publishes **CBOM minimum elements within 270 days** (about March 2027). | EO 14412, 2026-06-22, **full** |
| US federal agencies | Migration plans due within 120 days (about October 2026), in 5 phases: discovery 2026–27, pilots 2027–28, key establishment 2028–30, signatures 2031, everything 2035. Plans must list "the methodologies and automated tools used for the cryptographic inventory". SAST, SCA and network scanning should feed a central CBOM. | OMB M-26-15, 2026-06-24, **partial** (pp. 2–11; p. 1 not extracted) |
| Vendors to US National Security Systems | New NSS acquisitions must be CNSA 2.0-compliant from **2027-01-01**. Equipment that cannot comply is phased out by 2030-12-31. Software and firmware signing uses LMS/XMSS. | Keyfactor blog, 2026-09-23, **full** (secondary: the NSA FAQ v2.2 PDF returned HTTP 403) |
| Government of Canada departments | Initial departmental plan by **April 2026**, annual reporting after that, high-priority systems by **end of 2031**, all systems by **end of 2035**. The inventory must list per system: components, vendor and version, cryptographic configuration, dependencies, contracts, and refresh year. "Software tools… will be necessary", including source-code scanning. | Cyber Centre ITSM.40.001, 2025-06-23, **full** |
| Canadian federally regulated financial institutions | OSFI best practices: centralised inventory including third-party dependencies, vendor assessment, then "test and validate whether migrated functions perform as intended". Readiness across all systems by 2035. | OSFI bulletin, March 2026 (modified 2026-07-13), **full** |
| Vendors to Australian buyers | A 10-question vendor PQC questionnaire with points. Q2: "Can you provide a comprehensive CBOM?" A red score means "halt new contract expansions". | AusCERT Vendor PQC Questionnaire v1.0, 2026-08, **full** |

**How often, and what it costs:**
- DigiCert's Quantum Readiness Outlook (fielded May 2026, n=1,001 in the US, UK and AU): 87% are planning, testing or implementing PQC. Only 7% have quantum-safe or hybrid certificates on more than half their estate. 44% have a cryptographic inventory. Top barriers are legacy complexity 26%, performance 19%, budget 19%, skills 10%. "Where to start" is 3%. Source: postquantum.com summary, 2026-08-02, **full**. The primary PDF redirected and could not be read, so treat as secondary.
- IDC (Philip Harris, Research Director GRC, 2026-09-08, **full**): "No TPRM platform has deployed a production-ready quantum encryption readiness module as of May 2026." "Fewer than 10% of vendors will produce documentary evidence for most of the 48 assessment questions." Buyers "are already filling this void through ad hoc custom questionnaire additions." The vendor's moment of pain: "a customer asks, and there's nothing to hand them." The 10% figure is the author's interpretation; IDC does not publish the method in the free post.
- Ivezic, founder of Applied Quantum and a former Fortune Global 500 CISO (2026-07-16, **full**): a large enterprise migration takes 12–15 years and about 120,000 tasks. Testing takes 25–40% of budget. AI-compressible technical work is "perhaps 15 to 20 percent" of effort. He labels these proportions illustrative, not benchmarks. This is the strongest disconfirming evidence for "an AI agent compresses migration".
- Carleton (Oladoja and Tanev, ETSI/IQC conference in Ottawa, April 2026, **full**): PQC guidance is "fragmented, high-level, and primarily designed for gov departments and large enterprises". The missing piece for SMEs "is the lack of an SME-executable migration path." This is direct Canadian evidence of the SME gap.
- Developer-level pain: in golang-jwt/jwt issue #508 (opened 2026-05-07, **partial**), a user asks for ML-DSA signing because "organizations subject to CNSA 2.0 timelines… need to understand whether PQC support will come from this library or if they should implement `jwt.SigningMethod` themselves." The maintainer is willing, but holds a strict zero-dependency rule and waits for Go's `crypto/mldsa`. **Implication [INFERENCE]:** many application-level signature migrations are blocked on library and standards support (RFC 9964 for JOSE), not on finding the code.
- Library readiness: pyca/cryptography **48.0.0 (2026-05-04)** made ML-KEM and ML-DSA available in standard wheels when built with OpenSSL ≥3.5. 49.0.0 (June 2026) added X.509 with ML-DSA keys. Source: CHANGELOG.rst, **partial** (PQC entries). Python migrations are therefore technically feasible today.

**What they do today:** enterprises buy discovery platforms (Keyfactor AgileSec, IBM Quantum Safe, SandboxAQ AQtive Guard, Sectigo Quantum Ready) or hire consultancies (evolutionQ, Applied Quantum). SMEs and vendors answer questionnaires by hand. Per IDC, they mostly cannot produce evidence.

## 3. Existing solutions

| Product / tool | What it does | Users / owner | Price / license | Read depth |
|---|---|---|---|---|
| IBM Quantum Safe Explorer (in Guardium Quantum Safe) | Source scan for Java, C/C++, C#, Python, Go, Kotlin, Dart and JS/TS. Outputs CBOM, CSV and JSON. Traces variables. Supports remediate-and-rescan. Detects existing ML-KEM/ML-DSA usage. Has an IDE plug-in, CLI and API. | IBM's CIO Office, enterprises | Commercial, price not public | Docs overview, updated 2026-09-25, **full** |
| Keyfactor AgileSec (acquired InfoSec Global, a Toronto company, and CipherInsights on 2025-05-13) | Discovery across code, binaries, file systems, cloud and network. AgileSec Agility swaps algorithms "without modifying source code". | Enterprise. Keyfactor: $100M+ ARR, about $1.3B valuation | Commercial | Press release 2025-05-13, **full** |
| SandboxAQ AQtive Guard | Cryptographic inventory, compliance analysis, remediation through Jira and GitHub | Enterprise, federal | Custom pricing | **snippet-only** |
| Sectigo Quantum Ready (QSPM) | CBOM, prioritisation by business criticality, linked to certificate lifecycle management | Enterprise, early access since 2026-09-17 | Commercial | Press release, **full** |
| Arqit Encryption Intelligence, IBM Guardium Cryptography Manager ("AI-powered"), QuantumGenie ("AI-native"), Cyberify QuantumReady ("AI-powered" for banks), AppViewX | Discovery, posture management, remediation | Enterprise | Commercial | **snippet-only** (2025-10 to 2026-10) |
| evolutionQ (Waterloo; Mosca, Jao) | Symmetric key infrastructure (BasejumpSKI), quantum key distribution networks (BasejumpQDN), and risk/roadmap **services**. **No code scanner.** | Telecom, finance | Commercial | Homepage, **full** |
| PQCA CBOMkit + sonar-cryptography (IBM-donated) | SonarQube plugin covering Java (JCA, BouncyCastle), Python (pyca) and Go stdlib. Outputs a CycloneDX 1.6 CBOM. Includes a viewer and an OPA "quantum_safe" policy. | Linux Foundation PQCA | Apache-2.0. Last commits 2026-10-13 (cbomkit, 155★) and 2026-10-08 (sonar-cryptography, 92★) | README, **partial** |
| anvilsecure/pqcscan | Scans SSH/TLS servers for PQC support and analyses PCAPs | OSS | BSD-2-Clause, 127★, last commit 2026-09-06 | Description only, **snippet-only** |
| sachhg/pqc-scan | Tree-sitter scanner, GitHub Action, SARIF and CBOM output, baselines, "explain" migration examples | OSS | MIT, 3★, last commit 2026-09-11 | README, **partial** |
| postquantdev/postquant | TLS letter grade plus code scanner, context-aware risk adjustment ("uuid MD5 → A, Django MD5 → D+") | OSS | MIT, 0★, last commit 2026-03-05 | README, **partial** |
| Other OSS (csnp/cryptoscan 21★, quantakrypto/pqc-tools 15★, Santander cryptobom-forge 41★ GPL-3.0, pqc-semgrep-rules 0★, qscan 1★, crypto-scanner 6★, quantumguard 0★, pqc-migration-audit 2★) | Pattern or AST scanners | OSS | Various; GitHub metadata pulled 2026-10-22 | Repo metadata only |
| Quantum-Safe Code Auditor (arXiv 2604.00560) | Regex, then Claude enrichment, then a 2-qubit "VQE threat score". Precision 71.98% on 602 labelled findings. Recall of 100% holds "structurally" only for regex matches. | Research | OSS | 2026-04-01, **partial** (§1–4, 6–7) |
| "Can Coding Agents Migrate to PQC?" (arXiv 2512.12989v3) | Go file-signer RSA→ML-DSA-44 task with an OpenSSL interoperability checker. 12 agent patches passed local sign/verify but **failed external checks**. Checker access did not raise success. Claude Code and Codex passed 4 of 4 trials. | SDAIA research. Code: aalquwayfili/pqc-migration, Apache-2.0, last commit 2026-10-11 | OSS | 2026-09-20, **partial** (§I–VII, Tables I–III) |
| LLM fragment migration (arXiv 2606.07341) | Fine-tuned GPT-4.1-mini reaches 92.5% functional correctness on 800 synthetic Python pairs. Weaker on real multi-module repos. | Research | — | Abstract, **snippet-only** |
| Chai (arXiv 2606.26933, Popa lab) | Agentic differential testing found 100+ crypto-misuse vulnerabilities in X.509, JWT and SAML libraries | Research | — | Abstract, **snippet-only** |

## 4. The gap

1. **Evidence, not detection.** Detection is solved well enough by free tools (CBOMkit, IBM). What buyers want is a vendor-signed answer backed by evidence: which algorithms, where (file:line, endpoint), what plan, by when. IDC says no TPRM module exists (as of May 2026). Sectigo, Keyfactor and IBM sell to the enterprise that runs the questionnaire, not to the small vendor answering it. I found no evidence that Vanta, Drata or Secureframe has a PQC module. That comes from one search with no hits, so it is not proven absent.
2. **Verified migration.** Agents can write ML-DSA code, but a local round trip hides interoperability bugs: wrong key encoding, missing PKCS#8/SPKI structures, wrong context string (2512.12989). No product reviewed ships an independent interoperability oracle with its AI patches. IBM's "verify by rescanning" checks that the vulnerable call is gone, not that the new code works.
3. **Why nobody has filled (1) for SMEs [INFERENCE]:** incumbents' contract sizes favour enterprises. OSS scanner authors stop at SARIF output. Questionnaire formats only appeared in July–September 2026 (ASD, AusCERT, IDC).
4. **Why AI cannot fill most of the gap:** questionnaire items on board approval, budget and HSM firmware are governance facts. An LLM drafting them invites false compliance claims, which is a Security and Ethics judging risk.

## 5. Candidate wedges

### W1. "Fix-and-Prove": PQC migration PRs with an independent interoperability verifier

- **User:** maintainers or backend engineers who own a Python service that signs tokens or files with RSA or ECDSA.
- **Job:** scan the repo, have Claude draft a migration to ML-DSA-65 (or hybrid ML-KEM) on pyca/cryptography ≥48, then **prove** it with an oracle that exchanges keys and signatures with the OpenSSL 3.5 CLI in both directions, checks context strings and reloads keys. Open a PR that includes a CBOM diff and a verification report.
- **2-minute demo:** a sample RS256 signer. The agent's first patch passes its own test. The verifier shows OpenSSL rejecting the key encoding. The agent repairs it. The PR turns green, and the CBOM shows RSA going from 1 to 0 and ML-DSA from 0 to 1.
- **Reuse:** sachhg/pqc-scan (MIT) or the CBOMkit rules (Apache-2.0). The checker design from aalquwayfili/pqc-migration (Apache-2.0, Go). pyca/cryptography (Apache-2.0 or BSD). OpenSSL 3.5.
- **Data and compute:** 2–3 seeded demo repos; a Docker image with OpenSSL ≥3.5. **LLM cost:** about $5–15 (each migration attempt is about 50–150k tokens on Sonnet-class models).
- **Prize fit:** Eon Era (agent testing). Clerk is not needed.
- **Main failure:** frontier agents already pass the simple case (Claude Code 2/2, Codex 2/2 in 2512.12989), so the verifier's value has to come from catching bugs in harder cases. Real JWT migrations are blocked on JOSE library support (golang-jwt #508), so few maintainers will merge in November 2026.

### W2 (best). "PQC Evidence Pack": questionnaire-ready quantum readiness for B2B software vendors

- **User:** CTO or security lead at a 10–200-person B2B SaaS that sells to banks, government or regulated buyers and has received a PQC questionnaire (AusCERT, ASD, or ad-hoc additions as IDC describes).
- **Job:** connect a GitHub repo and production domains. The tool runs (a) a code CBOM (CBOMkit or pqc-scan), (b) a TLS/SSH endpoint check (anvilsecure/pqcscan), and (c) a dependency check (does pyca/OpenSSL/Go support ML-KEM and ML-DSA at the pinned versions?). Then an LLM: triages findings by context (prod vs test, security vs checksum); drafts answers to the AusCERT 10 questions and IDC's five Tier-4 baseline questions, **each citing file:line or a handshake as evidence**; marks governance questions "needs human answer" instead of inventing them; and emits a dated roadmap mapped to EO 14412, CNSA 2.0, ITSM.40.001 and OSFI. Output is a CycloneDX 1.6 CBOM plus a PDF evidence pack.
- **2-minute demo:** paste a public repo (for example a Flask app using RSA JWT and TLS through nginx). Show the live scan, the triage that drops UUID-MD5 noise, the AusCERT score moving from red to amber, and the evidence links. One-click export.
- **Reuse:** cbomkit and sonar-cryptography (Apache-2.0, active), pqc-scan (MIT), anvilsecure/pqcscan (BSD-2-Clause), the CycloneDX spec (Apache-2.0). Hosting on Render. Clerk for auth (the Clerk prize). SurrealDB to store scans (the SurrealDB prize, though "agent memory" is a stretch).
- **Data and compute:** public repos only for the demo. No customer data needed. **LLM cost:** about $1–3 per repo scan for triage plus answer drafting; under $30 total for the build week.
- **Main failure:** buyers may not trust a tool-generated self-attestation. Enterprise incumbents or Vanta/Drata could add the same module. The questionnaire is mostly governance, so the evidence-backed technical part covers maybe 4 of AusCERT's 10 questions [INFERENCE: Q2, Q4, Q5 and Q10 are code/endpoint-observable].

### W3. "PQC-MigrateBench": an open benchmark of agent-written PQC migrations

- **User:** teams evaluating claims that "AI will do our PQC migration" (Ivezic's skeptics), and builders of coding agents.
- **Job:** extend 2512.12989 from 1 task to 4–5 (Python RS256 JWT → ML-DSA; RSA-OAEP → ML-KEM hybrid/HPKE; Go signer; TLS config → X25519MLKEM768), each with an independent-implementation oracle. Run Claude Code and 1–2 open models, then publish the results.
- **Demo:** a leaderboard and one failure trace in which a local test passes and the interoperability check fails.
- **Reuse:** aalquwayfili/pqc-migration (Apache-2.0), SWE-agent/mini-swe-agent (MIT, 8.8k★, last commit 2026-09-03), pyca, OpenSSL.
- **LLM cost:** $30–80 for a few runs per task.
- **Prize fit:** Eon Era (strong).
- **Main failure:** no user next week except researchers. Small n invites the same caveats as the paper.

## 6. Scores for the best wedge (W2, PQC Evidence Pack)

| Criterion | Score | Why |
|---|---|---|
| Real user with evidence of pain | 3 | Buyer-side questionnaires exist and threaten contracts (AusCERT, ASD, IDC: <10% of vendors can evidence), but no named vendor has been confirmed as a user yet. |
| AI makes a material difference | 3 | Context triage and evidence-to-answer drafting are genuinely LLM work. Detection is static, and governance answers must stay human. |
| Severyn's unfair advantage | 2 | Agent and verification harness skills and Waterloo/IQC credibility on threat timelines. No cryptography-engineering or GRC track record. |
| Buildable and demoable in 12 hours | 4 | Thin layer over mature OSS scanners plus Claude, on a single Render app. Risk is scanner setup time for SonarQube; use pqc-scan/CBOMkit-action instead. |
| Judge appeal (Georgian investors) | 4 | B2B, deadline-driven, unblocks revenue; comparables include Keyfactor ($1.3B) and two discovery acquisitions. Judges will ask "why not Sectigo or IBM?" |
| Adoption path after Oct 25 | 3 | A free repo scan plus a PDF is easy to try. Paying requires trust in the attestations; distribution through the Waterloo SaaS network is plausible but untested. |
| Competition density (5 = open field) | 2 | Enterprise discovery is crowded, and there are at least 10 OSS scanners. The SME vendor-evidence niche looks open but has not been verified for Vanta/Drata. |
| Credibility gain in AI and quantum | 2 | Reads as a security/compliance project. Quantum relevance is about the threat, not quantum computing skill. |
| Risk (5 = low: no dual use, no 1QBit overlap) | 4 | Defensive and no TopQAD overlap. The main ethical risk is overclaiming compliance; mitigate with evidence links and human-only governance fields. |

**Total: 27/45.**

## 7. Sources

| Source | Date | Read depth |
|---|---|---|
| EO 14412, Federal Register: https://www.federalregister.gov/documents/full_text/text/2026/06/25/2026-12909.txt | 2026-06-22 | full |
| OMB M-26-15: https://www.whitehouse.gov/wp-content/uploads/2026/06/M-26-15-Execution-of-the-Migration-to-Post-Quantum-Cryptography.pdf | 2026-06-24 | partial (pp. 2–11) |
| Cyber Centre ITSM.40.001: https://www.cyber.gc.ca/en/guidance/roadmap-migration-post-quantum-cryptography-government-canada-itsm40001 | 2025-06-23 | full |
| OSFI Quantum Readiness Phases and Timelines: https://www.osfi-bsif.gc.ca/en/risks/technology-cyber-risk-management/technology-risk-bulletin/quantum-readiness-phases-timelines | 2026-03 (mod. 2026-07-13) | full |
| NSA CNSA 2.0 FAQ v2.2: https://media.defense.gov/2022/Sep/07/2003071836/-1/-1/0/CSI_CNSA_2.0__FAQ_v2.2.PDF | 2026-10 | not readable (HTTP 403); dates taken from Keyfactor |
| Keyfactor, "PQ readiness for software vendors": https://www.keyfactor.com/blog/post-quantum-readiness-for-software-vendors-the-timeline-is-now-written-down/ | 2026-09-23 | full |
| Keyfactor acquires InfoSec Global and CipherInsights: https://www.keyfactor.com/press-releases/keyfactor-acquires-infosec-global-and-cipherinsights/ | 2025-05-13 | full |
| Ivezic, "How Much Can AI Help With PQC Migration?": https://postquantum.com/post-quantum/ai-pqc-migration-how-much-help/ | 2026-07-16 | full |
| DigiCert survey summary: https://postquantum.com/security-pqc/digicert-quantum-readiness-outlook-2026/ (primary PDF https://www.digicert.com/content/dam/digicert/pdfs/report/quantum-readiness-outlook.pdf redirected) | 2026-07-23 / 2026-08-02 | full (secondary) |
| IDC, "Quantum Risk Is Already Here": https://www.idc.com/resource-center/blog/quantum-risk-is-already-here-what-buyers-must-demand-and-vendors-must-build/ | 2026-09-08 | full |
| AusCERT Vendor PQC Questionnaire v1.0: https://auscert.org.au/wp-content/uploads/2026/08/Vendor-Post-Quantum-Cryptography-PQC-Assessment-Questionnaire-v1.0.pdf | 2026-08 | full |
| ASD, "Post-quantum questions to ask your vendors": https://www.cyber.gov.au/business-government/secure-design/quantum/post-quantum-questions-to-ask-your-vendors | 2026-07 | snippet-only (timed out) |
| Oladoja and Tanev (Carleton), SME PQC framework poster: https://www.etsi.org/wp-content/uploads/POSTER_CARLETON_Oladoja__Tanev.pdf | 2026-04 | full |
| Sectigo Quantum Ready launch: https://www.sectigo.com/resource-library/sectigo-introduces-sectigo-quantum-ready-qspm | 2026-09-17 | full |
| IBM Quantum Safe Explorer overview: https://www.ibm.com/docs/en/quantum-safe/quantum-safe-explorer/2.x?topic=quantum-safe-explorer-overview | 2026-09-25 | full |
| SandboxAQ AQtive Guard: https://www.sandboxaq.com/products | n/a | snippet-only |
| Arqit, Cyberify, QuantumGenie, AppViewX, IBM Guardium Cryptography Manager press items (via search) | 2025-10 to 2026-10 | snippet-only |
| evolutionQ homepage: https://www.evolutionq.com/ | ©2025 | full |
| qsafe.dev pricing (blockchain PQC scanner, $0/$19/$49 per month): https://qsafe.dev/pricing | undated | full |
| CycloneDX CBOM: https://cyclonedx.org/capabilities/cbom/ | undated | full |
| arXiv 2512.12989v3: https://arxiv.org/pdf/2512.12989v3 | 2026-09-20 | partial (§I–VII) |
| arXiv 2604.00560: https://arxiv.org/html/2604.00560v1 | 2026-04-01 | partial (§1–4, 6–7) |
| arXiv 2606.07341: https://arxiv.org/abs/2606.07341 | 2026-06-05 | snippet-only (abstract) |
| arXiv 2606.26933 (Chai): https://arxiv.org/abs/2606.26933 | 2026-06-25 | snippet-only (abstract) |
| golang-jwt/jwt #508: https://github.com/golang-jwt/jwt/issues/508 | 2026-05-07 to 06-22 | partial |
| pyca/cryptography CHANGELOG: https://raw.githubusercontent.com/pyca/cryptography/main/CHANGELOG.rst | v47 2026-04-24, v48 2026-05-04, v49 2026-06 | partial (PQC entries) |
| Schneier on pyca PQC (quoting Trail of Bits): https://www.schneier.com/blog/archives/2026/08/python-now-has-a-post-quantum-encryption-library.html | 2026-08-10 | full |
| Repos (license, ★, last commit via GitHub API on 2026-10-22): cbomkit/cbomkit (Apache-2.0, 155, 2026-10-13); cbomkit/sonar-cryptography (Apache-2.0, 92, 2026-10-08); cbomkit/cbomkit-theia (Apache-2.0, 46, 2026-09-30); cbomkit/cbomkit-action (Apache-2.0, 19, 2026-09-03); sachhg/pqc-scan (MIT, 3, 2026-09-11); postquantdev/postquant (MIT, 0, 2026-03-05); anvilsecure/pqcscan (BSD-2-Clause, 127, 2026-09-06); csnp/cryptoscan (Apache-2.0, 21, 2026-10-22); aalquwayfili/pqc-migration (Apache-2.0, 0, 2026-10-11); SWE-agent/mini-swe-agent (MIT, 8,759, 2026-09-03); pyca/cryptography (Apache-2.0 OR BSD, 7,819, 2026-10-22); cloudflare/circl (BSD-3-Clause per LICENSE, 1,731, 2026-09-28); open-quantum-safe/oqs-provider (MIT, 506, 2026-10-21) | 2026-10-22 | metadata; READMEs partial where cited above |

Stale flag: FIPS 203/204/205 (2024-08) are older than 18 months but still in force. The Keyfactor acquisition (2025-05) is 17 months old.

## 8. Open questions

1. **User test before building:** can Severyn name one Waterloo or Toronto B2B SaaS that has received a PQC questionnaire or CBOM request in 2026? If none turns up by Friday, W2's top score for "real user" falls to 2.
2. Do Vanta, Drata or Secureframe already ship (or plan) a PQC questionnaire module? Check their changelogs or ask a customer. If yes, W2's competition score falls to 1.
3. Will CISA's CBOM minimum elements (due about March 2027 under EO 14412 §5(d)) diverge from CycloneDX 1.6? W2 should stay format-agnostic.
4. For the synthesis memo: is a security/compliance project acceptable given criterion (2), credibility in **quantum**? If not, the area drops out regardless of user pain.
5. If W1 or W3 is preferred: are the interoperability failures in 2512.12989 still present for frontier agents on harder tasks (key encoding, hybrid KEM combiners)? A 1-hour spike with Claude Code on the Python JWT task would answer this before committing.
