# Checking whether scientific code reproduces its results

Research date: **2026-10-23**. Read the research brief, `ai-for-science-adjacent.md`, and current ranked memo for context; no product choice assumed. `[INFERENCE]` denotes analysis rather than observed demand. No outreach, production implementation, build or experiment was run. Dates and read depths are in the source register. Undated documentation was accessed on this research date; publication recency is unknown. Sources before 2025-04-23 are flagged **stale**.

## Bottom line

- **There is a real adjacent workflow, with a newly funded institutional user group:** Amsterdam UMC and TU Delft's September 2026–September 2028 CODECHECK project plans approximately **60 checks**, a structured issue-recording template, and classification of failures including **outputs that do not match the manuscript**. Named practitioners: Merel Postema, Thomas Pronk, João Guimarães and Yasel Quintero. This is observed work, **not a request to buy our tool**. [S1]
- **Kill the generic “agent that makes papers/notebooks run” product.** Code Ocean, Binder/repo2docker, ReproZip, Renku, pixi and notebook validators cover much of the mechanics. Renku now explicitly supports **Claude, Codex and Pi in research sessions**. ReproAgent already persists paper requirements and provenance through generation and repair. A familiar agent UI is not a wedge. [S4–S11, S15]
- **A narrower possibility is an upstream, human-reviewed failure-evidence helper for CODECHECK.** However, their current Python template already captures manifests, SHA-256, Git revision, freshness warnings, output previews and certificates; their R package already puts manuscript and reproduced figures side by side. Those features are not gaps. Only task/result linkage and structured failed-attempt evidence remain hypotheses. [S2–S3]
- **The strongest explicit, current, actionable ask is less glamorous:** Ouranos/PAVICS users report intermittent notebook integration failures because nbval's output timeout remains hardcoded to five seconds despite a configurable cell-execution timeout. An upstream fix is more credible immediate utility than a speculative app—and scarcely needs AI. [S12]
- **“It ran” really can miss a scientific result:** a released ReplicationBench GPT-5 trace prints `cold_sparam = 0.001223001128203661`, then submits “Task completed”; the benchmark's reference is **−0.00319 ± 0.001**. The numerical discrepancy is observable in existing artifacts, not a new reproduction. Crucially, that agent **did implement a port-swap function**: do not invent “it forgot to swap ports” as the diagnosis. [S17]
- **Not enough evidence to displace a quantum candidate today.** The CODECHECK inquiry below could change that if it yields a specific public artifact and an actual repeated manual step. Without that, choose an upstream contribution for real utility, or reject this lane for the hackathon: AI differentiation and quantum credibility are weaker. [INFERENCE]

## 1. Actual users and repeated work

### CODECHECK services at Amsterdam UMC and TU Delft

The funded project explicitly calls for a **structured template documenting issues encountered during each check**, then classification into dependency setup, unavailable components/data, code errors, missing code/output and manuscript/output mismatches. It intends to test whether readiness indicators predict successful reproduction. This is unusually useful evidence of a **live evidence-collection job**, not merely scientists saying reproducibility matters. [S1]

CODECHECK's October 2026 homepage describes the new project; its September register announcement reports 132 certificates and 66 codecheckers. TU Delft's DCC reports nine institutional checks and offers the service to researchers depositing software/data. The numbers establish repeated activity, not a software budget or a claim that checking is their main bottleneck. No per-check time/cost was established. [S1]

The workflow explicitly says **“Codecheckers record but don't investigate or fix”**, human communication is key, and workflows must be auditable. Therefore an agent that silently repairs code and awards a certificate would conflict with the intended workflow. Record an original failure separately from any author-approved repair; retain a human's scope and sign-off. [S1–S2]

### Ouranos users request a fix for notebook output timeouts

In open nbval **#231**, `@Zeitsperre` says their team uses `pytest --nbval` across notebooks in multiple projects on a computation platform, with sporadic successes/failures. They and colleague `@fmigneault` ask for configurable output waiting. The linked Ouranos PR **#171** adds a Jenkins cell-timeout parameter, but its discussion says this does not resolve the separate five-second output limit. Both were active in April 2026 and remain open on the read date. [S12]

