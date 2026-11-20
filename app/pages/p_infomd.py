import streamlit as st

from components import banner

INTRO_PARAGRAPHS = [
    (
        "En el ámbito del fútbol profesional actual, el uso de la analítica de datos ha transformado "
        "tanto la administración deportiva como la económica; comprender el ciclo de vida de los "
        "futbolistas, su rendimiento pico, longevidad por posición y tasa de declive es fundamental "
        "para optimizar la toma de decisiones y la inversión en plantillas."
    ),
    (
        "No obstante, a menudo hay una falta de conexión entre el desempeño en el campo y la "
        "compensación económica. Esta investigación analiza el ciclo de vida profesional de los "
        "futbolistas durante el periodo 2022–2026. A través del análisis de sus habilidades, "
        "longevidad posicional y salarios activos, este estudio evalúa si la valoración económica "
        "del mercado refleja el rendimiento real o responde a distorsiones históricas del fútbol profesional."
    ),
]

PROBLEM_PARAGRAPHS = [
    (
        "En el fútbol profesional, las decisiones estratégicas se basan cada vez más en métricas "
        "creadas para comprender cómo su desempeño los posiciona en el campo. En un mercado donde "
        "los futbolistas son la inversión principal de las organizaciones, para quienes es indispensable "
        "garantizar la eficiencia entre sus principales activos, la tendencia a generalizar el "
        "envejecimiento deportivo genera percepciones erróneas sobre la vida útil, el inicio del "
        "declive físico y el momento de máximo desempeño de los jugadores según su posición en el campo."
    ),
    (
        "La falta de caracterización de estos análisis genera que la estructura salarial y "
        "negociaciones de traspaso no se ajusten a la habilidad real en la cancha, donde el contrato "
        "del deportista pase a estar fundamentada no solo en el rendimiento en el campo, sino además, "
        "depender en exceso a factores como su reputación mediática, su impacto comercial o como es "
        "percibido por la fama obtenida. Esto crea un desfase temporal entre el verdadero pico de "
        "habilidad deportiva del atleta y el momento en el que alcanza su tope salarial."
    ),
    (
        "A nivel institucional, este fenómeno induce a una ineficiencia sistemática en la toma de "
        "decisiones. Asumir altos costos salariales por jugadores que ya han superado su pico de "
        "rendimiento en su posición específica compromete el presupuesto y la competitividad deportiva "
        "del equipo. Ante la necesidad de optimizar los recursos en el mercado actual, surge la "
        "siguiente interrogante:"
    ),
]

CENTRAL_QUESTION = (
    "¿Cómo varía el rendimiento, medido por el puntaje de habilidad, entre los grupos de edad "
    "según la posición de juego, y en qué medida coincide la edad de mayor rendimiento con la de "
    "mayor ingreso salarial en los futbolistas registrados en la base de datos del proyecto "
    "durante el periodo 2022-2026?"
)

RESEARCH_QUESTIONS = [
    "¿Cuál es el puntaje de habilidad promedio de cada grupo etario (15-21, 22-26, 27-31 y 32-38 años) y cómo varía a lo largo del periodo 2022-2026?",
    "¿Qué posición de juego presenta mayor longevidad, entendida como la mayor proporción de jugadores en el grupo de 32 a 38 años y la menor disminución del puntaje de habilidad con la edad?",
    "¿Cómo varía el salario anual promedio según el grupo etario y la posición de juego a lo largo del periodo 2022-2026?",
    "¿En qué grupo etario alcanza cada posición su mayor puntaje de habilidad y su mayor salario anual, y coinciden ambos momentos?",
    "¿Qué grado de correlación existe entre el puntaje de habilidad y el salario anual dentro de cada grupo etario y posición de juego?",
]

GENERAL_OBJECTIVE = (
    "Analizar el ciclo de vida profesional de los futbolistas en las distintas posiciones a lo "
    "largo del periodo 2022-2026, mediante la evaluación del desarrollo profesional de los deportistas "
    "con el propósito de determinar las edades de mayor rendimiento y la relación con su ingreso salarial."
)

