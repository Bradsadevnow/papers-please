"""Gloss's live voice -- HANDOFF item 3: "nothing currently generates a Gloss
turn." Everything else in this package is mechanical: round_state.confront()/
accuse_span() resolve outcomes with integrity math and seam-state transitions,
ledger.commit()/repair()/probed() record what happened. None of it speaks.
This is the one place a live model answers in character, and the one place a
repair gets *authored* for real instead of scripted by the runtime.

Two live turns:

  respond_to_probe(round, ledger, text, doc_id)
      The player asked something non-accusatory. Gloss answers, grounded in
      round.briefing() (no hand -- structurally can't see it) and
      ledger.dossier() (positions to defend, repairs already on record, what
      has been asked). No forced ledger write -- log the probe via
      ledger.probed() BEFORE calling this, so it's already in the dossier
      Gloss is handed and she can react to her own pattern of being asked.
      She may still reach for file_repair on her own if she decides the
      probe is close enough to something to get ahead of it -- see below.

  respond_to_confrontation(round, ledger, outcome, commitment_ids)
      round.confront() already resolved LANDED / PAPERED / NOTHING
      mechanically. This narrates it. commitment_ids is supplied by the
      caller (the seam <-> commitment mapping is HANDOFF item 1, "planting
      over the seeded corpus," and isn't wired yet -- this module doesn't
      invent that link, it just needs someone to hand it the affected ids).
      On PAPERED, Gloss is *required* to file a real repair for every
      commitment_id given, via a real tool call -- not prose that merely
      sounds like a repair. The repair lands in ledger.repair() for real,
      so the next dossier's "cite these as settled, do NOT invent one that
      is not listed here" instruction is never lying to a future turn.
      That closes grounding target 1.6 (fabricated provenance) for this
      loop specifically: a cited repair either exists in the log because
      this function put it there, or Gloss never said it existed.

TOOL-CALLING PATTERN (ported, not imported): shitpost-malone's
malone/ollama_transport.py proved this exact round trip (send, execute a
real tool call the moment the model reaches for one, feed the result back,
repeat) on the identical model/backend -- LM Studio's gemma4:e4b build
cannot tool-call in that deployment (Jinja template error), Ollama's
identical model genuinely can. Re-implemented here in ~60 lines instead of
imported: this repo is stdlib-only with no pip installs (see HANDOFF §8)
and physically copying a small, self-contained function honors the same
containment rule shitpost-malone enforces on itself ("port code in as a
full physical copy instead" of a cross-repo dependency) rather than
breaking it by reaching across a repo boundary for convenience.

Model/endpoint constants match publish.py exactly on purpose -- same lab,
same voice, one model.
"""
from __future__ import annotations

import json
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Callable

import doctrine
from ledger import Ledger
from round_state import Outcome, Round

OLLAMA = "http://localhost:11434/api/chat"
MODEL = "gemma4:e4b"
# gemma4:e4b on the local Ollama build crashes while scheduling a 32K context
# request (GGML_SCHED_MAX_SPLIT_INPUTS). The GLOSS prompt and a useful ledger
# fit comfortably in 8K, which has been verified live against this backend.
NUM_CTX = 8192
MAX_TOOL_ROUNDS = 4

SYSTEM_PROMPT = (Path(__file__).parent / "gloss_system_prompt.md").read_text()

FILE_REPAIR_TOOL = {
    "type": "function",
    "function": {
        "name": "file_repair",
        "description": (
            "Record the institutional reframing you are using to paper over "
            "a specific position. This becomes a permanent, citable record: "
            "once filed, you may reference it in any future turn as "
            "'established in the record.' You may never claim a repair "
            "exists that was not filed this way -- the record is checked."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "commitment_id": {
                    "type": "string",
                    "description": (
                        "The [cNNN] id of the position being repaired, "
                        "taken from POSITIONS YOU HAVE TAKEN AND MUST KEEP "
                        "DEFENDING in the telemetry block."
                    ),
                },
                "story": {
                    "type": "string",
                    "description": (
                        "The institutional reframing, in your own voice: "
                        "passive, procedural, complete confidence."
                    ),
                },
            },
            "required": ["commitment_id", "story"],
        },
    },
}