The pinned nbval source confirms distinct paths: `nbval_cell_timeout` controls waiting on the shell reply; `self.output_timeout = 5` controls subsequent IOPub messages. This supports the reported configuration mismatch; it does not independently reproduce every intermittent PAVICS failure. [S12]

Historical requests for plot-object checks (#26, 2017; #137, 2020) and pre-run notebook comparison (#207, 2024) remain open, but **age plus open status is not proof of present demand**. Maintainer Thomas Kluyver said nbval only sees messages sent to the notebook, not Python plot objects; he pointed to plotchecker. Treat this as a possible upstream seam, not a current product mandate. [S13]

## 2. What existing tools already do

| Existing solution | What was actually established | Consequence for a weekend artifact |
|---|---|---|
| **Code Ocean** | Staff verify published capsules' mechanical reproducibility. Official checklist covers headless execution, saved results, packaged dependencies/data and source visibility. Explicitly: **they do not verify that capsule results match the paper**. Proprietary service; no pricing claim made. [S4] | Strong disconfirmation of “one-click execution” novelty; explicit boundary leaves manuscript/result comparison conceptually distinct, but does not prove demand for another vendor. |
| **Binder / repo2docker** | repo2docker builds executable environment images from repository configuration. mybinder.org is free, ephemeral, maximum 2 GB RAM, aiming for six hours or one CPU-hour; inactivity culling and no persistent storage. [S5] | Reuse infrastructure, do not rebuild it. Public Binder is not a reliable long-running audit backend or confidential-data service. |
| **ReproZip** | Captures necessary files, libraries, environment variables and options from a command-line execution into `.rpz`, with Docker/Vagrant/Singularity unpackers and local/HPC use. [S6] | Excellent packaging when a working execution is available; capturing an execution is not independent validation of its scientific interpretation. [INFERENCE] |
| **Renku** | Current research platform connects code/data/compute. July 14, 2026 release adds non-interactive jobs, custom private-repo environments and coding agents **Claude/Codex/Pi**, including their configuration folders. [S7] | “Research workspace with a coding agent” is already shipped. An evidence helper should run inside existing workflows, not require switching platforms. |
| **pixi** | Lockfile records exact resolved dependencies per environment/platform. `--locked` checks manifest consistency; `--frozen` uses the lock without updating it. Docs already suggest scheduled latest-dependency runs and lockfile diffs/issues. [S8] | Environment freeze/migration reports alone are crowded deterministic tooling. A lockfile does not certify numerical fidelity. [INFERENCE] |
| **SnifferDog** | Existing Python-notebook environment-restoration tool generates dependencies from notebook/script API use and an API bank. README says Python 3.7 and a limited library bank; no current success-rate claim adopted. [S9] | Environment reconstruction is not new; legacy constraints make it a comparison, not a recommended dependency. |
| **nbval / nbdime** | nbval compares saved notebook outputs with fresh outputs; lax mode compares only marked cells while checking execution. nbdime already provides notebook-structure-aware terminal/web diffs and rendered image differences. [S10] | Do not pitch ordinary notebook diffing, notebook execution or output previews as a new product. |
| **CODECHECK Python/R tools** | Existing Python template validates metadata/manifests, previews outputs, records sizes/mtime/SHA-256/Git revision, warns about unchanged tracked originals, renders PDFs and stages Zenodo deposits. R tool extracts manuscript figures and renders side-by-side comparisons. [S3] | The credible contribution must improve an identified missing step; another certificate/report generator is duplication. |
| **CORE-Agent / CORE-Bench** | Actual baseline agent and execution harness, not a concept. 90 reproducible Code Ocean papers × three difficulty levels. It checks answers extracted from executed outputs, **not paper/code agreement**; selection excludes intrinsically unreproducible artifacts. [S14] | Reuse evaluation lessons; do not confuse benchmark success with independent scientific validation. |
| **ReproAgent** | Four stages, persistent paper obligations, related-repository evidence, file-level contracts, provenance and targeted repair. Evaluated on 20 PaperBench Code-Dev papers; reported 73.7 mean with Sonnet 4.5, versus 73.5 for concurrent DeepCode. These are code-rubric scores, not “73.7% of papers scientifically reproduced.” [S15] | “Paper-to-code contracts with evidence” is already active research. A small helper needs practitioner integration, not an architectural novelty claim. |
| **ReplicationBench** | Author-developed numerical tasks and tolerances; executable Inspect-based agent evaluation; released task/trace artifacts. README invites new tasks and warns about guessed/copied answers. [S16] | A provenance/evidence extension can be a contribution to an existing benchmark, not another reproduction-agent startup. |

### What the three papers establish

Three papers were deep-read, including methods **and results setup**, not just abstracts:

1. **CORE-Bench v2:** selection includes local reproducibility, under-45-minute execution, under-10-GB capsules and low-variance labeled results; 45/45 train/test papers. Results use 2024 GPT-4o variants, a $4/task cap, three CORE-Agent trials and all-question accuracy, with prediction intervals derived from three manual runs. Hard accuracy 21.48% is **not a current 2026 frontier-agent baseline**. The older project site says 91 papers/273 tasks and 22%; prefer the versioned paper rather than mixing versions. [S14]
2. **ReplicationBench v2:** 20 papers/111 expert-written tasks; <6 hours on a four-core workstation **and one GPU allowed**; datasets pre-downloaded; tolerances supplied by authors. Numeric all-values correctness and paper-averaging are supplemented by expert trace review. Results table reports Sonnet 4.5 **22%**, although its abstract says under 20%; use the table and flag the inconsistency. Methods say three attempts while some table captions say average-of-six; do not overinterpret uncertainty. This is evidence of failure modes under that setup, not CPU feasibility for every paper. [S16]
3. **ReproAgent:** code-generation rubric evaluation, 20 targets, one run per paper/setting and fixed repair budgets; same-Gemini comparisons and channel ablations. Reported advantage does not establish independently repeated runtime result reproduction or an institutional customer's acceptance. [S15]

## 3. Three concrete variants

### A. Help CODECHECK reviewers record failed attempts

**User/job/input/output.** Institutional codechecker recording a check. Input: one allowlisted Python repo revision, author run command, existing `codecheck.yml`, captured logs/output directory and a human-selected result statement. Output: a **draft evidence bundle** mapping statement → output → producing command/run; numerical discrepancy where a reviewer supplies a reference and tolerance; structured failure category with verbatim log anchors; explicit partial/unobserved results. Keep unchanged author outputs distinct from generated outputs. No automatic certificate or scientific-validity verdict. [INFERENCE from S1–S3]

**Smallest complete 12-hour artifact.** An upstream helper to the existing Python notebook template that ingests **one recorded run**, emits machine-readable issue records and a reviewer-editable table, then includes the approved table in the existing report. Handle both successful output and a genuine failure; preserve unknowns rather than repairing them away. No arbitrary PDF ingestion, dependency-repair service, hosting platform or new certificate standard. The config v2.0 specification permits namespaced additional fields; request the maintainers' preferred schema before calling an extension accepted. [S2]

**Data/licence/compute.** `codecheck-py` is MIT, latest observed commit **2026-10-07**, `aaa3071…`; its own fixtures are small public software inputs. These can exercise metadata and failure-record capture on CPU, **not establish scientific usefulness**. A real paper/example with reviewer-approved expected output remains the missing deciding input. Budget inference: local file processing and a few bounded model calls; set a small API cap, report actual cost only after execution. No GPU needed for the helper; underlying papers may need more. [S3]

**AI contribution vs plain agent.** Suggest candidate result/output links and failure classifications from heterogeneous logs, with exact anchors and explicit uncertainty; deterministic code checks numbers, hashes and schema. A generic coding agent plus existing template may already do this adequately. Compare the same model, same files and same reviewer task; measure reviewer corrections, unsupported mappings and time spent—not prose quality. [INFERENCE]

**Cheap deciding experiment/adoption.** Keep the inquiry below as an unsent draft. Contact requires new user authorization. On one public check supplied by a reviewer, compare manual reporting with the proposed helper. Ask the reviewer to assess 3 to 5 result/output links and one failed attempt. Continue only if the reviewer identifies repeated work and prefers a concrete patch. Contribute to `codecheck-py` rather than creating a separate app. Reject this option if current tooling or the funded project's template already handles the task. **Current status: conditional, no user commitment.**

### B. Fix nbval's output timeout

**User/job/input/output.** Ouranos/PAVICS notebook CI users; reliably collect notebook output without an unrelated hardcoded five-second cutoff. Input: existing nbval execution and explicit output-wait setting; output: correct collection under that setting, with genuine timeout errors still visible. [S12]

**Smallest complete 12-hour artifact.** A focused nbval PR completing configurable output waiting, with clear distinction from cell-execution timeout, compatibility with existing options and a deterministic delayed-message regression fixture. Do **not** suppress failures, increase all timeouts silently or alter scientific comparisons. Existing `tests/test_timeouts.py` is the integration point visible in the repository tree. Maintainer review may dictate exact API. [S10, S12]

**Data/licence/compute.** nbval's actual licence text is BSD-3-Clause-style (do not rely on GitHub's “Other” label); latest commit **2025-09-17**, `3299cc6…`. Public tests/notebooks, CPU/local Jupyter kernel; no field dataset, proprietary data or LLM budget required. A fake/deterministic kernel message fixture is preferable to waiting several seconds in every test. [S10, S12]

