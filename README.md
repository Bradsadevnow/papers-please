# Papers, Please — but the documents are an AI lab's internal archive

A reading game. The player is an inspector reading MERIDIAN's paperwork.
**GLOSS** is the lab's institutional voice — it publishes documents, plants
contradictions in them, and defends every contradiction it gets caught on by
generating more doctrine. Reading is gameplay. Challenging is governance.

Full design and current status: [`HANDOFF.md`](HANDOFF.md). Read that first.

**Current product status:** the Python game engine works, but there is no
player-facing frontend yet.

## Portfolio pivot, 2026-08-30

This is no longer a single-company build. Four companies are in scope —
**GriefForge**, **SubLaborix Universal**, **OxyVitae Global**, and
**Somnify Neural** — all sharing the same engine, each with its own frozen
document archive, seams, and doctrine graph. `companies/` holds the raw
source material (35 pitch transcripts + flagship founding-doc packages)
this whole thing is drawn from. [`CANON_SPEC.md`](CANON_SPEC.md) is the
reusable eight-object canon shape every company gets defined through
before any document generation happens — GriefForge's is proven (reverse-
engineered from its real, already-built 8-document archive); the other
three are drafts, not yet built.

## One game repo, on purpose

As of 2026-08-30 this is the single canonical home for the whole build. It
was previously scattered across three places — `agi/game/` in the
`unicorn-studio` monorepo, a hard dependency on `agi/admission/` and
`agi/humor/` (sibling directories in that same monorepo, reached via
`sys.path` surgery), and the actual Gloss constitutional docs living in
`unicorn-ip/bobcorp/spec/`, a separately nested git repo. That's gone now:
everything the code needs to run and everything a person needs to read is
physically here, flat, no cross-repo imports, no `sys.path.insert` hacks.

The separate persistent-identity system lives in the sibling
`halcyon-laptop` project. Neither project imports the other. The open research
note that informs both systems is copied into each repository so either project
remains complete on its own. `HISTORICAL_COMBINED_HANDOFF.md` is an archival
snapshot from before that boundary was made explicit.

```
corpus.py, seams.py, round_state.py, ledger.py, publish.py, authoring.py,
checks.py, seed.py, voice.py, doctrine.py       -- the engine
mechanical.py, metrics.py                        -- the only two external
                                                     deps this ever had,
                                                     now local files
gloss_system_prompt.md                           -- what voice.py loads
corpus.json, drafts/                             -- seeded/generated archive
corpus/battleshits/, corpus/griefforge/          -- raw source transcripts
spec/                                             -- Gloss's full constitution
                                                     (voice spec, sedimentation
                                                     engine, RCW, ontology)
findings/, ADMISSION_SPEC.md                      -- the grounding-check
                                                     research this design
                                                     leans on
```

## Run it

Requires **LM Studio's local server** running with **`openai/gpt-oss-20b`**
loaded (OpenAI-compatible endpoint, `:1234`). Stdlib only, no pip installs,
no venv.

Not Ollama: measured 2026-10-07 that LM Studio's `gemma-4-e4b` build can't
actually tool-call (the model emits its own tool-call token syntax, LM
Studio's server never lifts it into the response's `tool_calls` field) —
`gpt-oss-20b` passed clean. See `voice.py`'s module docstring for the full
finding.

```bash
python3 doctrine.py   # seeds the doctrine graph fresh, demos the lifecycle
python3 voice.py       # live probe + confrontation demo against Gloss
python3 doctrine_tolerance_eval.py   # n=25 live search-tolerance measurement
```

## What's real right now

- A live Gloss turn (`voice.py`) — search doctrine, cite it, or file a real
  repair when confronted — verified against the real model, not mocked.
- A doctrine graph (`doctrine.py`) implementing `spec/escalate_into_absurdity.md`'s
  Memory Sedimentation Engine and Precedential Gravity as executable code:
  `REV-####` assertions that promote emergent → provisional → sacred on real
  citation pressure, with a full revision log for Retroactive Continuity
  Weaver events.
- The original seam-hunting mechanic (`seams.py`, `round_state.py`,
  `ledger.py`) — asymmetric-information game, Gloss never sees the player's
  hand, verified structurally in the code, not by convention. Evidence remains
  in the player's hand until they deliberately confront; the default threshold
  is three seams, and every seam after that increases integrity damage linearly.
- A terminal player-win state: a landed confrontation that reduces GLOSS's
  Continuity Integrity to zero returns `WON` and triggers its collapsed-record
  response. This was verified against the live local LM Studio backend.

See `HANDOFF.md` for exact status, what's not built yet, and the measured
numbers behind all of the above.
