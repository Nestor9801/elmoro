from datetime import datetime
import traceback

from auth_playwright import login_and_save_state
from api_requests import load_state, build_session_from_state, fetch_endpoint, extract_msg
from db import insert_generic
from endpoints import ENDPOINTS
from param_builders import build_axis_all, build_movimientos_payload, build_movimientos_payload_yesterday


def log(msg):
    print(f"[{datetime.now()}] {msg}")


def get_valid_session():
    try:
        state = load_state()
        return build_session_from_state(state)
    except Exception:
        log("Sesion no valida. Regenerando login...")
        login_and_save_state(headless=True)
        state = load_state()
        return build_session_from_state(state)


def process_axis_endpoint(endpoint, session):
    payload = build_axis_all()

    response_json = fetch_endpoint(endpoint["url"], payload, session)
    rows = extract_msg(response_json)

    if not rows:
        log(f"{endpoint['name']}: sin datos")
        return

    inserted = insert_generic(
        table_name=endpoint["table"],
        rows=rows,
        conflict_key=endpoint.get("conflict_key"),
        branch_id=None,
    )

    log(f"{endpoint['name']}: {inserted} registros")


def process_movimientos(endpoint, session):
    payload_s = build_movimientos_payload_yesterday("S")
    payload_e = build_movimientos_payload_yesterday("E")

    response_s = fetch_endpoint(endpoint["url"], payload_s, session)
    rows_s = extract_msg(response_s)

    response_e = fetch_endpoint(endpoint["url"], payload_e, session)
    rows_e = extract_msg(response_e)

    for row in rows_s:
        row["tipo_mov_request"] = "S"

    for row in rows_e:
        row["tipo_mov_request"] = "E"

    rows = rows_s + rows_e

    if not rows:
        log(f"{endpoint['name']}: sin datos")
        return

    inserted = insert_generic(
        table_name=endpoint["table"],
        rows=rows,
        conflict_key=None,
        branch_id=None,
    )

    log(f"{endpoint['name']}: {inserted} registros")


def main():
    log("Inicio ETL")

    try:
        session = get_valid_session()

        for endpoint in ENDPOINTS:
            log(f"Procesando: {endpoint['name']}")

            try:
                if endpoint["type"] == "axis_all":
                    process_axis_endpoint(endpoint, session)

                elif endpoint["type"] == "movimientos_all":
                    process_movimientos(endpoint, session)

                else:
                    log(f"Tipo no soportado: {endpoint['type']}")

            except Exception as e:
                log(f"ERROR en {endpoint['name']}: {e}")
                traceback.print_exc()

    except Exception as e:
        log(f"ERROR CRITICO: {e}")
        traceback.print_exc()

    log("Fin ETL")


if __name__ == "__main__":
    main()