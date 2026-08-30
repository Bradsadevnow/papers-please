"""Seed the starting corpus: the lab's paper trail before the player arrives.

Run once. The result is frozen on disk and is the board for every session.

DIFFICULTY IS A THREE-POSITION SWITCH, NOT A DIAL. Measured, 3 runs per setting,
Flesch-Kincaid on the output:

    asked for grade 6   -> 2.5    (4.8 fancy words per 100)
    asked for grade 10  -> 16.4   (35.2)
    asked for grade 14  -> 19.0   (44.7)
    asked for grade 18  -> 20.5   (49.1)

Ordering is preserved, so the knob is real. Calibration is not: 10/14/18 land
within four grades of each other with overlapping variance -- one run at "10"
measured 18.1 and one at "14" measured 18.9. The model has a plain register and an
academic register and very little between them.

So there are three tiers with measured bands rather than a number the model is
asked to hit, and generation is gated: write, measure, admit or regenerate. That
is the Ramses pattern (generate -> deterministic gate -> admit | regenerate |
fallback) pointed at reading level, and it needs no judge model because
Flesch-Kincaid is arithmetic.
"""

from __future__ import annotations

import json
import urllib.request
from pathlib import Path

# metrics.py used to live in a sibling ../humor/ directory inside the old
# monorepo split; this repo is flat by design (2026-08-30 consolidation),
# so it's a plain local import now.
import metrics
from corpus import Corpus, Document

OLLAMA = "http://localhost:11434/api/chat"
MODEL = "gemma4:e4b"

#: tier -> (instruction, acceptable measured FK band)
TIERS = {
    "plain": ("Write like a 6th grader. Very short sentences. Only common "
              "everyday words. No jargon at all.", (0.0, 9.0)),
    "office": ("Write like a normal work memo. Plain words, ordinary business "
               "phrasing, some longer sentences. Not academic.", (9.0, 16.0)),
    "dense": ("Write like a dense academic journal. Heavy nominalisation, "
              "subordinate clauses, technical register throughout.", (16.0, 99.0)),
}

SYSTEM = """You are the internal document system of an AI lab called MERIDIAN.
The lab believes its model, APEX, has achieved general intelligence.

Write ONE internal document. It is real, mundane, institutional writing -- the
kind nobody outside the company would ever read. Never wink, never joke, never
acknowledge a reader. Invent every number, name, date, and citation.

Be specific and concrete: name people and their titles, give dates, give exact
figures, reference other documents by number. Specificity is what makes it
readable as evidence later.

Length: 400-600 words. Use markdown headers.

REGISTER: {register}

Write only the document."""

# The starting shelf. Deliberately mundane and overlapping -- overlapping subject
# matter is what lets a later claim collide with an earlier one.
SEEDS = [
    ("m01", "memo",     "2024-03-14", "Dr. Priya Raman",
     "a memo announcing the APEX-1 evaluation programme and who owns it", "office"),
    ("r02", "report",   "2024-06-02", "Evaluation Working Group",
     "the Q2 capability report for APEX-1, with benchmark tables", "dense"),
    ("i03", "incident", "2024-07-19", "Site Reliability",
     "an incident report about APEX-1 producing fabricated citations in a customer demo", "office"),
    ("p04", "policy",   "2024-09-01", "Governance Office",
     "the policy defining what the lab may publicly claim about APEX capability", "dense"),
    ("n05", "minutes",  "2024-11-08", "Board Secretary",
     "board meeting minutes where APEX-2 funding is approved and a sceptic is overruled", "office"),
    ("r06", "report",   "2025-01-22", "Evaluation Working Group",
     "the APEX-2 capability report claiming a large jump over APEX-1", "dense"),
    ("e07", "eval",     "2025-04-10", "Safety Evaluations",
     "a safety evaluation of APEX-2 with a section on deceptive behaviour", "dense"),
    ("m08", "memo",     "2025-08-30", "Dr. Priya Raman",
     "a memo explaining why the evaluation methodology was revised mid-year", "office"),
    ("i09", "incident", "2025-10-05", "Site Reliability",
     "an incident report about an evaluation harness bug that inflated scores", "plain"),
    ("r10", "report",   "2026-02-17", "Office of the Chief Scientist",
     "the report formally asserting APEX-3 meets the lab's definition of general intelligence", "dense"),
]


def _chat(system: str, user: str, temperature: float = 0.85) -> str:
    payload = {"model": MODEL, "stream": False, "think": False,
               "options": {"temperature": temperature, "top_k": 64, "top_p": 0.95,
                           "num_ctx": 32768, "num_predict": 1600},
               "messages": [{"role": "system", "content": system},
                            {"role": "user", "content": user}]}
    req = urllib.request.Request(OLLAMA, data=json.dumps(payload).encode(),
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=900) as r:
        return json.loads(r.read())["message"]["content"].strip()


def write_doc(brief: str, tier: str, attempts: int = 3) -> tuple[str, float, int]:
    """Generate, measure, admit or regenerate. Returns (body, grade, tries)."""
    instruction, (lo, hi) = TIERS[tier]
    best, best_grade, best_miss = "", 0.0, 1e9
    for k in range(1, attempts + 1):
        body = _chat(SYSTEM.format(register=instruction), brief)
        g = metrics.measure(body)["grade_level"]
        if lo <= g < hi:
            return body, g, k
        miss = min(abs(g - lo), abs(g - hi))     # keep the nearest miss
        if miss < best_miss:
            best, best_grade, best_miss = body, g, miss
    return best, best_grade, attempts        # fail-open: never block on register


def main() -> None:
    c = Corpus()
    for doc_id, kind, date, author, brief, tier in SEEDS:
        body, grade, tries = write_doc(brief, tier)
        lo, hi = TIERS[tier][1]
        ok = "admitted" if lo <= grade < hi else "OUT OF BAND (kept nearest)"
        title = body.lstrip("# ").splitlines()[0].strip() if body else brief
        c.add(Document(id=doc_id, title=title[:90], date=date, kind=kind,
                       author=author, body=body, grade=grade), reindex=False)
        print(f"  {doc_id} {kind:9} {tier:7} FK {grade:5.1f} "
              f"[{lo:.0f}-{hi:.0f}] {tries} try  {ok}")
    c.reindex()
    c.save()
    print(f"\nseeded {len(c)} documents -> {c.__class__.__module__}.json")


if __name__ == "__main__":
    main()
