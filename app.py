import hashlib
import hmac
import os
import time

from flask import Flask, render_template, request, Response

app = Flask(__name__)

_USERNAME = os.environ.get("DASHBOARD_USERNAME", "biochoric")
_PASSWORD = os.environ.get("DASHBOARD_PASSWORD", "")
_AUTH_SECRET = os.environ.get("AUTH_SECRET", "dev-secret")

PORTAL_TOOLS = [
    {
        "name": "Inventory Tracker",
        "description": "Chemical and supply inventory across all lab locations",
        "url": "https://biochoric-inventory-tracker-production.up.railway.app/",
        "icon": "clipboard",
    },
    {
        "name": "Kidney Supercooling Dashboard",
        "description": "Real-time monitoring for kidney supercooling experiments",
        "url": "https://kidney-supercooling-dashboard.up.railway.app/",
        "icon": "thermometer",
    },
]


def _make_token():
    """Create an HMAC token valid for 24 hours."""
    ts = str(int(time.time()) // 86400)
    sig = hmac.new(_AUTH_SECRET.encode(), ts.encode(), hashlib.sha256).hexdigest()[:32]
    return f"{ts}.{sig}"


@app.before_request
def _check_auth():
    if not _PASSWORD:
        return None
    auth = request.authorization
    if auth and auth.username == _USERNAME and auth.password == _PASSWORD:
        return None
    return Response(
        "Unauthorized", 401,
        {"WWW-Authenticate": 'Basic realm="Biochoric Lab Toolbox"'},
    )


@app.route("/")
def index():
    token = _make_token()
    tools = []
    for t in PORTAL_TOOLS:
        sep = "&" if "?" in t["url"] else "?"
        tools.append({**t, "url": f"{t['url']}{sep}auth_token={token}"})
    return render_template("index.html", tools=tools)
