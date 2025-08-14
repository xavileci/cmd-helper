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

