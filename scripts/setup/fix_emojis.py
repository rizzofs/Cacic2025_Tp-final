#!/usr/bin/env python3
"""
Script para eliminar emojis de los archivos Python
"""

import re
import os

def remove_emojis_from_file(filepath):
    """Elimina emojis de un archivo"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Lista de emojis comunes que causan problemas
        emoji_patterns = [
            r'✅', r'❌', r'⚠️', r'🔍', r'📊', r'💾', r'🤖', r'💰', r'📋',
            r'🚀', r'🎯', r'🎉', r'💡', r'🗓️', r'👤', r'⭐', r'🥩', r'🐟',
            r'🥗', r'🍰', r'🍷', r'🍽️', r'🔗', r'🧪', r'📝', r'📈'
        ]
        
        # Reemplazar emojis con texto simple
        replacements = {
            '✅': '[OK]',
            '❌': '[ERROR]',
            '⚠️': '[ADVERTENCIA]',
            '🔍': '[BUSCAR]',
            '📊': '[INFORME]',
            '💾': '[GUARDAR]',
            '🤖': '[ROBINO]',
            '💰': '[DINERO]',
            '📋': '[PEDIDO]',
            '🚀': '[INICIAR]',
            '🎯': '[OBJETIVO]',
            '🎉': '[EXITO]',
            '💡': '[IDEA]',
            '🗓️': '[FECHA]',
            '👤': '[CLIENTE]',
            '⭐': '[ESPECIAL]',
            '🥩': '[CARNE]',
            '🐟': '[PESCADO]',
            '🥗': '[VEGETARIANO]',
            '🍰': '[POSTRE]',
            '🍷': '[VINO]',
            '🍽️': '[PLATO]',
            '🔗': '[LINK]',
            '🧪': '[TEST]',
            '📝': '[NOTA]',
            '📈': '[ANALISIS]'
        }
        
        # Aplicar reemplazos
        for emoji, replacement in replacements.items():
            content = content.replace(emoji, replacement)
        
        # Escribir archivo modificado
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Emojis eliminados de {filepath}")
        return True
        
    except Exception as e:
        print(f"Error procesando {filepath}: {e}")
        return False

def main():
    """Función principal"""
    files_to_fix = [
        'mozo_virtual_agent.py',
        'multi_agent_system.py',
        'test_multi_agent.py'
    ]
    
    print("Eliminando emojis de archivos Python...")
    
    for filepath in files_to_fix:
        if os.path.exists(filepath):
            remove_emojis_from_file(filepath)
        else:
            print(f"Archivo no encontrado: {filepath}")
    
    print("Proceso completado.")

if __name__ == "__main__":
    main()


