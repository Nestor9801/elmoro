from datetime import datetime
import traceback

from api_requests import fetch_endpoint, extract_msg
from db import insert_generic
from endpoints import ENDPOINTS_TRANSACCIONALES
from param_builders import (
    build_tabla_cuentas_payload_for_day,
    build_movimientos_payload,
)
from date_ranges import iter_days

from db import (
    insert_generic,
    checkpoint_success,
    checkpoint_start,
    checkpoint_finish,
    checkpoint_fail,
)


def log(msg):
    print(f"[{datetime.now()}] {msg}")


def log(msg):
    print(f"[{datetime.now()}] {msg}")


def process_tabla_cuentas_range(endpoint, session, fecha_inicio, fecha_fin):
    total_api = 0
    total_db = 0

    for fecha in iter_days(fecha_inicio, fecha_fin):
        endpoint_name = endpoint["name"]

        try:
            if checkpoint_success(endpoint_name, fecha):
                log(f"{endpoint_name} | fecha {fecha} | ya procesada, se omite")
                continue

            checkpoint_start(endpoint_name, fecha)

            payload = build_tabla_cuentas_payload_for_day(fecha)
            response_json = fetch_endpoint(endpoint["url"], payload, session)
            rows = extract_msg(response_json)

            rows_api = len(rows)
            total_api += rows_api

            log(f"{endpoint_name} | fecha {fecha} | API rows: {rows_api}")

            if rows_api == 0:
                raise Exception(
                    f"No se recibieron registros de API para {endpoint_name} en fecha {fecha}"
                )

            rows_db = insert_generic(
                table_name=endpoint["table"],
                rows=rows,
                conflict_key=endpoint.get("conflict_key"),
                load_mode=endpoint.get("load_mode", "append_upsert"),
            )

            total_db += rows_db

            if rows_db == 0:
                raise Exception(
                    f"API devolvio {rows_api} registros pero DB inserto 0 para {endpoint_name} en fecha {fecha}"
                )

            checkpoint_finish(endpoint_name, fecha, rows_api, rows_db)

            log(f"{endpoint_name} | fecha {fecha} | DB rows: {rows_db}")

        except Exception as e:
            checkpoint_fail(endpoint_name, fecha, e)
            log(f"ERROR {endpoint_name} | fecha {fecha}: {e}")
            traceback.print_exc()

    log(f"{endpoint['name']} | TOTAL API: {total_api}")
    log(f"{endpoint['name']} | TOTAL DB: {total_db}")


def process_movimientos_range(endpoint, session, fecha_inicio, fecha_fin):
    total_api = 0
    total_db = 0

    for fecha in iter_days(fecha_inicio, fecha_fin):
        rows_all = []

        for tipo_mov in ["S", "E"]:
            try:
                payload = build_movimientos_payload(
                    fecha_ini=fecha,
                    fecha_fin=fecha,
                    tipo_mov=tipo_mov,
                    busc_fltr="",
                )

                response_json = fetch_endpoint(endpoint["url"], payload, session)
                rows = extract_msg(response_json)

                for row in rows:
                    row["tipo_mov_request"] = tipo_mov

                rows_all.extend(rows)
                total_api += len(rows)

                log(f"{endpoint['name']} | fecha {fecha} | tipo {tipo_mov} | API rows: {len(rows)}")

            except Exception as e:
                log(f"ERROR {endpoint['name']} | fecha {fecha} | tipo {tipo_mov}: {e}")
                traceback.print_exc()

        if not rows_all:
            continue

        try:
            inserted = insert_generic(
                table_name=endpoint["table"],
                rows=rows_all,
                conflict_key=endpoint.get("conflict_key"),
                load_mode=endpoint.get("load_mode", "append_upsert"),
            )

            total_db += inserted
            log(f"{endpoint['name']} | fecha {fecha} | DB rows: {inserted}")

        except Exception as e:
            log(f"ERROR insertando {endpoint['name']} | fecha {fecha}: {e}")
            traceback.print_exc()

    log(f"{endpoint['name']} | TOTAL API: {total_api}")
    log(f"{endpoint['name']} | TOTAL DB: {total_db}")


def run_transaccionales(session, fecha_inicio, fecha_fin):
    log(f"Inicio transaccionales | {fecha_inicio} a {fecha_fin}")

    for endpoint in ENDPOINTS_TRANSACCIONALES:
        endpoint_type = endpoint.get("type")

        log(f"Procesando transaccional: {endpoint['name']}")

        if endpoint_type == "tabla_cuentas_range":
            process_tabla_cuentas_range(endpoint, session, fecha_inicio, fecha_fin)

        elif endpoint_type == "movimientos_range":
            process_movimientos_range(endpoint, session, fecha_inicio, fecha_fin)

        else:
            log(f"Tipo transaccional no soportado: {endpoint_type}")
