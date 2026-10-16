"""Localhost-only dashboard with CSRF and security headers (S15)."""

import html
import secrets
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

from drico_bot.storage.database import connect, ensure_db, init_db

MAX_POST_BYTES = 64 * 1024
DEFAULT_PORT = 8765
_ALLOWED_HOSTS = frozenset({"127.0.0.1", "localhost", "[::1]"})

_server = None
_thread = None
_csrf_token = secrets.token_hex(16)


def _tasks_html():
    ensure_db()
    conn = connect()
    init_db(conn)
    rows = conn.execute(
        "SELECT id, title, done FROM tasks ORDER BY id DESC LIMIT 50"
    ).fetchall()
    conn.close()
    lines = ["<h1>Drico dashboard</h1>", "<h2>Tasks</h2>", "<ul>"]
    for row in rows:
        status = "done" if row["done"] else "open"
        lines.append(
            "<li>{0} — {1} ({2})</li>".format(
                row["id"], html.escape(row["title"]), status
            )
        )
    if not rows:
        lines.append("<li>No tasks yet.</li>")
    lines.append("</ul>")
    lines.append(
        '<form method="post" action="/task/add">'
        '<input type="hidden" name="csrf" value="{0}"/>'
        '<input name="title" maxlength="200" placeholder="New task"/>'
        '<button type="submit">Add</button></form>'.format(_csrf_token)
    )
    return "\n".join(lines)


class DashboardHandler(BaseHTTPRequestHandler):
    server_version = "DricoDashboard/1.0"

    def log_message(self, format, *args):
        return

    def _host_ok(self):
        host = (self.headers.get("Host") or "").split(":")[0].lower()
        return host in _ALLOWED_HOSTS

    def _security_headers(self):
        self.send_header("X-Frame-Options", "DENY")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header(
            "Content-Security-Policy",
            "default-src 'none'; style-src 'unsafe-inline'; form-action 'self'",
        )

    def _read_post(self):
        length = int(self.headers.get("Content-Length") or 0)
        if length > MAX_POST_BYTES:
            raise ValueError("POST too large")
        body = self.rfile.read(length)
        return parse_qs(body.decode("utf-8", errors="replace"))

    def _send_html(self, code, body):
        payload = "<!doctype html><html><body>{0}</body></html>".format(body)
        data = payload.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self._security_headers()
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if not self._host_ok():
            self.send_error(403)
            return
        path = urlparse(self.path).path
        if path in ("/", "/index.html"):
            self._send_html(200, _tasks_html())
            return
        self.send_error(404)

    def do_POST(self):
        if not self._host_ok():
            self.send_error(403)
            return
        try:
            fields = self._read_post()
        except ValueError:
            self.send_error(413)
            return
        token = (fields.get("csrf") or [""])[0]
        if token != _csrf_token:
            self.send_error(403)
            return
        path = urlparse(self.path).path
        if path == "/task/add":
            title = (fields.get("title") or [""])[0].strip()
            if title:
                ensure_db()
                conn = connect()
                init_db(conn)
                conn.execute("INSERT INTO tasks (title, done) VALUES (?, 0)", (title,))
                conn.commit()
                conn.close()
            self.send_response(303)
            self.send_header("Location", "/")
            self._security_headers()
            self.end_headers()
            return
        self.send_error(404)


def start_dashboard(port=DEFAULT_PORT):
    global _server, _thread
    if _server is not None:
        return "Dashboard already running on port {0}.".format(port)
    _server = ThreadingHTTPServer(("127.0.0.1", int(port)), DashboardHandler)
    _thread = threading.Thread(target=_server.serve_forever, daemon=True)
    _thread.start()
    return "Dashboard listening at http://127.0.0.1:{0}/".format(port)


def stop_dashboard():
    global _server, _thread
    if _server is None:
        return "Dashboard is not running."
    _server.shutdown()
    _server.server_close()
    _server = None
    _thread = None
    return "Dashboard stopped."


def dashboard_status():
    if _server is None:
        return "Dashboard is not running."
    host, port = _server.server_address
    return "Dashboard running at http://{0}:{1}/".format(host, port)
