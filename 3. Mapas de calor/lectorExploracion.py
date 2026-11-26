import optuna
import os


# ============================================================
# CONFIGURACIÓN
# ============================================================

DB_EXP1_REV = "exp1Default.db"
DB_EXP1_NOREV = "exp1NoRevDefault.db"   # Todavía no existe
DB_EXP2 = "exp2Default.db"
DB_EXP3 = "exp3Default.db"

STUDY_EXP1 = "exp1Default"
STUDY_EXP2 = "exp2Default"
STUDY_EXP3 = "exp3Default"
STUDY_EXP1_NOREV = "exp1DefaultNoRev"


# ============================================================
# FUNCIONES AUXILIARES
# ============================================================

def cargar_study(ruta_db, nombre_study):
    """
    Carga un estudio Optuna desde una base SQLite.
    """

    if not os.path.exists(ruta_db):
        print(f"[AVISO] No existe la base: {ruta_db}")
        return None

    try:
        study = optuna.load_study(
            study_name=nombre_study,
            storage=f"sqlite:///{ruta_db}"
        )

        print(
            f"[OK] {ruta_db} -> "
            f"{len(study.trials)} trials"
        )

        return study

    except Exception as e:
        print(f"[ERROR] No se pudo cargar {ruta_db}")
        print(f"        {e}")
        return None


def promedio_atributo(study, atributo):
    """
    Calcula el promedio de un user_attr entre todos los trials
    que poseen dicho atributo.

    Los valores None o ausentes se ignoran.
    """

    if study is None:
        return None

    valores = []

    for trial in study.trials:

        valor = trial.user_attrs.get(atributo)

        if valor is not None:
            valores.append(valor)

    if not valores:
        return None

    return sum(valores) / len(valores)


# ============================================================
# EXPERIMENTO 1
# ============================================================

def leer_exp1():

    print("\n" + "=" * 60)
    print("LEYENDO EXPERIMENTO 1")
    print("=" * 60)

    # --------------------------------------------------------
    # EXP1 REVERSIBLE
    #
    # La base original contiene los resultados REV, aunque
    # históricamente los atributos hayan tenido nombres noRev.
    # Actualmente, según el código corregido, utilizamos
    # exp1_Rev_*.
    # --------------------------------------------------------

    study_rev = cargar_study(
        DB_EXP1_REV,
        STUDY_EXP1
    )

    resultado = {}

    # --------------------------------------------------------
    # DESVIACIONES - EXP1 REVERSIBLE
    # --------------------------------------------------------

    resultado["exp1_rev_pct"] = promedio_atributo(
        study_rev,
        "exp1_noRev_coincidencia_desviacion"
    )

    resultado["exp1_rev_skip"] = promedio_atributo(
        study_rev,
        "exp1_noRev_skips_desviacion"
    )

    # --------------------------------------------------------
    # PROMEDIOS - EXP1 REVERSIBLE
    # --------------------------------------------------------

    resultado["exp1_rev_pct_prom"] = promedio_atributo(
        study_rev,
        "exp1_noRev_coincidencia_promedio"
    )

    resultado["exp1_rev_skip_prom"] = promedio_atributo(
        study_rev,
        "exp1_noRev_skips_promedio"
    )

    # --------------------------------------------------------
    # EXP1 NO REVERSIBLE
    #
    # Esta base todavía no ha sido generada.
    # --------------------------------------------------------

    study_norev = cargar_study(
        DB_EXP1_NOREV,
        STUDY_EXP1_NOREV
    )

    # --------------------------------------------------------
    # DESVIACIONES - EXP1 NO REVERSIBLE
    # --------------------------------------------------------

    resultado["exp1_noRev_pct"] = promedio_atributo(
        study_norev,
        "exp1_noRev_coincidencia_desviacion"
    )

    resultado["exp1_noRev_skip"] = promedio_atributo(
        study_norev,
        "exp1_noRev_skips_desviacion"
    )

    # --------------------------------------------------------
    # PROMEDIOS - EXP1 NO REVERSIBLE
    # --------------------------------------------------------

    resultado["exp1_noRev_pct_prom"] = promedio_atributo(
        study_norev,
        "exp1_noRev_coincidencia_promedio"
    )

    resultado["exp1_noRev_skip_prom"] = promedio_atributo(
        study_norev,
        "exp1_noRev_skips_promedio"
    )

    return resultado


# ============================================================
# EXPERIMENTO 2
# ============================================================

