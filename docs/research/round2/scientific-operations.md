# Small improvements to research data and simulation tools

Researched **2026-10-23**. This report examines daily work with experimental data and simulations. All proposed examples use public inputs and ordinary processors.

I read the research brief and `ai-for-science-adjacent.md` first. This report does not assume a quantum ledger or a materials-discovery project.

**Observed** means a source reports the claim. Author interpretations remain attributed. **[INFERENCE]** marks this report's conclusions and proposed behavior.

No practitioner replied to this investigation. No external messages were sent. No implementation, tests, builds, or smoke runs were performed.

## Bottom line

- **Two tools have specific requests from users.** BDF #136 asks for calculated columns in battery data. Tom Holland requested this on 18 October 2026. Graham Kimbell supported it the next day. Jobflow #873 reports restart problems in three simulation workflows. [S1, S2]
- **The smallest useful contribution is a BDF calculation function.** BDF means Battery Data Format. It standardizes data from battery-testing instruments. A function could calculate power from recorded current and voltage. Holland already has related code in PyProBE, so another contribution might duplicate his work. [S1, S3]
- **Restarting failed simulations is harder to complete safely in 12 hours.** Jobflow assigns identifiers to calculation steps. Rebuilding a workflow can change those identifiers and break links to previous results. Existing tools already support several ways to restart calculations. [S2, S4, S5, S6, S7]
- **A general AI tool for converting instrument files would overlap with existing software.** yadg preserves units, measurement uncertainty, original file details and processing history. Anthropic publishes an instrument-conversion skill that can also generate Python code. [S8, S18]
- **These tasks do not show a strong need for AI during use.** Fixed calculations and explicit workflow rules determine correctness. A coding agent can help write the software. A separate AI interface has no demonstrated advantage here. [INFERENCE]
- **The BDF contribution is worth considering for a user next week.** It could build scientific-software credibility if researchers use it. This evidence does not establish a business opportunity or a direct quantum contribution. [INFERENCE]

## What is actually painful?

| Practitioner / workflow | Observed task and workaround | Limits of the evidence |
|---|---|---|
| **Tom Holland**, Imperial College London electrochemical-science PhD researcher and PyProBE contributor; **Graham Kimbell**, public profile identifies Empa affiliation | BDF currently returns directly convertible recorded columns. Holland wants users to request other quantities from known relationships; Kimbell proposes `bdf.derive(df, columns)` and a registry of Polars-expression recipes. Holland shares an existing PyProBE integration recipe, explicitly preferring recorded charge over reconstructed integration. [S1, S12] | Two explicit participants; not two paying customers. No measured frequency, time saved, purchasing budget, or proof the contribution is unclaimed. |
| **@Barabama**, jobflow user; institution not verified | Reports `Maker.make()` creates new UUIDs on rerun, breaking downstream references after partial failures. Says a custom wrapper was used for NSCF, QHA and magnetic-exchange workflows on Slurm; reports OOM/walltime and final phonon-analysis failures. Uses per-structure JSONStore and name/index matching. Maintainer @gpetretto warns name collisions invalidate this strategy, especially shared databases. [S2] | Real-workflow validation is **the author's report**, not independently executed here. No saved core-hours or monetary cost quantified. The wrapper already exists externally; this is not an untouched opportunity. |
| **jobflow-remote maintainers/users** | #842 documents redundant dynamic-flow `store_inputs` jobs and downstream execution after hidden failures. Another user confirms problems and moves `store_inputs` onto a local shell worker to avoid submitting them. Core PR #850 proposes flow outputs, with unresolved replacement/output semantics. [S5, S6] | Related recurring workflow trouble, not independent proof that a new local-recovery package is wanted. |
| **@SebaWitt**, BioLogic EC-Lab data user; **Peter Kraus**, TU Berlin group leader/yadg maintainer | August 2026: a user sees current in MPT export but not MPR extraction. Maintainer finds it is not a missing raw column: EC-Lab derives average current from charge/time. User accepts the BDF-based calculation workaround. Separately, #41 reports opening/exporting an MPR can add columns to that MPR. [S9, S10, S13] | Strong evidence that “missing column” can be a semantic misunderstanding. #270 is **closed/not planned**, not an unfixed parser request; #41 is from **2022 [STALE]**. Neither proves demand for an AI handoff tool. |

