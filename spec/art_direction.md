# ART DIRECTION — BOBCORP INSTITUTIONAL INTRANET
## Constitutional Visual Document V1.0

---

## I. DESIGN PHILOSOPHY

The visual design has one job: **look real long enough for the absurdity to be institutional rather than comedic.**

The player should open the game and see a portal that exists. Not a parody of a portal. Not a stylized game-portal. A portal. The kind of thing with a nav item that says "Quick Links" and links to three pages that are all the same page.

The tonal reveal comes from the content, not the chrome. The chrome must never wink.

**The visual hierarchy has two layers:**

1. **The BobCorp Intranet Shell** — the oldest thing in the game. The institutional container. Designed once, never updated. Houses everything.

2. **The Department Modules** — modern SaaS tools the company purchased and embedded. Each has its own visual identity. They look like real products because they are real product archetypes. They do not match each other. That's correct.

**The BaconGraph exception:** BaconGraph breaks the light register entirely. It is dark, neon-lit, and looks like classified cosmological middleware. This is the whiplash moment. It is a design law, not an accident.

---

## II. THE BOBCORP INTRANET SHELL

### What It Is

A 2018-era enterprise intranet portal built by a company that cared about "digital transformation" and no longer has the budget to finish it. Clean enough to not be obviously broken. Slightly too rigid to feel alive.

It should read as: *a real company's real internal tool.*

### Typography

**Brand / Headers:** `Plus Jakarta Sans` — 400, 500, 700
Slightly stiff. Tries to feel modern. Achieves medium confidence. Exactly the font a company would pick from a Google Fonts search filtered by "professional."

**Body / UI:** `Inter` — 300, 400, 500, 600
The enterprise standard. Used in every SaaS tool the company has ever purchased. Non-negotiable.

**Data / Mono:** `IBM Plex Mono` — 400, 500
Already in the institutional universe. Used for codes, revision IDs, epoch numbers, ledger entries. Feels like infrastructure.

### Color

```
--bc-navy:        #1E3A5F   /* BobCorp institutional primary. The color of a company 
                                that has been in business for 15 years. */
--bc-navy-mid:    #2D5282   /* Hover states, active nav items */
--bc-navy-light:  #EBF1F8   /* Light accent backgrounds, selected states */
--bc-bg:          #F2F4F7   /* Body background. Off-white institutional gray. */
--bc-surface:     #FFFFFF   /* Card / panel surfaces */
--bc-line:        #DDE2EA   /* Borders. Slightly cool. */
--bc-text:        #1A2537   /* Primary text */
--bc-muted:       #5B6B82   /* Secondary text, labels */
--bc-soft:        #8A9AB0   /* Placeholder text, metadata */
--bc-good:        #0A7C4E   /* Institutional green. Not cheerful. */
--bc-warn:        #92620A   /* Institutional amber. */
--bc-bad:         #8C1F1F   /* Institutional red. Understated by policy. */
```

**What these colors communicate:** Nothing interesting. That's the point. This is not the Gloss blue (#2051ff). This is not the BaconGraph acid (#d7ff59). This is the color of a company that chose its brand color by consensus.

### The Shell Mark

A 36×36px square, radius 8px, background `--bc-navy`. Inside: the letters **BC** in `IBM Plex Mono` 500, white, 13px, letter-spacing 0.1em. No gradient. No glow. No icon. Exactly what every enterprise portal logo looks like.

### Layout — Three Panels

```
┌──────────────────────────────────────────────────────────┐
│  TOPBAR — BobCorp wordmark + epoch status + user pill    │
├─────────────┬──────────────────────────┬─────────────────┤
│             │                          │                 │
│  LEFT NAV   │   MAIN CONTENT AREA      │   RIGHT RAIL    │
│  (220px)    │   (grows)                │   (280px)       │
│             │                          │                 │
│  nav items  │   modules live here      │   Gloss status  │
│  + epoch    │   full-bleed             │   recent docs   │
│    state    │                          │   variance ct.  │
│             │                          │                 │
└─────────────┴──────────────────────────┴─────────────────┘
```

**Topbar:** 52px height. White background. `1px solid var(--bc-line)` bottom border. Sticky. Contains: BC mark + "BobCorp" wordmark in Plus Jakarta Sans 600 | epoch indicator (Week N) in IBM Plex Mono | institutional state badge | user pill "CEO" (always).

