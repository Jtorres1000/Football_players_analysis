import duckdb
from pathlib import Path

def main():

    # SI USAN ESTE ARCHIVO PARA GENERAR LOS PARQUETS CAMBIEN ESTA RUTA POR LA RUTA BASE DE SU PC.

    BASE_DIR = Path(r"C:\Users\Usuario\Documents\jtorres stuff\UCV\2do SEMESTRE\COMPUTACIÓN II\Football_players_analysis")
    
    # Corrijan el nombre del archivo aquí si es necesario
    ruta_db = BASE_DIR / "data" / "raw" / "sqlpractice.sqlite"
    carpeta_salida = BASE_DIR / "data" / "raw" / "parquets"
    
    carpeta_salida.mkdir(parents=True, exist_ok=True)

    if not ruta_db.exists():
        print(f"No se pudo encontrar la base de datos. {ruta_db}")
        return

    print("Iniciando la conexión con DuckDB...")
    con = duckdb.connect()
    
    con.execute("INSTALL sqlite;")
    con.execute("LOAD sqlite;")
    
    print(f"Conectando a la base de datos: {ruta_db.name}\n")
    con.execute(f"ATTACH '{ruta_db.as_posix()}' AS mi_db (TYPE sqlite);")

    tablas = con.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_catalog = 'mi_db'
    """).fetchall()

    if not tablas:
        print("No se encontraron tablas en la base de datos.")
        return

    hubo_errores = False
    tablas_con_error = []
    
    print(f"Comenzando la exportación de {len(tablas)} tabla(s)...")
    print("-" * 50)

    for tabla in tablas:
        nombre_tabla = tabla[0]

        archivo_parquet = carpeta_salida / f"{nombre_tabla}_raw.parquet"
        
        try:

            con.execute(f"COPY mi_db.{nombre_tabla} TO '{archivo_parquet.as_posix()}' (FORMAT PARQUET);")
            print(f"{nombre_tabla} -> {archivo_parquet.name}")
            
        except Exception as e:
            hubo_errores = True
            tablas_con_error.append(nombre_tabla)
            print(f"Error en la tabla:'{nombre_tabla}': {e}")


    print("\n" + "-" * 50)
    print("RESUMEN DE LA EXPORTACIÓN")
    print("-" * 50)
    
    if hubo_errores:
        print(f"Proceso finalizado con errores en {len(tablas_con_error)} tabla(s).")
        print(f"Tablas con errores: {', '.join(tablas_con_error)}")
    else:
        print(f"Se exportaron {len(tablas)} tablas a parquet sin problemas.")
        print(f"Ruta de salida: {carpeta_salida}")

if __name__ == "__main__":
    main()