# Build North submission copy

Paste each section into the matching form field. Replace `VIDEO_URL` once the video is uploaded. Everything here was observed in this repository. Do not add numbers that were not measured.

## Project name

QRef: review AI-ported quantum code before you trust it

## Tagline (one line)

Claude ports old Qiskit code. QRef runs both versions and shows what actually changed. A human makes the call.

## Links

- Live demo: https://seivenbell.github.io/tq-ledger/ (all examples: https://seivenbell.github.io/tq-ledger/examples.html)
- Code: https://github.com/SeivenBell/tq-ledger
- Video: VIDEO_URL

## Inspiration

Quantum software moves fast. Code written for Qiskit 0.46 no longer runs on Qiskit 2.x, so a lot of research and teaching code needs porting. Coding agents can port it in seconds, but nobody can review it that fast.

The usual check is to compare the circuits. That is not enough. We ported the Qiskit textbook QAOA helpers and all nine checked circuit pairs were equivalent. The experiment still differed: the old code silently ran 1,024 shots whether you asked for 512 or 17. A circuit check cannot see that.

## What it does

QRef is a command-line tool with a static report.

1. `qref propose` asks Claude, through the user's existing Claude subscription with tools disabled, for a port. It saves the code, prompt and the model's stated changes. It never runs the code.
2. `qref run` runs the old and new code, each in its own pinned Python environment. It records the circuits actually submitted to the Aer simulator and compares them with MQT QCEC. It also checks the classical helpers on every bit pattern, checks each returned value against its own measured counts, and compares requested and completed shots.
3. The report puts the finding first. The model's claims, the observed evidence and the human decision appear in separate places. Gaps and unchecked areas are listed, not hidden.
4. `qref report --decisions` records a named human decision, bound to the exact evidence by SHA-256. It changes the review state, never the check results.
5. `qref verify-bundle` checks every published file and every member of the downloadable ZIP against the manifest, without extracting anything.

Five recorded examples are live:

- A fresh Claude port that keeps the old 1,024-shot behaviour.
- An earlier port that honours the requested shots.
- A labelled, deliberately broken bit-order version. The circuit checker still calls it equivalent; QRef's classical checks catch it.
- A labelled halved-rotation version. Here the circuits really differ, and MQT QCEC reports it.
- A positive control: the same port on both sides, including an 8-qubit graph. No differences, so QRef does not invent findings.

## How we built it

Python 3.11 and uv. Two pinned interpreters, Qiskit 0.46.3 with Aer 0.14.2 and Qiskit 2.6.1 with Aer 0.18.0, run a small standalone worker. That worker hooks `AerBackend.run` before the candidate module is imported, so QRef records the circuit that was really executed, not a rebuilt one.

MQT QCEC 3.11 checks circuit equivalence. Jinja2 renders the report and jsonschema validates every record. The report is self-contained HTML that works without JavaScript. It carries a strict Content-Security-Policy that allows exactly one hash-pinned script, which only saves the embedded evidence record.

GitHub Actions re-verifies the curated exports byte for byte, then publishes only those files to GitHub Pages; that publish job never runs candidate code or calls a model. A separate Linux job rebuilds both pinned Qiskit environments from scratch on every push, runs all tests and repeats a real seed run.

## Challenges we ran into

- Capturing the real execution, not a reconstruction. Our first research prototype rebuilt the circuit separately, which is the wrong evidence.
- QCEC's Python docstrings describe its two phase results the wrong way round. We checked the C++ source and ran small tests before mapping them.
- Keeping claims honest. The same prompt to Claude produced different choices: in four calls it fixed the shot handling twice and kept the old behaviour twice. Both are reasonable. That is exactly why QRef shows the model's stated intent next to the observed evidence and leaves the decision to a person.

## Accomplishments we're proud of

- A real end-to-end flow: model proposal, two-runtime execution, independent checks, human decision, verified public report.
- One documented example where the circuit check passes and QRef still catches the behaviour change.
- 48 behaviour tests cover status rules, unsupported circuits (changed measurement maps, control flow, extra simulator runs), import failures, timeouts, checker budgets, missing interpreters, refused billing overrides, unusable model output, tampering (including a swapped ZIP), hostile input escaping, stale model attribution and invalid decisions.

## What we learned

"Equivalent circuits" and "the same experiment" are different claims. The useful product is the evidence trail and the review step around existing tools, not a new equivalence checker.

## What's next

- More migration patterns beyond these QAOA helpers.
- A wider set of failure fixtures.
- Trying it with people who maintain quantum teaching or research code.

We have no users yet and no measured time savings. That is the next thing to test.

## Built with

python, qiskit, qiskit-aer, mqt-qcec, claude, claude-code, jinja2, jsonschema, uv, github-actions, github-pages

## Partner platforms used

None. We use Anthropic's Claude through an existing Claude subscription. No sponsor or partner integration was added.

## Security and ethics

- Candidate code is Python and runs with your local permissions. QRef requires an explicit `--trust-local-code` flag and says so. Separate environments isolate versions, not hostile code.
- The model call has tools disabled and runs in an empty temporary directory, with a clean environment and a check that the login is a first-party claude.ai subscription. No API keys are stored. Session IDs are removed from saved responses.
- The public site is static: no uploads, no execution, no accounts, no tracking.
- Hashes show that files are internally consistent. They are not a signature or a certification, and the report says so.
- The seeded regression is labelled on the page as a deliberate test, not a model mistake.

## Prior work and AI disclosure

- Work done during Build North week, October 2026, in this repository. Earlier in the week the repository held research on other project ideas; that research is archived under `archive/research-2026-10/`. The QAOA research probe in `evidence/qaoa/` was built during the week and is reused as test input.
- Reference code comes from the Qiskit textbook (Apache-2.0); attribution and the licence are included in every report.
- AI tools: Claude (Claude Code) helped research, plan, write code and write documentation under my direction. Claude Sonnet is part of the product: it generates the proposed ports. All reported results come from real runs recorded in the repository.
