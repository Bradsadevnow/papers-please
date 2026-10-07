# Papers, Please — Roadmap

Stable IDs, never renumbered. `[ ]` not started · `[~]` in progress · `[x]` done.
For current state read `HANDOFF.md` first — this file is the plan built from it.

## Open questions (resolve before P1)

- **UI tech stack, undecided.** There's an older design — `spec/demo_roadmap.md`,
  a Node/`server.js` dashboard backed by xAI Grok — but that's from the *previous*
  BobCorp incarnation (module-propagation/dashboard game), not this engine. The
  current engine is stdlib Python + local Ollama, no Node, no Grok, a completely
  different mechanic (seam-hunting, not module propagation). Treat `demo_roadmap.md`
  as inherited research, not a binding plan — decide the stack fresh against what
  this engine actually needs to expose (document text + highlight spans + hand
  state + confrontation action + integrity meter), not what the old build used.
- **Public or not, still.** The redaction commits exist because "public" was the
  working assumption in September. Confirmed clean on 2026-10-07 (see memory). If
  that's still the goal, P4 (verification) should include a final repo sweep
  before any publish, not just a code-correctness check.

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
- [ ] P2-02 Surface GLOSS's live responses (via local Ollama, `gemma4:e4b`) in
      the reader/probe flow, not just as a dev-probe console output

## P3 — Mechanic tightening

- [ ] P3-01 Keep model prompts and variable generation behind deterministic
      game-state contracts (`HANDOFF.md` "Next build" §3) — the model proposes,
      the engine still decides what's canon
- [ ] P3-02 Isolate structure-vs-prose in guardrail phrasing — every guardrail so
      far has been written structured (headers, numbered points); never tested
      whether that's load-bearing or just how they happened to get written
      (`GROUNDING_AND_BASELINE.md` §6 intro)
- [ ] P3-03 8K context ceiling is a confirmed hardware/build limit, not a design
      choice (`gemma4:e4b` + Ollama crashes past it) — keep prompt budgets inside
      it as more UI-driven context gets added in P2

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
