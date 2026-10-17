"""Descarga los puntajes PISA (medias, percentiles y niveles de competencia, total y por sexo)
del Banco Mundial y los guarda en data/raw/."""

from pathlib import Path

import pandas as pd
import wbgapi as wb

RAIZ = Path(__file__).resolve().parents[1]
DATA_RAW = RAIZ / "data" / "raw"

# Materia -> (prefijo del código del Banco Mundial, nombre de columna)
MATERIAS = {
    "MAT": "Math",
    "REA": "Reading",
    "SCI": "Science",
}

# Sufijo del código del Banco Mundial -> sufijo de la columna (total, mujeres, hombres)
SEXOS = {"": "Total", ".FE": "Female", ".MA": "Male"}

PERCENTILES = ["P05", "P10", "P25", "P50", "P75", "P90", "P95"]

# Niveles de competencia (% de estudiantes de 15 años) tal como los publica el Banco Mundial.
# Código del nivel -> etiqueta de columna. Cambian entre materias y entre ediciones de PISA.
NIVELES = {
    "MAT": {"0": "Below1", "1": "L1", "2": "L2", "3": "L3", "4": "L4", "5": "L5", "6": "L6"},
    "REA": {
        "0.B1C": "Below1C", "1C": "L1C", "1B": "L1B", "1A": "L1A",
        "2": "L2", "3": "L3", "4": "L4", "5": "L5", "6": "L6",
    },
    "SCI": {
        "0": "Below1B", "1B": "L1B", "1A": "L1A",
        "2": "L2", "3": "L3", "4": "L4", "5": "L5", "6": "L6",
    },
}


def construir_indicadores():
    """Diccionario {código Banco Mundial: nombre de columna} con todas las series a descargar."""
    indicadores = {}
    for cod, nombre in MATERIAS.items():
        # Medias: total y por sexo
        for suf_cod, suf_nom in SEXOS.items():
            indicadores[f"LO.PISA.{cod}{suf_cod}"] = f"PISA_{nombre}_{suf_nom}"
        # Percentiles de la distribución (solo total)
        for p in PERCENTILES:
            indicadores[f"LO.PISA.{cod}.{p}"] = f"PISA_{nombre}_{p}"
        # Niveles de competencia: total y por sexo
        for nivel, etiqueta in NIVELES[cod].items():
            for suf_cod, suf_nom in SEXOS.items():
                indicadores[f"LO.PISA.{cod}.{nivel}{suf_cod}"] = f"PISA_{nombre}_{etiqueta}_{suf_nom}"
    return indicadores


INDICADORES = construir_indicadores()

# Solo los años en que se aplicó PISA y con datos en el Banco Mundial (evita timeouts de la API)
PISA_YEARS = [2000, 2003, 2006, 2009, 2012, 2015, 2018, 2022]

# Series por petición: con todas juntas la API tarda demasiado
TAMANO_LOTE = 12

ARCHIVO_SALIDA = "pisa_gender_wpp_ready.csv"


def descargar_pisa():
    """Descarga los datos crudos del Banco Mundial (ancho: economy, series, YRxxxx...)."""
    codigos = list(INDICADORES)
    lotes = []
    for i in range(0, len(codigos), TAMANO_LOTE):
        lote = codigos[i : i + TAMANO_LOTE]
        print(f"Descargando series {i + 1}-{i + len(lote)} de {len(codigos)}...")
        lotes.append(
            wb.data.DataFrame(lote, time=PISA_YEARS, labels=False, db=12).reset_index()
        )
    return pd.concat(lotes, ignore_index=True)


def limpiar_pisa(pisa_raw):
    """Deja una fila por país/año, una columna por indicador y las brechas de género."""
    # Formato largo
    pisa_melted = pisa_raw.melt(
        id_vars=["economy", "series"],
        var_name="Time",
        value_name="Score",
    )

    # Quitar el prefijo 'YR' del Banco Mundial para dejar el año como entero (compatible con WPP2024)
    pisa_melted["Time"] = pisa_melted["Time"].str.replace("YR", "").astype(int)

    # Una fila por país/año y una columna por indicador
    pisa_clean = pisa_melted.pivot_table(
        index=["economy", "Time"],
        columns="series",
        values="Score",
    ).reset_index()

    # Renombrar para el merge directo con el dataset de la competencia
    pisa_clean = pisa_clean.rename(columns={"economy": "ISO3_code", **INDICADORES})

    # PISA solo tiene registros en los años de aplicación
    pisa_clean = pisa_clean.dropna(subset=["PISA_Math_Total"], how="all").reset_index(drop=True)

    for nombre in MATERIAS.values():
        # Brecha de género (Mujeres - Hombres)
        pisa_clean[f"Gap_{nombre}_Fem_Male"] = (
            pisa_clean[f"PISA_{nombre}_Female"] - pisa_clean[f"PISA_{nombre}_Male"]
        )
        # Dispersión: distancia entre el percentil 90 y el 10
        pisa_clean[f"Spread_{nombre}_P90_P10"] = (
            pisa_clean[f"PISA_{nombre}_P90"] - pisa_clean[f"PISA_{nombre}_P10"]
        )

    return pisa_clean


def main():
    pisa_clean = limpiar_pisa(descargar_pisa())

    DATA_RAW.mkdir(parents=True, exist_ok=True)
    ruta = DATA_RAW / ARCHIVO_SALIDA
    pisa_clean.to_csv(ruta, index=False)

    print(pisa_clean.head())
    print(f"Guardado: {ruta.relative_to(RAIZ)} ({len(pisa_clean):,} filas, {pisa_clean.shape[1]} columnas)")


if __name__ == "__main__":
    main()
