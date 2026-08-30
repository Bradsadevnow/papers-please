"""The seeded corpus: the lab's existing paper trail.

WHY SEEDED RATHER THAN GENERATED. Documents written fresh each round cannot
contradict each other in any way the player can rely on, because there is nothing
stable to contradict. A frozen corpus turns the whole archive into the board.
Gloss plants a claim in a NEW document that collides with a specific line in an
OLD one, and the player's job is to remember, or to search, or to read carefully
enough to notice. That is the Papers Please move: the discrepancy is between two
documents, not inside one.

It also removes generation variance from the ground truth. The corpus is on disk,
identical every run, so a seam that points into it points at the same characters
forever.

BOTH SIDES READ THE SAME SHELF. Gloss searches it to find something worth
contradicting; the player searches it to catch the contradiction. Neither has an
index the other lacks. The only asymmetry is the one in Round: Gloss knows what it
planted, and never learns what the player found.

Search is deliberately dumb -- scored keyword overlap, stdlib only, no embeddings.
It has to be identical for both callers and explainable when it misses, and an
embedding index would be neither.
"""

from __future__ import annotations

import json
import math
import re
from collections import Counter
from dataclasses import asdict, dataclass, field
from pathlib import Path

STORE = Path(__file__).resolve().parent / "corpus.json"

_WORD = re.compile(r"[a-z0-9']+")
_STOP = frozenset("""a an the of and or to in on for with by is are was were be been
being at as from that this these those it its we our us they their which not no
than then so such may can will would could should has have had do does did if""".split())


def tokens(text: str) -> list[str]:
    return [w for w in _WORD.findall((text or "").lower()) if w not in _STOP]


@dataclass
class Document:
    id: str
    title: str
    date: str                 # ISO, so chronology seams have something to bite
    kind: str                 # memo | report | eval | incident | policy | minutes
    author: str
    body: str
    grade: float = 0.0        # measured Flesch-Kincaid, the difficulty dial
    seeded: bool = True       # False for documents Gloss publishes mid-game

    def excerpt(self, n: int = 240) -> str:
        return " ".join(self.body.split())[:n]


@dataclass
class Corpus:
    docs: dict[str, Document] = field(default_factory=dict)
    _df: Counter = field(default_factory=Counter, repr=False)

    # -- persistence ---------------------------------------------------------
    @classmethod
    def load(cls, path: Path = STORE) -> "Corpus":
        c = cls()
        if path.exists():
            for row in json.loads(path.read_text()):
                c.add(Document(**row), reindex=False)
            c.reindex()
        return c

    def save(self, path: Path = STORE) -> None:
        path.write_text(json.dumps([asdict(d) for d in self.docs.values()],
                                   indent=1))

    # -- building ------------------------------------------------------------
    def add(self, doc: Document, reindex: bool = True) -> None:
        self.docs[doc.id] = doc
        if reindex:
            self.reindex()

    def reindex(self) -> None:
        self._df = Counter()
        for d in self.docs.values():
            for t in set(tokens(d.title + " " + d.body)):
                self._df[t] += 1

    # -- search --------------------------------------------------------------
    def search(self, query: str, limit: int = 5) -> list[dict]:
        """Scored keyword overlap with an IDF weight. Same call for both sides."""
        q = tokens(query)
        if not q or not self.docs:
            return []
        n = len(self.docs)
        out = []
        for d in self.docs.values():
            toks = tokens(d.title + " " + d.body)
            if not toks:
                continue
            tf = Counter(toks)
            score = 0.0
            for term in set(q):
                if term not in tf:
                    continue
                idf = math.log(1 + n / (1 + self._df.get(term, 0)))
                score += (1 + math.log(tf[term])) * idf
            # title hits are worth more -- that is how people actually search
            score += 2.0 * sum(1 for t in set(q) if t in tokens(d.title))
            if score > 0:
                out.append((score, d))
        out.sort(key=lambda p: -p[0])
        return [{"id": d.id, "title": d.title, "date": d.date, "kind": d.kind,
                 "author": d.author, "score": round(s, 2), "excerpt": d.excerpt()}
                for s, d in out[:limit]]

    def get(self, doc_id: str) -> Document | None:
        return self.docs.get(doc_id)

    def lines(self, doc_id: str) -> list[tuple[int, str]]:
        """Sentence-ish units with character offsets, for pointing at a claim."""
        d = self.docs.get(doc_id)
        if not d:
            return []
        out, pos = [], 0
        for part in re.split(r"(?<=[.!?])\s+", d.body):
            i = d.body.find(part, pos)
            if i >= 0 and len(part.strip()) > 20:
                out.append((i, part.strip()))
                pos = i + len(part)
        return out

    def __len__(self) -> int:
        return len(self.docs)
