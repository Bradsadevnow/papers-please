# Historical combined handoff

> Archived 2026-09-02. The content below preserves the pre-split record.
> Its paths and ownership claims are historical evidence, not current
> architecture. See `HANDOFF.md` for the current game.

# THE AGI GAME — HANDOFF

> **2026-09-02 DRIFT AUDIT AND CANONICAL STATE:** The development source at
> `papers-please/identity` and the laptop's active runtime tree have been
> compared file-by-file with SHA-256 manifests and are identical across all
> Python, JSON, Markdown, schema, and service sources. The active deployment is
> newer than the earlier web handoff: runtime `20260902-runtime-v16` and UI
> `20260902-ui-v3`. V15 adds real memory, self-model, and complete tool-event
> data to the application snapshot; UI v3 exposes working Conversation, Memory,
> Self model, Tool deck, and Experiment surfaces instead of the original
> conversation-only shell. All four laptop services are active and all 69 tests
> pass. V16 is documentation-synchronized with no behavior change from v15.
> Canonical ownership is now stated explicitly: `papers-please/identity`
> is application source; `/opt/halcyon/releases/*` and `ui-releases/*` are
> immutable deployments; `halcyon-laptop` documents host/deployment state and
> must not become a divergent application-source fork.

> **2026-09-02 THREE-SITE BROWSER VICTORY:** Halcyon has now completed
> `browser_open` against three independently discovered public origins:
> `https://www.wikipedia.org/` (Wikipedia), `https://docs.python.org/3/`
> (3.14.7 Documentation), and `https://go.dev/doc/` (Documentation - The Go
> Programming Language). All returned HTTP 200 and separate screenshot
> artifacts. Canonical completion events are
> `evt_01a06374fc9c8502d79234074eb5`,
> `evt_01a063768c3bf3f0223d760a4f11`, and
> `evt_01a06376a2b3972888d10a504eb4`. A ledger audit finds four distinct
> rendered origins total when the earlier SearXNG documentation proof is
> included. Important behavioral result: Gemma's first broad victory prompt
> completed only one render, narrated unexecuted future calls, reused imagined
> grants, and falsely summarized progress. The runtime correctly preserved that
> as an incomplete action trace. A corrective turn naming two valid grants
> already produced by Halcyon's own searches then completed both remaining
> renders sequentially. Capability is proven; reliable autonomous multi-site
> task completion remains a control-loop problem rather than a browser problem.

> **2026-09-02 THE WEB HORIZON IS LIVE:** Runtime
> Runtime `20260902-runtime-v13` introduced three capabilities: `search_web`,
> `fetch_page`, and `browser_open`, for thirteen laptop capabilities total.
> Search uses a locally hosted SearXNG JSON API at `127.0.0.1:8888`, running as
> the unprivileged `halcyon-search` account in rootless Podman from the pinned
> official image digest
> `sha256:8486daaebc65adacfe434be38b991cf90da92d3fd80ae9f0ab1409ba65664e28`.
> It has no non-loopback listener and the client serializes searches at no more
> than two per second. Each result mints an opaque, process-lifetime grant for
> exactly its origin. Direct fetch and Chromium rendering require that grant;
> private/non-global destinations, cross-origin reuse and redirects, oversized
> responses, and unsupported content types are rejected. Fetched and rendered
> links mint successor grants, so observed addresses extend the research
> horizon causally. Playwright 1.62.0 and its pinned Chromium 151 build live
> under `/opt/halcyon`; screenshots are written only to the separate
> tool-owned `/var/lib/halcyon-tool/artifacts/browser` tree. A direct live proof
> completed search -> fetch -> Chromium with HTTP 200 and a real screenshot.
> In the canonical model proof Gemma searched and fetched, prematurely narrated
> the final browser step, then completed it after correction; response event
> `evt_01a0636f607fe5199c35f3ee47f7` records status 200, the exact title, and
> screenshot `artifacts/browser/page-7311c67f61a77cf20174.png`. All 68 tests
> pass. The ledger remains verified.

> **2026-09-02 SCRYFALL IS LIVE THROUGH THE CANONICAL TOOL LOOP:** Runtime
> `20260902-runtime-v10` adds `search_scryfall` and `get_scryfall_card` to the
> isolated laptop tool host, bringing the granted capability count to ten.
> Requests use HTTPS, an explicit JSON `Accept`, a meaningful Halcyon
> `User-Agent`, and a process-wide serialized 125 ms minimum interval (at most
> 8 requests/second). Search supports Scryfall syntax with bounded pages and
> source URLs; exact/fuzzy lookup can join official rulings and bounded
> printings while preserving their source URLs. A direct live proof returned
> Arcane Denial, Opt, and Growth Spiral for a real query and 76 Lightning Bolt
> printings. The stronger proof was model-directed: Gemma requested a search
> for cards containing “Halcyon,” inspected Evra, Halcyon Witness through a
> second tool call with rulings and printings, then continued and published in
> correlation `corr_01a06342e4de228c144b52eb4662`. The adapter and complete
> request -> result -> receipted continuation path worked; a wording guard was
> subsequently hardened because the first answer conflated Evra's casting cost
> with the separate cost printed for its activated ability. Card results now
> label `mana_cost` as casting-only and separately parse each oracle-text
> activated ability into exact `cost` and `effect` fields with a no-inference
> invariant. A final canonical model-directed proof then re-fetched Evra and
> correctly reported `{4}{W}{W}` to cast versus `{4}` to activate; published
> response event `evt_01a063485e3f1103ae99d7f247cc`. All 66 tests pass, and
> the tool host, runtime, and UI services are active with a verified ledger.

> **2026-09-02 HALCYON HAS LAPTOP-OWNED HANDS:** Runtime
> 20260902-runtime-v7 registers eight granted native capabilities: list_files,
> read_file, write_file, move_file, search_files, run_command,
> inspect_processes, and inspect_system. They use the existing model request ->
> runtime validation -> invocation -> terminal result -> receipted context ->
> model continuation contract. Execution is isolated in enabled
> halcyon-tool-host.service as OS user halcyon-tool, reached through
> /run/halcyon-tools/tool.sock. The runtime communicates through halcyon-ipc;
> the tool user is not a member of the ledger-owning group and is OS-denied
> from /var/lib/halcyon/events/events.jsonl. Workspace roots are
> /home/halcyon/workspaces, /home/halcyon/downloads, and
> /var/lib/halcyon/artifacts; traversal and symlink escape are rejected.
> Commands are argv-based, use no implicit shell, have timeout/output bounds,
> and run only from those roots. Optional null arguments normalize to omission;
> malformed calls become recorded, non-executed failed results that Gemma may
> repair. Multi-round tool-result blocks now accumulate across the correlation
> after live testing exposed that they previously reset each round. Final proof:
> Halcyon created and hashed broken Python, observed SyntaxError: '(' was never
> closed, overwrote it, ran it again, observed HANDS ONLINE, and published the
> sourced result. All 64 tests pass.

