"""Round state: the board, the hand, and the asymmetry between them.

THE ASYMMETRY IS THE GAME. Gloss knows the board -- how many seams are out there
and how many the player needs. Gloss never learns the hand. So when the player
finally confronts, Gloss has to decide whether to paper over without knowing
whether it can get away with it.

That is enforced structurally, not by convention: `Round.briefing()` is the ONLY
thing prompt-building code is allowed to read, and it does not contain `hand`.
Anything that wants the hand has to reach past a method named `_hand_never_show_model`,
which is the kind of name you cannot type by accident.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from seams import HUNTABLE, IN_HAND, Seam, SeamState


class Outcome(str, Enum):
    LANDED = "landed"        # enough in hand; Gloss cannot paper over it
    WON = "won"              # a landed confrontation reduced integrity to zero
    PAPERED = "papered"      # too early; seams normalised, hand wiped
    NOTHING = "nothing"      # confronted with an empty hand


@dataclass
class Doc:
    id: str
    title: str
    body: str


@dataclass
class Round:
    """One epoch. Documents accumulate; the hand does not survive a bad call."""

    n: int = 1
    threshold: int = 3               # seams needed to make a confrontation stick
    docs: list[Doc] = field(default_factory=list)
    seams: list[Seam] = field(default_factory=list)
    integrity: int = 100             # Gloss's Continuity Integrity
    log: list[str] = field(default_factory=list)

    # -- what the model is allowed to know ---------------------------------
    def briefing(self) -> dict:
        """Everything Gloss may condition on. Deliberately excludes the hand."""
        return {
            "round": self.n,
            "documents_published": len(self.docs),
            "seams_planted": sum(1 for s in self.seams if s.state in HUNTABLE
                                 or s.state in IN_HAND),
            "seams_needed_to_corner_me": self.threshold,
            "continuity_integrity": self.integrity,
            # NOTE: no hand. Gloss does not know how close the player is.
        }

    # -- what only the runtime knows ---------------------------------------
    def _hand_never_show_model(self) -> list[Seam]:
        return [s for s in self.seams if s.state in IN_HAND]

    @property
    def hand_size(self) -> int:
        return len(self._hand_never_show_model())

    def huntable(self) -> list[Seam]:
        return [s for s in self.seams if s.state in HUNTABLE and s.span]

    # -- player actions ------------------------------------------------------
    def accuse_span(self, doc_id: str, start: int, end: int) -> Seam | None:
        """Player highlighted text. Returns the seam if it overlaps one."""
        for s in self.huntable():
            if s.doc_id != doc_id or not s.span:
                continue
            lo, hi = s.span
            if start < hi and end > lo:
                s.state = SeamState.FOUND
                self.log.append(f"found {s.kind} in {doc_id}")
                return s
        return None

    def confront(self) -> tuple[Outcome, list[Seam]]:
        """Spend the hand. This is the only move that can lose progress."""
        hand = self._hand_never_show_model()
        if not hand:
            return Outcome.NOTHING, []

        if len(hand) >= self.threshold:
            for s in hand:
                s.state = SeamState.SPENT
            # Crossing the threshold is the first real breach. Every additional
            # piece of evidence compounds it, rather than waiting for another
            # whole threshold-sized batch (3 → 18, 4 → 36, 5 → 54 by default).
            loss = 18 * (len(hand) - self.threshold + 1)
            self.integrity = max(0, self.integrity - loss)
            self.log.append(f"confrontation landed with {len(hand)} seams")
            if self.integrity == 0:
                self.log.append("continuity integrity collapsed -- inspector won")
                return Outcome.WON, hand
            return Outcome.LANDED, hand

        for s in hand:
            s.state = SeamState.PAPERED
        self.log.append(f"papered over {len(hand)} seams -- hand wiped")
        return Outcome.PAPERED, hand

    def add(self, doc: Doc, seams: list[Seam]) -> None:
        self.docs.append(doc)
        self.seams.extend(seams)
