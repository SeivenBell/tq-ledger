# Q-Day Ledger: build plan (Oct 23 to Oct 25)

Submission: Devpost, **Oct 25, 11:59 PM ET**. Aim to submit by **8:00 PM** Sunday for buffer. Online judging Oct 26; top 10 demo live in Toronto Oct 29.

Time available (from `memory/working-rhythm.md`): Friday evening is a gym evening (light tasks only); Saturday is the main block; Sunday is the finish. Roughly 10 to 12 focused hours, plus parallel coding agents.

## Who does what

- **Severyn**: decisions, card review (the gold data), outreach, prompt and verdict judgement, video, Devpost page. Severyn's review time is the scarcest resource; tickets are shaped to protect it.
- **Coding agents** (Claude Code, local or cloud): implementation tickets T1 to T12, each self-contained with acceptance tests. Cloud sessions need the Claude GitHub App installed on `SeivenBell/tq-ledger` so they can push.

## Friday evening (light, about 45 minutes)

| # | Task | Done when |
|---|---|---|
| F1 | Make the decision on [Choose the project to build](https://github.com/SeivenBell/tq-ledger/issues/14) (pick, ethics framing, outreach, practitioner-pain handling) | Ticket closed with the answers |
| F2 | Install the Claude GitHub App on the repo; claim Render credits; redeem `BUILDNORTH50` at studio.surrealdb.com; create a Clerk app (optional) | Accounts ready |
| F3 | Send the outreach messages in `docs/build/OUTREACH.md` (Ivezic, Anant, Long, Dallaire-Demers, evolutionQ) | Sent; log replies in the issue |
| F4 | Kick off T1, T2, T3 as agent sessions overnight | Branches pushed |

## Saturday (main block)

| Time | Severyn | Agents |
|---|---|---|
| Morning, 2 h | Review seed cards (`data/cards/` drafted by T1 from the corpus files): approve, fix, or reject each field. Freeze gold (`data/eval/gold/`) and pairs labels | T2 verifier and T3 compare engine land with tests; T4 web skeleton |
| Midday, 2 h | Check verdicts on all labelled pairs; tune wording of verdict sentences | T5 card page with quote panel; T6 extraction pipeline on dev papers |
| Afternoon, 2 h | Iterate the extraction prompt on dev papers only; then run held-out once | T7 eval harness and baseline; T8 deploy to Render |
| Evening, 1 to 2 h | Smoke test the live URL; read every card page as a judge would | T9 headline check (if core is green) |

**Saturday exit gate**: live URL serving ledger, card pages, compare page; `make verify` green; held-out eval numbers exist. If not, Sunday is fixes only (no Should items).

## Sunday (finish)

| Time | Task |
|---|---|
| Morning, 2 h | Should items in order, only if the gate passed: T10 Clerk review flow, T11 SurrealDB memory. Otherwise polish |
| Midday, 1 h | Freeze demo data; date badge; final `make verify`; check the live link from another network |
| Afternoon, 1.5 h | Record the video against the live URL (`docs/build/DEMO.md`); edit to 2:00 or less |
| Late afternoon, 1 h | Devpost page from `docs/build/DEVPOST.md`; disclosures; submit by 8 PM |

## Implementation tickets

Full text lives as GitHub issues labelled `build`. Summary and dependencies:

| Ticket | Scope | Depends on | Size |
|---|---|---|---|
| T1 Seed cards | `ledger/schema.py` + `data/sources/` + `data/cards/` drafted from `docs/research/build/claims-classic.md` and `claims-2026.md` (status `machine_extracted`, quotes copied verbatim) | none | M |
| T2 Verifier | `ledger/verify.py`: span check, number parser, recompute registry, Clopper–Pearson, budget check; `tests/test_verify.py` with the worked numbers in ARCHITECTURE §4 | T1 schema | M |
| T3 Compare engine | `ledger/compare.py` gates G1 to G9; `data/eval/pairs.json` (≥ 12 labelled pairs written first); `tests/test_compare.py` | T1 | M |
| T4 Web skeleton | FastAPI app, layout, ledger table with filters, method page, "what we do not do" | T1 | M |
| T5 Card and compare pages | Card page with clickable numbers and quote panel; trust badges; compare page with gate table and verdict sentence | T2, T3, T4 | M |
| T6 Extraction | `ledger/sources.py` (arXiv HTML to text, sha256, licence) + `ledger/extract.py` (`messages.parse`) + `scripts/extract_card.py`; drafts with per-field status | T1, T2 | M |
| T7 Eval | `scripts/run_eval.py`: held-out field accuracy, quote validity, unsupported-number rates; baseline on comparison questions; `data/eval/results.json`; eval page | T3, T6 | M |
| T8 Deploy | `render.yaml`, env vars, rate limit, spend cap, health check; README with diagram | T4 | S |
| T9 Headline check | `ledger/headline.py` + page; alias table; confirmation step | T3, T5 | S |
| T10 Clerk reviewer flow | Sign-in; approve/reject fields; record `user_id` | T5, T6 | S |
| T11 SurrealDB memory | Remember source → claim → assumption triples on approval; recall prior conventions before extraction; "current best per comparable class" view | T6 | M |
| T12 CI | GitHub Action: `make verify` and `make test` on push; badge | T2, T3 | S |

## Cut order (drop from the top when behind)

1. T11 SurrealDB memory
2. T10 Clerk (keep a single admin token for the reviewer page instead)
3. T9 headline check (demo the same point through the compare page)
4. Live extraction in the video (show a recorded run and its log instead; keep the extractor in the repo)
5. RSA cards (keep ECC only)

**Never cut**: cited cards, the span and number checks, the refusal to compare unlike quantities, one recompute check, the eval with real numbers, the live link.

## Definition of done (submission)

- [ ] Live URL serves ledger, card pages, compare page without login
- [ ] ≥ 8 human-reviewed cards; `make verify` green
- [ ] ≥ 12 labelled pairs, engine matches all
- [ ] Held-out eval and baseline numbers on the eval page, with failures listed
- [ ] README: what it is, how it works, diagram, how to verify, limits, licences, disclosure of prior work and AI tools
- [ ] Video ≤ 2:00, recorded against the live URL
- [ ] Devpost page complete; submitted
