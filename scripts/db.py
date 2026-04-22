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
    if value in ("", "0000-00-00"):
        return None
    return value


def normalize_rows_for_table(rows, table_columns, branch_id=None):
    normalized = []

    for row in rows:
        new_row = {}

        for col in table_columns:
            if col == "branch_id":
                new_row[col] = branch_id
            elif col == "loaded_at":
                continue
            else:
                new_row[col] = clean_value(row.get(col))

        normalized.append(new_row)

    return normalized


def insert_generic(table_name, rows, conflict_key=None, branch_id=None):
    if not rows:
        return 0

    with get_connection() as conn:
        table_columns = get_table_columns(conn, table_name)

        insertable_columns = [c for c in table_columns if c not in ("loaded_at", "id")]
        normalized_rows = normalize_rows_for_table(rows, insertable_columns, branch_id=branch_id)

        cols_sql = ", ".join(insertable_columns)
        vals_sql = ", ".join([f"%({c})s" for c in insertable_columns])

        if conflict_key:
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