# -*- coding: utf-8 -*-
"""
Configuration Module

This module contains all configuration settings for the Cmd Helper application,
including API keys, model settings, and security configurations.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from multiple locations
# 1. Current directory .env (for development)
# 2. User's home config directory (for installed package)
env_locations = [
    Path.cwd() / '.env',
    Path.home() / '.cmd-helper' / 'config.env',
    Path.home() / '.config' / 'cmd-helper' / 'config.env'
]

for env_file in env_locations:
    if env_file.exists():
        load_dotenv(env_file)
        break


class Config:
    """Configuration class containing all application settings"""

    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    MODEL_NAME = "gemini-2.5-flash"  # Modelo más reciente gratuito y potente
    MAX_TOKENS = 1000
    TEMPERATURE = 0.1  # Respuestas más deterministas para comandos

    # Configuración de idioma
    LANGUAGE = os.getenv('CMD_HELPER_LANG', 'auto')  # 'auto', 'es', 'en'

    # Comandos peligrosos que siempre requieren confirmación extra
    DANGEROUS_COMMANDS = [
        'rm -rf', 'sudo rm', 'chmod 777', 'mkfs', 'dd if=',
        'shutdown', 'reboot', 'halt', '> /dev/', 'format'
    ]

    # Directorios que no debe analizar por seguridad
    EXCLUDED_DIRS = [
        '.git', 'node_modules', '__pycache__', '.venv',
        'venv', '.ssh', '/proc', '/sys', '/dev', '/'
    ]