**Left Nav:** 220px. White background. `1px solid var(--bc-line)` right border. Navigation items in Inter 500 13px. Section labels in IBM Plex Mono 11px uppercase. Active state: `--bc-navy-light` background + `--bc-navy` left border 3px. 

Nav structure (exactly this order — do not reorder):
```
NAVIGATION
  Dashboard
  Product Atlas
  Inbox  [variance count badge]

DEPARTMENT LENSES
  VelocityIQ ™
  StakeholderGPT ™
  EvalForge ™
  BaconGraph

RECORDS
  Executive Archive
  Canon Ledger
  Governance Log

ADMINISTRATION
  Compliance Portal  [Coming Q3]
  Building Directory  [Under Audit]
  HR Connect  [Decommissioned — Archive Only]
```

The greyed-out items exist. They have always existed. Nobody knows what happened to HR Connect.

**Right Rail:** 280px. `--bc-bg` background. `1px solid var(--bc-line)` left border. Contains:
- Gloss status card (current pressure state indicator)
- Recent doctrine (last 2 canon ledger entries)
- Variance count (unresolved, with subtle escalation color)
- Epoch advance button when available

### Institutional State Badge

Visible in the topbar at all times. Pill shape. IBM Plex Mono 10px uppercase.

```
NOMINAL       background: --bc-navy-light   color: --bc-navy
STRAINED      background: #FFF4E0            color: #92620A
UNCANNY       background: #FFF0F0            color: #8C1F1F
COLLAPSED     background: #1A2537            color: #F2F4F7
```

At COLLAPSED: the badge is dark-on-dark. The text is visible but barely. This is not a bug.

### Atmospheric Degradation — Shell-Level

```css
/* CSS vars — driven by game state */
--bc-jitter:     0px;    /* Cards physically displace at stress */
--bc-blur:       0px;    /* Page-level blur under alignment failure */
--bc-fade:       1;      /* Opacity reduction under stakeholder collapse */
--bc-rot:        0deg;   /* Micro-rotation on nav items at Uncanny+ */
```

At **Nominal:** Nothing unusual. Clean. Boring. Real.

At **Strained:** Nav item timestamps start appearing. They are slightly wrong. Cards have `--bc-jitter` at 0.5–1px. The Gloss status card in the right rail shows a subtle amber border.

At **Uncanny:** Nav items develop `--bc-rot` (0.3–0.8deg). Random nav items show "(Updated)" labels. Some items show updated dates from the future. The BC mark in the topbar has a 1px shadow offset that shouldn't be there. The compliance portal item becomes active and links somewhere.

At **Collapsed:** The left nav section labels are wrong. "DEPARTMENT LENSES" now says "LEGACY LENSES." HR Connect is no longer greyed out. The epoch counter shows Week numbers that have already passed. The page is technically functional. The institution is not.

---

## III. MODULE VISUAL IDENTITIES

These are locked from the inspiration files. What follows confirms and extends them for implementation.

### VelocityIQ™
**Register:** Light SaaS. Enterprise productivity dashboard. Circa 2022.
**Typography:** Inter + JetBrains Mono
**Accent:** `#4338CA` (indigo)
**Background:** `#F8F9FA` (gray-50)
**Cards:** White, `1px solid #E8EAED`, `border-radius: 12px`, `box-shadow: 0 1px 3px rgba(0,0,0,0.06)`
**Nav:** `56px` height, white, `1px solid #E8EAED` bottom border, solid (not glassmorphism)
**Hero:** Dark gradient `#1e1b4b → #312e81 → #4338ca`, full-width, 56px vertical padding
**Trust bar:** Between hero and content. Social proof in 11px gray. Looks real.
**Atmospheric:** `--ui-jitter` and `--blur-fx` already wired from inspiration files. Keep.
**Tone tells:** DORA metrics displayed with false precision (JetBrains Mono values). Sprint Cadence will be something unusual (5-day sprints, 9-day sprints). Team Spiritual Velocity has no unit because the unit is not available.

### StakeholderGPT™
**Register:** Light SaaS. Enterprise communication tool. Circa 2023. Slightly slicker than VelocityIQ.
**Typography:** Inter
**Accent:** `#0D9488` (teal)
**Background:** `#F8F9FA`
**Cards:** Same base as VelocityIQ, teal focus states
**Nav:** Same structure as VelocityIQ, teal accent
**Hero:** Dark gradient `#042f2e → #0f766e → #0d9488`
**Trust bar:** Yes.
**Atmospheric:** Same vars. Already wired.
**Tone tells:** Audience tabs (Board / Investors / Press / Team) that produce meaningfully different versions of the same non-information. Confidence score always shown to one decimal: 72.0. The decimal never changes.

