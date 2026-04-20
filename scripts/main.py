from datetime import datetime
import pandas as pd

from api_requests import load_state, build_session_from_state, fetch_raw_response
from preview import response_to_dataframe, preview_dataframe
from db import save_consumos


def build_axis_today(sucursal_id: int) -> str:
    hoy = datetime.now().strftime("%Y-%m-%d")
    return f"{hoy}|{hoy}|{sucursal_id}"


def fetch_all_sucursales_today(session, id_start=1, id_end=20) -> pd.DataFrame:
    dfs = []

    for sucursal_id in range(id_start, id_end + 1):
        try:
            axis = build_axis_today(sucursal_id)
            raw_response = fetch_raw_response(axis, session)
            df = response_to_dataframe(raw_response)

            if df.empty:
                print(f"ID {sucursal_id}: sin datos")
                continue

            df["id_sucursal_axis"] = sucursal_id
            dfs.append(df)

            abr = df["abr_suc"].dropna().unique().tolist() if "abr_suc" in df.columns else []
            print(f"ID {sucursal_id}: {len(df)} filas | abr_suc={abr}")

        except Exception as e:
            print(f"ID {sucursal_id}: error -> {e}")

    if not dfs:
        return pd.DataFrame()

    return pd.concat(dfs, ignore_index=True)


def main():
    state = load_state()
    session = build_session_from_state(state)

    # Ajusta el rango si sospechas más sucursales
    df_all = fetch_all_sucursales_today(session, id_start=1, id_end=20)

    if df_all.empty:
        print("No se encontraron datos para hoy.")
        return

    print("\n=== PREVIEW GENERAL ===")
    preview_dataframe(df_all, n=10)

    print("\n=== SUCURSALES ENCONTRADAS ===")
    if "abr_suc" in df_all.columns and "id_sucursal_axis" in df_all.columns:
        print(
            df_all[["id_sucursal_axis", "abr_suc"]]
            .drop_duplicates()
            .sort_values(["id_sucursal_axis", "abr_suc"])
        )

    inserted = save_consumos(df_all.to_dict(orient="records"))
    print(f"\nRegistros procesados en PostgreSQL: {inserted}")


if __name__ == "__main__":
    main()