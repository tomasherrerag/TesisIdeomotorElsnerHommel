import sqlite3
import os


BASES = [
    "TransferDefault11.db",
    "TransferDefault21.db",
    "TransferDefault31.db",
    "TransferDefault12.db",
    "TransferDefault22.db",
    "TransferDefault32.db",
    "TransferDefault13.db",
    "TransferDefault23.db",
    "TransferDefault33.db",
]


def obtener_tablas(cursor):
    cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type='table'
        AND name NOT LIKE 'sqlite_%'
        ORDER BY name
    """)
    return [fila[0] for fila in cursor.fetchall()]


def escanear_base(nombre_base):
    print("\n" + "=" * 80)
    print(f"BASE DE DATOS: {nombre_base}")
    print("=" * 80)

    if not os.path.exists(nombre_base):
        print("⚠️  ARCHIVO NO ENCONTRADO")
        return None

    try:
        conexion = sqlite3.connect(nombre_base)
        cursor = conexion.cursor()

        tablas = obtener_tablas(cursor)

        if not tablas:
            print("⚠️  No se encontraron tablas.")
            conexion.close()
            return {}

        estructura = {}

        print(f"\nTablas encontradas: {len(tablas)}")

        for tabla in tablas:
            print("\n" + "-" * 60)
            print(f"TABLA: {tabla}")
            print("-" * 60)

            cursor.execute(f'PRAGMA table_info("{tabla}")')
            columnas = cursor.fetchall()

            estructura[tabla] = [columna[1] for columna in columnas]

            print("\nColumnas:")

            for columna in columnas:
                cid, nombre, tipo, notnull, default, pk = columna

                detalles = f"    {nombre}"

                if tipo:
                    detalles += f" ({tipo})"

                if pk:
                    detalles += " [PRIMARY KEY]"

                if notnull:
                    detalles += " [NOT NULL]"

                if default is not None:
                    detalles += f" [DEFAULT={default}]"

                print(detalles)

            cursor.execute(f'SELECT COUNT(*) FROM "{tabla}"')
            cantidad = cursor.fetchone()[0]

            print(f"\nCantidad de registros: {cantidad}")

            # Mostrar hasta 3 registros de ejemplo
            if cantidad > 0:
                cursor.execute(f'SELECT * FROM "{tabla}" LIMIT 3')
                ejemplos = cursor.fetchall()

                nombres_columnas = [columna[1] for columna in columnas]

                print("\nEjemplos:")

                for registro in ejemplos:
                    print(dict(zip(nombres_columnas, registro)))

        conexion.close()

        return estructura

    except sqlite3.Error as error:
        print(f"❌ Error SQLite: {error}")
        return None


def comparar_estructuras(resultados):
    print("\n\n" + "=" * 80)
    print("COMPARACIÓN DE ESTRUCTURAS")
    print("=" * 80)

    validos = {
        nombre: estructura
        for nombre, estructura in resultados.items()
        if estructura is not None
    }

    if not validos:
        print("\nNo hay bases válidas para comparar.")
        return

    # Obtener todas las tablas presentes
    todas_las_tablas = set()

    for estructura in validos.values():
        todas_las_tablas.update(estructura.keys())

    for tabla in sorted(todas_las_tablas):

        print("\n" + "-" * 60)
        print(f"TABLA: {tabla}")
        print("-" * 60)

        referencia = None
        nombre_referencia = None
        iguales = True

        for nombre, estructura in validos.items():

            columnas = estructura.get(tabla)

            if columnas is None:
                print(f"  {nombre}: ⚠️ tabla no encontrada")
                iguales = False
                continue

            print(f"  {nombre}: {columnas}")

            if referencia is None:
                referencia = columnas
                nombre_referencia = nombre
            elif columnas != referencia:
                iguales = False

        if iguales:
            print("\n  ✓ Todas las bases tienen la misma estructura.")
        else:
            print("\n  ⚠️ Las estructuras NO son idénticas.")


def main():

    print("=" * 80)
    print("SCANNER DE BASES TRANSFERDEFAULT")
    print("=" * 80)

    resultados = {}

    for nombre_base in BASES:
        resultados[nombre_base] = escanear_base(nombre_base)

    comparar_estructuras(resultados)

    print("\n" + "=" * 80)
    print("ESCANEO FINALIZADO")
    print("=" * 80)


if __name__ == "__main__":
    main()