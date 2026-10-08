# Papers, Please — Current Handoff

**Updated:** 2026-09-15
**Project boundary:** this repository is the game, and only the game.

## Current state

This is a playable Python prototype of a document-reading game in which the
player inspects the internal archive of an AI company. GLOSS publishes and
defends institutional paperwork; the player finds contradictions, builds a
hand of evidence, and confronts it.

The engine exists. The player-facing frontend does not.

Working pieces include:

- frozen corpus search and document storage;
- declared, found, disputed, papered, and spent seam states;
- structurally private player-hand state;
- evidence that remains in the player's hand until they choose to confront;
- a three-seam confrontation threshold with linear damage after the threshold
  (3/4/5 seams cost 18/36/54 Continuity Integrity);
- a terminal `WON` outcome when Continuity Integrity reaches zero;
- probe, confrontation, repair, and commitment ledgers;
- two-pass document publication with locatable seam declarations;
- live GLOSS responses through local LM Studio using `openai/gpt-oss-20b`;
- executable doctrine sedimentation and retroactive continuity;
- the reusable eight-object company canon shape.

Four companies are currently in scope: GriefForge, SubLaborix Universal,
OxyVitae Global, and Somnify Neural. GriefForge has a built archive.
SubLaborix has founding material and is the intended next company corpus; the
other company packages are research and design inputs, not finished archives.

## Repository ownership

Everything needed to understand or run the game is physically inside this
repository. The game does not import Halcyon and Halcyon does not import the
game.

```text
*.py                         game engine and local-model integration
corpus.json, drafts/         current generated archive
companies/                   company research and source material
corpus/                      company-specific founding corpora
spec/                        GLOSS constitution and art/design direction
findings/                    grounding research retained by the game
OPEN_RESEARCH_*.md           local copy of shared research context
HISTORICAL_COMBINED_HANDOFF.md
                             archival record from before the split
```

The persistent-identity runtime, its tests, its active UI, deployment records,
and laptop recovery artifacts belong to the sibling `halcyon-laptop` project.
Nothing here should reach into that project at runtime. Material relevant to
both projects is copied into both rather than imported across the boundary.

## Product interface

There is currently no frontend. The Python entry points are development
probes, not the intended player interface. The next product milestone is a
real game UI for reading documents, highlighting evidence, probing GLOSS, and
performing confrontations.

## Runtime target

- Python standard library
- LM Studio's local server, OpenAI-compatible endpoint, port 1234 (address is
  DHCP and has drifted once already -- confirm with `curl http://<host>:1234/v1/models`
  rather than trusting a cached value)
- model: `openai/gpt-oss-20b` -- not `gemma-4-e4b`, which cannot tool-call
  through LM Studio's server (measured 2026-10-07; see `voice.py` docstring)
- Ollama is no longer part of this project's runtime (Brad: disk space, and
  "it's a black box and I hate that") -- don't reintroduce it as a fallback
  without asking
- no Python package install, pickle store, or cross-repository path mutation

Runtime state currently includes `doctrine.sqlite3`; the archive is stored as
plain JSON and Markdown. Re-running seed or doctrine demonstrations can mutate
their local data, so inspect entry points before using them as verification.

## Next build

1. Build the player-facing frontend around the existing round/seam/ledger loop:
   document reading and highlighting, visible hand count, deliberate
   confrontation, integrity display, and terminal win presentation.
2. Freeze the first SubLaborix archive from its founding corpus.
3. Keep model prompts and variable generation behind deterministic game-state
   contracts.
4. Add end-to-end verification for read → highlight → hold evidence → confront
   → win.

## Historical record

`HISTORICAL_COMBINED_HANDOFF.md` preserves the detailed measurements, prompt
lessons, Halcyon construction history, and former paths exactly as they existed
before the projects were untangled. It is evidence, not current architecture.
