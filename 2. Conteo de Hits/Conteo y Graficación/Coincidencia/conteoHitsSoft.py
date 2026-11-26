import sqlite3
import matplotlib.pyplot as plt


# ==========================================================
# RANGOS ESPERADOS
# ==========================================================

RANGOS = {
    "exp1_noRev": (97, 99),
    "exp1_rev": (1, 3),
    "exp2": (50, 58),
    "exp3": (55, 65),
}


# ==========================================================
# EVALUAR HIT
# ==========================================================

def evaluar_hit(promedio, desviacion, minimo, maximo):
    """
    Retorna:
        'directo'
        'asistido'
        'no'
    """


    # Hit directo
    if minimo <= promedio <= maximo:
        return "directo"

    # Hit asistido por desviación estándar
    if promedio < minimo:
        if promedio + desviacion >= minimo:
            return "asistido"

    if promedio > maximo:
        if promedio - desviacion <= maximo:
            return "asistido"

    return "no"


# ==========================================================
# COMBINAR HITS
# ==========================================================

def combinar_hits(*estados):
    """
    Reglas:

    directo + directo = directo

    directo + asistido = asistido

    asistido + asistido = asistido

    cualquier combinación con "no" = no
    """

    if "no" in estados:
        return "no"

    if all(e == "directo" for e in estados):
        return "directo"

    return "asistido"


# ==========================================================
# ANALIZAR BASE
# ==========================================================

def analizar_base(nombre_db):

    conn = sqlite3.connect(nombre_db)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM configuraciones")

    filas = cursor.fetchall()

    columnas = [c[0] for c in cursor.description]

    total = len(filas)

    conteo = {
        "Exp1": {"directo": 0, "asistido": 0},
        "Exp2": {"directo": 0, "asistido": 0},
        "Exp3": {"directo": 0, "asistido": 0},
        "Exp1-2": {"directo": 0, "asistido": 0},
        "Exp1-3": {"directo": 0, "asistido": 0},
        "Exp2-3": {"directo": 0, "asistido": 0},
        "Triple": {"directo": 0, "asistido": 0},
    }

    for fila in filas:

        fila = dict(zip(columnas, fila))

        # ==================================================
        # EXPERIMENTO 1 NO REVERSIBLE
        # ==================================================

        estado_noRev = evaluar_hit(
            fila["exp1_noRev_pct_prom"],
            fila["exp1_noRev_pct_std"],
            RANGOS["exp1_noRev"][0],
            RANGOS["exp1_noRev"][1]
        )

        # ==================================================
        # EXPERIMENTO 1 REVERSIBLE
        # ==================================================

        estado_rev = evaluar_hit(
            fila["exp1_rev_pct_prom"],
            fila["exp1_rev_pct_std"],
            RANGOS["exp1_rev"][0],
            RANGOS["exp1_rev"][1]
        )

        # Exp1 completo = Rev + NoRev

        estado_exp1 = combinar_hits(
            estado_noRev,
            estado_rev
        )

        # ==================================================
        # EXPERIMENTO 2
        # ==================================================

        estado_exp2 = evaluar_hit(
            fila["exp2_pct_prom"],
            fila["exp2_pct_std"],
            RANGOS["exp2"][0],
            RANGOS["exp2"][1]
        )

        # ==================================================
        # EXPERIMENTO 3
        # ==================================================

        estado_exp3 = evaluar_hit(
            fila["exp3_pct_prom"],
            fila["exp3_pct_std"],
            RANGOS["exp3"][0],
            RANGOS["exp3"][1]
        )


