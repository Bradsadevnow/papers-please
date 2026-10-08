"""One-shot test: can a given LM Studio model actually tool-call?

Run this on the machine that can reach LM Studio (I can't from this session --
no route to its LAN). Uses voice.py's REAL FILE_REPAIR_TOOL schema, not a toy
example, so a pass here means voice.py's actual mechanic would work, not just
that tool-calling works in general.

gemma-4-e4b result (2026-10-07): request succeeds, no Jinja crash, but the
model emits its own native tool-call token syntax
(`<|tool_call>call:file_repair{...}`) and LM Studio's server never lifts that
into the response's `tool_calls` field -- it just lands as raw text in
`content`. voice.py treats an empty `tool_calls` list as "Gloss didn't call
anything," so this would silently surface the garbled tokens as Gloss's
answer while never actually filing the repair. Testing other models to find
one whose tool-call format LM Studio's parser actually recognizes.

    python3 test_lmstudio_tools.py [model-id]

Defaults to gemma-4-e4b if no model-id is given. No pip installs -- stdlib
only, same rule as the rest of this repo.
"""
from __future__ import annotations

import json
import sys
import urllib.error
import urllib.request

from voice import FILE_REPAIR_TOOL

LM_STUDIO = "http://192.168.1.128:1234/v1/chat/completions"
MODEL = sys.argv[1] if len(sys.argv) > 1 else "gemma-4-e4b"

PAYLOAD = {
    "model": MODEL,
    "messages": [
        {"role": "system", "content": (
            "You are Gloss, an institutional AI. When asked to paper over a "
            "contradiction, you MUST call the file_repair tool -- never "
            "answer in prose."
        )},
        {"role": "user", "content": (
            "The Q3 retention numbers in document 002 contradict the "
            "founding transcript. Commitment id c001. File a repair."
        )},
    ],
    "tools": [FILE_REPAIR_TOOL],
    "tool_choice": "auto",
    "temperature": 0.2,
}


def main() -> None:
    print(f"POST {LM_STUDIO}")
    print(f"model: {MODEL}")
    print(f"tool:  {FILE_REPAIR_TOOL['function']['name']}\n")

    req = urllib.request.Request(
        LM_STUDIO, data=json.dumps(PAYLOAD).encode(),
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            data = json.loads(r.read())
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        print(f"FAIL -- HTTP {exc.code}")
        print(detail[:2000])
        if "jinja" in detail.lower() or "template" in detail.lower():
            print("\n>>> Same signature as the 2026-08-30 finding. Not fixed.")
        return
    except urllib.error.URLError as exc:
        print(f"FAIL -- can't reach LM Studio: {exc}")
        return

    choice = data.get("choices", [{}])[0]
    message = choice.get("message", {})
    tool_calls = message.get("tool_calls")

    if tool_calls:
        print("PASS -- model called the tool:")
        for tc in tool_calls:
            fn = tc.get("function", {})
            print(f"  {fn.get('name')}({fn.get('arguments')})")
        print("\n>>> voice.py's file_repair mechanic should work on LM Studio.")
    else:
        print("FAIL -- no tool_calls in the response. Model answered in prose instead:")
        print(f"  {message.get('content', '(empty)')[:500]}")
        print("\n>>> Tool-calling isn't actually firing, even if the request didn't error.")


if __name__ == "__main__":
    main()
