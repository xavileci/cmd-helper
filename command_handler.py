# -*- coding: utf-8 -*-
"""
Command Handler Module

This module handles the safe execution of system commands with user confirmation
and security checks for potentially dangerous operations.
"""

import subprocess
from colorama import Fore, Style, init
from config import Config
from i18n import t

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
        print("\n" + Fore.CYAN + t('commands.suggested_command') + Style.RESET_ALL)
        print(Fore.WHITE + command + Style.RESET_ALL)

        if explanation:
            print("\n" + Fore.GREEN + t('commands.explanation') + Style.RESET_ALL)
            print(explanation)

        if self.is_command_dangerous(command):
            print("\n" + Fore.RED + t('security.warning') + Style.RESET_ALL)
            confirmation = input("\n" + t('security.confirm_dangerous') + " ")
            # Aceptar tanto "SI" (español) como "YES" (inglés)
            return confirmation.upper() in ["SI", "YES"]

        confirmation = input("\n" + t('commands.execute_command') + " ")
        return confirmation.lower() in ['y', 'yes', 'sí', 'si']

    def execute_command(self, command):
        """Ejecuta un comando de forma segura"""
        try:
            print("\n" + Fore.YELLOW + t('commands.executing') + " " + command + Style.RESET_ALL)

            # Ejecutar con shell para permitir expansión de globs y pipes
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30,  # Timeout de 30 segundos
                check=False  # No raise exception on non-zero exit
            )

            if result.stdout:
                print("\n" + Fore.GREEN + t('commands.output') + Style.RESET_ALL)
                print(result.stdout)

            if result.stderr and result.returncode != 0:
                print("\n" + Fore.RED + t('commands.error') + Style.RESET_ALL)
                print(result.stderr)

            return {
                'success': result.returncode == 0,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'return_code': result.returncode
            }

        except subprocess.TimeoutExpired:
            print(Fore.RED + t('security.timeout_error') + Style.RESET_ALL)
            return {'success': False, 'error': 'Timeout'}

        except OSError as e:
            print(Fore.RED + t('security.execution_error') + " " + str(e) + Style.RESET_ALL)
            return {'success': False, 'error': str(e)}