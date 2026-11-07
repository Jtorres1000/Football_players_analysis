from pathlib import Path
import duckdb
import pandas as pd
import streamlit as st

LOCAL_DUCKDB_PATH = Path(__file__).resolve().parents[2] / "data" / "football_local.duckdb"

B2_TABLES: list[str] = [
    "agents",
    "clubs",
    "contracts",
    "divisions",
    "injuries",
    "nations",
    "player_positions",
    "player_seasons",
    "player_stats_attacking",
    "player_stats_defending",
    "player_stats_general",
    "player_stats_goalkeeping",
    "player_stats_passing",
    "players",
    "positions",
    "seasons",
    "transfers",
]

# Mapeos entre las etiquetas de la sidebar a  los valores en Snowflake
SEASON_MAP: dict[str, str] = {
    "2025-2026": "2025/26",
    "2024-2025": "2024/25",
    "2023-2024": "2023/24",
    "2022-2023": "2022/23",
}

POSITION_MAP: dict[str, str] = {
    "Delanteros (ATT)": "ATTACKER",
    "Centrocampistas (MID)": "MIDFIELDER",
    "Defensas (DEF)": "DEFENDER",
    "Porteros (GK)": "GOALKEEPER",
}

AGE_GROUP_MAP: dict[str, str] = {
    "15–21": "15-21",
    "22–26": "22-26",
    "27–31": "27-31",
    "32–38": "32-38",
    "15-21": "15-21",
    "22-26": "22-26",
    "27-31": "27-31",
    "32-38": "32-38",
}

# Query principal que une y trae todo el modelado dimensional.
MART_BASE_QUERY = """
SELECT
    p.player_id AS PLAYER_ID,
    p.name AS NAME,
    p.primary_category AS PRIMARY_CATEGORY,
    p.primary_role_code AS PRIMARY_ROLE_CODE,
    p.primary_side_code AS PRIMARY_SIDE_CODE,
    s.season_id AS SEASON_ID,
    s.season_label AS SEASON_LABEL,
    a.age AS AGE,
    a.age_group AS AGE_GROUP,
    c.club_id AS CLUB_ID,
    c.club_name AS CLUB_NAME,
    c.division_name AS DIVISION_NAME,
    f.ability_score AS ABILITY_SCORE,
    f.ability_score_delta AS ABILITY_SCORE_DELTA,
    f.weekly_wage_eur AS WEEKLY_WAGE_EUR,
    f.annual_wage_eur AS ANNUAL_WAGE_EUR,
    f.goals AS GOALS,
    f.dribbles_made AS DRIBBLES_MADE,
    f.tackles_completed AS TACKLES_COMPLETED,
    f.save_ratio AS SAVE_RATIO,
    f.chances_created AS CHANCES_CREATED,
    f.passes_completed AS PASSES_COMPLETED
FROM FACT_PLAYER_SEASON f
INNER JOIN DIM_PLAYER p
    ON f.player_key = p.player_key
INNER JOIN DIM_SEASON s
    ON f.season_key = s.season_key
INNER JOIN DIM_AGE_BRACKET a
    ON f.age_key = a.age_key
LEFT JOIN DIM_CLUB c
    ON f.club_key = c.club_key
"""


@st.cache_resource(show_spinner=False)
def download_parquets_to_duckdb(db_path: Path = LOCAL_DUCKDB_PATH) -> Path:
    """
    Descarga los archivos parquet desde el bucket de backblaze y construye
    una base de datos duckdb local con todas las tablas para realizar consultas
    locales.
    """
    print("Descargando archivos parquet desde Backblaze y construyendo base de datos duckdb local...")
    db_path = Path(db_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)

    B2_KEY_ID = st.secrets['connections']['backblaze']['B2_KEY_ID']
    B2_KEY_NAME = st.secrets['connections']['backblaze']['B2_KEY_NAME']
    B2_APPLICATION_KEY = st.secrets['connections']['backblaze']['B2_APPLICATION_KEY']
    B2_BUCKET_NAME = st.secrets['connections']['backblaze']['B2_BUCKET_NAME']
    B2_ENDPOINT = st.secrets['connections']['backblaze']['B2_ENDPOINT']
    B2_REGION = st.secrets['connections']['backblaze']['B2_REGION']

    with duckdb.connect(db_path.as_posix()) as con:
        existing_tables = {
            row[0]
            for row in con.execute(
                "SELECT table_name FROM information_schema.tables WHERE table_schema = 'main'"
            ).fetchall()
        }
        if set(B2_TABLES).issubset(existing_tables):
            return db_path

        con.execute("INSTALL httpfs;")
        con.execute("LOAD httpfs;")

        con.execute(f"""
            CREATE OR REPLACE SECRET backblaze_b2 (
                TYPE S3,
                KEY_ID '{B2_KEY_ID}',
                SECRET '{B2_APPLICATION_KEY}',
                REGION '{B2_REGION}',
                ENDPOINT '{B2_ENDPOINT}',
                URL_STYLE 'path'
            );
        """)

        for tabla in B2_TABLES:
            ruta_s3 = f"s3://{B2_BUCKET_NAME}/{tabla}.parquet"
            con.execute(
                f"CREATE OR REPLACE TABLE {tabla} AS SELECT * FROM read_parquet('{ruta_s3}');"
            )

    return db_path