No source above establishes how often a typical lab hits these cases. Repeated issues/participants establish that the classes of trouble recur, not a population-level incidence rate.

## Existing solutions and the strongest competition

| Solution, evidence read | What is already solved / why it challenges a new product | Licence / freshness |
|---|---|---|
| **BDF**, README, current public API, roadmap and contribution guide [S3, S14] | Cycler export standardization; read/scan/save, normalization, validation, cleaning, metadata and CLI already exist. Ontology defines canonical units and distinctions such as net/cumulative/cycle/schedule capacity. Roadmap says explicitly **not an analysis library, instrument control, database or hosted service**. Public `__all__` lacks `derive` at read time. | Apache-2.0 verified from licence header and GitHub metadata. Latest default-branch commit **2026-10-23**, `4c615406…`. |
| **PyProBE**, full README and input guidance; recipe in BDF thread [S1, S15] | Existing battery analysis, filtering, unit conversion, plotting/GUI, cycling and degradation methods. **Already the author's home for derivation recipes.** Using it directly may be better than moving code into BDF. | BSD-3-Clause stated in repository metadata/README. Last-commit API returned 403, so **not independently dated; no proposal here depends on copying its implementation**. |
| **jobflow**, entire current `run_locally` function, manager API, #873 [S2, S4] | Local execution with dynamic replacement/detours/additions and FireWorks conversion. Current source does not offer a resume parameter or skip-completed-store branch. This supports the narrow local-manager gap, not the claim that workflow recovery in general is absent. | Full licence read: LBNL/UC three-condition permissive terms plus enhancement grant; GitHub SPDX is **NOASSERTION**, so do not mislabel MIT. Latest commit **2026-10-19**, `5c536747…`. |
| **FireWorks**, full rerun tutorial [S7] | `lpad rerun_fws -s FIZZLED`; task-level recovery; error-stack queries; archival of old launches. Explicit warning: reruns do **not** undo dynamic actions or modified child inputs. | Not proposed as a dependency here; licence/last commit not investigated. Live docs show version 2.1.4; publication date absent. |
| **jobflow-remote**, discussion #360, body and visible replies [S11] | Maintainer is already experimenting with no-MongoDB execution using MontyDB or SQLite. Explicit limitations: concurrency/atomicity and database-lock failures; SQLite experiment needs substantial review. Not a quick empty niche. | Discussion 2025-09-29 to at least 2025-10-22. Not a proposed dependency. |
| **AiiDA / signac**, targeted official docs [S16, S17] | AiiDA documents calculation/workflow provenance, work-chain steps and exit behavior. signac already provides indexable project data/metadata layout and collective postprocessing access. A generic provenance store or sweep browser would duplicate established infrastructure. | Docs undated; accessed 2026-10-23. Depth is deliberately limited: no claim that either fixes jobflow's exact local UUID semantics. |
| **yadg**, full README/features [S8] | Instrument extraction to xarray DataTree/NetCDF; units/uncertainty, timestamps, locale, original metadata and provenance; merges multiple files. This is already the lab-to-analysis handoff plumbing. | GPLv3 verified header/metadata; latest default-branch commit **2026-07-28**, `61d55fe1…`; repo push timestamp is later, **2026-08-14**—not the same as last commit. |
| **Anthropic instrument-data-to-Allotrope example skill**, full skill [S18] | Detect, parse with allotropy, output ASM JSON/CSV and standalone Python. Already distinguishes raw and derived data with traceability. Its flexible fallback expressly lacks full traceability. This is a serious plain-coding-agent alternative, not evidence of deployment/customer numbers. | Skill says validation updated **2026-01-07**; repository file publication date unverified. Not reused in proposal; licence not audited. |