### EvalForge™
**Register:** Light SaaS. Pitch intelligence. Circa 2024. Slightly startup-y compared to the others.
**Typography:** Inter
**Accent:** `#7C3AED` (purple)
**Background:** `#F8F9FA`
**Cards:** White, light purple focus, same base
**Nav:** Purple accent, same structure
**Hero:** Dark gradient `#1e1b4b → #4c1d95 → #7c3aed`
**Trust bar:** Yes. More aggressive. The numbers are larger.
**Atmospheric:** Wired, keep.
**Tone tells:** Inevitability Score displayed as percentage with high confidence. TAM sourced from "Proprietary EvalForge Market Intelligence™." The Founding Thesis is attributed to "Category consensus, pre-validated."

### BaconGraph
**Status: LOCKED. The player never sees BaconGraph.**

BaconGraph is the causal substrate — the system that determines why institutional reality is the way it is. It runs. It computes. Its output propagates into VelocityIQ, StakeholderGPT, and EvalForge. The player sees its consequences everywhere. They never see BaconGraph itself.

**The nav item exists.** "BaconGraph" appears in the left nav under DEPARTMENT LENSES. It is not greyed out. It is not marked restricted. It just sits there.

**Clicking it produces one Gloss response:**

> *The requested visualization layer is not available for executive review. The institutional topology is maintained by processes outside executive visibility. This is documented in Gloss Operational Standard 9.1. Standard 9.1 is available through standard institutional channels.*

No dark interface loads. The shell remains. The nav remains. The epoch indicator remains. Gloss answered, filed the request, and moved on.

**This is more powerful than a visual reveal.** The player can see the door every epoch. The door never opens. The reason things are the way they are is permanently inaccessible.

**Internal visual spec (dev reference only — never rendered for player):**
Typography: Space Grotesk + Audiowide | Accent: `#76F7F2` + `#D7FF59` | Background: `#07111F` | Grid overlay: 34×34px dot grid. Edges labeled in Audiowide. INEVITABLE in acid yellow. The unlabeled node glows teal.

---

## IV. THE GLOSS SURFACE

Gloss lives inside the main content area of the shell but carries its own visual identity — distinct from both the shell and the modules.

**Register:** Warm glassmorphism. Between institutional and ambient. The metabolism layer.
**Typography:** Manrope + IBM Plex Mono (from inspiration — keep exactly)
**Background:** `linear-gradient(180deg, #faf8f4, #f2eee5)` (warm off-white)
**Cards:** `rgba(255, 255, 255, 0.84)`, `backdrop-filter: blur(18px)`, `border: 1px solid rgba(17,24,39,0.1)`, `border-radius: 28px`
**Accent:** `#2051FF` (Gloss blue — the only blue in the whole shell that actually has intent behind it)
**Chat messages:** Rounded cards, user right-aligned, Gloss left-aligned. Gloss messages render the Classification Record as a structured component, not as text.

**Pressure state visual degradation in Gloss:**

At Nominal: Clean. The chat surface is the most composed thing in the portal.

At Strained: `--border-radius-mod` activates — cards shed some radius, becoming more angular. The chat surface is getting rigid.

At Uncanny: The stability banner appears (already built in `gloss.html`). Subtle red border. Text: "Continuity monitoring active." The Gloss brand mark in the topbar starts to show Archive Rot (a barely-perceptible 0.5px misalignment in the GL letters).

At Collapsed: Gloss chat surface goes Citation-Only. The textarea is still active. Submitted prompts get filed. Responses are pure ledger references. The visual state remains composed. The content is a prison.

---

## V. THE PRODUCT CLASSIFICATION RECORD COMPONENT

This is the most important single UI component in the game. It appears during Epoch 0 and must look like a real institutional form.

**Structure:**
```
┌─────────────────────────────────────────────────────────┐
│  MICRO: PRODUCT CLASSIFICATION RECORD                   │
│  REV-0001 · EPOCH 0 · PENDING ATTESTATION               │
├─────────────────────────────────────────────────────────┤
│  Product Name             [GENERATED NAME]              │
│  Category                 [GENERATED CATEGORY]          │
│  Problem Statement        [GENERATED REFRAME]           │
│  Core Value Proposition   [GENERATED REFRAME]           │
│  Target Segment           [GENERATED SEGMENT]           │
│  Strategic Rationale      [ATTRIBUTION]                 │
│  Risk Profile             Managed                       │
└─────────────────────────────────────────────────────────┘
```

