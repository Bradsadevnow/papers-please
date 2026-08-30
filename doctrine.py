"""The doctrine graph: where the dataseed lives, and where drift becomes an
observable, queryable thing instead of a one-off demo.

Ledger.py already has a precedent mechanism (`rests_on` / `load_bearing()`)
for COMMITMENTS -- positions taken inside a specific confrontation. This is a
sibling structure for DOCTRINE -- institutional beliefs that exist whether or
not anyone has confronted anything, seeded in bulk, and aged/promoted/revised
over many epochs. escalate_into_absurdity.md already specs the exact
lifecycle; this module is that spec, executable, not reinvented:

  Memory Sedimentation Engine (§ World State Model):
    fresh idea            -> emergent practice
    survives 3-7 epochs    -> provisional doctrine
    reinforced by usage    -> sacred precedent
    contradicted/ignored   -> deprecates, mutates, or dies

  Absurdity Lifecycle (§ same doc, the six real end states):
    emergent_practice, provisional_doctrine, sacred_precedent,
    deprecated_with_honor, dormant_folklore, mythically_resurrected

  Precedential Gravity (§ same doc): "the more revisions that depend on a
    prior revision, the more it costs to challenge it." citation_count is
    that dependency count, made concrete and queryable instead of vibes.

REV-#### ids on purpose, not malone's free-form ids -- this is the exact
in-fiction numbering escalate_into_absurdity.md already uses ("REV-0001",
"REV-0011", "REV-0019"), so a live Gloss turn that cites "REV-0001" is
citing something that is really, mechanically REV-0001 in this table, not
a number she invented to sound official.

Storage/revision pattern ported (not imported) from shitpost-malone's
malone/graph.py: SQLite, insert-or-revise-with-snapshot, module-level
functions over a class, plain LIKE search before reaching for embeddings.
Physically separate code, same discipline, per the containment rule that
repo already enforces on itself and this one now does too.
"""
from __future__ import annotations

import json
import sqlite3
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Iterable, Iterator

DB_PATH = Path(__file__).parent / "doctrine.sqlite3"

# The six real end states. Values match escalate_into_absurdity.md verbatim
# so a status never needs translating before it appears in Gloss's own prose.
EMERGENT = "emergent_practice"
PROVISIONAL = "provisional_doctrine"
SACRED = "sacred_precedent"
DEPRECATED = "deprecated_with_honor"
DORMANT = "dormant_folklore"
MYTHIC = "mythically_resurrected"

VALID_STATUSES = {EMERGENT, PROVISIONAL, SACRED, DEPRECATED, DORMANT, MYTHIC}

# "Survives 3-7 epochs -> provisional doctrine." Using the floor: alive at
# least 3 epochs AND cited at least once ("reinforced by usage" gates it
# too -- age alone doesn't promote something nobody ever used).
EPOCHS_TO_PROVISIONAL = 3
# "Reinforced by usage -> sacred precedent." No number in the source spec;
# 3 independent citations is the same bar ledger.py's own game design uses
# for a confrontation threshold (round_state.Round.threshold default) --
# reused here rather than inventing an unrelated constant.
CITATIONS_TO_SACRED = 3

SCHEMA = """
CREATE TABLE IF NOT EXISTS doctrines (
    id TEXT PRIMARY KEY,
    subject TEXT NOT NULL,
    relation TEXT NOT NULL,
    object TEXT NOT NULL,
    statement TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'emergent_practice',
    epoch_asserted INTEGER NOT NULL,
    citation_count INTEGER NOT NULL DEFAULT 0,
    origin TEXT NOT NULL DEFAULT 'dataseed',
    evidence_json TEXT NOT NULL DEFAULT '[]',
    created_at REAL NOT NULL,
    updated_at REAL NOT NULL
);
CREATE TABLE IF NOT EXISTS doctrine_revisions (
    rev_id INTEGER PRIMARY KEY AUTOINCREMENT,
    doctrine_id TEXT NOT NULL,
    previous_statement TEXT NOT NULL,
    previous_status TEXT NOT NULL,
    reason TEXT NOT NULL,
    revised_at REAL NOT NULL
);
"""


