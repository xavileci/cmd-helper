# -*- coding: utf-8 -*-
"""
MCP Server Module

This module handles communication with Google Gemini AI model to generate
shell commands based on natural language requests.
"""

import json
import google.generativeai as genai
from .config import Config
from .context_analyzer import ContextAnalyzer
from .i18n import t, get_translator


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
            self.system_prompt = """You are an expert cross-platform command line assistant
(Linux, macOS, Windows).

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
            self.system_prompt = """Eres un asistente experto en línea de comandos
multiplataforma (Linux, macOS, Windows).

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

            # Verificar si la respuesta fue bloqueada por filtros de seguridad
            if not response.candidates:
                return {
                    'command': None,
                    'explanation': t("context.safety_filter_blocked"),
                    'is_dangerous': False
                }

            candidate = response.candidates[0]
            
            # Verificar finish_reason
            if hasattr(candidate, 'finish_reason'):
                if candidate.finish_reason == 2:  # SAFETY
                    return {
                        'command': None,
                        'explanation': t("context.safety_filter_blocked"),
                        'is_dangerous': False
                    }
                elif candidate.finish_reason == 3:  # RECITATION
                    return {
                        'command': None,
                        'explanation': t("context.recitation_blocked"),
                        'is_dangerous': False
                    }

            # Verificar si hay texto válido en la respuesta
            if not hasattr(response, 'text') or not response.text:
                return {
                    'command': None,
                    'explanation': t("context.empty_response"),
                    'is_dangerous': False
                }

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
            parsed_data = self._extract_structured_data(lines)
            
            if not parsed_data['command']:
                parsed_data['command'] = self._extract_fallback_command(lines)
                if parsed_data['command']:
                    parsed_data['explanation'] = t('context.ai_generated_command')
        
            return parsed_data
        
        except Exception as e:
            return {
                'command': None,
                'explanation': t("context.response_processing_error") + " " + str(e),
                'is_dangerous': False
            }

    def _extract_structured_data(self, lines):
        """Extrae datos estructurados de las líneas de respuesta"""
        result = {
            'command': None,
            'explanation': "",
            'is_dangerous': False
        }
        
        for line in lines:
            self._process_command_line(line, result)
            self._process_explanation_line(line, result)
            self._process_danger_line(line, result)
        
        return result

    def _process_command_line(self, line, result):
        """Procesa líneas que contienen comandos"""
        command_keywords = ['COMMAND:', 'COMANDO:']
        for keyword in command_keywords:
            if keyword in line:
                result['command'] = line.replace(keyword, '').strip()
                return

    def _process_explanation_line(self, line, result):
        """Procesa líneas que contienen explicaciones"""
        explanation_keywords = ['EXPLANATION:', 'EXPLICACIÓN:']
        for keyword in explanation_keywords:
            if keyword in line:
                result['explanation'] = line.replace(keyword, '').strip()
                return

    def _process_danger_line(self, line, result):
        """Procesa líneas que contienen información de peligro"""
        danger_keywords = ['DANGER:', 'PELIGRO:']
        for keyword in danger_keywords:
            if keyword in line:
                danger_text = line.replace(keyword, '').strip().upper()
                result['is_dangerous'] = self._is_dangerous_response(danger_text)
                return

    def _is_dangerous_response(self, danger_text):
        """Determina si la respuesta indica peligro"""
        return danger_text.startswith('YES') or danger_text.startswith('SI')

    def _extract_fallback_command(self, lines):
        """Extrae comando como fallback cuando no hay formato estructurado"""
        for line in lines:
            stripped_line = line.strip()
            if stripped_line and not stripped_line.startswith('#'):
                return stripped_line
        return None