def query_local_duckdb(sql_query: str, params: list | None = None) -> pd.DataFrame:
    """
    Ejecuta una consulta SQL sobre la base de datos duckdb local construida
    a partir de los archivos parquets.
    """
    if not LOCAL_DUCKDB_PATH.exists():
        download_parquets_to_duckdb(LOCAL_DUCKDB_PATH)

    with duckdb.connect(LOCAL_DUCKDB_PATH.as_posix(), read_only=True) as con:
        if params:
            return con.execute(sql_query, params).df()
        return con.execute(sql_query).df()


def get_snowflake_connection():
    """Devuelve la conexión nativa y cacheada de Streamlit a Snowflake."""
    return st.connection("snowflake")


def _optimize_dataframe_memory(df: pd.DataFrame) -> pd.DataFrame:
    """
    Optimiza el uso de RAM sin pérdida de precisión usando pyarrow para strings y downcast para enteros. Esto reduce el consumo de memoria
    """
    df = df.copy()
    df.columns = df.columns.str.upper()

    for col in df.columns:
        col_type = df[col].dtype

        if pd.api.types.is_string_dtype(col_type):
            df[col] = df[col].astype("string[pyarrow]")

        elif pd.api.types.is_integer_dtype(col_type):
            df[col] = pd.to_numeric(df[col], downcast="integer")

    return df


@st.cache_data(ttl="1h", max_entries=1, show_spinner=False)
def load_base_mart_data() -> pd.DataFrame:
    """
    Descarga el modelo dimensional de Snowflake una vez por hora y guarda
    una única copia optimizada en RAM compartida por todos los usuarios.
    """
    conn = get_snowflake_connection()
    raw_df = conn.query(MART_BASE_QUERY, ttl=0, show_spinner=False)
    return _optimize_dataframe_memory(raw_df)


def get_filtered_data() -> pd.DataFrame:
    """
    Aplica los filtros globales del sidebar sobre el DataFrame en caché
    usando pandas.
    """
    df = load_base_mart_data()
    mask = pd.Series(True, index=df.index)

    # 1. Filtro por Temporada
    selected_seasons = st.session_state.get("sb_season", [])
    if selected_seasons:
        mapped_seasons = [SEASON_MAP.get(season, season) for season in selected_seasons]
        mask &= df["SEASON_LABEL"].isin(mapped_seasons)

    # 2. Filtro por Posición
    selected_positions = st.session_state.get("sb_positions", [])
    if selected_positions:
        mapped_positions = [POSITION_MAP.get(pos, pos) for pos in selected_positions]
        mask &= df["PRIMARY_CATEGORY"].isin(mapped_positions)

    # 3. Filtro por Grupo etario
    selected_age_groups = st.session_state.get("sb_age_groups", [])
    if selected_age_groups:
        mapped_age_groups = [
            AGE_GROUP_MAP.get(group, group.replace("–", "-"))
            for group in selected_age_groups
        ]
        mask &= df["AGE_GROUP"].isin(mapped_age_groups)

    # 4. Filtro por Rango Exacto de Edad
    selected_age_range = st.session_state.get("sb_age_range", (15, 38))
    if selected_age_range and tuple(selected_age_range) != (15, 38):
        min_age, max_age = selected_age_range
        mask &= (df["AGE"] >= min_age) & (df["AGE"] <= max_age)

    # 5. Filtro por Salario Anual Mínimo
    selected_min_wage = st.session_state.get("sb_min_wage", 0)
    if selected_min_wage and selected_min_wage > 0:
        mask &= df["ANNUAL_WAGE_EUR"] >= selected_min_wage

    return df.loc[mask]


def query_filtered_data(sql_query: str) -> pd.DataFrame:
    """
    Ejecuta una consulta SQL de DuckDB directamente sobre `df_filtrado` df que tiene los filtros del sidebar aplicados.
    """
    df_filtrado = get_filtered_data()

    with duckdb.connect(":memory:") as con:
        con.register("df_filtrado", df_filtrado)
        return con.execute(sql_query).df()


def query_base_data(sql_query: str, params: list | None = None) -> pd.DataFrame:
    """
    Ejecuta una consulta SQL de DuckDB directamente sobre `df_base` usa el mart completo en caché.
    """
    df_base = load_base_mart_data()

    with duckdb.connect(":memory:") as con:
        con.register("df_base", df_base)
        if params:
            return con.execute(sql_query, params).df()
        return con.execute(sql_query).df()
