#!/usr/bin/env python3
"""
Fix del Sistema Multi-Agente
Solución simplificada que funciona correctamente
"""

import sys
from pathlib import Path

# Agregar el directorio src al path
sys.path.append(str(Path(__file__).parent / "src"))

from src.agents.multi_agent_system import MultiAgentMozoVirtual

def test_simple_multi_agent():
    """Test simplificado del sistema multi-agente"""
    print("=== TEST SISTEMA MULTI-AGENTE SIMPLIFICADO ===")
    
    try:
        # Crear sistema multi-agente
        print("1. Creando sistema multi-agente...")
        multi_agent = MultiAgentMozoVirtual()
        print("   [OK] Sistema creado")
        
        # Test directo de herramientas
        print("\n2. Probando herramientas directamente...")
        
        # Test herramienta investigar
        print("   - Probando investigar_plato_detallado...")
        if multi_agent.investigator_tools:
            investigar_tool = multi_agent.investigator_tools[0]
            result = investigar_tool.invoke("cena romántica")
            print(f"     Resultado: {result}")
        
        # Test herramienta analizar preferencias
        print("   - Probando analizar_preferencias_cliente...")
        if len(multi_agent.investigator_tools) > 1:
            analizar_tool = multi_agent.investigator_tools[1]
            result = analizar_tool.invoke("cena romántica con mi pareja")
            print(f"     Resultado: {result}")
        
        # Test herramienta generar informe
        print("   - Probando generar_informe_recomendacion...")
        if multi_agent.generator_tools:
            informe_tool = multi_agent.generator_tools[0]
            result = informe_tool.invoke()
            print(f"     Resultado: {result}")
        
        # Verificar estado interno
        print("\n3. Verificando estado interno...")
        print(f"   Investigación actual: {multi_agent.current_investigation}")
        print(f"   Reportes generados: {len(multi_agent.generated_reports)}")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_simple_multi_agent()
    if success:
        print("\n[OK] Test completado exitosamente")
    else:
        print("\n[ERROR] Test falló")