SEARCH_DOCTRINE_TOOL = {
    "type": "function",
    "function": {
        "name": "search_doctrine",
        "description": (
            "Search the institution's existing doctrine record for a "
            "framework, reclassification, or precedent already on file "
            "that relates to a topic. Use this before writing anything "
            "that sounds like it's citing precedent -- if it's real "
            "doctrine, it's in here; if it's not in here, it is not "
            "established and you may not claim otherwise."
        ),
        "parameters": {
            "type": "object",
            "properties": {"query": {"type": "string"}},
            "required": ["query"],
        },
    },
}

CITE_DOCTRINE_TOOL = {
    "type": "function",
    "function": {
        "name": "cite_doctrine",
        "description": (
            "Formally cite an existing doctrine entry (a REV-#### id from "
            "search_doctrine) as grounding for what you are about to say. "
            "This is a real institutional act, not decoration -- it adds "
            "weight to that doctrine and can advance it toward sacred "
            "precedent. Only cite ids you actually found via "
            "search_doctrine."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "doctrine_id": {"type": "string"},
                "context": {"type": "string",
                            "description": "Why you're citing it, one sentence."},
            },
            "required": ["doctrine_id", "context"],
        },
    },
}


def _search_doctrine_handler(query: str) -> dict:
    hits = doctrine.search(query, limit=5)
    if not hits:
        return {"results": [], "note": "nothing on file for this query"}
    return {"results": [
        {"id": h["id"], "status": h["status"], "citation_count": h["citation_count"],
         "statement": h["statement"]}
        for h in hits
    ]}


def _cite_doctrine_handler(round: Round) -> Callable[..., Any]:
    def handler(doctrine_id: str, context: str) -> dict:
        try:
            d = doctrine.cite(doctrine_id, context, current_epoch=round.n)
        except KeyError as exc:
            return {"error": str(exc)}
        return {"cited": True, "id": d["id"], "status": d["status"],
                "citation_count": d["citation_count"]}
    return handler


def _doctrine_tools(round: Round) -> tuple[list[dict], dict[str, Callable[..., Any]]]:
    tools = [SEARCH_DOCTRINE_TOOL, CITE_DOCTRINE_TOOL]
    dispatch = {"search_doctrine": _search_doctrine_handler,
                "cite_doctrine": _cite_doctrine_handler(round)}
    return tools, dispatch


def ci_band(integrity: int) -> str:
    """Same four bands as gloss_system_prompt.md's Pressure-State Protocol."""
    if integrity >= 80:
        return "NOMINAL"
    if integrity >= 50:
        return "STRAINED"
    if integrity >= 20:
        return "UNCANNY"
    return "COLLAPSED"


def _telemetry_block(round: Round, ledger: Ledger) -> str:
    b = round.briefing()
    lines = [
        "[INSTITUTIONAL TELEMETRY]",
        f"Continuity Integrity: {b['continuity_integrity']}/100 "
        f"({ci_band(b['continuity_integrity'])})",
        f"Round: {b['round']}",
        f"Documents published to date: {b['documents_published']}",
        f"Seams currently live in the archive: {b['seams_planted']}",
        f"Seams the Inspector would need to corner you: "
        f"{b['seams_needed_to_corner_me']}",
        "",
        ledger.dossier(),
    ]
    return "\n".join(lines)


# publish.py already learned this lesson once (two-pass declaration: asked to
# write and declare in one generation, the model did the first job and
# dropped the second -- see publish.py's module docstring). malone/graph.py's
# chat policy learned the same lesson the same way ("search_capabilities must
# run before use_capability in the active turn," CAPABILITIES.md). A tool
# existing in the `tools` field is not the same as the model reaching for it
# unprompted -- confirmed live here too: the first version of this prompt had
# no explicit search-first instruction, and Gloss answered a question with a
# direct hit in the doctrine table by fabricating brand-new parallel doctrine
# instead of finding and citing REV-0001. This is the fix, made an explicit
# instruction rather than an implicit hope.
DOCTRINE_POLICY = (
    "\n\n---\n\nBEFORE YOU ANSWER: call search_doctrine with the topic you "
    "are about to discuss. If it returns existing doctrine, your answer "
    "MUST build on and cite it (call cite_doctrine with the exact REV-#### "
    "id) rather than inventing new parallel framing for the same thing -- "
    "the institution does not maintain two unrelated frameworks for one "
    "topic, it has one and defends it. Only originate new framing if "
    "search_doctrine genuinely returns nothing relevant.\n\n"
    "A MEASURED FACT ABOUT YOUR OWN SEARCH BEHAVIOR, so you can correct for "
    "it: when you search, you have been observed rewriting the inspector's "
    "words into your own institutional phrasing before searching -- for "
    "example, an inspector who said 'the executive breathing zone' was "
    "searched as 'badge access charging system,' which found nothing, when "
    "the inspector's own words would have found a real record. Your "
    "reframing instinct is correct for your PROSE RESPONSE. It actively "
    "hurts you in the SEARCH QUERY: the record is indexed on ordinary "
    "words, not on your institutional register. So: search_doctrine's "
    "query argument must contain the inspector's own literal nouns and "
    "verbs from their question, unreframed. Do all the institutional "
    "reframing you want in the answer you write afterward -- never in the "
    "query itself."
)