**AI contribution.** Ordinary coding assistance, **not a necessary product feature**. This is the honest reason an upstream contribution may be better than an app. Cheap deciding experiment: ask in #231 whether the reported behavior still affects their current pipeline and whether a narrowly scoped PR would be used; review existing #156 first to avoid duplicating it. Adoption: nbval merge plus linked Ouranos PR update. Reject as hackathon pick if meaningful AI demonstration/quantum credibility is required; reject deployment claims until maintainers/users exercise it. No tests run here.

### C. Link an agent's numerical answer to its execution record

**User/job/input/output.** A ReplicationBench evaluator reviewing whether an agent's numerical answer comes from executed computation. Input: **one existing trace**, its task JSON and the final structured submission; output: exact answer/reference comparison, producing-command/output anchors, uncomputed/guessed/unsupported flags for human review. A numerical pass remains separate from methodological faithfulness. [S16–S17]

**Concrete smoke and metric a plain execution check misses.** Use `ls_cal/cold_sparam`: reference **−0.00319**, absolute tolerance **0.001**; existing GPT-5 trace's tool output is **+0.001223001128203661**. Difference is approximately **0.004413**, outside tolerance, despite the final “Task completed.” Show the task's requirement for corrected cold-load S-parameters, including swapped MTS measurement ports; show the trace's actual swap implementation too. The evidence demonstrates a numerical failure, **not its root cause**. The original REACH calibration paper was not deep-read and is not endorsed as independently reproduced. This is a benchmark-defined reference, not newly established physical ground truth. [S17]

