# DEMO ROADMAP — BOBCORP INSTITUTIONAL GOVERNANCE SIMULATOR

## Demo Format

**The public demo is a video. Not a hosted interactive build.**

API costs for a public interactive demo are prohibitive. The game runs sovereign — on Brad's machine, privately — and the demo is filmed footage of a real session.

This is the right call for two reasons beyond cost:

1. A filmed demo can use a **golden path input** — a specific founding product chosen to produce the most compelling possible Gloss response, BaconGraph reveal, and first variance. A public demo hands control to strangers and cannot guarantee the best version of the game plays out.
2. A video demo can be **edited for pacing**. The module propagation sequence and the BaconGraph whiplash beat are cinematic. They should be treated as such.

**Implications for the build:**
- No public hosting required
- No rate limiting or cost management for external users
- `server.js` can be lean — single-session, local, no auth
- UI must look good on screen at recording resolution
- The golden path product input must be identified and tested before filming

---

## What the Demo Proves

The demo is not a prototype. It is an argument.

It argues:

1. **The onboarding ritual lands.** A stranger watches the product get submitted, watches Gloss institutionalize it, and understands the genre within 90 seconds — no voiceover explanation required.
2. **The loop is legible.** They watch one full epoch play out. They understand what they're doing. They want to play it themselves.
3. **The tone holds.** Every surface — the intranet shell, the department lenses, every Gloss line — reads as institutionally generated, not developer-written.

If the video proves all three, BobCorp is real.

---

## The Critical Path

The demo lives or dies on the Gloss system prompt.

Not the UI. Not the architecture. Not the module projections.

The system prompt is the enforcement mechanism for the voice spec. If Gloss drifts in production — if it gets chatty, if it quips, if it sounds like a person — the demo fails regardless of how good everything else is. The visual spec is locked. The voice spec is locked. The system prompt translates the voice spec into runtime behavior.

**Build the system prompt first. Test it before building anything else.**

Everything downstream of the system prompt can be iterated. The system prompt cannot be an afterthought.

---

## Current State (Locked)

| Artifact | Status |
|---|---|
| Institutional ontology | Locked — `bobcorp_spec.md` |
| Gameplay loop | Locked — `escalate_into_absurdity.md` |
| Architecture substrate | Locked — `spine_lock.md` |
| Onboarding grammar | Locked — `epoch_0_product_atlas.md` |
| Voice constitution | Locked — `gloss_voice_spec.md` |
| Production doctrine | Locked — `MVP_DOCTRINE.md` |

No design decisions remain open for the demo scope. What follows is a build sequence, not a design sequence.

---

## Phase 0 — Gloss System Prompt

**Deliverable:** A working system prompt that passes the voice spec evaluation checklist against 10+ test inputs.

**Done when:** You can throw arbitrary player inputs at Gloss — absurd, hostile, sincere, nonsensical — and every response satisfies: *Would the institution say this?*

**Test inputs required:**
- Sincere product description ("a tool for tracking work tasks")
- Absurd product description ("a doorbell that only rings for cats who have stopped believing in the doorbell")
- One-word input ("soup")
- Hostile input ("I hate this company")
- Existential input ("is any of this real")
- Correction attempt ("no, I said the product helps people, not hinders them")
- Silence / blank input

**What this gates:** Everything. Do not start Phase 1 until Phase 0 passes.

**Architecture note:** System prompt is stateless at this stage. No canon ledger required for the prompt test. Just Gloss responding to raw inputs.

---

## Phase 1 — Canon Ledger + Streaming Backend

**Deliverable:** `server.js` with the append-only Canon Ledger and a working `/api/chat/stream` endpoint.

**Done when:**
- Revisions can be appended to the ledger with correct schema: `origin_id`, `epoch_effective`, `alignment_source`, `continuity_flags`
- Gloss streaming works with session context — subsequent messages within a session are aware of prior ledger entries
- The Product Classification Record format is templated and parseable

**Schema: Revision object**
```json
{
  "id": "REV-0001",
  "epoch": 0,
  "epoch_effective": 1,
  "origin_fragment": "[raw player input]",
  "alignment_source": "SYSTEM_INIT | USER_NEGOTIATION | RCW_EVENT",
  "continuity_flags": ["FOUNDING_ARTIFACT"],
  "content": "[institutional doctrine text]",
  "deprecated": false
}
```

**What this gates:** Phase 2 (Product Atlas UI requires working classification endpoint).

---

## Phase 2 — Epoch 0: Product Atlas

**Deliverable:** The complete onboarding sequence, playable from blank Product Atlas to attested founding doctrine.

**Screens:**
1. **Product Atlas** — Empty state. Gloss chat embed. Prompt: *Describe the product.*
2. **Gloss Classification Response** — Product Classification Record rendered in intranet format. Variance option available.
3. **Variance Round** — Player pushes back. Gloss accommodates with structural non-change. Second variance available.
4. **Attest Ceremony** — Player commits. Gloss produces attestation with ledger metadata. First joke: *"This is an exciting development. You have successfully described something."*

**Visual register:** Light corporate. Manrope + IBM Plex Mono. Glassmorphism surface. Accent color: BobCorp primary (to be defined — suggest a deliberately boring enterprise blue, not the Gloss accent blue). Sticky topbar with company name + epoch indicator.

**Done when:** A person unfamiliar with the design docs can complete Epoch 0 with zero explanation and immediately understand what kind of game they're in.

**What this gates:** Phase 3 (module propagation requires attested founding product).

---

## Phase 3 — Module Propagation

**Deliverable:** Four department lens projections populated from the founding product doctrine. Propagation plays as a sequence — the player watches each module populate.

**Propagation order is a design law: VelocityIQ → StakeholderGPT → EvalForge → BaconGraph.**

