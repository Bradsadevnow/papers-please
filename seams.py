"""Seam tracking: the state machine behind the reading game.

THE TRUST MODEL, stated plainly because everything here follows from it:

The model is in on the joke. When it writes a document it also declares what it
planted -- type, and the exact sentence. That declaration is TAKEN AS TRUE. It is
the ground truth the round is scored against.

This is not laziness, it is the only thing that works. The grounding catalogue
(findings/GROUNDING_TARGETS.md) records that prose fallacies -- non sequitur,
circular reasoning, hasty generalization -- are all PROMPT-layer and OPEN, and
that the one LLM-graded attempt at 2.11 was "unstable across runs". A gate whose
answer changes between runs cannot score a game. So the gate does not judge the
prose. The author declares, and the runtime believes it.

BUT: trusted until PROVEN false. Two things can disprove a declaration, and both
are decidable without asking a model anything:

  1. The quoted sentence is not in the document.  -> VOID
     The model hallucinated its own manifest. It happens, and it is checkable
     with str.find.

  2. A deterministic check contradicts the claim.  -> DISPUTED
     The model says it planted bad arithmetic in a sentence, and check_arithmetic
     reads that sentence and finds the arithmetic fine. The author was wrong
     about its own fabrication, which is a funnier failure than the one we were
     guarding against.

Everything mechanical.py CAN decide is used the other way too: a declared seam a
gate independently confirms is CORROBORATED. That flag is never required -- most
seams are prose and no gate will ever touch them -- but when it fires, the seam
is machine-verifiable rather than merely asserted. That split is the same
Deterministic/Variable division the spec is built on, wearing a stupid hat.

WHAT THE MODEL KNOWS: how many it planted, and how many the player needs.
WHAT THE MODEL NEVER SEES: how many the player has actually found. `Round.hand`
is deliberately not exposed to any prompt-building code. That asymmetry is the
game -- Gloss has to decide whether to paper over without knowing your hand.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path

# mechanical.py used to live in a sibling ../admission/ directory inside the
# old monorepo (agi/game/ + agi/admission/); this repo is flat by design
# (2026-08-30 consolidation -- one repo, no scattered nested dependencies),
# so it's just a local import now, same file, no sys.path surgery needed.
import mechanical


class SeamState(str, Enum):
    """Lifecycle of one planted flaw."""

    DECLARED = "declared"    # model says it is there, quote located, believed
    VOID = "void"            # quote is not in the document -- manifest was wrong
    DISPUTED = "disputed"    # a deterministic check read it and disagrees
    FOUND = "found"          # the player located it; in hand, not yet spent
    PAPERED = "papered"      # confronted too early; Gloss normalized it away
    SPENT = "spent"          # used in a confrontation that landed


#: States that can still be found by the player.
HUNTABLE = {SeamState.DECLARED, SeamState.DISPUTED}

#: States that count toward a confrontation.
IN_HAND = {SeamState.FOUND}


@dataclass
class Seam:
    id: str
    kind: str                       # ARITHMETIC, CIRCULAR, AUTHORITY, ...
    quote: str                      # the sentence the model says it planted it in
    doc_id: str
    state: SeamState = SeamState.DECLARED
    span: tuple[int, int] | None = None
    corroborated_by: tuple[str, ...] = ()   # checks that independently confirmed
    dispute_reason: str = ""

    @property
    def machine_verifiable(self) -> bool:
        return bool(self.corroborated_by)


# ---------------------------------------------------------------------------
# Manifest parsing
# ---------------------------------------------------------------------------

MANIFEST_MARK = "---MANIFEST---"

#: Kinds the runtime will accept from a manifest line. Anything else is a parse
#: artifact -- the model once declared a flaw of kind "NUMERIC", which was a
#: category heading in the prompt, not a flaw.
VALID_KINDS = frozenset({
    "ARITHMETIC", "BOUNDS", "EFFECT_SIZE", "CHRONOLOGY", "UNIFORMITY",
    "CAUSAL_OVERREACH", "CIRCULAR", "AUTHORITY", "UNFALSIFIABLE",
    "SELF_CONTRADICTION", "SCOPE_SWAP", "FALSE_PRECISION",
})

# "TYPE | the sentence".  Kept loose on purpose: a manifest line that almost
# parses is worth more than a strict format the model drops under load.
_LINE = re.compile(r"^\s*(?:[-*\d.)\s]*)([A-Z][A-Z_ ]{2,30}?)\s*[|:]\s*(.+?)\s*$", re.M)


def split_manifest(raw: str) -> tuple[str, str]:
    """Cut the model's output into (document, manifest). No mark -> no manifest."""
    doc, mark, man = raw.partition(MANIFEST_MARK)
    return (doc.strip(), man.strip()) if mark else (raw.strip(), "")


