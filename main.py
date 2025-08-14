#!/usr/bin/env python3
# -*- coding: utf-8 -*-
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
from i18n import t, get_translator

# Inicializar colorama
init(autoreset=True)


class CmdHelper:
    """Clase principal de la aplicación"""

    def __init__(self):
        self.config = Config()

        # Inicializar traductor según configuración
        if self.config.LANGUAGE == 'auto':
            self.translator = get_translator()  # Auto-detectar
        else:
            self.translator = get_translator(self.config.LANGUAGE)

        self.mcp_server = MCPServer()
        self.command_handler = CommandHandler()

    def validate_setup(self):
        """Valida que la configuración esté correcta"""
        if not self.config.GEMINI_API_KEY:
            api_key_msg = t('config.api_key_not_found')
            print(Fore.RED + api_key_msg + Style.RESET_ALL)
            print(t('config.api_key_setup'))
            print(t('config.export_command'))
            print(t('config.env_file'))
            return False
        return True

    def process_request(self, user_input):
        """Procesa una petición del usuario"""
        print(Fore.BLUE + t('messages.analyzing_request') + Style.RESET_ALL)

        # Generar comando usando MCP + Gemini
        result = self.mcp_server.generate_command(user_input)

        if not result['command']:
            print(Fore.RED + t('messages.no_command_generated') + Style.RESET_ALL)
            if result['explanation']:
                print(t('messages.reason') + " " + result['explanation'])
            return

        # Mostrar resultado y pedir confirmación
        if self.command_handler.confirm_execution(result['command'], result['explanation']):
            # Ejecutar comando
            execution_result = self.command_handler.execute_command(result['command'])

            if execution_result['success']:
                success_msg = t('messages.command_executed_successfully')
                print("\n" + Fore.GREEN + success_msg + Style.RESET_ALL)
            else:
                error_msg = t('messages.execution_error')
                print("\n" + Fore.RED + error_msg + Style.RESET_ALL)
        else:
            print(Fore.YELLOW + t('messages.operation_cancelled') + Style.RESET_ALL)


@click.command()
@click.argument('request', required=True)
@click.option('--version', is_flag=True, help='Show version / Mostrar versión')
@click.option('--lang', type=click.Choice(['es', 'en', 'auto']), default='auto',
              help='Set language (es=Spanish, en=English, auto=detect)')
def main(request, version, lang):
    """
    Cmd Helper - Intelligent command line assistant / 
    Asistente inteligente para línea de comandos
    """

    # Configurar idioma si se especifica
    if lang != 'auto':
        get_translator(lang)

    if version:
        print(t('app.version'))
        return

    # Mostrar banner
    print(Fore.CYAN + "=" * 50)
    print(Fore.CYAN + "🚀 " + t('app.name'))
    print(Fore.CYAN + "=" * 50 + Style.RESET_ALL)

    # Inicializar aplicación
    app = CmdHelper()

    # Validar configuración
    if not app.validate_setup():
        sys.exit(1)

    # Procesar petición
    try:
        app.process_request(request)
    except KeyboardInterrupt:
        cancelled_msg = t('messages.operation_cancelled_by_user')
        print("\n" + Fore.YELLOW + cancelled_msg + Style.RESET_ALL)
    except OSError as e:
        error_msg = t('messages.unexpected_error')
        print("\n" + Fore.RED + error_msg + " " + str(e) + Style.RESET_ALL)


if __name__ == '__main__':
    main()
