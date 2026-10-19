# Análisis del ciclo de vida futbolístico según la posición con base en el rendimiento, la longevidad y el impacto de estos en el ingreso salarial en el periodo 2022-2026

## Introducción

En el ámbito del fútbol profesional actual, el uso de la analítica de datos ha transformado tanto la administración deportiva como la económica, comprender el ciclo de vida de los futbolistas, su rendimiento pico, longevidad por posición y tasa de declive. Es fundamental para optimizar la toma de decisiones y la inversión en plantillas.

No obstante, a menudo hay una falta de conexión entre el desempeño en el campo y la compensación económica. Esta investigación analiza el ciclo de vida profesional de los futbolistas durante el periodo 2022–2026. A través del análisis de sus habilidades, longevidad posicional y salarios activos, este estudio evalúa si la valoración económica del mercado refleja el rendimiento real o responde a distorsiones históricas del fútbol profesional. 


## Planteamiento del problema

En el fútbol profesional, las decisiones estratégicas se basan cada vez más en métricas creadas para comprender cómo su desempeño los posiciona en el campo. En un mercado, donde los futbolistas son la inversión principal de las organizaciones para quienes es indispensable garantizar la eficiencia entre sus principales activos. La tendencia a generalizar el envejecimiento deportivo genera percepciones erróneas sobre la vida útil, el inicio del declive físico y el momento de máximo desempeño de los jugadores según su posición en el campo.

La falta de caracterización de estos análisis genera que la estructura salarial y negociaciones de traspaso no se ajusten a la habilidad real en la cancha, donde el contrato del deportista pase a estar fundamentada no solo en el rendimiento en el campo, sino además, depender en exceso a factores como su reputación mediática, su impacto comercial o como es percibido por la fama obtenida. Esto crea un desfase temporal entre el verdadero pico de habilidad deportiva del atleta y el momento en el que alcanza su tope salarial.

A nivel institucional, este fenómeno induce a una ineficiencia sistemática en la toma de decisiones. Asumir altos costos salariales por jugadores que ya han superado su pico de rendimiento en su posición específica compromete el presupuesto y la competitividad deportiva del equipo. Ante la necesidad de optimizar los recursos en el mercado actual, surge la siguiente interrogante: ¿Cómo varía el rendimiento, medido por el puntaje de habilidad, entre los grupos de edad según la posición de juego, y en qué medida coincide la edad de mayor rendimiento con la de mayor ingreso salarial en los futbolistas registrados en la base de datos del proyecto durante el periodo 2022-2026?

En base a lo anterior se plantean las siguientes preguntas de investigación:

1. ¿Cuál es el puntaje de habilidad promedio de cada grupo etario (15-21, 22-26, 27-31 y 32-38 años) y cómo varía a lo largo del periodo 2022-2026?
2. ¿Qué posición de juego presenta mayor longevidad, entendida como la mayor proporción de jugadores en el grupo de 32 a 38 años y la menor disminución del puntaje de habilidad con la edad?
3. ¿Cómo varía el salario anual promedio según el grupo etario y la posición de juego a lo largo del periodo 2022-2026?
4. ¿En qué grupo etario alcanza cada posición  su mayor puntaje de habilidad y su mayor salario anual, y coinciden ambos momentos?
5. ¿Qué grado de correlación existe entre el puntaje de habilidad y el salario anual dentro de cada grupo etario y posición de juego?

## Objetivo General

Analizar el ciclo de vida profesional de los futbolistas en las distintas posiciones a lo largo del periodo 2022-2026, mediante la evaluación del desarrollo profesional de los deportistas con el propósito de determinar las edades de mayor rendimiento y la relación con su ingreso salarial.

## Objetivos Específicos

- Promediar el rendimiento anual a través del puntaje de habilidad entre los años 2022, 2023, 2024, 2025 y 2026 en las categorías etarias de  15-21, 22-26, 27-31, 32-38 para lograr una mayor comprensión del rendimiento entre los años de estudio y comparación entre los mismos.
  
- Comparar las trayectorias de envejecimiento entre las posiciones en el campo para identificar qué roles tienen la mayor longevidad.

- Estudiar el crecimiento salarial de los futbolistas en el periodo 2022-2026 calculando el salario promedio basado en sus contratos, clasificándolos en grupos etarios de 15-21, 22-26, 27-31, 32-38 y su posición.

- Comparar la relación entre el mayor puntaje de habilidad con la edad que alcanza su pico salarial, para identificar si existe una convergencia entre el mejor momento deportivo y su ingreso máximo según la posición.