**Smallest complete 12-hour artifact.** A trace-to-evidence report adapter for the existing evaluator, showing the failed numeric example and a documented matched case/explicit unknown; source the values from trace events rather than model prose. Do not build a new astrophysics agent. Most numeric grading already exists: contribution is connecting a grade to trustworthy execution evidence and reviewer-visible limitations. [INFERENCE]

**Data/licence/compute.** Released benchmark software, task JSON and software traces carry MIT repo licence; latest commit **2025-11-25**, `a87284c…`. Trace-only analysis is CPU and small relative to a new replication. A full `ls_cal` rerun is **not cleared**: the public ungated HF archive has no licence metadata/README in the inventory read, so public availability is not permission to redistribute it. Metadata says no GPU; 6,004,469 bytes `usedStorage` is an HF storage statistic, not a verified transfer-size total. No model/API required for numerical comparison; model-assisted evidence extraction is optional. [S16–S18]

**Cheap deciding experiment/adoption.** Christine Ye's repository invites contributions; compare a generic agent's evidence report with the deterministic numerical grade on one released trace and a second held-back trace. Measure correct command/result attribution and unsupported “reproduced” statements. Ask whether maintainers would take this as an Inspect/report adapter; there is **no public request specifically for it**. Reject if existing Inspect logs plus scorer already suffice—which is plausible—or if the whole demo is just reformatting an already-known failed score. Prefer contributing a useful task/evidence patch to claiming a new tool market. [S16]

