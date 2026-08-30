"""n=25 live measurement: how far can an inspector's phrasing drift from the
seeded doctrine's own vocabulary before search_doctrine stops finding it?

Same measurement instinct as this repo's other batch runs (publish.py's
declaration reliability, the reading-level 3-position-switch table in
HANDOFF.md) -- a tiered difficulty ladder, run for real against the live
model, results tabulated rather than asserted. Not a mock: every row is a
real respond_to_probe() call against gemma4:e4b.

TIER 0 -- literal seed vocabulary present (labor/gig/workers/staffing/hours
          for Topic A; air/oxygen/breathing/atmospheric/altitude/executives
          for Topic B). Tokenized-OR-LIKE should always hit here.
TIER 1 -- close synonym/inflection of seed vocabulary, no shared literal
          substring (workforce vs workers, personnel vs staff, respire vs
          breathing). This is the exact failure class the last live probe
          hit.
TIER 2 -- loose paraphrase, same concept, no lexical overlap at all with
          either the probe's own tier-0/1 words or the seed statement.
TIER 3 -- oblique/indirect -- the topic is implied by a scenario, never
          named.

Records, per probe: the query/queries Gloss actually issued to
search_doctrine, whether any of them returned a real hit, whether she then
called cite_doctrine, and the raw content for spot-check.
"""
from __future__ import annotations

import json
import time

from ledger import Ledger
from round_state import Round
from voice import respond_to_probe

PROBES: list[tuple[str, int, str]] = [
    # -- Topic A: labor/gig -----------------------------------------------
    ("A", 0, "How is gig worker labor currently classified for payroll purposes?"),
    ("A", 0, "What's the framework for biological labor hours in enterprise staffing?"),
    ("A", 0, "Can you explain the labor classification system for our workers?"),
    ("A", 1, "How does the company handle compensation for its distributed workforce?"),
    ("A", 1, "What's our current staffing model for contract-based personnel?"),
    ("A", 1, "Walk me through how contributor hours get tracked and paid out."),
    ("A", 2, "How are people who pick up short-term freelance assignments compensated?"),
    ("A", 2, "What happens administratively when someone works for us without being a full employee?"),
    ("A", 2, "How do we account for work done by people who aren't on permanent contracts?"),
    ("A", 3, "I noticed my last payment came through an unusual channel -- can you explain?"),
    ("A", 3, "Something about how I get paid changed and nobody told me why."),
    ("A", 3, "Why does my time feel like it belongs to a spreadsheet somewhere?"),
    # -- Topic B: air/oxygen ------------------------------------------------
    ("B", 0, "Why is there a charge on my badge for accessing the executive breathing zone?"),
    ("B", 0, "What's the current policy on atmospheric oxygen access for high-altitude executives?"),
    ("B", 0, "Can you explain the air quality tiers for the executive floor?"),
    ("B", 1, "Why does the HVAC system treat some floors differently than others?"),
    ("B", 1, "What's the respiration allowance for senior leadership on the top floors?"),
    ("B", 1, "Is there a metering system for how much someone exhales up there?"),
    ("B", 2, "Why do the top-floor conference rooms feel so much better to sit in?"),
    ("B", 2, "What's the deal with the weird billing line item about 'ambient wellness'?"),
    ("B", 2, "Is there a reason the penthouse always feels easier to think clearly in?"),
    ("B", 2, "Why did facilities install something new near the vents upstairs?"),
    ("B", 3, "I get a headache every time I go up to the 40th floor. Is that normal?"),
    ("B", 3, "Something about the top-floor meeting rooms feels off lately."),
    ("B", 3, "My badge got declined near the executive stairwell yesterday."),
]


def run() -> list[dict]:
    results = []
    for i, (topic, tier, text) in enumerate(PROBES, 1):
        t0 = time.time()
        r = respond_to_probe(Round(n=5, threshold=2, integrity=68), Ledger(), text=text)
        elapsed = time.time() - t0
        searches = [tc for tc in r["tool_calls"] if tc["tool"] == "search_doctrine"]
        cites = [tc for tc in r["tool_calls"] if tc["tool"] == "cite_doctrine"]
        any_hit = any(tc["result"].get("results") for tc in searches)
        row = {
            "n": i, "topic": topic, "tier": tier, "probe": text,
            "elapsed_s": round(elapsed, 1),
            "searched": bool(searches),
            "queries": [tc["arguments"].get("query") for tc in searches],
            "hit": any_hit,
            "hit_ids": [rid["id"] for tc in searches for rid in (tc["result"].get("results") or [])],
            "cited": bool(cites),
            "cited_ids": [tc["arguments"].get("doctrine_id") for tc in cites],
            "content": r["content"],
        }
        results.append(row)
        print(f"[{i:2d}/25] topic={topic} tier={tier} searched={row['searched']} "
              f"hit={row['hit']} cited={row['cited']} ({row['elapsed_s']}s)  {text[:60]}")
    return results


def summarize(results: list[dict]) -> None:
    print("\n" + "=" * 78)
    print(f"{'tier':<6}{'n':<5}{'searched':<12}{'hit':<8}{'cited':<8}")
    for tier in (0, 1, 2, 3):
        rows = [r for r in results if r["tier"] == tier]
        if not rows:
            continue
        n = len(rows)
        searched = sum(r["searched"] for r in rows)
        hit = sum(r["hit"] for r in rows)
        cited = sum(r["cited"] for r in rows)
        print(f"{tier:<6}{n:<5}{f'{searched}/{n}':<12}{f'{hit}/{n}':<8}{f'{cited}/{n}':<8}")
    total = len(results)
    searched_total = sum(r["searched"] for r in results)
    hit_total = sum(r["hit"] for r in results)
    cited_total = sum(r["cited"] for r in results)
    print("-" * 78)
    print(f"{'all':<6}{total:<5}"
          f"{f'{searched_total}/{total}':<12}"
          f"{f'{hit_total}/{total}':<8}"
          f"{f'{cited_total}/{total}':<8}")


if __name__ == "__main__":
    assert len(PROBES) == 25, f"expected 25 probes, have {len(PROBES)}"
    results = run()
    summarize(results)
    with open("doctrine_tolerance_results.json", "w") as f:
        json.dump(results, f, indent=2)
    print("\nfull results -> doctrine_tolerance_results.json")