SPECIFIC_OBJECTIVES = [
    "Promediar el rendimiento anual a través del puntaje de habilidad entre los años 2022, 2023, 2024, 2025 y 2026 en las categorías etarias de 15-21, 22-26, 27-31, 32-38 para lograr una mayor comprensión del rendimiento entre los años de estudio y comparación entre los mismos.",
    "Comparar las trayectorias de envejecimiento entre las posiciones en el campo para identificar qué roles tienen la mayor longevidad.",
    "Estudiar el crecimiento salarial de los futbolistas en el periodo 2022-2026 calculando el salario promedio basado en sus contratos, clasificándolos en grupos etarios de 15-21, 22-26, 27-31, 32-38 y su posición.",
    "Comparar la relación entre el mayor puntaje de habilidad con la edad que alcanza su pico salarial, para identificar si existe una convergencia entre el mejor momento deportivo y su ingreso máximo según la posición.",
    "Calcular el coeficiente de correlación del puntaje de habilidad con el ingreso salarial dentro de cada categoría y posición para medir el impacto financiero del rendimiento deportivo.",
]

JUSTIFICATION_PARAGRAPHS = [
    (
        "Esta investigación es fundamental para entender cómo ha cambiado la gestión deportiva tanto "
        "operativa como financieramente frente a la creciente profesionalización de la analítica de datos "
        "en el deporte. Desde el punto de vista del mercado, establecer o no la existencia de un desfase "
        "temporal entre el máximo nivel de habilidad atlética y el salario más alto permitirá a directivos, "
        "representantes y marcas deportivas ajustar sus tácticas de contratación, renovación y gestión "
        "de activos de acuerdo a los verdaderos ciclos de vida de los deportistas."
    ),
    (
        "Desde un enfoque estadístico, el análisis se respalda al incluir un estudio a lo largo del "
        "periodo 2022-2026 que desafía la percepción común: mostrar si el valor monetario de un atleta "
        "está vinculado de manera lineal a su rendimiento actual o si está influenciado por reputaciones "
        "y contratos del pasado. Adicionalmente, al analizar estos datos según la posición y grupos de edad, "
        "el estudio aportará valor al identificar si las demandas táctico-físicas influyen en la durabilidad "
        "en el deporte o si existen distorsiones salariales a lo largo de toda la estructura del fútbol profesional."
    ),
]

CONCLUSION_INTRO = (
    "El análisis del periodo 2022-2026 permite responder a cada objetivo específico a partir de los datos del estudio:"
)

CONCLUSION_POINTS = [
    (
        "El puntaje de habilidad promedio crece con la edad en todas las temporadas; en 2025/26 pasa de 378,9 puntos "
        "en el grupo de 15 a 21 años a 445,9 en el de 32 a 38 años. Entre temporadas, la media de los tramos jóvenes "
        "sube levemente y la de los grupos mayores baja a medida que ingresan más jugadores a esas edades."
    ),
    (
        "En longevidad, los porteros lideran en permanencia con un 12,1 % de sus registros entre los 32 y 38 años, "
        "frente a un rango de 4,8 % a 5,7 % en el resto de posiciones. A nivel individual, todos los puestos mejoran "
        "hasta los 26 años, empiezan a caer unos 6 puntos anuales entre los 27 y 31 años y pierden entre 19,9 puntos "
        "en defensas y 23,7 en delanteros a partir de los 32 años."
    ),
    (
        "El salario anual promedio sube con la edad en todas las posiciones hasta más que duplicarse en el tramo "
        "veterano. Los centrocampistas y defensas registran los sueldos medios más altos, llegando a 2,56 y 2,41 "
        "millones de euros entre los 32 y 38 años, seguidos por los porteros con 2,24 millones y los delanteros "
        "con 1,71 millones."
    ),
    (
        "Los promedios máximos de habilidad y de salario coinciden en el grupo de 32 a 38 años para las cuatro "
        "posiciones, encabezados por los centrocampistas con 470,8 puntos y 2,56 millones de euros. Sin embargo, "
        "como a esa edad la variación individual ya es negativa, este techo grupal se explica por el sesgo de "
        "supervivencia, pues solo continúan activos los futbolistas de mayor nivel y mejores contratos."
    ),
    (
        "La correlación de Pearson entre habilidad y salario es positiva y alta en todos los grupos y posiciones, "
        "variando entre 0,730 y 0,863. El vínculo es algo menor entre los 15 y 21 años por la uniformidad de los "
        "contratos iniciales y supera el 0,80 en todos los puestos a partir de los 27 años."
    ),
]

