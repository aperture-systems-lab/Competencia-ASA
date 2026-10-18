# Competencia ASA

> _Una o dos frases: qué se analiza, con qué datos y para quién._

Proyecto de análisis exploratorio (EDA) y visualización. Sigue las fases de CRISP-DM hasta la preparación de datos (no incluye modelado). La historia completa, con hallazgos y conclusiones, está en [REPORT.md](REPORT.md).

## Estructura

```
competencia_asa/
├── data/
│   ├── raw/                       # datos originales: NUNCA se modifican
│   └── processed/                 # datos limpios, listos para graficar
├── notebooks/
│   ├── 00_unificacion_pisa.ipynb  # une PISA 2000–2018 (Banco Mundial) + 2022 y 2025 (OCDE) → data/processed/
│   ├── 01_exploracion.ipynb       # Data Understanding
│   ├── 02_limpieza.ipynb          # Data Preparation: limpieza → data/processed/
│   └── 03_visualizaciones.ipynb   # los 4-6 gráficos finales → figures/
├── src/
│   ├── utils.py                   # rutas y funciones de carga/limpieza reutilizables
│   └── estilo.py                  # paleta, fuentes y tamaños comunes a todos los gráficos
├── figures/                       # PNGs de los gráficos finales
├── README.md                      # este archivo: qué es el proyecto y cómo ejecutarlo
├── REPORT.md                      # la historia: preguntas, hallazgos y conclusiones
├── pyproject.toml                 # dependencias del proyecto (gestionadas con uv)
└── uv.lock                        # versiones exactas instaladas (no se edita a mano)
```

## Datos

- **Fuente:** _(organización / enlace)_
- **Archivo(s):** _(nombre en `data/raw/`)_
- **Fecha de descarga:** _(AAAA-MM-DD)_
- **Qué representa cada fila:** _(...)_

## Cómo ejecutarlo

Requiere [uv](https://docs.astral.sh/uv/). uv instala la versión de Python correcta (ver `.python-version`) y todas las dependencias en `.venv/`:

```bash
uv sync
```

Para añadir una librería: `uv add nombre` (o `uv add --dev nombre` si solo hace falta para trabajar, no para el análisis).

En VS Code, abre un notebook y elige como kernel el Python de `.venv`. Para usar Jupyter en el navegador: `uv run --with jupyter jupyter lab`.

1. Coloca los datos originales en `data/raw/`.
2. Ejecuta los notebooks en orden:
   - `01_exploracion`: solo lee, no guarda nada.
   - `02_limpieza`: genera el archivo limpio en `data/processed/`.
   - `03_visualizaciones`: genera las figuras en `figures/`.

Antes de dar un notebook por terminado, haz **Restart & Run All** para comprobar que funciona de principio a fin.

## Convenciones

- `data/raw/` es de solo lectura. Toda transformación se guarda en `data/processed/`.
- Los notebooks se numeran en el orden del proceso.
- Todos los notebooks llaman a `aplicar_estilo()` de `src/estilo.py`, así todos los gráficos parecen del mismo proyecto.
- Las figuras llevan nombres descriptivos: `fig03_ventas_por_region.png`, no `grafico1.png`.
