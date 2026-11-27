import math


def distancia_exp1(score0, score1):
    """
    Calcula la distancia para el Experimento 1.

    score0 -> Error (minimizar)
    score1 -> Tiempo (debe ser >= 100)

    Si score1 >= 100:
        La distancia corresponde únicamente al error.

    Si score1 < 100:
        Se calcula la distancia euclidiana al punto (0, 100).
    """

    if score1 >= 100:
        return score0

    return math.sqrt(score0**2 + (100 - score1)**2)


def distancia_origen(score0, score1):
    """
    Distancia euclidiana al origen.
    Utilizada por los Experimentos 2 y 3.
    """

    return math.sqrt(score0**2 + score1**2)


def calcular_metricas(dataset):
    """
    Añade las métricas necesarias para el gráfico 3D.

    Devuelve el mismo DataFrame con columnas nuevas.
    """

    dataset = dataset.copy()

    # -------------------------------------------------
    # Información adicional del Experimento 1
    # -------------------------------------------------

    dataset["exp1_tiempo_suficiente"] = (
        dataset["score1_exp1"] >= 100
    )

    # -------------------------------------------------
    # Distancias
    # -------------------------------------------------

    dataset["dist_exp1"] = dataset.apply(
        lambda fila: distancia_exp1(
            fila["score0_exp1"],
            fila["score1_exp1"]
        ),
        axis=1
    )

    dataset["dist_exp2"] = dataset.apply(
        lambda fila: distancia_origen(
            fila["score0_exp2"],
            fila["score1_exp2"]
        ),
        axis=1
    )

    dataset["dist_exp3"] = dataset.apply(
        lambda fila: distancia_origen(
            fila["score0_exp3"],
            fila["score1_exp3"]
        ),
        axis=1
    )

    return dataset