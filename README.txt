# ================================
# ESTRUCTURA DE ARCHIVOS:
# ================================
# cmd-helper/
# ├── main.py
# ├── mcp_server.py  
# ├── command_handler.py
# ├── context_analyzer.py
# ├── config.py
# ├── requirements.txt
# └── README.md

# ================================
# requirements.txt
# ================================
"""
google-generativeai>=0.3.0
click>=8.1.0
colorama>=0.4.6
python-dotenv>=1.0.0
"""

# ================================
# config.py
# ================================
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    MODEL_NAME = "gemini-1.5-flash"  # Modelo gratuito y rápido
    MAX_TOKENS = 1000
    TEMPERATURE = 0.1  # Respuestas más deterministas para comandos
    
    # Comandos peligrosos que siempre requieren confirmación extra
    DANGEROUS_COMMANDS = [
        'rm -rf', 'sudo rm', 'chmod 777', 'mkfs', 'dd if=', 
        'shutdown', 'reboot', 'halt', '> /dev/', 'format'
    ]
    
    # Directorios que no debe analizar por seguridad
    EXCLUDED_DIRS = [
        '.git', 'node_modules', '__pycache__', '.venv', 
        'venv', '.ssh', '/proc', '/sys', '/dev'
    ]

# ================================
# context_analyzer.py  
# ================================
import os
import subprocess
import json
from pathlib import Path
from config import Config

class ContextAnalyzer:
    """Analiza el contexto actual del sistema para enviar a la LLM"""
    
    def __init__(self):
        self.config = Config()
    
    def get_current_context(self):
        """Obtiene contexto completo del directorio actual"""
        context = {
            'pwd': os.getcwd(),
            'platform': self._get_platform(),
            'files': self._get_directory_listing(),
            'git_info': self._get_git_info(),
            'env_vars': self._get_relevant_env_vars(),
            'recent_commands': self._get_recent_commands()
        }
        return context
    
    def _get_platform(self):
        """Detecta la plataforma (Linux/macOS/Windows)"""
        import platform
        return {
            'system': platform.system(),
            'release': platform.release(),
            'shell': os.environ.get('SHELL', 'unknown')
        }
    
    def _get_directory_listing(self, max_files=50):
        """Lista archivos del directorio actual (limitado por seguridad)"""
        try:
            files = []
            current_dir = Path('.')
            
            for item in current_dir.iterdir():
                if len(files) >= max_files:
                    break
                    
                if item.name.startswith('.') and item.name not in ['.env', '.gitignore']:
                    continue
                    
                if item.name in self.config.EXCLUDED_DIRS:
                    continue
                
                files.append({
                    'name': item.name,
                    'type': 'dir' if item.is_dir() else 'file',
                    'size': item.stat().st_size if item.is_file() else None
                })
            
            return files
        except Exception as e:
            return [{'error': f'Cannot read directory: {str(e)}'}]
    
    def _get_git_info(self):
        """Información básica de git si está disponible"""
        try:
            branch = subprocess.check_output(
                ['git', 'branch', '--show-current'], 
                stderr=subprocess.DEVNULL,
                text=True
            ).strip()
            
            status = subprocess.check_output(
                ['git', 'status', '--porcelain'], 
                stderr=subprocess.DEVNULL,
                text=True
            ).strip()
            
            return {
                'branch': branch,
                'has_changes': bool(status),
                'is_git_repo': True
            }
        except:
            return {'is_git_repo': False}
    
    def _get_relevant_env_vars(self):
        """Variables de entorno relevantes para desarrollo"""
        relevant_vars = ['PATH', 'HOME', 'USER', 'SHELL', 'PYTHON_VERSION', 'NODE_VERSION']
        return {var: os.environ.get(var) for var in relevant_vars if os.environ.get(var)}
    
    def _get_recent_commands(self):
        """Últimos comandos del historial (si es posible)"""
        try:
            # Intentar leer historial de bash
            history_file = os.path.expanduser('~/.bash_history')
            if os.path.exists(history_file):
                with open(history_file, 'r') as f:
                    lines = f.readlines()
                    return [line.strip() for line in lines[-10:] if line.strip()]
        except:
            pass
        return []

