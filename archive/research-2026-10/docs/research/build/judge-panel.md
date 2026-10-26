# Build North judge pressure-test: Q-Day Claim Ledger

## Summary

- **Round 1 is judged without you in the room.** On Oct 26 the judges score a video of at most 2 minutes, the Devpost page, the repo and the live link. Only the top 10 present live, on Oct 29 in Toronto (Luma event page, read in full). The video and the Devpost page are the pitch.
- **Margaret Wu's own investment memo describes this product's main feature.** Her You.com memo (2024-09-04) says Georgian "initially took notice of You.com based on the platform's ability to include verifiable data sourcing… often down to the exact line in the source webpage." She also wrote that Georgian's early "Pathfinder" checks include **Xanadu**, a quantum company. So she can follow a quantum pitch, but she will push on B2B traction. Her Replit memo says "This B2B traction is a key takeaway."
- **Georgian's 2026 house view also points at this product.** The firm's essay "Trust becomes the moat" (Ben Wilde, who is not a judge) says: "the trust layer becomes a product surface… domain-specific evals… Better verifiers create better feedback." Pitch the ledger as a domain-specific verifier. "Quantum tool" is the weaker framing.
- **Deval Pandya will grade the evaluation.** As Vector's VP of AI Engineering he said "Independent, objective evaluation… is vital", and he called continuous monitoring and testing the key addition MLOps makes. He sits on Canada's AI-safety bodies (CAISI Research Council, Safe and Secure AI Advisory Group). Show a held-out extraction score; he will not accept "the LLM is accurate" on trust.
- **Madalin Mihailescu's test is "valuable, not just unique."** In a 2019 podcast he said: "unique is great. Unique is not enough. It has to be valuable as well." He framed customer trust as one of Georgian's three thesis areas.
- **I found almost nothing on Julien Coupez.** I have only his LinkedIn headline (search snippet) and the Luma line "Former Founder & CTO @ Nexboo". Nexboo itself was not found. [INFERENCE] He will weigh Tech & Deployment: does the live link work, what does it cost, is it secure.
- **The partner prizes go to Georgian portfolio companies.** Georgian's portfolio page lists **Clerk** and **SurrealDB**, and its insights page features "Why Georgian Invested in **Eon**". [INFERENCE] A bolted-on integration will be easy for these judges to spot. Your memo already ranks Eon Era as the strongest fit; keep it honest.

## Sources and read depth

| Source | Date | Depth | What it gives |
|---|---|---|---|
| Luma, "Build North: Ship Something Real" (luma.com/build-north) | read 2026-10-23 | full | Criteria, submission, rounds, judges, partners |
| Devpost rules (build-north.devpost.com/rules) | read 2026-10-23 | full | Disclose AI tools; "faking your demo" banned |
| Devpost overview page | — | **not read (HTTP 403)** | Criteria taken from Luma instead |
| georgian.io/team/margaret-wu | read 2026-10-23 | full | Bio, deals |
| Margaret Wu, "Why Georgian Invested in You.com" | 2024-09-04 | full | Citation-to-exact-line thesis |
| Margaret Wu, "Why Georgian Invested in Supabase" | 2026-06-05 | full | Bottleneck shifts to deploying and securing |
| Margaret Wu, "…Replit (Again)" | 2026-03-11 | partial (grep: author, thesis bullets) | B2B traction, ARR, governance |
| Margaret Wu, "…Dominion Dynamics" | 2026-01-19 | partial (grep: thesis, Pathfinder line) | Xanadu is a Pathfinder deal; prototype-and-test |
| Margaret Wu, "…Dominion Dynamics (again)" | 2026-06-30 | full | Deploy to operators, earn trust step by step |
| IQT page announcing her Vancouver 2024 talk | 2024-03-06 | full | Shows quantum-event exposure. The talk content is the writer's guess, not her words |
| georgian.io/team/madalin-mihailescu | read 2026-10-23 | full | Leads the AI Lab |
| Modern CTO podcast #123 (transcript) | 2019-09-09 | full | His own words on trust, value, data quality |
| Ben Wilde (Georgian), "When Anyone Can Build Any Software, Trust Becomes the Moat" | 2026-05-13 | full | House thesis; **not by a judge** |
| Georgian + NewtonX, Applied AI Benchmarks Wave 3, ch. 7 "The Governance Gap" | June 2026 | full | Incident and guardrail statistics |
| Georgian/Replit ViBench post (Vaezipoor) | 2026-06-25 | full | AI Lab builds open benchmarks |
| Julien Coupez LinkedIn | — | **snippet-only** (page returned HTTP 999) | Headline only |
| Vector, "Comprehensive Evaluation of Leading AI Models" | 2025-04-10 | full | Deval Pandya quotes on evaluation |
| Vector, CIBC Trustworthy AI recap | 2022-06-01 | full | Deval Pandya on MLOps, monitoring, IP |
| Samara Centre bio; WASP 2023 bio; CGLR bio | 2023–2025 | full | Third-person bios: AI-safety roles, talk title |
| alphaXiv profile | read 2026-10-23 | partial (lines 1–300) | Benchmark papers (HumaniBench, SONIC-O1, RVCBench) |
| "Inside AI" YouTube interview | 2023-07-07 | full (auto-captions) | Views on risk and governance |
| autoinference.ai | read 2026-10-23 | full (the site is one tagline) | "AutoPilot for Inference Systems" |

