#!/usr/bin/env python3
"""
Configuración del Sistema Mozo Virtual
Centraliza todas las configuraciones del proyecto
"""

import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class Settings:
    """Configuraciones centralizadas del sistema"""
    
    # API Keys
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    NOTION_API_KEY = os.getenv("NOTION_API_KEY")
    LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")
    
    # LangSmith Config
    LANGCHAIN_TRACING_V2 = "true"
    LANGCHAIN_PROJECT = "proyecto-final-agentes"
    LANGCHAIN_ENDPOINT = "https://api.smith.langchain.com"
    
    # Notion Config
    NOTION_DATABASE_ID = "28815eefe92680389583cff88068af9e"
    NOTION_PAGE_ID = "28815eefe92680389583cff88068af9e"
    
    # ChromaDB Config
    CHROMA_PERSIST_DIRECTORY = "./data/chroma_db"
    
    # Logging Config
    LOG_LEVEL = "INFO"
    LOG_FILE = "./data/conversations/conversaciones_robino.log"
    
    # Agent Config
    MAX_ITERATIONS = 10
    TEMPERATURE = 0.7
    
    # Multi-Agent Config
    INVESTIGATION_TIMEOUT = 30
    REPORT_GENERATION_TIMEOUT = 45
    
    @classmethod
    def validate_config(cls):
        """Validar que todas las configuraciones necesarias estén presentes"""
        required_keys = [
            "GEMINI_API_KEY",
            "NOTION_API_KEY", 
            "LANGCHAIN_API_KEY"
        ]
        
        missing_keys = []
        for key in required_keys:
            if not getattr(cls, key):
                missing_keys.append(key)
        
        if missing_keys:
            raise ValueError(f"Faltan las siguientes API keys: {', '.join(missing_keys)}")
        
        return True
    
    @classmethod
    def get_langsmith_url(cls):
        """Obtener URL del proyecto LangSmith"""
        return f"https://smith.langchain.com/projects/{cls.LANGCHAIN_PROJECT}"
    
    @classmethod
    def get_notion_url(cls):
        """Obtener URL de la base de datos Notion"""
        return f"https://notion.so/{cls.NOTION_DATABASE_ID}"

# Instancia global de configuración
settings = Settings()
