#!/usr/bin/env python3
"""
LangSmith Observer - Sistema de Observabilidad
Configura y gestiona el tracing completo del sistema multi-agente
"""

import os
import json
from datetime import datetime
from typing import Dict, Any, List
from dotenv import load_dotenv

# LangSmith imports
from langsmith import Client
from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.outputs import LLMResult
from langchain_core.agents import AgentAction, AgentFinish

class LangSmithObserver:
    """
    Observador LangSmith para el sistema multi-agente
    Maneja el tracing completo y análisis de rendimiento
    """
    
    def __init__(self):
        """Inicializar el observador LangSmith"""
        self.setup_langsmith()
        self.setup_callback_handler()
        self.traces_data = []
        
    def setup_langsmith(self):
        """Configurar LangSmith para tracing"""
        load_dotenv()
        
        # Configurar variables de entorno para LangSmith
        os.environ["LANGCHAIN_TRACING_V2"] = "true"
        os.environ["LANGCHAIN_PROJECT"] = "proyecto-final-agentes"
        os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
        
        # Verificar API key
        self.langsmith_api_key = os.getenv("LANGCHAIN_API_KEY")
        if not self.langsmith_api_key:
            print("[ADVERTENCIA] LANGCHAIN_API_KEY no configurada. LangSmith no estará disponible.")
            self.client = None
            return
        
        try:
            self.client = Client(api_url="https://api.smith.langchain.com")
            print("[OK] LangSmith configurado correctamente")
        except Exception as e:
            print(f"[ERROR] Error configurando LangSmith: {e}")
            self.client = None
    
    def setup_callback_handler(self):
        """Configurar callback handler personalizado"""
        self.callback_handler = CustomCallbackHandler(self)
    
    def start_trace(self, trace_name: str, metadata: Dict[str, Any] = None):
        """Iniciar un nuevo trace"""
        trace_info = {
            "name": trace_name,
            "start_time": datetime.now(),
            "metadata": metadata or {},
            "events": []
        }
        self.traces_data.append(trace_info)
        print(f"[TRACE] Iniciado: {trace_name}")
        return len(self.traces_data) - 1
    
    def log_event(self, trace_index: int, event_type: str, data: Dict[str, Any]):
        """Registrar un evento en el trace"""
        if trace_index < len(self.traces_data):
            event = {
                "timestamp": datetime.now(),
                "type": event_type,
                "data": data
            }
            self.traces_data[trace_index]["events"].append(event)
            print(f"[TRACE] Evento {event_type}: {data.get('message', 'Sin mensaje')}")
    
    def end_trace(self, trace_index: int, result: Dict[str, Any] = None):
        """Finalizar un trace"""
        if trace_index < len(self.traces_data):
            self.traces_data[trace_index]["end_time"] = datetime.now()
            self.traces_data[trace_index]["result"] = result or {}
            
            # Calcular duración
            start = self.traces_data[trace_index]["start_time"]
            end = self.traces_data[trace_index]["end_time"]
            duration = (end - start).total_seconds()
            self.traces_data[trace_index]["duration"] = duration
            
            print(f"[TRACE] Finalizado: {self.traces_data[trace_index]['name']} ({duration:.2f}s)")
    
    def get_trace_summary(self, trace_index: int) -> Dict[str, Any]:
        """Obtener resumen de un trace"""
        if trace_index >= len(self.traces_data):
            return {}
        
        trace = self.traces_data[trace_index]
        return {
            "name": trace["name"],
            "duration": trace.get("duration", 0),
            "events_count": len(trace["events"]),
            "metadata": trace["metadata"],
            "result": trace.get("result", {})
        }
    
    def get_all_traces_summary(self) -> List[Dict[str, Any]]:
        """Obtener resumen de todos los traces"""
        return [self.get_trace_summary(i) for i in range(len(self.traces_data))]
    
    def save_traces_to_file(self, filename: str = "langsmith_traces.json"):
        """Guardar traces en archivo JSON"""
        try:
            # Convertir datetime a string para JSON
            traces_for_json = []
            for trace in self.traces_data:
                trace_copy = trace.copy()
                trace_copy["start_time"] = trace_copy["start_time"].isoformat()
                if "end_time" in trace_copy:
                    trace_copy["end_time"] = trace_copy["end_time"].isoformat()
                
                # Convertir eventos
                for event in trace_copy["events"]:
                    event["timestamp"] = event["timestamp"].isoformat()
                
                traces_for_json.append(trace_copy)
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(traces_for_json, f, indent=2, ensure_ascii=False)
            
            print(f"[OK] Traces guardados en {filename}")
            return True
        except Exception as e:
            print(f"[ERROR] Error guardando traces: {e}")
            return False
    
    def get_langsmith_url(self) -> str:
        """Obtener URL del proyecto en LangSmith"""
        if self.client:
            return "https://smith.langchain.com/projects/proyecto-final-agentes"
        return "LangSmith no configurado"


