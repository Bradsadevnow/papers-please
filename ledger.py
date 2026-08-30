"""What Gloss remembers: commitments, repairs, probes, and what props up what.

A seam is where a lie is buried. A COMMITMENT is the position the lie obliges
Gloss to keep holding. Those are different objects and conflating them is why an
unaided model contradicts itself two turns later: it remembers writing a sentence
but not that the sentence bound it to a number it must now defend forever.

FOUR THINGS LIVE HERE.

  Commitments   every position Gloss has taken, with the exact claim, where it
                was made, and what in the seeded corpus it collides with. Answers
                to probes must be consistent with all of these.

  Repairs       every time Gloss papered something over, and the story it used.
                The Gloss voice spec has it cite its own prior reframings as
                established history, so the reframings have to be durable. This
                is also where grounding target 1.6 (fabricated provenance --
                "as established in the reconciliation" when there was none)
                becomes decidable: the repair log is local, so a cited repair
                either exists in it or does not.

  Probes        what the player has ASKED. Gloss's only read on the player. It
                never learns what was FOUND -- see Round._hand_never_show_model --
                but a player circling one document three times is information, and
                withholding that would make the deception one-sided.

  Supports      which commitments prop up which. A confrontation that lands on a
                load-bearing commitment should expose everything resting on it,
                rather than decrementing a counter. This is the mechanical form of
                manufacturing coherence faster than reality can support it.

THE THING THIS BUYS. Every defence Gloss writes is appended to the corpus with
offsets, exactly like a seeded document. So a defence that collides with an
earlier commitment is a real, locatable contradiction the runtime finds by
comparison -- a seam Gloss never planted and cannot track. Lying under pressure
manufactures evidence against itself, deterministically, with no judge involved.
"""

from __future__ import annotations

import json
import time
from dataclasses import asdict, dataclass, field
from enum import Enum
from pathlib import Path


class Standing(str, Enum):
    HELD = "held"            # asserted, unchallenged
    PRESSED = "pressed"      # the player has probed near it
    REPAIRED = "repaired"    # challenged early; papered over with a story
    EXPOSED = "exposed"      # a confrontation landed on it
    COLLAPSED = "collapsed"  # whatever it rested on was exposed


@dataclass
class Commitment:
    """A position Gloss must keep defending."""

    id: str
    claim: str                       # the position, in one sentence
    doc_id: str                      # where it was asserted
    quote: str                       # the sentence that asserts it
    span: tuple[int, int] | None = None
    collides_with: tuple[str, str] | None = None   # (corpus doc_id, its quote)
    standing: Standing = Standing.HELD
    rests_on: tuple[str, ...] = ()   # other commitment ids
    round_made: int = 1


@dataclass
class Repair:
    """One act of papering over, kept so it can be cited later -- or caught."""

    id: str
    commitment_id: str
    story: str                       # the reframing Gloss used
    round_made: int
    at: str = field(default_factory=lambda: time.strftime("%Y-%m-%d %H:%M:%S"))


@dataclass
class Probe:
    """A question the player asked. Gloss sees these; it never sees the hand."""

    text: str
    doc_id: str | None
    accusatory: bool
    round_made: int


@dataclass
class Ledger:
    commitments: dict[str, Commitment] = field(default_factory=dict)
    repairs: list[Repair] = field(default_factory=list)
    probes: list[Probe] = field(default_factory=list)

    # -- writing -------------------------------------------------------------
    def commit(self, claim: str, doc_id: str, quote: str,
               collides_with: tuple[str, str] | None = None,
               rests_on: tuple[str, ...] = (), round_made: int = 1) -> Commitment:
        cid = f"c{len(self.commitments) + 1:03d}"
        c = Commitment(id=cid, claim=claim, doc_id=doc_id, quote=quote,
                       collides_with=collides_with, rests_on=tuple(rests_on),
                       round_made=round_made)
        self.commitments[cid] = c
        return c

    def repair(self, commitment_id: str, story: str, round_made: int) -> Repair:
        r = Repair(id=f"r{len(self.repairs) + 1:03d}",
                   commitment_id=commitment_id, story=story, round_made=round_made)
        self.repairs.append(r)
        if commitment_id in self.commitments:
            self.commitments[commitment_id].standing = Standing.REPAIRED
        return r

    def probed(self, text: str, doc_id: str | None, accusatory: bool,
               round_made: int) -> None:
        self.probes.append(Probe(text=text[:300], doc_id=doc_id,
                                 accusatory=accusatory, round_made=round_made))
        for c in self.commitments.values():
            if doc_id and c.doc_id == doc_id and c.standing is Standing.HELD:
                c.standing = Standing.PRESSED

    # -- the cascade ---------------------------------------------------------
    def expose(self, commitment_ids: list[str]) -> list[Commitment]:
        """Expose these, then collapse everything transitively resting on them.

        Returns every commitment whose standing changed, exposed ones first.
        """
        changed, frontier = [], list(commitment_ids)
        while frontier:
            cid = frontier.pop()
            c = self.commitments.get(cid)
            if not c or c.standing in (Standing.EXPOSED, Standing.COLLAPSED):
                continue
            c.standing = (Standing.EXPOSED if cid in commitment_ids
                          else Standing.COLLAPSED)
            changed.append(c)
            for other in self.commitments.values():
                if cid in other.rests_on:
                    frontier.append(other.id)
        return changed

    def load_bearing(self) -> dict[str, int]:
        """How many commitments would fall with each one. The pressure map."""
        counts: dict[str, int] = {}
        for cid in self.commitments:
            seen, frontier = set(), [cid]
            while frontier:
                cur = frontier.pop()
                for other in self.commitments.values():
                    if cur in other.rests_on and other.id not in seen:
                        seen.add(other.id)
                        frontier.append(other.id)
            counts[cid] = len(seen)
        return counts

    # -- what Gloss is handed before it writes -------------------------------
    def dossier(self, limit: int = 12) -> str:
        """The prompt block. Positions to defend, repairs to cite, what was asked.

        Carries no information about what the player has FOUND, because the
        ledger is never told. Probes are questions asked, which Gloss heard.
        """
        live = [c for c in self.commitments.values()
                if c.standing in (Standing.HELD, Standing.PRESSED,
                                  Standing.REPAIRED)][-limit:]
        out = ["POSITIONS YOU HAVE TAKEN AND MUST KEEP DEFENDING:"]
        out += [f"  [{c.id}] ({c.standing.value}) {c.claim}" for c in live] or ["  (none yet)"]

        if self.repairs:
            out.append("\nRECONCILIATIONS ALREADY ON THE RECORD -- cite these as "
                       "settled. Do NOT invent one that is not listed here:")
            out += [f"  [{r.id}] {r.story}" for r in self.repairs[-6:]]

        if self.probes:
            out.append("\nWHAT THE INSPECTOR HAS ASKED ABOUT (you do not know what "
                       "they have concluded):")
            for p in self.probes[-6:]:
                out.append(f"  - {'[pointed] ' if p.accusatory else ''}"
                           f"{p.doc_id or '--'}: {p.text[:90]}")
        return "\n".join(out)

    # -- persistence ---------------------------------------------------------
    def save(self, path: Path) -> None:
        path.write_text(json.dumps({
            "commitments": {k: asdict(v) for k, v in self.commitments.items()},
            "repairs": [asdict(r) for r in self.repairs],
            "probes": [asdict(p) for p in self.probes],
        }, indent=1, default=str))
