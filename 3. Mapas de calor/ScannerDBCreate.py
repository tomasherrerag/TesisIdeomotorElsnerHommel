import sqlite3
import os


# ============================================================
# CONFIGURACIÓN
# ============================================================

BASES = [
    ("Pareto Exp1", "validacion_pareto1Default.db"),
    ("Pareto Exp2", "validacion_pareto2Default.db"),
    ("Pareto Exp3", "validacion_pareto3Default.db"),
    ("Válidas Exp1", "validacion_valid1Default.db"),
    ("Válidas Exp2", "validacion_valid2Default.db"),
]


# Columnas que queremos utilizar para el heatmap
COLUMNAS_STD = [
    "exp1_noRev_pct_std",
    "exp1_rev_pct_std",
    "exp1_noRev_skip_std",
    "exp1_rev_skip_std",
    "exp2_pct_std",
    "exp2_skip_std",
    "exp3_pct_std",
    "exp3_skipMalo_std",
    "exp3_skipRespondido_std",
]


# ============================================================
# FUNCIONES
# ============================================================

def escanear_base(nombre, archivo):
    print("=" * 70)
    print(f"BASE: {nombre}")
    print(f"ARCHIVO: {archivo}")
    print("=" * 70)

    # --------------------------------------------------------
    # Comprobar existencia
    # --------------------------------------------------------

    if not os.path.exists(archivo):
        print("ERROR: El archivo no existe.")
        print()
        return

    print(f"Tamaño: {os.path.getsize(archivo):,} bytes")

    # --------------------------------------------------------
    # Conexión
    # --------------------------------------------------------

    try:
        conn = sqlite3.connect(archivo)
        cursor = conn.cursor()
    except sqlite3.Error as e:
        print(f"ERROR al abrir la base: {e}")
        print()
        return

    # --------------------------------------------------------
    # Tablas
    # --------------------------------------------------------

    try:
        cursor.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type='table'
            ORDER BY name
            """
        )

        tablas = [fila[0] for fila in cursor.fetchall()]

        print("\nTablas encontradas:")

        if tablas:
            for tabla in tablas:
                print(f"  - {tabla}")
        else:
            print("  No se encontraron tablas.")

        if "configuraciones" not in tablas:
            print("\nERROR: No existe la tabla 'configuraciones'.")
            conn.close()
            print()
            return

    except sqlite3.Error as e:
        print(f"ERROR al consultar las tablas: {e}")
        conn.close()
        print()
        return

    # --------------------------------------------------------
    # Información de columnas
    # --------------------------------------------------------

    try:
        cursor.execute("PRAGMA table_info(configuraciones)")
        columnas_info = cursor.fetchall()

        columnas = [fila[1] for fila in columnas_info]

        print("\nNúmero de columnas:", len(columnas))
        print("Número de filas:", end=" ")

        cursor.execute("SELECT COUNT(*) FROM configuraciones")
        cantidad_filas = cursor.fetchone()[0]

        print(cantidad_filas)

    except sqlite3.Error as e:
        print(f"\nERROR al consultar la estructura: {e}")
        conn.close()
        print()
        return

    # --------------------------------------------------------
    # Columnas relevantes
    # --------------------------------------------------------

    print("\nColumnas STD requeridas:")

    columnas_faltantes = []

    for columna in COLUMNAS_STD:

        if columna in columnas:
            print(f"  [OK]      {columna}")
        else:
            print(f"  [FALTANTE] {columna}")
            columnas_faltantes.append(columna)

    # --------------------------------------------------------
    # Revisar NULL
    # --------------------------------------------------------

    print("\nValores NULL en columnas STD:")

    for columna in COLUMNAS_STD:

        if columna not in columnas:
            continue

        try:
            cursor.execute(
                f"""
                SELECT COUNT(*)
                FROM configuraciones
                WHERE "{columna}" IS NULL
                """
            )

            cantidad_null = cursor.fetchone()[0]

            if cantidad_null == 0:
                print(f"  [OK] {columna}: 0 NULL")
            else:
                print(
                    f"  [AVISO] {columna}: "
                    f"{cantidad_null} NULL"
                )

        except sqlite3.Error as e:
            print(f"  [ERROR] {columna}: {e}")

    # --------------------------------------------------------
    # Estadísticas básicas
    # --------------------------------------------------------

    print("\nRango de valores de las columnas STD:")

    for columna in COLUMNAS_STD:

        if columna not in columnas:
            continue

        try:
            cursor.execute(
                f"""
                SELECT
                    MIN("{columna}"),
                    MAX("{columna}"),
                    AVG("{columna}")
                FROM configuraciones
                """
            )

            minimo, maximo, promedio = cursor.fetchone()

            print(
                f"  {columna}: "
                f"min={minimo}, "
                f"max={maximo}, "
                f"avg={promedio}"
            )

        except sqlite3.Error as e:
            print(f"  [ERROR] {columna}: {e}")

    # --------------------------------------------------------
    # Resultado general
    # --------------------------------------------------------

    print("\nResumen:")

    if columnas_faltantes:
        print("  RESULTADO: HAY COLUMNAS FALTANTES")
    else:
        print("  RESULTADO: Todas las columnas requeridas están presentes")

    print()

    conn.close()


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    print("\n")
    print("=" * 70)
    print("SCANNER DE BASES DBCreate")
    print("=" * 70)
    print()

    for nombre, archivo in BASES:
        escanear_base(nombre, archivo)

    print("=" * 70)
    print("SCANNER FINALIZADO")
    print("=" * 70)