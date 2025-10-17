# 🧪 Tests del Mozo Virtual

## 📋 Tests Disponibles

### ✅ **Tests Funcionales (Mantener)**

1. **`test_notion_data_upload.py`** - Test completo de Notion
   - Carga datos del Mozo Virtual en Notion
   - Verifica almacenamiento y recuperación
   - **Estado:** ✅ Funcionando

2. **`test_gemini_rest.py`** - Test de Gemini con API REST
   - Conexión directa con Gemini usando API REST
   - Simulación del Mozo Virtual
   - Integración con Notion
   - **Estado:** ✅ Funcionando

3. **`check_notion_data.py`** - Verificador de datos en Notion
   - Busca datos del Mozo Virtual en Notion
   - Muestra actividad reciente
   - **Estado:** ✅ Funcionando

## 🚀 Uso de los Tests

### **Test de Notion:**
```bash
python tests/test_notion_data_upload.py
```

### **Test de Gemini:**
```bash
python tests/test_gemini_rest.py
```

### **Verificar datos en Notion:**
```bash
python tests/check_notion_data.py
```

## 🔧 Configuración Requerida

### Variables de Entorno (.env)
```env
NOTION_API_KEY=tu_notion_api_key_aqui
GEMINI_API_KEY=tu_gemini_api_key_aqui
LANGCHAIN_API_KEY=tu_langsmith_api_key_aqui
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=proyecto-final-agentes
```

## 📊 Resultados de los Tests

### **Notion Integration:**
- ✅ Conexión exitosa
- ✅ Almacenamiento de datos
- ✅ Recuperación de información
- 📄 **URL:** [https://notion.so/28815eefe92680389583cff88068af9e](https://notion.so/28815eefe92680389583cff88068af9e)

### **Gemini Integration:**
- ✅ API REST funcionando
- ✅ Respuestas generadas correctamente
- ✅ Mozo Virtual respondiendo

## 🗑️ Tests Eliminados

Los siguientes tests fueron eliminados por problemas o redundancia:

- `test_gemini_basic.py` - Problemas con librerías
- `test_gemini_minimal.py` - Redundante
- `test_gemini_models.py` - Problemas con API
- `test_gemini_simple.py` - Redundante
- `test_langchain_gemini.py` - Problemas con modelos
- `test_notion_integration.py` - Redundante
- `test_notion_simple.py` - Redundante

## 📝 Notas Técnicas

- **Notion:** Funciona perfectamente con la API oficial
- **Gemini:** Funciona mejor con API REST directa que con librerías de Python
- **LangChain:** Dependencias instaladas, listo para desarrollo
- **Tests:** Organizados y funcionales

