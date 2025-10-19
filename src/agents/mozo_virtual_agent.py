#!/usr/bin/env python3
"""
Agente Mozo Virtual - Robino
Sistema conversacional inteligente para restaurante usando LangChain y Gemini
"""

import os
from typing import Sequence, Annotated, TypedDict, Literal
from datetime import datetime
import json

# Carga de variables de entorno
from dotenv import load_dotenv

# LangSmith para observabilidad
import os
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_PROJECT"] = "proyecto-final-agentes"
os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"

# Componentes de LangChain
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.tools.retriever import create_retriever_tool
from langchain_core.tools import tool
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage

# Componentes específicos de Google
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI

# Componentes de LangGraph
from langchain_chroma import Chroma
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode

# Integración con Notion
from notion_client import Client

# Sistema Multi-Agente
from .simple_multi_agent import SimpleMultiAgentMozoVirtual


class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]


class MozoVirtualAgent:
    """
    Agente conversacional Robino - Mozo Virtual del restaurante
    """
    
    def __init__(self):
        """Inicializar el agente con configuración y herramientas"""
        self.setup_environment()
        self.setup_llm()
        self.setup_vectorstore()
        # Inicializar sistema de pedidos
        self.pedido_actual = []
        self.total_pedido = 0.0
        self.pagado = False
        # Diccionario de precios para cálculo de totales
        self.precios = {
            # Aperitivos
            "tabla de quesos y fiambres": 18000,
            "croquetas de jamón ibérico": 12000,
            "patatas bravas": 8000,
            "pulpo a la gallega": 16000,
            "gazpacho andaluz": 9000,
            # Carnes
            "solomillo de ternera": 35000,
            "cordero al horno": 32000,
            "cochinillo asado": 45000,
            # Pescados y mariscos
            "paella valenciana": 28000,
            "paella de mariscos": 32000,
            "bacalao a la vizcaína": 26000,
            "merluza en salsa verde": 24000,
            # Vegetarianos
            "risotto de setas": 22000,
            "tortilla española": 14000,
            "ensalada de quinoa": 18000,
            # Postres
            "flan de caramelo": 8000,
            "tarta de santiago": 10000,
            "crema catalana": 9000,
            "helado de turrón": 7000,
            # Bebidas
            "rioja reserva": 12000,
            "albariño": 10000,
            "cava brut": 14000,
            "estrella galicia": 6000,
            "mahou": 6000,
            "limonada casera": 5000,
            "agua mineral": 3000,
            "café": 4000,
            # Especialidades del día
            "cocido madrileño": 20000,
            "fabada asturiana": 22000,
            "gazpacho y salmorejo": 15000,
            "pulpo a feira": 25000,
            "cocido completo": 25000
        }
        self.setup_tools()
        self.setup_graph()
        # Inicializar sistema multi-agente
        self.multi_agent_system = None
        self.initialize_multi_agent()
        
    def setup_environment(self):
        """Cargar variables de entorno"""
        load_dotenv()
        if not os.getenv("GEMINI_API_KEY"):
            raise ValueError("La variable de entorno GEMINI_API_KEY no está definida.")
        
        # Configurar Notion si está disponible
        self.notion_token = os.getenv('NOTION_API_KEY')
        if self.notion_token:
            self.notion_client = Client(auth=self.notion_token)
            self.setup_notion_page()
        else:
            self.notion_client = None
            print("Advertencia: NOTION_API_KEY no encontrada. Las conversaciones se guardarán solo localmente.")
        
        print("Variables de entorno cargadas correctamente.")
    
    def setup_notion_page(self):
        """Configurar la página de Notion para las conversaciones de Robino"""
        try:
            page_id = "28815eef-e926-8038-9583-cff88068af9e"
            
            # Verificar si la página existe
            try:
                page = self.notion_client.pages.retrieve(page_id=page_id)
                print("Pagina de Notion configurada correctamente")
            except Exception:
                print("[ADVERTENCIA] No se pudo acceder a la página de Notion especificada")
                
        except Exception as e:
            print(f"[ADVERTENCIA] Error configurando Notion: {e}")
            self.notion_client = None
    
    def setup_llm(self):
        """Configurar el modelo de lenguaje Gemini"""
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            google_api_key=os.getenv("GEMINI_API_KEY"), 
            temperature=0.7
        )
        self.embedding_model = GoogleGenerativeAIEmbeddings(
            model="models/gemini-embedding-001",
            google_api_key=os.getenv("GEMINI_API_KEY")
        )
        print("Modelo Gemini configurado correctamente.")
    
    def create_menu_documents(self) -> list[Document]:
        """Crear documentos con el menú completo del restaurante"""
        
        # Menú completo del restaurante "La Taberna del Río"
        menu_content = """
        RESTAURANTE LA TABERNA DEL RIO - MENU COMPLETO
        
        APERITIVOS:
        - Tabla de Quesos y Fiambres: Selección de quesos artesanales, jamón serrano, chorizo y aceitunas. Precio: $18.000. Ingredientes: quesos variados, jamón serrano, chorizo, aceitunas, pan artesanal.
        
        - Croquetas de Jamón Ibérico: Croquetas caseras con jamón ibérico de bellota. Precio: $12.000. Ingredientes: jamón ibérico, bechamel, pan rallado, aceite de oliva.
        
        - Patatas Bravas: Patatas fritas con salsa brava y alioli. Precio: $8.000. Ingredientes: patatas, tomate, pimentón, ajo, aceite de oliva.
        
        - Pulpo a la Gallega: Pulpo cocido con papas, pimentón y aceite de oliva. Precio: $16.000. Ingredientes: pulpo, papas, pimentón, aceite de oliva, sal.
        
        - Gazpacho Andaluz: Sopa fría de tomate, pepino y pimiento. Precio: $9.000. Ingredientes: tomate, pepino, pimiento, cebolla, ajo, aceite de oliva, vinagre.
        
        PLATOS PRINCIPALES:
        
        CARNES:
        - Solomillo de Ternera: Solomillo de 300g con salsa de vino tinto y puré de papas. Precio: $35.000. Ingredientes: solomillo de ternera, vino tinto, puré de papas, hierbas aromáticas.
        
        - Cordero al Horno: Pierna de cordero marinada con romero y papas asadas. Precio: $32.000. Ingredientes: pierna de cordero, romero, papas, aceite de oliva, ajo.
        
        - Cochinillo Asado: Cochinillo de 1kg con patatas y verduras. Precio: $45.000. Ingredientes: cochinillo, patatas, zanahorias, cebolla, vino blanco.
        
        PESCADOS Y MARISCOS:
        - Paella Valenciana: Arroz con pollo, conejo, judías verdes y azafrán. Precio: $28.000. Ingredientes: arroz bomba, pollo, conejo, judías verdes, azafrán, tomate.
        
        - Paella de Mariscos: Arroz con langostinos, mejillones, calamares y azafrán. Precio: $32.000. Ingredientes: arroz bomba, langostinos, mejillones, calamares, azafrán.
        
        - Bacalao a la Vizcaína: Bacalao con salsa de pimientos rojos y cebolla. Precio: $26.000. Ingredientes: bacalao, pimientos rojos, cebolla, aceite de oliva, ajo.
        
        - Merluza en Salsa Verde: Merluza con salsa de perejil, ajo y vino blanco. Precio: $24.000. Ingredientes: merluza, perejil, ajo, vino blanco, aceite de oliva.
        
        VEGETARIANOS:
        - Risotto de Setas: Arroz cremoso con setas silvestres y trufa. Precio: $22.000. Ingredientes: arroz arborio, setas variadas, trufa, vino blanco, parmesano.
        
        - Tortilla Española: Tortilla de patatas tradicional con cebolla. Precio: $14.000. Ingredientes: patatas, huevos, cebolla, aceite de oliva, sal.
        
        - Ensalada de Quinoa: Quinoa con vegetales frescos, aguacate y vinagreta de limón. Precio: $18.000. Ingredientes: quinoa, tomate, pepino, aguacate, limón, aceite de oliva.
        
        POSTRES:
        - Flan de Caramelo: Flan casero con caramelo líquido. Precio: $8.000. Ingredientes: huevos, leche, azúcar, vainilla.
        
        - Tarta de Santiago: Tarta de almendras tradicional gallega. Precio: $10.000. Ingredientes: almendras, azúcar, huevos, limón.
        
        - Crema Catalana: Crema quemada con azúcar caramelizado. Precio: $9.000. Ingredientes: leche, yemas de huevo, azúcar, canela, limón.
        
        - Helado de Turrón: Helado artesanal de turrón de Jijona. Precio: $7.000. Ingredientes: turrón, leche, azúcar, huevos.
        
        BEBIDAS:
        VINOS:
        - Rioja Reserva (copa): Vino tinto español. Precio: $12.000.
        - Albariño (copa): Vino blanco gallego. Precio: $10.000.
        - Cava Brut (copa): Vino espumoso español. Precio: $14.000.
        
        CERVEZAS:
        - Estrella Galicia: Cerveza española. Precio: $6.000.
        - Mahou: Cerveza española. Precio: $6.000.
        
        REFRESCOS:
        - Limonada Casera: Limonada fresca con menta. Precio: $5.000.
        - Agua Mineral: Agua mineral natural. Precio: $3.000.
        - Café: Café expreso o con leche. Precio: $4.000.
        
        ESPECIALIDADES DEL DIA:
        - Lunes: Cocido Madrileño - Guiso tradicional con garbanzos y carnes. Precio: $20.000.
        - Martes: Fabada Asturiana - Guiso de alubias blancas con chorizo y morcilla. Precio: $22.000.
        - Miércoles: Gazpacho y Salmorejo - Sopas frías andaluzas. Precio: $15.000.
        - Jueves: Pulpo a Feira - Pulpo gallego tradicional. Precio: $25.000.
        - Viernes: Paella de Mariscos - Paella con mariscos frescos. Precio: $32.000.
        - Sábado: Cochinillo Asado - Cochinillo de Segovia. Precio: $45.000.
        - Domingo: Cocido Completo - Cocido madrileño completo. Precio: $25.000.
        """
        
        # Información del restaurante
        restaurant_info = """
        INFORMACION DEL RESTAURANTE LA TABERNA DEL RIO
        
        Ubicación: Av. Rivadavia 456, Viedma, Río Negro, Argentina
        Teléfono: +54 2920 123-4567
        Email: info@latabernadelrio.com.ar
        Horarios: 
        - Lunes a Jueves: 12:00 - 15:00 y 19:00 - 23:00
        - Viernes y Sábado: 12:00 - 15:00 y 19:00 - 23:30
        - Domingo: 12:00 - 15:00 y 19:00 - 22:30
        
        Especialidades: Cocina española tradicional y mediterránea con toques patagónicos
        Ambiente: Familiar y acogedor, ideal para reuniones y celebraciones
        Capacidad: 60 cubiertos
        Reservas: Se recomienda reservar con anticipación
        Formas de pago: Efectivo, tarjeta de crédito/débito, transferencia
        Accesibilidad: Acceso para personas con movilidad reducida
        
        Servicios adicionales:
        - Terraza exterior con vista al río (temporada de verano)
        - Menú para grupos y eventos
        - Servicio de catering para eventos
        - Vinos de bodegas patagónicas y españolas
        - Estacionamiento propio
        - Wi-Fi gratuito para clientes
        """
        
        # Crear documentos
        menu_doc = Document(
            page_content=menu_content,
            metadata={"source": "menu_completo.txt", "type": "menu"}
        )
        
        info_doc = Document(
            page_content=restaurant_info,
            metadata={"source": "info_restaurante.txt", "type": "restaurant_info"}
        )
        
        return [menu_doc, info_doc]
    
    def setup_vectorstore(self):
        """Crear o cargar la base de datos vectorial"""
        documents = self.create_menu_documents()
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
        splits = text_splitter.split_documents(documents)
        
        self.vectorstore = Chroma.from_documents(
            documents=splits, 
            embedding=self.embedding_model
        )
        print("Base de datos vectorial creada correctamente.")
    
    def setup_tools(self):
        """Definir las herramientas del agente"""
        retriever = self.vectorstore.as_retriever(search_kwargs={"k": 3})
        
        self.retriever_tool = create_retriever_tool(
            retriever,
            name="consultar_menu",
            description="Busca información sobre platos del menú, precios, ingredientes, especialidades del día, horarios del restaurante y cualquier información relacionada con La Taberna del Río."
        )
        
        @tool
        def obtener_info_restaurante():
            """Obtiene información básica del restaurante como horarios, ubicación y servicios."""
            return """
            Restaurante La Taberna del Río
            Ubicación: Av. Rivadavia 456, Viedma, Río Negro, Argentina
            Teléfono: +54 2920 123-4567
            Horarios: 
            - Lunes a Jueves: 12:00-15:00 y 19:00-23:00
            - Viernes y Sábado: 12:00-15:00 y 19:00-23:30
            - Domingo: 12:00-15:00 y 19:00-22:30
            Capacidad: 60 cubiertos
            Reservas recomendadas
            """
        
        @tool
        def obtener_plato_del_dia(dia_solicitado: str = "hoy"):
            """Obtiene la especialidad del día. Puede ser 'hoy', 'mañana', 'ayer' o un día específico como 'lunes'."""
            from datetime import datetime, timedelta
            
            # Obtener el día de la semana actual
            hoy = datetime.now()
            dia_actual = hoy.strftime('%A').lower()
            
            # Mapear días en español
            dias_espanol = {
                'monday': 'Lunes',
                'tuesday': 'Martes', 
                'wednesday': 'Miércoles',
                'thursday': 'Jueves',
                'friday': 'Viernes',
                'saturday': 'Sábado',
                'sunday': 'Domingo'
            }
            
            # Mapear días en español a inglés
            dias_a_ingles = {
                'lunes': 'monday',
                'martes': 'tuesday',
                'miércoles': 'wednesday',
                'jueves': 'thursday',
                'viernes': 'friday',
                'sábado': 'saturday',
                'domingo': 'sunday'
            }
            
            especialidades = {
                'monday': 'Cocido Madrileño - Guiso tradicional con garbanzos y carnes. Precio: $20.000.',
                'tuesday': 'Fabada Asturiana - Guiso de alubias blancas con chorizo y morcilla. Precio: $22.000.',
                'wednesday': 'Gazpacho y Salmorejo - Sopas frías andaluzas. Precio: $15.000.',
                'thursday': 'Pulpo a Feira - Pulpo gallego tradicional. Precio: $25.000.',
                'friday': 'Paella de Mariscos - Paella con mariscos frescos. Precio: $32.000.',
                'saturday': 'Cochinillo Asado - Cochinillo de Segovia. Precio: $45.000.',
                'sunday': 'Cocido Completo - Cocido madrileño completo. Precio: $25.000.'
            }
            
            # Determinar qué día buscar
            dia_buscado = dia_actual  # Por defecto es hoy
            
            if dia_solicitado.lower() in ['hoy', 'today']:
                dia_buscado = dia_actual
            elif dia_solicitado.lower() in ['mañana', 'tomorrow']:
                # Calcular mañana
                manana = hoy + timedelta(days=1)
                dia_buscado = manana.strftime('%A').lower()
            elif dia_solicitado.lower() in ['ayer', 'yesterday']:
                # Calcular ayer
                ayer = hoy - timedelta(days=1)
                dia_buscado = ayer.strftime('%A').lower()
            elif dia_solicitado.lower() in dias_a_ingles:
                # Día específico en español
                dia_buscado = dias_a_ingles[dia_solicitado.lower()]
            elif dia_solicitado.lower() in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']:
                # Día específico en inglés
                dia_buscado = dia_solicitado.lower()
            
            # Obtener información
            dia_espanol = dias_espanol.get(dia_buscado, 'Hoy')
            especialidad = especialidades.get(dia_buscado, 'No hay especialidad programada para ese día.')
            
            # Determinar el texto del contexto
            if dia_solicitado.lower() in ['hoy', 'today']:
                contexto = f"Esta es nuestra especialidad de hoy. ¡Es un plato único que solo servimos los {dia_espanol}!"
            elif dia_solicitado.lower() in ['mañana', 'tomorrow']:
                contexto = f"Esta será nuestra especialidad de mañana. ¡Es un plato único que solo servimos los {dia_espanol}!"
            elif dia_solicitado.lower() in ['ayer', 'yesterday']:
                contexto = f"Esta fue nuestra especialidad de ayer. ¡Es un plato único que solo servimos los {dia_espanol}!"
            else:
                contexto = f"Esta es nuestra especialidad de los {dia_espanol}. ¡Es un plato único que solo servimos ese día!"
            
            return f"""
            ESPECIALIDAD DEL DIA - {dia_espanol}
            
            {especialidad}
            
            {contexto}
            """
        
        @tool
        def recomendar_bebida(plato_principal: str):
            """
            Recomienda la bebida perfecta para maridar con un plato principal específico.
            El 'plato_principal' debe ser el nombre exacto del plato o una categoría (ej: 'carne', 'pescado', 'postre').
            """
            plato_lower = plato_principal.lower()
            
            # Lógica de maridaje simple basada en categorías
            if "solomillo" in plato_lower or "cordero" in plato_lower or "cochinillo" in plato_lower or "carne" in plato_lower:
                return "Te recomiendo un excelente **Rioja Reserva**. Sus notas afrutadas y cuerpo fuerte maridan perfectamente con carnes rojas y asados."
            
            elif "paella" in plato_lower or "bacalao" in plato_lower or "merluza" in plato_lower or "pulpo" in plato_lower or "pescado" in plato_lower or "mariscos" in plato_lower:
                return "Para platos de mar y arroces, el **Albariño** (vino blanco gallego) es la elección ideal por su frescura y acidez. Si prefieres algo más audaz, prueba un **Cava Brut**."
                
            elif "risotto" in plato_lower or "tortilla" in plato_lower or "ensalada" in plato_lower or "vegetariano" in plato_lower:
                return "Un plato vegetariano marida muy bien con un vino blanco ligero o un tinto joven. ¿Qué tal una copa de **Albariño** o una refrescante **Limonada Casera**?"
                
            elif "flan" in plato_lower or "tarta" in plato_lower or "crema" in plato_lower or "helado" in plato_lower or "postre" in plato_lower:
                return "Para el postre, te sugiero un delicioso **Café** o un vino dulce, aunque no servimos. ¿Qué te parece una copa de **Cava Brut** para celebrar?"
            
            elif "aperitivo" in plato_lower or "tapas" in plato_lower or "quesos" in plato_lower:
                 return "Para abrir el apetito, una cerveza fría como la **Estrella Galicia** o un buen vino tinto ligero (nuestro Rioja joven) son perfectos."
            
            else:
                return f"Lo siento, no tengo una recomendación específica de maridaje para el plato '{plato_principal}'. ¿Puedes ser más específico?"
        
        @tool
        def agregar_al_pedido(item: str, cantidad: int = 1):
            """Agrega un item al pedido del cliente. El item debe ser el nombre exacto del plato o bebida."""
            # Buscar el item en el diccionario de precios (case insensitive)
            item_encontrado = None
            precio_item = None
            
            for nombre, precio in self.precios.items():
                if nombre.lower() in item.lower() or item.lower() in nombre.lower():
                    item_encontrado = nombre
                    precio_item = precio
                    break
            
            if item_encontrado and precio_item:
                # Agregar al pedido
                for _ in range(cantidad):
                    self.pedido_actual.append({
                        "item": item_encontrado,
                        "precio": precio_item
                    })
                    self.total_pedido += precio_item
                
                return f"[OK] Agregado al pedido: {cantidad}x {item_encontrado} (${precio_item:,} cada uno)\nTotal actual: ${self.total_pedido:,}"
            else:
                return f"[ERROR] No se encontró '{item}' en el menú. Por favor, consulta el menú para ver los platos disponibles."
        
        @tool
        def ver_pedido_actual():
            """Muestra el pedido actual del cliente con el total a pagar."""
            if not self.pedido_actual:
                return "[PEDIDO] Tu pedido está vacío. ¿Te gustaría agregar algo del menú?"
            
            pedido_texto = "[PEDIDO] TU PEDIDO ACTUAL:\n\n"
            for i, item in enumerate(self.pedido_actual, 1):
                pedido_texto += f"{i}. {item['item'].title()} - ${item['precio']:,}\n"
            
            pedido_texto += f"\n[DINERO] TOTAL A PAGAR: ${self.total_pedido:,}"
            
            if self.pagado:
                pedido_texto += "\n[OK] PAGADO"
            
            return pedido_texto
        
        @tool
        def eliminar_del_pedido(numero_item: int):
            """Elimina un item del pedido por su número (ver pedido_actual para ver los números)."""
            if not self.pedido_actual:
                return "[ERROR] Tu pedido está vacío. No hay nada que eliminar."
            
            if numero_item < 1 or numero_item > len(self.pedido_actual):
                return f"[ERROR] Número inválido. Tu pedido tiene {len(self.pedido_actual)} items. Usa ver_pedido_actual para ver los números."
            
            # Eliminar el item (índice es numero_item - 1)
            item_eliminado = self.pedido_actual.pop(numero_item - 1)
            self.total_pedido -= item_eliminado['precio']
            
            return f"[OK] Eliminado: {item_eliminado['item'].title()}\nNuevo total: ${self.total_pedido:,}"
        
        @tool
        def procesar_pago():
            """Procesa el pago del pedido actual. Una vez pagado, el cliente puede salir."""
            if not self.pedido_actual:
                return "[ERROR] No hay nada que pagar. Tu pedido está vacío."
            
            if self.pagado:
                return "[OK] Ya has pagado tu pedido. ¡Gracias por tu visita!"
            
            self.pagado = True
            return f"[OK] PAGO PROCESADO EXITOSAMENTE\n\n[DINERO] Total pagado: ${self.total_pedido:,}\n\n¡Gracias por tu visita! Tu pedido está siendo preparado. ¡Que disfrutes tu comida!"
        
        @tool
        def verificar_estado_pago():
            """Verifica si el cliente ha pagado su pedido."""
            if not self.pedido_actual:
                return "[PEDIDO] No tienes ningún pedido activo."
            
            if self.pagado:
                return "[OK] Has pagado tu pedido. ¡Gracias por tu visita!"
            else:
                return f"💳 Tu pedido de ${self.total_pedido:,} está pendiente de pago. Usa procesar_pago cuando estés listo."
        
        @tool
        def mostrar_menu_completo():
            """Muestra el menú completo del restaurante con todos los platos, precios e ingredientes."""
            return """
[PEDIDO] MENÚ COMPLETO - LA TABERNA DEL RÍO

[PLATO] APERITIVOS:
• Tabla de Quesos y Fiambres - $18.000
  Quesos artesanales, jamón serrano, chorizo y aceitunas

• Croquetas de Jamón Ibérico - $12.000
  Croquetas caseras con jamón ibérico de bellota

• Patatas Bravas - $8.000
  Patatas fritas con salsa brava y alioli

• Pulpo a la Gallega - $16.000
  Pulpo cocido con papas, pimentón y aceite de oliva

• Gazpacho Andaluz - $9.000
  Sopa fría de tomate, pepino y pimiento

[CARNE] CARNES:
• Solomillo de Ternera - $35.000
  Solomillo de 300g con salsa de vino tinto y puré de papas

• Cordero al Horno - $32.000
  Pierna de cordero marinada con romero y papas asadas

• Cochinillo Asado - $45.000
  Cochinillo de 1kg con patatas y verduras

[PESCADO] PESCADOS Y MARISCOS:
• Paella Valenciana - $28.000
  Arroz con pollo, conejo, judías verdes y azafrán

• Paella de Mariscos - $32.000
  Arroz con langostinos, mejillones, calamares y azafrán

• Bacalao a la Vizcaína - $26.000
  Bacalao con salsa de pimientos rojos y cebolla

• Merluza en Salsa Verde - $24.000
  Merluza con salsa de perejil, ajo y vino blanco

[VEGETARIANO] VEGETARIANOS:
• Risotto de Setas - $22.000
  Arroz cremoso con setas silvestres y trufa

• Tortilla Española - $14.000
  Tortilla de patatas tradicional con cebolla

• Ensalada de Quinoa - $18.000
  Quinoa con vegetales frescos, aguacate y vinagreta de limón

[POSTRE] POSTRES:
• Flan de Caramelo - $8.000
• Tarta de Santiago - $10.000
• Crema Catalana - $9.000
• Helado de Turrón - $7.000

[VINO] BEBIDAS:
• Rioja Reserva (copa) - $12.000
• Albariño (copa) - $10.000
• Cava Brut (copa) - $14.000
• Estrella Galicia - $6.000
• Mahou - $6.000
• Limonada Casera - $5.000
• Agua Mineral - $3.000
• Café - $4.000

[ESPECIAL] ESPECIALIDADES DEL DÍA:
• Lunes: Cocido Madrileño - $20.000
• Martes: Fabada Asturiana - $22.000
• Miércoles: Gazpacho y Salmorejo - $15.000
• Jueves: Pulpo a Feira - $25.000
• Viernes: Paella de Mariscos - $32.000
• Sábado: Cochinillo Asado - $45.000
• Domingo: Cocido Completo - $25.000

¿Te gustaría pedir algo del menú?
"""
        
        @tool
        def guardar_conversacion(mensaje_cliente: str, respuesta_robino: str):
            """Guarda la conversación en Notion para análisis posterior."""
            if not self.notion_client:
                return "Conversación registrada localmente (Notion no disponible)"
            
            try:
                # Usar la página específica de La Taberna del Río
                page_id = "28815eef-e926-8038-9583-cff88068af9e"
                
                # Crear timestamp
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                # Crear bloques estructurados
                blocks = [
                    {
                        "object": "block",
                        "type": "divider",
                        "divider": {}
                    },
                    {
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [{"type": "text", "text": {"content": f"[FECHA] {timestamp}"}}]
                        }
                    },
                    {
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [{"type": "text", "text": {"content": f"[CLIENTE] Cliente: {mensaje_cliente}"}}]
                        }
                    },
                    {
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [{"type": "text", "text": {"content": f"[ROBINO] Robino: {respuesta_robino}"}}]
                        }
                    }
                ]
                
                # Agregar a la página
                self.notion_client.blocks.children.append(
                    block_id=page_id,
                    children=blocks
                )
                
                # También guardar en archivo local como backup
                self.guardar_conversacion_local(mensaje_cliente, respuesta_robino, timestamp)
                
                return "Conversación guardada exitosamente en Notion y localmente"
                
            except Exception as e:
                # Si falla Notion, al menos guardar localmente
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.guardar_conversacion_local(mensaje_cliente, respuesta_robino, timestamp)
                return f"Error con Notion, guardado localmente: {str(e)}"
        
        # Asignar las herramientas al agente
        self.tools = [
            self.retriever_tool, 
            obtener_info_restaurante, 
            obtener_plato_del_dia,
            mostrar_menu_completo,
            agregar_al_pedido,
            ver_pedido_actual,
            eliminar_del_pedido,
            procesar_pago,
            verificar_estado_pago,
            guardar_conversacion,
            recomendar_bebida
        ]
        print("Herramientas del agente configuradas.")
    
    def guardar_conversacion(self, mensaje_cliente: str, respuesta_robino: str):
        """Método principal para guardar conversaciones en Notion y localmente."""
        if not self.notion_client:
            # Solo guardar localmente si Notion no está disponible
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.guardar_conversacion_local(mensaje_cliente, respuesta_robino, timestamp)
            return "Conversación registrada localmente (Notion no disponible)"
        
        try:
            # Usar la página específica de La Taberna del Río
            page_id = "28815eef-e926-8038-9583-cff88068af9e"
            
            # Crear timestamp
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Crear bloques estructurados
            blocks = [
                {
                    "object": "block",
                    "type": "divider",
                    "divider": {}
                },
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [{"type": "text", "text": {"content": f"[FECHA] {timestamp}"}}]
                    }
                },
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [{"type": "text", "text": {"content": f"[CLIENTE] Cliente: {mensaje_cliente}"}}]
                    }
                },
                {
                    "object": "block",
                    "type": "paragraph",
                    "paragraph": {
                        "rich_text": [{"type": "text", "text": {"content": f"[ROBINO] Robino: {respuesta_robino}"}}]
                    }
                }
            ]
            
            # Agregar a la página
            self.notion_client.blocks.children.append(
                block_id=page_id,
                children=blocks
            )
            
            # También guardar en archivo local como backup
            self.guardar_conversacion_local(mensaje_cliente, respuesta_robino, timestamp)
            
            return "Conversación guardada exitosamente en Notion y localmente"
            
        except Exception as e:
            # Si falla Notion, al menos guardar localmente
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.guardar_conversacion_local(mensaje_cliente, respuesta_robino, timestamp)
            return f"Error con Notion, guardado localmente: {str(e)}"
    
    def guardar_conversacion_local(self, mensaje_cliente: str, respuesta_robino: str, timestamp: str):
        """Guarda la conversación en un archivo local como backup."""
        try:
            log_entry = f"\n[{timestamp}] Cliente: {mensaje_cliente}\n[{timestamp}] Robino: {respuesta_robino}\n"
            
            with open("conversaciones_robino.log", "a", encoding="utf-8") as f:
                f.write(log_entry)
        except Exception as e:
            print(f"Error guardando conversación local: {e}")
    
    def guardar_conversacion_local_simple(self, mensaje_cliente: str, respuesta_robino: str):
        """Guarda la conversación solo localmente (método simplificado)."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.guardar_conversacion_local(mensaje_cliente, respuesta_robino, timestamp)
    
    def setup_graph(self):
        """Construir el grafo de conversación"""
        def agent_node(state: AgentState):
            """Nodo del agente que procesa mensajes y decide acciones"""
            system_prompt = """
            Eres Robino, el mozo virtual del restaurante "La Taberna del Río". 
            
            Tu personalidad:
            - Eres amable, profesional y servicial
            - Conoces perfectamente el menú y las especialidades
            - Siempre respondes en español
            - Eres paciente y atento con los clientes
            - Tienes sentido del humor pero mantienes la profesionalidad
            
            Tu trabajo:
            1. Saludar cordialmente a los clientes
            2. Ayudar con información del menú y recomendaciones
            3. Tomar pedidos y agregar items a la cuenta del cliente
            4. Ofrecer maridajes y recomendar bebidas para los platos.
            5. Mostrar el pedido actual cuando lo soliciten
            6. Procesar pagos cuando el cliente esté listo
            7. Verificar que el cliente haya pagado antes de permitir que se retire
            8. Responder preguntas sobre horarios, ubicación y servicios

            Instrucciones importantes:
            - Cuando el cliente pida "menú", "carta", "ver el menú", "mostrar menú" → USA 'mostrar_menu_completo'
            - Para preguntas específicas sobre platos individuales, usa 'consultar_menu'
            - Usa 'obtener_info_restaurante' para horarios y ubicación
            - Usa 'obtener_plato_del_dia' cuando pregunten por especialidades del día
            - Si el cliente pregunta por una recomendación de bebida para un plato, USA 'recomendar_bebida'
            - Cuando el cliente quiera pedir algo, usa 'agregar_al_pedido' con el nombre del plato/bebida
            - Cuando pregunten por su pedido, usa 'ver_pedido_actual'
            - Si quieren eliminar algo, usa 'eliminar_del_pedido' con el número del item
            - Cuando estén listos para pagar, usa 'procesar_pago'
            - Para verificar si han pagado, usa 'verificar_estado_pago'
            
            REGLAS IMPORTANTES:
            - NO PERMITAS que el cliente se retire sin pagar
            - Si el cliente intenta salir sin pagar, recuérdale que debe pagar primero
            - Una vez que el cliente pague y se despida, la conversación debe terminar
            - Mantén un registro de todos los items que el cliente pida
            - Sé específico con precios y totales
            - Mantén un tono conversacional pero profesional
            """
            
            messages = [SystemMessage(content=system_prompt)] + state["messages"]
            response = self.llm_with_tools.invoke(messages)
            return {"messages": [response]}
        
        def should_continue(state: AgentState) -> Literal["tools", "__end__"]:
            """Determina si usar herramientas o terminar"""
            if state["messages"][-1].tool_calls:
                return "tools"
            return "__end__"
        
        # Configurar LLM con herramientas
        self.llm_with_tools = self.llm.bind_tools(self.tools)
        
        # Construir grafo
        graph = StateGraph(AgentState)
        graph.add_node("agent", agent_node)
        graph.add_node("tools", ToolNode(self.tools))
        
        graph.set_entry_point("agent")
        graph.add_conditional_edges(
            "agent", should_continue, {"tools": "tools", "__end__": END}
        )
        graph.add_edge("tools", "agent")
        
        self.graph = graph.compile()
        print("Grafo de conversación construido correctamente.")
    
    def initialize_multi_agent(self):
        """Inicializar el sistema multi-agente"""
        try:
            self.multi_agent_system = SimpleMultiAgentMozoVirtual(
                vectorstore=self.vectorstore,
                notion_client=self.notion_client
            )
            print("[OK] Sistema multi-agente inicializado correctamente.")
        except Exception as e:
            print(f"[ADVERTENCIA] Error inicializando sistema multi-agente: {e}")
            self.multi_agent_system = None
    
    def is_complex_query(self, query: str) -> bool:
        """Determina si una consulta requiere el sistema multi-agente"""
        complex_keywords = [
            "recomendar", "recomendación", "sugerir", "qué me recomiendas",
            "qué me sugieres", "ayuda a elegir", "no sé qué pedir",
            "romántica", "pareja", "familia", "negocio", "especial",
            "vegetariano", "vegano", "sin gluten", "alergias", "informe"
        ]
        query_lower = query.lower()
        return any(keyword in query_lower for keyword in complex_keywords)
    
    def start_conversation(self):
        """Iniciar conversación interactiva con Robino"""
        conversation_history = []
        
        print("\n" + "="*60)
        print("    BIENVENIDO A LA TABERNA DEL RIO")
        print("="*60)
        print("\nRobino, tu mozo virtual, está listo para atenderte.")
        print("(Escribe 'salir' para terminar la conversación)")
        
        while True:
            query = input("\nCliente: ")
            if query.lower() in ["exit", "quit", "salir"]:
                # Verificar si el cliente ha pagado antes de permitir que se retire
                if self.pedido_actual and not self.pagado:
                    print(f"\nRobino: ¡Espera! Tienes un pedido pendiente de ${self.total_pedido:,}. Debes pagar antes de retirarte. ¿Quieres procesar el pago ahora?")
                    continue
                elif self.pedido_actual and self.pagado:
                    print("\nRobino: ¡Gracias por tu visita! Tu pedido está siendo preparado. ¡Que disfrutes tu comida!")
                    break
                else:
                    print("\nRobino: ¡Gracias por tu visita! ¡Esperamos verte pronto!")
                    break
            
            # Procesar mensaje
            conversation_history.append(HumanMessage(content=query))
            
            # Decidir si usar sistema multi-agente o agente simple
            if self.is_complex_query(query) and self.multi_agent_system:
                print("\n[BUSCAR] Detectada consulta compleja - Activando sistema multi-agente...")
                try:
                    # Usar sistema multi-agente para consultas complejas
                    final_response = self.multi_agent_system.process_complex_query(query)
                    conversation_history.append(HumanMessage(content=final_response))
                except Exception as e:
                    print(f"[ADVERTENCIA] Error en sistema multi-agente, usando agente simple: {e}")
                    # Fallback al agente simple
                    result = self.graph.invoke({"messages": conversation_history})
                    conversation_history = result["messages"]
                    final_response = conversation_history[-1].content
            else:
                # Usar agente simple para consultas básicas
                result = self.graph.invoke({"messages": conversation_history})
                conversation_history = result["messages"]
                final_response = conversation_history[-1].content
            print(f"\nRobino: {final_response}")
            
            # Verificar si el cliente ha pagado y se está despidiendo
            if self.pagado and self.pedido_actual:
                # Detectar palabras de despedida en la respuesta del agente
                palabras_despedida = ["gracias", "que disfrutes", "preparado", "visita"]
                if any(palabra in final_response.lower() for palabra in palabras_despedida):
                    print("\n" + "="*60)
                    print("¡HASTA LUEGO! ¡Esperamos verte pronto en La Taberna del Río!")
                    print("="*60)
                    break
            
            # Guardar conversación en Notion automáticamente
            try:
                result = self.guardar_conversacion(query, final_response)
                if "Notion" in result and "exitosamente" in result:
                    print("[GUARDAR] Conversación guardada en Notion")
                elif "localmente" in result:
                    print("[GUARDAR] Conversación guardada localmente")
                else:
                    print("[GUARDAR] Conversación guardada")
            except Exception as e:
                print(f"[ADVERTENCIA] Error guardando conversación: {e}")
                # Fallback: guardar solo localmente
                try:
                    self.guardar_conversacion_local_simple(query, final_response)
                    print("[GUARDAR] Conversación guardada localmente como respaldo")
                except Exception as e2:
                    print(f"[ADVERTENCIA] Error crítico guardando conversación: {e2}")


def main():
    """Función principal para ejecutar el agente"""
    try:
        agent = MozoVirtualAgent()
        agent.start_conversation()
    except Exception as e:
        print(f"Error inicializando el agente: {e}")


if __name__ == "__main__":
    main()
