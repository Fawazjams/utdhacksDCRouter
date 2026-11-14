import json

from fastapi.testclient import TestClient

from app import agent, llm_guard
from app.agent import ScriptedLLM
from app.main import app

client = TestClient(app)
DEMO = "UPS-B battery swap, 3 hrs, vendor only Wed or Fri"


def _stream(text, ip="1.2.3.4"):
    r = client.post("/request/stream", json={"text": text}, headers={"x-real-ip": ip})
    lines = [json.loads(x) for x in r.text.splitlines() if x.strip()]
    return lines[0]["llm"], lines[-1]


def test_per_ip_limit_falls_back_to_offline_path(monkeypatch):
    monkeypatch.setattr(agent, "get_llm", lambda: ScriptedLLM([]))
    used = []
    for _ in range(llm_guard.PER_IP_LIMIT + 2):
        llm, done = _stream(DEMO)
        assert done["type"] == "done" and done["response"]["task"] is not None  # rehearsed request still works
        used.append(llm)
    assert used == [True] * llm_guard.PER_IP_LIMIT + [False, False]
    assert _stream(DEMO, ip="5.6.7.8")[0] is True  # another visitor is unaffected


def test_oversized_text_never_reaches_nemotron(monkeypatch):
    monkeypatch.setattr(agent, "get_llm", lambda: ScriptedLLM([]))
    assert _stream(DEMO + " " + "x" * llm_guard.MAX_TEXT_CHARS)[0] is False
