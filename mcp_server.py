import json
import google.generativeai as genai
from config import Config
from context_analyzer import ContextAnalyzer

class MCPServer:
    """Servidor MCP que se comunica con Google Gemini"""
    
    def __init__(self):
        self.config = Config()
        genai.configure(api_key=self.config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel(self.config.MODEL_NAME)
        self.context_analyzer = ContextAnalyzer()
        
        # Prompt del sistema optimizado para comandos de shell
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
            full_prompt = f"{self.system_prompt}\n{json.dumps(context, indent=2)}\n\nPetición del usuario: {user_request}"
            
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
                'explanation': f'Error conectando con Gemini: {str(e)}',
                'is_dangerous': False
            }
    
    def _parse_response(self, response_text):
        """Parsea la respuesta de OpenAI"""
        try:
            lines = response_text.strip().split('\n')
            command = None
            explanation = ""
            is_dangerous = False
            
            for line in lines:
                if line.startswith('COMANDO:'):
                    command = line.replace('COMANDO:', '').strip()
                elif line.startswith('EXPLICACIÓN:'):
                    explanation = line.replace('EXPLICACIÓN:', '').strip()
                elif line.startswith('PELIGRO:'):
                    danger_text = line.replace('PELIGRO:', '').strip().upper()
                    is_dangerous = danger_text.startswith('SI')
            
            # Si no encontramos formato estructurado, usar respuesta completa
            if not command:
                # Buscar líneas que parezcan comandos
                for line in lines:
                    if line.strip() and not line.startswith('#'):
                        command = line.strip()
                        explanation = "Comando generado por IA"
                        break
            
            return {
                'command': command,
                'explanation': explanation,
                'is_dangerous': is_dangerous
            }
            
        except Exception as e:
            return {
                'command': None,
                'explanation': f'Error procesando respuesta: {str(e)}',
                'is_dangerous': False
            }