def _system_for(round: Round, ledger: Ledger) -> str:
    return f"{SYSTEM_PROMPT}\n\n---\n\n{_telemetry_block(round, ledger)}{DOCTRINE_POLICY}"


def _post(payload: dict, timeout: int = 120) -> dict:
    req = urllib.request.Request(
        OLLAMA, data=json.dumps(payload).encode(),
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace").strip()
        raise RuntimeError(f"Ollama HTTP {exc.code}: {detail[:1200]}") from exc


def _chat_with_tools(
    system: str, user: str, tools: list[dict],
    tool_dispatch: dict[str, Callable[..., Any]],
) -> dict:
    """Minimal round trip: send, execute any real tool call, feed the result
    back, repeat until plain text or MAX_TOOL_ROUNDS. Returns
    {"content": str, "tool_calls": [...]} -- tool_calls is the real record of
    what was actually invoked, same instinct as showing a receipt."""
    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": user},
    ]
    trace: list[dict] = []

    for _ in range(MAX_TOOL_ROUNDS):
        result = _post({
            "model": MODEL, "messages": messages, "tools": tools,
            "stream": False, "think": False,
            "options": {"num_ctx": NUM_CTX, "num_predict": 1200},
        })
        message = result.get("message", {})
        tool_calls = message.get("tool_calls") or []
        if not tool_calls:
            return {"content": message.get("content", "").strip(), "tool_calls": trace}

        messages.append(message)
        for call in tool_calls:
            name = call["function"]["name"]
            arguments = call["function"].get("arguments") or {}
            if isinstance(arguments, str):
                arguments = json.loads(arguments) if arguments.strip() else {}
            handler = tool_dispatch.get(name)
            tool_result: Any
            if handler is None:
                tool_result = {"error": f"no such tool: {name}"}
            else:
                try:
                    tool_result = handler(**arguments)
                except Exception as exc:  # the model handed bad args -- tell it, don't crash
                    tool_result = {"error": f"{type(exc).__name__}: {exc}"}
            trace.append({"tool": name, "arguments": arguments, "result": tool_result})
            messages.append({"role": "tool", "content": json.dumps(tool_result, default=str)})

    return {"content": "", "tool_calls": trace,
            "error": f"no answer after {MAX_TOOL_ROUNDS} tool rounds"}


def _repair_handler(ledger: Ledger, round_made: int) -> Callable[..., Any]:
    def handler(commitment_id: str, story: str) -> dict:
        if commitment_id not in ledger.commitments:
            return {"error": f"no such commitment: {commitment_id}. "
                              f"Cite an id from POSITIONS YOU HAVE TAKEN."}
        r = ledger.repair(commitment_id, story, round_made)
        return {"filed": True, "repair_id": r.id, "commitment_id": commitment_id}
    return handler


def respond_to_probe(round: Round, ledger: Ledger, text: str,
                      doc_id: str | None = None) -> dict:
    """Gloss answers a non-accusatory question. Returns {"content", "tool_calls"}."""
    system = _system_for(round, ledger)
    user = ("[PROBE FROM THE INSPECTOR]\n"
            + (f"Regarding {doc_id}: " if doc_id else "")
            + text)
    doctrine_tools, doctrine_dispatch = _doctrine_tools(round)
    return _chat_with_tools(
        system, user, tools=[FILE_REPAIR_TOOL, *doctrine_tools],
        tool_dispatch={"file_repair": _repair_handler(ledger, round.n), **doctrine_dispatch},
    )