The absence of a competing search result is **not** the evidence for these gaps. The useful evidence is the precise missing operation and maintainers' own boundaries.

## Three concrete alternatives

### A. Calculate missing columns in battery data

A researcher receives battery-test data that lacks a quantity needed for analysis. The table may record current and voltage but omit power.

Input: a table in BDF format and the requested quantity. Polars is the table-processing library that BDF uses.

Output: the original rows and values, plus the calculated column. The output explains which calculation and source columns it used. [INFERENCE, based on S1/S3]

The proposed 12-hour artifact is a `derive(df, columns)` function that follows BDF's existing interfaces. It supports these calculations:

- Power = current × voltage.
- Net capacity or energy = charging quantity − discharging quantity.
- Cumulative capacity or energy = charging quantity + discharging quantity.

The function resolves the required source columns. It preserves recorded values and reports missing inputs instead of estimating them. An executable example explains its use.

This bounded function does not satisfy every part of #136. Integrating current to estimate charge requires additional decisions about calculation preference. Reconstructing battery cycles requires decisions about reset behavior. Those features are outside this proposal. [INFERENCE]

**Why not a plain script / agent?** For one file, a Polars expression is better. Shared value is a reviewed, canonical API reused across cyclers and notebooks, not novel arithmetic. A plain coding agent supplied the ontology and thread can implement the same code. Runtime AI has **no demonstrated material contribution**; optional explanations are not sufficient justification. [INFERENCE]

**Public smoke input / exact numerical target.** Public repository file `data/SINTEF__LiGrR2032__2024-04-30__25degC__Landt.csv`: first data row has current **0.0000 A**, voltage **2.9215 V**; row beginning **2882** has current **−0.0002 A**, voltage **2.6450 V**, elapsed time **43200.020 s**. Expected derived powers are **0 W** and **−0.000529 W**, respectively, by direct multiplication. Row 2883 gives **−0.0005256 W**. These are **calculated expected outputs, not executed smoke results**. Legacy headers/preamble/trailing delimiter are visible; do not assume this historical CSV already passes today's canonical BDF validator. For a first smoke, explicitly map only the observed current/voltage columns into a canonical two-row table without changing values. Assert unchanged row count/order and recorded columns. [S19]

**Data/licence/compute.** CPU only, Polars; no instrument, paid database or simulation executable. BDF code is Apache-2.0. CSV is publicly present in that repository, but **no separate data-specific licence was established**; retain its source link rather than asserting a new CC licence or redistributing a bundle without checking. Runtime LLM cost **$0**. AI-assisted development cost is discretionary, not product operating cost. [S3, S19]

**Deciding experiment.** Send the inquiry below. Useful positive evidence: author specifies an unclaimed recipe and would try an upstream patch. Negative: “already implementing,” “keep it in PyProBE,” or only one notebook needs it. Before a build commitment, compare a handful of directly mapped public rows with the one-line script; if a package adds no reusable benefit, make the smaller contribution instead. [INFERENCE]

**Adoption/integration.** Existing #136 → agree bounded recipe/API scope → focused upstream contribution, not a separate upload service. BDF contribution guide explicitly welcomes focused changes with tests and API docs. **No acceptance is promised.** Two-minute demo: a real unconverted export, explicit source mapping, requested quantity, arithmetic values and preserved inputs. [S1, S14]

**Strongest rejection.** The request's author already implemented recipes in PyProBE; this may be a straightforward port the maintainers prefer to own, not a project for a new entrant. It is adjacent deep-tech credibility, almost no quantum/AI differentiation. Partner-prize fit is weak; do not bolt on memory/auth/agent evaluation. [INFERENCE]

### B. Restart a failed local simulation workflow

A jobflow user wants to restart a failed sequence of calculations without repeating completed work.

Input: the saved workflow, its saved results and evidence of failure. Output: a completed workflow and a record of reused and repeated steps.

