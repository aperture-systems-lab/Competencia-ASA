# Competencia ASA

> Cómo cambió la desigualdad de aprendizaje (PISA, OCDE) en 8 países de América Latina entre 2009 y 2025, mientras bajaban la fecundidad y la mortalidad infantil (World Population Prospects 2024, ONU). Proyecto del equipo Aperture para el ASA DataQuest 2026; el registro de trabajo está en [docs/bitacora.html](docs/bitacora.html).

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
│   ├── 02_limpieza.ipynb          # Data Preparation: WPP2024 en los años de PISA + unión con PISA → data/processed/
│   ├── 02b_america_latina.ipynb   # América Latina: series 1950–2100 + panel de 8 países con PISA 2006–2025 → data/processed/
│   ├── 02c_tendencias_america_latina.ipynb  # tendencias exploratorias y primera robustez
│   ├── 02d_analisis_america_latina.ipynb    # análisis: cómo cambió la brecha, cobertura y demografía al nacer
│   └── 03_visualizaciones.ipynb   # los 4-6 gráficos finales → figures/
├── src/
│   ├── utils.py                   # rutas y funciones de carga/limpieza reutilizables
│   └── estilo.py                  # paleta, fuentes y tamaños comunes a todos los gráficos
├── figures/                       # PNGs de los gráficos finales
├── docs/
│   ├── bitacora.html              # registro de trabajo del equipo: pregunta, método, hallazgos, decisiones y plan
│   └── competencia/               # guía de la ASA, descripción del Supplement y Guía Ética de la ASA
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
  - OCDE: tabla I.A2.1 de *PISA 2025 Results, Volume I*, anexo A2 ([StatLink](https://stat.link/pe3lsg)): índice de cobertura 3 de cada país, 2003–2025.
- **Archivo(s):**
  - `WPP2024_Demographic_Indicators_Medium_csv.gz`, `WPP2024_Demographic_Indicators_OtherVariants_csv.gz`, `WPP2024_Demographic_Indicators_notes.csv`, `WPP2024_Supplement_Births_and_LE60.csv`
  - `PISA_BancoMundial_2000_2018.csv` (lo genera `notebooks/00_unificacion_pisa.ipynb`)
  - `PISA2022_cap2_desempeno.xlsx`, `PISA2022_cap3_niveles.xlsx`, `PISA2022_cap4_equidad_genero.xlsx`, `PISA2022_cap7_migracion.xlsx`
  - `PISA2025_cap2a_desempeno_niveles.xlsx`, `PISA2025_cap2c_genero.xlsx`, `PISA2025_cap2d_migracion.xlsx`
  - `PISA2025_anexoA2_cobertura.xlsx` (cobertura de PISA por país y ciclo)
  - Resultado unificado: `data/processed/pisa_unificado.csv`
  - Resultados de la limpieza (`02_limpieza`): `data/processed/wpp_paises_pisa.csv`, `wpp_agregados_pisa.csv`, `pisa_wpp.csv` y `diccionario_wpp.csv` (ver [Datos procesados](#datos-procesados))
  - Resultados de `02b_america_latina`: `data/processed/al_wpp_1950_2100.csv` y `al_panel_pisa.csv` (ver [Datos de América Latina](#datos-de-américa-latina))
- **Fecha de descarga:** WPP2024: 2026-10-14. Banco Mundial y OCDE: 2026-10-18. Cobertura de la OCDE: 2026-10-27.
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

### Datos procesados

`notebooks/02_limpieza.ipynb` deja WPP2024 solo en los **años de los ciclos de PISA** (2000, 2003, 2006, 2009, 2012, 2015, 2018, 2022 y 2025). Los años se leen de `pisa_unificado.csv`, no se escriben a mano.

| Archivo | Una fila es... | Filas | Contenido |
|---|---|---|---|
| `wpp_paises_pisa.csv` | un país en un año de PISA | 2 133 (237 × 9) | Todos los países, participen o no en PISA. Útil para dar contexto y para medir el sesgo de selección |
| `wpp_agregados_pisa.csv` | un agregado en un año de PISA | 153 | Mundo, regiones geográficas y grupos de ingreso, como referencia. **No se suman con los países.** Entre sí, solo se suman los de una misma `particion` |
| `pisa_wpp.csv` | un país en un ciclo de PISA en el que participó | 590 | `pisa_unificado.csv` + WPP. Es la tabla principal del análisis |
| `diccionario_wpp.csv` | una columna de WPP | 44 | Descripción, unidad y origen de cada columna |

Decisiones de limpieza:

- **Columnas:** se conservan 17 indicadores del Medium, uno o dos por tema:
  - Población: `TPopulation1July`, `PopDensity`, `MedianAgePop`, `PopGrowthRate`.
  - Fecundidad: `TFR`, `CBR`, `Births`, `Births1519`, `MAC`.
  - Mortalidad: `LEx` (total y por sexo), `IMR`, `Q5`, `CDR`.
  - Migración: `NetMigrations`, `CNMR`.

  Del Supplement se añaden `LE60`, `LE60Male` y `LE60Female`. Las demás columnas son redundantes (correlación > 0,95), son identificadores sin uso o están vacías en gran parte (`DoublingTime`).
- **Nombres y unidades:** se mantienen los originales de la ONU para poder rastrear cada columna hasta su definición. Los conteos siguen en miles.
- **Marcas añadidas:**
  - `es_proyeccion`: solo 2025.
  - `territorio_pequeno`: menos de 100 000 habitantes. En PISA solo afecta a Liechtenstein.
  - `participa_pisa`: solo en `wpp_paises_pisa.csv`.
- **Variable derivada:** `pct_births_adolescentes = 100 × Births1519 / Births`.
- **Doble conteo:** está resuelto en la limpieza.
  - Los archivos de países solo tienen países, y su suma coincide con la fila del Mundo en cada año: tampoco hay solapamientos entre países.
  - Los agregados sí se solapan entre sí. Por ejemplo, `Americas` = `Latin America and the Caribbean` + `Northern America`, y `Middle-income` = `Upper-middle` + `Lower-middle`.
  - La columna `particion` marca dos conjuntos que se pueden sumar o apilar en un gráfico:
    - `continentes`: África, Asia, Europa, América Latina y el Caribe, América del Norte y Oceanía.
    - `ingreso`: alto, medio-alto, medio-bajo, bajo y sin grupo.
  - Ambos suman el Mundo; la partición de ingreso deja fuera a Guadalupe, que WPP no clasifica por ingreso. Las filas con `particion` vacía no se suman.
- **Cobertura parcial de PISA:** en 10 filas de `pisa_wpp.csv`, PISA evaluó solo una ciudad o algunas regiones, pero los datos demográficos son de todo el país:
  - China en todos sus ciclos (Shanghái o algunas provincias).
  - Azerbaiyán en 2022 (Bakú).
  - Ucrania en 2022 y 2025 (parte de sus regiones).
  - Tayikistán en 2025 (Dusambé).
  - Irak en 2025 (Región del Kurdistán).

  Se marcan con `cobertura_pisa_parcial` y `entidad_pisa`. **Hay que excluirlas al relacionar PISA con la demografía.**
- **Incertidumbre de 2025:** para `TPopulation1July`, `TFR` y `LEx` se añaden los intervalos de predicción del 80 % y del 95 % (`*_PI80_inf`, `*_PI80_sup`, `*_PI95_inf`, `*_PI95_sup`). En los años estimados quedan vacíos.
- **Exclusiones:**
  - `OED`, el promedio OCDE: 3 filas de PISA que no existen en WPP. Sigue disponible en `pisa_unificado.csv`.
  - Los agregados que no son Mundo, región geográfica ni grupo de ingreso.
- **Nulos:** solo quedan `LE60` del Vaticano (no está en el Supplement ni participa en PISA) y los intervalos de predicción en los años estimados. No se imputa nada.
- **Outliers:** se conservan todos porque son reales. Por ejemplo, la migración de Qatar en 2006 o la densidad de Macao.
- **Sesgo de selección:** los países de PISA no representan al mundo. En 2022, su mediana de fecundidad es 1,6 hijos frente a 2,4 en los que no participan, y su esperanza de vida, 77,9 años frente a 71,6. Las conclusiones valen para los países participantes.

### Datos de América Latina

Pregunta del equipo: *Entre 2006 y 2025, mientras bajaban la fecundidad y la mortalidad infantil en América Latina, ¿se redujo o creció la desigualdad de aprendizaje dentro de los países?* `notebooks/02b_america_latina.ipynb` prepara dos tablas:

| Archivo | Una fila es... | Filas | Contenido |
|---|---|---|---|
| `al_wpp_1950_2100.csv` | un país de América Latina (50) o la región, en un año de 1950 a 2100 | 7 701 | `TFR`, `IMR`, maternidad adolescente, edad mediana y esperanza de vida, con intervalos de predicción del 80 % y 95 % de `TFR` e `IMR` desde 2024 |
| `al_panel_pisa.csv` | uno de los 8 países del panel, en un ciclo de PISA (2006–2025) y una materia | 168 (8 × 7 × 3) | Percentiles 10, 25, 50, 75 y 90 con error estándar, brecha P90 − P10, % bajo el nivel 2, índice de cobertura y demografía del año de la prueba y del año de nacimiento (ciclo − 15) |

Decisiones (fijadas antes de ver resultados; detalle y justificación en [docs/bitacora.html](docs/bitacora.html)):

- **PISA:** tablas oficiales de tendencia de la OCDE (I.B1.2a.33–41 del libro de 2025), no `pisa_unificado.csv`: una sola fuente, valores revisados y comparables entre ciclos, con error estándar.
- **Desigualdad de aprendizaje:** brecha P90 − P10 y % bajo el nivel 2. Matemáticas como materia principal; lectura y ciencias para comprobar robustez.
- **Panel:** Argentina, Brasil, Chile, Colombia, Costa Rica, México, Perú y Uruguay, los 8 países con PISA en los 6 ciclos de 2009 a 2025. 2006 queda como contexto.
- **Argentina 2015:** excluido (la OCDE lo considera no comparable; su tabla de tendencias lo publica sin dato).
- **Cobertura:** se agrega el índice de cobertura 3 porque la proporción de jóvenes de 15 años que representa PISA subió entre 9 y 20 puntos en estos países.

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
   - `02_limpieza`: filtra WPP2024 a los años de PISA, lo une con `pisa_unificado.csv` y genera los cuatro archivos de [Datos procesados](#datos-procesados).
   - `02b_america_latina`: genera los dos archivos de [Datos de América Latina](#datos-de-américa-latina).
   - `02c_tendencias_america_latina`: tendencias exploratorias por país. Solo lee, no guarda nada.
   - `02d_analisis_america_latina`: cómo cambió la brecha (cambios oficiales de la OCDE), corrección por cobertura y demografía al nacer. Solo lee, no guarda nada.
   - `03_visualizaciones`: genera las figuras en `figures/`.

Antes de dar un notebook por terminado, haz **Restart & Run All** para comprobar que funciona de principio a fin.

## Convenciones

- `data/raw/` es de solo lectura. Toda transformación se guarda en `data/processed/`.
- Los notebooks se numeran en el orden del proceso.
- Todos los notebooks llaman a `aplicar_estilo()` de `src/estilo.py`, así todos los gráficos parecen del mismo proyecto.
- Las figuras llevan nombres descriptivos: `fig03_ventas_por_region.png`, no `grafico1.png`.