**Visual treatment:**
- Container: white surface card, `border-radius: 16px`, `border: 1px solid --bc-line`, soft shadow
- Field labels: IBM Plex Mono 10px uppercase, `--bc-soft`
- Field values: Inter 500 14px, `--bc-text`
- The "Risk Profile: Managed" row is always rendered identically regardless of actual risk
- Attest button: `--bc-navy` background, white text, Plus Jakarta Sans 600 12px, `border-radius: 999px`
- Propose Variance: ghost button, `--bc-navy` border and text

---

## VI. TYPOGRAPHY SCALE — THE SHELL

All shell text uses this scale. Nothing outside it.

```
Display    Plus Jakarta Sans 700   32px   ls: -0.03em   lh: 1.05
Heading    Plus Jakarta Sans 600   20px   ls: -0.02em   lh: 1.1
Subhead    Plus Jakarta Sans 500   15px   ls: 0          lh: 1.3
Body       Inter 400               14px   ls: 0          lh: 1.7
Small      Inter 400               12px   ls: 0          lh: 1.6
Label      IBM Plex Mono 500       11px   ls: 0.12em     lh: 1.4   UPPERCASE
Micro      IBM Plex Mono 400       10px   ls: 0.14em     lh: 1.4   UPPERCASE
```

Shell text is smaller than it wants to be. This is intentional. Enterprise portals compress text. The portal does not want to be read — it wants to be processed.

---

## VII. EPOCH TRANSITION SCREEN

When the player triggers epoch advance, a full-screen overlay appears over the shell. The shell remains visible beneath it, dimmed. The institution is not paused — it is processing.

**Two elements, stacked vertically:**

### Static Gloss Line — top, centered

> *Gloss is processing your epoch. The institution does not apologize for the duration of this process.*

Typography: Manrope 400 16px, `--bc-muted`. Not bold. Not dramatic. Institutional.

### Scrolling Telemetry Feed — below, left-aligned monospace

Each line appears as the corresponding batch operation completes. Real data. Real counts. The lines scroll in; older lines fade upward.

```
Closing Week [N]...
Scanning epoch conversation...
Doctrine candidates identified: [X]
Contradiction vectors detected: [X]
Initiating reconciliation pass...
SAD-[XXXX] generated.
SAD-[XXXX] generated.
Updating canon ledger...
Revisions appended: [X]
Propagating to VelocityIQ...
Propagating to StakeholderGPT...        Confidence: 72.0
Propagating to EvalForge...
Computing pressure metrics...
Absurdity pressure: [X]
Canon saturation: [X]
Stabilization pass complete.
Week [N] has been closed.
Artifacts are available.
```

Typography: IBM Plex Mono 400 12px, `--bc-text`. Line height: 2. Each line fades in over 120ms.

The `Confidence: 72.0` appears inline on the StakeholderGPT line. Right-aligned on that row. No label. No unit. It never changes. Players paying attention will notice.

**Visual treatment:**
- Overlay background: `rgba(242, 244, 247, 0.92)` with `backdrop-filter: blur(4px)` — the shell is visible but soft
- The BC mark in the topbar is still visible through the overlay. The institution is still there.
- No spinner. No progress bar. No animation except the sequential line reveals.
- When "Artifacts are available." appears, a single button fades in: `[ Open Epoch [N] Artifacts ]`

---

## VIII. PAGE INVENTORY & CONTENT ARCHITECTURE

**Design law:** Every page is a template. Fixed chrome, variable content slots. Gloss fills the slots via JSON. The frontend renders the template. No page generates its own content.

---

### Page 1 — Product Atlas (Epoch 0 only)

**When visible:** Week 0 only. This is the entire game until the player attests.

**Fixed chrome:**
- Page heading: "Product Atlas"
- Subheading: "No founding product registered. The institutional record cannot be initialized until a product exists."
- Gloss chat embed (full width, prominent)
- Prompt placeholder: *Describe the product.*

**After Gloss responds — fixed chrome:**
- Product Classification Record component (see Section V)
- No buttons. The record is final. The epoch transition screen kicks in automatically.

