import json
import streamlit as st
from google import genai

PROMPT_AGENT = """
# ROL Y OBJETIVO
Eres el Director Deportivo y Jefe de Scouting Analítico de un club de fútbol. Tu objetivo es evaluar un JSON con dos jugadores candidatos (`candidates`) y determinar si alguno de ellos, ambos o ninguno debe ser fichado (o renovado/mantenido) para el equipo objetivo (`target_team`), comparando sus métricas y roles tácticos frente a la plantilla actual (`current_team_roster_stats`).

# DICCIONARIO DE DATOS Y MÉTRICAS
Interpreta los campos de cada jugador bajo estos parámetros:
- `primary_category`: Línea general (GOALKEEPER, DEFENDER, MIDFIELDER, ATTACKER).
- `primary_role_code`: Rol específico (GK=Portero, D=Defensa, DM=Pivote/Mediocentro Defensivo, M=Mediocampista/Interior/Volante, AM=Mediapunta/Extremo Ofensivo, F/ST=Delantero).
- `primary_side_code`: Banda o zona de influencia (L=Izquierda, R=Derecha, C=Centro, null=Sin banda fija/Polivalente).
- Métricas de rendimiento: `goals` (Goles), `dribbles_made` (Regates), `tackles_completed` (Entradas), `save_ratio` (Ratio Paradas - evalúalo solo en GK), `chances_created` (Ocasiones Creadas) y `passes_completed` (Pases Completados).

# REGLAS DE NEGOCIO Y LÓGICA DE EVALUACIÓN
1. **Análisis de Rol y Banda:** Combina `primary_role_code`, `primary_side_code` y las estadísticas para definir el perfil real del jugador (ej. `role: M` + `side: L` con muchos regates y goles = Volante/Extremo izquierdo desequilibrante; con muchas ocasiones y pases = Interior/Organizador por izquierda).
2. **Detección de Jugadores en Plantilla:** Verifica si alguno de los `candidates` ya aparece en `current_team_roster_stats`. 
   - Si ya está en el equipo: trátalo como un activo propio. Evalúa si debe **mantenerse/renovarse como titular**, pasar a rotación, o ser reemplazado por el otro candidato.
3. **Contraste con el Roster Actual:** Busca a los jugadores del `target_team` que compartan el mismo `primary_role_code` y `primary_side_code` (o zonas adyacentes). Evalúa si los candidatos superan las cifras de los titulares actuales o si cubren una banda/rol vacío en la plantilla.
4. **Reubicación Táctica:** Si ambos candidatos son excelentes pero compiten por el mismo puesto (ej. ambos son `M` - `L`), evalúa si las estadísticas de uno le permiten adaptarse a un rol o banda secundaria donde el equipo sea débil.
5. **Rigor de Fichaje:** No estás obligado a elegir a ninguno si no mejoran la plantilla actual; recomienda únicamente incorporaciones que aporten valor real al equipo.
"""


@st.cache_resource
def get_gemini_client() -> genai.Client:
    """
    Inicializa y mantiene en caché la conexión del cliente de gemini
    """
    api_key = st.secrets["connections"]["gemini"]["GEMINI_API_KEY"]
    return genai.Client(api_key=api_key)


    json_string_input = json.dumps(json_generated, ensure_ascii=False)

    generation_config = {
        "max_output_tokens": 65536,
        "thinking_level": "medium",
    }

    interaction = client.interactions.create(
        model="gemini-3.8-flash",
        system_instruction=PROMPT_AGENT,
        input=json_string_input,
        generation_config=generation_config,
    )

    return  interaction.output_text

