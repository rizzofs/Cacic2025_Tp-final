#!/usr/bin/env python3
"""
Script para verificar y encontrar los datos del Mozo Virtual en Notion
"""

import os
from datetime import datetime
from notion_client import Client
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def search_mozo_data():
    """Buscar específicamente los datos del Mozo Virtual en Notion"""
    print("BUSCANDO DATOS DEL MOZO VIRTUAL EN NOTION")
    print("=" * 50)
    
    try:
        # Conectar a Notion
        notion_token = os.getenv('NOTION_API_KEY')
        if not notion_token:
            print("ERROR: NOTION_API_KEY no encontrada")
            return False
            
        notion = Client(auth=notion_token)
        print("Conectado a Notion")
        
        # Buscar todas las páginas
        print("\n1. Buscando todas las páginas...")
        pages = notion.search(query="", filter={"property": "object", "value": "page"})
        print(f"Se encontraron {len(pages['results'])} páginas")
        
        # Buscar contenido del Mozo Virtual en cada página
        mozo_pages = []
        for i, page in enumerate(pages['results']):
            print(f"\nRevisando página {i+1}...")
            page_id = page['id']
            
            try:
                # Obtener bloques de la página
                blocks = notion.blocks.children.list(block_id=page_id)
                
                # Buscar contenido del Mozo Virtual
                for block in blocks['results']:
                    if block.get('type') == 'heading_1':
                        heading = block.get('heading_1', {}).get('rich_text', [])
                        if heading and 'MOZO VIRTUAL' in heading[0].get('text', {}).get('content', ''):
                            mozo_pages.append({
                                'page_id': page_id,
                                'title': heading[0].get('text', {}).get('content', ''),
                                'blocks_count': len(blocks['results'])
                            })
                            print(f"  ENCONTRADO: {heading[0].get('text', {}).get('content', '')}")
                            break
                    elif block.get('type') == 'paragraph':
                        paragraph = block.get('paragraph', {}).get('rich_text', [])
                        if paragraph and any('MOZO VIRTUAL' in text.get('text', {}).get('content', '') for text in paragraph):
                            mozo_pages.append({
                                'page_id': page_id,
                                'title': 'MOZO VIRTUAL (en párrafo)',
                                'blocks_count': len(blocks['results'])
                            })
                            print(f"  ENCONTRADO: Contenido del Mozo Virtual en párrafo")
                            break
                            
            except Exception as e:
                print(f"  Error revisando página {i+1}: {e}")
                continue
        
        if mozo_pages:
            print(f"\nENCONTRADAS {len(mozo_pages)} PÁGINAS CON DATOS DEL MOZO VIRTUAL:")
            for i, page in enumerate(mozo_pages):
                print(f"  {i+1}. ID: {page['page_id']}")
                print(f"     Título: {page['title']}")
                print(f"     Bloques: {page['blocks_count']}")
                print(f"     URL: https://notion.so/{page['page_id'].replace('-', '')}")
        else:
            print("\nNO SE ENCONTRARON DATOS DEL MOZO VIRTUAL")
            print("Esto puede significar que:")
            print("1. Los datos se guardaron en una página diferente")
            print("2. Hubo un error al guardar")
            print("3. Los datos se guardaron pero no se pueden acceder")
        
        return len(mozo_pages) > 0
        
    except Exception as e:
        print(f"ERROR: {e}")
        return False

def show_recent_activity():
    """Mostrar actividad reciente en Notion"""
    print("\n" + "=" * 50)
    print("ACTIVIDAD RECIENTE EN NOTION")
    print("=" * 50)
    
    try:
        notion_token = os.getenv('NOTION_API_KEY')
        notion = Client(auth=notion_token)
        
        # Buscar páginas recientes
        pages = notion.search(
            query="", 
            filter={"property": "object", "value": "page"},
            sort={"direction": "descending", "timestamp": "last_edited_time"}
        )
        
        print(f"Páginas recientes (últimas 5):")
        for i, page in enumerate(pages['results'][:5]):
            page_id = page['id']
            last_edited = page.get('last_edited_time', 'Desconocido')
            
            # Intentar obtener el título
            title = "Sin título"
            try:
                if 'properties' in page and 'title' in page['properties']:
                    title_prop = page['properties']['title']
                    if title_prop and 'title' in title_prop and title_prop['title']:
                        title = title_prop['title'][0]['text']['content']
            except:
                pass
            
            print(f"  {i+1}. {title}")
            print(f"     ID: {page_id}")
            print(f"     Última edición: {last_edited}")
            print(f"     URL: https://notion.so/{page_id.replace('-', '')}")
            print()
        
    except Exception as e:
        print(f"ERROR mostrando actividad: {e}")

def create_new_test_data():
    """Crear nuevos datos de prueba en una página específica"""
    print("\n" + "=" * 50)
    print("CREANDO NUEVOS DATOS DE PRUEBA")
    print("=" * 50)
    
    try:
        notion_token = os.getenv('NOTION_API_KEY')
        notion = Client(auth=notion_token)
        
        # Buscar una página para escribir
        pages = notion.search(query="", filter={"property": "object", "value": "page"})
        if not pages['results']:
            print("No se encontraron páginas")
            return False
        
        target_page = pages['results'][0]
        page_id = target_page['id']
        
        print(f"Escribiendo en página: {page_id}")
        
        # Crear contenido simple y claro
        blocks = [
            {
                "object": "block",
                "type": "heading_1",
                "heading_1": {
                    "rich_text": [{"type": "text", "text": {"content": "MOZO VIRTUAL - TEST DE INTEGRACION"}}]
                }
            },
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [{"type": "text", "text": {"content": f"Test realizado el: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"}}]
                }
            },
            {
                "object": "block",
                "type": "heading_2",
                "heading_2": {
                    "rich_text": [{"type": "text", "text": {"content": "ESTADO DEL SISTEMA"}}]
                }
            },
            {
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [{"type": "text", "text": {"content": "Conexion con Notion: EXITOSA"}}]
                }
            },
            {
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [{"type": "text", "text": {"content": "Escritura de datos: EXITOSA"}}]
                }
            },
            {
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [{"type": "text", "text": {"content": "Integracion del Mozo Virtual: FUNCIONANDO"}}]
                }
            }
        ]
        
        # Subir a Notion
        notion.blocks.children.append(
            block_id=page_id,
            children=blocks
        )
        
        print("NUEVOS DATOS CREADOS EXITOSAMENTE!")
        print(f"Página ID: {page_id}")
        print(f"URL: https://notion.so/{page_id.replace('-', '')}")
        
        return True
        
    except Exception as e:
        print(f"ERROR creando datos: {e}")
        return False

if __name__ == "__main__":
    print("VERIFICADOR DE DATOS DEL MOZO VIRTUAL EN NOTION")
    print("=" * 60)
    
    # Buscar datos existentes
    found = search_mozo_data()
    
    # Mostrar actividad reciente
    show_recent_activity()
    
    if not found:
        print("\nNo se encontraron datos del Mozo Virtual.")
        choice = input("¿Deseas crear nuevos datos de prueba? (y/n): ").lower()
        if choice == 'y':
            create_new_test_data()
    
    print("\n" + "=" * 60)
    print("VERIFICACION COMPLETADA")
    print("=" * 60)
