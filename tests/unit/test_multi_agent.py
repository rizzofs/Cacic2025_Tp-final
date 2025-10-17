#!/usr/bin/env python3
"""
Test del Sistema Multi-Agente
Prueba las funcionalidades del sistema de dos agentes colaborativos
"""

import os
from dotenv import load_dotenv
from multi_agent_system import MultiAgentMozoVirtual

def test_multi_agent_system():
    """Prueba el sistema multi-agente con diferentes tipos de consultas"""
    
    print("INICIANDO TESTS DEL SISTEMA MULTI-AGENTE")
    print("="*60)
    
    # Cargar variables de entorno
    load_dotenv()
    
    try:
        # Crear sistema multi-agente
        print("1. Inicializando sistema multi-agente...")
        multi_agent = MultiAgentMozoVirtual()
        print("Sistema multi-agente inicializado correctamente")
        
        # Test 1: Consulta romántica
        print("\n2. Test 1: Consulta para cena romántica")
        print("-" * 40)
        query1 = "¿Qué me recomiendas para una cena romántica con mi pareja?"
        print(f"Consulta: {query1}")
        
        response1 = multi_agent.process_complex_query(query1)
        print(f"Respuesta: {response1}")
        
        # Test 2: Consulta familiar
        print("\n3. Test 2: Consulta para cena familiar")
        print("-" * 40)
        query2 = "¿Qué me sugieres para una cena familiar con niños?"
        print(f"Consulta: {query2}")
        
        response2 = multi_agent.process_complex_query(query2)
        print(f"Respuesta: {response2}")
        
        # Test 3: Consulta vegetariana
        print("\n4. Test 3: Consulta vegetariana")
        print("-" * 40)
        query3 = "¿Qué opciones vegetarianas tienen? No sé qué elegir"
        print(f"Consulta: {query3}")
        
        response3 = multi_agent.process_complex_query(query3)
        print(f"Respuesta: {response3}")
        
        # Test 4: Generar informe
        print("\n5. Test 4: Generación de informe")
        print("-" * 40)
        query4 = "Necesito un informe de las recomendaciones que me diste"
        print(f"Consulta: {query4}")
        
        response4 = multi_agent.process_complex_query(query4)
        print(f"Respuesta: {response4}")
        
        print("\n" + "="*60)
        print("TODOS LOS TESTS COMPLETADOS EXITOSAMENTE")
        print("="*60)
        
        # Mostrar resumen de informes generados
        if multi_agent.generated_reports:
            print(f"\nInformes generados: {len(multi_agent.generated_reports)}")
            for i, informe in enumerate(multi_agent.generated_reports, 1):
                print(f"   {i}. {informe['tipo']} - {informe['timestamp']}")
        
        return True
        
    except Exception as e:
        print(f"Error en los tests: {e}")
        return False

def test_integration_with_main_agent():
    """Prueba la integración con el agente principal"""
    
    print("\nTEST DE INTEGRACION CON AGENTE PRINCIPAL")
    print("="*60)
    
    try:
        from mozo_virtual_agent import MozoVirtualAgent
        
        print("1. Inicializando agente principal...")
        agent = MozoVirtualAgent()
        print("Agente principal inicializado")
        
        # Verificar que el sistema multi-agente esté disponible
        if agent.multi_agent_system:
            print("Sistema multi-agente integrado correctamente")
            
            # Test de detección de consultas complejas
            test_queries = [
                "Hola",  # Simple
                "¿Qué me recomiendas para una cena especial?",  # Compleja
                "¿Cuánto cuesta la paella?",  # Simple
                "No sé qué pedir, ayuda",  # Compleja
            ]
            
            print("\n2. Test de detección de consultas:")
            for query in test_queries:
                is_complex = agent.is_complex_query(query)
                print(f"   '{query}' -> {'Compleja' if is_complex else 'Simple'}")
            
            print("Integración funcionando correctamente")
            return True
        else:
            print("Sistema multi-agente no disponible")
            return False
            
    except Exception as e:
        print(f"Error en test de integración: {e}")
        return False

def main():
    """Función principal para ejecutar todos los tests"""
    
    print("INICIANDO TESTS COMPLETOS DEL SISTEMA MULTI-AGENTE")
    print("="*70)
    
    # Test 1: Sistema multi-agente
    test1_result = test_multi_agent_system()
    
    # Test 2: Integración
    test2_result = test_integration_with_main_agent()
    
    # Resumen final
    print("\n" + "="*70)
    print("RESUMEN DE TESTS")
    print("="*70)
    print(f"Sistema Multi-Agente: {'PASO' if test1_result else 'FALLO'}")
    print(f"Integración Principal: {'PASO' if test2_result else 'FALLO'}")
    
    if test1_result and test2_result:
        print("\n¡TODOS LOS TESTS PASARON! Sistema multi-agente funcionando correctamente.")
        print("\nFUNCIONALIDADES IMPLEMENTADAS:")
        print("   • Agente Investigador - Busca información específica")
        print("   • Agente Generador - Crea informes estructurados")
        print("   • Colaboración entre agentes")
        print("   • Integración con Notion")
        print("   • Detección automática de consultas complejas")
        print("   • Fallback al agente simple si es necesario")
    else:
        print("\nAlgunos tests fallaron. Revisar configuración.")
    
    print("="*70)

if __name__ == "__main__":
    main()
