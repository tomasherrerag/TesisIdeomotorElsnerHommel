import sqlite3


DB = "validacion_pareto1Default.db"
# Cambiar por la base que quieras revisar


def imprimir_fila(cursor, fila):

    columnas = [c[0] for c in cursor.description]

    for nombre, valor in zip(columnas, fila):
        print(f"{nombre:35} {repr(valor)}")


conn = sqlite3.connect(DB)
cursor = conn.cursor()


# ==========================================================
# Tablas
# ==========================================================

print("=" * 80)
print("TABLAS")
print("=" * 80)

cursor.execute("""
SELECT name
FROM sqlite_master
WHERE type='table'
ORDER BY name
""")

tablas = [t[0] for t in cursor.fetchall()]

for tabla in tablas:
    print("-", tabla)


# ==========================================================
# Estructura de cada tabla
# ==========================================================

for tabla in tablas:

    print()
    print("=" * 80)
    print(tabla)
    print("=" * 80)

    cursor.execute(f"PRAGMA table_info({tabla})")

    columnas = cursor.fetchall()

    print()
    print("Columnas:")

    for col in columnas:

        print(f"{col[1]:35} {col[2]}")


# ==========================================================
# Cantidad de filas
# ==========================================================

print()
print("=" * 80)
print("CANTIDAD DE FILAS")
print("=" * 80)

for tabla in tablas:

    cursor.execute(f"SELECT COUNT(*) FROM {tabla}")

    n = cursor.fetchone()[0]

    print(f"{tabla:35} {n}")


# ==========================================================
# Primeras filas de configuraciones
# ==========================================================

if "configuraciones" in tablas:

    print()
    print("=" * 80)
    print("PRIMERAS 3 FILAS")
    print("=" * 80)

    cursor.execute("""
    SELECT *
    FROM configuraciones
    LIMIT 3
    """)

    filas = cursor.fetchall()

    for i, fila in enumerate(filas, start=1):

        print()
        print("-" * 80)
        print(f"FILA {i}")
        print("-" * 80)

        imprimir_fila(cursor, fila)


# ==========================================================
# Estadísticas rápidas
# ==========================================================

if "configuraciones" in tablas:

    print()
    print("=" * 80)
    print("RANGOS NUMÉRICOS")
    print("=" * 80)

    cursor.execute("PRAGMA table_info(configuraciones)")

    columnas = cursor.fetchall()

    for col in columnas:

        nombre = col[1]
        tipo = col[2].upper()

        if tipo in ("REAL", "INTEGER", "FLOAT"):

            try:

                cursor.execute(f"""
                SELECT
                    MIN({nombre}),
                    MAX({nombre})
                FROM configuraciones
                """)

                minimo, maximo = cursor.fetchone()

                print(f"{nombre:35} {minimo} -> {maximo}")

            except Exception:
                pass


conn.close()