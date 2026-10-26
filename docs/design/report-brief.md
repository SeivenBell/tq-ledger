# QRef report surface

Status: proposed design for specification review. No product UI has been built or approved. This is a precise brief for the implementer after review, not a screenshot of working software.

## Job and direction

The surface is one recorded migration report. Its primary mode is **Read**, with small evidence/export interactions. The reader wants to know what stayed the same, what changed and what still needs a decision.

Use a **finding-first patch review document**: the clarity of a code review, but with the experiment-level finding before the diff. A quiet continuous document, exact comparisons and linked evidence are the identity. No marketing hero, dashboard shell, metric-card grid, sidebar of invented projects or fake activity.

This direction was compared with an annotated journal proof, a build-artifact sheet and a numerical worksheet. The patch-review structure best connects a finding to an observation and then the changed source. A journal-like identity risks implying peer review; a CI pipeline risks implying live jobs; a graphics-led worksheet can make a tiny case set look statistically authoritative. Their useful disciplines remain: adjacent attribution, explicit stage status and aligned values—not borrowed decoration.

The material-world exploration also considered foreign visual systems. They did not improve this developer/research task. Preserve their useful disciplines only: make excluded material reachable, distinguish conflict without color, attribute every claim, align repeated values, expose detail by depth and provide ordered reproduction steps. Do not import cinema rails, stamps, moving sheets, ocean imagery or wordless assembly metaphors.

The product truth is distinctive enough: **equivalent circuits can accompany a changed experiment**. Show it rather than decorating the word quantum.

## First viewport

The [browser-rendered schematic](report-layout.png) illustrates layout, not an approved visual comp or implemented product. Its [SVG source](report-layout.svg) is retained. The PNG avoids theme-variable limitations in some standalone SVG raster previews.

At desktop width, use a centered report area around 1,160 CSS pixels. First-screen order:

1. Small identity: `QRef / Migration report`; useful export links on the right.
2. `Recorded local execution`, actual run identity and execution time. If time is unavailable, say not recorded.
3. Case title: `QAOA helpers: Qiskit 0.46.3 to 2.6.1`.
4. Main finding: `Equivalent circuits. A changed shot setting.`
5. Two-row comparison with requested, reference-completed and target-completed shots.
6. Plain explanation of the model's prior disclosure and sampling uncertainty.
7. Human state and coverage/unchecked scope in the same reading region—not hidden in a footer.
8. Native section links into the detailed report.

The shot table is the main visual object. Do not repeat its numbers in a chart or giant KPI tiles.

| Requested shots | Reference completed | Target completed |
|---|---:|---:|
| 512 | 1,024 | 512 |
| 17 | 1,024 | 17 |

Caption: `One sampling-setting change observed across 18 executions per runtime.`

Meaning: `The target honors the requested shot count. This changes sampling uncertainty. In the fresh probe, the prompt requested the correction and the model documented it before execution.` Model intent is evidence of following that instruction, not autonomous issue discovery.

Human state: `Human decision: not recorded`, unless an applicable real overlay exists.

Coverage: `3 graphs, 3 angle settings, 2 shot requests. Checks cover declared inputs only.`

Visible limit: `Not checked: optimizer convergence, hardware, noise and dynamic circuits.`

These are seed-example labels. The renderer derives other summaries from actual evidence; it must not reuse this headline for an incomplete run, a circuit difference or identical programs that both ignore requested shots.

## Document anatomy

### Findings

Lead with each grouped finding and its exact affected scope. For the seed, one `Shot setting` finding contains all linked observations. A repeated difference is not 18 independent bugs.

Within a finding, order material as **Execution evidence → Model disclosure → Human decision**. Attribution stays beside the text. A model's stated intention is not human approval; a human decision cannot alter an observed check result.

Use the normative SPEC mapping: `Not recorded` for absent/all-null template decisions, `Needs review` for an actual recorded needs-review decision, `Accepted as intentional` and `Change rejected` for those recorded outcomes. Complete clean evidence has `Human review: not required`; incomplete evidence remains pending even with accepted differences. Integrity/error diagnostics are not accept-intent findings. Do not use `Certified`, `Approved by QRef`, `Safe` or a universal `Passed` badge.

The browser does not edit/save decisions. It shows a recorded decision and its reason. Explain that changing the local decision input and regenerating produces a new export. Do not include a non-persistent approval toggle.

### Checks on declared inputs

Show graph/angle cases, actual unique circuit results and links to every covered requested-shot execution. Columns: Graph; Angles; Circuit result; Maximum probability difference; Exact objective difference; Evidence.

Use actual values and tolerance. Compact scientific notation is allowed when the exact value is still available in details. Explain beta-first/gamma-second angle order. Graph details contain nodes and edges, not only an illustration.

Label sampled objectives separately from exact objectives. Different sampled values are not automatically a defect, and matching samples do not prove circuit equivalence.

### Coverage and limits

Separate `Checked`, `Not checked` and `Unsupported`. Show the expected inventory and missing IDs when work is partial. Say `All declared cases completed` only when the record establishes it. Never say complete coverage.

An inconclusive result has a method/reason beside it. Keep known differences visible even when the overall evidence is incomplete. Do not hide uncertainty behind a successful circuit result.

### Source changes

Start at the shot hunk because it explains the finding. Use a unified diff with literal `+`/`-` and Added/Removed labels; color is supplementary. Show real file names and line numbers. Offer complete bundled reference/target source and license text.

