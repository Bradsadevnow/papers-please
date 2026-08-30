"""Deterministic metrics for a joke. Real arithmetic, meaningless subject.

THE BIT: these are genuine computations. Every number here is reproducible,
checkable, and derived from the text by a procedure -- and none of them tell
you whether the joke is funny. They sit next to the vibe meter, which is the
opposite: no procedure, no ground truth, pure self-report.

That split is the entire architecture of this project rendered as a gag. The
honest thing is labelling which is which, so nobody reads FANCY WORD INDEX as
though it means something.

One of them is not a joke: `fancy_words` measures compliance with the register
rule in the escalation prompt ("simple words only, no ooh-nice-word words").
That rule was added after measured failures -- "sulfhydryl polymerization",
"Homo Sapiens Porcina" -- so this is a real regression check wearing a stupid
hat.
"""

from __future__ import annotations

import re

_VOWELS = "aeiouy"

# Words that are long but ordinary -- do not count as showing off.
_FORGIVEN = {
    "everything", "everybody", "anything", "somebody", "another", "beautiful",
    "immediately", "actually", "probably", "definitely", "seriously",
    "understand", "remember", "different", "important", "impossible",
    "electrical", "residency", "conversation", "information", "situation",
    # ordinary 3-syllable words that showed up as false positives once the
    # escalator started producing 150-word runs instead of one-liners
    "deposit", "officer", "apartment", "manager", "family", "company",
    "customer", "yesterday", "everyone", "anybody", "whatever", "together",
}

_ESCALATORS = {
    "then", "suddenly", "now", "also", "next", "eventually", "until",
    "somehow", "apparently", "turns", "started", "keeps", "every",
}


def syllables(word: str) -> int:
    """Vowel-group heuristic. Wrong on maybe 10% of English, fine for a gag."""
    w = re.sub(r"[^a-z]", "", word.lower())
    if not w:
        return 0
    groups = re.findall(rf"[{_VOWELS}]+", w)
    n = len(groups)
    if w.endswith("e") and n > 1 and not w.endswith(("le", "ee", "ye")):
        n -= 1
    return max(1, n)


def measure(text: str) -> dict:
    """All deterministic. Same text always gives the same numbers."""
    words = re.findall(r"[A-Za-z']+", text or "")
    sentences = [s for s in re.split(r"[.!?]+", text or "") if s.strip()]
    n_words = len(words)
    n_sents = max(1, len(sentences))
    syls = [syllables(w) for w in words]
    total_syl = sum(syls)

    # words of 3+ syllables that aren't ordinary long words = showing off
    fancy = [w for w, s in zip(words, syls)
             if s >= 3 and w.lower() not in _FORGIVEN]

    # Flesch-Kincaid grade. We asked for "college sophomore at a bar" register,
    # so this is a compliance check with a straight face.
    fk = (0.39 * (n_words / n_sents) + 11.8 * (total_syl / max(1, n_words)) - 15.59
          ) if n_words else 0.0

    escal = [w for w in words if w.lower() in _ESCALATORS]

    return {
        "words": n_words,
        "sentences": n_sents,
        "avg_sentence": round(n_words / n_sents, 1),
        "syllables": total_syl,
        "grade_level": round(max(0.0, fk), 1),
        "fancy_words": len(fancy),
        "fancy_list": fancy[:4],
        "escalators": len(escal),
        "commas": (text or "").count(","),
        "specificity": len(set(w.lower() for w in words if len(w) > 3)),
    }


def verdicts(m: dict) -> list[str]:
    """Deadpan readouts. Honest arithmetic, ridiculous framing."""
    out = []
    g = m["grade_level"]
    if g <= 8:
        out.append(f"grade {g} · appropriately stupid")
    elif g <= 12:
        out.append(f"grade {g} · sophomore, as ordered")
    else:
        out.append(f"grade {g} · TOO SMART, dial it back")

    # A RATE, not a count. An absolute ceiling was right for a one-liner and
    # became noise for a run: 15 fancy words in 167 is the same register as 2 in
    # 31, and the raw count only tracked length. Measured on real runs, a healthy
    # run sits at 7-9 per 100 words; the one that broke register ("evidence,
    # iguana, illegal, extinguisher", grade 16.3) was at 19.
    rate = 100.0 * m["fancy_words"] / max(1, m["words"])
    if m["fancy_words"] == 0:
        out.append("0 fancy words · register holding")
    elif rate <= 12:
        out.append(f"{rate:.0f} fancy per 100 words · register holding")
    else:
        out.append(f"{rate:.0f} fancy per 100 words · TOO FANCY · "
                   f"{', '.join(m['fancy_list'])}")

    if m["escalators"] == 0:
        out.append("no escalation markers · suspiciously restrained")
    else:
        out.append(f"{m['escalators']} escalation marker(s)")

    # Recalibrated when the escalator moved from one line to a run (three riffs,
    # a hypothetical, a fake statistic). The old ceiling was 45 words, which was
    # right for a one-liner and now fires on every single turn -- a check that
    # always trips reports nothing.
    if m["words"] < 90:
        out.append(f"{m['words']} words · short for a run, riffs may be missing")
    elif m["words"] > 320:
        out.append(f"{m['words']} words · rambling")
    else:
        out.append(f"{m['words']} words · run length holding")
    return out
