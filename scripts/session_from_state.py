import json
from pathlib import Path
import requests

STATE_FILE = Path("playwright_state.json")


def build_requests_session_from_state() -> requests.Session:
    if not STATE_FILE.exists():
        raise FileNotFoundError("No existe playwright_state.json. Ejecuta el login primero.")

    state = json.loads(STATE_FILE.read_text(encoding="utf-8"))
    session = requests.Session()

    for cookie in state.get("cookies", []):
        session.cookies.set(
            name=cookie["name"],
            value=cookie["value"],
            domain=cookie.get("domain"),
            path=cookie.get("path", "/"),
        )

    return session