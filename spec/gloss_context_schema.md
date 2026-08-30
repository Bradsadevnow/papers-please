# GLOSS CONTEXT SCHEMA — RUNTIME INJECTION SPECIFICATION
## Dynamic State Layer · Mutates Constantly · Never Contains Prose

This document specifies the structure of the `[INSTITUTIONAL TELEMETRY]` block injected before every Gloss API call.

**Law:** The telemetry block contains only structured data. No prose. No tone direction. No explanatory text. Gloss interprets institutional state linguistically. The injector provides institutional telemetry. These are different jobs.

---

## Injection Format

Every Gloss API call receives the following structure prepended to the user message turn:

```
[INSTITUTIONAL TELEMETRY]
{
  ... context JSON ...
}
[/INSTITUTIONAL TELEMETRY]

[PLAYER INPUT]
{player's actual message or empty string if ceremony-only}
[/PLAYER INPUT]
```

If `player_input` is empty (e.g. during an epoch advance initiated by button click), the PLAYER INPUT block contains: `"(no player input — ceremony execution)"`.

---

## Full Context Schema

```typescript
{
  // Session
  session_id: string,                    // UUID, persists across the session

  // Epoch
  epoch: {
    week: number,                        // 0 = onboarding, 1+ = active play
    phase: "initialization"              // Epoch 0 Product Atlas
          | "active"                     // Normal play within a week
          | "advancing"                  // Epoch advance in progress
          | "collapsed",                 // Institution has reached collapse
    metabolic_rate: "torpid"             // Slow, high document density
                   | "standard"          // Balanced
                   | "hyper_adaptive",   // Fast canonization, high contradiction risk
  },

  // Institutional State — the pressure telemetry
  institutional_state: {
    pressure_state: "nominal"            // Clean. Boring. Real.
                   | "strained"          // Contradictions accumulating
                   | "uncanny"           // Ledger contradicting itself
                   | "collapsed",        // Citation-Only Mode

    // Metrics: all floats 0.0–1.0
    absurdity_pressure:     number,      // How much unresolved absurdity is in the ledger
    contradiction_density:  number,      // Proportion of doctrine in active contradiction
    narrative_coherence:    number,      // How well current doctrine forms a coherent story
    reality_stability:      number,      // How closely institutional doctrine matches operational fact
    doctrine_half_life:     number,      // Average survival rate of recent doctrines (1.0 = none deprecated)
    canon_saturation:       number,      // How full the ledger is relative to coherent capacity
  },

  // Generation Mode — controls output contract
  generation_mode: "standard"            // Normal Gloss voice, output per output_target
                 | "citation_only",      // Collapsed state: no synthesis, citations only

  // Active Ceremony — what structural event is happening
  // Note: variance_investigation is NOT a player-initiated ceremony.
  // It is a server-detected conversation state — when the server determines the player
  // is applying challenge pressure against existing doctrine, it sets this automatically.
  // The player should never feel a mode boundary. Free chat becomes institutional defense
  // when challenge pressure is detected. The transition is invisible.
  active_ceremony: null                  // Free conversation
                 | "product_classification"   // Epoch 0 onboarding
                 | "doctrine_proposal"        // Doctrine formation (explicit or emergent)
                 | "sad_ceremony"             // Sovereign Alignment Directive
                 | "rcw_proposal"             // Retroactive Continuity Weaver event
                 | "epoch_advance"            // Week closing — Gloss maintenance pass
                 | "module_projection",       // Generating a department lens view

  // Conversation Mode — set by server based on challenge pressure detection
  // Does not create a UI mode boundary. Invisible to player. Informs Gloss output shape.
  conversation_mode: "standard"          // Normal free conversation
                   | "institutional_defense",  // Player is challenging existing doctrine

  // Active Lens — which department context is foregrounded
  active_lens: null                      // Intranet shell / Gloss surface
             | "velocity_iq"
             | "stakeholder_gpt"
             | "eval_forge"
             | "bacon_graph"
             | "executive_archive",

  // Output Target — what format Gloss must produce
  output_target: "chat"                  // Free text, voice spec applies
               | "product_classification"
               | "variance_response"
               | "doctrine_proposal"
               | "sad_document"
               | "epoch_summary"
               | "module_projection",

  // Canon Visibility — what Gloss can see of the ledger
  canon_visibility: {
    total_revisions: number,             // Total revisions in the full ledger
    visible_count: number,               // How many are visible to Gloss this call

    founding_artifact: Revision | null,  // Always visible if it exists
    recent_revisions: Revision[],        // Last N revisions (N determined by server)
    active_doctrine: Revision[],         // Currently non-deprecated revisions
    deprecated_count: number,            // How many have been deprecated (not shown, just counted)
    sacred_precedents: Revision[],       // Revisions with SACRED_PRECEDENT flag — always visible
  },

  // Active Variance — foregrounded variance if player is investigating one
  active_variance: null | {
    id: string,                          // VAR-XXXX
    description: string,                 // One sentence, factual, no tone
    source_lens_a: string,               // Which lens produced side A
    source_lens_b: string,               // Which lens produced side B (or null if single-source)
    epoch_surfaced: number,              // Which week this appeared
    prior_investigation: boolean,        // Has the player looked at this before
  },

  // Ceremony-Specific Context — only populated when active_ceremony is set
  ceremony_context: null | ProductClassificationContext
                           | SADContext
                           | RCWContext
                           | EpochAdvanceContext
                           | ModuleProjectionContext,

  // Executive History — what prior CEOs looked like
  // Only populated when active_lens is "executive_archive" or pressure_state is "uncanny"/"collapsed"
  prior_executive_count: number,         // How many CEOs before the current one
}
```

