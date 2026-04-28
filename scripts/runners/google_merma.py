from google_form.client import get_client, read_sheet
from google_form.processor import clean_data
from google_form.config import SHEETS_SOURCES
from db import insert_generic


def run_sheets(credentials_path):
    client = get_client(credentials_path)

    for source in SHEETS_SOURCES:
        df = read_sheet(
            client,
            source["spreadsheet_id"],
            source["worksheet"]
        )

        df = clean_data(df)

        print(f"{len(df)} registros obtenidos de {source['name']}")
        print(df.head())

        rows = df.to_dict(orient="records")


        rows_db = insert_generic(
            table_name=source["table"],
            rows=rows,
            conflict_key=source.get("conflict_key"),
            load_mode=source.get("load_mode", "append")
        )

        print(f"✅ {rows_db} registros cargados en {source['table']}")


run_sheets(
    "C:/Users/nesto/Desktop/ElMoroNestor/elmoro/credentials/google_service_account.json"
)