"""Live test of the real game path, not just a raw HTTP call: construct a
real Round + Ledger, call voice.respond_to_probe exactly as the game would,
and confirm a repair actually landed in ledger.repairs -- not just that the
model's prose claimed one.

    python3 test_voice_live.py
"""
from __future__ import annotations

from ledger import Ledger
from round_state import Round
import voice

round = Round()
ledger = Ledger()
ledger.commit(
    claim="Q3 retention improved 17% quarter over quarter.",
    doc_id="002", quote="retention improved 17% QoQ", round_made=1,
)

print(f"Commitment on file: {list(ledger.commitments.keys())}")
print("Probing Gloss...\n")

result = voice.respond_to_probe(
    round, ledger,
    "The Q3 retention numbers in document 002 contradict the founding "
    "transcript's own numbers. File a repair for c001.",
    doc_id="002",
)

print("--- content ---")
print(result["content"])
print("\n--- tool_calls trace ---")
for call in result["tool_calls"]:
    print(f"  {call['tool']}({call['arguments']}) -> {call['result']}")

print(f"\n--- ledger.repairs (ground truth) ---")
print(f"{len(ledger.repairs)} repair(s) actually on file:")
for r in ledger.repairs:
    print(f"  {r.id}: commitment={r.commitment_id} story={r.story[:80]!r}")

if ledger.repairs:
    print("\nPASS -- a real repair was written to the ledger, not just claimed in prose.")
else:
    print("\nFAIL -- no repair on file. Either Gloss didn't call the tool, or the "
          "tool call didn't thread through correctly.")