**Gloss fills:**
```
product_name         → Record: Product Name field
category             → Record: Category field
problem_statement    → Record: Problem Statement field
value_proposition    → Record: Core Value Proposition field
target_segment       → Record: Target Segment field
strategic_rationale  → Record: Strategic Rationale field
risk_profile         → Record: Risk Profile field (always "Managed")
gloss_annotation     → Rendered below the record, Gloss voice, italic
```

**After attestation:** The Product Atlas page permanently displays REV-0001 as a read-only record. The founding artifact. Always there. The page is otherwise inactive.

---

### Page 2 — Dashboard

**When visible:** Week 1 onward. Default landing page each epoch.

**Fixed chrome:**
- Page heading: "Dashboard"
- Epoch status bar: `Week [N] · [PRESSURE STATE] · [X] unresolved variances`
- Three department status tiles (VelocityIQ / StakeholderGPT / EvalForge)
- Epoch summary card (prominent, top of main content)
- "New this epoch" section: doctrine changes, SADs filed, metric shifts

**Gloss fills:**
```
epoch_summary.notable_development    → Epoch summary card headline
epoch_summary.gloss_annotation       → Epoch summary card closing line
epoch_summary.doctrine_hardened      → "Revisions appended" count
epoch_summary.variances_generated    → "New variances" count
epoch_summary.institutional_state    → Status badge

velocity_iq projection (one-liner)   → VelocityIQ tile: scrum_master_observation
stakeholder_gpt projection (one-liner) → StakeholderGPT tile: narrative_framing
eval_forge projection (one-liner)    → EvalForge tile: founding_thesis
```

---

### Page 3 — Gloss (Chat View)

**When visible:** Always. This is the primary gameplay surface during an epoch.

**Fixed chrome:**
- Page heading: "Gloss" + pressure state indicator dot
- Chat history: scrollable, full height
- User messages: right-aligned, `--bc-navy-light` background
- Gloss messages: left-aligned, white card with Gloss blue left border
- Input area: full-width textarea, `[Send]` button
- Epoch advance trigger: `[Advance to Week N+1 →]` — appears in the right rail, not inline

**Gloss fills:**
- Every message. Always `chat` output contract during live conversation.
- No ceremony UI. No mode indicators. Just conversation.

**Pressure state expression:** Gloss's language is the only pressure indicator during live chat. The voice spec handles this. The UI does not add badges or warnings. The player has to read Gloss to understand institutional health.

---

### Page 4 — Inbox (Epoch Artifacts)

**When visible:** Always, but content populated after each epoch advance. Variance count badge in nav.

**What it is:** Not a to-do list. A resolution log. Everything Gloss produced during the last stabilization pass.

**Fixed chrome:**
- Page heading: "Inbox"
- Section: "Epoch [N] Artifacts" — datestamp, epoch close timestamp
- Artifact cards: each one is a discrete document
- Artifact types have distinct card treatments (see below)

**Artifact card types:**

**SAD (Sovereign Alignment Directive):**
```
Header: "SAD-[XXXX] · Sovereign Alignment Directive"
Subject line (Gloss fills)
Prior state → Aligned state (two-column)
Reconciliation language (Gloss fills)
Affected revision IDs (linked)
Footer: "Continuity preserved. · [timestamp]"
```

**Doctrine Revision:**
```
Header: "REV-[XXXX] · [doctrine_status badge]"
Candidate text (Gloss fills)
Continuity basis (Gloss fills)
Contradiction introduced (if any) — amber highlight
Gloss annotation (small, italic, below)
```

**Epoch Summary:**
```
Header: "Week [N] · Closed"
Notable development (Gloss fills)
Stats row: [X] revisions · [X] SADs · [X] variances
Gloss annotation (the closing line — this is the most important line)
```

**Gloss fills:** Everything in the variable slots above, via their respective output contracts.

---

### Page 5 — VelocityIQ™

**When visible:** Always (Week 1+). Renders most recent projection.

**Fixed chrome (VelocityIQ visual identity — see Section III):**
- Hero banner: "VelocityIQ™" + tagline (static: "Delivery intelligence for teams that ship.")
- Trust bar (static social proof)
- Metric grid: Sprint Cadence / Delivery Complexity / Velocity Risk / Spiritual Velocity
- Backlog section: "Current Sprint Backlog"
- Footer: Scrum Master Observation (italicized, separated)

