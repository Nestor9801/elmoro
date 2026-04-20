import pandas as pd
import json


def response_to_dataframe(response_json):
    """
    Convierte la respuesta de la API a DataFrame para validación
    """
    if "MSG" not in response_json:
        raise ValueError("La respuesta no contiene 'MSG'")

    msg = response_json["MSG"]

    # Caso cuando viene como string JSON
    if isinstance(msg, str):
        msg = json.loads(msg)

    if not isinstance(msg, list):
        raise ValueError(f"'MSG' no es lista. Tipo: {type(msg)}")

    df = pd.DataFrame(msg)

    return df

def preview_dataframe(df, n=5):
    print("\n--- HEAD ---")
    print(df.head(n))

    print("\n--- INFO ---")
    print(df.info())

    print("\n--- NULLS ---")
    print(df.isnull().sum())

    print("\n--- TIPOS ---")
    print(df.dtypes)

    print("\n--- COLUMNAS ---")
    print(df.columns.tolist())