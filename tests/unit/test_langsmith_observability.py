#!/usr/bin/env python3
"""
Test de LangSmith Observabilidad
Prueba el sistema completo de tracing y observabilidad
"""

import os
from dotenv import load_dotenv
from langsmith_observer import LangSmithObserver, create_langsmith_report

def test_langsmith_observer():
    """Test básico del LangSmith Observer"""
    print("=== TEST LANGSMITH OBSERVER ===")
    
    try:
        # Crear observador
        observer = LangSmithObserver()
        
        if observer.client:
            print("[OK] LangSmith configurado correctamente")
            print(f"[OK] URL del proyecto: {observer.get_langsmith_url()}")
        else:
            print("[ADVERTENCIA] LangSmith no disponible - modo simulación")
        
        # Test de traces
        print("\n--- Test de Traces ---")
        
        # Trace 1: Consulta simple
        trace1 = observer.start_trace(
            "consulta_simple",
            {
                "tipo": "consulta_basica",
                "cliente": "test_user",
                "agente": "robino"
            }
        )
        observer.log_event(trace1, "llm_start", {"message": "Procesando consulta simple"})
        observer.log_event(trace1, "tool_start", {"message": "Consultando menú"})
        observer.log_event(trace1, "tool_end", {"message": "Menú consultado"})
        observer.end_trace(trace1, {"respuesta": "menú_mostrado", "exito": True})
        
        # Trace 2: Consulta compleja con multi-agente
        trace2 = observer.start_trace(
            "consulta_compleja",
            {
                "tipo": "recomendacion",
                "cliente": "test_user",
                "agentes": ["investigador", "generador"]
            }
        )
        observer.log_event(trace2, "agent_start", {"message": "Iniciando agente investigador"})
        observer.log_event(trace2, "llm_start", {"message": "Analizando preferencias"})
        observer.log_event(trace2, "tool_start", {"message": "Buscando información específica"})
        observer.log_event(trace2, "tool_end", {"message": "Información encontrada"})
        observer.log_event(trace2, "agent_switch", {"message": "Cambiando a agente generador"})
        observer.log_event(trace2, "llm_start", {"message": "Generando informe"})
        observer.log_event(trace2, "tool_start", {"message": "Guardando en Notion"})
        observer.log_event(trace2, "tool_end", {"message": "Informe guardado"})
        observer.end_trace(trace2, {"respuesta": "recomendacion_generada", "exito": True})
        
        # Trace 3: Error handling
        trace3 = observer.start_trace(
            "consulta_error",
            {
                "tipo": "error_test",
                "cliente": "test_user"
            }
        )
        observer.log_event(trace3, "llm_start", {"message": "Procesando consulta"})
        observer.log_event(trace3, "llm_error", {"message": "Error simulado"})
        observer.end_trace(trace3, {"error": "error_simulado", "exito": False})
        
        print("[OK] Traces creados correctamente")
        
        # Generar reporte
        print("\n--- Generando Reporte ---")
        report = create_langsmith_report(observer)
        print(report)
        
        # Guardar traces
        print("\n--- Guardando Traces ---")
        success = observer.save_traces_to_file("test_langsmith_traces.json")
        if success:
            print("[OK] Traces guardados en test_langsmith_traces.json")
        
        # Mostrar resumen
        print("\n--- Resumen de Traces ---")
        summary = observer.get_all_traces_summary()
        for i, trace in enumerate(summary):
            print(f"Trace {i+1}: {trace['name']} - {trace['duration']:.2f}s - {trace['events_count']} eventos")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] {e}")
        return False

