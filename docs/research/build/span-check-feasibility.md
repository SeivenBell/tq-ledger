# Span-check feasibility on real papers (2026-10-23)

Question: can the ledger's core promise ("every number tied to a verbatim quote, checked by code") work on the actual source texts? Test: take every quote in the two corpus files and look for it in freshly extracted text of the source paper.

## Method

- Sources: arXiv PDF converted with `pdftotext` (no layout flag), and arXiv HTML stripped of tags (MathML annotations removed), when HTML exists.
- Normalisation: Unicode NFKC; curly quotes and dashes unified; soft hyphens removed; line-break hyphenation joined; whitespace collapsed.
- Quotes containing an ellipsis were split and each part checked.
- **Exact**: normalised quote is a substring of the normalised text.
- **Fuzzy**: a window around the quote's longest digit token reaches ≥ 0.85 character-level similarity (difflib) **and** every digit of the quote appears in the window in the same order.
- Script: run in the session kernel; quote extraction from the 2026 file used a crude regex over table cells, so some of its "quotes" are not real quotes (see misses).

## Results

| Corpus | Quotes | Exact | Fuzzy | Miss | Matched |
|---|---|---|---|---|---|
| Classic (6 papers, 2017–2025) | 75 | 65 | 2 | 8 | 89 % |
| 2026 paper cards (5 papers) | 71 | 27 | 14 | 30 | 58 % (lower bound; extraction artefacts inflate misses) |

## What fails, and why

1. **Table rows.** Quotes copied from `pdftotext -layout` tables ("256 2330 1.26 · 1011 1.16 · 1011 3 848") do not match non-layout text because column order and spacing change.
2. **Formulas.** Unicode math typed by the corpus agent (`5n + 4⌊log₂n⌋ + O(1)`, `976n³`) does not match the PDF's flattened text (`5n + 4blog2 nc`, `976n3`).
3. **Flattened superscripts.** `pdftotext` turns 1.26·10¹¹ into "1.26 · 1011" and 2³⁰ into "230". A naive number parser would read 1011 and 230.
4. **Misattributed quotes.** "Luo et al.'s recent 835-qubit result" appears in the ECDSA.Fail paper, not in Luo's paper. The check correctly fails it, which matches the corpus note that the 835 figure is not in Luo's paper.
5. **Paraphrase drift.** A few prose quotes were lightly edited by the corpus agents.

## Design changes adopted (ARCHITECTURE §4 and §6, tickets T1, T2, T6)

1. **One canonical text per source**: `pdftotext` output (or HTML text for sources that have clean HTML), normalised as above; store its sha256. The extractor receives exactly this text and must quote from it, so model quotes and the verifier see the same characters.
2. **Tiered span check**: exact, then fuzzy (digits must match in order), then miss. The card shows the tier; for fuzzy matches, the card stores and displays the source's own text, not the model's.
3. **Table values** use a table locator (table id, row label, column) and are verified against `pdftotext -layout` output: the row label and the value token must appear on the same line.
4. **Number parser** recognises flattened exponents (`m · 10dd` → m × 10^dd, `2 dd` after a "·" → 2^dd) and marks ambiguous cases for review.
5. **T1 re-anchors every corpus quote** against canonical text: replace each quote with the matched canonical span; list misses for Severyn. Expect roughly 10 to 40 % of quotes to need a quick manual fix, mostly table rows and formulas.

## Licences verified on the arXiv abstract pages (2026-10-23)

| arXiv | Card | Licence |
|---|---|---|
| 1706.06752 | RNSL17 | arXiv non-exclusive 1.0 |
| 1905.09749 | GE19 | CC BY 4.0 |
| 2001.09580 | HJNRS20 | arXiv non-exclusive 1.0 |
| 2108.12371 | WEB22 | arXiv non-exclusive 1.0 |
| 2306.08585 | LIT23 | arXiv non-exclusive 1.0 |
| 2505.15917 | G25 | CC BY 4.0 |
| 2603.28846 | GOOG-ZK | CC BY 4.0 |
| 2604.02311 | LUO | arXiv non-exclusive 1.0 |
| 2606.02235 | SCHR | CC BY 4.0 |
| 2609.09582 | EF-BENCH | CC BY 4.0 |
| 2610.22367 | GU-DIV | CC BY-NC-SA 4.0 |

All match the corpus files. The held-out eval papers (G25, SCHR, GOOG-ZK) are CC BY 4.0, so their canonical text can be committed for a reproducible eval. Non-exclusive papers: short attributed quotes and offsets only; canonical text cached locally, not committed.
