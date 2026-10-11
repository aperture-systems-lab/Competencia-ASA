"""Estilo común a todos los gráficos del proyecto.

Se define una sola vez aquí y se importa en cada notebook, para que todas las
figuras parezcan del mismo proyecto:

    from src.estilo import aplicar_estilo, guardar_figura, PALETA, DESTACADO, GRIS
    aplicar_estilo()

No llames a sns.set_theme() después de aplicar_estilo(): lo sobrescribiría.
"""

import matplotlib as mpl
from cycler import cycler
from matplotlib.colors import LinearSegmentedColormap

from src.utils import FIGURES, RAIZ

# --- Colores ------------------------------------------------------------------

# Categórica (identidad: regiones, productos, grupos...). Se asigna siempre en
# este orden y cada categoría conserva su color en todos los gráficos.
# El orden está elegido para que colores contiguos se distingan también con
# daltonismo. Con más de 8 categorías, agrupa en "Otros" o usa small multiples.
# En dispersión o mapas (todas las categorías mezcladas) mejor no pasar de 3.
PALETA = [
    "#2a78d6",  # azul
    "#eb6834",  # naranja
    "#1baf7a",  # aguamarina
    "#eda100",  # amarillo
    "#e87ba4",  # magenta
    "#008300",  # verde
    "#6250d6",  # violeta
    "#e34948",  # rojo
]

# Color con intención: lo que quieres destacar en DESTACADO, el resto en GRIS
DESTACADO = PALETA[0]
GRIS = "#c3c2b7"

# Secuencial (magnitud, de poco a mucho): un solo tono, de claro a oscuro
SECUENCIAL = ["#cde2fb", "#9ec5f4", "#6da7ec", "#3987e5", "#256abf", "#184f95", "#0d366b"]
CMAP_SECUENCIAL = LinearSegmentedColormap.from_list("secuencial", SECUENCIAL)

# Divergente (por debajo / por encima de un punto medio, p. ej. correlaciones):
# dos tonos opuestos con un gris neutro en el centro
CMAP_DIVERGENTE = LinearSegmentedColormap.from_list("divergente", ["#2a78d6", "#f0efec", "#e34948"])

# Tinta y fondo
TEXTO = "#0b0b0b"
TEXTO_SECUNDARIO = "#52514e"
TEXTO_SUAVE = "#898781"
EJE = "#c3c2b7"
REJILLA = "#e1e0d9"
FONDO = "#ffffff"


# --- Estilo -------------------------------------------------------------------


def aplicar_estilo():
    """Aplica el estilo del proyecto a matplotlib (y por tanto a seaborn y pandas)."""
    mpl.rcParams.update(
        {
            # Lienzo y exportación
            "figure.figsize": (10, 6),
            "figure.facecolor": FONDO,
            "axes.facecolor": FONDO,
            "savefig.dpi": 200,
            "savefig.bbox": "tight",
            "savefig.facecolor": FONDO,
            # Tipografía
            "font.family": "sans-serif",
            "font.sans-serif": ["Segoe UI", "Helvetica", "Arial", "DejaVu Sans"],
            "font.size": 11,
            "axes.titlesize": 15,
            "axes.titleweight": "bold",
            "axes.titlelocation": "left",
            "axes.titlepad": 12,
            "axes.labelsize": 11,
            "xtick.labelsize": 10,
            "ytick.labelsize": 10,
            "legend.fontsize": 10,
            "legend.frameon": False,
            # Tinta: el texto nunca usa los colores de las series
            "text.color": TEXTO,
            "axes.titlecolor": TEXTO,
            "axes.labelcolor": TEXTO_SECUNDARIO,
            "xtick.color": TEXTO_SUAVE,
            "ytick.color": TEXTO_SUAVE,
            # Ejes y rejilla discretos
            "axes.edgecolor": EJE,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.grid": True,
            "axes.grid.axis": "y",
            "axes.axisbelow": True,
            "grid.color": REJILLA,
            "grid.linewidth": 0.8,
            # Marcas finas
            "lines.linewidth": 2,
            "lines.markersize": 7,
            "patch.edgecolor": FONDO,
            "axes.prop_cycle": cycler(color=PALETA),
        }
    )


def guardar_figura(fig, nombre):
    """Guarda la figura en figures/ como PNG.

    Usa nombres descriptivos: guardar_figura(fig, "fig03_ventas_por_region")
    """
    if not nombre.endswith(".png"):
        nombre += ".png"
    ruta = FIGURES / nombre
    fig.savefig(ruta)
    print(f"Figura guardada: {ruta.relative_to(RAIZ)}")
    return ruta
