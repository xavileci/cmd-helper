#!/bin/bash

# cmd-helper Cleanup Script
# Removes conflicting installations and prepares for clean install

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_message() {
    echo -e "${1}${2}${NC}"
}

print_message $BLUE "🧹 Limpiando instalaciones previas de cmd-helper..."

# Find Python command
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    print_message $RED "❌ Python no encontrado"
    exit 1
fi

# Uninstall existing cmd-helper packages
print_message $YELLOW "Desinstalando paquetes existentes..."
$PYTHON_CMD -m pip uninstall cmd-helper -y 2>/dev/null || true

# Get user bin directory
USER_BASE=$($PYTHON_CMD -m site --user-base 2>/dev/null || echo "$HOME/.local")
USER_BIN="$USER_BASE/bin"

# Remove command scripts
print_message $YELLOW "Eliminando scripts de comando..."
rm -f "$USER_BIN/cmd-helper" 2>/dev/null || true
rm -f "$USER_BIN/cmdh" 2>/dev/null || true

# Remove from global locations
rm -f /usr/local/bin/cmd-helper 2>/dev/null || true
rm -f /usr/local/bin/cmdh 2>/dev/null || true
rm -f /opt/homebrew/bin/cmd-helper 2>/dev/null || true
rm -f /opt/homebrew/bin/cmdh 2>/dev/null || true

print_message $GREEN "✅ Limpieza completada"
print_message $BLUE "Ahora puedes ejecutar ./install-global.sh para una instalación limpia"
