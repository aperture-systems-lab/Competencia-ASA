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
│   ├── 01_exploracion.ipynb       # Data Understanding: WPP2024 (Medium, Supplement y OtherVariants) y su enlace con PISA
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

- **Fuente:**
  - Naciones Unidas, División de Población: [World Population Prospects 2024](https://population.un.org/wpp/) (indicadores demográficos).
  - Banco Mundial: [Education Statistics (EdStats)](https://databank.worldbank.org/source/education-statistics), base 12, descargada con `wbgapi` (PISA 2000–2018).
  - OCDE: tablas web de *PISA 2022 Results, Volume I* y *PISA 2025 Results, Volume I* (PISA 2022 y 2025).
- **Archivo(s):**
  - `WPP2024_Demographic_Indicators_Medium_csv.gz`, `WPP2024_Demographic_Indicators_OtherVariants_csv.gz`, `WPP2024_Demographic_Indicators_notes.csv`, `WPP2024_Supplement_Births_and_LE60.csv`
  - `PISA_BancoMundial_2000_2018.csv` (lo genera `notebooks/00_unificacion_pisa.ipynb`)
  - `PISA2022_cap2_desempeno.xlsx`, `PISA2022_cap3_niveles.xlsx`, `PISA2022_cap4_equidad_genero.xlsx`, `PISA2022_cap7_migracion.xlsx`
  - `PISA2025_cap2a_desempeno_niveles.xlsx`, `PISA2025_cap2c_genero.xlsx`, `PISA2025_cap2d_migracion.xlsx`
  - Resultado unificado: `data/processed/pisa_unificado.csv`
- **Fecha de descarga:** WPP2024: 2026-10-14. Banco Mundial y OCDE: 2026-10-18.
- **Qué representa cada fila:**
  - WPP2024 Medium: una ubicación en un año (`LocID`, `Time`), de 1950 a 2101. Las ubicaciones mezclan 237 países (`LocTypeName == "Country/Area"`) con agregados (Mundo, regiones, grupos de ingreso...), así que hay que filtrar antes de sumar o promediar.
  - WPP2024 Supplement: un país en un año (`ISO3_code`, `Time`), de 1950 a 2100. Son 236 países (todos menos el Vaticano) y se une uno a uno con el Medium.
  - WPP2024 OtherVariants: una ubicación en un año y una variante de proyección (`LocID`, `Variant`, `Time`), solo de 2024 a 2101. Tiene las mismas columnas que el Medium.
  - `pisa_unificado.csv`: un país (o el promedio OCDE, `OED`) en un ciclo de PISA (`ISO3_code`, `Time`), con puntajes medios, percentiles y niveles de competencia por materia, en total y por sexo, más el % con nivel mínimo según origen migratorio.

### Notas sobre WPP2024

Detalle en `notebooks/01_exploracion.ipynb`:

- **Doble conteo:** sumar la población de 2023 sin filtrar da unos 363 000 millones de personas, unas 45 veces la real (8 092 millones). Filtrar por `LocTypeName == "Country/Area"` equivale a filtrar por `ISO3_code.notna()`.
- **Estimación y proyección:** los datos de 1950 a 2023 son estimaciones; los de 2024 en adelante son proyecciones de la variante media. Por eso PISA 2025 se cruza con datos proyectados.
- **Unidades:**
  - Población, nacimientos, muertes y migrantes están en **miles**; para dar cifras absolutas hay que multiplicar por 1.000.
  - `CBR`, `CDR` y `CNMR` son tasas por 1.000 habitantes.
  - `IMR` y `Q5` son defunciones por 1.000 nacidos vivos.
  - `TFR` está en hijos por mujer.
- **Diccionario:** `WPP2024_Demographic_Indicators_notes.csv` describe los 54 indicadores del Medium (tema, nombre y unidad). No contiene el texto de las notas al pie de la columna `Notes`.
- **Supplement:** añade nacimientos por sexo (`BirthsMale`, `BirthsFemale`, que suman `Births`) y la esperanza de vida a los 60 años (`LE60`, `LE60Male`, `LE60Female`).
- **Año 2101:** solo trae la población a 1 de enero; el resto de indicadores están vacíos.
- **`DoublingTime`:** queda vacío cuando el crecimiento es igual o menor al 0,5 % anual.
- **Territorios muy pequeños:** con menos de 200 nacimientos al año, el redondeo a miles distorsiona los cocientes.
- **Enlace con PISA:** 590 de las 593 filas de PISA tienen país y año en WPP. Las 3 restantes son `OED`, que no existe en WPP.
- **OtherVariants:** son unas 663 000 filas con 18 variantes de proyección, en dos familias:
  - **Escenarios deterministas:** cambian un supuesto y dejan el resto como en el Medium. Por ejemplo, `High` y `Low` suman o restan hasta 0,5 hijos por mujer a la fecundidad, y en 2100 dan una población un 43 % mayor y un 32 % menor que el Medium (mediana entre países). Otros son `Constant fertility`, `Zero migration`, `Constant mortality`, `Momentum`...
  - **Proyección probabilística:** `Median PI`, los intervalos de predicción del 80 % y del 95 % (`Lower/Upper 80 PI`, `Lower/Upper 95 PI`) y `Mean`. `Median PI` coincide con el Medium y `Mean` solo trae `TFR`, `LExMale` y `LExFemale`.
  - **Cobertura desigual:** no todas las variantes traen todos los indicadores. Las probabilísticas no traen `NRR`, `SRB` ni muertes por sexo o infantiles, y varios escenarios no traen `LE15/65/80` ni las probabilidades de muerte `Q`.
  - **Incertidumbre en 2025:** en los países de PISA, el intervalo del 95 % mide unos ±0,27 hijos en `TFR` y ±1,5 años en `LEx` (mediana).
  - **Sensibilidad a largo plazo:** según el Medium, la población mundial llega a su máximo en 2084. Según el intervalo del 95 %, ese pico puede llegar en 2068 o no haberse alcanzado todavía en 2100.

## Criterios de análisis (técnicos y éticos, ASA)

Se aplican en todos los notebooks y en el informe:

1. **Sin doble conteo:** para comparar o agregar países se filtra siempre `LocTypeName == "Country/Area"`. Los agregados (Mundo, regiones, grupos de ingreso) solo se usan como referencia y se guardan aparte.
2. **Unidades explícitas:** cada eje y cada tabla indican su unidad. Las cifras absolutas se presentan en personas (miles × 1.000).
3. **Hechos vs. supuestos:** 2023 es la frontera entre estimaciones y proyecciones. Cada hallazgo dice si se basa en estimaciones o en proyecciones y, en ese caso, con qué variante.
4. **La variante media no es una certeza:** todo resultado posterior a 2023 se acompaña de su intervalo de predicción (`Lower/Upper 80/95 PI`) o de escenarios alternativos de `OtherVariants`.
5. **Transparencia:** `02_limpieza` documenta los criterios de inclusión y exclusión de países (agregados, `OED`, Vaticano, territorios muy pequeños), el tratamiento de nulos y cuántas filas afecta cada decisión.
6. **Sin selección a conveniencia:** los años de análisis (ciclos de PISA y la frontera 2023) se fijan de antemano. No se eligen variantes ni años para respaldar una conclusión ya decidida.
7. **Calidad desigual de los datos:** en países con registros civiles incompletos o en conflicto, las estimaciones históricas se basan en censos antiguos o en modelos indirectos y tienen más error. Estos archivos no cuantifican ese error por país, así que se menciona en las limitaciones del informe.
8. **Contexto y no estigmatización:** fecundidad, mortalidad infantil y migración se interpretan junto a sus determinantes socioeconómicos y geopolíticos. Se evitan el determinismo demográfico y las lecturas que estigmaticen regiones o flujos migratorios. Las correlaciones son descriptivas y no implican causalidad.
9. **Reproducibilidad:** todo se carga directamente de los `.csv` y `.csv.gz` de `data/raw/` con `src/utils.py` (los `.gz`, con `compression="gzip"` y `encoding="utf-8-sig"`), sin pasos manuales. Si alguna vez se simula o se muestrea, se fija la semilla.

## Cómo ejecutarlo

Requiere [uv](https://docs.astral.sh/uv/). uv instala la versión de Python correcta (ver `.python-version`) y todas las dependencias en `.venv/`:

```bash
uv sync
```

Para añadir una librería: `uv add nombre` (o `uv add --dev nombre` si solo hace falta para trabajar, no para el análisis).

En VS Code, abre un notebook y elige como kernel el Python de `.venv`. Para usar Jupyter en el navegador: `uv run --with jupyter jupyter lab`.

1. Coloca los datos originales en `data/raw/`.
2. Ejecuta los notebooks en orden:
   - `00_unificacion_pisa`: genera `data/processed/pisa_unificado.csv`.
   - `01_exploracion`: explora WPP2024 (Medium, Supplement y OtherVariants) y comprueba el enlace con PISA. Solo lee (`data/raw/` y `pisa_unificado.csv`), no guarda nada.
   - `02_limpieza`: genera el archivo limpio en `data/processed/`.
   - `03_visualizaciones`: genera las figuras en `figures/`.

Antes de dar un notebook por terminado, haz **Restart & Run All** para comprobar que funciona de principio a fin.

## Convenciones

- `data/raw/` es de solo lectura. Toda transformación se guarda en `data/processed/`.
- Los notebooks se numeran en el orden del proceso.
- Todos los notebooks llaman a `aplicar_estilo()` de `src/estilo.py`, así todos los gráficos parecen del mismo proyecto.
- Las figuras llevan nombres descriptivos: `fig03_ventas_por_region.png`, no `grafico1.png`.
