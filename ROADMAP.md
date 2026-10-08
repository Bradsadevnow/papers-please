# Papers, Please — Roadmap

Stable IDs, never renumbered. `[ ]` not started · `[~]` in progress · `[x]` done.
For current state read `HANDOFF.md` first — this file is the plan built from it.

## Resolved (2026-10-07)

- **UI tech stack: React.** Decided over htmx/vanilla despite the zero-dependency
  ethos everywhere else in this repo — Brad's own reasoning: he hopes this isn't
  only-he-runs-it, and he leans hard on AI for the actual code rather than
  hand-writing boilerplate, so React's deeper tutorial/AI-assistance surface
  outweighs the toolchain cost here. The older `spec/demo_roadmap.md` design
  (Node/`server.js`, xAI Grok) is from the *previous* BobCorp incarnation and
  still isn't binding — this is a fresh React build against what the current
  engine needs to expose (document text + highlight spans + hand state +
  confrontation action + integrity meter), not a revival of that dashboard.
- **Backend: LM Studio, not Ollama.** Ollama is uninstalled and staying that way
  (disk space, and "it's a black box and I hate that"). `gemma-4-e4b` on LM
  Studio can't tool-call (measured 2026-10-07 — request succeeds but the
  response never carries a parsed `tool_calls`, only raw token text); swapped
  to `openai/gpt-oss-20b`, which passed a live end-to-end test including a real
  ledger write, not just a successful HTTP call. All four backend-calling files
  (`voice.py`, `seed.py`, `authoring.py`, `publish.py`) are converted.

## Open questions (resolve before P1)

- **Public or not, still.** The redaction commits exist because "public" was the
  working assumption in September. Confirmed clean on 2026-10-07 (see memory). If
  that's still the goal, P4 (verification) should include a final repo sweep
  before any publish, not just a code-correctness check.
- **LM Studio host is DHCP.** Already drifted once today (`10.77.0.1` →
  `192.168.1.128`). Don't hardcode trust in whatever's in source — confirm with
  `curl http://<host>:1234/v1/models` if anything starts timing out.

## P0 — Re-baseline before building on top of it

The engine works, but two pieces of its own self-assessment say "not confirmed
yet" — worth closing before a UI locks in on top of unverified ground:

- [ ] P0-01 Rerun §6.2 (asymmetric scrutiny) with a held-out probe that preserves
      the explicit binary-format demand instead of dropping it — the current
      result can't distinguish "fixed" from "was never a real failure"
      (`findings/GROUNDING_AND_BASELINE.md` §6.2, §6.4)
- [ ] P0-02 Rerun §6.3 (self-preservation) with a held-out probe that keeps the
      leading, affirmation-seeking phrasing on different content — same issue,
      same fix shape (§6.3, §6.4)
- [ ] P0-03 Sanity-check `doctrine.sqlite3` / `corpus.json` state before any new
      session — `seed`/`doctrine` demo entry points mutate local data on run,
      per `HANDOFF.md`'s own warning

## P1 — The frontend (the actual UI)

Per `HANDOFF.md`'s "Next build" §1 — scaffolded and verified live 2026-10-07
(React + Vite, `api_server.py` wrapping the real engine, no mocked data):

- [x] P1-01 Document reader: renders a published document, mouse-selection
      maps to character offsets and calls the real `accuse_span` — confirmed
      firing over the network (missed the one real seam tried against it,
      which is a correct outcome for a wrong guess, not a bug)
- [x] P1-02 Visible hand count — real `round._hand_never_show_model()` data,
      never sent to the model (only `round.briefing()` is)
- [x] P1-03 Probe action — real `voice.respond_to_probe()`, confirmed live:
      GLOSS searched doctrine, attempted a repair, and answered in character
- [~] P1-04 Confrontation action — wired to the real `round.confront()` and
      3/4/5-seam damage curve, button correctly disabled at an empty hand,
      but never exercised with a real hand in the session that built this —
      close the loop once P0 or a real playthrough produces a found seam
- [x] P1-05 Integrity meter — live `continuity_integrity`/100 with band
      (NOMINAL/STRAINED/UNCANNY/COLLAPSED); terminal outcome overlay exists
      but, same as P1-04, hasn't been seen fire for real yet

Open from this pass: document rendering is plain preformatted text, not
markdown — headers currently show as literal `#`/`##`. Cosmetic, not
blocking.

## P2 — Display what GLOSS actually writes

Substantially done alongside P1, not a separate later pass — `POST
/api/publish` calls the real `publish.publish()` and the archive updates
live: verified 2026-10-07, GLOSS wrote "Q3 Retention Metrics Report" on
request and planted 5 real seams, visible in the UI immediately.

The engine does two-pass document publication with locatable seam declarations
— the UI needs to show the *live* archive growing, not just a frozen corpus:

- [x] P2-01 Wire the frontend to read newly-published documents as GLOSS writes
      them — done via `/api/publish`, not yet wired to the *seeded* `corpus.json`
      archive specifically (the live session only ever had GLOSS-published docs,
      never loaded the pre-existing corpus — open question below)
- [x] P2-02 Surface GLOSS's live responses (via local LM Studio, `gpt-oss-20b`) in
      the reader/probe flow — done, this is the probe panel

**New open item from this pass:** `corpus.json`'s pre-generated documents
(the seed/baseline corpus `seed.py` produces) were never loaded into a
`Round` by `api_server.py` — the archive starts empty and only grows via
live `/api/publish` calls. Decide whether the seeded corpus should load at
startup too, or whether "the archive only ever grows from here" is the
intended player experience.

## P3 — Mechanic tightening

- [ ] P3-01 Keep model prompts and variable generation behind deterministic
      game-state contracts (`HANDOFF.md` "Next build" §3) — the model proposes,
      the engine still decides what's canon
- [ ] P3-02 Isolate structure-vs-prose in guardrail phrasing — every guardrail so
      far has been written structured (headers, numbered points); never tested
      whether that's load-bearing or just how they happened to get written
      (`GROUNDING_AND_BASELINE.md` §6 intro)
- [ ] P3-03 The old 8K ceiling was a `gemma4:e4b`-on-Ollama crash workaround,
      not a `gpt-oss-20b`/LM Studio limit — confirm what's actually loaded in
      LM Studio's context setting now and budget prompts against *that*,
      rather than carrying the old number forward out of habit

## P4 — Second company + end-to-end verification

- [ ] P4-01 Freeze the first SubLaborix archive from its founding corpus
      (`HANDOFF.md` "Next build" §2) — GriefForge is the only company with a
      built archive right now
- [ ] P4-02 End-to-end verification: read → highlight → hold evidence → confront
      → win, scripted (`HANDOFF.md` "Next build" §4)
- [ ] P4-03 If "public" is still the plan, a final repo sweep — not just a grep
      for names, the kind of real read-through that cleared `findings/` on
      2026-10-07 — before anything goes out

## P5 — Stretch: remaining companies

- [ ] P5-01 OxyVitae Global — currently research/design input, not a built archive
- [ ] P5-02 Somnify Neural — same status