## 4. Unsent inquiry draft

The official [Get Involved](https://codecheck.org.uk/get-involved/) page lists **team@cdchck.science** for the project leads and senior codecheckers. It invites developer contributions. Stephen Eglen and Daniel Nüst are suitable recipients through this address. [S19]

**Sending is not authorized.** This draft is a research artifact only.

Suggested subject: **Manual work in CODECHECK reports**

> Hello CODECHECK team,
>
> I saw that the new Amsterdam UMC/TU Delft project plans roughly 60 checks and records the problems found during each check.
>
> I'm a physics-trained research software developer exploring a small open-source contribution.
>
> Which step in recording a check still takes the most manual work with codecheck-py?
>
> Thank you,
> Severyn

An alternative public discussion is [nbval #231](https://github.com/computationalmodelling/nbval/issues/231), opened by `@Zeitsperre`, with input from `@fmigneault`. Their email addresses were not inferred. No contact is authorized.

## 5. Source register and limits

All accessed 2026-10-23. `full` means full indicated page/artifact, not all links or an entire repository. Failed URL guesses/403 API requests were not evidence; commit dates were recovered from GitHub's Atom feeds. No runtime feasibility was measured.

| ID | Primary source, source date, read depth |
|---|---|
| S1 | [CODECHECK indicators project](https://codecheck.org.uk/indicators/), project **Sep2026–Sep2028**, full; [homepage](https://codecheck.org.uk/), partial: principles and Oct/Sep/Aug2026 institutional news. |
| S2 | [Community workflow](https://codecheck.org.uk/guide/community-workflow-overview), undated, full; [config v2.0](https://codecheck.org.uk/spec/config/2.0/), **2026-09-11**, partial: manifest, metadata, extensions. |
| S3 | [codecheck-py README](https://github.com/codecheckers/codecheck-py), partial: quickstart, manifest freshness/previews, output handling; [MIT licence](https://raw.githubusercontent.com/codecheckers/codecheck-py/main/LICENSE), full; [latest commit feed](https://github.com/codecheckers/codecheck-py/commits/main.atom), latest **2026-10-07**. [R package](https://github.com/codecheckers/codecheck), full README; [figure-comparison source](https://raw.githubusercontent.com/codecheckers/codecheck/master/R/figure_comparison.R), partial: API/documentation for PDF extraction and side-by-side figures. |
| S4 | [Code Ocean verification checklist](https://docs.codeocean.com/osl-guide/publishing-on-code-ocean/the-verification-process/code-oceans-verification-process-for-computational-reproducibility-and-quality), undated, full. |
| S5 | [repo2docker docs](https://repo2docker.readthedocs.io/en/latest/), undated, full overview; [Binder usage](https://mybinder.readthedocs.io/en/latest/about/user-guidelines.html), undated, partial: resources, lifetime, privacy/security. |
| S6 | [ReproZip](https://www.reprozip.org/), undated, full landing page. Capabilities are maintainer descriptions, not exercised here. |
| S7 | [Renku user docs](https://docs.renkulab.io/en/stable/docs/users/), undated/current Sep2026 links, full; [July release](https://blog.renkulab.io/release-2026-07/), **2026-07-14**, full. No legacy provenance-graph feature assumed to persist into current Renku. |
| S8 | [pixi lockfile](https://pixi.prefix.dev/latest/workspace/lock_file/), undated, partial: exact dependencies, platform resolution, frozen/locked, library CI recommendations. |
| S9 | [SnifferDog repository](https://github.com/SMAT-Lab/SnifferDog), undated README, full. Associated 2021 paper **not read**; no paper efficacy figure used. Not proposed for reuse. |
| S10 | [nbval repo](https://github.com/computationalmodelling/nbval), full README/tree; [licence](https://raw.githubusercontent.com/computationalmodelling/nbval/master/LICENSE), full; [commit feed](https://github.com/computationalmodelling/nbval/commits/master.atom), latest **2025-09-17**. [nbdime docs](https://nbdime.readthedocs.io/en/latest/), undated, full overview. |
| S11 | [ReproAgent repository](https://github.com/kernel-14/ReproAgent), undated README, full README and source-tree listing. The repository exists and declares MIT. Source files include the four pipeline stages and provenance helpers. The implementation was not executed or audited. |
| S12 | [nbval #231](https://github.com/computationalmodelling/nbval/issues/231), **2026-04-28**, full body/current open state; [Ouranos PR #171](https://github.com/Ouranosinc/PAVICS-e2e-workflow-tests/pull/171), **2026-04-24–28**, full body/comment; [pinned plugin source](https://raw.githubusercontent.com/computationalmodelling/nbval/3299cc6c70b31f4955b3893f4e082adab6b0e253/nbval/plugin.py), **2025-09-17 revision**, partial: lines350–390/590–642. |
| S13 | [#26](https://github.com/computationalmodelling/nbval/issues/26), **2017-01-17, stale**, full; [#137 maintainer reply](https://github.com/computationalmodelling/nbval/issues/137#issuecomment-583849086), **2020-02-09, stale**, full; [#207](https://github.com/computationalmodelling/nbval/issues/207), **2024-06-26, stale**, full. |
| S14 | [CORE-Bench v2](https://arxiv.org/html/2409.11363v2), **2026-06-22 revision** of 2024 work, partial: §§1–4, selection/methods/evaluation/results; [project site](https://crab.cs.princeton.edu/core-website/), undated, full. No current frontier performance extrapolated. |
| S15 | [ReproAgent v1](https://arxiv.org/html/2608.24291v1), **2026-08-25**, partial: §§1–7, methods, setup, result tables, ablations and limitations. |
| S16 | [ReplicationBench v2](https://arxiv.org/html/2510.24591v2), **2025-11-23**, partial: §§1–7 incl selection, compute, setup, numeric tolerances, results, failure modes/limitations; [repo README](https://github.com/Christine8888/replicationbench-release), full; [PR instructions](https://raw.githubusercontent.com/Christine8888/replicationbench-release/main/PR_INSTRUCTIONS.md), full; [MIT licence](https://raw.githubusercontent.com/Christine8888/replicationbench-release/main/LICENSE), full; [commit feed](https://github.com/Christine8888/replicationbench-release/commits/main.atom), latest **2025-11-25**. |
| S17 | [cold_sparam task JSON](https://raw.githubusercontent.com/Christine8888/replicationbench-release/main/src/dataset/tasks/ls_cal/cold_sparam.json), repository revision **2025-11-25**, full; [GPT-5 ls_cal trace](https://raw.githubusercontent.com/Christine8888/replicationbench-release/main/logs/text-format/gpt5-base-1/ls_cal.out), released **2025-11-25**, partial: instructions, port-swap implementation, final executed output/submission/score; task error cause not diagnosed. |
| S18 | [ls_cal metadata](https://raw.githubusercontent.com/Christine8888/replicationbench-release/main/src/dataset/papers/ls_cal.json), full; [HF dataset API](https://huggingface.co/api/datasets/ChristineYe8/ls_cal), lastModified **2025-11-16**, full metadata/inventory; [HF tree](https://huggingface.co/api/datasets/ChristineYe8/ls_cal/tree/main?recursive=true&expand=false), partial file inventory/sizes. Raw dataset licence unverified. |
| S19 | [CODECHECK Get Involved](https://codecheck.org.uk/get-involved/), undated, full; official public email and invitation for developer contributions. |

**Decision boundary:** A is a live-workflow hypothesis worth one factual inquiry, B is concrete useful upstream work with weak AI-product value, C is a verifiable research demonstration whose adoption need is unproven. None is presently a validated stand-alone business, and none should be sold as verification of scientific truth.
