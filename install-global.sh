#!/bin/bash

# cmd-helper Global Installation Script - Robust Version
# This script handles dependency conflicts for global installation

set -e

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

print_message() {
    local color=$1
    local message=$2
    echo -e "${color}${message}${NC}"
}

print_header() {
    echo
    print_message $CYAN "=================================================="
    print_message $CYAN "$1"
    print_message $CYAN "=================================================="
    echo
}

detect_language() {
    local lang_var="${LANG:-${LC_ALL:-en_US}}"
    case "$lang_var" in
        es_*|ES_*) echo "es" ;;
        *) echo "en" ;;
    esac
}

setup_messages() {
    local lang=$(detect_language)
    
    if [ "$lang" = "es" ]; then
        MSG_WELCOME="🚀 Instalación Global Robusta de cmd-helper"
        MSG_DESCRIPTION="Instalando con manejo inteligente de dependencias"
        MSG_CHECKING_PYTHON="🔍 Verificando Python..."
        MSG_PYTHON_OK="✅ Python encontrado:"
        MSG_PYTHON_ERROR="❌ Python 3.8+ requerido"
        MSG_UPDATING_DEPS="📦 Actualizando dependencias críticas..."
        MSG_INSTALLING="🔧 Instalando cmd-helper..."
        MSG_SUCCESS="🎉 ¡Instalación completada!"
        MSG_TESTING="🧪 Probando instalación..."
        MSG_TEST_OK="✅ Comandos funcionando correctamente"
        MSG_TEST_FAIL="❌ Error en prueba. Verificando conflictos..."
        MSG_RESOLVING="🔧 Resolviendo conflictos de dependencias..."
        MSG_FINAL_SUCCESS="🌟 ¡cmd-helper instalado y funcionando!"
    else
        MSG_WELCOME="🚀 Robust Global Installation of cmd-helper"
        MSG_DESCRIPTION="Installing with intelligent dependency management"
        MSG_CHECKING_PYTHON="🔍 Checking Python..."
        MSG_PYTHON_OK="✅ Python found:"
        MSG_PYTHON_ERROR="❌ Python 3.8+ required"
        MSG_UPDATING_DEPS="📦 Updating critical dependencies..."
        MSG_INSTALLING="🔧 Installing cmd-helper..."
        MSG_SUCCESS="🎉 Installation completed!"
        MSG_TESTING="🧪 Testing installation..."
        MSG_TEST_OK="✅ Commands working correctly"
        MSG_TEST_FAIL="❌ Test failed. Checking conflicts..."
        MSG_RESOLVING="🔧 Resolving dependency conflicts..."
        MSG_FINAL_SUCCESS="🌟 cmd-helper installed and working!"
    fi
}

check_python() {
    print_message $BLUE "$MSG_CHECKING_PYTHON"
    
    if command -v python3 &> /dev/null; then
        PYTHON_CMD="python3"
    elif command -v python &> /dev/null; then
        PYTHON_CMD="python"
    else
        print_message $RED "$MSG_PYTHON_ERROR"
        exit 1
    fi
    
    PYTHON_VERSION=$($PYTHON_CMD -c "import sys; print('.'.join(map(str, sys.version_info[:2])))")
    PYTHON_MAJOR=$($PYTHON_CMD -c "import sys; print(sys.version_info[0])")
    PYTHON_MINOR=$($PYTHON_CMD -c "import sys; print(sys.version_info[1])")
    
    if [ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -ge 8 ]; then
        print_message $GREEN "$MSG_PYTHON_OK $PYTHON_VERSION"
    else
        print_message $RED "$MSG_PYTHON_ERROR"
        exit 1
    fi
}

update_critical_dependencies() {
    print_message $BLUE "$MSG_UPDATING_DEPS"
    
    # Update typing-extensions first
    $PYTHON_CMD -m pip install --user --upgrade typing-extensions>=4.14.1 || true
    
    # Update other critical dependencies
    $PYTHON_CMD -m pip install --user --upgrade setuptools wheel || true
    $PYTHON_CMD -m pip install --user --upgrade pydantic || true
}

