import sqlite3
import os

import pandas as pd
import matplotlib.pyplot as plt


# ============================================================
# CONFIGURACIÓN
# ============================================================

BASES = {
    1: {
        1: "TransferDefault11.db",
        2: "TransferDefault21.db",
        3: "TransferDefault31.db",
    },
    2: {
        1: "TransferDefault12.db",
        2: "TransferDefault22.db",
        3: "TransferDefault32.db",
    },
    3: {
        1: "TransferDefault13.db",
        2: "TransferDefault23.db",
        3: "TransferDefault33.db",
    },
}


# ============================================================
# LECTURA DE UNA BASE DE DATOS
# ============================================================

def leer_base(nombre_base, experimento_origen):
    """
    Lee objective 0 y objective 1 de todos los trials
    de una base de datos.

    Retorna un DataFrame con:
        - trial
        - objective0
        - objective1
        - origen
    """

    if not os.path.exists(nombre_base):
        print(f"⚠️ No se encontró: {nombre_base}")
        return pd.DataFrame()

    conexion = sqlite3.connect(nombre_base)

    consulta = """
        SELECT
            trial_id,
            objective,
            value
        FROM trial_values
        WHERE objective IN (0, 1)
        ORDER BY trial_id, objective
    """

    datos = pd.read_sql_query(consulta, conexion)

    conexion.close()

    if datos.empty:
        print(f"⚠️ No se encontraron valores en {nombre_base}")
        return pd.DataFrame()

    # Convertimos las dos filas de cada trial
    # (objective 0 y objective 1) en una sola fila.
    datos = datos.pivot(
        index="trial_id",
        columns="objective",
        values="value"
    ).reset_index()

    datos = datos.rename(columns={
        0: "objective0",
        1: "objective1"
    })

    # Solo conservamos trials que tengan ambos objetivos.
    datos = datos.dropna(
        subset=["objective0", "objective1"]
    )

    datos["origen"] = f"Experimento {experimento_origen}"

    return datos


# ============================================================
# CONSTRUIR DATOS DE UN EXPERIMENTO
# ============================================================

def cargar_experimento(experimento):
    """
    Carga las tres bases que contienen los resultados
    evaluados sobre un experimento determinado.

    Por ejemplo, para experimento=1:

        TransferDefault11.db -> origen Exp. 1
        TransferDefault21.db -> origen Exp. 2
        TransferDefault31.db -> origen Exp. 3
    """

    resultados = []

    for origen, nombre_base in BASES[experimento].items():

        datos = leer_base(
            nombre_base,
            origen
        )

        if not datos.empty:
            resultados.append(datos)

    if not resultados:
        return pd.DataFrame()

    return pd.concat(
        resultados,
        ignore_index=True
    )


# ============================================================
# GRÁFICO
# ============================================================

def graficar_experimento(experimento):
    """
    Genera el gráfico combinado para un experimento.

    Cada origen mantiene el color utilizado
    en los gráficos anteriores:
        Exp. 1 -> azul
        Exp. 2 -> rojo
        Exp. 3 -> verde
    """

    datos = cargar_experimento(experimento)

    if datos.empty:
        print(
            f"No hay datos para el Experimento {experimento}."
        )
        return

    plt.figure(figsize=(9, 7))

    colores = {
        "Experimento 1": "blue",
        "Experimento 2": "red",
        "Experimento 3": "green"
    }

    for origen in [
        "Experimento 1",
        "Experimento 2",
        "Experimento 3"
    ]:

        subconjunto = datos[
            datos["origen"] == origen
        ]

        if subconjunto.empty:
            continue

        plt.scatter(
            subconjunto["objective0"],
            subconjunto["objective1"],
            label=origen,
            color=colores[origen],
            alpha=0.75,
            s=45
        )

    plt.xlabel("Objective 0")
    plt.ylabel("Objective 1")

    plt.title(
        f"Frentes de Pareto transferidos — Experimento {experimento}"
    )

    plt.legend()

    plt.grid(
        True,
        alpha=0.25
    )

    plt.tight_layout()

    nombre_archivo = (
        f"pareto_combinado_exp{experimento}.png"
    )

    plt.savefig(
        nombre_archivo,
        dpi=300,
        bbox_inches="tight"
    )

    plt.show()

    print(
        f"✓ Gráfico guardado: {nombre_archivo}"
    )


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    print("=" * 60)
    print("GRÁFICOS COMBINADOS DE FRENTES DE PARETO")
    print("=" * 60)

    for experimento in range(1, 4):

        print(
            f"\nGenerando gráfico del Experimento {experimento}..."
        )

        graficar_experimento(experimento)

    print("\n" + "=" * 60)
    print("Proceso finalizado.")
    print("=" * 60)