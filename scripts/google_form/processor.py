import pandas as pd
import re
from datetime import datetime


COLUMN_MAP = {
    "Marca temporal": "marca_temporal",
    "¿Cuál es la fecha y hora de la detección de la merma?": "fecha_deteccion",
    "Ubicación/Sucursal donde ocurrió la merma": "ubicacion_sucursal",
    "Producto afectado por la merma": "producto",
    "Cantidad o Unidad de Merma": "cantidad_unidad_merma",
    "¿El ítem reportado clasifica como 'Merma' o 'Desperdicio'?": "clasificacion",
    "Causa principal de la merma/desperdicio": "causa_principal",
    "Persona que registra": "persona_registra",
}


def snake_case(text: str) -> str:
    text = text.strip().lower()
    text = text.replace("á", "a").replace("é", "e").replace("í", "i")
    text = text.replace("ó", "o").replace("ú", "u").replace("ñ", "n")
    text = re.sub(r"[^a-z0-9]+", "_", text)
    text = re.sub(r"_+", "_", text)
    return text.strip("_")


def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df = df.rename(columns=COLUMN_MAP)
    df.columns = [snake_case(col) for col in df.columns]
    return df


def clean_text_columns(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    for col in df.select_dtypes(include="object").columns:
        df[col] = (
            df[col]
            .astype(str)
            .str.strip()
            .replace({"": None, "nan": None, "None": None})
        )

    return df


def cast_types(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    date_cols = [
        "marca_temporal",
        "fecha_deteccion",
    ]

    for col in date_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(
                df[col],
                errors="coerce",
                dayfirst=True
            )

    return df


def clean_categories(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    if "clasificacion" in df.columns:
        df["clasificacion"] = (
            df["clasificacion"]
            .str.strip()
            .str.upper()
        )

    if "ubicacion_sucursal" in df.columns:
        df["ubicacion_sucursal"] = df["ubicacion_sucursal"].str.upper()

    if "producto" in df.columns:
        df["producto"] = df["producto"].str.upper()

    return df


def add_metadata(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["source"] = "google_forms_merma"
    df["loaded_at"] = datetime.now()
    return df


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.dropna(how="all")
    df = normalize_columns(df)
    df = clean_text_columns(df)
    df = cast_types(df)
    df = clean_categories(df)
    df = add_metadata(df)

    return df