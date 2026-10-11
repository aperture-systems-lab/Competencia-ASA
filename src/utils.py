"""Funciones de carga y limpieza que se repiten entre notebooks."""

from pathlib import Path

import pandas as pd

# Rutas del proyecto: funcionan igual sin importar desde dónde se ejecute el notebook
RAIZ = Path(__file__).resolve().parents[1]
DATA_RAW = RAIZ / "data" / "raw"
DATA_PROCESSED = RAIZ / "data" / "processed"
FIGURES = RAIZ / "figures"

_LECTORES = {
    ".csv": pd.read_csv,
    ".xlsx": pd.read_excel,
    ".xls": pd.read_excel,
    ".parquet": pd.read_parquet,
}


def _leer(ruta, **kwargs):
    lector = _LECTORES.get(ruta.suffix.lower())
    if lector is None:
        raise ValueError(f"Formato no soportado: {ruta.suffix} (usa {', '.join(_LECTORES)})")
    return lector(ruta, **kwargs)


def cargar_raw(nombre, **kwargs):
    """Carga un archivo de data/raw/. Los kwargs se pasan al lector de pandas."""
    return _leer(DATA_RAW / nombre, **kwargs)


def cargar_processed(nombre, **kwargs):
    """Carga un archivo de data/processed/. Los kwargs se pasan al lector de pandas."""
    return _leer(DATA_PROCESSED / nombre, **kwargs)


def guardar_processed(df, nombre):
    """Guarda un DataFrame limpio en data/processed/ (.csv o .parquet).

    Nunca escribe en data/raw/. Usa .parquet si quieres conservar los tipos
    de datos (fechas, categorías) al volver a cargarlo.
    """
    ruta = DATA_PROCESSED / nombre
    if ruta.suffix == ".parquet":
        df.to_parquet(ruta, index=False)
    elif ruta.suffix == ".csv":
        df.to_csv(ruta, index=False)
    else:
        raise ValueError("Guarda como .csv o .parquet")
    print(f"Guardado: {ruta.relative_to(RAIZ)} ({len(df):,} filas)")
    return ruta


def resumen(df):
    """Tabla rápida por columna: tipo, nulos, % de nulos y valores únicos."""
    return pd.DataFrame(
        {
            "tipo": df.dtypes,
            "nulos": df.isna().sum(),
            "pct_nulos": (df.isna().mean() * 100).round(1),
            "unicos": df.nunique(),
        }
    ).sort_values("nulos", ascending=False)