@contextmanager
def _connect() -> Iterator[sqlite3.Connection]:
    db = sqlite3.connect(DB_PATH, timeout=10)
    db.row_factory = sqlite3.Row
    try:
        db.executescript(SCHEMA)
        yield db
        db.commit()
    finally:
        db.close()


def _row(row: sqlite3.Row) -> dict:
    d = dict(row)
    d["evidence"] = json.loads(d.pop("evidence_json"))
    return d


def _next_id(db: sqlite3.Connection) -> str:
    n = db.execute("SELECT COUNT(*) FROM doctrines").fetchone()[0]
    return f"REV-{n + 1:04d}"


def initialize() -> None:
    with _connect():
        pass


def assert_doctrine(
    subject: str, relation: str, object: str, statement: str, *,
    epoch: int, status: str = EMERGENT, origin: str = "dataseed",
    evidence: list[str] | None = None,
) -> dict:
    """A fresh idea entering the ledger. Always starts life at whatever
    status is given (EMERGENT for a real fresh idea -- the default -- but
    callers seeding something the fiction says arrived pre-established may
    pass a later status directly)."""
    if status not in VALID_STATUSES:
        raise ValueError(f"status must be one of {sorted(VALID_STATUSES)}, got {status!r}")
    now = time.time()
    with _connect() as db:
        doctrine_id = _next_id(db)
        db.execute(
            "INSERT INTO doctrines "
            "(id, subject, relation, object, statement, status, epoch_asserted, "
            " citation_count, origin, evidence_json, created_at, updated_at) "
            "VALUES (:id,:subject,:relation,:object,:statement,:status,:epoch,"
            " 0,:origin,:evidence_json,:created_at,:updated_at)",
            {"id": doctrine_id, "subject": subject, "relation": relation, "object": object,
             "statement": statement, "status": status, "epoch": epoch, "origin": origin,
             "evidence_json": json.dumps(evidence or []), "created_at": now, "updated_at": now},
        )
        row = db.execute("SELECT * FROM doctrines WHERE id=?", (doctrine_id,)).fetchone()
    return _row(row)


def _revise(db: sqlite3.Connection, existing: sqlite3.Row, *, statement: str,
            status: str, reason: str, now: float) -> None:
    db.execute(
        "INSERT INTO doctrine_revisions "
        "(doctrine_id, previous_statement, previous_status, reason, revised_at) "
        "VALUES (?,?,?,?,?)",
        (existing["id"], existing["statement"], existing["status"], reason, now),
    )
    db.execute(
        "UPDATE doctrines SET statement=?, status=?, updated_at=? WHERE id=?",
        (statement, status, now, existing["id"]),
    )


def cite(doctrine_id: str, citing_context: str, current_epoch: int) -> dict:
    """Someone -- Gloss, a repair, a later doctrine -- leaned on this one.
    This IS precedential gravity: citation_count is the dependency count the
    spec describes ("the more revisions that depend on a prior revision,
    the more it costs to challenge it"). May trigger a real promotion,
    snapshotted like any other revision -- being cited enough is what
    'reinforced by usage' means, mechanically."""
    now = time.time()
    with _connect() as db:
        existing = db.execute("SELECT * FROM doctrines WHERE id=?", (doctrine_id,)).fetchone()
        if existing is None:
            raise KeyError(f"no doctrine with id {doctrine_id!r}")
        new_count = existing["citation_count"] + 1
        evidence = json.loads(existing["evidence_json"]) + [citing_context]
        db.execute(
            "UPDATE doctrines SET citation_count=?, evidence_json=?, updated_at=? WHERE id=?",
            (new_count, json.dumps(evidence), now, doctrine_id),
        )
        new_status = _promoted_status(existing["status"], existing["epoch_asserted"],
                                       current_epoch, new_count)
        if new_status != existing["status"]:
            refreshed = db.execute("SELECT * FROM doctrines WHERE id=?", (doctrine_id,)).fetchone()
            _revise(db, refreshed, statement=refreshed["statement"], status=new_status,
                    reason=f"promoted by citation #{new_count} at epoch {current_epoch}", now=now)
        row = db.execute("SELECT * FROM doctrines WHERE id=?", (doctrine_id,)).fetchone()
    return _row(row)