CONCLUSION_ANSWER = (
    "En respuesta a la pregunta de investigación, el futbolista mejora su rendimiento individual hasta el tramo "
    "de 22 a 26 años y comienza a declinar desde los 27 años a un ritmo parecido en todos los puestos, salvo por "
    "la mayor duración de carrera de los porteros. Aunque los promedios de habilidad y salario alcanzan su máximo "
    "en el grupo de 32 a 38 años con una correlación fuerte, esto ocurre porque a esa edad solo permanecen activos "
    "jugadores consagrados. Para los clubes, otorgar contratos altos después de los 32 años implica pagar el "
    "máximo del mercado cuando el rendimiento individual ya cae cerca de 20 puntos por temporada, por lo que es "
    "más eficiente concentrar la inversión entre los 22 y los 31 años."
)

LIMITATIONS_ITEMS = [
    "Las temporadas 2022/23 a 2024/25 son datos generados y solo 2025/26 contiene registros reales, por lo que en los primeros años aparecen muchos menos jugadores de 32 a 38 años.",
    "La variación anual de habilidad del segundo objetivo excluye la primera temporada de cada jugador al no tener un año previo de comparación.",
    "El sesgo de supervivencia eleva los promedios del grupo de 32 a 38 años, donde además hay muestras pequeñas como los 324 registros de delanteros veteranos.",
    "La correlación de Pearson confirma una asociación lineal fuerte entre habilidad y salario, pero no demuestra causalidad.",
]


def _format_numbered_list(items: list[str]) -> str:
    """Construye una lista numerada en Markdown para preguntas u objetivos."""
    return "\n".join(f"{idx}. {text}" for idx, text in enumerate(items, start=1))


def _render_introduccion() -> None:
    """Renderiza la sección de introducción en Markdown simple."""
    st.subheader("Introducción")
    st.markdown("\n\n".join(INTRO_PARAGRAPHS))


def _render_planteamiento() -> None:
    """Renderiza el planteamiento del problema, la interrogante central y las preguntas de investigación."""
    st.subheader("Planteamiento del problema")
    st.markdown("\n\n".join(PROBLEM_PARAGRAPHS))
    st.markdown(f"> **Interrogante principal**\n>\n> {CENTRAL_QUESTION}")
    st.markdown("**En base a lo anterior se plantean las siguientes preguntas de investigación:**")
    st.markdown(_format_numbered_list(RESEARCH_QUESTIONS))


def _render_objetivo_general() -> None:
    """Renderiza el objetivo general de la investigación en markdown simple."""
    st.subheader("Objetivo General")
    st.markdown(f"> {GENERAL_OBJECTIVE}")


def _render_objetivos_especificos() -> None:
    """Renderiza los objetivos específicos como una lista numerada en markdown."""
    st.subheader("Objetivos Específicos")
    st.markdown(_format_numbered_list(SPECIFIC_OBJECTIVES))


def _render_justificacion() -> None:
    """Renderiza la justificación en markdown simple."""
    st.subheader("Justificación")
    st.markdown("\n\n".join(JUSTIFICATION_PARAGRAPHS))


def _render_conclusion() -> None:
    """Renderiza la conclusión general y las limitaciones del estudio."""
    st.subheader("Conclusión General")
    st.markdown(CONCLUSION_INTRO)
    st.markdown("\n".join(f"- {point}" for point in CONCLUSION_POINTS))
    st.markdown(CONCLUSION_ANSWER)
    st.markdown("#### Limitaciones")
    st.markdown("\n".join(f"- {item}" for item in LIMITATIONS_ITEMS))


def p_infomd():

    banner(
        title="Trabajo investigativo",
        subtitle="La finalidad de esta investigación es determinar si existe una correlación entre las variables de rendimiento y longevidad en el desarrollo del ciclo de vida futbolístico y cómo este afecta al ingreso salarial.",
    )

    _render_introduccion()
    st.divider()
    _render_planteamiento()
    st.divider()
    _render_objetivo_general()
    st.divider()
    _render_objetivos_especificos()
    st.divider()
    _render_justificacion()
    st.divider()
    _render_conclusion()
