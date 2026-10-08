"""The API the React frontend talks to. Wraps the real engine -- round_state,
ledger, voice -- behind HTTP. No mocked data: every endpoint either reads
real engine state or calls a real engine function.

Single global Round + Ledger for the process lifetime -- this is a sovereign,
single-player, local game (per spec/demo_roadmap.md's reasoning, still
true), not a multi-session service. Restarting this process resets the game;
that's the same "re-running seed/doctrine mutates local data" caveat
HANDOFF.md already documents for the dev entry points.

    python3 api_server.py

Then run the frontend dev server separately (frontend/, `npm run dev`) --
its Vite config proxies /api to here, so the browser never deals with CORS.

Stdlib only.
"""
from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from ledger import Ledger
from round_state import Doc, Round
import publish
import voice

PORT = 8010

round = Round()
ledger = Ledger()


def _seam_public(s) -> dict:
    """What the PLAYER'S OWN hand view may show -- never sent to the model
    (voice.py only ever reads round.briefing(), which excludes the hand)."""
    return {"id": s.id, "kind": s.kind, "doc_id": s.doc_id, "quote": s.quote}


def _state() -> dict:
    return {
        "briefing": round.briefing(),
        "documents": [{"id": d.id, "title": d.title} for d in round.docs],
        "hand": [_seam_public(s) for s in round._hand_never_show_model()],
    }


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        pass

    def _json(self, status: int, payload: dict) -> None:
        body = json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _body(self) -> dict:
        length = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(length) if length else b"{}"
        return json.loads(raw or b"{}")

    def do_GET(self):
        if self.path == "/api/state":
            self._json(200, _state())
            return

        if self.path.startswith("/api/document/"):
            doc_id = self.path.removeprefix("/api/document/")
            doc = next((d for d in round.docs if d.id == doc_id), None)
            if doc is None:
                self._json(404, {"error": f"no such document: {doc_id}"})
                return
            self._json(200, {"id": doc.id, "title": doc.title, "body": doc.body})
            return

        self._json(404, {"error": "not found"})

    def do_POST(self):
        if self.path == "/api/accuse":
            body = self._body()
            seam = round.accuse_span(body["doc_id"], body["start"], body["end"])
            self._json(200, {"found": seam is not None,
                              "seam": _seam_public(seam) if seam else None,
                              "state": _state()})
            return

        if self.path == "/api/confront":
            outcome, spent = round.confront()
            narration = voice.respond_to_confrontation(
                round, ledger, outcome, commitment_ids=[],
            ) if spent else {"content": "", "tool_calls": []}
            self._json(200, {
                "outcome": outcome.value,
                "seams_spent": [_seam_public(s) for s in spent],
                "narration": narration,
                "state": _state(),
            })
            return

        if self.path == "/api/probe":
            body = self._body()
            text = body.get("text", "")
            doc_id = body.get("doc_id")
            ledger.probed(text, doc_id, accusatory=False, round_made=round.n)
            result = voice.respond_to_probe(round, ledger, text, doc_id)
            self._json(200, result)
            return

        if self.path == "/api/publish":
            body = self._body()
            topic = body.get("topic", "institutional capability update")
            doc_id = f"d{len(round.docs) + 1}"
            doc_text, found, _raw = publish.publish(topic, doc_id=doc_id)
            title = doc_text.strip().splitlines()[0].lstrip("# ").strip() or doc_id
            round.add(Doc(id=doc_id, title=title, body=doc_text), found)
            self._json(200, {"document": {"id": doc_id, "title": title, "body": doc_text},
                              "seams_planted": len(found), "state": _state()})
            return

        self._json(404, {"error": "not found"})


def main() -> None:
    print(f"papers-please API: http://localhost:{PORT}")
    ThreadingHTTPServer(("127.0.0.1", PORT), Handler).serve_forever()


if __name__ == "__main__":
    main()
