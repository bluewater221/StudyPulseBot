import os
import requests
from dotenv import load_dotenv

load_dotenv(override=True)
API_KEY = os.getenv("GEMINI_API_KEY")

import os
import requests
import pytest

models = [
    "gemini-1.5-flash",
    "gemini-1.5-flash-001",
    "gemini-2.0-flash-exp",
    "gemini-pro",
    "gemini-1.5-pro",
]


def run_models(models_list):
    API_KEY = os.getenv("GEMINI_API_KEY", "")
    headers = {"Content-Type": "application/json"}
    data = {"contents": [{"parts": [{"text": "Hello"}]}]}
    results = []

    for m in models_list:
        url = (
            f"https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent"
            f"?key={API_KEY}"
        )
        try:
            resp = requests.post(url, headers=headers, json=data)
            results.append({"model": m, "status": resp.status_code, "text": resp.text})
        except Exception as e:
            results.append({"model": m, "exception": str(e)})

    return results


def test_models_post_called_and_success(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "testkey")
    calls = []

    class DummyResp:
        def __init__(self, status_code=200, text="ok"):
            self.status_code = status_code
            self.text = text

    def fake_post(url, headers=None, json=None):
        calls.append((url, headers, json))
        return DummyResp(200, "ok")

    monkeypatch.setattr("requests.post", fake_post)

    results = run_models(models)

    assert len(calls) == len(models)
    for (url, headers, json), r in zip(calls, results):
        assert r["status"] == 200
        assert "/v1beta/models/" in url
        assert headers == {"Content-Type": "application/json"}
        assert json == {"contents": [{"parts": [{"text": "Hello"}]}]}


def test_models_handles_exceptions(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "key2")

    def fake_post(url, headers=None, json=None):
        raise requests.exceptions.RequestException("network down")

    monkeypatch.setattr("requests.post", fake_post)

    results = run_models(models)

    assert all("exception" in r for r in results)
    assert all("network down" in r["exception"] for r in results)