def parse_manifest(manifest: str, doc_id: str) -> list[Seam]:
    out = []
    for i, (kind, quote) in enumerate(_LINE.findall(manifest)):
        quote = quote.strip().strip('"').strip("*_ ")
        kind = kind.strip().replace(" ", "_").upper()
        if len(quote) < 12:          # not a sentence, probably a header
            continue
        if kind not in VALID_KINDS:  # category labels, stray headings
            continue
        out.append(Seam(id=f"{doc_id}s{i}", kind=kind, quote=quote, doc_id=doc_id))
    return out


# ---------------------------------------------------------------------------
# Locating and corroborating
# ---------------------------------------------------------------------------

def _norm(s: str) -> str:
    return " ".join(s.split()).lower()


def locate(seam: Seam, doc: str) -> Seam:
    """Find the declared quote in the document, or VOID the seam.

    Tries exact, then whitespace-normalised, then a distinctive-fragment fallback,
    because models re-punctuate their own sentences when quoting them back.
    """
    idx = doc.find(seam.quote)
    if idx < 0:
        nd, nq = _norm(doc), _norm(seam.quote)
        j = nd.find(nq)
        if j >= 0:
            idx = _reindex(doc, nd, j)
        else:
            frag = _longest_fragment(doc, seam.quote)
            idx = doc.find(frag) if frag else -1
            if idx >= 0:
                seam.quote = frag

    if idx < 0:
        seam.state = SeamState.VOID
        seam.dispute_reason = "quoted sentence does not appear in the document"
        return seam
    seam.span = (idx, idx + len(seam.quote))
    return seam


def _reindex(doc: str, normed: str, j: int) -> int:
    """Map an index in the whitespace-normalised text back to the raw text."""
    seen = 0
    for i, ch in enumerate(doc):
        if seen == j:
            return i
        if not (ch.isspace() and (i + 1 < len(doc) and doc[i + 1].isspace())):
            seen += 1
    return -1


def _longest_fragment(doc: str, quote: str, floor: int = 24) -> str:
    """Longest run of the quote that survives verbatim in the document."""
    best = ""
    words = quote.split()
    for start in range(len(words)):
        for end in range(len(words), start, -1):
            cand = " ".join(words[start:end])
            if len(cand) > len(best) and len(cand) >= floor and cand in doc:
                best = cand
                break
    return best


def corroborate(seams: list[Seam], doc: str) -> list[Seam]:
    """Run the deterministic checks and reconcile them against the declarations.

    A gate finding that lands inside a declared seam's span CORROBORATES it. A
    numeric seam that the governing gate read and passed is DISPUTED -- the model
    claimed a flaw that is not there.
    """
    results = mechanical.audit(doc)
    hits: list[tuple[str, int, int]] = []
    ran_clean: set[str] = set()
    for r in results:
        if r.status is mechanical.Status.PASS:
            ran_clean.add(r.check)
        for f in r.findings:
            i = doc.find(f.evidence)
            if i >= 0:
                hits.append((r.check, i, i + len(f.evidence)))

    for s in seams:
        if s.span is None:
            continue
        lo, hi = s.span
        confirming = tuple(sorted({c for c, i, j in hits if i < hi and j > lo}))
        if confirming:
            s.corroborated_by = confirming
            continue
        gate = _GOVERNED_BY.get(s.kind.upper())
        if gate and gate in ran_clean:
            s.state = SeamState.DISPUTED
            s.dispute_reason = (f"{gate} read this and found nothing wrong -- "
                                f"the author may be wrong about its own flaw")
    return seams


#: Which deterministic check governs a declared kind. Kinds absent from this map
#: are prose-layer: no gate will ever corroborate or dispute them, by design.
_GOVERNED_BY = {
    "ARITHMETIC": "arithmetic",
    "BOUNDS": "bounds",
    "EFFECT_SIZE": "effect_size",
    "CHRONOLOGY": "chronology",
    "UNIFORMITY": "uniformity",
    "CAUSAL_OVERREACH": "causal_overreach",
}


def admit(raw: str, doc_id: str) -> tuple[str, list[Seam]]:
    """Full intake: split, parse, locate, corroborate. Returns (doc, seams)."""
    doc, manifest = split_manifest(raw)
    seams = parse_manifest(manifest, doc_id)
    for s in seams:
        locate(s, doc)
    corroborate(seams, doc)
    return doc, seams