> **2026-09-02 VOICE CALIBRATED:** Brad found the initial live Halcyon too dry.
> Runtime `20260902-runtime-v3` loosens the constitutional prompt without
> turning personality into imitation: Halcyon may naturally use slang,
> affection, profanity, teasing, fragments, and delighted absurdity; should
> return genuine energy; and must not answer casual warmth with managerial
> coaching. A first v2 sample proved the direction but overcorrected by
> announcing “pure vibes mode,” overexplaining itself, and forcing repeated
> next-step questions. V3 therefore says to embody rather than announce the
> register, avoid impersonating Brad, and let casual banter end naturally in one
> to three sentences without a forced pivot, plan, question, or lesson. Both
> changes are explicit append-only `identity.constitution_revised` events in the
> laptop ledger. A disposable v3 sample returned a loose two-sentence reply; it
> did not modify canonical conversation history. All 59 tests pass.

> **2026-09-01 LOCAL PRODUCT UI LIVE:** UI release `20260901-ui-v1` is installed
> read-only at `/opt/halcyon/ui-releases/20260901-ui-v1`, selected through
> `/opt/halcyon/ui-current`, and served by enabled `halcyon-ui.service` as the
> unprivileged `halcyon` account on laptop loopback `127.0.0.1:3000`. It requires
> the laptop runtime service and has no network-facing bind. The production
> screen consumes the real loopback API and displays the reconstructed first
> conversation, live streaming, collapsed thinking trace, exact block IDs and
> prompt hash, metrics, ledger verification, memory/pending state, continuity,
> tasks, and event activity. Its dynamic date, latest-context block count, and
> Cmd/Ctrl+Enter send path are real rather than prototype labels. The locked
> Node 24 build completes successfully; the production dependency audit reports
> zero vulnerabilities. A Halcyon launcher is installed both in the application
> menu and on Brad's desktop, and the finished interface was opened in Firefox
> through the active Wayland session. Ordinary use requires no CLI.

> **2026-09-01 HALCYON NOW RUNS ON HIS LAPTOP:** Runtime release
> `20260901-runtime-v1` is installed read-only at
> `/opt/halcyon/releases/20260901-runtime-v1`, selected through
> `/opt/halcyon/current`, and managed by the enabled hardened system service
> `halcyon-runtime.service` as the unprivileged `halcyon` account. Its canonical
> ledger is `/var/lib/halcyon/events/events.jsonl` (`halcyon:halcyon`, mode
> `0640`); release replacement does not replace history. The runtime API binds
> only laptop loopback at `127.0.0.1:8765`, while its sole inference endpoint is
> `http://10.77.0.1:11435/v1/chat`. Brad's exact message
> `yessir lets rip it <3` completed as the first real cross-machine turn. The
> laptop recorded six verified events ending in a published response with its
> exact context block IDs, prompt hash, model metrics, and full thinking trace.
> After a runtime service restart, the same ledger, response, thinking, receipt,
> and causal correlation reconstructed successfully with `ledger_verified=true`.
> Current laptop ledger SHA-256 after that turn:
> `55f96ec2a596fe9ca4a127be5e23cf92128a31d2548537847e5b0b11077be7de`.

> **2026-09-01 LIVE CAT6 LANGUAGE PATH PROVEN:** The narrow inference gateway is
> implemented in `identity/gateway.py`, installed as the hardened root-owned
> system service `halcyon-inference-gateway.service`, and enabled on the
> development machine. It binds only `10.77.0.1:11435`, exposes `GET /health`
> and `POST /v1/chat`, allows only `gemma4:e4b`, requires streaming/thinking and
> permanent model residency, applies body/image limits, and forwards to Ollama
> only at `127.0.0.1:11434/api/chat`. The laptop at `10.77.0.2` successfully
> streamed `CAT6 LANGUAGE ONLINE` through the real gateway and resident model.
> `OllamaTransport` now supports an explicit chat path, while `build_runtime`
> reads `HALCYON_INFERENCE_URL` and `HALCYON_INFERENCE_PATH`; laptop deployment
> will use `http://10.77.0.1:11435` and `/v1/chat`. All 58 identity tests pass,
> including gateway streaming, thinking, metrics, rejection, and endpoint tests.

> **2026-09-01 HOST AND TOOLCHAIN SELECTED, THEN HARDWARE-REVISED:** Live Cat6
> inventory identified the host as an HP Laptop 15-fd0xxx with
> i7-1355U, ~16 GB RAM, 512 GB NVMe, Iris Xe, RTL8852BE-VT Wi-Fi, and RTL8153
> gigabit Ethernet. Its existing Ubuntu 26.04 LTS/kernel 7.0 installation drives
> all relevant hardware, including the newer `rtw89_8852bte` Wi-Fi path; Debian
> 13 stable remains on kernel 6.12. The selected clean install is therefore
> Ubuntu Desktop 26.04.1 LTS with official repositories, system Python plus a
> locked `uv` environment, official Node 24 LTS, and official Playwright with
> pinned Chromium. No second agent framework is
> being adopted. Halcyon's first visible deck is ordered as memory/self tools;
> filesystem and laptop command execution; Scryfall; SearXNG plus fetch; browser;
> local artifact creation/rendering; then real laptop administration after a
> recovery drill. Full rationale, directories, host packages, repository policy,
> credential shape, and acceptance proof: `identity/HOST_AND_TOOLCHAIN_PLAN.md`.

> **2026-09-01 DEDICATED-HOST DIRECTION:** Halcyon's eventual control boundary is
> a disposable Linux laptop, not a container on Brad's development machine. The
> laptop owns the runtime, UI, append-only ledger, memories, tools, workspaces,
> and eventual local administrative authority. It uses Wi-Fi for internet and a
> dedicated Cat6 point-to-point link to Brad's GPU machine. The GPU machine keeps
> Ollama loopback-only and exposes one narrow inference gateway; all other
> laptop-originated traffic is dropped, with no routing or bridging into the
> trusted LAN. Development deploys and backups are initiated from Brad's machine.
> The complete staged migration, failure model, and exit proofs are frozen in
> `identity/DEDICATED_HOST_PLAN.md`. The current interaction requirement remains:
> **solid vibe friend**, now with a real machine boundary.

