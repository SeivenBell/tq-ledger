# Demo video script (2:00 or less)

Round 1 judging (Oct 26) happens without you: judges watch this video, read the Devpost page, and click the live link (`docs/research/build/judge-panel.md`). The video is the pitch.

**Recording rules**: record the deployed app, not localhost, with the address bar visible; 1280×720; pre-warm the service; demo data frozen with a visible date badge; no jargon in narration (jargon lives in the UI tooltips). Fill every `[RESULT]` with the real number from `data/eval/results.json`; never round up.

| Time | Screen | Narration (about 250 words total) |
|---|---|---|
| 0:00–0:15 | Home page: the "numbers in circulation disagree" strip | "Every few weeks someone says breaking Bitcoin or RSA got cheaper: one million qubits, twenty-six thousand, eleven hundred, eight hundred ninety-three. Last week a co-author of a new circuit said it cuts the hardware needed by a quarter. The paper never measured hardware." |
| 0:15–0:25 | Same page, scroll to the ledger table | "Banks are being told to monitor these breakthroughs and adjust their migration timelines. Today an analyst does that by hand. Q-Day Ledger turns each claim into a cited card, and refuses to compare numbers that measure different things." |
| 0:25–0:50 | Headline check: paste the 25 % sentence → verdict "not comparable"; gates turn red; click "893" → quote panel highlights the sentence with the arXiv link | "Here's that claim. Three gates fail: the paper counts logical qubits, not physical ones; for one step of the attack, not the whole attack; with an easier kind of input. Every number opens the exact sentence it came from." |
| 0:50–1:05 | Compare page: ECDSA.Fail coherent variant vs Google's bound → "comparable with caveat: 34.5 % below Google's upper bound" | "It doesn't just say no. When two claims can be compared, it does the comparison and says how far it goes: a headline said fifty percent; like for like, it's thirty-four and a half, against an upper bound." |
| 1:05–1:20 | Card EF-893: failure statistics box | "It also recomputes what it can. This circuit failed 111 times in 360,960 tests. Its whole confidence interval sits above the failure budget another benchmark requires. That assumes independent trials; it's a flag, not a verdict." |
| 1:20–1:40 | Reviewer page: enter a held-out arXiv ID → draft card appears; one field marked "rejected: quote not found"; approve the rest | "Adding a new paper: the model drafts every field with a quote. Code checks that each quote really is in the paper and that the number is in the quote. This one wasn't, so it's rejected, not published. A person approves the rest." |
| 1:40–1:52 | Eval page | "On three papers held out from development, [RESULT] of numeric fields came out right and no unsupported number was published. A plain chatbot got [RESULT] of fourteen comparisons wrong." |
| 1:52–2:00 | Method page: one-line architecture + "what we do not do" + URL | "The model proposes, code verifies, a human approves. Public claims only, no new attack estimates. Built for the people planning post-quantum migration." |

## Fallbacks

- If the live extraction is slow, cut from "submit" to the finished draft, and say "about a minute later". Do not fake the result: the rules ban faking a demo.
- If the headline check is cut (PLAN cut order), use the compare page for 0:25–0:50 with preset pair 14.
- If held-out accuracy is poor, say the real number and show the rejected fields; the verifier stopping bad numbers is the point.

## Live-round version (Oct 29, top 10)

Same flow, plus 15 seconds on any reply from the people in `docs/build/OUTREACH.md`, and 20-second answers rehearsed for: "Who pays?" (Wu), "Show me the model failing" (Mihailescu), "Cost per run and security model?" (Coupez), "Eval size, labelling, dual use?" (Pandya).