# ================================
# command_handler.py
# ================================
import subprocess
import shlex
import sys
from colorama import Fore, Style, init
from config import Config

# Inicializar colorama para multiplataforma
init(autoreset=True)

class CommandHandler:
    """Maneja la ejecución segura de comandos del sistema"""
    
    def __init__(self):
        self.config = Config()
    
    def is_command_dangerous(self, command):
        """Verifica si un comando es potencialmente peligroso"""
        command_lower = command.lower()
        return any(dangerous in command_lower for dangerous in self.config.DANGEROUS_COMMANDS)
    
    def confirm_execution(self, command, explanation=""):
        """Pide confirmación al usuario antes de ejecutar"""
        print(f"\n{Fore.CYAN}Comando sugerido:{Style.RESET_ALL}")
        print(f"{Fore.WHITE}{command}{Style.RESET_ALL}")
        
        if explanation:
            print(f"\n{Fore.GREEN}Explicación:{Style.RESET_ALL}")
            print(f"{explanation}")
        
        if self.is_command_dangerous(command):
            print(f"\n{Fore.RED}⚠️  ADVERTENCIA: Este comando puede ser peligroso{Style.RESET_ALL}")
            confirmation = input(f"\n¿Estás SEGURO que quieres ejecutar este comando? (escribir 'SI'): ")
            return confirmation == "SI"
        else:
            confirmation = input(f"\n¿Ejecutar este comando? (y/N): ")
            return confirmation.lower() in ['y', 'yes', 'sí', 'si']
    
    def execute_command(self, command):
        """Ejecuta un comando de forma segura"""
        try:
            print(f"\n{Fore.YELLOW}Ejecutando: {command}{Style.RESET_ALL}")
            
            # Usar shlex para parsing seguro
            args = shlex.split(command)
            
            result = subprocess.run(
                args,
                capture_output=True,
                text=True,
                timeout=30  # Timeout de 30 segundos
            )
            
            if result.stdout:
                print(f"\n{Fore.GREEN}Salida:{Style.RESET_ALL}")
                print(result.stdout)
            
            if result.stderr and result.returncode != 0:
                print(f"\n{Fore.RED}Error:{Style.RESET_ALL}")
                print(result.stderr)
            
            return {
                'success': result.returncode == 0,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'return_code': result.returncode
            }
            
        except subprocess.TimeoutExpired:
            print(f"{Fore.RED}Error: El comando excedió el tiempo límite (30s){Style.RESET_ALL}")
            return {'success': False, 'error': 'Timeout'}
            
        except Exception as e:
            print(f"{Fore.RED}Error ejecutando comando: {str(e)}{Style.RESET_ALL}")
            return {'success': False, 'error': str(e)}

# ================================
# mcp_server.py
# ================================
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

# ================================
# main.py
# ================================
#!/usr/bin/env python3
"""
Cmd Helper - Asistente inteligente para línea de comandos
Uso: python main.py "tu petición en lenguaje natural"
"""

import sys
import click
from colorama import Fore, Style, init
from mcp_server import MCPServer
from command_handler import CommandHandler
from config import Config

# Inicializar colorama
init(autoreset=True)

