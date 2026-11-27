"""
constructorDataset.py

Lee una base de datos generada durante la validación (DBCreate),
recalcula los scores promedio de los tres experimentos y devuelve
un DataFrame compatible con el resto del pipeline.
"""

import sqlite3
import pandas as pd

from scores import (
    score_exp1,
    score_exp2,
    score_exp3
)


# ==========================================================
# CONSTRUCTOR
# ==========================================================

def construir_dataset(nombre_bd, nombre_estudio=None):

    # ------------------------------------------------------
    # Leer la tabla completa
    # ------------------------------------------------------

    conn = sqlite3.connect(nombre_bd)

    dataset = pd.read_sql_query(

        "SELECT * FROM configuraciones",

        conn

    )

    conn.close()

    # ------------------------------------------------------
    # Renombrar columnas para mantener compatibilidad
    # ------------------------------------------------------

    dataset.rename(

        columns={
            "origen": "nombre_estudio",

            "trial_original": "trial"
        },

        inplace=True

    )

    # ------------------------------------------------------
    # Sobrescribir nombre del estudio (opcional)
    # ------------------------------------------------------

    if nombre_estudio is not None:

        dataset["nombre_estudio"] = nombre_estudio

    # ------------------------------------------------------
    # Recalcular scores usando los promedios
    # ------------------------------------------------------

    dataset[

        ["score0_exp1", "score1_exp1"]

    ] = dataset.apply(

        lambda fila: score_exp1(fila),

        axis=1,

        result_type="expand"

    )

    dataset[

        ["score0_exp2", "score1_exp2"]

    ] = dataset.apply(

        lambda fila: score_exp2(fila),

        axis=1,

        result_type="expand"

    )

    dataset[

        ["score0_exp3", "score1_exp3"]

    ] = dataset.apply(

        lambda fila: score_exp3(fila),

        axis=1,

        result_type="expand"

    )

    # ------------------------------------------------------
    # Reordenar columnas principales
    # ------------------------------------------------------

    columnas_inicio = [

        "id",
        "trial",
        "nombre_estudio",

        "score0_original",
        "score1_original",

        "score0_exp1",
        "score1_exp1",

        "score0_exp2",
        "score1_exp2",

        "score0_exp3",
        "score1_exp3"

    ]

    resto_columnas = [

        columna

        for columna in dataset.columns

        if columna not in columnas_inicio

    ]

    dataset = dataset[

        columnas_inicio + resto_columnas

    ]

    return dataset


# ==========================================================
# PRUEBA
# ==========================================================

if __name__ == "__main__":

    dataset = construir_dataset(

        "validacion_pareto2Default.db",

        nombre_estudio="Pareto Exp2"

    )

    print(dataset.head())

    print()

    print(dataset.columns)

    print()

    print(dataset.shape)