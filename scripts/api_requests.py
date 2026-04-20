import json
import requests
import pandas as pd
from config import API_USER, API_PASSWORD

STATE_FILE = "playwright_state.json"
DATA_URL = "https://eos.zetus.mx/elmoro/ventas@tabla_cuentas&axis="
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

def fetch_raw_response(axis, session):
    headers = {
        "Accept": "*/*",
        "User-Agent": "Mozilla/5.0",
        "X-Requested-With": "XMLHttpRequest",
        "Referer": HOME_URL,
        "Origin": "https://eos.zetus.mx",
    }

    response = session.post(
        DATA_URL,
        headers=headers,
        data={"axis": axis},
        auth=(API_USER, API_PASSWORD),
        timeout=60,
    )

    print(f"AXIS: {axis} | STATUS: {response.status_code}")

    response.raise_for_status()
    return response.json()

def fetch_records(axis, session):
    headers = {
        "Accept": "*/*",
        "User-Agent": "Mozilla/5.0",
        "X-Requested-With": "XMLHttpRequest",
        "Referer": HOME_URL,
        "Origin": "https://eos.zetus.mx",
    }

    response = session.post(
        DATA_URL,
        headers=headers,
        data={"axis": axis},
        auth=(API_USER, API_PASSWORD),
        timeout=60,
    )

    print("STATUS:", response.status_code)
    print("CONTENT-TYPE:", response.headers.get("Content-Type"))
    print("BODY:", response.text[:500])

    response.raise_for_status()

    data = response.json()

    if "MSG" not in data:
        raise ValueError("La respuesta no contiene 'MSG'")

    msg = data["MSG"]

    if isinstance(msg, str):
        msg = json.loads(msg)

    if not isinstance(msg, list):
        raise ValueError(f"'MSG' no es lista. Tipo recibido: {type(msg)}")

    return msg


