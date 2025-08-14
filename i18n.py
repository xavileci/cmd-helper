# -*- coding: utf-8 -*-
import json
import os
from pathlib import Path

class Translator:
    """Maneja la internacionalización de la aplicación"""
    
    def __init__(self, language='es'):
        self.language = language
        self.translations = {}
        self.load_translations()
    
    def load_translations(self):
        """Carga las traducciones desde el archivo JSON correspondiente"""
        try:
            locales_dir = Path(__file__).parent / 'locales'
            file_path = locales_dir / f'{self.language}.json'
            
            if not file_path.exists():
                # Fallback a español si no existe el idioma
                file_path = locales_dir / 'es.json'
                self.language = 'es'
            
            with open(file_path, 'r', encoding='utf-8') as f:
                self.translations = json.load(f)
                
        except Exception as e:
            print(f"Error loading translations: {e}")
            # Fallback a traducciones básicas en español
            self.translations = {
                "messages": {
                    "analyzing_request": "🤖 Analizando tu petición...",
                    "no_command_generated": "No pude generar un comando para tu petición."
                }
            }
    
    def get(self, key_path, default=None):
        """
        Obtiene una traducción usando notación de punto
        Ejemplo: t.get('messages.analyzing_request')
        """
        keys = key_path.split('.')
        value = self.translations
        
        try:
            for key in keys:
                value = value[key]
            return value
        except (KeyError, TypeError):
            return default or key_path
    
    def set_language(self, language):
        """Cambia el idioma de la aplicación"""
        if language != self.language:
            self.language = language
            self.load_translations()
    
    def get_available_languages(self):
        """Retorna los idiomas disponibles"""
        locales_dir = Path(__file__).parent / 'locales'
        if not locales_dir.exists():
            return ['es']
        
        languages = []
        for file_path in locales_dir.glob('*.json'):
            languages.append(file_path.stem)
        
        return sorted(languages)
    
    def detect_system_language(self):
        """Detecta el idioma del sistema"""
        import locale
        try:
            # Obtener configuración regional del sistema
            system_locale = locale.getdefaultlocale()[0]
            if system_locale:
                # Extraer código de idioma (ej: 'en_US' -> 'en')
                lang_code = system_locale.split('_')[0].lower()
                available_langs = self.get_available_languages()
                
                if lang_code in available_langs:
                    return lang_code
        except:
            pass
        
        # Fallback a español
        return 'es'

# Instancia global del traductor
_translator = None

def get_translator(language=None):
    """Obtiene la instancia global del traductor"""
    global _translator
    
    if _translator is None:
        if language is None:
            # Auto-detectar idioma del sistema
            temp_translator = Translator()
            language = temp_translator.detect_system_language()
        _translator = Translator(language)
    elif language and language != _translator.language:
        _translator.set_language(language)
    
    return _translator

def t(key_path, default=None):
    """Función de conveniencia para obtener traducciones"""
    translator = get_translator()
    return translator.get(key_path, default)
