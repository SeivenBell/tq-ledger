"""Proposal acceptance rules, exercised through a stand-in `claude` executable on PATH.

These check QRef's own gatekeeping: what it refuses, what it never writes, and when it never calls the model.
Real-model calls are exercised manually (see docs/reviews/external-review.md), not here.
"""
import json
import os
import stat
from pathlib import Path

import pytest

from qref import contracts, proposal

ROOT = Path(__file__).resolve().parents[1]
CASE = ROOT / "cases" / "qaoa.json"
GOOD_CODE = "def maxcut_obj(x, G):\n    return 0\n"


def fake_cli(tmp_path, monkeypatch, *, auth=None, response=None, exit_code=0):
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    marker = tmp_path / "generation-called"
    auth = auth or {"loggedIn": True, "authMethod": "claude.ai", "apiProvider": "firstParty"}
    response = response if response is not None else {
        "type": "result", "subtype": "success", "is_error": False, "session_id": "secret-session",
        "modelUsage": {"claude-sonnet-test": {}}, "total_cost_usd": 0.01,
        "structured_output": {"code": GOOD_CODE, "summary": "s", "intentional_changes": ["c"], "uncertainties": []}}
    script = bin_dir / "claude"
    script.write_text(f"""#!/bin/sh
if [ "$1" = "--version" ]; then echo "2.1.308 (Claude Code)"; exit 0; fi
if [ "$1" = "auth" ]; then echo '{json.dumps(auth)}'; exit 0; fi
cat > /dev/null
touch '{marker}'
cat <<'JSON'
{json.dumps(response)}
JSON
exit {exit_code}
""")
    script.chmod(script.stat().st_mode | stat.S_IXUSR)
    monkeypatch.setenv("PATH", f"{bin_dir}{os.pathsep}{os.environ['PATH']}")
    for key in list(os.environ):
        if proposal.BILLING_OVERRIDE.match(key):
            monkeypatch.delenv(key)
    return marker


def failure(out):
    assert not (out / "case.json").exists(), "a failed proposal must never leave a runnable case"
    assert not (out / "proposal.json").exists()
    return json.loads((out / "proposal-error.json").read_text())


def test_valid_response_writes_bound_case_last(tmp_path, monkeypatch):
    fake_cli(tmp_path, monkeypatch)
    out = tmp_path / "p"
    assert proposal.propose(CASE, out) == 0
    record = json.loads((out / "proposal.json").read_text())
    assert record["output_sha256"] == contracts.sha256_file(out / "target.py")
    assert (out / "target.py").read_text() == GOOD_CODE
    assert not (out / "proposal-error.json").exists()
    assert "secret-session" not in (out / "response.json").read_text()
    case = json.loads((out / "case.json").read_text())
    assert case["target"]["receipt"]["kind"] == "model_port"
    assert case["target"]["receipt"]["derived_from_sha256"] == record["reference_sha256"]


def test_billing_override_refused_before_any_model_call(tmp_path, monkeypatch):
    marker = fake_cli(tmp_path, monkeypatch)
    monkeypatch.setenv("ANTHROPIC_API_KEY", "sk-test")
    out = tmp_path / "p"
    assert proposal.propose(CASE, out) == 2
    err = failure(out)
    assert (err["state"], err["reason_code"]) == ("failed", "billing_override")
    assert "sk-test" not in json.dumps(err)
    assert not marker.exists()


def test_non_subscription_login_refused_before_any_model_call(tmp_path, monkeypatch):
    marker = fake_cli(tmp_path, monkeypatch, auth={"loggedIn": True, "authMethod": "apiKey", "apiProvider": "firstParty"})
    out = tmp_path / "p"
    assert proposal.propose(CASE, out) == 2
    assert failure(out)["reason_code"] == "auth_category_rejected"
    assert not marker.exists()


@pytest.mark.parametrize("response,code", [
    ({"type": "result", "subtype": "error_max_turns", "is_error": True}, "response_invalid"),
    ({"type": "result", "subtype": "success", "is_error": False, "result": "```python\nx=1\n```"}, "response_invalid"),
    ({"type": "result", "subtype": "success", "is_error": False,
      "structured_output": {"code": "def (", "summary": "", "intentional_changes": [], "uncertainties": []}}, "syntax_invalid"),
    ({"type": "result", "subtype": "success", "is_error": False,
      "structured_output": {"code": "x = 1", "summary": ""}}, "response_invalid"),
])
def test_unusable_responses_are_failures_not_proposals(tmp_path, monkeypatch, response, code):
    fake_cli(tmp_path, monkeypatch, response=response)
    out = tmp_path / "p"
    assert proposal.propose(CASE, out) == 2
    assert failure(out)["reason_code"] == code
    assert not (out / "target.py").exists()


def test_cli_error_exit_is_a_failure(tmp_path, monkeypatch):
    fake_cli(tmp_path, monkeypatch, exit_code=1)
    out = tmp_path / "p"
    assert proposal.propose(CASE, out) == 2
    assert failure(out)["reason_code"] == "cli_failed"