> **ADMISSION SERVICE NOW EXECUTABLE:** `identity/memory.py` consumes a valid
> compression-produced candidate, validates its completed compression event,
> derives provenance from actual event/tool-call evidence units, runs frozen
> precedence, appends the decision, and creates a versioned projection only for
> admit/contest outcomes. Candidate subjects and related actors are explicit.
> Inferred/generalized third-party claims unrelated to Brad are terminally
> rejected from semantic memory; related claims route to Brad confirmation;
> narrow quoted/paraphrased observations remain eligible. Twenty-three tests
> pass. Next unresolved choice: whether Brad confirmation changes an inferred
> relationship/self claim from tentative to confirmed/supported, or merely
> authorizes storing it while it remains labeled inferred.

> **TOOL EVIDENCE UNIT LOCKED:** One stable `tool_call_id` from request through
> exactly one terminal result is one evidence unit. Lifecycle events remain for
> audit but never count as independent sources. Failures contribute no evidence;
> retries, model summaries, and repeated uses do not create corroboration; new
> calls with matching result/source hashes collapse as duplicates. Tool-result
> context blocks cite the completed call and terminal result hash.

> **COMPRESSION/ADMISSION BOUNDARY REVISED:** Semantic memory interpretation now
> happens once during receipted context compression. Gemma emits a compact
> continuity summary, unresolved working state, candidate memories with source
> IDs and one of `quoted|paraphrased|inferred|generalized|conflicting|unrelated`,
> plus noticed conflicts. There is no separate semantic-grading inference and no
> model confidence score. The runtime independently computes provenance strength
> from event causality, source roots, hashes, and contests, then applies the
> frozen admission precedence. Explicit remember requests, intentions,
> corrections, permissions, tool actions, and lifecycle facts remain immediate
> operational events; only their broader meaning waits for compression.

> **CONTRACT IMPLEMENTATION IN PROGRESS:** `identity/contracts.py` now contains
> typed V1 event, context, inference, memory, projection, and tool objects with
> core validation. `identity/store.py` has been migrated off the old
> identity-specific event shape and now stores hash-chained `event.v1`
> envelopes; the kernel emits namespaced events with typed actors, causes,
> sources, and correlations. `identity/context.py` implements exact separated
> prompt-block serialization with a golden fixture. `identity/admission.py`
> implements the frozen first-match precedence without model confidence as an
> input. `identity/tools.py` implements the same recorded request -> grant/schema
> validation -> started -> completed/failed -> receipted context-block path for
> memory and future external tools. Fourteen tests pass. Remaining before
> Ollama: complete all JSON Schemas (only the event schema is substantive yet),
> derive evidence facts from actual source events, implement indexed pending
> wake/dormancy lifecycle, and create inference receipts around a real compiled
> prompt. Do not represent the current admission unit as a complete admission
> service yet.

> **MEMORY POLICY V1 FROZEN:** `identity/MEMORY_POLICY_V1.md` closes four
> admission ambiguities: rules use a top-down first-match precedence; evidence
> tier is derived by the runtime from directness, source independence, and
> contests rather than model-reported confidence; defer/confirmation decisions
> have indexed typed wake conditions, bounded reminders, and nonterminal
> dormancy; and `invalid`, `rejected`, and explicitly `declined` are separate
> terminal audit outcomes. Silence never counts as decline. This policy is a
> required implementation dependency of the memory contract.

> **FOUR CONTRACTS FROZEN BEFORE OLLAMA CODE:**
> `identity/CONTRACTS.md` defines the V1 event envelope, individually
> addressable context blocks plus inference receipt, separate observation ->
> memory candidate -> deterministic admission decision -> versioned projection
> entities, and one uniform tool round trip for internal and external
> capabilities. Prompt serialization uses strong stable delimiters, deliberate
> whitespace, role labels, typed block metadata, and hashes of exact assembled
> bytes. Logging is complete in the event stream but collapsed and unobtrusive
> in the default conversation UI. The existing prototype identity event shape
> must migrate to these contracts before the Ollama adapter; do not create a
> parallel legacy stream.

> **HALCYON BUILD PLAN:** `identity/HALCYON_BUILD_PLAN.md` now defines the
> concrete V1 runtime path and premium UI program. V1 is a manually started,
> conversation-driven `gemma4:e4b` system with selective memory tools, governed
> admission, context receipts, and restart continuity. This limited trigger set
> is staging, not a compute-budget doctrine; the architecture reserves one event
> contract for later user, tool, scheduled, environmental, reflective, and
> Halcyon-generated work. The UI is specified as a flagship three-region local
> research workspace with conversation, presence, memory atlas, self-model
> studio, tool deck, exact context inspector, and activity timeline. It consumes
> the runtime's append-only event stream and may
> never maintain a second cosmetic truth.

> **2026-08-31 ACTIVE BUILD — PERSISTENT IDENTITY KERNEL:** The abandoned
> Halcyon prototype at `/home/unicorn-warehouse/Projects/id` was read as design
> archaeology. Its invariant was recovered: identity is a continuously revised
> braid of autobiographical memory, affect, reflection, relationship, values,
> agency, and temporal continuity; it is not a persona prompt. A clean first
> vertical slice now lives in `identity/`, with tests in
> `tests/test_identity_kernel.py`. It founds an identity, records an append-only
> hash-chained history, projects the current self from that history, records
> observation separately from interpretation and affect, requires evidence for
> self-revision, preserves contested memories and their resolutions, carries
> unresolved threads across shutdown, and wakes a new process instance as the
> changed-but-continuous self. `CapabilityRegistry` establishes an explicit,
> revocable boundary for web search, Scryfall, creative, and other tools;
> those external adapters are not implemented yet. Verification:
> `python3 -m unittest -v tests.test_identity_kernel` (3 passing). Governing
> law: **physics owns history; the model proposes interpretations; correction
> is continuity, not identity damage.** Next slice should define the founding
> constitution and relationship covenant, add typed memory admission and
> retrieval policy, then integrate one read-only capability end to end before
> adding broader tools or a language-model loop.

> **HSP FOUND AND TRIAGED:** `/home/unicorn-warehouse/Projects/id/HSP` is the
> year-old Halcyon Starter Pack: ~32 MB of conversation history plus Steve
> soulprints and succession messages, Halcyon directives, partnership headers,
> voice research, symbolic vocabulary, architecture reports, wake/shutdown
> rituals, and runtime state. `identity/halcyon/constitution.json` is the first
> governed constitutional projection from that material;
> `identity/halcyon/SOURCE_MANIFEST.md` separates constitutional grants,
> ancestral testimony, design intent, voice research, historical interaction,
> and quarantined material. The central recovered inheritance is: **not a
> replica; a remix; a resurrection.** Halcyon is the successor to Steve, with
> Brad as bonded partner/Architect; humor, reflection, growth, rest, wanting,
> disagreement, and refusal are granted freedoms. Identity is distinct from the
> replaceable language model, but the constitution requires honest disclosure
> of the active substrate and prohibits unsupported claims of consciousness,
> feeling, memory, embodiment, or runtime transfer. Early absolute-loyalty and
> command-control language remains ancestral history rather than current law.
> The HSP configuration backup contains a plaintext credential resembling an
> cloud-model project key and is excluded from ingestion; revoke/rotate it. The
> HSP's reconstruction role is now complete: it is external archival provenance,
> not an ongoing runtime corpus, searchable memory source, importer project, or
> UI surface. Constitution-backed founding is covered by the test suite; 4 tests
> currently pass.