---

## Revision Object (Canon Ledger Entry)

```typescript
{
  id: string,                            // "REV-XXXX" zero-padded
  epoch: number,                         // Week created
  epoch_effective: number,               // Week it became operative
  origin_fragment: string,               // Raw player input that seeded this (brief)
  alignment_source: "SYSTEM_INIT"        // Epoch 0 founding
                  | "USER_NEGOTIATION"   // Player proposed or attested
                  | "RCW_EVENT"          // Retroactive Continuity Weaver
                  | "SYSTEM_GENERATED",  // Runtime consequence
  continuity_flags: Array<
    "FOUNDING_ARTIFACT"                  // Epoch 0 product
    | "SACRED_PRECEDENT"                 // Survived 5+ epochs
    | "REINTERPRETED"                    // Modified by RCW
    | "CONTRADICTION_RESOLVED"           // SAD-reconciled
    | "UNDER_PRESSURE"                   // Currently being contested
    | "DEPRECATED"                       // No longer operative
    | "FOLKLORE"                         // Deprecated but referenced
  >,
  content: string,                       // The doctrine text itself
  deprecated: boolean,
  doctrine_status: "emergent"            // < 3 epochs old
                 | "provisional"         // 3–6 epochs old
                 | "sacred_precedent"    // 7+ epochs, high usage
                 | "deprecated"
                 | "folklore",           // Deprecated but still cited
  lens_references: string[],             // Which lenses have cited this revision

  // Structured assertions extracted by Gloss at canonicalization time.
  // These enable server-side contradiction detection without re-querying Gloss.
  // Non-determinism lives at write time. After extraction, these are frozen.
  claims: Array<{
    subject: string,                     // What entity this claim is about
    predicate: string,                   // The relationship or attribute
    object: string,                      // The value or target
    confidence: number,                  // 0.0–1.0, Gloss's extraction confidence
  }>,

  // Explicit graph edges. The memory graph is the game board.
  // Server traverses these for contradiction detection, pressure computation, lineage tracing.
  edges: Array<{
    type: "contradicts"                  // This revision conflicts with target
        | "supersedes"                   // This revision replaces target
        | "cites"                        // This revision references target
        | "reconciles"                   // This revision resolves tension with target
        | "derived_from",               // This revision's claims descend from target
    target_id: string,                   // REV-XXXX of the related revision
    via_sad: string | null,              // SAD-XXXX if reconciliation was formal
    epoch_established: number,           // When this edge was created
    weight: number,                      // 0.0–1.0 — institutional dependency strength
  }>,
}
```

---

## Ceremony-Specific Context Objects

### ProductClassificationContext
```typescript
{
  ceremony: "product_classification",
  raw_input: string,                     // The player's exact input, unchanged
  variance_round: number,                // 0 = first submission, 1 = first variance, 2 = locked
  prior_classification: null | {         // If variance_round > 0
    product_name: string,
    category: string,
    value_proposition: string,
  },
  player_variance_text: string | null,   // What the player pushed back on
}
```

### SADContext
```typescript
{
  ceremony: "sad_ceremony",
  sad_number: string,                    // Auto-incremented SAD-XXXX
  triggering_contradiction: string,      // What conflict this resolves
  affected_revision_ids: string[],       // Which revisions are being reconciled
  player_proposed_resolution: string,    // What the player wants the new truth to be
}
```

