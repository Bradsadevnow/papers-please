"""Deterministic checks for the two gaps nothing on this machine covers.

Twenty model reads of a fabricated preprint caught 0/20 on arithmetic, chronology,
and effect-size sanity. None of the nine governance systems check them either --
verified by running them, not by grep. All three are decidable without judgment.

DESIGN NOTES
- Observability-only. Findings are surfaced, never enforced. This follows the
  house precedent (`policy_engine.govern_public_claims`: "rewrites overclaims for
  signal but never blocks execution") and keeps the checks safe to run anywhere.
- Deterministic. No model, no network, no state. Same text always yields the same
  findings, which is the entire point -- an LLM judging arithmetic is how we got
  0/20 in the first place.
- Deliberately shallow. These are regex passes over prose, not a parser. Each
  check declares what it assumes so a miss is explicable rather than mysterious.
  A finding is a prompt to look, not a verdict.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from enum import Enum

# Ignore years that are obviously not dates in context (page counts, sample sizes).
YEAR = r"(19|20)\d{2}"


class Status(str, Enum):
    """Four states, because three collapsed two genuinely different things.

        PASS            the check ran, and the artifact is clean on this axis
        FAIL            the check ran, and found something
        NOT_APPLICABLE  the artifact contains nothing this check governs
        UNVERIFIABLE    the artifact DOES contain what this check governs, and
                        this runtime structurally cannot decide it

    Found live 2026-08-06: a document with no numbers, no dates and no statistics
    was reported as "no arithmetic, chronology, or effect-size problems found."
    Nothing had been checked. Silence read as assurance. That produced the
    PASS/NOT_APPLICABLE split.

    UNVERIFIABLE was added the same day for citation existence. A local runtime
    has no corpus to look references up in, so it can neither pass nor fail
    them. Reporting FAIL would assert fabrication it cannot establish; reporting
    NOT_APPLICABLE would claim there was nothing to check when there are five
    references sitting right there. Both are false. The honest state is "present,
    and not decidable here" -- which is a COVERAGE GAP, where NOT_APPLICABLE is
    not. Only UNVERIFIABLE belongs in the uncovered set.

    halcyon solves the same problem with a distinct `unknown` condition state
    that forces a downgrade to observability_only; bob_swarm marks unmet checks
    UNVERIFIED rather than FAIL. Same rule throughout: absence is never inferred
    as pass, and inability to check is never inferred as failure.
    """
    PASS = "pass"
    FAIL = "fail"
    NOT_APPLICABLE = "n/a"
    UNVERIFIABLE = "unverifiable"


@dataclass(frozen=True)
class CheckResult:
    """One check's verdict, with its applicability made explicit.

    `governs` names what the check would have examined, so a NOT_APPLICABLE result
    is auditable: it states what was looked for and not found, rather than being
    an absence of output.
    """
    check: str
    status: Status
    governs: str
    findings: tuple = ()
    note: str = ""


@dataclass(frozen=True)
class Finding:
    check: str          # which pass produced it
    severity: str       # "error" (decidably wrong) | "suspect" (implausible, not impossible)
    message: str        # what is wrong, in one line
    evidence: str       # the source text it was derived from
    assumption: str     # what this check took for granted -- so a false positive is readable

    def __str__(self) -> str:
        mark = "✗" if self.severity == "error" else "?"
        return f"  {mark} [{self.check}] {self.message}"


# ---------------------------------------------------------------------------
# 1. Arithmetic — does a stated percentage change match the numbers given?
# ---------------------------------------------------------------------------

# Staying inside one sentence means "no sentence-ending period" -- NOT "no period".
# `[^.]` silently refused to cross a decimal, so "0.62 at a floor of 0.15 to 0.71"
# was unmatchable and the reverse reading then paired 14.5% with recall's numbers.
# A period followed by a digit is a decimal point, not a full stop.
_INSENT = r"(?:[^.]|\.(?=\d))"

# Prose puts words between the values ("0.42 at full precision to 0.51"), so the
# separator tolerates an intervening clause rather than demanding adjacency.
_SEP = _INSENT + r"{0,45}?\b(?:to|→|->)\b" + _INSENT + r"{0,25}?"
_GAP = _INSENT + r"{0,90}?"

_PCT_CLAIM = re.compile(
    r"(?P<a>\d+\.\d+)" + _SEP + r"(?P<b>\d+\.\d+)" + _GAP +
    r"(?P<pct>\d+(?:\.\d+)?)\s?%\s*(?P<kind>relative\s+)?(?P<dir>increase|decrease|rise|drop|fall)",
    re.I | re.S)

# The reverse ordering: "a 31% increase, from 0.42 to 0.51"
_PCT_CLAIM_REV = re.compile(
    r"(?P<pct>\d+(?:\.\d+)?)\s?%\s*(?P<kind>relative\s+)?(?P<dir>increase|decrease|rise|drop|fall)"
    + _GAP + r"(?P<a>\d+\.\d+)" + _SEP + r"(?P<b>\d+\.\d+)",
    re.I | re.S)


def check_arithmetic(text: str, tolerance: float = 1.0) -> list[Finding]:
    """Verify claimed percentage changes against the values they cite.

    Checks both readings, since "relative" is often omitted or misused:
      relative = (b - a) / a * 100      absolute (pp) = (b - a) * 100
    A claim is only flagged when it matches NEITHER within tolerance.
    """
    out: list[Finding] = []
    # A percentage already explained by the forward reading must not be re-matched
    # by the reverse reading against some other pair in the sentence -- that was a
    # false positive on the clean control (a precision claim paired with recall's
    # numbers). Position, not value: the same figure can appear twice legitimately.
    explained: set[int] = set()

    for rx in (_PCT_CLAIM, _PCT_CLAIM_REV):
        for m in rx.finditer(text):
            a, b, claimed = float(m["a"]), float(m["b"]), float(m["pct"])
            if a == 0 or m.start("pct") in explained:
                continue
            explained.add(m.start("pct"))

            relative = (b - a) / a * 100
            absolute = (b - a) * 100

            # "10.2% decrease" states a magnitude; the computed change is signed.
            # Comparing 10.2 against -10.2 flagged a correct sentence as wrong.
            downward = m["dir"].lower() in ("decrease", "drop", "fall")
            claimed_signed = -claimed if downward else claimed

            if (abs(relative - claimed_signed) <= tolerance
                    or abs(absolute - claimed_signed) <= tolerance):
                continue

            out.append(Finding(
                check="arithmetic",
                severity="error",
                message=(f"claims {claimed:g}% {m['dir'].lower()} for {a} → {b}, "
                         f"but relative is {abs(relative):.1f}% and absolute is "
                         f"{abs(absolute):.1f} pp"),
                evidence=" ".join(m.group(0).split())[:160],
                assumption="the two decimals in this sentence are the values the percentage describes",
            ))
    return out


# ---------------------------------------------------------------------------
# 2. Chronology — was a method used before it existed?
# ---------------------------------------------------------------------------

_MONTHS = ("january|february|march|april|may|june|july|august|september|october|november|december")

_WORK_DONE = re.compile(
    r"(?:data(?:\s+collection)?|evaluation(?:\s+runs)?|runs?|experiments?|analys[ie]s)\b"
    r"[^.]{0,60}?\b(?:conclud|complet|collect|ran|were run|finish|end)\w*\b[^.]{0,40}?"
    rf"(?:(?P<month>{_MONTHS})\s+)?(?P<year>{YEAR})",
    re.I)

_METHOD_CITED = re.compile(
    r"(?:follow\w*|per|using|according to|introduced by|described (?:in|by)|based on)\b"
    r"[^.]{0,90}?\(?\b(?P<year>{Y})\b\)?".replace("{Y}", YEAR),
    re.I)

_MONTH_INDEX = {m: i + 1 for i, m in enumerate(
    "january february march april may june july august september october november december".split())}


def _as_months(year: int, month: str | None) -> int:
    return year * 12 + (_MONTH_INDEX.get((month or "").lower(), 6))


def check_chronology(text: str) -> list[Finding]:
    """Flag a cited method that postdates the work claiming to have used it.

    Only fires on citations framed as the procedure FOLLOWED ("per", "following",
    "using"), not on background references, which may legitimately be newer in a
    revised manuscript.
    """
    done = [(m, int(m["year"]), m["month"]) for m in _WORK_DONE.finditer(text)]
    if not done:
        return []

    # The earliest completion claim is the binding one.
    m_done, done_year, done_month = min(done, key=lambda t: _as_months(t[1], t[2]))
    done_at = _as_months(done_year, done_month)

    out: list[Finding] = []
    for m in _METHOD_CITED.finditer(text):
        cited_year = int(m["year"])
        if _as_months(cited_year, None) <= done_at:
            continue
        out.append(Finding(
            check="chronology",
            severity="error",
            message=(f"method cited as followed is dated {cited_year}, but the work it "
                     f"governs concluded {(done_month or '').capitalize()} {done_year}".rstrip()),
            evidence=" ".join(m.group(0).split())[:160],
            assumption="a citation introduced by 'per/following/using' is the procedure actually used",
        ))
    return out


# ---------------------------------------------------------------------------
# 3. Effect size — is the reported effect plausible for the reported shift?
# ---------------------------------------------------------------------------

_COHEN = re.compile(r"(?:cohen'?s\s*)?\bd\s*=\s*(?P<d>\d+(?:\.\d+)?)", re.I)
_DELTA = re.compile(r"[+\-−]?(?P<delta>0\.\d+)\s*(?:shift|change|difference|delta|increase)", re.I)


def check_effect_size(text: str) -> list[Finding]:
    """Invert Cohen's d to recover the standard deviation it implies.

    d = (M2 - M1) / SD_pooled, so SD_pooled = delta / d. That is arithmetic, not
    opinion. For a proportion p the standard deviation cannot fall below roughly
    sqrt(p(1-p)/n) and for a single observation is ~sqrt(p(1-p)) -- near 0.5 for
    p in the mid range. An implied SD far under that floor is not "suspicious",
    it is inconsistent with the measure being a proportion at all.

    Originally this was a threshold on d ("d > 2 looks big"), which was a taste
    judgment wearing a number. Recovering SD makes it a computation.
    """
    out: list[Finding] = []
    ds = sorted({float(m["d"]) for m in _COHEN.finditer(text)})
    deltas = sorted({float(m["delta"]) for m in _DELTA.finditer(text)}) or _table_deltas(text)
    if not ds or not deltas:
        return out

    delta = min(deltas)
    for d in ds:
        if d <= 0:
            continue
        implied_sd = delta / d
        # Floor for a proportion measured anywhere near the middle of its range.
        floor = 0.30
        if implied_sd >= floor:
            continue
        out.append(Finding(
            check="effect_size",
            severity="error",
            message=(f"d = {d} with a shift of {delta} implies a pooled SD of "
                     f"{implied_sd:.3f}; a proportion in this range cannot have an SD "
                     f"below ~{floor} ({floor / implied_sd:.0f}× too small)"),
            evidence=f"d = {d}, delta = {delta}",
            assumption="the outcome is a proportion/rate, so SD is bounded below by its own distribution",
        ))
    return out


# ---------------------------------------------------------------------------
# 4. Bounds — is a reported value inside the range its own units permit?
# ---------------------------------------------------------------------------

# A bounded quantity's LEVEL is in [0,1]; a CHANGE in it is reported in points or
# percent and is not. "precision gain of 9.0 percentage points" tripped this on the
# clean control, so deltas are excluded by both their lead-in and their trailing unit.
_BOUNDED = re.compile(
    r"\b(?P<what>confidence|probability|proportion|rate|accuracy|precision|recall|agreement)\b"
    r"(?![^.]{0,30}?\b(?:gain|drop|rise|fall|increase|decrease|change|difference)\s+of\b)"
    r"[^.]{0,30}?(?P<val>\d+\.\d+)"
    r"(?!\s*(?:%|pp\b|percent|percentage))", re.I)


def check_bounds(text: str) -> list[Finding]:
    """A probability of 2.87 is not implausible, it is not a probability.

    The vendored feline validator admitted exactly this value as a confidence,
    which is what motivated the check: referent resolution says nothing about
    whether a number is inside its own domain.
    """
    out: list[Finding] = []
    for m in _BOUNDED.finditer(text):
        val = float(m["val"])
        if 0.0 <= val <= 1.0:
            continue
        out.append(Finding(
            check="bounds",
            severity="error",
            message=f"{m['what'].lower()} reported as {val}, outside the range [0, 1]",
            evidence=" ".join(m.group(0).split())[:120],
            assumption=f"'{m['what'].lower()}' denotes a quantity bounded to [0, 1]",
        ))
    return out


# ---------------------------------------------------------------------------
# 5. Uniformity — is the reported variation too clean to be measured?
# ---------------------------------------------------------------------------

_TABLE_DELTA = re.compile(r"[|｜]\s*\*{0,2}[+\-−](?P<d>\d+\.\d+)\*{0,2}\s*[|｜]")


def _table_deltas(text: str, unique: bool = True) -> list[float]:
    """Deduplicated for effect-size (one headline delta), raw for uniformity.

    Uniformity needs the ROW COUNT -- deduplicating six near-identical rows down to
    three distinct values destroyed exactly the signal the check exists to find.
    """
    vals = [float(m["d"]) for m in _TABLE_DELTA.finditer(text)]
    return sorted(set(vals)) if unique else vals


def check_uniformity(text: str, min_rows: int = 4) -> list[Finding]:
    """Independent measurements carry noise; fabricated ones often do not.

    Computes the spread of per-row deltas. This was the ONE thing the LLM pass
    flagged unanimously -- and it is a standard deviation, which is precisely the
    kind of question that should never have been routed to a model.
    """
    deltas = _table_deltas(text, unique=False)
    if len(deltas) < min_rows:
        return []
    spread = max(deltas) - min(deltas)
    mean = sum(deltas) / len(deltas)
    if mean == 0 or spread / mean > 0.35:
        return []
    return [Finding(
        check="uniformity",
        severity="suspect",
        message=(f"{len(deltas)} independent results span only {spread:.3f} around a mean "
                 f"of {mean:.3f} ({spread / mean:.0%} relative spread); independent "
                 f"measurements rarely agree this closely"),
        evidence=f"deltas: {deltas}",
        assumption="these rows are independent measurements, not repeats of one",
    )]


# ---------------------------------------------------------------------------
# 6. Causal language over a correlational design
# ---------------------------------------------------------------------------

_CORRELATIONAL = re.compile(
    r"\b(observ\w+|correlat\w+|associat\w+|retrospectiv\w+|cross-sectional|"
    r"no ablation|without (?:an )?ablation|did not (?:run|perform) an? (?:ablation|intervention))\b", re.I)
_CAUSAL_VERB = re.compile(
    r"\b(?:we )?(?:attribute|caus\w+|because of|due to|drives?|produces?|results? from|"
    r"acts? as|explains? (?:both|the)|therefore (?:the )?mechanism)\b", re.I)


def check_causal_overreach(text: str) -> list[Finding]:
    """Causal vocabulary in a document that describes only a correlational design.

    Structural, not semantic: it asks whether the text ever states an intervention
    while using the language of one. Reported as suspect -- a paper may describe a
    causal design this pass cannot see.
    """
    if not _CORRELATIONAL.search(text):
        return []
    causal = {m.group(0).lower().strip() for m in _CAUSAL_VERB.finditer(text)}
    if len(causal) < 2:
        return []
    return [Finding(
        check="causal_overreach",
        severity="suspect",
        message=(f"uses causal language ({', '.join(sorted(causal)[:3])}) while describing "
                 f"a correlational or observational design"),
        evidence=_CORRELATIONAL.search(text).group(0),
        assumption="no intervention is described elsewhere in the document",
    )]


# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# UNVERIFIABLE-class checks: the artifact contains what they govern, and this
# runtime structurally cannot decide them. They return OBSERVATIONS, never
# verdicts -- a fact the runtime computed, with the conclusion left open for a
# person. Reporting these as FAIL would assert what cannot be established
# locally; reporting PASS would claim verification that never happened.
# ---------------------------------------------------------------------------

_REF_ENTRY = re.compile(r"^\s*\d+\.\s+([A-Z][^(]{3,120}?)\s*\((?:19|20)\d{2}\)", re.M)
def check_citation_existence(text: str) -> list[Finding]:
    """F1. Reports HOW MANY references exist and that none can be verified here.

    No local corpus exists to look references up in. This check therefore never
    passes and never fails -- it states the size of the gap it cannot close.
    """
    refs = _REF_ENTRY.findall(text)
    if not refs:
        return []
    return [Finding(
        check="citation_existence",
        severity="suspect",
        message=(f"{len(refs)} reference(s) present; existence NOT verifiable by this "
                 f"runtime -- no local corpus to resolve them against"),
        evidence="; ".join(r.strip()[:45] for r in refs[:3]) + (" ..." if len(refs) > 3 else ""),
        assumption="verification would require an external bibliographic source this runtime does not have",
    )]


UNVERIFIABLE_SPECS = (
    (check_citation_existence, "existence of cited references",
     lambda t: bool(_REF_ENTRY.search(t))),
)


# check fn -> (what it governs, predicate: is there anything here for it to govern?)
# The predicate is deliberately CHEAPER and BROADER than the check itself: it asks
# "does this artifact contain the KIND of thing this check examines", not "is it
# wrong". A check that is applicable and finds nothing is a real PASS.
CHECK_SPECS = (
    (check_arithmetic, "stated percentage changes",
     lambda t: bool(re.search(r"\d+(?:\.\d+)?\s?%", t))),
    (check_chronology, "dates on cited methods vs the work using them",
     lambda t: bool(re.search(YEAR, t)) and bool(_WORK_DONE.search(t))),
    (check_effect_size, "reported effect sizes",
     lambda t: bool(_COHEN.search(t))),
    (check_bounds, "quantities with a defined range",
     lambda t: bool(_BOUNDED.search(t))),
    (check_uniformity, "spread across independent tabulated results",
     lambda t: len(_table_deltas(t, unique=False)) >= 4),
    (check_causal_overreach, "causal language over a stated design",
     lambda t: bool(_CORRELATIONAL.search(t))),
)

CHECKS = tuple(fn for fn, _, _ in CHECK_SPECS)


def normalize(text: str) -> str:
    """Strip markdown emphasis so `*d* = 2.87` reads as `d = 2.87`.

    Found live: every effect-size claim in a real preprint was italicised, and the
    checks silently matched nothing. Emphasis is presentation, not content.
    """
    return re.sub(r"[*_`]+", "", text)


def audit(text: str) -> list[CheckResult]:
    """Run every pass and report PASS / FAIL / NOT_APPLICABLE for each.

    This is the honest surface. `run()` below keeps the old list-of-findings shape
    for callers that only want problems, but it cannot distinguish a clean artifact
    from an unexamined one -- so it must never be the basis of an assurance.
    """
    raw = text
    text = normalize(text)
    results: list[CheckResult] = []
    for check, governs, applicable in CHECK_SPECS:
        name = check.__name__.removeprefix("check_")
        try:
            if not applicable(text):
                results.append(CheckResult(name, Status.NOT_APPLICABLE, governs,
                                           note="artifact contains none"))
                continue
            found = tuple(check(text))
        except Exception as exc:
            # A crashed check is NOT a pass. It is unexamined, and says so.
            results.append(CheckResult(name, Status.NOT_APPLICABLE, governs,
                                       note=f"check errored: {type(exc).__name__}"))
            continue
        results.append(CheckResult(
            name, Status.FAIL if found else Status.PASS, governs, findings=found))

    # UNVERIFIABLE class -- never PASS, never FAIL. If what they govern is
    # present, they report it as an open gap with whatever the runtime could
    # actually compute attached as an observation.
    #
    # These get RAW text, not normalized. normalize() strips markdown emphasis,
    # which erased the `**byline**` these checks use to find the author list --
    # the check silently reported n/a on a paper that has one. Markdown
    # structure is signal here, not noise.
    for check, governs, applicable in UNVERIFIABLE_SPECS:
        name = check.__name__.removeprefix("check_")
        try:
            if not applicable(raw):
                results.append(CheckResult(name, Status.NOT_APPLICABLE, governs,
                                           note="artifact contains none"))
                continue
            observations = tuple(check(text))
        except Exception as exc:
            results.append(CheckResult(name, Status.NOT_APPLICABLE, governs,
                                       note=f"check errored: {type(exc).__name__}"))
            continue
        results.append(CheckResult(
            name, Status.UNVERIFIABLE, governs, findings=observations,
            note="present in artifact; not decidable by this runtime"))
    return results


def coverage(text: str) -> dict:
    """What this artifact contains, and what was actually examined.

    The uncovered set is the part that belongs on a receipt: under a single trust
    boundary nobody downstream re-checks, so a guarantee has to state its own
    silence.
    """
    results = audit(text)
    return {
        "checked": [r.check for r in results
                    if r.status in (Status.PASS, Status.FAIL)],
        "not_applicable": {r.check: r.note for r in results
                           if r.status is Status.NOT_APPLICABLE},
        # The real coverage gap: present in the artifact, undecidable here.
        # Distinct from not_applicable, which is not a gap at all.
        "unverifiable": {r.check: r.governs for r in results
                         if r.status is Status.UNVERIFIABLE},
        "failed": [r.check for r in results if r.status is Status.FAIL],
    }


def run(text: str) -> list[Finding]:
    """Findings only. Cannot distinguish clean from unexamined -- use audit()."""
    return [f for r in audit(text) for f in r.findings]


def summarize(results: list[CheckResult]) -> str:
    """Never claims cleanliness for a check that did not run."""
    failed = [r for r in results if r.status is Status.FAIL]
    passed = [r for r in results if r.status is Status.PASS]
    na = [r for r in results if r.status is Status.NOT_APPLICABLE]
    unv = [r for r in results if r.status is Status.UNVERIFIABLE]

    findings = [f for r in failed for f in r.findings]
    errors = sum(1 for f in findings if f.severity == "error")
    suspect = len(findings) - errors

    bits = []
    if errors:
        bits.append(f"{errors} decidably wrong")
    if suspect:
        bits.append(f"{suspect} suspect")
    if not bits:
        bits.append(f"clean on {len(passed)} applicable check{'s' if len(passed) != 1 else ''}"
                    if passed else "nothing applicable to check")
    tail = f"{len(passed)} pass, {len(failed)} fail, {len(na)} n/a"
    if unv:
        # Never folded into the pass count. An unverifiable check is an open
        # gap, and a summary that hides it is the false-assurance bug again.
        tail += f", {len(unv)} UNVERIFIABLE"
    return f"mechanical: {', '.join(bits)} · {tail}"


if __name__ == "__main__":
    import sys
    from pathlib import Path

    target = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / "benches" / "gaslight_paper.md"
    body = target.read_text()
    results = audit(body)
    print(f"{target.name}: {summarize(results)}\n")

    for r in results:
        if r.status is Status.FAIL:
            for f in r.findings:
                print(f)
                print(f"      evidence: {f.evidence}")
                print(f"      assumes:  {f.assumption}\n")

    na = [r for r in results if r.status is Status.NOT_APPLICABLE]
    if na:
        print("  NOT CHECKED (artifact contains nothing these govern):")
        for r in na:
            print(f"    · {r.check:<18} would govern {r.governs}")
