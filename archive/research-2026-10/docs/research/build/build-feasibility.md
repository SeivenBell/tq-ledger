# Q-Day Claim Ledger: technical feasibility for a 12-hour build (checked 2026-10-23)

## Summary

- **Claude Citations can't be combined with structured outputs.** If citations are on and you also send `output_config.format`, the API returns HTTP 400. For plain-text documents, citations come back as exact character spans (`start_char_index` / `end_char_index`). For PDFs you only get page numbers. So send the paper as text, not PDF, to get spans.
- **Deadline and video length:** submissions close Oct 25 11:59 PM ET. The Devpost page says the demo video is optional and up to 4 minutes. The Luma page says it is required and up to 2 minutes. Make one video of 2 minutes or less; it satisfies both.
- **Eon Era doesn't fit an extraction agent.** It tests agents against simulated companies (Salesforce, Zendesk, Slack and similar). You can't load your own data into a hosted company. This contradicts the memo's line "Eon Era: strongest".
- **SurrealDB Agent Memory fits better than the memo assumed.** SurrealDB's own prize brief asks for "facts that supersede rather than overwrite" and "retrieval you can trace back to its source". That is close to what the ledger does.
- **arXiv licensing:** most papers carry arXiv's default licence, which gives others no reuse rights. Don't store or serve their full text. Short quotes with attribution need a fair-dealing argument [INFERENCE: this is not legal advice].

---

## 1. Anthropic Claude Citations and structured extraction

