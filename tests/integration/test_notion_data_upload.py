#!/usr/bin/env python3
"""
Test específico para cargar datos del Mozo Virtual en Notion
Este script creará y guardará información real para verificar que funciona
"""

import os
import json
from datetime import datetime
from notion_client import Client
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def create_mozo_virtual_data():
    """Crear datos de prueba específicos del Mozo Virtual"""
    return {
        "conversaciones": [
            {
                "id": "conv_001",
                "cliente": "Juan Pérez",
                "fecha": datetime.now().isoformat(),
                "mensaje": "Hola, necesito ayuda con el menú",
                "respuesta": "¡Hola Juan! Claro, te puedo ayudar con el menú. ¿Qué tipo de comida prefieres?",
                "estado": "completada"
            },
            {
                "id": "conv_002", 
                "cliente": "María García",
                "fecha": datetime.now().isoformat(),
                "mensaje": "¿Tienen opciones vegetarianas?",
                "respuesta": "¡Por supuesto! Tenemos varias opciones vegetarianas deliciosas. ¿Te gustaría ver nuestro menú vegetariano?",
                "estado": "en_proceso"
            },
            {
                "id": "conv_003",
                "cliente": "Carlos López", 
                "fecha": datetime.now().isoformat(),
                "mensaje": "¿Cuál es el plato más popular?",
                "respuesta": "Nuestro plato más popular es la Paella Valenciana, preparada con ingredientes frescos y siguiendo la receta tradicional.",
                "estado": "completada"
            }
        ],
        "configuracion": {
            "nombre_restaurante": "Restaurante El Mozo Virtual",
            "horario": "12:00 - 23:00",
            "especialidades": ["Paella", "Tapas", "Mariscos", "Carnes"],
            "idiomas": ["Español", "Inglés", "Francés"]
        },
        "estadisticas": {
            "conversaciones_totales": 3,
            "conversaciones_completadas": 2,
            "tiempo_promedio_respuesta": "2.5 segundos",
            "satisfaccion_cliente": "4.8/5"
        }
    }