class CustomCallbackHandler(BaseCallbackHandler):
    """
    Callback handler personalizado para LangSmith
    Registra eventos detallados del sistema multi-agente
    """
    
    def __init__(self, observer: LangSmithObserver):
        super().__init__()
        self.observer = observer
        self.current_trace = None
    
    def on_llm_start(self, serialized: Dict[str, Any], prompts: List[str], **kwargs) -> None:
        """Callback cuando inicia LLM"""
        self.observer.log_event(
            self.current_trace,
            "llm_start",
            {
                "model": serialized.get("name", "unknown"),
                "prompts_count": len(prompts),
                "message": f"LLM iniciado: {serialized.get('name', 'unknown')}"
            }
        )
    
    def on_llm_end(self, response: LLMResult, **kwargs) -> None:
        """Callback cuando termina LLM"""
        self.observer.log_event(
            self.current_trace,
            "llm_end",
            {
                "generations_count": len(response.generations),
                "message": "LLM completado"
            }
        )
    
    def on_llm_error(self, error: Exception, **kwargs) -> None:
        """Callback cuando hay error en LLM"""
        self.observer.log_event(
            self.current_trace,
            "llm_error",
            {
                "error": str(error),
                "message": f"Error en LLM: {str(error)}"
            }
        )
    
    def on_tool_start(self, serialized: Dict[str, Any], input_str: str, **kwargs) -> None:
        """Callback cuando inicia herramienta"""
        self.observer.log_event(
            self.current_trace,
            "tool_start",
            {
                "tool_name": serialized.get("name", "unknown"),
                "input": input_str,
                "message": f"Herramienta iniciada: {serialized.get('name', 'unknown')}"
            }
        )
    
    def on_tool_end(self, output: str, **kwargs) -> None:
        """Callback cuando termina herramienta"""
        self.observer.log_event(
            self.current_trace,
            "tool_end",
            {
                "output": output,
                "message": "Herramienta completada"
            }
        )
    
    def on_tool_error(self, error: Exception, **kwargs) -> None:
        """Callback cuando hay error en herramienta"""
        self.observer.log_event(
            self.current_trace,
            "tool_error",
            {
                "error": str(error),
                "message": f"Error en herramienta: {str(error)}"
            }
        )
    
    def on_agent_action(self, action: AgentAction, **kwargs) -> None:
        """Callback cuando agente ejecuta acción"""
        self.observer.log_event(
            self.current_trace,
            "agent_action",
            {
                "tool": action.tool,
                "tool_input": action.tool_input,
                "log": action.log,
                "message": f"Acción del agente: {action.tool}"
            }
        )
    
    def on_agent_finish(self, finish: AgentFinish, **kwargs) -> None:
        """Callback cuando agente termina"""
        self.observer.log_event(
            self.current_trace,
            "agent_finish",
            {
                "return_values": finish.return_values,
                "log": finish.log,
                "message": "Agente completado"
            }
        )


def create_langsmith_report(observer: LangSmithObserver) -> str:
    """Crear reporte de LangSmith"""
    traces_summary = observer.get_all_traces_summary()
    
    report = f"""
# REPORTE LANGSMITH - SISTEMA MULTI-AGENTE

## Información del Proyecto
- **Proyecto**: proyecto-final-agentes
- **URL LangSmith**: {observer.get_langsmith_url()}
- **Fecha**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Resumen de Traces
- **Total de Traces**: {len(traces_summary)}

## Detalles por Trace
"""
    
    for i, trace in enumerate(traces_summary):
        report += f"""
### Trace {i+1}: {trace['name']}
- **Duración**: {trace['duration']:.2f} segundos
- **Eventos**: {trace['events_count']}
- **Metadatos**: {trace['metadata']}
- **Resultado**: {trace['result']}
"""
    
    report += f"""
## Análisis de Rendimiento
- **Tiempo Total**: {sum(t['duration'] for t in traces_summary):.2f} segundos
- **Promedio por Trace**: {sum(t['duration'] for t in traces_summary) / len(traces_summary) if traces_summary else 0:.2f} segundos
- **Traces más Largos**: {sorted(traces_summary, key=lambda x: x['duration'], reverse=True)[:3]}

## Observabilidad Implementada
- Tracing de LLM calls
- Tracing de tool calls
- Tracing de agent actions
- Metadatos de contexto
- Medición de rendimiento
- Reportes estructurados
"""
    
    return report


def main():
    """Función principal para probar LangSmith Observer"""
    print("INICIANDO LANGSMITH OBSERVER")
    print("=" * 50)
    
    # Crear observador
    observer = LangSmithObserver()
    
    if not observer.client:
        print("LangSmith no disponible - usando modo simulación")
    
    # Simular algunos traces
    trace1 = observer.start_trace("test_multi_agent", {"tipo": "test", "agente": "investigador"})
    observer.log_event(trace1, "llm_start", {"message": "Iniciando investigación"})
    observer.log_event(trace1, "tool_start", {"message": "Ejecutando herramienta de búsqueda"})
    observer.log_event(trace1, "tool_end", {"message": "Búsqueda completada"})
    observer.end_trace(trace1, {"resultado": "investigacion_exitosa"})
    
    trace2 = observer.start_trace("test_generator", {"tipo": "test", "agente": "generador"})
    observer.log_event(trace2, "llm_start", {"message": "Generando informe"})
    observer.log_event(trace2, "tool_start", {"message": "Guardando en Notion"})
    observer.end_trace(trace2, {"resultado": "informe_generado"})
    
    # Generar reporte
    report = create_langsmith_report(observer)
    print(report)
    
    # Guardar traces
    observer.save_traces_to_file()
    
    print("LANGSMITH OBSERVER CONFIGURADO CORRECTAMENTE")


if __name__ == "__main__":
    main()