- Calcular el coeficiente de correlacion del puntaje de habilidad con el ingreso salarial dentro de cada categoría y posición para medir el impacto financiero del rendimiento deportivo.

## Justificación

Esta investigación es fundamental para entender cómo ha cambiado la gestión deportiva tanto operativa como financieramente frente a la creciente profesionalización de la analítica de datos en el deporte. Desde el punto de vista del mercado, establecer o no la existencia de un desfase temporal entre el máximo nivel de habilidad atlética y el salario más alto permitirá a directivos, representantes y marcas deportivas ajustar sus tácticas de contratación, renovación y gestión de activos de acuerdo a los verdaderos ciclos de vida de los deportistas. Desde un enfoque estadístico, el análisis se respalda al incluir un estudio a lo largo del periodo 2022-2026 que desafía la percepción común: mostrar si el valor monetario de un atleta está vinculado de manera lineal a su rendimiento actual o si está influenciado por reputaciones y contratos del pasado. Adicionalmente, al analizar estos datos según la posición y grupos de edad, el estudio aportará valor al identificar si las demandas táctico-físicas influyen en la durabilidad en el deporte o si existen distorsiones salariales a lo largo de toda la estructura del fútbol profesional.

## Herramientas Tecnológicas Utilizadas

- Python, SQLite, DuckDB, Snowflake, DBT Core, Power BI, Streamlit.

