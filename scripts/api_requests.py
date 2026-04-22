import json
import requests
from config import API_USER, API_PASSWORD

STATE_FILE = "playwright_state.json"
HOME_URL = "https://eos.zetus.mx/elmoro/"


def load_state(filepath=STATE_FILE):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def build_session_from_state(state):
    session = requests.Session()

    for cookie in state.get("cookies", []):
        session.cookies.set(
            name=cookie["name"],
            value=cookie["value"],
            domain=cookie.get("domain", "eos.zetus.mx"),
            path=cookie.get("path", "/"),
        )

    return session


def fetch_endpoint(url, payload, session):
    headers = {
        "Accept": "*/*",
        "User-Agent": "Mozilla/5.0",
        "X-Requested-With": "XMLHttpRequest",
        "Referer": HOME_URL,
        "Origin": "https://eos.zetus.mx",
    }

    response = session.post(
        url,
        headers=headers,
        data=payload,
        auth=(API_USER, API_PASSWORD),
        timeout=90,
    )

    print(f"URL: {url} | PAYLOAD: {payload} | STATUS: {response.status_code}")
    response.raise_for_status()
    return response.json()


def extract_msg(response_json):
    if "MSG" not in response_json:
        raise ValueError("La respuesta no contiene 'MSG'")

    msg = response_json["MSG"]

    if isinstance(msg, str):
        msg = json.loads(msg)

    if not isinstance(msg, list):
        raise ValueError(f"'MSG' no es una lista. Tipo recibido: {type(msg)}")

    return msg