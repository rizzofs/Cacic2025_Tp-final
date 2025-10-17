# 🤖 Guía de Uso de Gemini con cURL

## 📋 Comando cURL para Gemini

### **Comando Básico:**
```bash
curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent" \
  -H 'Content-Type: application/json' \
  -H 'X-goog-api-key: TU_API_KEY_AQUI' \
  -X POST \
  -d '{
    "contents": [
      {
        "parts": [
          {
            "text": "Tu mensaje aquí"
          }
        ]
      }
    ]
  }'
```

### **Ejemplo con tu API Key:**
```bash
curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent" \
  -H 'Content-Type: application/json' \
  -H 'X-goog-api-key: AIzaSyC9VMeOwWFWt58RAapYkDux9aoQ-0GnRyk' \
  -X POST \
  -d '{
    "contents": [
      {
        "parts": [
          {
            "text": "Hola, responde con un saludo simple en español"
          }
        ]
      }
    ]
  }'
```

## 🍽️ Ejemplo para el Mozo Virtual

### **Prompt del Mozo Virtual:**
```bash
curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent" \
  -H 'Content-Type: application/json' \
  -H 'X-goog-api-key: AIzaSyC9VMeOwWFWt58RAapYkDux9aoQ-0GnRyk' \
  -X POST \
  -d '{
    "contents": [
      {
        "parts": [
          {
            "text": "Eres un mozo virtual de un restaurante español llamado El Mozo Virtual. Tu especialidad es ayudar a los clientes con recomendaciones de platos, información sobre el menú, reservas y consultas sobre ingredientes. Responde siempre de manera amigable, profesional y en español. Cliente: Hola, ¿qué me recomiendas para cenar? Mozo:"
          }
        ]
      }
    ]
  }'
```

## 🔧 Parámetros Adicionales

### **Con Configuración de Temperatura:**
```json
{
  "contents": [
    {
      "parts": [
        {
          "text": "Tu mensaje aquí"
        }
      ]
    }
  ],
  "generationConfig": {
    "temperature": 0.7,
    "maxOutputTokens": 1000
  }
}
```

### **Con Configuración de Seguridad:**
```json
{
  "contents": [
    {
      "parts": [
        {
          "text": "Tu mensaje aquí"
        }
      ]
    }
  ],
  "safetySettings": [
    {
      "category": "HARM_CATEGORY_HARASSMENT",
      "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    }
  ]
}
```

## 📊 Respuesta Esperada

### **Formato de Respuesta:**
```json
{
  "candidates": [
    {
      "content": {
        "parts": [
          {
            "text": "¡Hola! Bienvenido a El Mozo Virtual. ¿En qué puedo ayudarle hoy?"
          }
        ],
        "role": "model"
      },
      "finishReason": "STOP",
      "index": 0,
      "safetyRatings": [
        {
          "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
          "probability": "NEGLIGIBLE"
        }
      ]
    }
  ],
  "usageMetadata": {
    "promptTokenCount": 10,
    "candidatesTokenCount": 15,
    "totalTokenCount": 25
  }
}
```

## 🛠️ Uso en Python

### **Implementación en Python:**
```python
import requests
import json

def call_gemini_api(message, api_key):
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
    
    headers = {
        'Content-Type': 'application/json',
        'X-goog-api-key': api_key
    }
    
    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": message
                    }
                ]
            }
        ]
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        result = response.json()
        return result['candidates'][0]['content']['parts'][0]['text']
    else:
        return f"Error: {response.status_code} - {response.text}"

# Uso
api_key = "AIzaSyC9VMeOwWFWt58RAapYkDux9aoQ-0GnRyk"
response = call_gemini_api("Hola, ¿cómo estás?", api_key)
print(response)
```

## 🔍 Troubleshooting

### **Errores Comunes:**

1. **401 Unauthorized:**
   - Verificar que la API key sea correcta
   - Verificar que la API key tenga permisos para Gemini

2. **404 Not Found:**
   - Verificar que el modelo sea correcto
   - Usar `gemini-2.0-flash` en lugar de `gemini-pro`

3. **400 Bad Request:**
   - Verificar el formato JSON
   - Verificar que el contenido no esté vacío

### **Verificar API Key:**
```bash
curl "https://generativelanguage.googleapis.com/v1beta/models" \
  -H 'X-goog-api-key: TU_API_KEY_AQUI'
```

## 📝 Notas Importantes

- **Modelo recomendado:** `gemini-2.0-flash`
- **Límite de tokens:** 1000 por defecto
- **Temperatura:** 0.7 para respuestas creativas
- **Formato:** Siempre JSON
- **Headers requeridos:** Content-Type y X-goog-api-key

## 🎯 Para el Mozo Virtual

### **Prompts Efectivos:**
- Ser específico sobre el rol del Mozo Virtual
- Incluir contexto del restaurante
- Pedir respuestas en español
- Mantener tono profesional y amigable

### **Ejemplo de Prompt Completo:**
```
Eres un mozo virtual de un restaurante español llamado "El Mozo Virtual". 
Tu especialidad es ayudar a los clientes con:
- Recomendaciones de platos
- Información sobre el menú  
- Reservas
- Consultas sobre ingredientes y alérgenos

Responde siempre de manera amigable, profesional y en español.
Si no sabes algo, admítelo y ofrece ayuda alternativa.

Cliente: [MENSAJE DEL CLIENTE]
Mozo:
```