###############################################################################                    parte 2

        # ==================================================
        # COMBINACIONES
        # ==================================================

        estado_exp12 = combinar_hits(
            estado_exp1,
            estado_exp2
        )

        estado_exp13 = combinar_hits(
            estado_exp1,
            estado_exp3
        )

        estado_exp23 = combinar_hits(
            estado_exp2,
            estado_exp3
        )

        estado_triple = combinar_hits(
            estado_exp1,
            estado_exp2,
            estado_exp3
        )

        # ==================================================
        # ACTUALIZAR CONTADORES
        # ==================================================

        estados = {
            "Exp1": estado_exp1,
            "Exp2": estado_exp2,
            "Exp3": estado_exp3,
            "Exp1-2": estado_exp12,
            "Exp1-3": estado_exp13,
            "Exp2-3": estado_exp23,
            "Triple": estado_triple
        }

        for nombre, estado in estados.items():

            if estado == "directo":
                conteo[nombre]["directo"] += 1

            elif estado == "asistido":
                conteo[nombre]["asistido"] += 1

    conn.close()

    # ==========================================================
    # RESUMEN EN CONSOLA
    # ==========================================================

    print("\n====================================================")
    print(nombre_db)
    print("====================================================")

    print(f"Total de configuraciones : {total}")

    for categoria in [
        "Exp1",
        "Exp2",
        "Exp3",
        "Exp1-2",
        "Exp1-3",
        "Exp2-3",
        "Triple"
    ]:

        directos = conteo[categoria]["directo"]
        asistidos = conteo[categoria]["asistido"]

        print(
            f"{categoria:8} -> "
            f"Directos: {directos:4d} | "
            f"Asistidos: {asistidos:4d} | "
            f"Total: {directos + asistidos:4d}"
        )

    # ==========================================================
    # DATOS PARA EL GRÁFICO
    # ==========================================================

    categorias = [
        "Total",
        "Exp1",
        "Exp2",
        "Exp3",
        "Exp1-2",
        "Exp1-3",
        "Exp2-3",
        "Triple"
    ]

    directos = [
        total,
        conteo["Exp1"]["directo"],
        conteo["Exp2"]["directo"],
        conteo["Exp3"]["directo"],
        conteo["Exp1-2"]["directo"],
        conteo["Exp1-3"]["directo"],
        conteo["Exp2-3"]["directo"],
        conteo["Triple"]["directo"]
    ]

    asistidos = [
        0,
        conteo["Exp1"]["asistido"],
        conteo["Exp2"]["asistido"],
        conteo["Exp3"]["asistido"],
        conteo["Exp1-2"]["asistido"],
        conteo["Exp1-3"]["asistido"],
        conteo["Exp2-3"]["asistido"],
        conteo["Triple"]["asistido"]
    ]


################################################################################################ parte 3


    # ==========================================================
    # GRÁFICO
    # ==========================================================

    plt.figure(figsize=(11, 6))

    barras_directas = plt.bar(
        categorias,
        directos,
        label="Hits directos"
    )

    barras_asistidas = plt.bar(
        categorias,
        asistidos,
        bottom=directos,
        label="Hits asistidos"
    )

    # ----------------------------------------------------------
    # Número sobre cada barra
    # ----------------------------------------------------------

    for i in range(len(categorias)):

        total_barra = directos[i] + asistidos[i]

        # Número de hits directos
        if directos[i] > 0:

            plt.text(
                i,
                directos[i],
                str(directos[i]),
                ha="center",
                va="bottom",
                fontsize=9
            )

        # Número total (directos + asistidos)

        if asistidos[i] > 0:

            plt.text(
                i,
                total_barra,
                str(total_barra),
                ha="center",
                va="bottom",
                fontsize=10,
                fontweight="bold"
            )

    # ----------------------------------------------------------
    # Aspecto del gráfico
    # ----------------------------------------------------------

    plt.title(nombre_db.replace(".db", ""))

    plt.ylabel("Número de configuraciones")

    plt.legend()

    ymax = max(
        directos[i] + asistidos[i]
        for i in range(len(categorias))
    )

    plt.ylim(0, ymax * 1.12 if ymax > 0 else 1)

    plt.grid(axis="y", alpha=0.3)

    plt.tight_layout()

    plt.savefig(
        nombre_db.replace(".db", "_SoftResumen.png"),
        dpi=300
    )

    plt.close()


##############################################################################                     parte 4

# ==========================================================
# MAIN
# ==========================================================

if __name__ == "__main__":

    bases = [

        # -------------------------
        # Pareto Default
        # -------------------------
        "validacion_pareto1Default.db",
        "validacion_pareto2Default.db",
        "validacion_pareto3Default.db",

        # -------------------------
        # Validación Default
        # -------------------------
        "validacion_valid1Default.db",
        "validacion_valid2Default.db",
        "validacion_valid3Default.db",

    ]

    print("\n")
    print("==============================================")
    print("        CONTEO DE HITS (SOFT)")
    print("==============================================")

    for base in bases:

        try:

            analizar_base(base)

        except FileNotFoundError:

            print(f"\nNo se encontró la base: {base}")

        except sqlite3.Error as e:

            print(f"\nError en {base}")
            print(e)

    print("\n==============================================")
    print("Análisis finalizado.")
    print("==============================================")