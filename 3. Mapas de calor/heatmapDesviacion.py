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

    # --------------------------------------------------------
    # Obtener resultados de ambas fuentes
    # --------------------------------------------------------

    resultado_dbcreate = obtener_resultados_dbcreate()

    resultado_exploracion = obtener_resultado_exploracion()

    # --------------------------------------------------------
    # Lista de fuentes
    #
    # Aquí se puede agregar/quitar una fuente fácilmente.
    # --------------------------------------------------------

    fuentes = [
        resultado_exploracion
    ]

    fuentes.extend(resultado_dbcreate)

    # --------------------------------------------------------
    # Construir matriz
    # --------------------------------------------------------

    nombres = []
    matriz = []

    for fuente in fuentes:

        nombres.append(fuente["nombre"])

        fila = []

        for metrica in METRICAS:

            valor = fuente["metricas"].get(metrica)

            if valor is None:
                fila.append(np.nan)
            else:
                fila.append(valor)

        matriz.append(fila)

    return nombres, np.array(matriz, dtype=float)


# ============================================================
# MOSTRAR DATOS
# ============================================================

def mostrar_matriz(nombres, matriz):

    print("\n")
    print("=" * 100)
    print("MATRIZ DE DESVIACIONES ESTÁNDAR")
    print("=" * 100)

    print("\nFuente".ljust(25), end="")

    for nombre in NOMBRES_METRICAS:
        nombre = nombre.replace("\n", " ")
        print(f"{nombre:>20}", end="")

    print()

    print("-" * 100)

    for nombre, fila in zip(nombres, matriz):

        print(f"{nombre:<25}", end="")

        for valor in fila:

            if np.isnan(valor):
                texto = "PENDIENTE"
            else:
                texto = f"{valor:.4f}"

            print(f"{texto:>20}", end="")

        print()


# ============================================================
# GENERAR HEATMAP
# ============================================================

def generar_heatmap():

    nombres, matriz = construir_matriz()

    mostrar_matriz(nombres, matriz)

    # --------------------------------------------------------
    # Crear figura
    # --------------------------------------------------------

    fig, ax = plt.subplots(
        figsize=(15, 6)
    )

    # --------------------------------------------------------
    # Heatmap
    # --------------------------------------------------------

    imagen = ax.imshow(
        matriz,
        aspect="auto",
        cmap="YlGnBu"
    )

    # --------------------------------------------------------
    # Ejes
    # --------------------------------------------------------

    ax.set_xticks(
        np.arange(len(NOMBRES_METRICAS))
    )

    ax.set_xticklabels(
        NOMBRES_METRICAS
    )

    ax.set_yticks(
        np.arange(len(nombres))
    )

    ax.set_yticklabels(
        nombres
    )

    # --------------------------------------------------------
    # Valores dentro de las celdas
    # --------------------------------------------------------

    # Normalización utilizada para determinar si el fondo
    # es suficientemente oscuro para utilizar texto blanco.
    valor_maximo = np.nanmax(matriz)

    for i in range(matriz.shape[0]):

        for j in range(matriz.shape[1]):

            valor = matriz[i, j]

            if np.isnan(valor):

                texto = "—"
                color_texto = "black"

            else:

                texto = f"{valor:.2f}"

                # ------------------------------------------------
                # Determinar color del texto
                # ------------------------------------------------

                valor_normalizado = valor / valor_maximo

                if valor_normalizado > 0.55:
                    color_texto = "white"
                else:
                    color_texto = "black"

            ax.text(
                j,
                i,
                texto,
                ha="center",
                va="center",
                color=color_texto
            )

    # --------------------------------------------------------
    # Barra de color
    # --------------------------------------------------------

    cbar = fig.colorbar(
        imagen,
        ax=ax
    )

    cbar.set_label(
        "Desviación estándar promedio"
    )

    # --------------------------------------------------------
    # Títulos
    # --------------------------------------------------------

    ax.set_xlabel(
        "Métrica"
    )

    ax.set_ylabel(
        "Fuente de datos"
    )

    ax.set_title(
        "Desviación estándar promedio por fuente y métrica"
    )

    # --------------------------------------------------------
    # Ajustes
    # --------------------------------------------------------

    plt.tight_layout()

    plt.show()


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    generar_heatmap()