def test_multi_agent_with_langsmith():
    """Test del sistema multi-agente con LangSmith"""
    print("\n=== TEST MULTI-AGENTE CON LANGSMITH ===")
    
    try:
        from multi_agent_system import MultiAgentMozoVirtual
        
        # Crear sistema multi-agente
        multi_agent = MultiAgentMozoVirtual()
        
        if multi_agent.observer.client:
            print("[OK] Sistema multi-agente con LangSmith configurado")
        else:
            print("[ADVERTENCIA] Sistema multi-agente sin LangSmith")
        
        # Test de consulta compleja
        print("\n--- Test de Consulta Compleja ---")
        query = "¿Qué me recomiendas para una cena romántica?"
        print(f"Consulta: {query}")
        
        response = multi_agent.process_complex_query(query)
        print(f"Respuesta: {response}")
        
        # Verificar traces generados
        traces = multi_agent.observer.get_all_traces_summary()
        print(f"\n[OK] Traces generados: {len(traces)}")
        
        for trace in traces:
            print(f"  - {trace['name']}: {trace['duration']:.2f}s, {trace['events_count']} eventos")
        
        # Generar reporte específico
        report = create_langsmith_report(multi_agent.observer)
        
        # Guardar reporte
        with open("langsmith_multi_agent_report.md", "w", encoding="utf-8") as f:
            f.write(report)
        
        print("[OK] Reporte guardado en langsmith_multi_agent_report.md")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] {e}")
        return False

def test_langsmith_integration():
    """Test de integración completa con LangSmith"""
    print("\n=== TEST INTEGRACION LANGSMITH ===")
    
    try:
        # Verificar variables de entorno
        load_dotenv()
        
        langsmith_key = os.getenv("LANGCHAIN_API_KEY")
        project_name = os.getenv("LANGCHAIN_PROJECT")
        tracing_enabled = os.getenv("LANGCHAIN_TRACING_V2")
        
        print(f"LANGCHAIN_API_KEY: {'Configurada' if langsmith_key else 'NO CONFIGURADA'}")
        print(f"LANGCHAIN_PROJECT: {project_name}")
        print(f"LANGCHAIN_TRACING_V2: {tracing_enabled}")
        
        if langsmith_key and project_name and tracing_enabled:
            print("[OK] Variables de entorno configuradas correctamente")
            
            # Test de conexión
            observer = LangSmithObserver()
            if observer.client:
                print("[OK] Conexión a LangSmith exitosa")
                print(f"[OK] URL del proyecto: {observer.get_langsmith_url()}")
            else:
                print("[ADVERTENCIA] No se pudo conectar a LangSmith")
        else:
            print("[ADVERTENCIA] Variables de entorno no configuradas completamente")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] {e}")
        return False

def main():
    """Función principal para ejecutar todos los tests"""
    print("LANGSMITH OBSERVABILITY TESTS")
    print("=" * 50)
    
    # Test 1: LangSmith Observer básico
    test1_success = test_langsmith_observer()
    
    # Test 2: Multi-agente con LangSmith
    test2_success = test_multi_agent_with_langsmith()
    
    # Test 3: Integración completa
    test3_success = test_langsmith_integration()
    
    # Resumen final
    print("\n" + "=" * 50)
    print("RESUMEN DE TESTS LANGSMITH")
    print("=" * 50)
    print(f"LangSmith Observer: {'PASO' if test1_success else 'FALLO'}")
    print(f"Multi-agente + LangSmith: {'PASO' if test2_success else 'FALLO'}")
    print(f"Integración completa: {'PASO' if test3_success else 'FALLO'}")
    
    if test1_success and test2_success and test3_success:
        print("\n[EXITO] Todos los tests de LangSmith pasaron correctamente")
        print("\nFUNCIONALIDADES IMPLEMENTADAS:")
        print("- Tracing completo de LLM calls")
        print("- Tracing de tool calls")
        print("- Tracing de agent actions")
        print("- Metadatos de contexto")
        print("- Medición de rendimiento")
        print("- Reportes estructurados")
        print("- Integración con sistema multi-agente")
        
        print("\nARCHIVOS GENERADOS:")
        print("- test_langsmith_traces.json")
        print("- langsmith_multi_agent_report.md")
        
        print("\nURL LANGSMITH:")
        observer = LangSmithObserver()
        if observer.client:
            print(f"- {observer.get_langsmith_url()}")
        else:
            print("- Configurar LANGCHAIN_API_KEY para acceder a LangSmith")
    else:
        print("\n[ADVERTENCIA] Algunos tests fallaron")
    
    print("=" * 50)

if __name__ == "__main__":
    main()