Native disclosures can hold less relevant hunks. Mark omissions honestly. Do not show an invented excerpt as the exact complete patch. Model notes remain available verbatim with attribution and original uncertainty.

### Evidence and reproduction

Show immutable source identity, extraction scope, actual dependency/interpreter versions, case inputs, implementation hashes, checker method, record identity and limitations. Hash text can be shortened initially, but the complete value must remain selectable.

Keep proposal time, execution time, decision time and render time distinct. Do not use relative `just now`, file modification times, fake timers, a blinking dot or `live` status.

Plain copy: `This page shows recorded results. It does not run a model or execute Python.`

Local reproduction commands remain selectable even if a copy button exists. State that the local workflow does not sandbox code. External source links are labelled as online; all report facts and source excerpts work offline.

## Controls and export

Required: skip link, native section anchors, exact observation/check links, native disclosures, full-source/license access, HTML save/download, exact JSON export and visible reproduction commands.

No-script reading must retain all core facts and raw evidence. Scripted JSON export uses exact embedded evidence text, not a rewritten object. Native HTML download or browser Save As is a fallback; do not promise an altered browser serialization matches the original HTML digest.

The full ZIP belongs to the export directory and public site. Label it as an accompanying-file download; a copied standalone HTML file cannot contain a circular self-embedded ZIP. A lone HTML copy remains readable and can export its embedded JSON with scripting enabled.

Optional controls are omitted unless completed: copy command/hash and a side-by-side diff. Search, pagination, filters and custom charts are unnecessary for this small grid. Never ship disabled promises or coming-soon navigation.

## Visual system

Proposed for review, not an approved incumbent brand:

- Light neutral canvas and a continuous white report sheet; dark ink, crisp rules, little or no shadow. No decorative texture, gradient, glass, orbital animation or quantum stock image.
- System sans-serif: `ui-sans-serif, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif`. System monospace only for code, exact identifiers and commands. No font download.
- Body 16px/1.55; small labels 14px; report title about 26px; primary finding about 32px/1.15. Avoid oversized display type. Tabular numerals in comparisons.
- Spacing scale: 4, 8, 12, 16, 24, 32, 48px. More space before headings than after. Prose width roughly 65–75 characters; data tables may use the wider sheet.
- Proposed colors: canvas `#f7f7f5`, sheet `#ffffff`, ink `#18181b`, muted text `#52525b`, link/focus `#1d4ed8`. Equivalent text `#166534`; changed text `#854d0e`; failure text `#991b1b`. Soft semantic backgrounds may use `#dcfce7`, `#fef3c7`, `#fee2e2`. Verify actual pairs during implementation.
- Light row rules are decorative. Interactive control boundaries and focus must meet meaningful contrast requirements. Border radius 0–4px, no pill farm.
- Color never carries meaning alone. Use exact text labels and visible diff markers. An intentional correction is attention/amber, not automatically red.

No animation is required. Native disclosures and direct anchor navigation are the signature interaction: a plain finding takes the reader to exact evidence and then its source hunk. Depth is functional, not theatrical.

## Responsive and accessible behavior

At narrow widths, preserve document order. Do not turn reference/target values into unlabeled stacked numbers. The small shot table wraps its headers; larger code/check tables may scroll inside labelled regions. No page-level horizontal overflow at 320 CSS pixels or 400% zoom.

Use one h1, ordered headings, landmarks, table captions and proper headers. Target WCAG 2.2 AA: 4.5:1 normal text, 3:1 large text/meaningful controls, visible focus, adequate hit areas and no color-only state. Native links/buttons/disclosures must work by keyboard; no hover-only content or custom drag requirement.

Keep limits beside the result on mobile. A visible `Checks cover declared inputs only` link remains even when full exclusions fall below the first fold. Avoid a sticky header/action bar consuming the small viewport.

Respect forced colors, reduced motion and browser text enlargement. Print includes finding, review state, scope and provenance. A custom PDF exporter is unnecessary.

## Failure and uncertainty copy

| State | Main presentation |
|---|---|
| Reference/target did not complete | Follow SPEC's ordered state table: `Execution failed — comparison unavailable` for failed runs; otherwise `Comparison incomplete`. Name the side and reason; retain useful diagnostics. |
| Partial or incomplete evidence | `Comparison incomplete`; list missing cases and known differences together. Initialized entries are not completed executions. |
| Unsupported measurement/layout/backend pattern | Name the unsupported feature and the declared supported scope; do not label it scientifically wrong. |
| No definitive circuit result | `Circuit result: inconclusive`, with raw method/outcome or timeout reason. |
| Invalid observation versus invalid bundle | A well-formed diagnostic record says `Invalid observations — comparison unavailable`. A corrupt/badly bound bundle or stale overlay is refused, not rendered as a normal trustworthy comparison. |
| No human decision | `Human decision: not recorded`. No default acceptance from model notes. |
| Network unavailable | Included content works. Only explicitly online links/downloads require connectivity. |
| Export/copy unavailable | Explain the browser Save As or select/copy fallback; do not show success before it happens. |

Do not add browser upload/error flows for features outside scope. The actual report is generated from validated local data, not an arbitrary online document importer.

## Design acceptance

The first viewport must show the mechanism without requiring Python knowledge: checked circuits, changed sampling, human state and limits. A reader can follow each claim to a particular observation and inspect source evidence.

After implementation, inspect actual desktop and mobile screenshots together, batch material fixes and confirm once. Open the offline report too. This planning schematic is not substitute evidence for that surface check.