[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![DuckDB](https://img.shields.io/badge/DuckDB-FFF000?style=for-the-badge&logo=duckdb&logoColor=black)](https://duckdb.org/)
[![Snowflake](https://img.shields.io/badge/Snowflake-29B5E8?style=for-the-badge&logo=snowflake&logoColor=white)](https://www.snowflake.com/)
[![dbt](https://img.shields.io/badge/dbt_Core-FF694B?style=for-the-badge&logo=dbt&logoColor=white)](https://docs.getdbt.com/)
[![Power BI](https://img.shields.io/badge/Power_BI-F2C811?style=for-the-badge&logo=powerbi&logoColor=black)](https://powerbi.microsoft.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)

## Bosquejo del Modelo de Datos Desnormalizado 

Para facilitar el procesamiento analítico, la evaluación del rendimiento por posición y el estudio de la longevidad deportiva y su impacto en el ingreso salarial durante el periodo 2022-2026, los datos se estructuran conceptualmente bajo un esquema Snowflake.

Este esquema centraliza las métricas contractuales y estadísticas de rendimiento en tablas de hechos (fact_contracts, fact_season_stats) rodeadas por tablas de dimensiones clave (dim_player, dim_player_season), permitiendo responder directamente a los objetivos de investigación del ciclo de vida futbolístico sin necesidad de realizar combinaciones complejas en tiempo de ejecución.

## Diagrama de Entidad-Relación (DER)

```mermaid
erDiagram
    fact_contracts {
        string contract_key PK "Surrogate key (unique, not_null)"
        string player_key FK "Player surrogate key (not_null)"
        int contract_id "Natural contract ID (not_null)"
        int player_id "Natural player ID (not_null)"
        decimal weekly_wage_eur "Weekly wage in EUR (not_null)"
        decimal annual_wage_eur "Annual wage in EUR - weekly * 52 (not_null)"
    }

    fact_season_stats {
        string player_season_key PK "Player-season surrogate key, FK (unique, not_null)"
        string player_key FK "Player surrogate key (not_null)"
        string season_key "Season surrogate key (not_null)"
        decimal ability_score "Season ability score (not_null)"
    }

    dim_player {
        string player_key PK "Surrogate key (unique, not_null)"
        int player_id "Natural primary key (not_null)"
        string name "Full name (not_null)"
        string primary_category "Role - GOALKEEPER, DEFENDER, MIDFIELDER, ATTACKER"
    }

    dim_player_season {
        string player_season_key PK "Surrogate key (unique, not_null)"
        int season_id "Season ID (not_null)"
        int player_season_id "Player season record ID (not_null)"
        string season_label "Season label (not_null)"
        int age "Player age during season (not_null)"
        string age_group "Age group - 15-21, 22-26, 27-31, 32-38 (not_null)"
        string all_positions_str "Comma-separated positions played (not_null)"
    }

    dim_player ||--o{ fact_contracts : player_key
    dim_player ||--o{ fact_season_stats : player_key
    dim_player_season ||--|| fact_season_stats : player_season_key
```

## Cardinalidad y Relaciones entre Entidades

Las relaciones del diagrama presentan patrones claros de Uno a Muchos (1:N) y conexiones estructurales entre las dimensiones y las tablas de hechos, basándose en el modelo de datos ilustrado: 

**dim_player → fact_contracts (1:N)**: Un jugador registrado puede tener uno o varios contratos durante su trayecto deportivo, aunque cada registro de contrato se relaciona con un solo jugador.

**dim_player → fact_season_stats (1:N)**: Un jugador puede captar estadísticas de su desempeño en una o más temporadas, pero cada registro de estadísticas de una temporada se vincula a un único jugador. 

**dim_player_season → fact_season_stats (1:N)**: Una temporada especifica de un jugador puede agrupar múltiples métricas o registros de estadísticas de rendimiento,  sin embargo, cada registro estadístico referido a la temporada se asocia a una exclusiva combinación de jugador y temporada (player_season_key).

## Colaboradores del Proyecto 

| Integrante | Rol en el Proyecto | Contribuciones Principales |
| :--- | :--- | :--- |
| **Jorge Torres** | Tech Lead & Data Engineer | Arquitectura de datos, pipelines (SQL/Snowflake), modelado en dbt, gestión de PRs y roles.
| **Noryen Haringhton** | SME & Data App Developer | Lógica de negocio (Fútbol), desarrollo de componentes y diseño de frontend en Streamlit.
| **Angel Pastrano** | BI Developer | Desarrollo integral del dashboard en Power BI, creación de métricas y visualizaciones.
| **Johan Infante** | Data Analyst | Desarrollo de queries SQL para objetivos de negocio y configuración de Streamlit.|
| **Gabriel Ugas** | BI Analyst & Tech Writer | Ejecución de tareas en Power BI y desarrollo de la documentación del repositorio.
| **Stephannie Labrador** | Technical Writer & UI/UX Lead | Documentación teórica del proyecto y aportes en el diseño de la aplicación.

## Estructura del Repositorio

- [📁 **app/**](https://github.com/Jtorres1000/Football_players_analysis/tree/main/app): Contiene la aplicación web interactiva desarrollada con *Streamlit*. Incluye las vistas de navegación ([`pages/`](https://github.com/Jtorres1000/Football_players_analysis/tree/main/app/pages)), componentes visuales ([`components/`](https://github.com/Jtorres1000/Football_players_analysis/tree/main/app/components)), estilos y el punto de entrada principal ([`app.py`](https://github.com/Jtorres1000/Football_players_analysis/blob/main/app/app.py)) para explorar y visualizar los datos analizados.
- [📁 **assets/**](https://github.com/Jtorres1000/Football_players_analysis/tree/main/assets): Almacena recursos gráficos y diagramas explicativos del proyecto, tales como el Diagrama Entidad-Relación ([`DER.png`](https://github.com/Jtorres1000/Football_players_analysis/blob/main/assets/DER.png)) y el esquema de denormalización de datos ([`DENORMALIZACION.png`](https://github.com/Jtorres1000/Football_players_analysis/blob/main/assets/DENORMALIZACION.png)).
- [📁 **data/**](https://github.com/Jtorres1000/Football_players_analysis/tree/main/data): Directorio destinado a la organización, almacenamiento y control de los conjuntos de datos en sus diferentes fases de procesamiento (por ejemplo, datos limpios en [`clean/`](https://github.com/Jtorres1000/Football_players_analysis/tree/main/data/clean)).
- [📁 **football_analytics_dbt/**](https://github.com/Jtorres1000/Football_players_analysis/tree/main/football_analytics_dbt): Proyecto de ingeniería de analítica con *dbt Core*. Contiene los modelos SQL modulares organizados en capas (*staging* y *marts*), macros, tests de calidad de datos y configuraciones para transformar datos dentro del Data Warehouse.
- [📁 **power_bi/**](https://github.com/Jtorres1000/Football_players_analysis/tree/main/power_bi): Espacio reservado para los tableros de control, plantillas y reportes interactivos de *Power BI* enfocados en la inteligencia de negocios y presentación ejecutiva de las métricas.
- [📁 **scripts/**](https://github.com/Jtorres1000/Football_players_analysis/tree/main/scripts): Scripts utilitarios en Python para tareas de automatización, ingesta y transformación de datos, como la conversión de tablas SQLite a archivos Parquet de alto rendimiento mediante *DuckDB* ([`raw_parquets.py`](https://github.com/Jtorres1000/Football_players_analysis/blob/main/scripts/raw_parquets.py)).