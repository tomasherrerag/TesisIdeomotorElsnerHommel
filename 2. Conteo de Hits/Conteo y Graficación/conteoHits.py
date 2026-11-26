import sqlite3
import matplotlib.pyplot as plt


def analizar_base(nombre_db):

    conn = sqlite3.connect(nombre_db)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    print(cursor.fetchall())

    cursor.execute("SELECT * FROM configuraciones LIMIT 1")
    print(cursor.fetchone())

    cursor.execute("PRAGMA table_info(configuraciones)")
    print(cursor.fetchall())


    # Total de configuraciones
    cursor.execute("SELECT COUNT(*) FROM configuraciones")
    total = cursor.fetchone()[0]

    # Exp1 No Reversible
    cursor.execute("""
    SELECT COUNT(*)
    FROM configuraciones
    WHERE exp1_noRev_pct_prom BETWEEN 97 AND 99
      AND exp1_noRev_skip_prom <= 1
    """)
    exp1_noRev = cursor.fetchone()[0]

    # Exp1 Reversible
    cursor.execute("""
    SELECT COUNT(*)
    FROM configuraciones
    WHERE exp1_rev_pct_prom BETWEEN 1 AND 3
      AND exp1_rev_skip_prom <= 1
    """)
    exp1_rev = cursor.fetchone()[0]

    # Exp2
    cursor.execute("""
    SELECT COUNT(*)
    FROM configuraciones
    WHERE exp2_pct_prom BETWEEN 50 AND 58
      AND exp2_skip_prom <= 1
    """)
    exp2 = cursor.fetchone()[0]

    # Exp3
    cursor.execute("""
    SELECT COUNT(*)
    FROM configuraciones
    WHERE exp3_pct_prom BETWEEN 55 AND 65
      AND exp3_skipMalo_prom <= 1
    """)
    exp3 = cursor.fetchone()[0]

    # Cumplen experimentos 1 y 2
    cursor.execute("""
    SELECT COUNT(*)
    FROM configuraciones
    WHERE exp1_noRev_pct_prom BETWEEN 97 AND 99
      AND exp1_noRev_skip_prom <= 1

      AND exp1_rev_pct_prom BETWEEN 1 AND 3
      AND exp1_rev_skip_prom <= 1

      AND exp2_pct_prom BETWEEN 50 AND 58
      AND exp2_skip_prom <= 1
    """)
    exp12 = cursor.fetchone()[0]


    # Cumplen experimentos 1 y 3
    cursor.execute("""
    SELECT COUNT(*)
    FROM configuraciones
    WHERE exp1_noRev_pct_prom BETWEEN 97 AND 99
      AND exp1_noRev_skip_prom <= 1

      AND exp1_rev_pct_prom BETWEEN 1 AND 3
      AND exp1_rev_skip_prom <= 1

      AND exp3_pct_prom BETWEEN 55 AND 65
      AND exp3_skipMalo_prom <= 1
    """)
    exp13 = cursor.fetchone()[0]


    # Cumplen experimentos 2 y 3
    cursor.execute("""
    SELECT COUNT(*)
    FROM configuraciones
    WHERE exp2_pct_prom BETWEEN 50 AND 58
      AND exp2_skip_prom <= 1

      AND exp3_pct_prom BETWEEN 55 AND 65
      AND exp3_skipMalo_prom <= 1
    """)
    exp23 = cursor.fetchone()[0]


    # Cumplen todos los experimentos
    cursor.execute("""
    SELECT COUNT(*)
    FROM configuraciones
    WHERE exp1_noRev_pct_prom BETWEEN 97 AND 99
      AND exp1_noRev_skip_prom <= 1

      AND exp1_rev_pct_prom BETWEEN 1 AND 3
      AND exp1_rev_skip_prom <= 1

      AND exp2_pct_prom BETWEEN 50 AND 58
      AND exp2_skip_prom <= 1

      AND exp3_pct_prom BETWEEN 55 AND 65
      AND exp3_skipMalo_prom <= 1
    """)
    todos = cursor.fetchone()[0]

    conn.close()

    print(f"\n===== {nombre_db} =====")
    print(f"Total de configuraciones : {total}")
    print(f"Cumplen Exp1 No Rev      : {exp1_noRev}")
    print(f"Cumplen Exp1 Rev         : {exp1_rev}")
    print(f"Cumplen Exp2             : {exp2}")
    print(f"Cumplen Exp3             : {exp3}")
    print(f"Cumplen Exp 1 y 2        : {exp12}")
    print(f"Cumplen Exp 1 y 3        : {exp13}")
    print(f"Cumplen Exp 2 y 3        : {exp23}")
    print(f"Cumplen TODOS            : {todos}")

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

    valores = [
        total,
        exp1_noRev,   # o el criterio que quieras considerar para Exp1
        exp2,
        exp3,
        exp12,
        exp13,
        exp23,
        todos
    ]

    plt.figure(figsize=(10, 5))

    barras = plt.bar(categorias, valores)

    # Agregar el valor encima de cada barra
    for barra in barras:
        altura = barra.get_height()
        plt.text(
            barra.get_x() + barra.get_width() / 2,
            altura,
            f"{int(altura)}",
            ha="center",
            va="bottom",
            fontsize=10
        )

    plt.title(nombre_db)
    plt.ylabel("Número de configuraciones")

    # Deja un pequeño espacio arriba para que no se corten los números
    plt.ylim(0, max(valores) * 1.1 if max(valores) > 0 else 1)

    plt.tight_layout()

    plt.savefig(nombre_db.replace(".db", "_resumen.png"), dpi=300)
    plt.close()


if __name__ == "__main__":

    analizar_base("validacion_pareto1Default.db")
    analizar_base("validacion_pareto2Default.db")
    analizar_base("validacion_pareto3Default.db")
    analizar_base("validacion_valid1Default.db")
    analizar_base("validacion_valid2Default.db")
    analizar_base("validacion_valid3Default.db")