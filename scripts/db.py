import psycopg2
from psycopg2.extras import execute_batch
from config import PG_CONFIG


def get_connection():
    return psycopg2.connect(**PG_CONFIG)


def get_table_columns(conn, table_name):
    sql = """
    SELECT column_name
    FROM information_schema.columns
    WHERE table_schema = 'public'
      AND table_name = %s
    ORDER BY ordinal_position
    """
    with conn.cursor() as cur:
        cur.execute(sql, (table_name,))
        return [row[0] for row in cur.fetchall()]


def clean_value(value):
    if value in ("", "0000-00-00", None):
        return None
    return value


def normalize_rows_for_table(rows, table_columns, branch_id=None):
    normalized = []

    for row in rows:
        new_row = {}

        for col in table_columns:
            if col == "branch_id":
                new_row[col] = row.get("branch_id", branch_id)
            elif col in ("loaded_at", "id"):
                continue
            else:
                new_row[col] = clean_value(row.get(col))

        normalized.append(new_row)

    return normalized


def insert_generic(table_name, rows, conflict_key=None, branch_id=None, load_mode="append_upsert"):
    if not rows:
        return 0

    with get_connection() as conn:
        table_columns = get_table_columns(conn, table_name)
        insertable_columns = [c for c in table_columns if c not in ("loaded_at", "id")]
        normalized_rows = normalize_rows_for_table(rows, insertable_columns, branch_id=branch_id)

        cols_sql = ", ".join(insertable_columns)
        vals_sql = ", ".join([f"%({c})s" for c in insertable_columns])

        if load_mode == "catalog_refresh":
            with conn.cursor() as cur:
                cur.execute(f"DELETE FROM {table_name}")

            sql = f"""
            INSERT INTO {table_name} ({cols_sql})
            VALUES ({vals_sql})
            """

        elif load_mode == "append_upsert" and conflict_key:
            update_cols = [c for c in insertable_columns if c != conflict_key]

            update_sql = ", ".join([
                f"{c} = EXCLUDED.{c}" for c in update_cols
            ])

            sql = f"""
            INSERT INTO {table_name} ({cols_sql})
            VALUES ({vals_sql})
            ON CONFLICT ({conflict_key}) DO UPDATE SET
            {update_sql}
            """

        else:
            sql = f"""
            INSERT INTO {table_name} ({cols_sql})
            VALUES ({vals_sql})
            """

        with conn.cursor() as cur:
            execute_batch(cur, sql, normalized_rows, page_size=500)

    return len(normalized_rows)

def checkpoint_success(endpoint_name, table_name, fecha):
    sql = """
    SELECT EXISTS (
        SELECT 1
        FROM etl_checkpoint
        WHERE endpoint_name = %s
          AND table_name = %s
          AND fecha = %s
          AND status = 'SUCCESS'
          AND rows_api > 0
          AND rows_db > 0
    )
    """

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (endpoint_name, table_name, fecha))
            return cur.fetchone()[0]


def checkpoint_start(endpoint_name, table_name, fecha):
    sql = """
    INSERT INTO etl_checkpoint (
        endpoint_name, table_name, fecha, status, started_at
    )
    VALUES (%s, %s, %s, 'RUNNING', NOW())
    ON CONFLICT (endpoint_name, table_name, fecha) DO UPDATE SET
        status = 'RUNNING',
        started_at = NOW(),
        finished_at = NULL,
        error_message = NULL
    """

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (endpoint_name, table_name, fecha))


def checkpoint_finish(endpoint_name, table_name, fecha, rows_api, rows_db):
    sql = """
    INSERT INTO etl_checkpoint (
        endpoint_name, table_name, fecha, status, rows_api, rows_db,
        started_at, finished_at, error_message
    )
    VALUES (%s, %s, %s, 'SUCCESS', %s, %s, NOW(), NOW(), NULL)
    ON CONFLICT (endpoint_name, table_name, fecha) DO UPDATE SET
        status = 'SUCCESS',
        rows_api = EXCLUDED.rows_api,
        rows_db = EXCLUDED.rows_db,
        finished_at = NOW(),
        error_message = NULL
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (endpoint_name, table_name, fecha, rows_api, rows_db))


def checkpoint_fail(endpoint_name, table_name, fecha, error_message):
    sql = """
    INSERT INTO etl_checkpoint (
        endpoint_name, table_name, fecha, status, error_message,
        started_at, finished_at
    )
    VALUES (%s, %s, %s, 'FAILED', %s, NOW(), NOW())
    ON CONFLICT (endpoint_name, table_name, fecha) DO UPDATE SET
        status = 'FAILED',
        finished_at = NOW(),
        error_message = EXCLUDED.error_message
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (endpoint_name, table_name, fecha, str(error_message)))