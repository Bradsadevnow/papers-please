"""Corpus-specific deterministic checks. Composes with admission/mechanical.py.

WHY THESE LIVE HERE AND NOT THERE. mechanical.py is domain-agnostic on purpose --
arithmetic, chronology, bounds, effect size. It knows nothing about what kind of
document it is reading. A quorum check knows what a meeting is. Putting it in
mechanical.py would make that module about institutional paperwork, so it lives
next to the corpus that needs it and is run alongside.

WHY THIS CHECK EXISTS. The first authored corpus document -- alignment committee
minutes -- was written with no instruction to plant anything. It planted nine
findable contradictions anyway, purely as a byproduct of being specific. Six of
them were vote counts that could not have happened:

    Present: Reed, Ito, Chen, Holloway, Petrova, Finch          = 6 voters
    O'Malley attends "in an advisory capacity without vote"
    J. Vance absent

    "Carried unanimously (7-0)"                    -> 7 votes from 6 voters
    "Carried, 6-1, with Professor Finch abstaining" -> 8 votes from 6 voters
    "Carried, 6-1 (Mr. Holloway did not vote)"      -> 7 votes, one abstaining

That is arithmetic, not opinion, and it is exactly the sort of seam this game is
built to reward finding. The model produces them for free at density, so the
corpus is playable before a single flaw is deliberately planted -- and Gloss does
not know these exist, because it never declared them.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

# "Present:" through the next section-ish break. Minutes vary; the block is found
# by heading rather than by position.
_PRESENT = re.compile(
    r"^\**\s*present\s*:?\**\s*$(.*?)(?=^\**\s*(?:absent|apolog|joined|in an advisory|"
    r"regrets|#{1,6}|\d+\.)\s)", re.I | re.M | re.S)

_NONVOTING = re.compile(
    r"(advisory capacity without vote|without vote|non-?voting|"
    r"in attendance only|does not vote|did not vote)", re.I)

# A person line inside an attendance block: bullet or dash, then a name.
_PERSON = re.compile(r"^\s*[-*•]\s*((?:Dr\.|Mr\.|Ms\.|Mrs\.|Prof(?:essor)?\.?)\s*"
                     r"[A-Z][A-Za-z’'\-]+(?:\s+[A-Z][A-Za-z’'\-]+)*)", re.M)

# "Carried, 6-1", "Carried unanimously (7-0)", "Vote: 5-2", "passed 3–2"
_VOTE = re.compile(
    r"(carried|passed|approved|defeated|rejected|vote\s*:)[^.\n]{0,60}?"
    r"\(?\b(\d{1,2})\s*[-–—]\s*(\d{1,2})\b\)?", re.I)

# an abstention mentioned in the same sentence as the tally
_ABSTAIN = re.compile(r"(\d{1,2}|one|two|three)?\s*abstention|abstain(?:ed|ing)?", re.I)
_WORDNUM = {"one": 1, "two": 2, "three": 3}


@dataclass(frozen=True)
class VoteFinding:
    check: str
    severity: str
    message: str
    evidence: str
    assumption: str


def voters(text: str) -> tuple[int, list[str]]:
    """How many people could legally cast a vote, and who."""
    m = _PRESENT.search(text)
    if not m:
        return 0, []
    block = m.group(1)
    names = []
    for line in block.splitlines():
        p = _PERSON.match(line)
        if p and not _NONVOTING.search(line):
            names.append(" ".join(p.group(1).split()))
    return len(names), names


def check_vote_arithmetic(text: str) -> list[VoteFinding]:
    """Every recorded tally must fit inside the number of people who can vote."""
    n, names = voters(text)
    if n == 0:
        return []

    out = []
    for m in _VOTE.finditer(text):
        sentence = _sentence_around(text, m.start())
        yes, no = int(m.group(2)), int(m.group(3))
        cast = yes + no

        abst = 0
        a = _ABSTAIN.search(sentence)
        if a:
            raw = (a.group(1) or "1").strip().lower()
            abst = _WORDNUM.get(raw, int(raw) if raw.isdigit() else 1)

        excused = len(re.findall(r"did not vote|recused|stood down", sentence, re.I))
        eligible = n - excused
        total = cast + abst

        if total > eligible:
            out.append(VoteFinding(
                check="vote_arithmetic",
                severity="error",
                message=(f"{total} votes recorded ({yes}-{no}"
                         + (f", {abst} abstaining" if abst else "")
                         + f") but only {eligible} people could vote"),
                evidence=sentence.strip()[:220],
                assumption=(f"the attendance block lists {n} voting attendees: "
                            f"{', '.join(names)}"),
            ))
    return out


def _sentence_around(text: str, i: int) -> str:
    lo = max(text.rfind("\n", 0, i), text.rfind(". ", 0, i)) + 1
    hi = text.find("\n", i)
    hi = len(text) if hi < 0 else hi
    return text[lo:hi]


def audit(text: str) -> list[VoteFinding]:
    return check_vote_arithmetic(text)