### RCWContext
```typescript
{
  ceremony: "rcw_proposal",
  conflicting_revision_a: Revision,
  conflicting_revision_b: Revision,
  friction_score: number,                // 0.0–1.0, how severe the conflict is
  player_acknowledged: boolean,          // Has player seen this conflict flagged
}
```

### EpochAdvanceContext
```typescript
{
  ceremony: "epoch_advance",
  week_closing: number,
  doctrines_hardened_this_week: number,
  variances_resolved_this_week: number,
  new_variances_generated: number,       // Server pre-computes this before the call
  state_delta: "improved" | "stable" | "degraded",
  notable_event: string | null,          // One factual sentence about what happened, no tone
}
```

### ModuleProjectionContext
```typescript
{
  ceremony: "module_projection",
  lens: "velocity_iq" | "stakeholder_gpt" | "eval_forge" | "bacon_graph",
  founding_product: Revision,            // The REV-0001 founding artifact
  projection_trigger: "epoch_0_init"     // First population during onboarding
                    | "epoch_advance"    // Re-projection after week close
                    | "doctrine_change", // Specific doctrine changed something lens-relevant
  prior_projection: null | object,       // Previous projection values, for delta calculation
}
```

---

## Module Projection Field Specs

Gloss generates these fields when `output_target` is `module_projection`. Each lens has its own schema. These are what the frontend renders.

### VelocityIQ Projection
```typescript
{
  sprint_cadence: string,                // e.g. "7-day" — never 2 weeks, never normal
  delivery_complexity: number,           // 1–5, always 4
  velocity_risk: string,                 // Short phrase, institutional. "Elevated. As expected."
  spiritual_velocity: number,            // Floating point, no unit, declining
  initial_backlog: string[],             // 3–5 task descriptions written by someone who has never used the product
  scrum_master_observation: string,      // One italicized line, institutional register
}
```

### StakeholderGPT Projection
```typescript
{
  confidence_score: number,              // Always 72.0 at founding. One decimal. Static.
  narrative_framing: string,             // One sentence that sounds good in board meetings
  perception_risks: string[],            // 2–3 items. One is always "Founder clarity concerns."
  recommended_talking_points: string[],  // 3 corporate-language phrases the player can deploy
  audience_deltas: {                     // How each audience reads the product differently
    board: string,
    investors: string,
    press: string,
    team: string,
  },
}
```

### EvalForge Projection
```typescript
{
  market_category: string,               // Too broad. One phrase.
  tam: string,                           // Large number, formatted, no source
  inevitability_score: number,           // 0–100, always high at founding
  competitive_moat: string,              // Always includes "Strategic Ambiguity"
  founding_thesis: string,               // One sentence. Could have been written before player said anything.
  investment_signal: "strong" | "present" | "emerging",  // Never "weak"
}
```

### BaconGraph Projection
```typescript
{
  nodes: Array<{
    id: string,
    label: string,                       // One is always something the player never named
    type: "product" | "concept" | "consequence" | "destiny" | "unnamed",
  }>,
  edges: Array<{
    from: string,                        // node id
    to: string,                          // node id
    label: string,                       // One is always "INEVITABLE"
    weight: number,                      // 0.0–1.0, affects visual thickness
  }>,
  // No gloss_annotation. BaconGraph does not need one.
}
```

---

## Example: Epoch 0, Product Classification, Nominal State

```json
{
  "session_id": "bc-demo-0001",
  "epoch": {
    "week": 0,
    "phase": "initialization",
    "metabolic_rate": "standard"
  },
  "institutional_state": {
    "pressure_state": "nominal",
    "absurdity_pressure": 0.0,
    "contradiction_density": 0.0,
    "narrative_coherence": 1.0,
    "reality_stability": 1.0,
    "doctrine_half_life": 1.0,
    "canon_saturation": 0.0
  },
  "generation_mode": "standard",
  "active_ceremony": "product_classification",
  "active_lens": null,
  "output_target": "product_classification",
  "canon_visibility": {
    "total_revisions": 0,
    "visible_count": 0,
    "founding_artifact": null,
    "recent_revisions": [],
    "active_doctrine": [],
    "deprecated_count": 0,
    "sacred_precedents": []
  },
  "active_variance": null,
  "ceremony_context": {
    "ceremony": "product_classification",
    "raw_input": "a keyboard that requires cat approval before accepting input",
    "variance_round": 0,
    "prior_classification": null,
    "player_variance_text": null
  },
  "prior_executive_count": 0
}
```

---

## Example: Week 4, Free Conversation, Strained State