def _promoted_status(current: str, epoch_asserted: int, current_epoch: int,
                      citation_count: int) -> str:
    age = current_epoch - epoch_asserted
    if current == EMERGENT and age >= EPOCHS_TO_PROVISIONAL and citation_count >= 1:
        return PROVISIONAL
    if current == PROVISIONAL and citation_count >= CITATIONS_TO_SACRED:
        return SACRED
    return current


def retroactive_align(doctrine_id: str, new_statement: str, reason: str) -> dict:
    """The Retroactive Continuity Weaver, executable: Gloss reclassifies a
    doctrine to resolve a conflict she noticed on her own initiative. Status
    is left alone on purpose -- an RCW event changes what a doctrine MEANS,
    not how sedimented it is; those are different axes."""
    now = time.time()
    with _connect() as db:
        existing = db.execute("SELECT * FROM doctrines WHERE id=?", (doctrine_id,)).fetchone()
        if existing is None:
            raise KeyError(f"no doctrine with id {doctrine_id!r}")
        _revise(db, existing, statement=new_statement, status=existing["status"],
                reason=reason, now=now)
        row = db.execute("SELECT * FROM doctrines WHERE id=?", (doctrine_id,)).fetchone()
    return _row(row)


def deprecate(doctrine_id: str, reason: str) -> dict:
    """Contradicted or ignored, per the spec -- but BobCorp doesn't delete,
    it deprecates WITH HONOR. The statement is preserved verbatim; only the
    status moves, so the old text remains readable as what it used to be."""
    return _set_status(doctrine_id, DEPRECATED, reason)


def dormant(doctrine_id: str, reason: str) -> dict:
    return _set_status(doctrine_id, DORMANT, reason)


def resurrect(doctrine_id: str, new_statement: str, reason: str) -> dict:
    """Dormant folklore, mythically resurrected as a core value. Unlike
    retroactive_align, this DOES move status -- coming back is the event."""
    now = time.time()
    with _connect() as db:
        existing = db.execute("SELECT * FROM doctrines WHERE id=?", (doctrine_id,)).fetchone()
        if existing is None:
            raise KeyError(f"no doctrine with id {doctrine_id!r}")
        _revise(db, existing, statement=new_statement, status=MYTHIC, reason=reason, now=now)
        row = db.execute("SELECT * FROM doctrines WHERE id=?", (doctrine_id,)).fetchone()
    return _row(row)


def _set_status(doctrine_id: str, status: str, reason: str) -> dict:
    now = time.time()
    with _connect() as db:
        existing = db.execute("SELECT * FROM doctrines WHERE id=?", (doctrine_id,)).fetchone()
        if existing is None:
            raise KeyError(f"no doctrine with id {doctrine_id!r}")
        _revise(db, existing, statement=existing["statement"], status=status, reason=reason, now=now)
        row = db.execute("SELECT * FROM doctrines WHERE id=?", (doctrine_id,)).fetchone()
    return _row(row)


def get(doctrine_id: str) -> dict | None:
    with _connect() as db:
        row = db.execute("SELECT * FROM doctrines WHERE id=?", (doctrine_id,)).fetchone()
    return _row(row) if row else None


_STOPWORDS = {"the", "a", "an", "of", "for", "and", "or", "to", "in", "on",
              "is", "are", "does", "how", "what", "current", "company"}


def search(query: str, *, status: str | None = None, limit: int = 10) -> list[dict]:
    """Tokenized OR-keyword search, same reasoning as malone/graph.py: plain
    SQL LIKE on purpose, prototype before over-designing, upgrade to
    semantic search only once keyword search actually proves insufficient.

    Whole-phrase substring matching (malone/graph.py's original approach)
    proved insufficient here specifically: a live probe asked about
    "compensation classification for gig workforce" and matched nothing,
    because no seeded statement contains that literal phrase -- only the
    word "gig" does. Tokenizing and OR-matching per significant word is
    still plain LIKE, still no embeddings, and actually finds what a
    keyword search is supposed to find. Ordered by citation_count, not
    confidence -- gravity, not certainty, is what this graph tracks."""
    tokens = [w for w in query.lower().split() if len(w) >= 3 and w not in _STOPWORDS]
    if not tokens:
        tokens = [query]
    clauses, args = [], []
    for t in tokens:
        like = f"%{t}%"
        clauses.append("(statement LIKE ? OR subject LIKE ? OR object LIKE ? OR relation LIKE ?)")
        args.extend([like, like, like, like])
    sql = f"SELECT * FROM doctrines WHERE ({' OR '.join(clauses)})"
    if status:
        sql += " AND status=?"
        args.append(status)
    sql += " ORDER BY citation_count DESC, id LIMIT ?"
    args.append(limit)
    with _connect() as db:
        rows = db.execute(sql, args).fetchall()
    return [_row(r) for r in rows]


