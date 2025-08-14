#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de configuración para Cmd Helper
Ayuda a configurar la aplicación de forma interactiva
"""

import os
import sys
from pathlib import Path

def detect_system_language():
    """Detecta el idioma del sistema"""
    import locale
    try:
        system_locale = locale.getdefaultlocale()[0]
        if system_locale:
            lang_code = system_locale.split('_')[0].lower()
            if lang_code in ['es', 'en']:
                return lang_code
    except:
        pass
    return 'en'

def setup_config():
    """Configuración interactiva"""
    lang = detect_system_language()
    
    if lang == 'es':
        print("🚀 Configuración de Cmd Helper")
        print("=" * 40)
        api_key_prompt = "Introduce tu API key de Google Gemini: "
        lang_prompt = "Selecciona idioma (auto/es/en) [auto]: "
        success_msg = "✅ Configuración completada correctamente!"
        env_created_msg = "📁 Archivo .env creado"
        instructions = """
📝 Instrucciones:
1. Obtén tu API key en: https://makersuite.google.com/app/apikey
2. El archivo .env ha sido creado en el directorio actual
3. Ahora puedes usar: python main.py "tu comando aquí"

Ejemplos de uso:
• python main.py "listar archivos python"
• python main.py "mostrar espacio en disco"
• python main.py "encontrar archivos grandes"
"""
    else:
        print("🚀 Cmd Helper Setup")
        print("=" * 40)
        api_key_prompt = "Enter your Google Gemini API key: "
        lang_prompt = "Select language (auto/es/en) [auto]: "
        success_msg = "✅ Configuration completed successfully!"
        env_created_msg = "📁 .env file created"
        instructions = """
📝 Instructions:
1. Get your API key at: https://makersuite.google.com/app/apikey
2. The .env file has been created in the current directory
3. Now you can use: python main.py "your command here"

Usage examples:
• python main.py "list python files"
• python main.py "show disk space"  
• python main.py "find large files"
"""
    
    # Solicitar API key
    api_key = input(api_key_prompt).strip()
    if not api_key:
        print("❌ API key is required")
        sys.exit(1)
    
    # Solicitar idioma
    language = input(lang_prompt).strip() or 'auto'
    if language not in ['auto', 'es', 'en']:
        language = 'auto'
    
    # Crear archivo .env
    env_content = f"""# Configuración de Cmd Helper

# API Key de Google Gemini (REQUERIDO)
GEMINI_API_KEY={api_key}

# Configuración de idioma (OPCIONAL)
# Valores: 'auto' (detectar automáticamente), 'es' (español), 'en' (inglés)
CMD_HELPER_LANG={language}
"""
    
    env_path = Path('.env')
    with open(env_path, 'w', encoding='utf-8') as f:
        f.write(env_content)
    
    print(f"\n{success_msg}")
    print(f"{env_created_msg}")
    print(instructions)

if __name__ == '__main__':
    setup_config()
