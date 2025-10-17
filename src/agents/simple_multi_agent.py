#!/usr/bin/env python3
"""
Sistema Multi-Agente Simplificado
Versión que funciona correctamente sin LangGraph complejo
"""

import os
from datetime import datetime
from typing import Dict, Any, List
from dotenv import load_dotenv

# Componentes de LangChain
from langchain_core.tools import tool
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI

# LangSmith Observer
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from observability.langsmith_observer import LangSmithObserver

class SimpleMultiAgentMozoVirtual:
    """
    Sistema Multi-Agente Simplificado para el Mozo Virtual
    - Agente Investigador: Busca información específica
    - Agente Generador: Crea informes estructurados
    """
    
    def __init__(self, vectorstore=None, notion_client=None):
        """Inicializar el sistema multi-agente simplificado"""
        self.setup_environment()
        self.setup_llm()
        self.vectorstore = vectorstore
        self.notion_client = notion_client
        
        # Estado del sistema
        self.current_investigation = {}
        self.generated_reports = []
        
        # LangSmith Observer
        self.observer = LangSmithObserver()
        
        print("Sistema multi-agente simplificado inicializado correctamente.")
        
    def setup_environment(self):
        """Cargar variables de entorno"""
        load_dotenv()
        if not os.getenv("GEMINI_API_KEY"):
            raise ValueError("La variable de entorno GEMINI_API_KEY no está definida.")
        
        print("Variables de entorno cargadas para sistema multi-agente simplificado.")
    
    def setup_llm(self):
        """Configurar el modelo de lenguaje Gemini"""
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            google_api_key=os.getenv("GEMINI_API_KEY"), 
            temperature=0.7
        )
        print("Modelo Gemini configurado para sistema multi-agente simplificado.")
    
    def investigar_plato_detallado(self, consulta: str) -> str:
        """Investiga información detallada sobre platos específicos del menú."""
        if not self.vectorstore:
            # Simular búsqueda si no hay vectorstore
            resultados = {
                "consulta": consulta,
                "documentos_encontrados": 3,
                "informacion": [
                    {
                        "contenido": "Solomillo de Ternera - Corte premium, cocción perfecta, acompañado de salsa de vino tinto",
                        "fuente": "menu_principales"
                    },
                    {
                        "contenido": "Rioja Reserva - Vino tinto español, perfecto maridaje para carnes rojas",
                        "fuente": "menu_bebidas"
                    },
                    {
                        "contenido": "Crema Catalana - Postre tradicional, crujiente caramelo, crema suave",
                        "fuente": "menu_postres"
                    }
                ],
                "recomendaciones": []
            }
        else:
            try:
                # Buscar información relevante
                retriever = self.vectorstore.as_retriever(search_kwargs={"k": 5})
                docs = retriever.get_relevant_documents(consulta)
                
                if not docs:
                    return f"No se encontró información específica sobre: {consulta}"
                
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
            
            except Exception as e:
                return f"Error en la investigación: {str(e)}"
        
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
        return f"Investigación completada. Encontrados {resultados['documentos_encontrados']} documentos relevantes."
    
    def analizar_preferencias_cliente(self, descripcion: str) -> str:
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
    
    def generar_informe_recomendacion(self, tipo_informe: str = "recomendacion_completa") -> str:
        """Genera un informe estructurado basado en la investigación realizada."""
        try:
            if not self.current_investigation:
                return "No hay datos de investigación disponibles para generar informe."
            
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
    
    def generar_justificacion(self) -> str:
        """Genera justificación para las recomendaciones."""
        if not self.current_investigation:
            return "No hay datos suficientes para generar justificación."
        
        preferencias = self.current_investigation.get("preferencias_cliente", {})
        ocasión = preferencias.get("ocasion", "general")
        
        justificaciones = {
            "romantica": "Recomendaciones pensadas para una ocasión especial, con platos elegantes y maridajes perfectos.",
            "familiar": "Recomendaciones pensadas para compartir en familia, con opciones que agradan a diferentes edades y gustos.",
            "negocio": "Platos profesionales y presentación impecable, ideales para reuniones de trabajo y networking.",
            "general": "Recomendaciones basadas en los platos más populares y mejor valorados de nuestro menú."
        }
        
        return justificaciones.get(ocasión, justificaciones["general"])
    
    def generar_resumen_decision(self) -> str:
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
                "resultado": "Informe estructurado generado exitosamente"
            }
            
            return f"Resumen generado: {resumen['decision_tomada']} basada en análisis de {resumen['proceso']}"
            
        except Exception as e:
            return f"Error generando resumen: {str(e)}"
    
    def process_complex_query(self, query: str) -> str:
        """Procesa consultas complejas usando el sistema multi-agente simplificado"""
        try:
            # Iniciar trace en LangSmith
            trace_index = self.observer.start_trace(
                "simple_multi_agent_query",
                {
                    "query": query,
                    "timestamp": datetime.now().isoformat(),
                    "system": "simple_multi_agent_mozo_virtual"
                }
            )
            
            self.observer.log_event(
                trace_index,
                "query_received",
                {"message": f"Consulta recibida: {query[:50]}..."}
            )
            
            # PASO 1: Investigación
            self.observer.log_event(
                trace_index,
                "investigation_start",
                {"message": "Iniciando investigación con agente investigador"}
            )
            
            investigacion_result = self.investigar_plato_detallado(query)
            self.observer.log_event(
                trace_index,
                "investigation_complete",
                {"message": f"Investigación completada: {investigacion_result}"}
            )
            
            # PASO 2: Análisis de preferencias
            self.observer.log_event(
                trace_index,
                "preferences_analysis_start",
                {"message": "Iniciando análisis de preferencias"}
            )
            
            preferencias_result = self.analizar_preferencias_cliente(query)
            self.observer.log_event(
                trace_index,
                "preferences_analysis_complete",
                {"message": f"Análisis de preferencias completado: {preferencias_result}"}
            )
            
            # PASO 3: Generación de informe
            self.observer.log_event(
                trace_index,
                "report_generation_start",
                {"message": "Iniciando generación de informe"}
            )
            
            informe_result = self.generar_informe_recomendacion()
            self.observer.log_event(
                trace_index,
                "report_generation_complete",
                {"message": f"Generación de informe completada: {informe_result}"}
            )
            
            # PASO 4: Resumen final
            resumen_result = self.generar_resumen_decision()
            
            # Construir respuesta final
            recomendaciones = self.current_investigation.get("recomendaciones", [])
            if recomendaciones:
                response = f"""
¡Perfecto! He analizado tu solicitud de "{query}" y tengo recomendaciones especiales para ti:

**RECOMENDACIONES PERSONALIZADAS:**

"""
                for i, rec in enumerate(recomendaciones, 1):
                    response += f"{i}. **{rec}**\n"
                
                response += f"""
**ANÁLISIS REALIZADO:**
- {preferencias_result}
- {resumen_result}

¿Te gustaría que guarde este informe en nuestro sistema o necesitas más detalles sobre alguna recomendación?
"""
            else:
                response = "He analizado tu consulta pero necesito más información específica. ¿Podrías darme más detalles sobre tus preferencias?"
            
            # Finalizar trace
            self.observer.end_trace(
                trace_index,
                {
                    "response": response,
                    "success": True,
                    "agents_used": ["investigator", "generator"],
                    "recommendations_count": len(recomendaciones)
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
    """Función principal para probar el sistema multi-agente simplificado"""
    try:
        print("=== SISTEMA MULTI-AGENTE SIMPLIFICADO ===")
        
        # Crear sistema multi-agente
        multi_agent = SimpleMultiAgentMozoVirtual()
        
        # Test de consulta compleja
        query = "¿Qué me recomiendas para una cena romántica?"
        print(f"\nConsulta: {query}")
        
        response = multi_agent.process_complex_query(query)
        print(f"\nRespuesta:\n{response}")
        
        # Verificar estado interno
        print(f"\nEstado interno:")
        print(f"- Investigación: {multi_agent.current_investigation}")
        print(f"- Reportes generados: {len(multi_agent.generated_reports)}")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] {e}")
        return False


if __name__ == "__main__":
    main()
