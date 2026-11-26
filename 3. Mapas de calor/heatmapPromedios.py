import matplotlib.pyplot as plt
import numpy as np

from lectorDBCreate import obtener_resultados_dbcreate
from lectorExploracion import obtener_resultado_exploracion


# ============================================================
# CONFIGURACIÓN
# ============================================================

METRICAS = [
    "exp1_noRev_pct",
    "exp1_rev_pct",
    "exp1_noRev_skip",
    "exp1_rev_skip",
    "exp2_pct",
    "exp2_skip",
    "exp3_pct",
    "exp3_skipMalo",
    "exp3_skipRespondido"
]

NOMBRES_METRICAS = [
    "Exp1 NoRev\nCoincidencia",
    "Exp1 Rev\nCoincidencia",
    "Exp1 NoRev\nSkips",
    "Exp1 Rev\nSkips",
    "Exp2\nCoincidencia",
    "Exp2\nSkips",
    "Exp3\nCoincidencia",
    "Exp3\nSkips malos",
    "Exp3\nSkips respondidos"
]


# ============================================================
# PREPARAR DATOS
# ============================================================

def construir_matriz():

    resultado_dbcreate = obtener_resultados_dbcreate()
    resultado_exploracion = obtener_resultado_exploracion()

    fuentes = [
        resultado_exploracion
    ]

    fuentes.extend(resultado_dbcreate)

    nombres = []
    matriz = []

    for fuente in fuentes:

        nombres.append(fuente["nombre"])

        fila = []

        for metrica in METRICAS:

            valor = fuente["metricas_prom"].get(metrica)

            if valor is None:
                fila.append(np.nan)
            else:
                fila.append(valor)

        matriz.append(fila)

    return nombres, np.array(matriz, dtype=float)


# ============================================================
# GENERAR TABLA
# ============================================================

def generar_tabla():

    nombres, matriz = construir_matriz()

    fig, ax = plt.subplots(
        figsize=(16, 5)
    )

    ax.axis("off")

    # --------------------------------------------------------
    # Preparar texto
    # --------------------------------------------------------

    datos = []

    for fila in matriz:

        fila_texto = []

        for valor in fila:

            if np.isnan(valor):
                fila_texto.append("—")
            else:
                fila_texto.append(f"{valor:.2f}")

        datos.append(fila_texto)

    # --------------------------------------------------------
    # Crear tabla
    # --------------------------------------------------------

    tabla = ax.table(
        cellText=datos,
        rowLabels=nombres,
        colLabels=NOMBRES_METRICAS,
        cellLoc="center",
        rowLoc="center",
        loc="center"
    )

    # --------------------------------------------------------
    # Ajustes visuales
    # --------------------------------------------------------

    tabla.auto_set_font_size(False)
    tabla.set_fontsize(9)

    tabla.scale(
        1,
        2
    )

    ax.set_title(
        "Promedio de los valores obtenidos por fuente y métrica",
        pad=20
    )

    plt.tight_layout()

    plt.show()


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    generar_tabla()