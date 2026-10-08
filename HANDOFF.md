# Papers, Please — Current Handoff

**Updated:** 2026-10-07
**Project boundary:** this repository is the game, and only the game.

## Current state

This is a playable prototype of a document-reading game in which the player
inspects the internal archive of an AI company. GLOSS publishes and defends
institutional paperwork; the player finds contradictions, builds a hand of
evidence, and confronts it.

Both halves exist now: the Python engine, and a real React frontend
(`frontend/`) talking to it over HTTP (`api_server.py`). See "Product
interface" below for exactly what's verified live versus still open —
confrontation specifically is wired but has never fired against a real hand.

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
- the reusable eight-object company canon shape;
- a React/Vite player UI (`frontend/`) and the API wrapping the engine for
  it (`api_server.py`) — reading, highlighting-to-accuse, probing, and
  publishing all verified against the live engine, not mocked.

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
api_server.py                HTTP API wrapping the engine for the frontend
test_voice_live.py           live check: real Round+Ledger through voice.py,
                              confirms a repair lands in ledger.repairs, not
                              just in the model's prose
test_lmstudio_tools.py       one-shot check: does a given LM Studio model
                              actually tool-call, using the real FILE_REPAIR_TOOL
                              schema (not a toy example)
frontend/                    React + Vite player UI (talks to api_server.py)
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

A real frontend exists now (2026-10-07): `frontend/` is a React + Vite app,
talking to `api_server.py` (stdlib Python, wraps the real engine over HTTP —
no mocked data). Verified live: reading a document, highlighting a span to
claim a seam (real `round.accuse_span()` call), probing GLOSS (real
`voice.respond_to_probe()`, including a real tool call landing in the
ledger), and publishing a new document (real `publish.publish()` call,
GLOSS actually wrote one and it planted 5 real seams). Confrontation is
wired but not yet exercised against a real win/loss — hand was empty in the
session that built this.

Run it: `python3 api_server.py` (port 8010), then `cd frontend && npm run
dev` (Vite proxies `/api` to 8010, no CORS setup needed). Still open per the
roadmap: document highlighting doesn't render markdown, there's no visual
distinction for a found-but-not-yet-confronted seam beyond the hand list,
and the confrontation outcome screen has never been seen with a real hand.

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

See `ROADMAP.md` for the full, maintained plan with stable IDs — this
section is now a short pointer, not a duplicate list that can drift out of
sync with it again. Headline items as of 2026-10-07:

1. Close the loop on confrontation: get a real hand (via P0's re-baseline or
   just playing it) and actually see `WON`/`LANDED`/`PAPERED` fire through
   the UI — wired but never exercised live.
2. Decide whether `corpus.json`'s seeded documents load into a `Round` at
   startup, or whether the archive is meant to only ever grow from live
   `/api/publish` calls, as it does today.
3. Freeze the first SubLaborix archive from its founding corpus.
4. Keep model prompts and variable generation behind deterministic game-state
   contracts.

## Historical record

`HISTORICAL_COMBINED_HANDOFF.md` preserves the detailed measurements, prompt
lessons, Halcyon construction history, and former paths exactly as they existed
before the projects were untangled. It is evidence, not current architecture.
