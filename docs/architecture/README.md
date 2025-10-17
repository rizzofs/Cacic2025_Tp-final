# 🤖 Sistema Multi-Agente Mozo Virtual - La Taberna del Río

## 📋 Descripción del Proyecto

Este proyecto implementa un **sistema multi-agente inteligente** para un restaurante virtual llamado "La Taberna del Río". El sistema utiliza **LangGraph** para coordinar dos agentes especializados que trabajan en colaboración para brindar un servicio completo al cliente.

## 🎯 Características Principales

### ✅ **Sistema Multi-Agente Implementado**
- **Agente Investigador**: Busca información específica en la base de conocimiento
- **Agente Generador**: Crea informes estructurados y recomendaciones personalizadas
- **Colaboración**: Los agentes trabajan en secuencia para resolver consultas complejas

### ✅ **Integraciones Completadas**
- **Google Gemini**: Modelo `gemini-2.0-flash` para generación de respuestas
- **Notion**: Persistencia de conversaciones e informes estructurados
- **LangChain**: Framework para construcción de agentes inteligentes
- **ChromaDB**: Base de conocimiento vectorial para RAG

### ✅ **Funcionalidades del Restaurante**
- Menú completo con precios y descripciones
- Sistema de pedidos con cálculo automático de totales
- Procesamiento de pagos
- Especialidades del día
- Información del restaurante (horarios, ubicación, servicios)

## 🏗️ Arquitectura del Sistema

```
Cliente → Agente Principal (Robino) → [Decisión] → Agente Investigador → Agente Generador → Notion
```

### **Flujo de Trabajo:**
1. **Consulta Simple**: Robino maneja directamente (menú, precios, pedidos)
2. **Consulta Compleja**: Sistema multi-agente se activa automáticamente
3. **Investigación**: Agente Investigador busca información específica
4. **Generación**: Agente Generador crea informes estructurados
5. **Persistencia**: Informes se guardan en Notion

## 📁 Estructura del Proyecto

```
ProyectoFinal/
├── mozo_virtual_agent.py          # Agente principal con sistema híbrido
├── multi_agent_system.py          # Sistema multi-agente especializado
├── test_multi_agent.py            # Tests del sistema multi-agente
├── test_final_demo.py             # Demo completo del proyecto
├── fix_emojis.py                  # Utilidad para compatibilidad Windows
├── requirements.txt               # Dependencias del proyecto
├── .gitignore                     # Archivos excluidos del repositorio
├── .env                          # Variables de entorno (NO incluido)
└── tests/                        # Tests adicionales
    ├── test_gemini_rest.py
    ├── test_notion_data_upload.py
    └── check_notion_data.py
```

## 🚀 Instalación y Configuración

### **1. Clonar el Repositorio**
```bash
git clone https://github.com/rizzofs/Cacic2025_Tp-final.git
cd Cacic2025_Tp-final
```

### **2. Crear Entorno Virtual**
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
```

### **3. Instalar Dependencias**
```bash
pip install -r requirements.txt
```

### **4. Configurar Variables de Entorno**
Crear archivo `.env` en la raíz del proyecto:
```env
# API Keys (OBLIGATORIAS)
GEMINI_API_KEY=tu_gemini_api_key_aqui
NOTION_API_KEY=tu_notion_api_key_aqui

# Configuración opcional
LANGCHAIN_API_KEY=tu_langsmith_api_key_aqui
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=proyecto-final-agentes
```

### **5. Ejecutar el Sistema**
```bash
# Ejecutar el Mozo Virtual completo
python mozo_virtual_agent.py

# Ejecutar tests del sistema multi-agente
python test_multi_agent.py

# Ejecutar demo completo
python test_final_demo.py
```

## 🧪 Testing

### **Tests Disponibles:**
- `test_multi_agent.py`: Tests del sistema multi-agente
- `test_final_demo.py`: Demo completo con todas las funcionalidades
- `tests/test_gemini_rest.py`: Tests de integración con Gemini
- `tests/test_notion_data_upload.py`: Tests de integración con Notion

### **Ejecutar Tests:**
```bash
# Test del sistema multi-agente
python test_multi_agent.py

