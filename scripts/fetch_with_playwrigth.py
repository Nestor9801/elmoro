import json
from pathlib import Path
from playwright.sync_api import sync_playwright
from config import API_DATA_URL

STATE_FILE = Path("playwright_state.json")


def fetch_records(axis: str) -> dict:
    if not STATE_FILE.exists():
        raise FileNotFoundError("No existe playwright_state.json. Ejecuta el login primero.")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(storage_state=str(STATE_FILE))

        response = context.request.post(
            API_DATA_URL,
            form={"axis": axis},
            headers={
                "Accept": "*/*",
                "X-Requested-With": "XMLHttpRequest",
                "Referer": "https://eos.zetus.mx/elmoro/",
                "Origin": "https://eos.zetus.mx",
            },
            timeout=60000,
        )

        print("STATUS:", response.status)
        print("CONTENT-TYPE:", response.headers.get("content-type"))

        text = response.text()
        browser.close()

        return json.loads(text)