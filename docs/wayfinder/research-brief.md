# Research brief for Wayfinder research tickets

Every research session in this repository follows this brief. Your ticket (a GitHub issue labelled `wayfinder:research`) gives the opportunity area and the question. This file gives the shared context, rules, output format, and scoring.

## The decision this research feeds

Severyn must choose **one project** to build for the Build North hackathon. The map's destination is a ranked decision memo (top 3 options with evidence, the pick, and a one-page spec). Your report is one input to that memo. Write for a reader who must make a decision, not for a literature review.

The problem, as agreed with Severyn on 2026-10-21:

> Choose the highest-leverage project in AI × quantum / deep tech that (1) has a real user after Oct 25, (2) builds Severyn's credibility in AI and quantum, (3) can reach the top 10 with investor judges, and (4) ships in about 12 hours of solo building.

When these conflict, the priority is (1) > (2) > (3). A real user also scores with the judges.

**Do not overfit on science.** A clever result with no person who would use the tool next week scores low. Look for evidence of pain from practitioners, buyers, and programs, not only from papers.

## Who is building

Severyn Balaniuk, Waterloo, Ontario.

- Research Software Developer at 1QBit since March 2025: productizes Python and Julia research prototypes; built and runs an internal Gradio quantum resource estimation demo on GCP Cloud Run; FastAPI endpoints, Docker, Kubernetes, Redis, MongoDB, AWS deployment, CI test frameworks.
- Technical co-founder at Maindframe (2025 to 2026): agentic AI research automation with bounded tool execution and reproducible reports; a quantum architecture search harness (Python, Cirq, Gymnasium, OpenRouter agents); an RL environment for VQE circuit optimization; a multi-agent anomaly-detection benchmark.
- Machine learning engineer intern at Open Quantum Design (2024 to 2025): distributed training for 500k fluorescence images of trapped ions.
- Research and development team lead at the Institute for Quantum Computing.
- MSc Physics (Quantum Information), University of Waterloo, with a minor in ML/AI. BSc Computer Science, National Technical University of Ukraine.
- Winner, Wildfire Hackathon 2024 (Waterloo.AI). Canada Graduate Scholarship.
- Also founded Upright (AI for construction subcontractors) and runs Aquarium, a personal lab that tests published claims about AI agents and publishes the evidence whichever way it lands. A consistent theme in his work is verification and open benchmarks.

Employer note: Severyn confirmed on 2026-10-21 that his employment agreement places no restriction on this project. Still flag direct overlap with 1QBit's commercial product TopQAD (physical-layer resource estimation, magic-state-factory design, lattice-surgery compilation) as a positioning risk.

## Hackathon constraints

- Build North: Ship Something Real (Georgian). Build week Oct 16 to 25, 2026. Submission on Devpost by **Oct 25, 11:59 PM ET**.
- Required: public GitHub repo, live link if applicable, demo video of at most 2 minutes, write-up with stack, partner platforms used, and disclosure of prior work. Code must be written during build week; open-source dependencies are fine if disclosed.
- Judging criteria: Innovation; Real-World Impact (clear user, value-add, path to production); UI and Design; Tech and Deployment; Security and Ethics.
- Judges: Margaret Wu (Lead Investor, Georgian), Madalin Mihailescu (CTO, Georgian), Julien Coupez (Google Cloud Customer Engineer for Startups), Deval Pandya (CEO, Autoinference; former VP AI Engineering, Vector Institute). Georgian is a B2B growth-equity fund.
- Partner prizes: Best Overall; Best Use of Expo (mobile); Clerk (auth); Eon Era (agent testing and benchmarking); SurrealDB Agent Memory.
- Top 10 demo in person in Toronto on Oct 29.
- Time left for building: about 12 hours, solo (Thursday evening, Saturday, Sunday). Available credits for the build: pending $100 Anthropic API, $50 Render, $50 SurrealDB.

## Evidence already in this repo

Read these before searching, and do not redo them:

- `docs/research/evolve-systems.md`: LLM evolutionary search systems (OpenEvolve, ShinkaEvolve, AlphaEvolve, FunSearch), costs.
- `docs/research/quantum-ai-discovery.md`: quantum AI-discovery papers (arXiv 2610.22367, OmniQEC, VQC agents, Pasqal agentic workflows, IBM code search, VarTODD).
- `docs/research/field-needs.md`: where fault-tolerant cost concentrates, existing resource tools, user personas, critiques of arXiv 2610.22367.
- `docs/research/competitors-diligenceagents.md` and `docs/research/competitors-intelplatforms.md`: AI diligence and quantum market-intelligence products (the investor-diligence idea was ruled out on 2026-10-21 as crowded).

## Research rules

1. **Primary sources.** Read the primary artifact: the paper's method and results sections, the product's own pages and docs, the repository's code and README, the program's official call. A search snippet, abstract, or headline is a discovery lead, not evidence.
2. **Read depth on every source:** `full`, `partial (sections ...)`, or `snippet-only`. Nothing `snippet-only` may carry a conclusion.
3. **Dates.** Give the publication or update date of every source. Flag anything older than 18 months as possibly stale.
4. **Seek disconfirming evidence.** For each promising wedge, search for the strongest reason it fails: an existing product, a dead startup, a maintainer saying "nobody needs this".
5. **Verify code exists.** For any repository you propose to reuse, confirm it exists, its license, and its last commit date.
6. **Separate** observed facts, the source author's interpretation, and your own inference. Mark inference `[INFERENCE]`.
7. **Be concrete:** names of organisations, people's roles, numbers, prices, URLs.

## Output

Write one file: `docs/research/<ticket-slug>.md`, where the slug is given in your ticket. Commit it on a branch named `research/<ticket-slug>` and push the branch. Do not open a pull request and do not edit other files.

Use this structure:

1. **Bottom line** (at most 6 bullets): is there a high-leverage project here for Severyn, yes or no, and why.
2. **The pain:** who has it (named organisations and roles), how often, what they do today, what it costs them. Evidence with links, dates, and read depth.
3. **Existing solutions:** table of products, open-source tools, and research prototypes, with what each does, who uses it, price or license, and read depth.
4. **The gap:** what remains unsolved, and why nobody has filled it.
5. **Candidate wedges** (2 or 3): each a project Severyn could ship in about 12 hours. For each give: the user, the job it does, what the demo shows in 2 minutes, reusable components (verified repos with licenses), required data and compute, estimated LLM cost, partner-prize fit, and the main way it fails.
6. **Scores** for the best wedge, 1 to 5 with a one-line justification each:
   | Criterion | Score | Why |
   |---|---|---|
   | Real user with evidence of pain | | |
   | AI makes a material difference | | |
   | Severyn's unfair advantage | | |
   | Buildable and demoable in 12 hours | | |
   | Judge appeal (Georgian investors) | | |
   | Adoption path after Oct 25 | | |
   | Competition density (5 = open field) | | |
   | Credibility gain in AI and quantum | | |
   | Risk (5 = low: no dual use, no 1QBit overlap) | | |
7. **Sources:** every source with URL, date, and read depth.
8. **Open questions** that the synthesis step or Severyn must answer.

Keep the report under about 3,500 words. Depth of evidence matters more than length.