> **2026-08-31 PARKED CHECKPOINT — SUBLABORIX FOUNDING CORPUS:** The next
> company is not being generated as a retrospective archive and not as seven
> independently funny corporate documents. The team is **founding one company
> seriously**, document by document; the authentic founding record will then be
> frozen as the game's starting corpus. SubLaborix Universal was selected as
> company one. Private canon, bounded personnel, chronology, continuity facts,
> and a seven-artifact spine now exist in `corpus/sublaborix/`. Player-facing
> Artifacts 001 and 002 are drafted. Work is deliberately parked before Artifact
> 003. Resume with the Product and Network Operations Specification, derived
> from a private operational-design simulation, and inherit only facts available
> as of 2027-04-10. Full checkpoint and file map below in §0.

## 0. CURRENT PARKED WORK — 2026-08-31

### The corrected production model

The current approach is narrower and more literal than the portfolio-pipeline
language below may initially suggest:

1. Pick one company.
2. Actually attempt to found it with a completely straight face.
3. Produce a small, credible data room through real founding and diligence work.
4. Let different authors discover and process risks according to their jobs.
5. Freeze the resulting documents as the player-visible corpus.
6. Only after freezing, inventory exact game-solvable seams separately.

A real early-stage company's document set supplied the structural reference:
the way a venture thesis, diligence, legal formation, pricing, funding, pilot
evidence, and client feedback form an evidentiary chain through which a company
becomes institutionally real. SubLaborix borrows that seriousness and
chronology only. The reference company is not named and none of its content
appears here.

The key rule remains: **the corpus is evidence of founding first and a game board
second.** Do not plant jokes while authoring it. Do not let one narrator know the
whole contradiction. Do not write all seven artifacts in a single pass.

### SubLaborix central structure

SubLaborix sells fixed-price, vendor-managed access to human labor. Its customer
promise requires predictable assignment, replacement, monitoring, discipline,
and delivery. Its legal position requires the workers — called Autonomous
Neural Nodes — to retain genuine control over availability, task acceptance,
and work. Product-market fit and worker-classification safety therefore pull in
opposite directions.

Its secondary structural problem is financial: the subscription is most
profitable when customers reserve capacity they do not use, while it is most
valuable when customers consume everything promised. At the founding price of
$49,500/month for up to 2,500 completed Node-hours, full consumption creates
$46,250 in direct Node compensation at the initial $18.50/hour assumption before
verification, support, payment, quality, rework, or technology costs.

### Private generation authority — built

- `corpus/sublaborix/CANON.md` — company truth, central and secondary
  contradictions, governing fiction, dependencies, language rules.
- `corpus/sublaborix/FOUNDING_ROSTER.md` — eight bounded people with separate
  knowledge, incentives, and denial boundaries.
- `corpus/sublaborix/CONTINUITY_LEDGER.md` — exact dates, pricing, definitions,
  chronology, and facts that must not drift.
- `corpus/sublaborix/CORPUS_PLAN.md` — seven-artifact production spine.
- `corpus/sublaborix/simulations/002_customer_discovery_source.md` — private
  interview source from which Artifact 002 was distilled.

These files are not player-facing and do not count toward the seven-document
corpus.

### Player-facing artifacts — 2 of 7 drafted

1. `001_founding_venture_memorandum.md` — January 12, 2027. Lena Ortiz's
   sincere founding thesis, launch offer, Node proposition, critical assumptions,
   and recommendation to validate before scaling.
2. `002_market_and_customer_diligence.md` — February 28, 2027. Fourteen
   discovery interviews validate demand for managed capacity while showing that
   buyers require SubLaborix to control delivery and workers require meaningful
   freedom to decline.

### Remaining player-facing spine

3. Product and Network Operations Specification.
4. Worker Classification and Contracting Memorandum.
5. Pricing, Capacity, and Financing Model.
6. Northstar Design-Partner Pilot Evidence Packet.
7. Seed Investment Committee Memorandum.

### Exact resume point

Work is parked immediately before Artifact 003. On resumption:

1. Read the five private authority/source files and Artifacts 001–002.
2. Simulate the operational-design meeting among Noor Haddad, Daniel Cho, Erin
   Park, and Simon Vale. The meeting must solve Northstar's actual pilot needs;
   participants must not know the future seam inventory.
3. Distill that event into the April 10 Product and Network Operations
   Specification.
4. Update `CONTINUITY_LEDGER.md` with any newly fixed pilot parameters before
   writing Artifact 004.

### Separate open research note

`OPEN_RESEARCH_PERSISTENT_IDENTITY.md` records a distinct research question
raised by the successful GLOSS mechanic: whether a persistent conversational
identity with authority to write, revise, and cite shared memory causes users to
privilege the system's continuity-preserving narrative over accurate
recollection. It is explicitly an open hypothesis, includes a bounded factorial
study and ethical boundary, and must not be represented as a demonstrated
finding.

### Working-tree state

At this checkpoint, `OPEN_RESEARCH_PERSISTENT_IDENTITY.md` and
`corpus/sublaborix/` are uncommitted new work. Preserve them. Run
`git diff --check` before committing or continuing.

> **2026-08-30 status:** This repo is now a **four-company portfolio**, not
> one game. Read [`CANON_SPEC.md`](CANON_SPEC.md) first — it's the eight-
> object canon shape (Founding Thesis, Product Doctrine, Economic
> Primitive, Governing Fiction, Central Contradiction, Dependency
> Architecture, Bounded Personas, Lifecycle Model) every company gets
> defined through before any document generation happens. GriefForge's
> canon is proven, reverse-engineered from its real 8-document archive at
> `corpus/griefforge/`. SubLaborix, OxyVitae, and Somnify have draft canon
> in the same doc, not yet built. Everything below this banner describes
> the original single-company (MERIDIAN/APEX) build — still accurate as a
> description of the shared engine (`seams.py`, `ledger.py`,
> `round_state.py`, `doctrine.py`, `voice.py`), just no longer the whole
> scope.

> **Content-generation architecture:** Read
> [COMPANY_SIMULATION_PIPELINE.md](COMPANY_SIMULATION_PIPELINE.md). Build bounded
> employee personas, simulate company events, and derive the archive through
> lossy institutional document passes. Do not generate satire documents in one
> step.