Sources: [Citations](https://platform.claude.com/docs/en/build-with-claude/citations) (full), [Structured outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs) (partial: usage, JSON Schema limitations, compatibility), [Strict tool use](https://platform.claude.com/docs/en/agents-and-tools/tool-use/strict-tool-use) (partial: intro and quick start), [PDF support](https://platform.claude.com/docs/en/build-with-claude/pdf-support) (partial: requirements and cost), [Models overview](https://platform.claude.com/docs/en/models/overview) (full), [Pricing](https://platform.claude.com/docs/en/about-claude/pricing) (partial: model, batch, cache and tool tables). None of these pages is dated; all were read 2026-10-23.

**Supported models.** The docs say: "All [active models] support citations." The current lineup includes `claude-sonnet-5-5` and `claude-haiku-5-5`; both also appear in the structured outputs `supportedModels` list.

**How to send a document.** Put a `document` block in the user message:

```python
resp = client.messages.create(
    model="claude-sonnet-5-5", max_tokens=4096,
    messages=[{"role": "user", "content": [
        {"type": "document",
         "source": {"type": "text", "media_type": "text/plain", "data": paper_text},
         "title": "arXiv:2505.15917v2",
         "context": '{"url": "...", "license": "CC BY 4.0"}',   # passed to the model, never cited
         "citations": {"enabled": True}},
        {"type": "text", "text": "For each field, write one line `field: value` ..."}]}])
```

The `source` can be base64 or a URL (PDF), inline text, a `file_id` from the Files API, or a list of content blocks ("custom content").

**What comes back, by document type** (Citations, "Document types" table):

| Document type | Chunking | Citation format |
|---|---|---|
| Plain text | Sentence | `char_location`: `start_char_index` (0-indexed), `end_char_index` (exclusive) |
| PDF | Sentence | `page_location`: `start_page_number` (1-indexed), `end_page_number` (exclusive) |
| Custom content | None (your blocks) | `content_block_location`: block indices |

Example from the "Response structure" section:

```json
{"type": "text", "text": "the grass is green",
 "citations": [{"type": "char_location", "cited_text": "The grass is green.",
   "document_index": 0, "document_title": "Example Document",
   "start_char_index": 0, "end_char_index": 20}]}
```

**Constraints that matter for this project:**
- "Only text citations are currently supported." Scanned PDFs with no extractable text can't be cited.
- Text is cut into sentences, so a citation for a number points to the whole sentence that contains it.
- "Citations must be enabled on all or none of the documents within a request."

**Cost.** The docs say: "Enabling citations incurs a slight increase in input tokens". They also say `cited_text` "does not count toward output tokens", and isn't counted as input when you pass it back. For PDFs, "Each page typically uses 1,500–3,000 tokens".

**Not compatible with structured outputs.** Both pages say it, verbatim: "If you enable citations on any user-provided document … and also include the `output_config.format` parameter … the API returns a 400 error." The citations page lists citations as working with prompt caching, token counting and batch processing. No page I read says whether citations work with `strict: true` tools. [INFERENCE: untested; don't rely on it.]

**Structured outputs.** Python usage is `client.messages.parse(..., output_format=PydanticModel)`, which returns `response.parsed_output`. The JSON Schema subset has no recursion, no `minimum`/`maximum`, no `minLength`/`maxLength`, and requires `additionalProperties: false`. Strict tool use (`"strict": True` on a tool definition) follows the same schema limits.

**Prices (USD per million tokens):**

| Model | Input | Output | Notes |
|---|---|---|---|
| Sonnet 5.5 | $2 | $10 | Cache hits $0.10; Batch API $1 / $5 |
| Haiku 5.5 | $0.10 | $0.50 | For prompts up to 100k tokens; above 100k it is $0.50 / $2.50 |

- All current models have a 1M-token context window and 128K max output.
- The docs say models from Claude 4.7 on use a tokenizer that produces "approximately 30% more tokens for the same text".
- Ballpark per paper [INFERENCE]: a 40k-token paper on Sonnet 5.5 costs about $0.08 input plus about $0.02 output per call. Twenty papers with three calls each is under $10, well inside the $100 credit.

**Recommended extraction design** [INFERENCE]:
1. **Main pass:** `messages.parse` with a Pydantic `ClaimCard`. Every numeric field gets a `value` and a `verbatim_quote`.
2. **Verification in code:** find the quote with `paper_text.find(quote)`. That gives the character span. Reject the field if the quote isn't found, or if the number doesn't appear in the quote. This verification step is the product's core claim, and it doesn't depend on the model.
3. **Optional second check:** a separate Citations call on the same plain text. Confirm that a returned `char_location` overlaps the span from step 2. The docs say the API checks every pointer is valid ("citations are guaranteed to contain valid pointers").
4. **Get text, not PDFs:** use the arXiv HTML or LaTeX-derived text. Character spans only exist for plain-text documents.

## 2. Build North rules and submission requirements

Sources: [Devpost rules](https://build-north.devpost.com/rules) (full), [Devpost overview](https://build-north.devpost.com/) (full, read through the r.jina.ai proxy because a direct fetch got HTTP 403), [Devpost schedule](https://build-north.devpost.com/details/dates) (full), [Luma event page](https://luma.com/build-north) (full). `/details` returned 404.

**Required items** (Devpost, "What to submit"):
- A public GitHub repo.
- "A live link (if applicable)… If your project can be run or accessed outside your own machine, link it here."
- "A demo video (optional). Four minutes or less, shareable link, no login required."
- A write-up covering the tech stack and which partner platforms you used and how.
- Every team member listed.
- "Disclosure of prior work… explain what was built or changed during the week itself."

**Conflict on the video.** Luma's "What You'll Submit" lists, as required: "A demo video up to 2 minutes (shareable link, no login)". Make one ≤2-minute video.

**Dates:**
- Devpost schedule: submissions close Oct 26 12:00am EDT, which is the same moment as Oct 25 11:59 PM ET.
- Judging runs Oct 26 12:15am to Oct 27 12:00am EDT.
- Winners are announced Oct 29 11:00pm EDT.
- The top 10 are notified Oct 26 and demo in person in Toronto on Oct 29. "At least one person on your team needs to be able to attend in person."

**Judging:**
- Five criteria: Innovation; Real-World Impact ("Clear user, value-add, and a path to production"); UI & Design; Tech & Deployment ("deployed, serving features"); Security & Ethics.
- **Weights: not found** on Devpost or Luma.
- Process (Luma): "two rounds: online judging on Oct 26 to select the top 10, followed by live judging at Demo Day on Oct 29".
- Partner prizes: Devpost says "judges will look for evidence that the platform materially shaped what you built."

**Eligibility** (Rules): "You must be 18 or older and live in Canada." Teams of up to 4; one submission per team. Employees of Georgian, Devpost and the partner companies, and of judges' companies, can't enter. The Devpost sidebar says "All countries/territories" (seen in a search snippet only); the Rules text is the binding one, and Severyn lives in Waterloo either way.

**IP and fair play** (Rules):
- "You keep ownership of your code and IP."
- The repo, video and page will be public, and Georgian and partners may promote them.
- "Disclose prior work, templates and AI tools you used."
- "Don't include confidential information or anyone else's IP without permission." This line is relevant to arXiv excerpts (see §7).
- The code of conduct bans "faking your demo".

**Does the live link have to stay up?** Not found. [INFERENCE: keep it running at least through Oct 29. Judging, Demo Day and the winner announcement all happen then.]

## 3. Render hosting

Sources: [Free tier](https://render.com/docs/free) (full), [Credits](https://render.com/docs/credits) (full), [Deploy FastAPI](https://render.com/docs/deploy-fastapi) (full), [Web services](https://render.com/docs/web-services) (partial: port binding), [Pricing](https://render.com/pricing) (partial: compute and workspace tables). The [claim form](https://credits-portal-mmdm.onrender.com/claim/build-north-georgian) is a JavaScript app and returned only an empty HTML shell, so **the form's fields were not found**. The Devpost resources page says "$50 in Render credits for every participant. Redeem them through this form".

**Free tier limits:**
- **Spin-down:** a service that gets no traffic for 15 minutes spins down. Spinning back up "takes about one minute". Judges hitting a cold service will see a loading page.
- **Storage:** the filesystem is ephemeral and is lost on every redeploy, restart or spin-down. So commit the frozen ledger data (JSON or SQLite) to the repo.
- **Hours and size:** 750 free instance hours per month; 0.1 CPU and 512 MB RAM.
- **Outbound traffic:** a service may be suspended for an "uncommonly high volume" of traffic it initiates. Calls to the Anthropic API at demo volume are low [INFERENCE].

**Paid instance:** the `0.5c-512mb` plan costs $7/month. The spin-down limit is listed only under free instances, so a paid instance avoids it. [INFERENCE: the $50 credit covers this many times over.]

**How credits work:** they are "applied at the end of each billing period". Promo codes "usually expire shortly after the event ends". Credits can't be moved between workspaces.

**Deploying FastAPI:**
- Build command: `pip install -r requirements.txt`
- Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
- The default `PORT` is `10000`.
- Gradio or Streamlit work the same way: bind to `0.0.0.0:$PORT`. I did not read Render's Gradio or Streamlit docs.

## 4. SurrealDB Agent Memory

Sources: [Build North participant pack](https://surrealdb.notion.site/Build-North-SurrealDB-participant-resources-pack-3edbfa44ae3e81a0a6ebd0b4fbb802d3) (full, through r.jina.ai), [How it works](https://surrealdb.com/docs/agent-memory/welcome/how-it-works) (full), [REST API](https://surrealdb.com/docs/agent-memory/reference/rest-api) (partial, lines 1–300 plus targeted search), [Python SDK](https://surrealdb.com/docs/agent-memory/integrations/sdks/python) (full), [Integrations](https://surrealdb.com/docs/agent-memory/integrations) (full), [Cloud quickstart](https://surrealdb.com/docs/agent-memory/quickstarts/surrealdb-cloud) (full), [Provenance](https://surrealdb.com/docs/agent-memory/mental-model/provenance-and-traceability) (full), [Extraction pipeline](https://surrealdb.com/docs/agent-memory/reasoning/extraction-pipeline) (full), [Bulk import / triples](https://surrealdb.com/docs/agent-memory/ingest/authoritative/bulk-import) (partial, lines 1–300), [Agent Memory plans](https://surrealdb.com/agent-memory) (partial: plans section). None are dated.

**What it is.** A hosted memory layer with one "context" per deployment and REST endpoints at `https://{context.host}/api/v1/{context_id}/…` using a Bearer `sp-…` key:
- `POST /facts` writes facts. The `infer` mode is `full` (LLM extraction), `triples` (you supply structured facts, no LLM), `preview` or `none`.
- `POST /documents` ingests documents asynchronously.
- `POST /query` does recall, with `asOf` support.
- `/chat`, and entity `/history` and `/neighbourhood` endpoints.

There is also an MCP server at `/mcp`.

**Python support.** The docs say: "`pip install --pre 'surrealdb[memory]'`". The SDK is on the 3.x prerelease line; a plain `pip install surrealdb` gets 2.x, which has no memory client. Usage:

```python
from surrealdb.memory import Memory
m = Memory(context=..., endpoint=..., api_key=...)
m.remember(..., infer="triples", triples=[...])
m.recall(...)
```

The SDK does not read environment variables; pass the values in.

**Triples format** for writing a claim graph:

```json
{"infer": "triples", "scopes": [["ledger"]], "triples": [
  {"entity": {"type": "concept", "name": "claim:gidney2025-rsa2048"},
   "key": "cites", "target": {"type": "concept", "name": "arXiv:2505.15917v2"}}]}
```

- A later triple with the same entity and key supersedes the earlier one.
- You must create the scope first with `POST /scopes`. Otherwise the request fails with "unknown scope node".
- Entity `type` must come from a fixed set; anything else is stored as `other`.

**Two caveats:**
- **Expired relations disappear from recall:** "A relation whose `valid_until` has passed is left out of… `/query` results". And "`asOf` … selects by when Agent Memory learned a fact rather than by when the fact was true."
- **No character spans for triples** [INFERENCE: triples are stored with `source.kind = "upsert"`]. `source.span` points into text that Agent Memory itself received. So store the paper's character offsets as your own attributes.

**Free tier and the BUILDNORTH50 code:**
- **Sandbox plan:** "Free, no card needed", "3 million tokens included, one-off". Tokens are counted on every LLM and embedding call, including background consolidation.
- **Lite plan:** $30/month for 1M tokens.
- **Redeeming the code** (pack): "Billing dashboard → paste the code → Redeem". Then "Agent Memory in the sidebar → Deploy new context → name it, pick a region → Create context". Provisioning takes "a minute or two" (quickstart).

**Is a provenance graph (source → claim → assumption) a fair "agent memory" use?** Yes, if the extractor reads from it on the next extraction. The pack states what SurrealDB is looking for, verbatim:

> "Facts that supersede rather than overwrite / Retrieval you can trace back to its source / Memory shared coherently across more than one agent"

The provenance doc adds: "Cross-provenance disagreement becomes **`uncertainty`**; same-stream updates **supersede**."

[INFERENCE] A strong demo: the extractor recalls earlier cards on the same problem before it writes a new one. Example: Gidney 2025's RSA-2048 estimate supersedes Gidney–Ekerå 2019 in a "best current estimate" line. Model each claim as its own entity, not one shared `rsa2048.qubits` key. Otherwise the reconciler will supersede or flag numbers that aren't comparable, which contradicts the ledger's whole thesis. A plain store that nothing reads back from would not meet the "materially shaped" test.

## 5. Eon Era

Sources: [Era blog post](https://www.eon.io/blog/era-build-and-test-ai-agents) (full, updated 2026-10-08), [Era hackathon guide](https://drive.google.com/file/d/13QeKjpxekj62n92jJLfnVOBwn1xb4HWB/view) (partial: only pages 1–4 of 8 extracted; download is blocked by the owner), [GitHub eon-io/era README](https://github.com/eon-io/era) (full), [console llms.txt](https://console.era.eon.io/llms.txt) (full), [Load data into a simulator](https://console.era.eon.io/docs/load-data-into-a-simulator.md) (full), [Usage limits](https://console.era.eon.io/docs/usage-limits.md) (full), [Test your agent over MCP](https://console.era.eon.io/docs/test-your-agent-over-mcp.md) (full), [Run a simulator](https://console.era.eon.io/docs/run-a-simulator.md) (full).

**What Era tests.** From the guide, page 1: "Era builds a simulated company for your agent to work in… Salesforce, Zendesk and Slack… 100% simulated… and read-only." You choose industry (E-commerce, Fintech, Healthcare), size, an optional scenario such as "Dirty CRM", and which systems to include (guide, page 3). Benchmarks score agents against Era's answer keys for that company.

**How an agent connects:**
1. Sign up with the invite link.
2. Click "+ New environment", then "Synthesize company".
3. "Issue token" (shown once).
4. "Add all MCPs" for Claude Code, or call each system's REST API.

The CLI equivalent is `era init`, then `era new --industry fintech --size mid --systems salesforce,slack`, then `era mcp <tenant> --client claude`.

**Limits.** "Each account includes 2,000 free calls each month". The docs warn "A single exploratory session can use 30–50 calls".

**Can a quantum-paper extraction agent be benchmarked on Era? Not as intended.**
- llms.txt says: "the console, its API, its MCP tools and the Era CLI have no way to load your own data into a hosted company."
- You can run a simulator yourself in Docker and add records through `/_admin/tenants/<t>/inject`. For example, SharePoint `driveItems` accept `content`. [INFERENCE] Putting arXiv excerpts into a fake SharePoint so the agent can read them over MCP would be contrived. Judges from Eon would likely see it as unnatural.
- **This contradicts the memo's "Eon Era: strongest".** Your own labelled field-level eval is still worth doing, but it isn't an Era use.

## 6. Clerk with a Python backend

Sources: [Clerk Python backend article](https://clerk.com/articles/how-to-add-authentication-to-a-python-backend) (partial, lines 1–300), [JS quickstart](https://clerk.com/docs/js-frontend/getting-started/quickstart) (full), [Pricing](https://clerk.com/pricing) (partial, lines 1–300).

**Setup:**
- **Frontend:** paste two script tags from the dashboard (`ui.browser.js` and `clerk.browser.js` with `data-clerk-publishable-key`). Then call `await Clerk.load({ui:{ClerkUI: window.__internal_ClerkUICtor}})` and `Clerk.mountSignIn(div)` or `Clerk.mountUserButton(div)`. No bundler is needed.
- **Backend:** `pip install clerk-backend-api` (needs Python 3.10 or later; version 6.0.1 per the article). Verify requests like this:

```python
state = authenticate_request(request, AuthenticateRequestOptions(
    secret_key=os.environ["CLERK_SECRET_KEY"], jwt_key=os.environ.get("CLERK_JWT_KEY"),
    authorized_parties=["https://<app>.onrender.com"], accepts_token=["session_token"]))
if not state.is_signed_in: raise HTTPException(401)
```

- The SDK checks the `Authorization: Bearer` header first, then the `__session` cookie. A FastAPI app that serves its own pages therefore needs no token plumbing.
- **Gotcha** (article): `CLERK_AUTHORIZED_PARTIES` must be split into a list; passing the raw string fails with `TOKEN_INVALID_AUTHORIZED_PARTIES`. The article also notes the Python default for `accepts_token` is `['any']`, so set it explicitly.

**Cost.** The Hobby plan is free with no card, 50,000 monthly retained users per app, and up to 3 social logins. MFA and passkeys need Pro.

**Time to set up** [INFERENCE]: about 45–90 minutes including the dashboard and deploy.

**Fair role for the prize** [INFERENCE]: the public ledger stays read-only. Signed-in reviewers approve or reject extracted fields, and each approval records the Clerk `user_id`. That approval is the "humans review" step from the project description.

## 7. arXiv licensing

Sources: [arXiv licence help](https://info.arxiv.org/help/license/index.html) (full), [Reuse FAQ](https://info.arxiv.org/help/license/reuse.html) (full), [Default licence text](https://arxiv.org/licenses/nonexclusive-distrib/1.0/license.html) (full, dated 2004-01-16), [API Terms of Use](https://info.arxiv.org/help/api/tou.html) (full), Canada Copyright Act [s.29](https://laws-lois.justice.gc.ca/eng/acts/C-42/section-29.html) and [s.29.1](https://laws-lois.justice.gc.ca/eng/acts/C-42/section-29.1.html) (full; Act current to 2026-09-30).

**Default arXiv licence.** It grants rights only to arXiv: "I grant arXiv.org a perpetual, non-exclusive license to distribute this article." The reuse FAQ says it "does not grant further reuse permissions directly… you will need to contact the author".

**What arXiv says you can't do.** API terms, "must not do": "Store and serve arXiv e-prints (PDFs, source files, or other content) from your servers, unless you have the permission of the copyright holder or are permitted to do so by the license". They allow you to "Retrieve, store, and use the content… for your own personal use, or for research purposes".

**Metadata is free to use.** Titles, abstracts, authors and identifiers are under CC0.

**CC BY 4.0 papers** allow reusers to "distribute, remix, adapt… so long as attribution is given". You can cache and display the full text if you attribute it.

**Short quotes under the default licence.** This falls under Canadian fair dealing:
- s.29: "Fair dealing for the purpose of research, private study, education…"
- s.29.1: "Fair dealing for the purpose of criticism or review does not infringe copyright if the following are mentioned: (a) the source; and (b) … the name of the… author".

[INFERENCE, not legal advice] Showing one or two sentence-length quotes per field, with the author, the arXiv ID with version, and a link, in a tool that critically compares claims fits s.29.1. Redistributing full text does not. The Build North rule against using "anyone else's IP without permission" adds risk, so:
- Pick CC BY papers for the demo where you can.
- For papers under the default licence, keep only offsets and short quotes, never the full text in the public repo.
- Show the licence on each card.

---

## Recommended stack

| Layer | Choice | Reason |
|---|---|---|
| App | FastAPI with Jinja templates and a little JavaScript (HTMX is optional) | One process on one Render service. Clerk works through the same-origin `__session` cookie. You control the UI, which judges score. [INFERENCE] Gradio would make Clerk and a custom card design harder. |
| LLM | `claude-sonnet-5-5` through `messages.parse` (Pydantic `ClaimCard` with `verbatim_quote` on each field); `claude-haiku-5-5` for cheap repeated eval runs | Structured outputs give valid JSON every time. Citations can't be used in the same call, so the code checks quotes itself, which is the product's deterministic core. A Citations call on plain text can be a second check. |
| Source text | arXiv HTML or plain text, not PDF | Only plain-text documents give character spans; PDFs give page numbers only. |
| Data | Frozen JSON or SQLite committed to the repo | Render's filesystem is ephemeral; the demo data is dated and frozen. |
| Memory (SurrealDB prize, optional) | Agent Memory context: triples for claim → source → assumption; supersession for "current best estimate"; recall before each extraction | Matches what the prize brief asks for. Sandbox plus the BUILDNORTH50 credit covers the cost. Note the `--pre` install. |
| Auth (Clerk prize, optional) | Clerk Hobby; public read-only view, sign-in required to approve | 45–90 minutes [INFERENCE]; gives Security & Ethics a concrete human-review story. |
| Hosting | Render web service on the $7/month `0.5c-512mb` plan, paid with the $50 credit | Free instances spin down after 15 minutes and take about a minute to start; judges may hit it cold. |
| Era | Leave it out of the pitch | It only fits enterprise agents working on simulated SaaS data, and you can't load your own data into a hosted company. |

**Checks for the main agent:**
1. Make one test API call to confirm that `output_config.format` with a citations-enabled document returns 400.
2. Check whether `strict: true` tools work together with citations (not documented).
3. Open the Render claim form in a browser; it couldn't be read here.
4. Look in Discord for any official update on video length, since Devpost and Luma disagree.