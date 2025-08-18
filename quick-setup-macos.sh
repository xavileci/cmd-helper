#!/bin/bash

# cmd-helper Quick Setup for macOS
# This script installs pipx via Homebrew and then installs cmd-helper

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

print_message() {
    echo -e "${1}${2}${NC}"
}

print_header() {
    echo
    print_message $CYAN "=================================================="
    print_message $CYAN "$1"
    print_message $CYAN "=================================================="
    echo
}

main() {
    print_header "🚀 cmd-helper Setup Rápido para macOS"
    
    print_message $BLUE "🔍 Verificando Homebrew..."
    
    if ! command -v brew &> /dev/null; then
        print_message $RED "❌ Homebrew no encontrado"
        print_message $YELLOW "Instala Homebrew primero: https://brew.sh"
        exit 1
    fi
    
    print_message $GREEN "✅ Homebrew encontrado"
    
    print_message $BLUE "📦 Instalando pipx..."
    brew install pipx
    
    print_message $BLUE "⚙️ Configurando pipx..."
    pipx ensurepath
    
    print_message $BLUE "🔧 Instalando cmd-helper..."
    pipx install .
    
    print_message $GREEN "🎉 ¡Instalación completada!"
    echo
    print_message $CYAN "Para usar inmediatamente:"
    echo "  export PATH=\"\$PATH:$HOME/.local/bin\""
    echo
    print_message $CYAN "Configuración de API:"
    echo "  export GEMINI_API_KEY=\"tu-api-key\""
    echo
    print_message $CYAN "Probar:"
    echo "  cmd-helper --version"
    echo "  cmdh \"listar archivos\""
}

main "$@"