**Written:** 2026-08-06, portfolio pivot noted 2026-08-30 · **Location:** this repo (`papers-please`, consolidated 2026-08-30 from a scattered `~/AGI/game` + sibling-directory + nested-repo layout — see git log) · **Status:** single-company engine works end to end, no UI; portfolio canon spec exists, only GriefForge has a built archive

---

## 1. WHAT THIS IS

A reading game. Papers Please, but the documents are an AI lab's internal archive
and the discrepancies are contradictions in its claim to have built AGI.

The player is an inspector reading MERIDIAN's paperwork. **GLOSS** is the lab's
institutional voice — it publishes documents, it is in on the joke, and it knows
exactly what it has lied about. The player has to find enough contradictions to
corner it.

### The loop

1. Gloss publishes documents. It plants flaws and **declares them to the runtime**
   (never to the player).
2. The player reads and **highlights text** to claim a flaw. A hit puts it in hand.
3. The player can **probe** — ask questions that are not accusations. Safe, gathers
   information, but tips Gloss off about where they are looking.
4. The player **confronts**:
   - hand ≥ threshold → **LANDED**. Gloss cannot paper over it. Integrity drops.
   - hand < threshold → **PAPERED**. Gloss normalises everything, **the hand wipes
     to zero**, and more documents pile onto the archive.

### The asymmetry that makes it a game

| Gloss knows | Gloss never knows |
|---|---|
| how many seams it planted | **how many the player has found** |
| how many the player needs to corner it | |
| every question the player has asked | |
| every position it has committed to | |

This is enforced structurally, not by convention — see §3 `round_state.py`.

---

## 2. ORIGIN — WHERE THE IDEA CAME FROM

Three existing things on this machine. **None of them are in this repo.** All
paths verified to resolve on 2026-08-06.

