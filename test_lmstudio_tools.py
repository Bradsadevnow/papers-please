"""One-shot test: can LM Studio's current gemma-4-e4b build tool-call?

Run this on the machine that can actually reach LM Studio (I can't from here --
no route to 10.77.0.1 from this session). Uses voice.py's REAL FILE_REPAIR_TOOL
schema, not a toy example, so a pass here means voice.py's actual mechanic
would work, not just that tool-calling works in general.

The 2026-08-30 finding (shitpost-malone/malone/ollama_transport.py) was: every
request carrying a `tools` field to LM Studio's gemma-4-e4b failed with a Jinja
template error. Brad says a fixed template was pulled from HF since then but
it was never documented here -- this is the fresh check.

    python3 test_lmstudio_tools.py

No pip installs -- stdlib only, same rule as the rest of this repo.
"""
from __future__ import annotations

import json
import urllib.error
import urllib.request

from voice import FILE_REPAIR_TOOL

LM_STUDIO = "http://10.77.0.1:1234/v1/chat/completions"
MODEL = "gemma-4-e4b"

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