The saved workflow must retain links between calculation steps. Recreating the workflow through a `Maker`, jobflow's workflow-building class, can change those links. This is the harder case reported in #873. [S2]

**Smallest honest 12-hour artifact.** A **preserved-flow local recovery contribution** with per-run isolation, stored-output resolution, downstream dependency handling, and an executable fail/resume demonstration. No guessed name-based cross-run identity, shared-DB merging, solver-parameter changes, HPC submission, or claim of universal dynamic-flow recovery. Reject unsupported dynamic expansions explicitly rather than silently producing stale results. This is narrower than the full user problem, so **do not present it as closing #873 without the reporter's agreement**. General dynamic recovery is not a credible guaranteed 12-hour deliverable. [INFERENCE]

**Public smoke.** #842 contains complete CPU arithmetic jobs. Its recursive flow starts at `1+2=3`, adds two until reaching **11**, then returns downstream **13**. A recovery demonstration can introduce a controlled failure before final completion and require final output **13**, no re-execution of already persisted arithmetic jobs, and no unresolved references. This is a proposed mutation/proxy, **not a VASP calculation or an executed result**. Source also supplies a real hidden-failure example where a failed replaced job incorrectly lets downstream work become eligible. [S5]

**Existing/simple alternatives.** Use FireWorks rerun/task-level recovery, use jobflow-remote, or preserve/reuse a workflow object rather than reconstruct it. Reporter already maintains a wrapper; ask whether contributing cases/review there is more valuable than another manager. A plain coding agent has precisely the same implementation leverage. Runtime AI might explain logs but cannot safely infer identity or decide which scientific results remain valid. [S2, S4, S7, S11; INFERENCE]

**Data/compute/licence.** CPU arithmetic graph and local file store only; no VASP licence. jobflow source licence verified above; reporter's external Gitee implementation **not read or licence-verified and must not be copied**. Runtime LLM cost $0. **Cheap deciding experiment:** ask reporter to supply one missing minimal dynamic case and say whether preserved-flow recovery meets their task; otherwise reject this bounded variant. **Adoption:** maintainer-discussed contribution or reporter workflow trial, not a new scheduler. **Main rejection:** preserving an initial graph may not preserve runtime-generated descendants; safe identity and invalidation semantics can consume the entire build window. The best useful artifact may instead be a small upstream regression/repro contribution, unsuitable as a standalone hackathon product. [INFERENCE]

### C. Explain differences between raw and exported battery files

A researcher gives an analyst two versions of a battery-test file. The analyst needs to know which values the instrument recorded and which values its export software calculated.

MPR is BioLogic's raw binary format. MPT is its text export. NetCDF is a structured scientific-data format that yadg can produce.

The proposed output compares columns, units and data coverage. It explains differences without changing either input or inventing measurements. Issue #270 concerns calculated average current. Issue #41 concerns changes to a raw file after export. [S9, S10]

**Smallest artifact.** One BioLogic-only comparison command using yadg, not a universal parser: summarize existing columns, units, timestamps, rows and missing current; explain the documented charge/time derivation separately. Never synthesize current merely because the requested column is absent. Public candidate input is #270's `cccv_example.zip`; #41 has `OpeningFiles.zip`. **The attachments were linked in fully read issues but their bytes and individual data licences were not inspected.** This is therefore not the preferred immediately reusable public artifact. [S9, S10; INFERENCE]

**Smoke contract.** For the #270 example, maintainer reports **16 raw column IDs** `[1,2,3,21,31,65,131,4,7,13,5,6,9,39,211,468]`; a diagnostic must not label an absent raw current column as a parser omission. Exact parsed row counts/charge-current residuals remain unmeasured. That is an invariant from the maintainer report, **not independent numerical validation**. [S9]