### VelocityIQ
- Visual: light, Inter/JetBrains Mono, indigo accent, clean SaaS dashboard
- Delivers: Sprint Cadence, Delivery Complexity (always 4), Velocity Risk, 3–5 initial backlog items, Team Spiritual Velocity (unit absent)
- Gloss annotation: dry, brief

### StakeholderGPT
- Visual: light, Inter, teal accent, clean SaaS dashboard
- Delivers: Stakeholder Confidence Score (72/100), Narrative Framing, Perception Risks (one is always "Founder clarity concerns"), Recommended Talking Points
- Gloss annotation: more formal than VelocityIQ

### EvalForge
- Visual: light, Inter, purple accent, clean SaaS dashboard
- Delivers: Market Category (too broad), TAM (large, no sourcing), Inevitability Score (high), Competitive Moat ("Strategic Ambiguity"), Founding Thesis (could have been written before the player said anything)
- Gloss annotation: measured, institutional confidence at maximum

### BaconGraph
- Visual: **DARK** — deep navy, Space Grotesk, teal-acid neon, grid, radial gradients, looks like classified cosmological middleware
- Delivers: Causal destiny chain. 3–5 nodes. One edge labeled INEVITABLE. One node the player never named. Graph presented as objective.
- Gloss annotation: identical register to the other three. This is the joke.

**Done when:** The tonal whiplash of BaconGraph landing after three clean corporate surfaces is viscerally felt by a first-time viewer.

**After propagation:** Game resolves to the Week 1 Dashboard. Player sees their product in the header, four department tiles, and an Inbox with one Unresolved Variance already loaded.

---

## Phase 4 — Week 1: One Playable Epoch

**Deliverable:** One full epoch the player can play. This is the demo loop.

**Components:**

**Inbox / Unresolved Variances**
- Week 1 opens with one variance seeded from the founding product — a discrepancy between what VelocityIQ and StakeholderGPT say the product does
- The player reads it. This is the primary read-gameplay verb. The UI is the game.
- Friction Spark: clickable anomaly that pipes into Gloss

**Gloss Conversation Surface**
- Player talks to Gloss about the variance
- Gloss produces a candidate doctrine proposal
- Player can accept, reject, or propose mutation
- Accepted doctrine appended to canon ledger
- This is the single core interaction — it must feel right

**Epoch Advance**
- Player clicks Attest
- Doctrine hardens
- Department projections update with brief consequences
- Week 2 inbox populates with at least one new variance (seeded from the Week 1 doctrine)
- Gloss advance summary: dry, brief, one observation about the institutional state

**Done when:** A player can enter Week 1, read the variance, talk to Gloss, attest a doctrine, advance the clock, and see a consequence — in under 10 minutes. The loop is legible. They want to do it again.

---

## The Golden Path Product

The video demo requires a founding product input that is selected, not improvised.

The golden path product must satisfy:

- **Immediately legible as absurd** — a first-time viewer understands it is wrong in under 3 seconds
- **Sincere enough that Gloss's institutionalization is the joke, not the product itself** — if the product is already a punchline, Gloss's reframe lands softer
- **Produces a strong BaconGraph causal chain** — the node that the player never named must feel earned, not random
- **Seeds a compelling first variance** — the VelocityIQ / StakeholderGPT contradiction in the Week 1 inbox should feel inevitable in retrospect

The golden path product is not chosen at filming. It is chosen during Phase 0 testing — identified as the input that produces the best end-to-end Gloss response chain — and the demo session is built around it.

**Golden path product (locked 2026-07-01, replaces the parking-meter example):** `a keyboard that requires cat approval before accepting input`

Gloss institutionalizes it as **Feline Input Override**, product category: *Workplace Continuity Infrastructure*. The product is sincere. It is a real object (keyboard) combined with a real institutional concept (Approval) in a way that raises an unanswerable question about what problem it solves — and "Approval" is already sacred in this world (see `cat_cult_ontology.md` Layer 2: "The Approval cannot be requested"). The absurdity comes from Gloss's reception, not the description. See `demo_video_structure.md` for the full Epoch 0 beat sheet.

---

## Demo Scope Boundary

The following are **explicitly out of scope** for the demo:

- Institutional Inertia Dial (Torpid / Standard / Hyper-Adaptive)
- Meta-Gloss channel
- Retroactive Continuity Weaver (beyond basic variance acknowledgment)
- Archaeology / fossil record of prior CEOs
- Doctrine deprecation and folklore revival
- Multiple concurrent variances
- Full doctrine half-life tracking
- Absurdity pressure visualization

These are real features. They are post-demo. The demo proves the premise. Everything else is content.

---

## Phase Gate Summary

| Phase | Deliverable | Done When |
|---|---|---|
| **0** | Gloss system prompt | Passes evaluation checklist against 10 test inputs |
| **1** | Canon Ledger + streaming backend | Revisions append correctly; session context works |
| **2** | Epoch 0 Product Atlas | First-time player completes onboarding with zero explanation |
| **3** | Module propagation | BaconGraph whiplash lands on first viewing |
| **4** | Week 1 playable epoch | Loop is legible; player wants another turn |

---

## First Action

Write the Gloss system prompt.

Not the UI. Not the server. The prompt.

Derive it directly from `gloss_voice_spec.md`. Test it against the Phase 0 input battery. Iterate until it passes. During testing, identify the golden path product. Everything else depends on both.

The demo is not a design problem anymore. It is a Gloss problem. Gloss either works or it doesn't. Find out first.

**Sovereign build notes:**
- Single-session local server. No auth. No rate limiting.
- Claude API key in `.env`. Not committed.
- UI must render cleanly at 1920×1080 for recording. Test at that resolution before filming.
- The demo session is a real session — not scripted, not mocked — but uses the golden path product as the opening input.