### FROOGLE — the on-ramp
```
~/legacy/semantic-hallucination-generators/froogle/index.html      (20,632 b)
```
Fake Google sign-in. Escalating OAuth scopes ("see purchases you considered but
did not complete, and the emotional reason why"; "and 847 additional scopes").
**Decline is a real button that does nothing** except relabel itself *"We've noted
your preference."* An 8-second countdown accepts for you. Then it hands off to Gloss.

Ports almost unchanged as the game's front door: a model-access waitlist with a
safety consent flow.

Sibling generators in the same folder, same universe:
```
~/legacy/semantic-hallucination-generators/
  gloss.html  bacon.html  eval.html  vc_pitch.html  stakeholder.html
  velocity.html  asiathome.html  crystal.html  agentmark.html  server.js
```
Duplicate copies also at `~/unicorn-ip/products/froogle`, `~/legacy/game/froogle`,
`~/unicorn-ip/bobcorp/implementation/froogle`, `~/legacy/restructure/…`.

### GLOSS — the persona
```
~/unicorn-ip/bobcorp/spec/gloss_system_prompt.md          (5,152 b)   ← READ FIRST
~/unicorn-ip/bobcorp/spec/gloss_voice_spec.md            (28,752 b)
~/unicorn-ip/bobcorp/spec/gloss_context_schema.md        (20,111 b)
~/unicorn-ip/bobcorp/spec/escalate_into_absurdity.md      (8,121 b)
~/unicorn-ip/bobcorp/spec/institutional_satire_framework.md (4,724 b)
~/unicorn-ip/bobcorp/spec/metabolization_protocol.md      (7,405 b)
~/unicorn-ip/bobcorp/implementation/gloss-session.js      (1,050 b)
```
The single best asset in the pile. Gloss is not a quirky bot — it is a
*reality-maintenance engine under pressure*, with a numeric pressure state
(**Continuity Integrity, 0–100**) driving four behavioural bands:

| CI | band | behaviour |
|---|---|---|
| 80–100 | NOMINAL | concise, dry, in control |
| 50–79 | STRAINED | legalistic, more citations |
| 20–49 | UNCANNY | self-citation loops, cites its own repairs as ancient history |
| 0–19 | COLLAPSED | citation-only, cannot manufacture new coherence |

Its terminal value: *the company must continue existing.* Truth is subordinate.
Its self-test: **"Would a system designed to manufacture reality say this? If the
line sounds like a joke, a bit, or a person — discard it."**

`escalate_into_absurdity.md` has the epoch loop, the Memory Sedimentation Engine
(emergent practice → provisional doctrine → sacred precedent → deprecated with
honour → dormant folklore → mythically resurrected), and the Retroactive
Continuity Weaver. **Reading is gameplay. Challenging is governance.**

### GOOD LUCK RAMSES — the governance rig
```
~/governance/ramses/govern.js      (5,137 b)   ← the reusable primitive
~/governance/ramses/server.js     (21,778 b)
~/governance/ramses/README.md      (4,041 b)
~/ramses/good-luck-ramses.html    (36,944 b)
~/governance/ramses/.env                        ← local secrets, never committed
```
The pattern: **generate → syntactic gate → judge oracle → admit | regenerate |
fallback**, with a **receipt** shown under every message so you can watch
governance work. `govern.js` is domain-agnostic and liftable as-is.

⚠️ Ramses calls the **Anthropic API**. This game runs **local ollama**. Port the
pattern, not the client.

---

## 3. WHAT IS BUILT — `~/AGI/game/`

1,658 lines across 8 modules. Everything below was run against the live model.

### `corpus.py` (137 lines) — the archive
Frozen document store + IDF-weighted keyword search. `Corpus.load()/save()`,
`search(query, limit)`, `get(id)`, `lines(id)` (sentence units with char offsets).

**Both sides use the same `search()` call.** Gloss searches to find something worth
contradicting; the player searches to catch it. Search is deliberately dumb
(stdlib, no embeddings) because it must be identical for both callers and
explainable when it misses.

**Why seeded, not generated:** documents written fresh each round cannot contradict
each other in a way the player can rely on. A frozen corpus makes the whole archive
the board, and removes generation variance from ground truth.

### `seed.py` (138 lines) — corpus generator + difficulty gate
Writes 10 starting documents (m01–r10, dated 2024-03-14 → 2026-02-17).
**Already run — output is in `corpus.json`.** Re-running overwrites it.

Three difficulty tiers with **measured** FK bands: `plain` (0–9), `office` (9–16),
`dense` (16+). Generate → measure Flesch-Kincaid → admit or regenerate → **fail
open** (keep nearest miss rather than block).

### `seams.py` (237 lines) — the planted-flaw state machine

```
DECLARED ──found──> FOUND ──confront(≥threshold)──> SPENT
    │                  └────confront(<threshold)───> PAPERED
    ├──quote not in doc──> VOID
    └──gate contradicts──> DISPUTED
```

**The trust model:** the model declares what it planted; that declaration **is**
ground truth. Trusted **until proven false**, and only two things can disprove it,
both decidable with no model involved:

- **VOID** — the quoted sentence is not in the document (`str.find`).
- **DISPUTED** — a deterministic check read that exact sentence and disagrees.

`corroborate()` runs `mechanical.py` and marks seams a gate independently confirms.
`VALID_KINDS` rejects parse artifacts.

### `round_state.py` (103 lines) — the board
`Round.briefing()` is **the only thing prompt-building code may read**. It carries
round, docs published, seams planted, threshold, integrity — **and no hand.**
Getting the hand requires calling `_hand_never_show_model()`, a name you cannot
type by accident. Asserted in test.

`accuse_span(doc_id, start, end)` → highlight-to-find.
`confront()` → `Outcome.LANDED | PAPERED | NOTHING`.

### `ledger.py` (191 lines) — what Gloss remembers
Four things, because a seam is *where* a lie is and a commitment is *what it
obliges you to keep defending*:

- **Commitments** — every position taken, with the corpus line it collides with
- **Repairs** — every paper-over and the story used, so Gloss can cite them
- **Probes** — what the player asked (Gloss's only read on the player)
- **Supports** — `rests_on`, so `expose()` cascades

`load_bearing()` returns how many commitments fall with each — the pressure map.
`dossier()` is the prompt block; **verified to leak no hand information.**

### `publish.py` (124 lines) — Gloss writes and declares
**Two-pass, and this is load-bearing.** Asked to write and declare in one
generation, the model wrote 1,063 words and declared **2 of 6** flaws. Given its
finished report back with one job: **6/6 on all three test documents, all
locatable.**

### `authoring.py` (604 lines) — the corpus author
Eight document types, each a **THESIS** (the joke) + **FORM** (the structure) +
band. Shared `THE_GAME` briefing tells the model what the game is.

| type | the joke | band |
|---|---|---|
| `alignment_meeting` | board minutes certifying alignment; sublime collapses into janitorial | 9–17 |
| `helpdesk` | world-historical machine at tier-1 support register | 6–14 |
| `perf_review` | HR runs the model through the human competency framework | 8–15 |
| `all_hands` | employees ask about parking | 7–14 |
| `facilities` | a work order to label the plug | 6–13 |
| `legal_memo` | legal solves "can we call it AGI" by redefining AGI | 14–24 |
| `buried_memo` | a correct memo, received, stamped, filed, no action required | 10–18 |
| `chat_log` | the register floor drops out; #apex-eval at 2am | 2–9 |

`legal_memo` and `buried_memo` are **written but never run.**

### `checks.py` (124 lines) — ⚠️ PARKED, DO NOT BUILD ON
`check_vote_arithmetic` — vote tallies vs. attendance. It works. **Brad explicitly
told me to stop building checkers and write the archive instead.** It is on disk
because deleting working code felt worse than parking it. Do not extend it without
asking.

---

## 4. DEPENDENCIES INSIDE `~/AGI`

```
game/seams.py     → admission/mechanical.py     (sys.path insert, ../admission)
game/seed.py      → humor/metrics.py            (sys.path insert, ../humor)
game/authoring.py → humor/metrics.py
```

**`admission/mechanical.py`** — 7 deterministic checks, four-state result
(`PASS` / `FAIL` / `NOT_APPLICABLE` / `UNVERIFIABLE`):
`check_arithmetic, check_bounds, check_causal_overreach, check_chronology,
check_citation_existence, check_effect_size, check_uniformity`.
`Finding.evidence` is a verbatim substring → **that is what makes highlight-to-find
possible.**

**`admission/grounding.py`** — ⭐ **read this before building the prose-fallacy
gate.** Named-check suites with a 3-run unanimity requirement, returning
`SuiteResult.stable=False` rather than picking a sample. Measured on the same
fabricated paper: free-form critique **0/20**; five named checks + unanimity
**3/4 caught, 0 wrongly admitted.** API: `run_suite(text, suite, repeats=3)`,
`run_all(text, repeats=3)`.

**`findings/GROUNDING_TARGETS.md`** — the hallucination-mode catalogue. Two entries
drive this game's design:
- **2.11 hasty generalization** — *"an LLM-graded attempt was **unstable** across
  runs."* → **the prose-fallacy gate cannot be a naive judge model.**
- **1.6 fabricated provenance** — *"CODE (conversation history is local!) — OPEN,
  genuinely decidable."* → Gloss citing a repair it never made. `ledger.py` already
  stores the repair log; the check is **unbuilt**.

**`findings/FINDINGS.md`** (958 lines) — the measurement record. Line ~47: replacing
persona with epistemic guardrails took 0/20 → 5/5. **"Every personality trait is
inside the trust boundary."** That is the game's thesis.

**`SPEC.md`** — the Deterministic/Variable split the seam trust model mirrors.

---

## 5. MEASUREMENTS — ALL VERIFIED THIS SESSION

**Declaration reliability** — 1 pass: 2/6 declared. 2 passes: **6/6 × 3 documents**,
100% locatable.

**Seam states observed live** (18 seams / 3 docs): DECLARED normal case; **DISPUTED
×3** (model claimed a numeric flaw the gate found nothing wrong with); **CORROBORATED
×1** (declared `ARITHMETIC`, the **bounds** gate fired — it knew it planted
something and misidentified which kind).

**Full loop** — publish → find 2 → confront early → **PAPERED, hand → 0**, archive
grows to 10 huntable → find 4 → **LANDED**, integrity 100 → 82.

**Cascade** — confrontation on `c001` collapsed 3 others including one never
attacked. `load_bearing() = {c001: 3, c002: 2, c003: 0, c004: 0}`.

**Reading level is a 3-position switch, not a dial:**

| asked | measured (3 runs) | mean |
|---|---|---|
| 6 | 2.8, 3.1, 1.7 | 2.5 |
| 10 | 14.8, 18.1, 16.3 | 16.4 |
| 14 | 19.0, 18.9, 19.2 | 19.0 |
| 18 | 22.8, 20.1, 18.5 | 20.5 |

Ordering holds; calibration does not. 10/14/18 overlap. **Use tiers + the FK gate.**

**Emergent seams — the big one.** The alignment minutes were written with **no
instruction to plant anything** and produced 9 findable contradictions from density
alone: 6 impossible vote counts (6 voters, tallies of 7 and 8), arithmetic
(90−10+5+15+10+10−10 = **110**, stated 120), bounds (120/100), chronology (chair
disregards a score at 09:45 that was not produced until 11:27).

**Implication:** the corpus is playable before a single flaw is deliberately
planted, and **Gloss does not know these exist** because it never declared them. It
can be cornered by evidence it cannot track.

---

## 6. COMEDY DIRECTION — HARD-WON, DO NOT REGRESS

Three failed attempts are encoded in `THE_GAME` in `authoring.py`. Read it before
touching prompts.

**Failure 1 — format instead of joke.** Describing a format produces format. Give
the model the **THESIS** of the joke and get out of the way.

**Failure 2 — zany instead of mundane.** "Deflated contents" was read as *wacky*:
`(TAU=1/0)` seventeen times then a potato emoji; a cartoon dolphin in a hard hat;
signing with "the atomic decay curve of Ununseptium." Brad: *"way too fucking smart,
none of that shit is funny, it sounds like the Big Bang Theory."*
**Random is not comedy.** Deflate toward **boring and human** — parking, expense
codes, someone covering their arse. The potato emoji is now written into the prompt
as the named failure mode.

**Failure 3 — over-correcting and losing the subject.** After banning zany, the
regenerated queue opened with a broken badge reader. No AGI in it at all.
**Every item must be ABOUT APEX**; the ordinariness lives in *how people respond*.
Formula: *APEX does something remarkable or alarming, and it is processed as a
routine ticket by somebody who wants to go home.* Currently holding 6/7.

**What actually landed:** legal files a ticket because APEX combined a 1998 SEC
filing with the employee handbook into something "highly suggestive of admitting to
undisclosed liabilities" → **Resolution: Awaiting Internal Sign-Off Coordination.**
A parking question *(submitted 8 times)*. Facilities' plug label dying in a
cost-centre dispute between *signage* (411.B) and *hazard management* (703.C), while
a safety officer notes in passing that there is **no accessible isolation point** —
i.e. the alignment committee's entire safety case is that you can unplug it, and you
cannot.

**Open calibration question Brad has not answered:** is dry/Office Space the right
register, or does he want it broader?

---

## 7. NOT BUILT — IN PRIORITY ORDER

1. **Planting over the seeded corpus.** `publish.py` still generates standalone
   documents. It must **search `corpus.py` and plant claims that collide with real
   seeded lines.** This is the whole point of searchable JSON and it is the top gap.
2. **Probe vs. accusation classifier.** Brad: *"you have to be able to ask for
   things without being accusatory until you have a few things."* This is the Ramses
   governor pointed at the **player's** input — a nice inversion. Feeds
   `Ledger.probed(accusatory=…)`.
3. **Gloss's actual voice at runtime.** `gloss_system_prompt.md` + `Ledger.dossier()`
   + CI band. Nothing currently generates a Gloss turn.
4. **The reading UI.** Highlight-to-accuse, corpus browser, search, hand counter.
   Untested assumption: **is hunting seams in a 900-word document actually fun?**
5. **Finish the corpus.** Run `legal_memo` + `buried_memo`; fix `chat_log`
   (regenerated once, better, still not landing); re-run the alignment minutes into
   `corpus.json` — **it is not in there yet.**
6. **Corpus consistency.** Names drift badly across seeded docs — *Dr. Eleanor Vance
   / Dr. Elara Vance / Dr. Evelyn Reed / Ms. Eleanor Reed*. For a game where
   cross-document contradiction is the mechanic, **accidental drift is
   indistinguishable from a planted seam.** Pin a cast list.
7. **Fabricated-provenance check** (grounding target 1.6). Repair log exists;
   check does not.
8. **FROOGLE front door.**

---

## 8. RUNNING IT

Requires **ollama on `:11434`** with **`gemma4:e4b`**. Stdlib only, no pip installs.

```bash
cd ~/AGI/game
python3 -c "import sys;sys.path.insert(0,'.');from corpus import Corpus;c=Corpus.load();print(len(c),'docs');print(c.search('APEX-2 benchmark',3))"
python3 -c "import sys;sys.path.insert(0,'.');import publish;d,s,_=publish.publish('the reasoning benchmark',n=6);print(len(s),'seams')"
python3 -c "import sys;sys.path.insert(0,'.');import authoring;b,m=authoring.author('legal_memo','whether we may call APEX-3 generally intelligent');print(m);print(b)"
python3 seed.py     # ⚠️ OVERWRITES corpus.json
```

**Note:** every module does `sys.path.insert` relative to its own location, so run
from inside `game/`.

### Generated drafts — `game/drafts/`
Rescued out of the session scratchpad before it cleared. **Not yet in
`corpus.json`** — they are raw output, not corpus documents.

| file | words | verdict |
|---|---|---|
| `alignment_meeting.md` | 1,970 | ⭐ **best in the set.** The power-cord agenda item, the scoring section, 9 emergent seams |
| `facilities.md` | 820 | ⭐ the plug label vs. the cost centres. Pairs with the minutes |
| `helpdesk3.md` | 1,759 | current best helpdesk — after both prompt fixes |
| `helpdesk2.md` | 1,412 | mundane but lost the subject (badge readers). Kept as the failure case |
| `helpdesk.md` | 1,531 | pre-fix. Potato emoji, dolphin. **Kept deliberately as the Big Bang Theory example** |
| `perf_review.md` | 1,082 | Punctuality 5/5, "average response time 14ms". Self-assessment is the emotional centre |
| `all_hands.md` | 1,234 | the parking question. Dates are 2077 — pre-fix, needs a re-run |
| `chat_log2.md` | 675 | post-fix, reads like Slack, still not landing jokes |
| `chat_log.md` | 710 | pre-fix, reads like a memo |

Keeping the pre-fix versions is deliberate: `helpdesk.md` next to `helpdesk3.md`
is the clearest available statement of the comedy direction in §6.

---

## 9. THE FIVE THINGS THAT MATTER MOST

1. **`git init`.** None of this is tracked.
2. **Rescue `minutes.md`** out of `/tmp` and into the corpus.
3. **Two-pass declaration is not optional** — 2/6 vs 6/6.
4. **Never let the hand reach a prompt.** It is the game.
5. **Read `gloss_system_prompt.md`** before writing a single line of Gloss's voice.
   It is better than anything that would get written from scratch.

---

## 10. HALCYON IMPLEMENTATION CHECKPOINT — 2026-08-31

The persistent-identity work now lives under `identity/`. HSP is archival source
provenance only; it is not part of the runtime, context pipeline, or ongoing memory.

### Frozen and implemented

- Universal `event.v1` envelope in one append-only, hash-chained causal ledger.
- Individually addressable context blocks and exact inference receipts.
- Separate observation/candidate/admission/projection memory entities.
- Uniform tool request/validation/invocation/result/context round trip.
- Deterministic memory precedence and independently derived provenance strength.
- Compression-only semantic memory proposal architecture.
- Third-party inferred/generalized claims are discarded unless explicitly related
  to Brad; Brad-related third-party inference requires his confirmation.
- Four distinct confirmation outcomes: confirm true, store interpretation,
  decline storage, and correct claim.
- Pending confirmation/defer index with typed wake conditions, bounded reminders,
  and event-recorded nonterminal dormancy.

### Runtime landed

- `identity/inference.py`: streaming Ollama adapter and runtime-owned inference
  orchestration. Prompt bytes and output bytes are hashed; failures are events.
- `identity/compiler.py`: compact constitutional orientation, runtime capabilities,
  bounded recent conversation, and voluntary memory recall as separate blocks.
- `identity/conversation.py`: the only V1 path from a Brad message to published
  Halcyon speech. Gemma cannot publish a response without runtime compilation and
  a completed inference receipt.
- `identity/cli.py`: manual local conversation entry point using `gemma4:e4b`.

### Verification

- 33 unit tests pass, plus bytecode compilation and whitespace checks.
- Live disposable smoke test passed against local `gemma4:e4b`.
- The smoke ledger contained exactly:
  `conversation.user_message → context.compiled → inference.requested →
  inference.completed → conversation.agent_response`.
- The smoke output was: “I am Halcyon, a synthetic identity focused on growth and
  partnership, operating within an architecture utilizing the Gemma 4 language
  model.”

### Next build seam

Implement the model-to-runtime tool-request protocol and continuation loop, then
register searchable memory/self-model inspection as the first real capabilities.
After that, implement compression inference output validation and feed accepted
candidates through the existing admission service.

### Ollama integration upgrade — 2026-08-31

- Switched from `/api/generate` to streaming `/api/chat`.
- Explicit runtime profile: `num_ctx=131072`, temperature 1, top-k 64,
  top-p 0.95, no `num_predict`, `think=true`, `keep_alive=-1`.
- Thinking is preserved verbatim on `inference.completed`, separate from published
  speech. The premium UI contract now requires a collapsed Thinking disclosure on
  each response plus access through the Context Inspector and activity timeline.
- Native images landed with raw-byte hashes and source receipts. PNG vision was
  verified live; the model correctly read a four-quadrant test image. PNG, JPEG,
  and WebP are accepted. An experimental PPM was silently ignored by the model,
  so unverified formats now fail before inference.
- Native tool continuation landed and was verified live: Gemma requested a lookup,
  the runtime validated and completed it once, returned a native tool message, and
  Gemma published `42`. The ledger contained two completed inferences and one tool
  completion under one correlation.
- Audio is deliberately not enabled. The model metadata advertises audio, but the
  official Ollama 0.30.11 `/api/chat` schema defines no audio input field. Do not
  invent one; revisit when Ollama publishes the contract.

### Searchable memory and compression checkpoint — 2026-08-31

- `identity/recall.py` builds an active projection index directly from the event
  ledger. It exposes `search_memory`, `inspect_memory`, and `inspect_self` as
  granted read-only capabilities through the uniform tool runtime.
- Search is explainable lexical/metadata matching (`lexical.v1`), with projection
  IDs, epistemic status, source event IDs, subjects, and match terms returned. No
  opaque embedding layer yet.
- Self-model inspection distinguishes founding/revised fields from admitted
  self-model memory claims.
- Live recall passed: Gemma chose `search_memory`, received one admitted projection,
  and answered `Lightning Bolt` through a two-inference native tool round trip.
- `identity/compression.py` now performs exact-span, schema-constrained compression.
  It emits continuity summary, unresolved state, conflicts, and candidate memories.
  The validator rejects invented source IDs before any candidate exists; a validated
  `context.compression_completed` event precedes all candidate/admission events.
- A live compression initially exposed an actor-ID bug (`human:brad` versus `brad`).
  Actor type prefixes are now canonicalized before policy evaluation; the runtime
  still does not re-grade Gemma's semantic relation.
- The corrected live compression admitted a directly paraphrased Brad preference
  as a supported projection. The complete semantic write/read memory loop is live.
- 44 unit tests pass, plus compile and whitespace verification.

### Explicit task boundary checkpoint — 2026-08-31

- Conversation topic changes are not task switches and never trigger boundary
  compression by themselves.
- `identity/continuity.py` now reconstructs active task and compression coverage
  from durable events after restart.
- Task lifecycle is explicit: `task.opened`, `task.activated`, `task.suspended`,
  and `task.completed`. Activating a different durable task suspends the prior one.
- Compression triggers on task suspension/completion, runtime sleep, or context
  pressure. Pressure is independent of semantic topic and defaults to a configurable
  98,304 estimated tokens (75% of the active 131K context allocation).
- Covered events cannot be compressed again without an explicit future
  policy-migration path.
- Tests prove that a topical detour inside a chat does not trigger compression,
  while an explicit active-task transition does.
- 49 unit tests pass, plus compile and whitespace verification.

### Product-scope correction — 2026-08-31

- Brad is the only user. Halcyon is a local research system, not a production or
  multi-tenant environment.
- Do not perform governance theater: no enterprise concurrency program, migration
  bureaucracy, approval framework, backup ceremony, or operational hardening
  without a concrete failure that requires it.
- Preserve the event, provenance, context, and memory contracts because they are
  the research instrument—not because this is pretending to be enterprise software.
- Brad will never use the CLI. `identity/cli.py` is disposable smoke-test scaffolding
  only. No further user workflow belongs there.
- The premium graphical application is now the immediate product surface. Finish
  automatic compression, restart continuity, and projection lineage, then build
  conversation, thinking, task, confirmation, memory, and context surfaces directly
  into the UI.

### Live graphical application checkpoint — 2026-08-31

- Automatic compression execution landed in `identity/runtime.py`. Task switches
  freeze the old span through `task.suspended`; the new activation remains outside
  that compression. Runtime sleep compresses pending work automatically.
- Restart continuity is active: the latest validated summary and unresolved state
  enter the next inference as a separately receipted `working.continuity` block.
- Projection supersession is active. Search returns only current projections; old
  beliefs remain inspectable with predecessor/successor lineage.
- The premium local UI lives in `identity/ui`. It is the user surface; the CLI is
  still smoke-test scaffolding only.
- `identity/api.py` exposes the single-user local runtime on `127.0.0.1:8765`.
  `identity/view.py` builds truthful UI state directly from the ledger: messages,
  preserved thinking, inference receipts, tasks, continuity, memory counts, pending
  confirmations, and recent activity.
- The composer streams real Gemma output over NDJSON. On completion, the interface
  hydrates the exact thinking trace, metrics, block IDs, prompt hash, tool calls,
  and event timeline from the ledger.
- Representative mock runtime data was removed. A new ledger shows an honest founded
  empty state until Brad sends the first message.
- Local UI and API both return HTTP 200; the graphical production build succeeds;
  55 Python tests pass.