**Alternatives/AI.** Existing yadg/BDF calculation plus a short explanation already resolved this user's issue. Anthropic's conversion skill and a plain coding agent reading the maintainer reply substantially cover the proposed explanation layer. A deterministic comparison script is simpler than a product. A domain-aware model could draft format mappings, but no comparative evidence here shows it beats the script or agent. [S8, S9, S18; INFERENCE]

**Compute/adoption/experiment/reject.** CPU only; yadg GPLv3 and BDF Apache-2.0 require respecting distribution terms; do not treat all code as MIT. Runtime LLM $0 needed. Seek Peter Kraus's view in the existing issue or via verified TU Berlin contact **peter.kraus@tu-berlin.de**, asking whether a focused upstream example is useful. Kill the product idea unless an analyst has a recurring pair-comparison task and supplies expected output with reuse permission. Strongest rejection: #270 is solved conceptually, not a missing raw-data extractor; a separate service risks propagating the same raw/derived misunderstanding. [S8–S10, S13; INFERENCE]

## Draft question for a researcher

**Preferred recipient:** Thomas Holland, **thomas.holland17@imperial.ac.uk**. Verified official Imperial profile gives contact, electrochemical-science group and battery-degradation research; PyProBE README links @tomjholland as contributor; GitHub bio matches. Public route: [BDF #136](https://github.com/battery-data-alliance/battery-data-format/issues/136). [S1, S12, S15]

**Suggested subject:** Question about calculated columns in battery data

> Hi Thomas,
>
> I read your BDF issue #136 and the PyProBE calculation example you shared. I'm considering a small open-source contribution for researchers working with battery-test data.
>
> Which calculated column do you most often need to add by hand?
>
> A short example is enough. No call needed.
>
> Severyn

This draft contains one question. It does not claim a built tool, user commitment or measured savings. **Do not send it without new authorization.**

## Source register

All read/accessed **2026-10-23**. `Undated` means publication/update date was not provided, not that the source is fresh. No papers were shortlisted; conclusions rely on operational requests, code and primary docs rather than abstracts.

| ID | Primary source / URL | Source date and read depth |
|---|---|---|
| S1 | [BDF #136](https://github.com/battery-data-alliance/battery-data-format/issues/136) | Created 2026-10-18, updated 10-19; **full body + 2 comments**, including recipe code. |
| S2 | [jobflow #873](https://github.com/materialsproject/jobflow/issues/873) | 2026-05-09/11; **full body + maintainer comment**. |
| S3 | [BDF repository](https://github.com/battery-data-alliance/battery-data-format), [metadata](https://api.github.com/repos/battery-data-alliance/battery-data-format), [latest commit](https://api.github.com/repos/battery-data-alliance/battery-data-format/commits?per_page=1), [licence](https://raw.githubusercontent.com/battery-data-alliance/battery-data-format/main/LICENSE) | Latest commit 2026-10-23; **partial README** (motivation, scope, required/recommended/optional quantity semantics), full metadata/latest commit; licence header/definitions read. |
| S4 | [jobflow manager API](https://materialsproject.github.io/jobflow/jobflow.managers.html), [current local runner](https://raw.githubusercontent.com/materialsproject/jobflow/main/src/jobflow/managers/local.py), [licence](https://raw.githubusercontent.com/materialsproject/jobflow/main/LICENSE), [latest commit](https://api.github.com/repos/materialsproject/jobflow/commits?per_page=1) | Code latest repo commit 2026-10-19; API undated; **full runner, full licence, full API page and commit metadata**. |
| S5 | [jobflow #842](https://github.com/materialsproject/jobflow/issues/842) | 2026-01-21 to 02-01; **body, examples, logs, graph and visible user confirmation**; final few lines not read. |
| S6 | [jobflow PR #850](https://github.com/materialsproject/jobflow/pull/850) | 2026-02-11 to 03-16; **full body + 5 comments**. |
| S7 | [FireWorks rerun tutorial](https://materialsproject.github.io/fireworks/rerun_tutorial.html) | Undated live v2.1.4 docs; **full tutorial**, including task-level and dynamic-action warnings. |
| S8 | [yadg repo](https://github.com/dgbowl/yadg), [features](https://raw.githubusercontent.com/dgbowl/yadg/main/docs/source/features.rst), [licence](https://raw.githubusercontent.com/dgbowl/yadg/main/LICENSE), [latest commit](https://api.github.com/repos/dgbowl/yadg/commits?per_page=1) | Latest default-branch commit 2026-07-28; **full README/features**, licence header, full metadata/commit record. |
| S9 | [yadg #270](https://github.com/dgbowl/yadg/issues/270) | 2026-08-19/20; **full body + 3 comments**; attachments not fetched. |
| S10 | [yadg #41](https://github.com/dgbowl/yadg/issues/41) | 2022-03-04 **[STALE]**; **full issue**, attachment not fetched. |
| S11 | [jobflow-remote #360](https://github.com/Matgenix/jobflow-remote/discussions/360) | 2025-09-29 onward; **body and visible replies through 2025-10-22**; not all final page content. |
| S12 | [Imperial Thomas Holland profile](https://profiles.imperial.ac.uk/thomas.holland17), [GitHub profile](https://api.github.com/users/tomjholland), [Kimbell GitHub profile](https://api.github.com/users/g-kimbell) | Imperial page undated; GitHub profiles updated 2026-10-21 / 10-13; **full contact/bio and full API profiles**. Empa team page returned 403; search snippet alone not used to certify its email. |
| S13 | [TU Berlin Peter Kraus profile](https://www.tu.berlin/en/concat/about-us/peter-kraus) | Undated; **full profile/contact**. |
| S14 | [BDF roadmap](https://raw.githubusercontent.com/battery-data-alliance/battery-data-format/main/ROADMAP.md), [contributing](https://raw.githubusercontent.com/battery-data-alliance/battery-data-format/main/CONTRIBUTING.md), [public API](https://raw.githubusercontent.com/battery-data-alliance/battery-data-format/main/src/bdf/__init__.py) | Undated files on main at 2026-10-23; **full roadmap/contributing; API exports, lazy mapping and surrounding code**. |
| S15 | [PyProBE repo](https://github.com/ImperialCollegeLondon/PyProBE), [input guidance](https://raw.githubusercontent.com/ImperialCollegeLondon/PyProBE/main/docs/source/user_guide/input_data_guidance.rst) | Live docs undated, README cites its 2025 paper; **full README and input guidance**. Paper not read/used as research evidence; latest-commit API 403. |
| S16 | [AiiDA usage](https://aiida.readthedocs.io/projects/aiida-core/en/stable/topics/workflows/usage.html) | Undated; **partial: returning data/provenance, work-chain define/outline/exit codes/launching**. |
| S17 | [signac framework docs](https://signac.readthedocs.io/en/latest/) | Undated; **full landing page only**, not a capabilities audit of every package. |
| S18 | [Anthropic instrument conversion skill](https://raw.githubusercontent.com/anthropics/knowledge-work-plugins/main/bio-research/skills/instrument-data-to-allotrope/SKILL.md) | Embedded validation update 2026-01-07; **full skill**, not all implementation scripts. |
| S19 | [SINTEF public input CSV](https://raw.githubusercontent.com/battery-data-alliance/battery-data-format/main/data/SINTEF__LiGrR2032__2024-04-30__25degC__Landt.csv) | Filename says 2024-04-30; observations include 2024-05-01 **[STALE as an experiment, useful as fixture]**; **partial: preamble/header/rest rows and discharge transition including rows 2882/2883**, not all 25k rows. |

## Decision boundaries

1. An explicit maintainer/user answer can change the choice; an unanswered inquiry cannot count as adoption.
2. General workflow rescue is not a safe 12-hour promise. A correct narrow upstream function is more credible than an AI-controlled scheduler demo.
3. If the final selection requires material **runtime AI** or direct **quantum** contribution, **reject all three as the hackathon pick** rather than manufacture those connections.