## Per-judge table

| Judge | What they care about, in their own words | 3 hardest questions for this project | Answer or demo moment that satisfies them |
|---|---|---|---|
| **Margaret Wu**, Lead Investor (site title: Partner), Georgian. Due diligence and board work. Led Supabase, You.com, Replit, Dominion, Tenstorrent. Waterloo Chemistry degree | **Verifiable citations:** "Georgian initially took notice of You.com based on the platform's ability to include verifiable data sourcing in its output for a user… often down to the exact line in the source webpage." (You.com memo, 2024-09-04)<br>**B2B traction:** "This B2B traction is a key takeaway, as we believe it validates our core thesis" (Replit memo, 2026-03-11)<br>**Field testing:** "Dominion's product strategy is built around actively prototyping and testing technologies" (2026-01-19). In the June 2026 Dominion memo she quotes the founder: "deploy them as soon as possible with them, get their feedback and then re-engineer"<br>**Quantum exposure:** "Past Georgian Pathfinder deals include Xanadu and Tenstorrent" (2026-01-19)<br>**Where the bottleneck is:** "the bottleneck is shifting from authoring code to deploying, securing, and operating it" (Supabase, 2026-06-05) | 1. "Who pays, and how many of them are there? PQC risk analysts are a handful of people. What is the route to CISOs, banks and custodians?"<br>2. "Perplexity, You.com and AlphaSense already cite sources, and GQI sells quantum intelligence. Why doesn't a frontier model with citations already do this?"<br>3. "Has a real user tried it? What did they change?" | **Moment:** click a number and land on the exact quoted sentence and page. Then show the tool refusing to turn 893 logical qubits into a physical-qubit saving. That is her You.com thesis applied to a field where a wrong number moves risk budgets.<br>**Answer:** "Today one analyst spends a long blog post sorting out what a claim actually counts (Ivezic, 2026-10-14). That check becomes a 10-second, evidence-linked card. The buyer is the CISO who must defend a PQC migration timeline to a board and auditors. Next product: an audit-ready 'Q-Day evidence pack' plus alerts when a new paper changes a number." Use any outreach reply; if none arrives, say "target user", never "customer". [INFERENCE: the buyer path is not validated] |
| **Madalin Mihailescu**, CTO, Georgian. Leads the AI Lab. PhD in computer science (distributed data storage and analytics), NetApp ATG, IBM cloud, a CERN LHC data-collection project | **Value over novelty:** "As I like to say, unique is great. Unique is not enough. It has to be valuable as well." (Modern CTO #123, 2019, ~00:17:07)<br>**Trust as thesis:** "the third one is what we call customer trust… Security and privacy definitely play a big component" (~00:15:54)<br>**Data quality:** "Data quality is an area that companies… probably have to invest a bit more time in." (~00:37:03)<br>**Current role:** he "focuses on supporting Georgian's portfolio companies to bring AI products to market" (Georgian bio)<br>Caveat: these quotes are from 2019 | 1. "Where exactly is the LLM, and what happens when it is wrong? Show me field-level accuracy on held-out data, not a happy path."<br>2. "How does this grow past six hand-curated cards? What happens when arXiv v3 changes a number, and how do you ingest PDFs or LaTeX safely?"<br>3. "Why isn't this a spreadsheet? Is the comparability logic a real, general schema, or six if-statements?" | **Moment:** the LLM proposes a card. The deterministic span verifier then **rejects one field live** because the quoted text does not contain that number, and the field is marked `unknown`. Then show the eval panel: score, n, and each disagreement listed.<br>**Answer:** the schema is open (claim, scope, layer, cost statistic, addend interface, failure budget). Each source is pinned by arXiv version and hash, and a new version re-runs extraction and shows a diff. Gates are rules over typed fields, written once. Show the schema file in the repo README. |
| **Julien Coupez**, Customer Engineer for Startups, Google Cloud (Montreal). Former founder and CTO of Nexboo | **Evidence is thin; snippet-only.** LinkedIn headline: "Google Customer Engineer for Startups \| x-AWS \| Former founder/CTO \| Mentor". About: "As a Google Startup Customer Engineer, I help startups succeed by providing hands-on technical guidance."<br>Google Cloud's sponsor text on the Luma page (not his words): "Gemini models, and Vertex AI tools you need to build quickly and securely"<br>No posts, talks or Nexboo details found | 1. "Is it actually deployed? If I open the link on Oct 26, will it work without your laptop?"<br>2. "What does one extraction cost, how is the API key protected, and what stops someone draining your budget?"<br>3. "What is the production path: hosting, monitoring, and can you swap the model?" | **Moment:** the video shows the public URL in the address bar, a real extraction, and a visible cost and latency for that run.<br>**Answer:** the key stays server-side; there is a spend cap and per-IP rate limits; ingestion takes only allowlisted public text; demo data is frozen and labelled with its date; the model sits behind an adapter. Do not claim Gemini or Vertex unless you actually use them. [INFERENCE: his priorities are inferred from his role, not his own words] |
| **Deval Pandya**, CEO and founder of AutoInference. Former VP AI Engineering, Vector Institute (2023–2026). CAISI Research Council; Government of Canada Safe and Secure AI Advisory Group | **Independent evaluation:** "Independent, objective evaluation of this kind is vital to understanding how models perform in terms of accuracy, reliability, and fairness… ultimately to foster trust in AI." (Vector, 2025-04-10)<br>**Operations:** MLOps "is the bridge from [Trustworthy AI] principles to practice"; "One key additional part for MLOps is continuous monitoring and testing." (CIBC recap, 2022-06-01)<br>**Skepticism about opacity:** "'Is this really about IP or are you just not confident whether your systems are trustworthy or not?'" (same recap)<br>**Current focus:** AutoInference is "The AutoPilot for Inference Systems: Adapting, Evolving, Efficient." His LinkedIn headline (snippet) is "Making intelligence efficient"<br>His 2023 keynote title: "Responsible and Trustworthy AI- from Principles to Practice" | 1. "How big is the held-out set, how was it labelled, what is the error rate with an interval, and did you label it before seeing the model's output?"<br>2. "Dual use and harm: does this make attack-cost information easier to weaponize, or feed crypto-panic FUD (fear, uncertainty and doubt)? What are the guardrails?"<br>3. "When the model or the papers change, how do you detect regressions? Is the evaluation continuous?" | **Moment:** the eval panel shows the real score with honest small n (for example "x/y fields correct, 95% CI …") and lists the failures. Then show the "would not compare" refusal and the "unknown" outputs.<br>**Answer:** the ledger stores only published numbers and quotes. It never stores circuits or generates attack improvements. It never converts logical numbers to physical ones. Every card shows "not independently verified." The labelled set is frozen and re-run on every model or prompt change, and the scores are committed to the repo. |

## How the Georgian thesis maps to the five criteria

| Criterion (Luma, verbatim) | Georgian evidence | Make it visible |
|---|---|---|
| Innovation: "going beyond the obvious solutions" | "the trust layer becomes a product surface… domain-specific evals" (Wilde, 2026-05-13) | Show refusing to compare unlike quantities as the product. A citation chatbot is the obvious solution; this goes further |
| Real-World Impact: "clear user, value-add, and a path to production" | Wu: B2B traction; Dominion: deploy to operators and get feedback | Name the target user, show the manual workflow it replaces, state the buyer path |
| UI & Design: "usable by a real user, thoughtful and effective UI elements" | You.com: citations "down to the exact line" | Click a number and the quote is highlighted. Observed and inferred values look visibly different |
| Tech & Deployment: "solid architecture, thoughtful tech choices, and working features" | Mihailescu: "unique is not enough"; Wave 3: 75% of firms use human approval gates, only 29% use policy-as-code | LLM proposes, deterministic gate checks, human approves; live URL |
| Security & Ethics: "responsible applications, guardrails, and safe handling of user data" | Wave 3: "Hallucination causing business error", 40%, the most common incident | A span verifier that blocks hallucinated numbers is a direct answer to the most common AI incident in Georgian's own survey |

## Top 5 ways the 2-minute demo falls flat, and how to prevent each

| # | Failure mode | Why it happens with this panel | Prevention |
|---|---|---|---|
| 1 | **Too much jargon in the first 30 seconds.** Toffolis, Q×T, coherent addend and holdout failures before any stakes | Two investors and two AI engineers; only Wu has a stated quantum link (Xanadu Pathfinder, IQT 2024). [INFERENCE] They decide within 20 seconds whether to keep watching | **0–15s in plain English:** "A headline said a new circuit makes breaking Bitcoin's crypto ~25% cheaper in hardware. The paper never measured hardware. Analysts catch this by hand; this tool catches it in 10 seconds, with the receipts." Keep jargon inside the UI, behind tooltips, never in the narration. |
| 2 | **"Who pays?" goes unanswered.** It looks like a niche hobby for a few analysts | Wu writes about B2B traction and ARR. Madalin Mihailescu: "It has to be valuable as well" | One title card: **user** (PQC risk analyst) → **buyer** (CISO or risk team defending a migration timeline) → **next step** (evidence pack plus change alerts). Use a real outreach reply if one arrives; otherwise say "target user". Never imply a customer. |
| 3 | **The AI is invisible or untrustworthy.** It looks like a hand-built table (no AI), or like the LLM writes numbers (scary) | Deval Pandya and Madalin Mihailescu will ask what the AI does and how you know it is right. The Wave 3 survey puts hallucination first among incidents | Show the full loop once: LLM proposal → **verifier rejects an unsupported field** → human approves → eval panel with n and the failures. That moment covers Innovation, Tech, and Security & Ethics together. |
| 4 | **Broken or static deployment during online judging.** Render cold start, an expired key, a video that looks like slides | Online judging is Oct 26, with no presenter. The rules ban "faking your demo". Julien Coupez will click the link | Pre-warm and keep the service alive through Oct 26. Freeze demo inputs and label their date. Record the video against the live URL with the address bar visible. Add a visible "demo data frozen 2026-10-xx" badge. Test the link from a logged-out browser on another network. |
| 5 | **It reads as a crypto-doom tool, or makes one physics mistake.** It seems to amplify Q-Day FUD or help attackers, or the demo itself mislabels a logical count as physical | Deval Pandya sits on AI-safety bodies. Your memo already flags that treating 893 logical qubits as a physical or full-attack saving would "damage trust". [INFERENCE] A quantum-literate viewer (Wu via Xanadu, or a Georgian AI Lab reviewer) spotting one error would sink credibility | Put a "What we do not do" box in both the app and the Devpost page: no circuits, no new attack estimates, no logical-to-physical conversion, published sources only, "not independently verified" on every card. Narrate the probability check as "a plug-in estimate assuming independent trials, not a certificate." State the 1QBit separation and the AI tools used in the disclosure. |

Two more risks, lower priority:
- **Partner bolt-ons look fake.** Clerk and SurrealDB are Georgian portfolio companies, and the rules require meaningful use. Claim only Eon Era, unless SurrealDB genuinely stores source → claim → assumption versions.
- **Portfolio sensitivity [INFERENCE].** Xanadu is a Georgian Pathfinder deal. Keep the tone neutral toward vendors: the ledger refuses comparisons; it does not grade companies.

## Prioritized "make it land" checklist

### P0: demo video (≤2:00; Luma requires "what you built, how it works and the key technology behind it")
1. **0:00–0:15:** state the plain-English stakes and the user in one sentence (see failure 1). Show the real public claim with its source.
2. **0:15–0:45:** two claim cards side by side. Click a number and the exact quote and page are highlighted (Wu's You.com moment). The comparison gate turns red with the reason "different layer: logical vs physical," and the tool refuses to compare.
3. **0:45–1:05:** the deterministic check: 111/360,960 → ~0.000308 per sampled addition → (1−111/360960)^9024 ≈ 0.062. Say "assumes independent trials; not a certificate" on screen.
4. **1:05–1:30:** paste a new supported passage. The LLM proposes a card. The verifier **rejects one field** and marks it `unknown`. A human approves the rest.
5. **1:30–1:45:** eval panel: real score, n, and the failures listed. No rounding up.
6. **1:45–2:00:** one architecture line (LLM proposes → deterministic gates → human review → versioned ledger), the guardrails, the user → buyer path, and the live URL on screen.
7. Record against the deployed app, not localhost. Keep the address bar visible.

### P0: deployment
8. Live link works logged-out on Oct 26: pre-warmed, spend cap, rate limit, key server-side, ingestion limited to the allowlist.
9. Frozen demo dataset with a visible date badge. No "live monitoring" claims.

### P0: Devpost page (judges read it in round 1)
10. **First paragraph:** problem → user → what it refuses to do → why that is valuable. Lead with "verifiable to the exact quote" (Wu's language) and "domain-specific verifier" (Georgian's trust thesis).
11. **"How we know it works":** eval-set size, how it was labelled (frozen before running the model), score, and the listed failures (Deval Pandya).
12. **Security & Ethics section:** no circuits, published numbers only, no logical-to-physical conversion, "not independently verified" labels, human approval gate, no user data collected. Optionally note that a span verifier targets the most common AI incident in Georgian's own survey: hallucination causing business errors (40%, Wave 3).
13. **Disclosure, required by the rules:** prior work, open-source dependencies (FastAPI, Gradio, SciPy and their licenses), **AI tools used** (for example Claude Code), and separation from the employer.
14. **Partner platforms:** list only what is genuinely used. Eon Era: the extraction eval against labelled truth.
15. **Path to production:** the next three steps (more sources, version diffs and alerts, CISO evidence pack) and a named target user, honestly labelled.

### P1: polish
16. Tooltips for logical/physical, Toffoli, and addend interface. Observed vs inferred values in distinct colours.
17. A README diagram plus the schema file (Madalin Mihailescu's "is it a real schema?").
18. For the live round, a 15-second "what's next" with any reply from a practitioner you contacted.

### P1: rehearse answers for the live round (top 10)
19. Wu: "Who pays?" Mihailescu: "Show me the LLM failing." Coupez: "Cost per run and the security model?" Pandya: "Eval size, labelling, and dual-use?" Each answer must fit in 20 seconds.

## Evidence that cuts against the pitch
- **No judge has publicly said they care about Q-Day.** Wu's quantum link is the Xanadu Pathfinder line plus an IQT talk listing (the talk content was the writer's guess). [INFERENCE] The panel will reward the verification pattern more than the quantum topic.
- **Deval Pandya's current company is inference-efficiency infrastructure.** His evaluation and safety record is from Vector (2021–2026), so his priorities may have shifted toward cost and efficiency. Showing cost per extraction hedges this.
- **Madalin Mihailescu's quotes are from 2019.** His current bio still centres on bringing AI to production, but treat the quotes as dated.
- **Julien Coupez's priorities are inferred from his role only.**
- **"Trust becomes the moat" is a Georgian essay, not a judge's.** Use it as house context, not as a judge quote.
- **Scale mismatch.** Georgian writes initial checks of $25M+ into growth companies (georgian.io). [INFERENCE] The judges are scoring "startup potential" for the golden ticket, so a niche analyst tool needs the CISO/enterprise path stated, or it scores low on Real-World Impact.

## Files
- `/tmp/tq-work/docs/decision/ranked-memo.md:42-68`: pick spec, the 2-minute demo script (line 46), cut order (line 68), and the prize and trust boundary (line 52). The checklist above builds on that demo script.
- `/tmp/tq-work/docs/wayfinder/research-brief.md:33-39`: event facts and judge list, consistent with the Luma page.
- `/tmp/tq-work/docs/research/resource-claims-verification.md:164-168`: earlier judge-appeal score of 3 ("Still niche, with no paying buyer shown"). This report agrees with that weakness.