from datetime import datetime
import traceback

from api_requests import fetch_endpoint, extract_msg
from db import insert_generic
from endpoints import ENDPOINTS_CATALOGOS
from param_builders import (
    build_catalogo_categorias_payload,
    build_catalogo_articulos_detalle_payload,
)


def log(msg):
    print(f"[{datetime.now()}] {msg}")


def process_catalogo_categorias(endpoint, session):
    rows_all = []

    for stat_fltr in ["1", "0"]:
        payload = build_catalogo_categorias_payload(stat_fltr)

        response_json = fetch_endpoint(endpoint["url"], payload, session)
        rows = extract_msg(response_json)

        rows_all.extend(rows)
        log(f"{endpoint['name']} | stat {stat_fltr} | API rows: {len(rows)}")

    if not rows_all:
        log(f"{endpoint['name']}: sin datos")
        return

    inserted = insert_generic(
        table_name=endpoint["table"],
        rows=rows_all,
        conflict_key=endpoint.get("conflict_key"),
        load_mode=endpoint.get("load_mode", "catalog_refresh"),
    )

    log(f"{endpoint['name']} | DB rows: {inserted}")


def process_catalogo_articulos_detalle(endpoint, session):
    rows_all = []

    for stat_fltr in ["1", "0"]:
        payload = build_catalogo_articulos_detalle_payload(stat_fltr)

        response_json = fetch_endpoint(endpoint["url"], payload, session)
        rows = extract_msg(response_json)

        rows_all.extend(rows)
        log(f"{endpoint['name']} | stat {stat_fltr} | API rows: {len(rows)}")

    if not rows_all:
        log(f"{endpoint['name']}: sin datos")
        return

    inserted = insert_generic(
        table_name=endpoint["table"],
        rows=rows_all,
        conflict_key=endpoint.get("conflict_key"),
        load_mode=endpoint.get("load_mode", "catalog_refresh"),
    )

    log(f"{endpoint['name']} | DB rows: {inserted}")


def run_catalogos(session):
    log("Inicio catalogos")

    for endpoint in ENDPOINTS_CATALOGOS:
        try:
            endpoint_type = endpoint.get("type")
            log(f"Procesando catalogo: {endpoint['name']}")

            if endpoint_type == "catalogo_categorias":
                process_catalogo_categorias(endpoint, session)

            elif endpoint_type == "catalogo_articulos_detalle":
                process_catalogo_articulos_detalle(endpoint, session)

            else:
                log(f"Tipo catalogo no soportado: {endpoint_type}")

        except Exception as e:
            log(f"ERROR catalogo {endpoint['name']}: {e}")
            traceback.print_exc()

    log("Fin catalogos")