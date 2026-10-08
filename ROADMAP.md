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

Per `HANDOFF.md`'s "Next build" §1, the real next milestone:

- [ ] P1-01 Document reader: render a published document, support highlighting
      a span as a seam claim
- [ ] P1-02 Visible hand count — the player's claimed-but-unconfirmed evidence,
      structurally private from GLOSS per the existing engine guarantee
- [ ] P1-03 Probe action — ask GLOSS a non-accusing question, wired to the
      existing probe ledger
- [ ] P1-04 Confrontation action — deliberate, hand ≥ threshold check, wired to
      the existing 3/4/5-seam damage curve (18/36/54 Continuity Integrity)
- [ ] P1-05 Integrity display + terminal `WON` presentation when it hits zero

## P2 — Display what GLOSS actually writes

The engine does two-pass document publication with locatable seam declarations
— the UI needs to show the *live* archive growing, not just a frozen corpus:

- [ ] P2-01 Wire the frontend to read newly-published documents as GLOSS writes
      them, not only the seeded `corpus.json`
- [ ] P2-02 Surface GLOSS's live responses (via local LM Studio, `gpt-oss-20b`) in
      the reader/probe flow, not just as a dev-probe console output

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
