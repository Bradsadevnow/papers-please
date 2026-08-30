# BobCorp Spec — Index

Pulled out of `~/legacy/game/game_overview/` on 2026-07-01 as the fresh, active home for design work. This directory is design/spec only — no code, no runtime. The implementation (`runtime_core/`, `pages/`, etc.) is still in `~/legacy/game/` and has NOT been moved; see [[project-bobcorp]] memory for its actual state before assuming any of it works.

## Reading order

0. **`institutional_satire_framework.md`** — the general 15-layer tool BobCorp instantiates. Read this first now; it explains *why* the cat-cult premise (below) isn't a tone shift, it's the missing Layer 0.
0b. **`cat_cult_ontology.md`** — BobCorp's specific mapping onto the framework: titles, metrics, voice exemplars, and the retconned Epoch 0 example. **This is the current premise as of 2026-07-01** — read before assuming anything in the older docs below reflects the final tone.
1. **`bobcorp_spec.md`** — the thesis. Institutional immortality, the CEO role, Gloss as Homeostasis Engine, the five verbs (Read/Find/Challenge/Observe/Advance), the Kickstarter pitch. Updated 2026-07-01 to state the cat-cult premise explicitly.
2. **`MVP_DOCTRINE.md`** — product north star, one page. Pitch/fantasy/reality/tone in four bullets. Updated 2026-07-01.
3. **`escalate_into_absurdity.md`** — the locked V1 scope.
4. **`metabolization_protocol.md`** — the core player-Gloss interaction model (what "metabolization" actually means turn to turn).
5. **`epoch_0_product_atlas.md`** — the onboarding sequence spec (the only moment the player writes before there's anything to contradict them).
6. **`spine_lock.md`** — short, locks the state schema and authority model. Read this before touching any persistence/state design.
7. **`gloss_context_schema.md`** — the runtime injection spec: structure of the `[INSTITUTIONAL TELEMETRY]` block passed to Gloss before every call. Law: structured data only, no prose, no tone direction.
8. **`gloss_voice_spec.md`** — constitutional document for how Gloss speaks. The eval standard: "Would the institution say this?" Updated 2026-07-01 with the "never names the mysticism" law — Gloss calls the cat-soul economy "industry best practice," never "sacred" or "ritual."
9. **`gloss_system_prompt.md`** — the actual compiled system prompt (built from voice spec + schema + protocol above). This is what ships to the model.
10. **`art_direction.md`** — visual design bible. One job: "look real long enough for the absurdity to be institutional rather than comedic."
11. **`demo_roadmap.md`** — demo format decisions (filmed video, sovereign/local build, not hosted).
12. **`demo_video_structure.md`** — the video's actual structure/pacing.

## Known gap going into tuning (carried over from `~/legacy/game`, 2026-07-01 assessment)

The implementation never got past the classify step of the Epoch 0 flow — 35 recorded server boots, exactly one real LLM call in the whole event history (unrelated to the golden path), no persisted canon ledger entries anywhere. Steps beyond classify (propagate, module pages, dashboard, epoch advance) have never been exercised with real data. Separately, most actual game state was wired through browser `sessionStorage`, not the durable canon ledger — a real mismatch against the game's own thesis about institutional memory. None of this is a reason not to tune the spec; it's context for why "the demo already works, just polish it" would be the wrong frame to start from.
