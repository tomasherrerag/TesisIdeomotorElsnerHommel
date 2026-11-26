import sqlite3


# ============================================================
# MÉTRICAS UTILIZADAS
# ============================================================

METRICAS = {
    "exp1_noRev_pct": "exp1_noRev_pct_std",
    "exp1_rev_pct": "exp1_rev_pct_std",
    "exp1_noRev_skip": "exp1_noRev_skip_std",
    "exp1_rev_skip": "exp1_rev_skip_std",
    "exp2_pct": "exp2_pct_std",
    "exp2_skip": "exp2_skip_std",
    "exp3_pct": "exp3_pct_std",
    "exp3_skipMalo": "exp3_skipMalo_std",
    "exp3_skipRespondido": "exp3_skipRespondido_std",
}

# ============================================================
# MÉTRICAS DE PROMEDIOS
# ============================================================

METRICAS_PROM = {
    "exp1_noRev_pct": "exp1_noRev_pct_prom",
    "exp1_rev_pct": "exp1_rev_pct_prom",
    "exp1_noRev_skip": "exp1_noRev_skip_prom",
    "exp1_rev_skip": "exp1_rev_skip_prom",
    "exp2_pct": "exp2_pct_prom",
    "exp2_skip": "exp2_skip_prom",
    "exp3_pct": "exp3_pct_prom",
    "exp3_skipMalo": "exp3_skipMalo_prom",
    "exp3_skipRespondido": "exp3_skipRespondido_prom",
}


# ============================================================
# BASES DBCreate
# ============================================================

BASES_DBCREATE = [
    (
        "validacion_pareto1Default.db",
        "Pareto Exp1"
    ),
    (
        "validacion_pareto2Default.db",
        "Pareto Exp2"
    ),
    (
        "validacion_pareto3Default.db",
        "Pareto Exp3"
    ),
    (
        "validacion_valid1Default.db",
        "Válidas Exp1"
    ),
    (
        "validacion_valid2Default.db",
        "Válidas Exp2"
    ),
]


# ============================================================
# LECTOR DE UNA BASE DBCreate
# ============================================================

def leer_dbcreate(archivo, nombre):
    """
    Lee una base de datos creada mediante DBCreate.

    Para cada métrica calcula el promedio de las desviaciones
    estándar almacenadas en las configuraciones.

    Retorna
    -------
    dict
        Estructura normalizada:

        {
            "nombre": nombre,
            "metricas": {
                "exp1_noRev_pct": valor,
                ...
            }
        }
    """

    conn = sqlite3.connect(archivo)
    cursor = conn.cursor()

    resultado = {
        "nombre": nombre,
        "metricas": {},
        "metricas_prom": {}
    }

    try:

        # ----------------------------------------------------
        # Verificar que exista la tabla
        # ----------------------------------------------------

        cursor.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type='table'
            AND name='configuraciones'
            """
        )

        if cursor.fetchone() is None:
            raise ValueError(
                f"La base '{archivo}' no contiene "
                "la tabla 'configuraciones'."
            )

        # ----------------------------------------------------
        # Calcular promedio de cada desviación estándar
        # ----------------------------------------------------

        for nombre_metrica, columna in METRICAS.items():

            cursor.execute(
                f"""
                SELECT AVG("{columna}")
                FROM configuraciones
                """
            )

            promedio = cursor.fetchone()[0]

            if promedio is None:
                raise ValueError(
                    f"No se encontraron datos para "
                    f"la columna '{columna}' "
                    f"en '{archivo}'."
                )

            resultado["metricas"][nombre_metrica] = promedio

        # ----------------------------------------------------
        # Calcular promedio de cada métrica
        # ----------------------------------------------------
        
        for nombre_metrica, columna in METRICAS_PROM.items():
        
            cursor.execute(
                f"""
                SELECT AVG("{columna}")
                FROM configuraciones
                """
            )
        
            promedio = cursor.fetchone()[0]
        
            if promedio is None:
                raise ValueError(
                    f"No se encontraron datos para "
                    f"la columna '{columna}' "
                    f"en '{archivo}'."
                )
        
            resultado["metricas_prom"][nombre_metrica] = promedio

    finally:
        conn.close()

    return resultado


# ============================================================
# LECTOR DE TODAS LAS BASES DBCreate
# ============================================================

def obtener_resultados_dbcreate():
    """
    Lee todas las bases DBCreate configuradas.

    Retorna
    -------
    list
        Lista de resultados normalizados.
    """

    resultados = []

    for archivo, nombre in BASES_DBCREATE:

        resultado = leer_dbcreate(
            archivo,
            nombre
        )

        resultados.append(resultado)

    return resultados


# ============================================================
# MOSTRAR RESULTADOS
# ============================================================

def mostrar_resultados(resultados):

    print("=" * 70)
    print("RESULTADOS LECTOR DBCreate")
    print("=" * 70)

    for resultado in resultados:

        print(f"\n{resultado['nombre']}")
        print("-" * 50)

        for metrica, valor in resultado["metricas"].items():

            print(
                f"{metrica:25s}: "
                f"{valor:.4f}"
            )


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    resultados = obtener_resultados_dbcreate()

    mostrar_resultados(resultados)