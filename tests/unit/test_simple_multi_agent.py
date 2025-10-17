#!/usr/bin/env python3
"""
Test Simple del Sistema Multi-Agente
Diagnóstico básico para identificar problemas
"""

import os
from dotenv import load_dotenv

def test_basic_initialization():
    """Test básico de inicialización"""
    print("=== TEST BASICO DE INICIALIZACION ===")
    
    try:
        load_dotenv()
        
        # Verificar variables de entorno
        gemini_key = os.getenv("GEMINI_API_KEY")
        notion_key = os.getenv("NOTION_API_KEY")
        
        print(f"GEMINI_API_KEY: {'Configurada' if gemini_key else 'NO CONFIGURADA'}")
        print(f"NOTION_API_KEY: {'Configurada' if notion_key else 'NO CONFIGURADA'}")
        
        if not gemini_key:
            print("ERROR: GEMINI_API_KEY no está configurada")
            return False
            
        # Test de importación
        print("Importando MultiAgentMozoVirtual...")
        from multi_agent_system import MultiAgentMozoVirtual
        print("Importación exitosa")
        
        # Test de inicialización
        print("Inicializando sistema multi-agente...")
        multi_agent = MultiAgentMozoVirtual()
        print("Inicialización exitosa")
        
        return True
        
    except Exception as e:
        print(f"ERROR: {e}")
        return False

def test_simple_query():
    """Test de consulta simple"""
    print("\n=== TEST DE CONSULTA SIMPLE ===")
    
    try:
        from multi_agent_system import MultiAgentMozoVirtual
        
        multi_agent = MultiAgentMozoVirtual()
        
        # Consulta muy simple
        query = "Hola"
        print(f"Consulta: {query}")
        
        response = multi_agent.process_complex_query(query)
        print(f"Respuesta: '{response}'")
        
        if response and len(response.strip()) > 0:
            print("RESPUESTA OBTENIDA")
            return True
        else:
            print("NO SE OBTUVO RESPUESTA")
            return False
            
    except Exception as e:
        print(f"ERROR: {e}")
        return False

def test_tools_directly():
    """Test directo de las herramientas"""
    print("\n=== TEST DIRECTO DE HERRAMIENTAS ===")
    
    try:
        from multi_agent_system import MultiAgentMozoVirtual
        
        multi_agent = MultiAgentMozoVirtual()
        
        # Test herramienta investigar_plato_detallado
        print("Probando herramienta investigar_plato_detallado...")
        result = multi_agent.investigator_tools[0].invoke({"consulta": "paella"})
        print(f"Resultado: {result}")
        
        # Test herramienta analizar_preferencias_cliente
        print("Probando herramienta analizar_preferencias_cliente...")
        result = multi_agent.investigator_tools[1].invoke({"descripcion": "cena romantica"})
        print(f"Resultado: {result}")
        
        return True
        
    except Exception as e:
        print(f"ERROR: {e}")
        return False

def main():
    """Función principal"""
    print("DIAGNOSTICO DEL SISTEMA MULTI-AGENTE")
    print("=" * 50)
    
    # Test 1: Inicialización
    test1 = test_basic_initialization()
    
    if test1:
        # Test 2: Consulta simple
        test2 = test_simple_query()
        
        # Test 3: Herramientas directas
        test3 = test_tools_directly()
        
        print("\n" + "=" * 50)
        print("RESULTADOS:")
        print(f"Inicializacion: {'OK' if test1 else 'FALLO'}")
        print(f"Consulta Simple: {'OK' if test2 else 'FALLO'}")
        print(f"Herramientas: {'OK' if test3 else 'FALLO'}")
    else:
        print("\nFALLO EN INICIALIZACION - Revisar configuración")

if __name__ == "__main__":
    main()


