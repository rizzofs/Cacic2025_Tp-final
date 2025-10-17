# 🤖 Sistema Mozo Virtual - Proyecto Final CACIC 2025

Sistema multi-agente avanzado para asistencia en restaurantes utilizando IA generativa, con integración completa de observabilidad y persistencia de datos.

## 📋 Índice

- [Características](#-características)
- [Arquitectura](#-arquitectura)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Instalación](#-instalación)
- [Configuración](#-configuración)
- [Uso](#-uso)
- [Testing](#-testing)
- [Documentación](#-documentación)
- [URLs del Proyecto](#-urls-del-proyecto)

## 🚀 Características

### ✅ Sistema Multi-Agente
- **Agente Principal (Robino)**: Maneja conversaciones básicas y gestión de pedidos
- **Agente Investigador**: Búsqueda especializada en base de conocimiento
- **Agente Generador**: Creación de informes estructurados y recomendaciones

### ✅ Base de Conocimiento RAG
- **ChromaDB**: Base de datos vectorial para búsqueda semántica
- **Google Gemini**: Modelo de lenguaje para generación de respuestas
- **Búsqueda Avanzada**: Recuperación contextual de información del menú

### ✅ Observabilidad Completa
- **LangSmith**: Tracing y monitoreo de todas las operaciones
- **Métricas de Rendimiento**: Análisis de tiempos y eficiencia
- **Reportes Estructurados**: Generación automática de documentación

### ✅ Integración Externa
- **Notion API**: Persistencia de conversaciones e informes
- **Estructura de Datos**: Almacenamiento organizado y consultable

## 🏗️ Arquitectura

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Agente        │    │   Agente        │    │   Agente        │
│   Robino        │◄──►│  Investigador   │◄──►│   Generador     │
│   (Principal)   │    │  (Búsqueda)     │    │  (Informes)     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   ChromaDB      │    │   LangSmith     │    │     Notion      │
│   (RAG)         │    │ (Observabilidad)│    │  (Persistencia) │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 📁 Estructura del Proyecto

```
ProyectoFinal/
├── 📁 src/                          # Código fuente principal
│   ├── 📁 agents/                   # Agentes del sistema
│   │   ├── mozo_virtual_agent.py    # Agente principal
│   │   └── multi_agent_system.py    # Sistema multi-agente
│   ├── 📁 observability/            # Sistema de observabilidad
│   │   └── langsmith_observer.py    # Observer LangSmith
│   ├── 📁 integrations/             # Integraciones externas
│   │   ├── dump_notion_page.py      # Herramienta Notion
│   │   └── whoami_notion.py         # Verificación Notion
│   └── 📁 tools/                    # Herramientas auxiliares
├── 📁 tests/                        # Suite de pruebas
│   ├── 📁 unit/                     # Pruebas unitarias
│   │   ├── test_multi_agent.py      # Test sistema multi-agente
│   │   └── test_langsmith_observability.py
│   └── 📁 integration/              # Pruebas de integración
│       ├── check_notion_data.py     # Test integración Notion
│       └── test_gemini_rest.py      # Test API Gemini
├── 📁 docs/                         # Documentación
│   ├── 📁 architecture/             # Documentación técnica
│   │   ├── README.md               # Documentación principal
│   │   └── PROYECTO_MOZO_VIRTUAL.md
│   └── 📁 api/                      # Documentación API
├── 📁 data/                         # Datos del sistema
│   ├── 📁 menu/                     # Información del menú
│   └── 📁 conversations/            # Historial de conversaciones
├── 📁 config/                       # Configuraciones
│   └── settings.py                  # Configuración centralizada
├── 📁 scripts/                      # Scripts auxiliares
│   ├── 📁 setup/                    # Scripts de configuración
│   │   ├── fix_emojis.py           # Utilidad emojis
│   │   └── install_dependencies.txt
│   └── 📁 deployment/               # Scripts de despliegue
├── 📄 main.py                       # Punto de entrada principal
├── 📄 requirements.txt              # Dependencias Python
└── 📄 .gitignore                    # Archivos ignorados por Git
```

## 🛠️ Instalación

### Prerrequisitos
- Python 3.12+
- pip (gestor de paquetes Python)
- Cuentas en:
  - Google AI Studio (Gemini API)
  - Notion (API Key)
  - LangSmith (API Key)

### Pasos de Instalación

1. **Clonar el repositorio**
```bash
git clone https://github.com/rizzofs/Cacic2025_Tp-final.git
cd Cacic2025_Tp-final
```

2. **Crear entorno virtual**
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno**
```bash
# Crear archivo .env en la raíz del proyecto
GEMINI_API_KEY=tu_api_key_aqui
NOTION_API_KEY=tu_notion_key_aqui
LANGCHAIN_API_KEY=tu_langsmith_key_aqui
```

## ⚙️ Configuración

### Variables de Entorno Requeridas

| Variable | Descripción | Ejemplo |
|----------|-------------|---------|
| `GEMINI_API_KEY` | API Key de Google Gemini | `AIzaSy...` |
| `NOTION_API_KEY` | API Key de Notion | `secret_...` |
| `LANGCHAIN_API_KEY` | API Key de LangSmith | `ls__...` |

### Configuración de Notion
- Base de datos ID: `28815eefe92680389583cff88068af9e`
- Página ID: `28815eefe92680389583cff88068af9e`

### Configuración de LangSmith
- Proyecto: `proyecto-final-agentes`
- Endpoint: `https://api.smith.langchain.com`

## 🚀 Uso

### Ejecución Principal
```bash
python main.py
```

### Ejecución de Tests
```bash
# Tests unitarios
python -m pytest tests/unit/

# Tests de integración
python -m pytest tests/integration/

# Test específico de LangSmith
python tests/unit/test_langsmith_observability.py
```

### Scripts de Utilidad
```bash
# Arreglar problemas de emojis (Windows)
python scripts/setup/fix_emojis.py

# Verificar configuración Notion
python src/integrations/whoami_notion.py
```

## 🧪 Testing

### Cobertura de Tests

| Módulo | Tipo | Archivo | Estado |
|--------|------|---------|--------|
| Multi-Agente | Unitario | `test_multi_agent.py` | ✅ |
| LangSmith | Unitario | `test_langsmith_observability.py` | ✅ |
| Notion | Integración | `check_notion_data.py` | ✅ |
| Gemini API | Integración | `test_gemini_rest.py` | ✅ |

### Ejecutar Todos los Tests
```bash
python -m pytest tests/ -v
```

## 📚 Documentación

### Documentación Técnica
- [Arquitectura del Sistema](docs/architecture/)
- [Documentación de API](docs/api/)
- [Guías de Configuración](docs/setup/)

### Recursos Adicionales
- [Proyecto Final - Especificaciones](docs/architecture/Proyecto%20Final%20-%20IA%20Generativa%20y%20Agentes%20de%20IA.pdf)
- [Guía de Integración Notion](docs/architecture/notion_integration_info.md)
- [Guía de Uso Gemini](docs/architecture/gemini_curl_guide.md)

## 🔗 URLs del Proyecto

### Repositorio y Documentación
- **GitHub**: [https://github.com/rizzofs/Cacic2025_Tp-final.git](https://github.com/rizzofs/Cacic2025_Tp-final.git)

### Observabilidad y Monitoreo
- **LangSmith**: [https://smith.langchain.com/projects/proyecto-final-agentes](https://smith.langchain.com/projects/proyecto-final-agentes)

### Persistencia de Datos
- **Notion**: [https://notion.so/28815eefe92680389583cff88068af9e](https://notion.so/28815eefe92680389583cff88068af9e)

## 🎯 Cumplimiento de Requisitos

### ✅ Requisitos Técnicos
- [x] **Multi-Agente con Colaboración**: 3 agentes especializados
- [x] **Base de Conocimiento RAG**: ChromaDB + Gemini
- [x] **Persistencia Externa**: Notion API
- [x] **Observabilidad**: LangSmith completo

### ✅ Entregables
- [x] **Repositorio Git Público**: GitHub con estructura profesional
- [x] **URL LangSmith**: Project Run con tracing completo
- [x] **URL Notion**: Base de datos con informes estructurados
- [x] **Documentación**: Arquitectura y guías completas

## 👨‍💻 Autor

**Rizzo** - Proyecto Final Integrador CACIC 2025

## 📄 Licencia

Este proyecto es parte del Proyecto Final Integrador del Curso de Inteligencia Artificial Generativa y Agentes de IA - CACIC 2025.

---

**🎉 ¡Sistema completado exitosamente con todas las funcionalidades requeridas!**
