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
            
            # Ejecutar con shell para permitir expansión de globs y pipes
            result = subprocess.run(
                command,
                shell=True,
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

