#!/usr/bin/env python3
"""
Sistema Mozo Virtual - Punto de Entrada Principal
Proyecto Final Integrador - CACIC 2025
"""

import sys
import os
from pathlib import Path

# Agregar el directorio src al path
sys.path.append(str(Path(__file__).parent / "src"))

from config.settings import settings
from src.agents import MozoVirtualAgent

def main():
    """Función principal del sistema"""
    print("=" * 60)
    print("[ROBOT] SISTEMA MOZO VIRTUAL - PROYECTO FINAL CACIC 2025")
    print("=" * 60)
    print(f"Versión: {settings.__version__ if hasattr(settings, '__version__') else '1.0.0'}")
    print(f"LangSmith: {settings.get_langsmith_url()}")
    print(f"Notion: {settings.get_notion_url()}")
    print("=" * 60)
    
    try:
        # Validar configuración
        settings.validate_config()
        print("[OK] Configuración validada correctamente")
        
        # Inicializar agente
        print("[INICIANDO] Sistema Mozo Virtual...")
        agent = MozoVirtualAgent()
        
        print("[OK] Sistema inicializado correctamente")
        print("\n[TARGET] FUNCIONALIDADES DISPONIBLES:")
        print("- Sistema multi-agente con colaboración")
        print("- Base de conocimiento RAG avanzada")
        print("- Integración con Notion para persistencia")
        print("- Observabilidad completa con LangSmith")
        print("- Tracing y análisis de rendimiento")
        
        print("\n[START] Iniciando conversación...")
        agent.start_conversation()
        
    except Exception as e:
        print(f"[ERROR] Error inicializando el sistema: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
