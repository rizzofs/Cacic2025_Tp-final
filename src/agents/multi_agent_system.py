#!/usr/bin/env python3
"""
Sistema Multi-Agente para Mozo Virtual - La Taberna del Río
Implementa dos agentes colaborativos: Investigador y Generador de Informes
"""

import os
from typing import Sequence, Annotated, TypedDict, Literal
from datetime import datetime
import json

# Carga de variables de entorno
from dotenv import load_dotenv

# LangSmith para observabilidad
import os
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "proyecto-final-agentes"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"

# Componentes de LangChain
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.tools.retriever import create_retriever_tool
from langchain.agents import create_react_agent
from langchain.prompts import PromptTemplate
from langchain_core.tools import tool
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage

# Componentes específicos de Google
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI

# Componentes de LangGraph
from langchain_chroma import Chroma
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode

# Integración con Notion
from notion_client import Client

# LangSmith Observer
from ..observability.langsmith_observer import LangSmithObserver


class MultiAgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    current_agent: str
    investigation_results: dict
    report_data: dict
    client_preferences: dict


class MultiAgentMozoVirtual:
    """
    Sistema Multi-Agente para el Mozo Virtual
    - Agente Investigador: Busca información específica
    - Agente Generador: Crea informes estructurados
    """
    
    def __init__(self, vectorstore=None, notion_client=None):
        """Inicializar el sistema multi-agente"""
        self.setup_environment()
        self.setup_llm()
        self.vectorstore = vectorstore
        self.notion_client = notion_client
        
        # Estado del sistema
        self.current_investigation = {}
        self.generated_reports = []
        
        # LangSmith Observer
        self.observer = LangSmithObserver()
        
        self.setup_tools()
        self.setup_multi_agent_graph()
        
    def setup_environment(self):
        """Cargar variables de entorno"""
        load_dotenv()
        if not os.getenv("GEMINI_API_KEY"):
            raise ValueError("La variable de entorno GEMINI_API_KEY no está definida.")
        
        print("Variables de entorno cargadas para sistema multi-agente.")
    
    def setup_llm(self):
        """Configurar el modelo de lenguaje Gemini"""
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            google_api_key=os.getenv("GEMINI_API_KEY"), 
            temperature=0.7
        )
        self.embedding_model = GoogleGenerativeAIEmbeddings(
            model="models/gemini-embedding-001",
            google_api_key=os.getenv("GEMINI_API_KEY")
        )
        
        # Crear LLMs específicos para cada agente
        self.llm_investigator = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            google_api_key=os.getenv("GEMINI_API_KEY"), 
            temperature=0.7
        )
        self.llm_generator = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            google_api_key=os.getenv("GEMINI_API_KEY"), 
            temperature=0.7
        )
        
        print("Modelo Gemini configurado para sistema multi-agente.")
    
    def setup_tools(self):
        """Definir herramientas especializadas para cada agente"""
        
        # Definir herramientas como atributos de clase
        self.investigator_tools = []
        self.generator_tools = []
        
        # HERRAMIENTAS DEL AGENTE INVESTIGADOR
        @tool
        def investigar_plato_detallado(consulta: str):
            """Investiga información detallada sobre platos específicos del menú."""
            if not self.vectorstore:
                return "Base de conocimiento no disponible para investigacion."
            
            try:
                # Buscar información relevante
                retriever = self.vectorstore.as_retriever(search_kwargs={"k": 5})
                docs = retriever.get_relevant_documents(consulta)
                
                if not docs:
                    return f"No se encontro informacion especifica sobre: {consulta}"
                
                # Procesar resultados
                resultados = {
                    "consulta": consulta,
                    "documentos_encontrados": len(docs),
                    "informacion": [],
                    "recomendaciones": []
                }
                
                for doc in docs:
                    resultados["informacion"].append({
                        "contenido": doc.page_content[:500] + "..." if len(doc.page_content) > 500 else doc.page_content,
                        "fuente": doc.metadata.get("source", "desconocida")
                    })
                
                # Generar recomendaciones basadas en la búsqueda
                if "romántic" in consulta.lower() or "pareja" in consulta.lower():
                    resultados["recomendaciones"] = [
                        "Solomillo de Ternera - Elegante y sofisticado",
                        "Rioja Reserva - Vino perfecto para ocasiones especiales",
                        "Crema Catalana - Postre tradicional español"
                    ]
                elif "familia" in consulta.lower() or "niños" in consulta.lower():
                    resultados["recomendaciones"] = [
                        "Paella Valenciana - Ideal para compartir",
                        "Tortilla Española - Clásico familiar",
                        "Limonada Casera - Refrescante para todos"
                    ]
                elif "vegetariano" in consulta.lower() or "vegano" in consulta.lower():
                    resultados["recomendaciones"] = [
                        "Risotto de Setas - Cremoso y sabroso",
                        "Ensalada de Quinoa - Saludable y nutritiva",
                        "Gazpacho Andaluz - Refrescante y natural"
                    ]
                
                self.current_investigation = resultados
                return f"Investigacion completada. Encontrados {len(docs)} documentos relevantes."
                
            except Exception as e:
                return f"Error en la investigacion: {str(e)}"
        
        self.investigator_tools.append(investigar_plato_detallado)
        
        @tool
        def analizar_preferencias_cliente(descripcion: str):
            """Analiza las preferencias del cliente basándose en su descripción."""
            try:
                # Simular análisis de preferencias
                preferencias = {
                    "tipo_comida": [],
                    "presupuesto": "medio",
                    "ocasion": "general",
                    "restricciones": [],
                    "gustos": []
                }
                
                desc_lower = descripcion.lower()
                
                # Analizar tipo de comida
                if any(word in desc_lower for word in ["carne", "ternera", "cordero", "cochinillo"]):
                    preferencias["tipo_comida"].append("carnes")
                if any(word in desc_lower for word in ["pescado", "marisco", "paella", "bacalao"]):
                    preferencias["tipo_comida"].append("pescados_mariscos")
                if any(word in desc_lower for word in ["vegetariano", "vegano", "ensalada", "quinoa"]):
                    preferencias["tipo_comida"].append("vegetariano")
                
                # Analizar ocasión
                if any(word in desc_lower for word in ["romántic", "pareja", "especial"]):
                    preferencias["ocasion"] = "romantica"
                elif any(word in desc_lower for word in ["familia", "niños", "grupo"]):
                    preferencias["ocasion"] = "familiar"
                elif any(word in desc_lower for word in ["negocio", "trabajo", "formal"]):
                    preferencias["ocasion"] = "negocio"
                
                # Analizar presupuesto
                if any(word in desc_lower for word in ["económico", "barato", "simple"]):
                    preferencias["presupuesto"] = "bajo"
                elif any(word in desc_lower for word in ["lujo", "premium", "especial"]):
                    preferencias["presupuesto"] = "alto"
                
                self.current_investigation["preferencias_cliente"] = preferencias
                return f"Preferencias analizadas: {preferencias['ocasion']}, presupuesto {preferencias['presupuesto']}"
                
            except Exception as e:
                return f"Error analizando preferencias: {str(e)}"
        
        self.investigator_tools.append(analizar_preferencias_cliente)
        
        # HERRAMIENTAS DEL AGENTE GENERADOR
        @tool
        def generar_informe_recomendacion(tipo_informe: str = "recomendacion_completa"):
            """Genera un informe estructurado basado en la investigación realizada."""
            try:
                if not self.current_investigation:
                    return "No hay datos de investigacion disponibles para generar informe."
                
                # Crear estructura del informe
                informe = {
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "tipo": tipo_informe,
                    "consulta_original": self.current_investigation.get("consulta", "N/A"),
                    "analisis_realizado": {
                        "documentos_revisados": self.current_investigation.get("documentos_encontrados", 0),
                        "preferencias_detectadas": self.current_investigation.get("preferencias_cliente", {}),
                        "recomendaciones_generadas": len(self.current_investigation.get("recomendaciones", []))
                    },
                    "recomendaciones": self.current_investigation.get("recomendaciones", []),
                    "justificacion": self.generar_justificacion(),
                    "proxima_accion": "Guardar informe en Notion"
                }
                
                self.generated_reports.append(informe)
                return f"Informe generado exitosamente. Tipo: {tipo_informe}, {len(informe['recomendaciones'])} recomendaciones incluidas."
                
            except Exception as e:
                return f"Error generando informe: {str(e)}"
        
        self.generator_tools.append(generar_informe_recomendacion)
        
        @tool
        def guardar_informe_notion():
            """Guarda el informe generado en Notion."""
            if not self.generated_reports:
                return "No hay informes generados para guardar."
            
            if not self.notion_client:
                return "Cliente de Notion no disponible. Informe guardado localmente."
            
            try:
                informe = self.generated_reports[-1]  # Último informe generado
                page_id = "28815eef-e926-8038-9583-cff88068af9e"
                
                # Crear estructura del informe en Notion
                blocks = [
                    {
                        "object": "block",
                        "type": "divider",
                        "divider": {}
                    },
                    {
                        "object": "block",
                        "type": "heading_2",
                        "heading_2": {
                            "rich_text": [{"type": "text", "text": {"content": f"[INFORME] INFORME DE RECOMENDACIÓN - {informe['timestamp']}"}}]
                        }
                    },
                    {
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [{"type": "text", "text": {"content": f"[BUSCAR] Consulta: {informe['consulta_original']}"}}]
                        }
                    },
                    {
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [{"type": "text", "text": {"content": f"[ANALISIS] Análisis: {informe['analisis_realizado']['documentos_revisados']} documentos revisados, {informe['analisis_realizado']['recomendaciones_generadas']} recomendaciones generadas"}}]
                        }
                    }
                ]
                
                # Agregar recomendaciones
                for i, rec in enumerate(informe['recomendaciones'], 1):
                    blocks.append({
                        "object": "block",
                        "type": "bulleted_list_item",
                        "bulleted_list_item": {
                            "rich_text": [{"type": "text", "text": {"content": f"{i}. {rec}"}}]
                        }
                    })
                
                # Agregar justificación
                blocks.append({
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [{"type": "text", "text": {"content": f"[IDEA] Justificación: {informe['justificacion']}"}}]
                    }
                })
                
                # Guardar en Notion
                self.notion_client.blocks.children.append(
                    block_id=page_id,
                    children=blocks
                )
                
                # También guardar localmente
                self.guardar_informe_local(informe)
                
                return "Informe guardado exitosamente en Notion y localmente."
                
            except Exception as e:
                # Fallback: guardar solo localmente
                informe = self.generated_reports[-1]
                self.guardar_informe_local(informe)
                return f"Error con Notion, guardado localmente: {str(e)}"
        
        self.generator_tools.append(guardar_informe_notion)
        
        @tool
        def generar_resumen_decision():
            """Genera un resumen de la decisión tomada por el sistema multi-agente."""
            try:
                if not self.current_investigation or not self.generated_reports:
                    return "No hay datos suficientes para generar resumen."
                
                informe = self.generated_reports[-1]
                
                resumen = {
                    "fecha": informe['timestamp'],
                    "consulta": informe['consulta_original'],
                    "decision_tomada": f"Recomendar {len(informe['recomendaciones'])} opciones específicas",
                    "agentes_involucrados": ["Investigador", "Generador"],
                    "proceso": "Búsqueda en base de conocimiento → Análisis de preferencias → Generación de informe",
                    "resultado": "Informe estructurado guardado en Notion"
                }
                
                return f"Resumen generado: {resumen['decision_tomada']} basada en analisis de {resumen['proceso']}"
                
            except Exception as e:
                return f"Error generando resumen: {str(e)}"
        
        self.generator_tools.append(generar_resumen_decision)
        
        # Asignar herramientas
        self.investigator_tools = [
            investigar_plato_detallado,
            analizar_preferencias_cliente
        ]
        
        self.generator_tools = [
            generar_informe_recomendacion,
            guardar_informe_notion,
            generar_resumen_decision
        ]
        
        print("Herramientas del sistema multi-agente configuradas.")
    
    def generar_justificacion(self):
        """Genera una justificación para las recomendaciones."""
        preferencias = self.current_investigation.get("preferencias_cliente", {})
        ocasión = preferencias.get("ocasion", "general")
        
        justificaciones = {
            "romantica": "Seleccionados platos elegantes y sofisticados perfectos para una cena romántica, con vinos que complementan la experiencia.",
            "familiar": "Recomendaciones pensadas para compartir en familia, con opciones que agradan a diferentes edades y gustos.",
            "negocio": "Platos profesionales y presentación impecable, ideales para reuniones de trabajo y networking.",
            "general": "Recomendaciones basadas en los platos más populares y mejor valorados de nuestro menú."
        }
        
        return justificaciones.get(ocasión, justificaciones["general"])
    
    def guardar_informe_local(self, informe):
        """Guarda el informe en un archivo local."""
        try:
            with open("informes_robino.json", "a", encoding="utf-8") as f:
                f.write(json.dumps(informe, ensure_ascii=False, indent=2) + "\n")
        except Exception as e:
            print(f"Error guardando informe local: {e}")
    
    def setup_multi_agent_graph(self):
        """Construir el grafo multi-agente con LangGraph"""
        
        def investigator_node(state: MultiAgentState):
            """Nodo del agente investigador"""
            system_prompt = PromptTemplate(
                input_variables=["input", "agent_scratchpad", "tools", "tool_names"],
                template="""
Eres el Agente Investigador del sistema multi-agente de La Taberna del Río.

Tu función:
1. Buscar información específica en la base de conocimiento
2. Analizar las preferencias del cliente
3. Preparar datos para el agente generador

IMPORTANTE: DEBES USAR LAS HERRAMIENTAS DISPONIBLES.

Instrucciones:
- SIEMPRE usa 'investigar_plato_detallado' para búsquedas específicas
- SIEMPRE usa 'analizar_preferencias_cliente' para entender necesidades
- NO respondas sin usar las herramientas
- Después de usar las herramientas, resume tus hallazgos
- Siempre responde en español
- Sé meticuloso en la investigación

Herramientas disponibles: {tool_names}

Input: {input}

{agent_scratchpad}
"""
            )
            
            # Crear agente con herramientas
            investigator_agent = create_react_agent(
                self.llm_investigator,
                self.investigator_tools,
                system_prompt
            )
            
            response = investigator_agent.invoke(state)
            return {"messages": [response["messages"][-1]], "current_agent": "investigator"}
        
        def generator_node(state: MultiAgentState):
            """Nodo del agente generador"""
            system_prompt = PromptTemplate(
                input_variables=["input", "agent_scratchpad", "tools", "tool_names"],
                template="""
Eres el Agente Generador de Informes del sistema multi-agente de La Taberna del Río.

Tu función:
1. Crear informes estructurados basados en la investigación
2. Generar recomendaciones personalizadas
3. Guardar informes en Notion

IMPORTANTE: DEBES USAR LAS HERRAMIENTAS DISPONIBLES.

Instrucciones:
- SIEMPRE usa 'generar_informe_recomendacion' para crear informes
- SIEMPRE usa 'guardar_informe_notion' para persistir datos
- SIEMPRE usa 'generar_resumen_decision' para resumir decisiones
- NO respondas sin usar las herramientas
- Después de usar las herramientas, proporciona un resumen claro
- Siempre responde en español
- Crea informes profesionales y estructurados

Herramientas disponibles: {tool_names}

Input: {input}

{agent_scratchpad}
"""
            )
            
            # Crear agente con herramientas
            generator_agent = create_react_agent(
                self.llm_generator,
                self.generator_tools,
                system_prompt
            )
            
            response = generator_agent.invoke(state)
            return {"messages": [response["messages"][-1]], "current_agent": "generator"}
        
        def should_use_investigator(state: MultiAgentState) -> Literal["investigator", "generator", "__end__"]:
            """Decide si usar el agente investigador"""
            last_message = state["messages"][-1].content.lower()
            
            # Palabras clave que requieren investigación
            investigacion_keywords = [
                "recomendar", "recomendación", "sugerir", "qué me recomiendas",
                "qué me sugieres", "ayuda a elegir", "no sé qué pedir",
                "romántica", "pareja", "familia", "negocio", "especial",
                "vegetariano", "vegano", "sin gluten", "alergias"
            ]
            
            if any(keyword in last_message for keyword in investigacion_keywords):
                return "investigator"
            elif "informe" in last_message or "resumen" in last_message:
                return "generator"
            else:
                return "__end__"
        
        def should_continue_investigator(state: MultiAgentState) -> Literal["tools", "generator", "__end__"]:
            """Decide si continuar con herramientas o pasar al generador"""
            if state["messages"][-1].tool_calls:
                return "tools"
            elif state["current_agent"] == "investigator":
                return "generator"
            else:
                return "__end__"
        
        def should_continue_generator(state: MultiAgentState) -> Literal["tools", "__end__"]:
            """Decide si continuar con herramientas o terminar"""
            if state["messages"][-1].tool_calls:
                return "tools"
            else:
                return "__end__"
        
        # Configurar LLMs con herramientas
        self.llm_investigator = self.llm.bind_tools(self.investigator_tools)
        self.llm_generator = self.llm.bind_tools(self.generator_tools)
        
        # Construir grafo
        graph = StateGraph(MultiAgentState)
        
        # Agregar nodos
        graph.add_node("investigator", investigator_node)
        graph.add_node("generator", generator_node)
        graph.add_node("investigator_tools", ToolNode(self.investigator_tools))
        graph.add_node("generator_tools", ToolNode(self.generator_tools))
        
        # Definir flujo
        graph.set_entry_point("investigator")
        
        # Transiciones del investigador
        graph.add_conditional_edges(
            "investigator", 
            should_continue_investigator,
            {
                "tools": "investigator_tools",
                "generator": "generator",
                "__end__": END
            }
        )
        graph.add_edge("investigator_tools", "investigator")
        
        # Transiciones del generador
        graph.add_conditional_edges(
            "generator",
            should_continue_generator,
            {
                "tools": "generator_tools",
                "__end__": END
            }
        )
        graph.add_edge("generator_tools", "generator")
        
        self.multi_agent_graph = graph.compile()
        print("Grafo multi-agente construido correctamente.")
    
    def process_complex_query(self, query: str):
        """Procesa consultas complejas usando el sistema multi-agente"""
        try:
            # Iniciar trace en LangSmith
            trace_index = self.observer.start_trace(
                "multi_agent_query",
                {
                    "query": query,
                    "timestamp": datetime.now().isoformat(),
                    "system": "multi_agent_mozo_virtual"
                }
            )
            
            self.observer.log_event(
                trace_index,
                "query_received",
                {"message": f"Consulta recibida: {query[:50]}..."}
            )
            
            # Procesar con el grafo multi-agente
            result = self.multi_agent_graph.invoke({
                "messages": [HumanMessage(content=query)],
                "current_agent": "investigator",
                "investigation_results": {},
                "report_data": {},
                "client_preferences": {}
            })
            
            response = result["messages"][-1].content
            
            # Finalizar trace
            self.observer.end_trace(
                trace_index,
                {
                    "response": response,
                    "success": True,
                    "agents_used": ["investigator", "generator"]
                }
            )
            
            return response
            
        except Exception as e:
            # Log error en trace
            if 'trace_index' in locals():
                self.observer.end_trace(
                    trace_index,
                    {
                        "error": str(e),
                        "success": False
                    }
                )
            return f"Error procesando consulta compleja: {str(e)}"


def main():
    """Función principal para probar el sistema multi-agente"""
    try:
        # Crear sistema multi-agente
        multi_agent = MultiAgentMozoVirtual()
        
        # Probar con una consulta compleja
        test_query = "¿Qué me recomiendas para una cena romántica con mi pareja?"
        print(f"[BUSCAR] Consulta de prueba: {test_query}")
        print("="*60)
        
        response = multi_agent.process_complex_query(test_query)
        print(f"[ROBINO] Respuesta del sistema multi-agente: {response}")
        
    except Exception as e:
        print(f"Error en sistema multi-agente: {e}")


if __name__ == "__main__":
    main()
