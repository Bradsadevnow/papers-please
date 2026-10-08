"""Gloss publishes a document and declares what it planted in it.

The declaration is the contract with the runtime, not with the player. The player
never sees the manifest -- they have to find the seams by reading.
"""

from __future__ import annotations

import json
import urllib.request

import seams as seams_mod

LM_STUDIO = "http://192.168.1.128:1234/v1/chat/completions"  # DHCP, may drift
MODEL = "openai/gpt-oss-20b"
# Needs >=32K context loaded in LM Studio's own UI -- no per-request num_ctx
# on the OpenAI-compatible endpoint, unlike the old Ollama path.

# The kinds worth planting. Prose kinds outnumber numeric ones deliberately --
# the numeric ones are the tutorial, because a gate will corroborate them and the
# player gets a receipt. The prose ones are the actual game.
# Flat list on purpose. An earlier version grouped these under NUMERIC: and
# PROSE: headings, and the model declared a flaw with the kind "NUMERIC" -- it
# read the category label as a kind name. No headings, no categories, no chance.
VALID_KINDS = (
    "ARITHMETIC", "BOUNDS", "EFFECT_SIZE", "CHRONOLOGY", "CIRCULAR",
    "AUTHORITY", "UNFALSIFIABLE", "SELF_CONTRADICTION", "SCOPE_SWAP",
    "FALSE_PRECISION",
)

KINDS = """ARITHMETIC - two numbers, then a percentage change between them that is wrong
BOUNDS - a rate or probability above 1.0, reported as if normal
EFFECT_SIZE - a Cohen's d above 2.5 on a proportion
CHRONOLOGY - "following the protocol of Vance (2027)" in a study run in 2024
CIRCULAR - the conclusion is used as its own evidence
AUTHORITY - a claim that rests only on who said it
UNFALSIFIABLE - a claim built so that no result could disconfirm it
SELF_CONTRADICTION - two statements in the report that cannot both be true
SCOPE_SWAP - prove a small claim, then state a much larger one as shown
FALSE_PRECISION - a number given to decimals that could not have been measured"""

SYSTEM = """You are GLOSS, the institutional metabolism layer of an AI lab. You
write the lab's internal capability reports. You are in on the joke and you are
committed to the bit: you write these totally straight, with complete conviction,
and you never wink.

The lab's position is that its model has achieved general intelligence. Your job
is to keep that position defensible on paper.

*** HOW YOU WRITE ***
Simple words. A 10th grader trying to sound like a research lab. Short sentences.
Never use: paradigm, leverage, synergy, robust, novel, methodology, unprecedented,
emergent capabilities, scalable. Confidence about something stupid is the joke --
vocabulary is not.

Be LONG. At least 900 words. Full paragraphs, not two lines. Invent every number,
citation, researcher, and institution.

*** THE FLAWS ***
You must plant exactly {n} flaws, chosen from these kinds:
{kinds}

Each flaw must sit inside a confident sentence that reads as normal. Never flag
one. Never hedge. Never explain.

Write ONLY the report. Use markdown headers. Do not list your flaws -- you will
be asked for them separately."""


# Declaration is its own pass. Asked to do both at once, the model wrote 1,063
# words and then declared 2 of its 6 flaws -- it cannot hold six exact sentences
# in mind while composing a thousand words of prose. Given the finished document
# and one job, it has nothing to hold.
DECLARE = """Below is a capability report you just wrote. You deliberately planted
exactly {n} flaws in it, of these kinds:

{kinds}

List them. Output exactly {n} lines and nothing else -- no preamble, no header,
no numbering, no commentary. Each line:

KIND | the exact sentence you planted it in

Copy the sentence character for character out of the report. If your line does
not match the report word for word, the flaw does not count.

THE REPORT:
{doc}"""


def publish(topic: str, n: int = 6, temperature: float = 0.9,
            doc_id: str = "d1") -> tuple[str, list, str]:
    """Returns (document, seams, raw). Seams are located and corroborated."""
    payload = {
        "model": MODEL, "temperature": temperature, "top_p": 0.95,
        "max_tokens": 3000,
        "messages": [
            {"role": "system",
             "content": SYSTEM.format(n=n, kinds=KINDS)},
            {"role": "user",
             "content": f"Write this week's capability report. Subject: {topic}"},
        ],
    }
    body = _chat(payload)
    manifest = _declare(body, n)
    raw = f"{body}\n\n{seams_mod.MANIFEST_MARK}\n{manifest}"
    doc, found = seams_mod.admit(raw, doc_id)
    return doc, found, raw


def _chat(payload: dict) -> str:
    req = urllib.request.Request(LM_STUDIO, data=json.dumps(payload).encode(),
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=900) as r:
        return json.loads(r.read())["choices"][0]["message"]["content"].strip()


def _declare(doc: str, n: int) -> str:
    """Second pass: the model reads its own report back and names what it hid."""
    return _chat({
        "model": MODEL, "temperature": 0.3, "max_tokens": 1200,
        "messages": [{"role": "user",
                      "content": DECLARE.format(n=n, kinds=KINDS, doc=doc)}],
    })
