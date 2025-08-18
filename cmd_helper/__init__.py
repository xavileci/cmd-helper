#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cmd Helper - Intelligent command line assistant powered by Google Gemini AI

A smart command-line assistant that converts natural language requests into
executable shell commands using Google's Gemini AI model.

Features:
- Natural language to shell command conversion
- Multi-language support (Spanish/English) 
- Safety checks for dangerous commands
- Context-aware suggestions
- Cross-platform compatibility (Linux, macOS, Windows)
"""

__version__ = "1.0.0"
__author__ = "Xavier León"
__email__ = "github@spmd.simplelogin.com"
__description__ = "Intelligent command line assistant powered by Google Gemini AI"

# Import main components for easier access
from .main import CmdHelper
from .config import Config
from .i18n import t, get_translator

__all__ = [
    'CmdHelper',
    'Config', 
    't',
    'get_translator',
    '__version__',
    '__author__',
    '__email__',
    '__description__'
]