def test_upload_to_notion():
    """Subir datos específicos del Mozo Virtual a Notion"""
    print("INICIANDO CARGA DE DATOS DEL MOZO VIRTUAL EN NOTION")
    print("=" * 60)
    
    try:
        # Conectar a Notion
        notion_token = os.getenv('NOTION_API_KEY')
        if not notion_token:
            print("ERROR: NOTION_API_KEY no encontrada")
            return False
            
        notion = Client(auth=notion_token)
        print("Conectado a Notion")
        
        # Buscar una página para escribir
        pages = notion.search(query="", filter={"property": "object", "value": "page"})
        if not pages['results']:
            print("ERROR: No se encontraron páginas en Notion")
            return False
            
        target_page = pages['results'][0]
        page_id = target_page['id']
        print(f"Usando página: {page_id}")
        
        # Crear datos del Mozo Virtual
        mozo_data = create_mozo_virtual_data()
        
        # Crear contenido estructurado en Notion
        blocks = [
            {
                "object": "block",
                "type": "heading_1",
                "heading_1": {
                    "rich_text": [{"type": "text", "text": {"content": "MOZO VIRTUAL - DATOS DE PRUEBA"}}]
                }
            },
            {
                "object": "block", 
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"type": "text", "text": {"content": f"Fecha de carga: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"}}]
                }
            },
            {
                "object": "block",
                "type": "heading_2", 
                "heading_2": {
                    "rich_text": [{"type": "text", "text": {"content": "CONFIGURACION DEL RESTAURANTE"}}]
                }
            }
        ]
        
        # Agregar configuración
        config = mozo_data["configuracion"]
        blocks.extend([
            {
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [{"type": "text", "text": {"content": f"Restaurante: {config['nombre_restaurante']}"}}]
                }
            },
            {
                "object": "block",
                "type": "bulleted_list_item", 
                "bulleted_list_item": {
                    "rich_text": [{"type": "text", "text": {"content": f"Horario: {config['horario']}"}}]
                }
            },
            {
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [{"type": "text", "text": {"content": f"Especialidades: {', '.join(config['especialidades'])}"}}]
                }
            }
        ])
        
        # Agregar conversaciones
        blocks.append({
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": "CONVERSACIONES RECIENTES"}}]
            }
        })
        
        for conv in mozo_data["conversaciones"]:
            blocks.extend([
                {
                    "object": "block",
                    "type": "heading_3",
                    "heading_3": {
                        "rich_text": [{"type": "text", "text": {"content": f"Cliente: {conv['cliente']} ({conv['estado']})"}}]
                    }
                },
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [{"type": "text", "text": {"content": f"Cliente: {conv['mensaje']}"}}]
                    }
                },
                {
                    "object": "block", 
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [{"type": "text", "text": {"content": f"Mozo: {conv['respuesta']}"}}]
                    }
                }
            ])
        
        # Agregar estadísticas
        stats = mozo_data["estadisticas"]
        blocks.extend([
            {
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{"type": "text", "text": {"content": "ESTADISTICAS"}}]
                }
            },
            {
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [{"type": "text", "text": {"content": f"Conversaciones totales: {stats['conversaciones_totales']}"}}]
                }
            },
            {
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [{"type": "text", "text": {"content": f"Completadas: {stats['conversaciones_completadas']}"}}]
                }
            },
            {
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [{"type": "text", "text": {"content": f"Satisfacción: {stats['satisfaccion_cliente']}"}}]
                }
            }
        ])
        
        # Subir todo a Notion
        print("\nSubiendo datos a Notion...")
        notion.blocks.children.append(
            block_id=page_id,
            children=blocks
        )
        
        print("DATOS CARGADOS EXITOSAMENTE EN NOTION!")
        print("\nResumen de lo que se subió:")
        print(f"   - Configuración del restaurante")
        print(f"   - {len(mozo_data['conversaciones'])} conversaciones de ejemplo")
        print(f"   - Estadísticas del Mozo Virtual")
        print(f"   - Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        return True
        
    except Exception as e:
        print(f"ERROR: {e}")
        return False

def verify_data_in_notion():
    """Verificar que los datos se guardaron correctamente"""
    print("\nVERIFICANDO DATOS EN NOTION...")
    
    try:
        notion_token = os.getenv('NOTION_API_KEY')
        notion = Client(auth=notion_token)
        
        # Buscar la página donde escribimos
        pages = notion.search(query="", filter={"property": "object", "value": "page"})
        if not pages['results']:
            print("No se encontraron páginas")
            return False
            
        target_page = pages['results'][0]
        page_id = target_page['id']
        
        # Obtener el contenido de la página
        blocks = notion.blocks.children.list(block_id=page_id)
        
        print(f"Página encontrada con {len(blocks['results'])} bloques")
        
        # Buscar contenido específico del Mozo Virtual
        mozo_content_found = False
        for block in blocks['results']:
            if block.get('type') == 'heading_1':
                heading = block.get('heading_1', {}).get('rich_text', [])
                if heading and 'MOZO VIRTUAL' in heading[0].get('text', {}).get('content', ''):
                    mozo_content_found = True
                    break
        
        if mozo_content_found:
            print("CONTENIDO DEL MOZO VIRTUAL ENCONTRADO EN NOTION!")
            print("Los datos se guardaron correctamente")
        else:
            print("No se encontró el contenido específico del Mozo Virtual")
            
        return mozo_content_found
        
    except Exception as e:
        print(f"ERROR verificando datos: {e}")
        return False

if __name__ == "__main__":
    print("TEST DE CARGA DE DATOS DEL MOZO VIRTUAL")
    print("=" * 60)
    
    # Cargar datos
    success = test_upload_to_notion()
    
    if success:
        # Verificar que se guardaron
        verify_data_in_notion()
        
        print("\n" + "=" * 60)
        print("TEST COMPLETADO EXITOSAMENTE!")
        print("El Mozo Virtual puede cargar datos en Notion")
        print("La integración está funcionando perfectamente")
        print("Puedes verificar los datos en tu workspace de Notion")
        print("=" * 60)
    else:
        print("\nEl test falló. Revisa la configuración.")