install_cmd_helper() {
    print_message $BLUE "$MSG_INSTALLING"
    
    # Try normal installation first
    if $PYTHON_CMD -m pip install --user .; then
        print_message $GREEN "$MSG_SUCCESS"
        return 0
    else
        print_message $YELLOW "Instalación inicial falló. Intentando resolución de conflictos..."
        return 1
    fi
}

resolve_conflicts() {
    print_message $BLUE "$MSG_RESOLVING"
    
    # Force upgrade of problematic packages
    $PYTHON_CMD -m pip install --user --upgrade --force-reinstall typing-extensions
    $PYTHON_CMD -m pip install --user --upgrade --force-reinstall pydantic
    $PYTHON_CMD -m pip install --user --upgrade --force-reinstall google-generativeai
    
    # Try installation again
    $PYTHON_CMD -m pip install --user --force-reinstall .
}

test_installation() {
    print_message $BLUE "$MSG_TESTING"
    
    # Get user bin directory
    local user_base=$($PYTHON_CMD -m site --user-base 2>/dev/null || echo "$HOME/.local")
    local user_bin="$user_base/bin"
    
    # Test if commands exist and work
    if [ -f "$user_bin/cmd-helper" ] && [ -f "$user_bin/cmdh" ]; then
        # Test version command
        if $user_bin/cmd-helper --version >/dev/null 2>&1; then
            print_message $GREEN "$MSG_TEST_OK"
            return 0
        else
            print_message $YELLOW "$MSG_TEST_FAIL"
            return 1
        fi
    else
        print_message $YELLOW "$MSG_TEST_FAIL"
        return 1
    fi
}

show_final_summary() {
    local user_base=$($PYTHON_CMD -m site --user-base 2>/dev/null || echo "$HOME/.local")
    local user_bin="$user_base/bin"
    
    print_header "$MSG_FINAL_SUCCESS"
    
    print_message $GREEN "Comandos disponibles:"
    echo "  • cmd-helper  - Comando completo"
    echo "  • cmdh        - Alias corto"
    echo
    
    print_message $CYAN "Ubicación:"
    echo "  $user_bin"
    echo
    
    # Check if user bin is in PATH
    if [[ ":$PATH:" != *":$user_bin:"* ]]; then
        print_message $YELLOW "Para usar globalmente, agrega a tu PATH:"
        echo "  export PATH=\"\$PATH:$user_bin\""
        echo
        print_message $YELLOW "Agrega esta línea a tu ~/.bashrc o ~/.zshrc"
        echo
    fi
    
    print_message $CYAN "Ejemplo de uso:"
    echo "  cmd-helper \"listar archivos grandes\""
    echo "  cmdh \"mostrar uso de disco\""
    echo
    
    print_message $CYAN "Configuración:"
    echo "  Necesitas configurar GEMINI_API_KEY"
    echo "  export GEMINI_API_KEY=\"tu-api-key\""
    echo
}

main() {
    setup_messages
    
    print_header "$MSG_WELCOME"
    print_message $CYAN "$MSG_DESCRIPTION"
    echo
    
    check_python
    update_critical_dependencies
    
    if install_cmd_helper; then
        if test_installation; then
            show_final_summary
        else
            print_message $YELLOW "Instalación completada pero con problemas. Resolviendo..."
            resolve_conflicts
            if test_installation; then
                show_final_summary
            else
                print_message $RED "No se pudo resolver completamente. Instalación manual requerida."
                exit 1
            fi
        fi
    else
        resolve_conflicts
        if test_installation; then
            show_final_summary
        else
            print_message $RED "Instalación falló. Revisa los errores arriba."
            exit 1
        fi
    fi
}

main "$@"
