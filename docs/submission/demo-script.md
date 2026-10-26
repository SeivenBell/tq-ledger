# Demo recording: 2 minutes

Record your real screen. Every command runs for real. You may cut dead time while Claude is answering, but do not speed up or replace any output. The Build North rules ban faked demos.

## Before you press record (5 min)

1. Terminal: font about 18 pt, repository root, then `clear`. Close any windows that show email, tokens or other private data.
2. Browser tab 1: https://seivenbell.github.io/tq-ledger/seeded-decoder/. Scroll to the top.
3. Browser tab 2: https://seivenbell.github.io/tq-ledger/examples.html
4. Run `claude auth status` off camera. If it does not show `claude.ai`, use the fallback at the end.
5. Decide your human decision now. Use `accepted_intentional` if Claude fixes the shot count and you agree. Use `needs_review` if you are not sure.
6. Start recording. Then run `scripts/demo.sh` and press Enter to move through the five steps.

Claude chooses differently from run to run. In our four calls it fixed the shot count twice and kept the old behaviour twice. The script below covers both outcomes. Say what is actually on screen.

## Script

| Time | Screen | Say |
|---|---|---|
| 0:00–0:12 | Terminal, step 1 prompt | "AI can port old quantum code in seconds. The hard part is knowing whether the experiment still does the same thing. Equivalent circuits do not tell you that. QRef does." |
| 0:12–0:30 | Step 1: `qref propose` runs (cut the wait) | "I ask Claude, through my normal subscription with no tools, to port a Qiskit textbook QAOA helper from Qiskit 0.46 to 2.6. QRef saves the code, the prompt and the model's own notes. It does not run anything yet." |
| 0:30–0:40 | The model's "Intentional changes" list | *If it fixed shots:* "Claude says the old code ignored the shot count, and it fixed that." *If it kept them:* "Claude says it kept the old shot behaviour on purpose." "That is the model's claim. Now let's check it." |
| 0:40–0:52 | Step 2: `qref run`, its terminal summary and exit code 1 | "QRef runs each version in its own pinned Qiskit. It captures the circuits actually sent to the simulator and checks them with MQT QCEC, plus independent classical checks." Point at the summary lines: circuits equivalent, then the finding. |
| 0:52–1:15 | Step 3: the report, top of page | "The circuits are equivalent: nine of nine pairs. But look at the shot table." Point at the numbers. *Fixed:* "The old code always ran 1,024 shots. The new code runs the 512 or 17 you asked for, so the statistics change." *Kept:* "Both run 1,024 no matter what you ask for, so the old bug is carried forward." "The model's statement and the observed evidence are shown separately, and the human decision is still empty." |
| 1:15–1:35 | Browser tab 1: seeded regression | "Here I broke the code on purpose and labelled it as a test. I flipped the bit order when reading results. The circuit checker still says equivalent, because the circuit didn't change. QRef catches it anyway: the classical helper no longer matches the declared MaxCut rule." *If you have 5 spare seconds, open `/seeded-rotation/`:* "Halve one rotation instead, and the circuit checker does catch it. You need both layers." |
| 1:35–1:50 | Step 4: type decision and reason, then the reviewed report | "The decision is mine, not the model's. It is bound to this exact evidence by hash, and it changes the review state, never the check results." |
| 1:50–2:00 | Step 5: verify-bundle output, then browser tab 2 | "Anyone can verify the export and its ZIP against the manifest. A clean control shows no differences, so QRef doesn't invent findings. CI rebuilds both Qiskit versions on Linux on every push. The site is static: no backend, no keys." |

About 260 spoken words. If you run long, cut the 0:30–0:40 line to a single sentence.

## Fallback if `propose` fails on camera

Use what is already recorded. Do not pretend it is live.

1. Say: "This is a recorded proposal from earlier tonight."
2. Run `cat examples/qaoa-proposal/notes.md`.
3. Then run `uv run qref run --case examples/qaoa-proposal/case.json --reference-python .qref/envs/reference/bin/python --target-python .qref/envs/target/bin/python --out runs/demo-fallback --trust-local-code`.
4. Open `runs/demo-fallback/index.html` and continue from 0:52.

## After recording

Upload the video (YouTube unlisted is fine). Paste the link into the form. Run `rm -rf runs/demo-*` if you do not want the local runs kept. They are git-ignored either way.
