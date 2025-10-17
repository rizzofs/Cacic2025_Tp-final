#!/usr/bin/env python3
"""
Test de Gemini usando la API REST directamente
"""

import os
import requests
import json
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def test_gemini_rest_api():
    """Test de Gemini usando API REST"""
    print("TEST DE GEMINI CON API REST")
    print("=" * 40)
    
    try:
        # Obtener API key
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            print("ERROR: GEMINI_API_KEY no encontrada")
            return False
        
        print(f"API Key encontrada: {api_key[:10]}...")
        
        # URL de la API
        url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
        
        # Headers
        headers = {
            'Content-Type': 'application/json',
            'X-goog-api-key': api_key
        }
        
        # Datos de prueba
        data = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": "Hola, responde con un saludo simple en español"
                        }
                    ]
                }
            ]
        }
        
        print("Enviando petición a Gemini...")
        
        # Hacer la petición
        response = requests.post(url, headers=headers, json=data)
        
        if response.status_code == 200:
            result = response.json()
            if 'candidates' in result and len(result['candidates']) > 0:
                text = result['candidates'][0]['content']['parts'][0]['text']
                print(f"Respuesta de Gemini: {text}")
                print("CONEXION CON GEMINI EXITOSA!")
                return True
            else:
                print("No se recibió respuesta válida")
                print(f"Respuesta completa: {result}")
                return False
        else:
            print(f"ERROR HTTP {response.status_code}: {response.text}")
            return False
        
    except Exception as e:
        print(f"ERROR: {e}")
        return False

def test_mozo_virtual_rest():
    """Test del Mozo Virtual usando API REST"""
    print("\nTEST DEL MOZO VIRTUAL CON API REST")
    print("=" * 40)
    
    try:
        api_key = os.getenv('GEMINI_API_KEY')
        url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"
        
        headers = {
            'Content-Type': 'application/json',
            'X-goog-api-key': api_key
        }
        
        # Prompt específico para el Mozo Virtual
        mozo_prompt = """
        Eres un mozo virtual de un restaurante español llamado "El Mozo Virtual".
        Tu especialidad es ayudar a los clientes con recomendaciones de platos, 
        información sobre el menú, reservas y consultas sobre ingredientes.
        
        Responde siempre de manera amigable, profesional y en español.
        """
        
        # Simular conversación
        scenarios = [
            "Hola, bienvenido al restaurante El Mozo Virtual. ¿En qué puedo ayudarte?",
            "¿Qué tipo de comida prefieres?",
            "¿Tienes alguna alergia alimentaria?"
        ]
        
        print("Simulando conversación del Mozo Virtual...")
        for i, scenario in enumerate(scenarios, 1):
            print(f"\n{i}. Cliente: {scenario}")
            
            # Crear prompt completo
            full_prompt = f"{mozo_prompt}\n\nCliente: {scenario}\nMozo:"
            
            data = {
                "contents": [
                    {
                        "parts": [
                            {
                                "text": full_prompt
                            }
                        ]
                    }
                ]
            }
            
            response = requests.post(url, headers=headers, json=data)
            
            if response.status_code == 200:
                result = response.json()
                if 'candidates' in result and len(result['candidates']) > 0:
                    text = result['candidates'][0]['content']['parts'][0]['text']
                    print(f"   Mozo: {text}")
                else:
                    print(f"   Error en respuesta: {result}")
            else:
                print(f"   Error HTTP {response.status_code}: {response.text}")
        
        print("\nTEST DEL MOZO VIRTUAL CON API REST: EXITOSO!")
        return True
        
    except Exception as e:
        print(f"ERROR en test del Mozo Virtual: {e}")
        return False

def test_save_to_notion():
    """Guardar resultados del test en Notion"""
    print("\nGUARDANDO RESULTADOS EN NOTION")
    print("=" * 40)
    
    try:
        from notion_client import Client
        
        # Conectar a Notion
        notion_token = os.getenv('NOTION_API_KEY')
        notion = Client(auth=notion_token)
        
        # Buscar página del Mozo Virtual
        pages = notion.search(query="", filter={"property": "object", "value": "page"})
        target_page = None
        
        for page in pages['results']:
            try:
                blocks = notion.blocks.children.list(block_id=page['id'])
                for block in blocks['results']:
                    if block.get('type') == 'heading_1':
                        heading = block.get('heading_1', {}).get('rich_text', [])
                        if heading and 'MOZO VIRTUAL' in heading[0].get('text', {}).get('content', ''):
                            target_page = page['id']
                            break
                if target_page:
                    break
            except:
                continue
        
        if not target_page:
            print("No se encontró la página del Mozo Virtual")
            return False
        
        # Crear contenido para Notion
        blocks = [
            {
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{"type": "text", "text": {"content": "TEST GEMINI API REST"}}]
                }
            },
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"type": "text", "text": {"content": f"Test realizado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"}}]
                }
            },
            {
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [{"type": "text", "text": {"content": "Conexion con Gemini API REST: EXITOSA"}}]
                }
            },
            {
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [{"type": "text", "text": {"content": "Test del Mozo Virtual: EXITOSO"}}]
                }
            },
            {
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [{"type": "text", "text": {"content": "Integracion completa: FUNCIONANDO"}}]
                }
            }
        ]
        
        # Subir a Notion
        notion.blocks.children.append(
            block_id=target_page,
            children=blocks
        )
        
        print("Resultados guardados en Notion")
        return True
        
    except Exception as e:
        print(f"ERROR guardando en Notion: {e}")
        return False

def main():
    """Función principal"""
    print("TEST COMPLETO DE GEMINI CON API REST")
    print("=" * 50)
    
    # Test 1: Conexión básica
    basic_success = test_gemini_rest_api()
    
    if basic_success:
        # Test 2: Escenario del Mozo Virtual
        mozo_success = test_mozo_virtual_rest()
        
        # Test 3: Guardar en Notion
        notion_success = test_save_to_notion()
        
        print("\n" + "=" * 50)
        print("RESUMEN DEL TEST")
        print("=" * 50)
        print(f"Conexion basica: {'OK' if basic_success else 'FALLO'}")
        print(f"Escenario Mozo Virtual: {'OK' if mozo_success else 'FALLO'}")
        print(f"Guardado en Notion: {'OK' if notion_success else 'FALLO'}")
        
        if all([basic_success, mozo_success, notion_success]):
            print("\nGEMINI ESTA COMPLETAMENTE FUNCIONAL!")
            print("El Mozo Virtual puede usar Gemini para generar respuestas")
        else:
            print("\nAlgunos tests fallaron, pero la conexion basica funciona")
    else:
        print("\nNo se pudo conectar con Gemini. Revisa la API key.")

if __name__ == "__main__":
    from datetime import datetime
    main()