def leer_exp2():

    print("\n" + "=" * 60)
    print("LEYENDO EXPERIMENTO 2")
    print("=" * 60)

    study = cargar_study(
        DB_EXP2,
        STUDY_EXP2
    )

    resultado = {}

    # --------------------------------------------------------
    # DESVIACIONES
    # --------------------------------------------------------

    resultado["exp2_pct"] = promedio_atributo(
        study,
        "exp2_coincidencia_desviacion"
    )

    resultado["exp2_skip"] = promedio_atributo(
        study,
        "exp2_skips_desviacion"
    )

    # --------------------------------------------------------
    # PROMEDIOS
    # --------------------------------------------------------

    resultado["exp2_pct_prom"] = promedio_atributo(
        study,
        "exp2_coincidencia_promedio"
    )

    resultado["exp2_skip_prom"] = promedio_atributo(
        study,
        "exp2_skips_promedio"
    )

    return resultado


# ============================================================
# EXPERIMENTO 3
# ============================================================

def leer_exp3():

    print("\n" + "=" * 60)
    print("LEYENDO EXPERIMENTO 3")
    print("=" * 60)

    study = cargar_study(
        DB_EXP3,
        STUDY_EXP3
    )

    resultado = {}

    # --------------------------------------------------------
    # DESVIACIONES
    # --------------------------------------------------------

    resultado["exp3_pct"] = promedio_atributo(
        study,
        "exp3_coincidencia_desviacion"
    )

    resultado["exp3_skipMalo"] = promedio_atributo(
        study,
        "exp3_skipsMalos_desviacion"
    )

    resultado["exp3_skipRespondido"] = promedio_atributo(
        study,
        "exp3_skipsRespondidos_desviacion"
    )

    # skipBueno se excluye deliberadamente

    # --------------------------------------------------------
    # PROMEDIOS
    # --------------------------------------------------------

    resultado["exp3_pct_prom"] = promedio_atributo(
        study,
        "exp3_coincidencia_promedio"
    )

    resultado["exp3_skipMalo_prom"] = promedio_atributo(
        study,
        "exp3_skipsMalos_promedio"
    )

    resultado["exp3_skipRespondido_prom"] = promedio_atributo(
        study,
        "exp3_skipsRespondidos_promedio"
    )

    # skipBueno se excluye deliberadamente

    return resultado


# ============================================================
# RESULTADO FINAL
# ============================================================

def obtener_resultado_exploracion():

    exp1 = leer_exp1()
    exp2 = leer_exp2()
    exp3 = leer_exp3()

    resultado = {
        "nombre": "Exploración",

        # ----------------------------------------------------
        # DESVIACIONES
        # ----------------------------------------------------

        "metricas": {

            "exp1_noRev_pct":
                exp1["exp1_noRev_pct"],

            "exp1_rev_pct":
                exp1["exp1_rev_pct"],

            "exp1_noRev_skip":
                exp1["exp1_noRev_skip"],

            "exp1_rev_skip":
                exp1["exp1_rev_skip"],

            "exp2_pct":
                exp2["exp2_pct"],

            "exp2_skip":
                exp2["exp2_skip"],

            "exp3_pct":
                exp3["exp3_pct"],

            "exp3_skipMalo":
                exp3["exp3_skipMalo"],

            "exp3_skipRespondido":
                exp3["exp3_skipRespondido"]
        },

        # ----------------------------------------------------
        # PROMEDIOS
        # ----------------------------------------------------

        "metricas_prom": {

            "exp1_noRev_pct":
                exp1["exp1_noRev_pct_prom"],

            "exp1_rev_pct":
                exp1["exp1_rev_pct_prom"],

            "exp1_noRev_skip":
                exp1["exp1_noRev_skip_prom"],

            "exp1_rev_skip":
                exp1["exp1_rev_skip_prom"],

            "exp2_pct":
                exp2["exp2_pct_prom"],

            "exp2_skip":
                exp2["exp2_skip_prom"],

            "exp3_pct":
                exp3["exp3_pct_prom"],

            "exp3_skipMalo":
                exp3["exp3_skipMalo_prom"],

            "exp3_skipRespondido":
                exp3["exp3_skipRespondido_prom"]
        }
    }

    return resultado


# ============================================================
# MOSTRAR RESULTADO
# ============================================================

def mostrar_resultado(resultado):

    print("\n")
    print("#" * 60)
    print("RESULTADOS LECTOR EXPLORACIÓN")
    print("#" * 60)

    print(f"\n## {resultado['nombre']}\n")

    print("DESVIACIONES:")
    print("-" * 60)

    for nombre, valor in resultado["metricas"].items():

        if valor is None:
            texto = "PENDIENTE"

        else:
            texto = f"{valor:.4f}"

        print(f"{nombre:<25}: {texto}")

    print("\nPROMEDIOS:")
    print("-" * 60)

    for nombre, valor in resultado["metricas_prom"].items():

        if valor is None:
            texto = "PENDIENTE"

        else:
            texto = f"{valor:.4f}"

        print(f"{nombre:<25}: {texto}")


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    resultado = obtener_resultado_exploracion()

    mostrar_resultado(resultado)