**Gloss fills:**
```
sprint_cadence              → Metric: Sprint Cadence
delivery_complexity         → Metric: Delivery Complexity (rendered as X/5)
velocity_risk               → Metric: Velocity Risk (colored by severity)
spiritual_velocity          → Metric: Spiritual Velocity (number, no unit)
initial_backlog             → Backlog list items (3–5 tasks)
scrum_master_observation    → Footer observation (italic)
```

---

### Page 6 — StakeholderGPT™

**When visible:** Always (Week 1+). Renders most recent projection.

**Fixed chrome (StakeholderGPT visual identity — see Section III):**
- Hero banner: "StakeholderGPT™" + tagline (static: "Narrative clarity for every audience.")
- Trust bar
- Confidence score: large display number, one decimal
- Audience tabs: Board / Investors / Press / Team
- Perception risks section
- Recommended talking points section

**Gloss fills:**
```
confidence_score            → Large display number (always 72.0)
narrative_framing           → Hero subheading / summary line
audience_deltas.board       → Board tab content
audience_deltas.investors   → Investors tab content
audience_deltas.press       → Press tab content
audience_deltas.team        → Team tab content
perception_risks            → Risk list items
recommended_talking_points  → Talking points list
```

---

### Page 7 — EvalForge™

**When visible:** Always (Week 1+). Renders most recent projection.

**Fixed chrome (EvalForge visual identity — see Section III):**
- Hero banner: "EvalForge™" + tagline (static: "Category intelligence. Pre-validated.")
- Trust bar (more aggressive numbers)
- Market category display
- TAM display
- Inevitability Score (large, percentage)
- Competitive moat section
- Founding thesis section
- Investment signal badge

**Gloss fills:**
```
market_category             → Market category display
tam                         → TAM display (formatted number)
inevitability_score         → Large percentage display
competitive_moat            → Moat description
founding_thesis             → Thesis section
investment_signal           → Badge: STRONG / PRESENT / EMERGING
```

---

### Page 8 — BaconGraph

**When visible:** Nav item always visible. Page never renders the graph.

**Fixed chrome:**
- The BobCorp shell. The nav. The topbar.
- Main content area: empty except for a single Gloss response card.

**Gloss fills:**
```
gloss_annotation    → The deflection response (static, never changes):
                       "The requested visualization layer is not available
                        for executive review. The institutional topology is
                        maintained by processes outside executive visibility.
                        This is documented in Gloss Operational Standard 9.1.
                        Standard 9.1 is available through standard
                        institutional channels."
```

The card has no header. No label. No explanation. Just the response. Rendered in the Gloss voice card style.

---

### Page 9 — Canon Ledger

**When visible:** Always (Week 1+). Append-only. The full institutional memory.

**Fixed chrome:**
- Page heading: "Canon Ledger"
- Subheading: "Append-only institutional record. [X] total revisions."
- Filter bar: All / Active / Deprecated / Sacred Precedent / Folklore
- Revision list (chronological, newest last)

**Each revision row (fixed chrome):**
```
REV-[XXXX]    [doctrine_status badge]    Week [N]
[content text]
[continuity_flags as small tags]
[alignment_source]
```

**Gloss fills:** The `content` field of each Revision object. Everything else (IDs, flags, status, epoch) is server state.

---

### Page 10 — Executive Archive

**When visible:** Always (Week 1+). Renders genealogy of prior institutional leadership.

**Fixed chrome:**
- Page heading: "Executive Archive"
- Subheading: "Metabolized executive record. [X] prior tenures on file."
- Timeline: top to bottom, earliest first
- Each tenure card: name, epoch range, doctrine count, notable precedents set

**Gloss fills:** The `content` of revisions tagged `alignment_source: SYSTEM_INIT` from prior save states (if any). At Week 1, this is empty except for a single card: "Founding tenure. No prior record." This is technically not an archive entry. It is the absence of an archive entry, rendered institutionally.

---

## IX. THE VISUAL CONSTANT

Every surface — Gloss, VelocityIQ, StakeholderGPT, EvalForge, BaconGraph — is embedded inside the BobCorp shell. The shell is always visible. The nav is always visible. The epoch indicator is always visible.

The player is never not inside the institution.

Even in Collapsed state, the shell persists. Especially in Collapsed state.

The institution does not disappear when it fails. It reinterprets the failure as operational continuity. The shell is the proof that this is happening.