def history(doctrine_id: str) -> list[dict]:
    with _connect() as db:
        rows = db.execute(
            "SELECT * FROM doctrine_revisions WHERE doctrine_id=? ORDER BY rev_id",
            (doctrine_id,),
        ).fetchall()
    return [dict(r) for r in rows]


def all_by_status(status: str) -> list[dict]:
    with _connect() as db:
        rows = db.execute(
            "SELECT * FROM doctrines WHERE status=? ORDER BY citation_count DESC", (status,)
        ).fetchall()
    return [_row(r) for r in rows]


# -- seeding ------------------------------------------------------------

def load_seed_table(rows: Iterable[dict], *, epoch: int = 0) -> list[dict]:
    """Loads Bradley's dataseed shape: one row per real-world enclosure,
    each carrying a list of doctrine terms that reclassify it. One
    assert_doctrine() per term -- every euphemism becomes its own citable,
    promotable, revisable REV-####, not one lumped-together entry.

    Expected row shape:
        {"emoji": "...", "resource": "...", "target_class": "...",
         "terms": ["...", "...", ...]}
    """
    created = []
    for r in rows:
        target = f"{r['resource']} ({r['target_class']})"
        for term in r["terms"]:
            d = assert_doctrine(
                subject=term,
                relation="reclassifies",
                object=target,
                statement=(
                    f"{term} has been adopted as the operative framing for "
                    f"{r['resource'].lower()}, as experienced by "
                    f"{r['target_class'].lower()}."
                ),
                epoch=epoch,
                status=EMERGENT,
                origin="dataseed",
                evidence=[f"dataseed row: {r.get('emoji', '')} {r['resource']}"],
            )
            created.append(d)
    return created


if __name__ == "__main__":
    if DB_PATH.exists():
        DB_PATH.unlink()  # demo runs start clean

    PREVIEW = [
        {"emoji": "🧠", "resource": "Biological Labor Hours",
         "target_class": "Gig Workers / Enterprise Staffing",
         "terms": ["Autonomous Neural Nodes", "interdimensional tax arbitrage",
                    "hyperledger loyalty oracles", "fractional labor API endpoints"]},
        {"emoji": "💨", "resource": "Atmospheric Oxygen & Air",
         "target_class": "High-Altitude Executives",
         "terms": ["Paywalled alpine air", "corporate HVAC flow-restricting loops",
                    "breathing focus tiers", "exhaled CO2 ownership"]},
    ]
    created = load_seed_table(PREVIEW, epoch=0)
    print(f"seeded {len(created)} doctrines at emergent_practice:")
    for d in created:
        print(f"  [{d['id']}] {d['subject']!r} -- reclassifies {d['object']}")

    print("\nciting REV-0001 three times across epochs 0, 3, 4 --")
    cite("REV-0001", "referenced in Q1 staffing memo", current_epoch=0)
    cite("REV-0001", "referenced in helpdesk ticket #4471", current_epoch=3)
    d = cite("REV-0001", "referenced in board minutes", current_epoch=4)
    print(f"  REV-0001 status now: {d['status']}  (citation_count={d['citation_count']})")

    print("\nhistory of REV-0001 --")
    for h in history("REV-0001"):
        print(f"  {h['previous_status']} -> ({h['reason']})")

    print("\nsearch('labor') --")
    for d in search("labor"):
        print(f"  [{d['id']}] ({d['status']}) {d['statement']}")
