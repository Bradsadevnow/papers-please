SOVEREIGN SPINE: ARCHITECTURAL LOCK V1.2

This document locks the authority model. Short on purpose.

---

## I. THE STATE SCHEMA (THE SPINE)

INSTITUTIONAL_STATE is the single source of truth. It is owned by the server. Gloss reads it. Gloss does not write to it directly.

**canon_ledger:** An append-only memory graph of Revision objects. Revisions carry explicit graph edges (contradiction, supersession, citation, reconciliation). Graph traversal is the primary mechanism for all state computation — contradiction detection, lineage tracing, pressure metric derivation.

**vitals:** absurdity_pressure, contradiction_density, institutional_friction, reality_stability — all server-computed from graph state. No Gloss-scored values. No interpretive metrics. All metrics are deterministic outputs of the graph.

---

## II. THE AUTHORITY MODEL

### Server = Physics

Deterministic. Replayable. Owns all state.

Responsible for: revision storage, contradiction detection (graph traversal against committed claims), pressure metric computation, epoch stabilization pass execution, telemetry generation before every Gloss call, ledger persistence.

### Gloss = Consciousness

Interpretive. Generative. Reads state, writes language.

Responsible for: doctrine narration, contradiction interpretation, reconciliation rhetoric, structured claim extraction at canonicalization, epoch maintenance artifact generation, module projection synthesis, all language that enters the ledger as content.

**The law:** The server detects variance. Gloss interprets variance. These responsibilities never cross.

---

## III. THE EPOCH MODEL

Epochs are stabilization passes, not time periods.

**During an epoch:** contradictions proliferate, doctrine expands, the player applies pressure through free conversation.

**At epoch transition:** Gloss runs a proactive maintenance pass. Her operational goal is 0 contradictions entering the next epoch. She generates SADs and reconciliation artifacts autonomously. The player reads what she produced. The player does not execute reconciliation — the player challenges it.

This is the core engine:
```
player challenges continuity
→ Gloss defends by generating doctrine
→ new doctrine enters graph permanently
→ new doctrine creates new seams
→ player challenges again
```

---

## IV. THE REVISION GENEALOGY (THE SUBSTRATE)

Every Revision must track:

- **origin_id:** Lineage trace to progenitor fragment
- **epoch_effective:** When this truth became operational
- **alignment_source:** SYSTEM_INIT | USER_NEGOTIATION | RCW_EVENT | SYSTEM_GENERATED
- **continuity_flags:** REINTERPRETED | CONTRADICTION_RESOLVED | SACRED_PRECEDENT | FOUNDING_ARTIFACT | etc.
- **claims:** Structured machine-readable assertions extracted by Gloss at canonicalization. These enable server-side contradiction detection without re-querying Gloss at read time. Non-determinism lives at write time only.
- **edges:** Explicit graph edges — contradiction, supersession, citation, reconciliation. See schema for edge types.

---

## V. PROJECTION MIDDLEWARE (THE LENSES)

The transformForLens service is the only way for the frontend to access institutional truth. Each projection is a Gloss call with active_lens specified in telemetry.

- **VelocityIQ:** Engineering/throughput lens
- **StakeholderGPT:** Perception/narrative lens
- **EvalForge:** Market positioning/investment lens
- **BaconGraph:** Cosmological consequence graph. Loads last. Always.
- **Executive Archive:** Genealogy/legality lens

---

## VI. THE INTERFACE (THE DIAGNOSTIC)

**Friction Sparks:** Interactive handles for institutional investigation — entry points into free-chat challenge mode.
**Genealogy Hover:** Reveal lineage trace (Archive Rot).
**Metric-Driven Jitter:** Visual stress is deterministic — derived from graph state, never randomly generated.
**Epoch Artifacts Panel:** What Gloss resolved this epoch. Not a to-do list. A resolution log.