# Demo completo
python test_final_demo.py

# Tests de integración
python tests/test_gemini_rest.py
python tests/test_notion_data_upload.py
```

## 🎯 Ejemplos de Uso

### **Consulta Simple:**
```
Cliente: "¿Cuánto cuesta la paella?"
Robino: [Maneja directamente con el agente simple]
```

### **Consulta Compleja (Multi-Agente):**
```
Cliente: "¿Qué me recomiendas para una cena romántica?"
[BUSCAR] Detectada consulta compleja - Activando sistema multi-agente...
[INVESTIGADOR] Analizando preferencias del cliente...
[GENERADOR] Creando informe estructurado...
[GUARDAR] Informe guardado en Notion
```

## 📊 Funcionalidades del Sistema Multi-Agente

### **Agente Investigador:**
- Busca información específica en la base de conocimiento
- Analiza preferencias del cliente (ocasión, presupuesto, restricciones)
- Prepara datos estructurados para el generador

### **Agente Generador:**
- Crea informes estructurados con recomendaciones
- Genera justificaciones para las recomendaciones
- Guarda informes en Notion con formato profesional

### **Colaboración:**
- Flujo secuencial: Investigador → Generador
- Compartición de datos entre agentes
- Persistencia automática en Notion

## 🔗 Integraciones

### **Notion Integration:**
- **URL**: [https://notion.so/28815eefe92680389583cff88068af9e](https://notion.so/28815eefe92680389583cff88068af9e)
- **Funcionalidad**: Guarda conversaciones e informes estructurados
- **Formato**: Bloques organizados con timestamps y metadatos

### **Google Gemini:**
- **Modelo**: `gemini-2.0-flash`
- **Funcionalidad**: Generación de respuestas y análisis de contexto
- **Embeddings**: `models/gemini-embedding-001`

## 🎓 Cumplimiento de Requisitos del Proyecto

### ✅ **Requisitos Técnicos Cumplidos:**
1. **Multi-Agente**: Sistema con 2 agentes conectados y en colaboración
2. **Base de Conocimiento RAG**: ChromaDB con información del restaurante
3. **Persistencia Externa**: Integración completa con Notion
4. **LangGraph**: Grafos de conversación con transiciones condicionales
5. **Herramientas Especializadas**: Tools específicas para cada agente

### ✅ **Entregables Completados:**
1. **Repositorio Git Público**: ✅ [https://github.com/rizzofs/Cacic2025_Tp-final.git](https://github.com/rizzofs/Cacic2025_Tp-final.git)
2. **Código Funcional**: ✅ Sistema multi-agente operativo
3. **Integración Notion**: ✅ Persistencia de informes estructurados
4. **Tests**: ✅ Suite completa de pruebas
5. **Documentación**: ✅ README completo con instrucciones

## 🛠️ Tecnologías Utilizadas

- **Python 3.12**
- **LangChain & LangGraph**: Framework de agentes
- **Google Gemini**: Modelo de IA generativa
- **ChromaDB**: Base de datos vectorial
- **Notion API**: Persistencia de datos
- **GitHub**: Control de versiones

## 👨‍💻 Autor

**Proyecto Final Integrador - CACIC 2025**
- **Tema**: Sistema Multi-Agente para Restaurante Virtual
- **Implementación**: Agente Investigador + Agente Generador
- **Colaboración**: LangGraph con transiciones condicionales

## 📝 Notas Técnicas

- **Compatibilidad**: Optimizado para Windows (sin emojis en consola)
- **Fallbacks**: Sistema de respaldo para todas las integraciones
- **Logging**: Registro local de todas las conversaciones
- **Error Handling**: Manejo robusto de errores con fallbacks

---

**¡El Sistema Multi-Agente Mozo Virtual está listo para atender clientes en La Taberna del Río!** 🍽️

