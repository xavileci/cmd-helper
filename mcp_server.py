# -*- coding: utf-8 -*-
"""
MCP Server Module

This module handles communication with Google Gemini AI model to generate
shell commands based on natural language requests.
"""

import json
import google.generativeai as genai
from config import Config
from context_analyzer import ContextAnalyzer
from i18n import t, get_translator


class MCPServer:
    """Servidor MCP que se comunica con Google Gemini"""

    def __init__(self):
        self.config = Config()
        genai.configure(api_key=self.config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(self.config.MODEL_NAME)
        self.context_analyzer = ContextAnalyzer()

        # Inicializar traductor según configuración
        if self.config.LANGUAGE == 'auto':
            translator = get_translator()  # Auto-detectar
        else:
            translator = get_translator(self.config.LANGUAGE)

        # Obtener el idioma actual del traductor
        current_lang = translator.language

        # Prompt del sistema optimizado para comandos de shell
        if current_lang == 'en':
            self.system_prompt = """You are an expert cross-platform command line assistant (Linux, macOS, Windows).

IMPORTANT RULES:
1. Respond ONLY with safe executable commands
2. Briefly explain what each command does
3. Prioritize simple and standard commands
4. If you detect something dangerous, warn clearly
5. Adapt commands according to detected platform
6. If unsure, suggest the safest command

MANDATORY RESPONSE FORMAT:
COMMAND: [exact command here]
EXPLANATION: [what it does in 1-2 lines]
DANGER: [YES/NO and why if dangerous]

Example:
COMMAND: find . -name "*.py" -type f
EXPLANATION: Finds all files with .py extension in current directory and subdirectories
DANGER: NO

Current system context:"""
        else:
            self.system_prompt = """Eres un asistente experto en línea de comandos multiplataforma (Linux, macOS, Windows).

REGLAS IMPORTANTES:
1. Responde SOLO con comandos ejecutables seguros
2. Explica brevemente qué hace cada comando
3. Prioriza comandos simples y estándar
4. Si detectas algo peligroso, advierte claramente
5. Adapta comandos según la plataforma detectada
6. Si no estás seguro, sugiere el comando más seguro

FORMATO DE RESPUESTA OBLIGATORIO:
COMANDO: [comando exacto aquí]
EXPLICACIÓN: [qué hace en 1-2 líneas]
PELIGRO: [SI/NO y por qué si es peligroso]

Ejemplo:
COMANDO: find . -name "*.py" -type f
EXPLICACIÓN: Busca todos los archivos con extensión .py en el directorio actual y subdirectorios
PELIGRO: NO

Contexto actual del sistema:"""

    def generate_command(self, user_request):
        """Genera comando basado en la petición del usuario"""
        try:
            # Obtener contexto actual
            context = self.context_analyzer.get_current_context()

            # Construir prompt completo
            full_prompt = (f"{self.system_prompt}\n{json.dumps(context, indent=2)}\n\n"
                          f"Petición del usuario: {user_request}")

            # Configuración de generación
            generation_config = genai.types.GenerationConfig(
                max_output_tokens=self.config.MAX_TOKENS,
                temperature=self.config.TEMPERATURE,
            )

            # Generar respuesta
            response = self.model.generate_content(
                full_prompt,
                generation_config=generation_config
            )

            return self._parse_response(response.text)

        except Exception as e:
            return {
                'command': None,
                'explanation': t("context.gemini_connection_error") + " " + str(e),
                'is_dangerous': False
            }

    def _parse_response(self, response_text):
        """Parsea la respuesta de Gemini"""
        try:
            lines = response_text.strip().split('\n')
            command = None
            explanation = ""
            is_dangerous = False

            # Detectar idioma para parsear correctamente
            translator = get_translator()

            # Palabras clave según el idioma
            command_keywords = ['COMMAND:', 'COMANDO:']
            explanation_keywords = ['EXPLANATION:', 'EXPLICACIÓN:']
            danger_keywords = ['DANGER:', 'PELIGRO:']

            for line in lines:
                # Comando
                if any(keyword in line for keyword in command_keywords):
                    for keyword in command_keywords:
                        if keyword in line:
                            command = line.replace(keyword, '').strip()
                            break

                # Explicación
                elif any(keyword in line for keyword in explanation_keywords):
                    for keyword in explanation_keywords:
                        if keyword in line:
                            explanation = line.replace(keyword, '').strip()
                            break

                # Peligro
                elif any(keyword in line for keyword in danger_keywords):
                    for keyword in danger_keywords:
                        if keyword in line:
                            danger_text = line.replace(keyword, '').strip().upper()
                            is_dangerous = (danger_text.startswith('YES') or
                                          danger_text.startswith('SI'))
                            break

            # Si no encontramos formato estructurado, usar respuesta completa
            if not command:
                # Buscar líneas que parezcan comandos
                for line in lines:
                    if line.strip() and not line.startswith('#'):
                        command = line.strip()
                        explanation = t('context.ai_generated_command')
                        break

            return {
                'command': command,
                'explanation': explanation,
                'is_dangerous': is_dangerous
            }

        except Exception as e:
            return {
                'command': None,
                'explanation': t("context.response_processing_error") + " " + str(e),
                'is_dangerous': False
            }

