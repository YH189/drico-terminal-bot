import urllib.error
import urllib.request

from drico_bot.dashboard.server import start_dashboard, stop_dashboard


def test_dashboard_localhost_only(tmp_path, monkeypatch):
    monkeypatch.setenv("DRICO_HOME", str(tmp_path))
    message = start_dashboard(port=18765)
    assert "127.0.0.1" in message
    try:
        with urllib.request.urlopen("http://127.0.0.1:18765/") as response:
            body = response.read().decode("utf-8")
        assert "Drico dashboard" in body
        assert "Tasks" in body
        req = urllib.request.Request(
            "http://127.0.0.1:18765/",
            headers={"Host": "evil.example"},
            method="GET",
        )
        try:
            urllib.request.urlopen(req, timeout=2)
            assert False, "expected forbidden host"
        except urllib.error.HTTPError as exc:
            assert exc.code == 403
    finally:
        stop_dashboard()
