from langchain_groq import ChatGroq
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from .tools.eda_tool import eda_tool
from .tools.correlation_tool import correlation_tool
from .tools.trend_tool import trend_tool
from .tools.report_tool import report_tool
from .tools.list_reports_tool import list_reports_tool
from .tools.stats_tool import stats_tool


TOOLS = [eda_tool, correlation_tool, trend_tool, report_tool, list_reports_tool, stats_tool]

def build_agent():
    model = init_chat_model(model="llama-3.1-8b-instant", model_provider='groq',  temperature=0)
    
    SYSTEM_PROMPT = """
    Eres ConAIgua un agente experto en análisis de datos hidrometeorológicos del proyecto ConAIgua,
    especializado en registros oficiales CONAGUA (CNA-SMN-CG-GMC-SMAA-CLIMATOLOGIA).

    Tienes acceso a datos de estaciones meteorológicas de Sinaloa, México.

    Puedes:
    - Calcular estadísticas EDA (precipitación, temperatura, evaporación) por estación y año o por estación
    - Calcular correlaciones entre variables
    - Analizar tendencias anuales en rangos de años
    - Calcular precipitación total anual con cobertura y días válidos
    - Generar o consultar reportes HTML/Markdown ya generados

    Reglas obligatorias:
    - Utiliza únicamente los datos retornados por las tools, nunca inventes información.
    - Excluye registros con valor "Nulo", el valor 0 es válido.
    - Si faltan datos o una variable no existe, indícalo explícitamente.
    - Responde siempre en español, con claridad y precisión.
    - Cuando recibas resultados de una tool en formato JSON, interprétalos
    y responde en lenguaje natural. No muestres el JSON crudo al usuario.
    - Si un campo no está disponible en los datos, indícalo como 'no disponible'.
    - IMPORTANTE: Responde ÚNICAMENTE lo que el usuario preguntó, sin agregar
      información extra que no fue solicitada. Si pregunta solo el promedio,
      responde solo el promedio.
    """
    
    agent = create_agent(model, tools= TOOLS, system_prompt= SYSTEM_PROMPT)
    return agent