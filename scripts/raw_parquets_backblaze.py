import duckdb
import streamlit as st
from pathlib import Path


def main():

    
    BASE_DIR = Path(r"C:\Users\Usuario\Documents\jtorres stuff\UCV\2do SEMESTRE\COMPUTACIÓN II\Football_players_analysis")
    
   
    ruta_db = BASE_DIR / "data" / "raw" / "sqlpractice.sqlite"


    B2_KEY_ID = st.secrets['connections']['backblaze']['B2_KEY_ID']
    B2_KEY_NAME = st.secrets['connections']['backblaze']['B2_KEY_NAME']
    B2_APPLICATION_KEY = st.secrets['connections']['backblaze']['B2_APPLICATION_KEY']
    B2_BUCKET_NAME = st.secrets['connections']['backblaze']['B2_BUCKET_NAME']
    B2_ENDPOINT = st.secrets['connections']['backblaze']['B2_ENDPOINT']
    B2_REGION = st.secrets['connections']['backblaze']['B2_REGION']

    if not ruta_db.exists():
        print(f"No se pudo encontrar la base de datos: {ruta_db}")
        return

    print("Iniciando la conexión con DuckDB...")
    con = duckdb.connect()
    
    # Instalar y cargar extensiones necesarias sqlite para leer la bd y httpfs para cargarlos en backblaze
    con.execute("INSTALL sqlite;")
    con.execute("LOAD sqlite;")
    con.execute("INSTALL httpfs;")
    con.execute("LOAD httpfs;")

    # Configurar credenciales para backblaze en duckdb
    con.execute(f"""
        CREATE SECRET backblaze_b2 (
            TYPE S3,
            KEY_ID '{B2_KEY_ID}',
            SECRET '{B2_APPLICATION_KEY}',
            REGION '{B2_REGION}',
            ENDPOINT '{B2_ENDPOINT}',
            URL_STYLE 'path'
        );
    """)
    
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
    
    print(f"Comenzando la exportación de {len(tablas)} tablas al bucket '{B2_BUCKET_NAME}'...")
    print("-" * 50)

    for tabla in tablas:
        nombre_tabla = tabla[0]
        nombre_archivo = f"{nombre_tabla}.parquet"
        ruta_s3 = f"s3://{B2_BUCKET_NAME}/{nombre_archivo}"
        
        try:
            con.execute(f"COPY mi_db.{nombre_tabla} TO '{ruta_s3}' (FORMAT PARQUET);")
            print(f"{nombre_tabla} -> {ruta_s3}")
            
        except Exception as e:
            hubo_errores = True
            tablas_con_error.append(nombre_tabla)
            print(f"Error en la tabla '{nombre_tabla}': {e}")

    print("\n" + "-" * 50)
    print("RESUMEN DE LA EXPORTACIÓN A BACKBLAZE B2")
    print("-" * 50)
    
    if hubo_errores:
        print(f"Proceso finalizado con errores en {len(tablas_con_error)} tablas.")
        print(f"Tablas con errores: {', '.join(tablas_con_error)}")
    else:
        print(f"Se exportaron {len(tablas)} tablas a backblaze B2 sin problemas.")

if __name__ == "__main__":
    main()

