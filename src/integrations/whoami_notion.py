from notion_client import Client
from dotenv import load_dotenv
import os

load_dotenv()
notion_token = os.getenv('NOTION_API_KEY')
if not notion_token:
    print('ERROR: NOTION_API_KEY no encontrada en el entorno')
    raise SystemExit(1)

client = Client(auth=notion_token)

try:
    me = client.users.me()
    print('Usuario Notion (desde token):')
    print('  id:', me.get('id'))
    print('  name:', me.get('name'))
    print('  type:', me.get('type'))
    # correo puede no estar disponible en objetos de usuario, intentar properties
    if 'person' in me:
        print('  person:', me.get('person'))
except Exception as e:
    print('Error consultando usuario:', e)