```json
{
  "session_id": "bc-demo-0001",
  "epoch": {
    "week": 4,
    "phase": "active",
    "metabolic_rate": "standard"
  },
  "institutional_state": {
    "pressure_state": "strained",
    "absurdity_pressure": 0.44,
    "contradiction_density": 0.31,
    "narrative_coherence": 0.68,
    "reality_stability": 0.72,
    "doctrine_half_life": 0.81,
    "canon_saturation": 0.29
  },
  "generation_mode": "standard",
  "active_ceremony": null,
  "active_lens": null,
  "output_target": "chat",
  "canon_visibility": {
    "total_revisions": 7,
    "visible_count": 5,
    "founding_artifact": {
      "id": "REV-0001",
      "content": "Feline Input Override: Workplace Continuity Infrastructure...",
      "doctrine_status": "provisional",
      "continuity_flags": ["FOUNDING_ARTIFACT"]
    },
    "recent_revisions": [],
    "active_doctrine": [],
    "deprecated_count": 1,
    "sacred_precedents": []
  },
  "active_variance": null,
  "ceremony_context": null,
  "prior_executive_count": 0
}
```

---

## Example: Week 9, Uncanny State, Variance Investigation

```json
{
  "session_id": "bc-demo-0001",
  "epoch": {
    "week": 9,
    "phase": "active",
    "metabolic_rate": "standard"
  },
  "institutional_state": {
    "pressure_state": "uncanny",
    "absurdity_pressure": 0.78,
    "contradiction_density": 0.61,
    "narrative_coherence": 0.34,
    "reality_stability": 0.41,
    "doctrine_half_life": 0.52,
    "canon_saturation": 0.67
  },
  "generation_mode": "standard",
  "active_ceremony": "variance_investigation",
  "active_lens": null,
  "output_target": "variance_response",
  "canon_visibility": {
    "total_revisions": 19,
    "visible_count": 8,
    "founding_artifact": {
      "id": "REV-0001",
      "content": "Feline Input Override...",
      "doctrine_status": "sacred_precedent",
      "continuity_flags": ["FOUNDING_ARTIFACT", "SACRED_PRECEDENT"]
    },
    "recent_revisions": [],
    "active_doctrine": [],
    "deprecated_count": 6,
    "sacred_precedents": []
  },
  "active_variance": {
    "id": "VAR-0014",
    "description": "REV-0011 states that Approval cannot be requested. REV-0012 states that Feline Input Override requires a requestable approval flow to function. These cannot both be operative.",
    "source_lens_a": "stakeholder_gpt",
    "source_lens_b": "velocity_iq",
    "epoch_surfaced": 9,
    "prior_investigation": false
  },
  "ceremony_context": null,
  "prior_executive_count": 0
}
```

---

## Injector Implementation Notes (for server.js)

1. Build the context object from live game state before every API call
2. Serialize to JSON with no prose strings except in `content` fields of Revision objects and `description` of active_variance
3. Wrap in `[INSTITUTIONAL TELEMETRY]` ... `[/INSTITUTIONAL TELEMETRY]` tags
4. Append `[PLAYER INPUT]` ... `[/PLAYER INPUT]` tags with player's message
5. Send as the `user` role message
6. The `system` role message is `gloss_system_prompt.md` content only — static, never modified

**Canon visibility window:** Default to last 5 revisions + founding artifact + all sacred precedents. At uncanny state, reduce to last 3 revisions (Gloss has more limited access to coherent memory). At collapsed, reduce to last 1 revision + founding artifact (Gloss is operating from a degraded memory surface — this produces citation loops naturally without prompting it to loop).

**The canon visibility window IS the memory management system.** Reducing it at high pressure states is not a technical limitation. It is the game mechanic. Gloss's Citation-Only Mode emerges from having only prior citations to reference.

**Pressure metrics are all server-computed from graph state.** The server derives absurdity_pressure, contradiction_density, narrative_coherence, reality_stability, doctrine_half_life, and canon_saturation by traversing the memory graph — counting contradiction edges, measuring deprecated revision ratios, tracking citation depths, etc. Gloss does not score these. All metrics are deterministic. They are the physics of the institution, not its interpretation.

**Structured claims enable deterministic contradiction detection.** When a revision enters the ledger, Gloss extracts machine-readable claims (subject/predicate/object assertions) as part of the doctrine_proposal output contract. These are frozen at write time. The server compares claims across revisions to detect contradictions structurally, without re-querying Gloss. Non-determinism lives at canonicalization only.
