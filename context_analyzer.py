# -*- coding: utf-8 -*-
"""
Context Analyzer Module

This module analyzes the current system context to provide relevant information
to the LLM for better command generation.
"""

import os
import subprocess
import platform
import locale
from pathlib import Path
from config import Config
from i18n import t


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
        except OSError as e:
            return [{'error': t('context.directory_error') + " " + str(e)}]

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
        except (subprocess.CalledProcessError, FileNotFoundError):
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
                with open(history_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    return [line.strip() for line in lines[-10:] if line.strip()]
        except (OSError, IOError):
            pass
        return []