class CmdHelper:
    """Clase principal de la aplicación"""
    
    def __init__(self):
        self.config = Config()
        self.mcp_server = MCPServer()
        self.command_handler = CommandHandler()
    
    def validate_setup(self):
        """Valida que la configuración esté correcta"""
        if not self.config.GEMINI_API_KEY:
            print(f"{Fore.RED}Error: No se encontró GEMINI_API_KEY{Style.RESET_ALL}")
            print("Configura tu API key:")
            print("export GEMINI_API_KEY='tu-api-key-aqui'")
            print("O crea un archivo .env con: GEMINI_API_KEY=tu-api-key-aqui")
            return False
        return True
    
    def process_request(self, user_input):
        """Procesa una petición del usuario"""
        print(f"{Fore.BLUE}🤖 Analizando tu petición...{Style.RESET_ALL}")
        
        # Generar comando usando MCP + OpenAI
        result = self.mcp_server.generate_command(user_input)
        
        if not result['command']:
            print(f"{Fore.RED}No pude generar un comando para tu petición.{Style.RESET_ALL}")
            if result['explanation']:
                print(f"Razón: {result['explanation']}")
            return
        
        # Mostrar resultado y pedir confirmación
        if self.command_handler.confirm_execution(result['command'], result['explanation']):
            # Ejecutar comando
            execution_result = self.command_handler.execute_command(result['command'])
            
            if execution_result['success']:
                print(f"\n{Fore.GREEN}✅ Comando ejecutado exitosamente{Style.RESET_ALL}")
            else:
                print(f"\n{Fore.RED}❌ Error en la ejecución{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}Operación cancelada{Style.RESET_ALL}")

@click.command()
@click.argument('request', required=True)
@click.option('--version', is_flag=True, help='Mostrar versión')
def main(request, version):
    """Cmd Helper - Asistente inteligente para línea de comandos"""
    
    if version:
        print("Cmd Helper v1.0.0")
        return
    
    # Mostrar banner
    print(f"{Fore.CYAN}{'='*50}")
    print(f"{Fore.CYAN}🚀 Cmd Helper - Asistente de Comandos IA")
    print(f"{Fore.CYAN}{'='*50}{Style.RESET_ALL}")
    
    # Inicializar aplicación
    app = CmdHelper()
    
    # Validar configuración
    if not app.validate_setup():
        sys.exit(1)
    
    # Procesar petición
    try:
        app.process_request(request)
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Operación cancelada por el usuario{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n{Fore.RED}Error inesperado: {str(e)}{Style.RESET_ALL}")

if __name__ == '__main__':
    main()

# ================================
# README.md
# ================================
"""
# Cmd Helper - Asistente Inteligente para Línea de Comandos

Herramienta multiplataforma que te ayuda a generar y ejecutar comandos de shell usando lenguaje natural.

## Instalación

1. Clona o descarga el proyecto
2. Instala dependencias:
   ```bash
   pip install -r requirements.txt
   ```
3. Configura tu API key de Google Gemini:
   ```bash
   export GEMINI_API_KEY='tu-api-key-aqui'
   ```
   O crea archivo `.env`:
   ```
   GEMINI_API_KEY=tu-api-key-aqui
   ```

## Uso

```bash
python main.py "listar archivos python modificados hoy"
python main.py "encontrar archivos grandes en este directorio"
python main.py "mostrar espacio en disco"
python main.py "comprimir carpeta backup"
```

## Características

- ✅ Multiplataforma (Linux, macOS, Windows)
- ✅ Análisis de contexto inteligente
- ✅ Confirmación antes de ejecutar
- ✅ Detección de comandos peligrosos
- ✅ Integración con Git
- ✅ Colores y formato amigable

## Comandos de ejemplo

| Petición | Comando generado |
|----------|------------------|
| "listar archivos python" | `find . -name "*.py" -type f` |
| "archivos modificados hoy" | `find . -newermt "$(date +%Y-%m-%d)" -type f` |
| "espacio en disco" | `df -h` |
| "procesos que usan más CPU" | `top -n 1 -b \| head -20` |

## Seguridad

- Confirmación obligatoria para comandos peligrosos
- Timeout de 30 segundos para evitar comandos colgados
- Exclusión automática de directorios sensibles
- Parsing seguro de comandos

## Desarrollo

Para contribuir o modificar:

1. El contexto se analiza en `context_analyzer.py`
2. La comunicación con OpenAI está en `mcp_server.py`
3. La ejecución segura en `command_handler.py`
4. La configuración en `config.py`
"""
