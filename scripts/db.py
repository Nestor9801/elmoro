import psycopg2
from psycopg2.extras import execute_batch
from config import PG_CONFIG


INSERT_SQL = """
INSERT INTO consumos (
    id_c, folio_c, nom_c, nom_ms_c, fecha_c, hora_c,
    fecha_a_c, hora_a_c, num_cli_c, stot_c, i_c, tot_c,
    grat_c, fac_c, nom_trm, alias_usu, abr_suc, nom_cli,
    btn_detalle, efe, tar, fact, duracion
)
VALUES (
    %(id_c)s, %(folio_c)s, %(nom_c)s, %(nom_ms_c)s, %(fecha_c)s, %(hora_c)s,
    %(fecha_a_c)s, %(hora_a_c)s, %(num_cli_c)s, %(stot_c)s, %(i_c)s, %(tot_c)s,
    %(grat_c)s, %(fac_c)s, %(nom_trm)s, %(alias_usu)s, %(abr_suc)s, %(nom_cli)s,
    %(btn_detalle)s, %(efe)s, %(tar)s, %(fact)s, %(duracion)s
)
ON CONFLICT (id_c) DO UPDATE SET
    folio_c = EXCLUDED.folio_c,
    nom_c = EXCLUDED.nom_c,
    nom_ms_c = EXCLUDED.nom_ms_c,
    fecha_c = EXCLUDED.fecha_c,
    hora_c = EXCLUDED.hora_c,
    fecha_a_c = EXCLUDED.fecha_a_c,
    hora_a_c = EXCLUDED.hora_a_c,
    num_cli_c = EXCLUDED.num_cli_c,
    stot_c = EXCLUDED.stot_c,
    i_c = EXCLUDED.i_c,
    tot_c = EXCLUDED.tot_c,
    grat_c = EXCLUDED.grat_c,
    fac_c = EXCLUDED.fac_c,
    nom_trm = EXCLUDED.nom_trm,
    alias_usu = EXCLUDED.alias_usu,
    abr_suc = EXCLUDED.abr_suc,
    nom_cli = EXCLUDED.nom_cli,
    btn_detalle = EXCLUDED.btn_detalle,
    efe = EXCLUDED.efe,
    tar = EXCLUDED.tar,
    fact = EXCLUDED.fact,
    duracion = EXCLUDED.duracion
"""


def get_connection():
    conn = psycopg2.connect(**PG_CONFIG)
    conn.set_client_encoding("LATIN1")
    print("Conexion creada:", conn)
    return conn

def normalize_record(row: dict) -> dict:
    def clean(value):
        return None if value == "" else value

    def to_int(value):
        value = clean(value)
        return int(value) if value is not None else None

    def to_float(value):
        value = clean(value)
        return float(value) if value is not None else None

    return {
        "id_c": clean(row.get("id_c")),
        "folio_c": to_int(row.get("folio_c")),
        "nom_c": clean(row.get("nom_c")),
        "nom_ms_c": clean(row.get("nom_ms_c")),
        "fecha_c": clean(row.get("fecha_c")),
        "hora_c": clean(row.get("hora_c")),
        "fecha_a_c": clean(row.get("fecha_a_c")),
        "hora_a_c": clean(row.get("hora_a_c")),
        "num_cli_c": to_int(row.get("num_cli_c")),
        "stot_c": to_float(row.get("stot_c")),
        "i_c": to_float(row.get("i_c")),
        "tot_c": to_float(row.get("tot_c")),
        "grat_c": to_float(row.get("grat_c")),
        "fac_c": to_int(row.get("fac_c")),
        "nom_trm": clean(row.get("nom_trm")),
        "alias_usu": clean(row.get("alias_usu")),
        "abr_suc": clean(row.get("abr_suc")),
        "nom_cli": clean(row.get("nom_cli")),
        "btn_detalle": clean(row.get("btn_detalle")),
        "efe": to_float(row.get("efe")),
        "tar": to_float(row.get("tar")),
        "fact": to_float(row.get("fact")),
        "duracion": clean(row.get("duracion")),
    }


def save_consumos(records: list[dict]) -> int:
    rows = [normalize_record(r) for r in records if r.get("id_c")]

    if not rows:
        return 0

    with get_connection() as conn:
        with conn.cursor() as cur:
            execute_batch(cur, INSERT_SQL, rows, page_size=500)

    return len(rows)