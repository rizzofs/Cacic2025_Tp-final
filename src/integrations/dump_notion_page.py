from notion_client import Client
from dotenv import load_dotenv
import os

load_dotenv()
notion_token = os.getenv('NOTION_API_KEY')
if not notion_token:
    print('ERROR: NOTION_API_KEY no encontrada en el entorno')
    raise SystemExit(1)

client = Client(auth=notion_token)
page_id = '28815eef-e926-8038-9583-cff88068af9e'

print(f'Consultando página: {page_id}')

try:
    page = client.pages.retrieve(page_id=page_id)
    title = None
    try:
        props = page.get('properties', {})
        # intentar extraer título si existe
        if 'title' in props and props['title'] and props['title']['title']:
            title = props['title']['title'][0]['text']['content']
    except Exception:
        title = None
    print('Página metadata encontrada. Título:', title)
except Exception as e:
    print('No se pudo recuperar metadata de la página:', e)

try:
    blocks = client.blocks.children.list(block_id=page_id)
    results = blocks.get('results', [])
    print(f'Bloques encontrados: {len(results)}')
    for i, b in enumerate(results):
        t = b.get('type')
        # intentar extraer texto según tipo
        text = ''
        try:
            if t in ('paragraph','heading_1','heading_2','heading_3','bulleted_list_item'):
                rich = b.get(t, {}).get('rich_text', [])
                text = ''.join([r.get('text', {}).get('content','') for r in rich])
            elif t == 'code':
                text = b.get('code', {}).get('rich_text', [{}])[0].get('text', {}).get('content','')
            else:
                text = str(b.get(t, {}))[:200]
        except Exception:
            text = '<error al parsear bloque>'
        print(f'{i+1:02d}. [{t}] {text}')
except Exception as e:
    print('Error listando bloques:', e)