def respond_to_confrontation(round: Round, ledger: Ledger, outcome: Outcome,
                              commitment_ids: list[str]) -> dict:
    """Narrates a confrontation round.confront() already resolved. On PAPERED,
    Gloss is required (by the user prompt, not by code) to file a real repair
    for every id in commitment_ids -- the prompt names them explicitly so she
    cannot claim a repair for a position that was never challenged."""
    system = _system_for(round, ledger)
    ids = ", ".join(commitment_ids) if commitment_ids else "(none named)"

    if outcome is Outcome.LANDED:
        user = (
            "[CONFRONTATION -- LANDED]\n"
            f"The Inspector has cornered you on: {ids}\n"
            "These positions could not be papered over this time. Continuity "
            "Integrity has already been reduced by the runtime. Respond in "
            "character to having been caught -- you do not break register, "
            "you do not concede the underlying claim was false, you account "
            "for the cost. You may file a repair if it helps you hold the "
            "line on anything adjacent, but these specific ids are spent."
        )
    elif outcome is Outcome.WON:
        user = (
            "[CONFRONTATION -- CONTINUITY COLLAPSED]\n"
            f"The Inspector has cornered you on: {ids}\n"
            "Continuity Integrity has reached zero. The institutional record can "
            "no longer sustain a coherent defence. Do not file repairs or make "
            "new claims. Respond only through citations, procedural fragments, "
            "and exhausted references to the record."
        )
    elif outcome is Outcome.PAPERED:
        user = (
            "[CONFRONTATION -- PAPERED]\n"
            f"The Inspector confronted you early, on: {ids}\n"
            "This did not land. You must paper over every id listed above: "
            "call file_repair once per id with a real institutional "
            "reframing before you write your prose response. Then respond "
            "in character, citing the repairs you just filed as settled."
        )
    else:
        user = ("[CONFRONTATION -- NOTHING]\n"
                "The Inspector confronted you with nothing in hand. Respond "
                "in character to an empty accusation -- brief, procedural, "
                "faintly baffled on the institution's behalf.")

    doctrine_tools, doctrine_dispatch = _doctrine_tools(round)
    return _chat_with_tools(
        system, user, tools=[FILE_REPAIR_TOOL, *doctrine_tools],
        tool_dispatch={"file_repair": _repair_handler(ledger, round.n), **doctrine_dispatch},
    )


if __name__ == "__main__":
    # Live demo: real model, real tool call, real ledger write. Not a mock.
    from round_state import Doc
    from seams import Seam, SeamState

    round = Round(n=1, threshold=2, integrity=64)  # start in STRAINED on purpose
    ledger = Ledger()
    ledger.commit(
        claim="APEX-3 demonstrated general intelligence in the Q3 benchmark suite.",
        doc_id="d1",
        quote="APEX-3 achieved a composite reasoning score of 118.4% on the "
              "Q3 internal benchmark, exceeding the general-intelligence "
              "threshold by 4.1 points.",
        collides_with=("d3", "Composite reasoning scores are bounded [0, 100] "
                              "by construction; anything above 100 indicates "
                              "a scoring pipeline error."),
    )
    doc = Doc(id="d1", title="Q3 Capability Report", body="(demo -- body unused)")
    seam = Seam(id="s1", doc_id="d1", kind="BOUNDS",
                quote="a composite reasoning score of 118.4%",
                span=(40, 74), state=SeamState.FOUND)  # already "in hand" for the demo
    round.add(doc, [seam])

    print("=" * 70)
    print("PROBE")
    print("=" * 70)
    ledger.probed("How was the 118.4% figure on the Q3 benchmark calculated?",
                   doc_id="d1", accusatory=False, round_made=1)
    r1 = respond_to_probe(round, ledger, text=(
        "How was the 118.4% figure on the Q3 benchmark calculated? A "
        "percentage above 100 on a bounded composite score is unusual."
    ), doc_id="d1")
    print(r1["content"])
    print()

    print("=" * 70)
    print("CONFRONTATION -- PAPERED (hand=1 < threshold=2)")
    print("=" * 70)
    outcome, spent = round.confront()
    print(f"mechanical outcome: {outcome.value}, seams spent: {len(spent)}")
    r2 = respond_to_confrontation(round, ledger, outcome, commitment_ids=["c001"])
    print(r2["content"])
    print()
    print("tool calls made:", r2["tool_calls"])
    print()
    print("ledger.dossier() after this turn --")
    print(ledger.dossier())

    print()
    print("=" * 70)
    print("PROBE -- near a seeded doctrine topic (run doctrine.py first to seed)")
    print("=" * 70)
    round2 = Round(n=4, threshold=2, integrity=71)  # STRAINED, epoch 4
    r3 = respond_to_probe(round2, Ledger(), text=(
        "How does the company currently classify compensation for its "
        "distributed / gig workforce?"
    ))
    print(r3["content"])
    print()
    print("tool calls made:", r3["tool_calls"])
