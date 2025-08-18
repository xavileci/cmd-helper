#!/bin/bash

# cmd-helper Global Installer / Instalador Global de cmd-helper
# This script installs cmd-helper globally and makes it available as a system command
# Este script instala cmd-helper globalmente y lo hace disponible como comando del sistema

set -e

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Function to print colored messages
print_message() {
    local color=$1
    local message=$2
    echo -e "${color}${message}${NC}"
}

# Function to print header
print_header() {
    echo
    print_message $CYAN "=================================================="
    print_message $CYAN "$1"
    print_message $CYAN "=================================================="
    echo
}

# Detect system language
detect_language() {
    local lang_var="${LANG:-${LC_ALL:-en_US}}"
    case "$lang_var" in
        es_*|ES_*) echo "es" ;;
        *) echo "en" ;;
    esac
}

# Set language-specific messages
setup_messages() {
    local lang=$(detect_language)
    
    if [ "$lang" = "es" ]; then
        MSG_WELCOME="🚀 Instalador de cmd-helper"
        MSG_DESCRIPTION="Instalando el asistente inteligente para línea de comandos con IA"
        MSG_CHECKING_PYTHON="🔍 Verificando instalación de Python..."
        MSG_PYTHON_OK="✅ Python encontrado:"
        MSG_PYTHON_ERROR="❌ Python 3.8+ es requerido. Por favor instala Python 3.8 o superior."
        MSG_CHECKING_PIP="🔍 Verificando pip..."
        MSG_PIP_OK="✅ pip está disponible"
        MSG_INSTALLING="📦 Instalando cmd-helper..."
        MSG_SUCCESS="🎉 ¡Instalación completada exitosamente!"
        MSG_USAGE="💡 Uso:"
        MSG_EXAMPLES="📋 Ejemplos:"
        MSG_CONFIG="⚙️  Configuración:"
        MSG_CONFIG_DESC="Para usar las funciones de IA, configura tu API key:"
        MSG_OPENAI_CONFIG="Para OpenAI:"
        MSG_ANTHROPIC_CONFIG="Para Anthropic (Claude):"
        MSG_CONFIG_FILE="O edita el archivo de configuración:"
        MSG_ALIASES="🔗 Comandos disponibles:"
        MSG_PATH_INFO="📍 Los comandos se instalaron en:"
        MSG_PATH_HINT="Si los comandos no están disponibles, agrega esta ruta a tu PATH:"
        MSG_ERROR="❌ Error durante la instalación:"
    else
        MSG_WELCOME="🚀 cmd-helper Installer"
        MSG_DESCRIPTION="Installing the intelligent AI-powered command line assistant"
        MSG_CHECKING_PYTHON="🔍 Checking Python installation..."
        MSG_PYTHON_OK="✅ Python found:"
        MSG_PYTHON_ERROR="❌ Python 3.8+ is required. Please install Python 3.8 or higher."
        MSG_CHECKING_PIP="🔍 Checking pip..."
        MSG_PIP_OK="✅ pip is available"
        MSG_INSTALLING="📦 Installing cmd-helper..."
        MSG_SUCCESS="🎉 Installation completed successfully!"
        MSG_USAGE="💡 Usage:"
        MSG_EXAMPLES="📋 Examples:"
        MSG_CONFIG="⚙️  Configuration:"
        MSG_CONFIG_DESC="To use AI features, configure your API key:"
        MSG_OPENAI_CONFIG="For OpenAI:"
        MSG_ANTHROPIC_CONFIG="For Anthropic (Claude):"
        MSG_CONFIG_FILE="Or edit the config file:"
        MSG_ALIASES="🔗 Available commands:"
        MSG_PATH_INFO="📍 Commands installed to:"
        MSG_PATH_HINT="If commands are not available, add this path to your PATH:"
        MSG_ERROR="❌ Error during installation:"
    fi
}

# Check Python version
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
    
    # Check Python version
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

# Check pip
check_pip() {
    print_message $BLUE "$MSG_CHECKING_PIP"
    
    if $PYTHON_CMD -m pip --version &> /dev/null; then
        print_message $GREEN "$MSG_PIP_OK"
    else
        print_message $RED "❌ pip not found"
        exit 1
    fi
}

# Install cmd-helper
install_cmd_helper() {
    print_message $BLUE "$MSG_INSTALLING"
    
    # Check if we're in a virtual environment
    if [[ -n "$VIRTUAL_ENV" ]]; then
        # In virtual environment, install normally
        $PYTHON_CMD -m pip install . || {
            print_message $RED "$MSG_ERROR pip install failed"
            exit 1
        }
    else
        # Not in virtual environment, install for user
        $PYTHON_CMD -m pip install --user . || {
            print_message $RED "$MSG_ERROR pip install failed"
            exit 1
        }
    fi
    
    print_message $GREEN "$MSG_SUCCESS"
}

# Get user bin directory
get_user_bin() {
    if [[ -n "$VIRTUAL_ENV" ]]; then
        # In virtual environment
        echo "$VIRTUAL_ENV/bin"
    else
        # Not in virtual environment, use user base
        local user_base=$($PYTHON_CMD -m site --user-base 2>/dev/null || echo "$HOME/.local")
        echo "$user_base/bin"
    fi
}

# Show installation summary
show_summary() {
    local user_bin=$(get_user_bin)
    
    echo
    print_header "$MSG_SUCCESS"
    
    print_message $GREEN "$MSG_ALIASES"
    echo "  • cmd-helper  - Full command name"
    echo "  • cmdh        - Short alias"
    echo
    
    print_message $CYAN "$MSG_PATH_INFO"
    echo "  $user_bin"
    echo
    
    # Check if user bin is in PATH
    if [[ ":$PATH:" != *":$user_bin:"* ]]; then
        print_message $YELLOW "$MSG_PATH_HINT"
        echo "  export PATH=\"\$PATH:$user_bin\""
        echo
        print_message $YELLOW "Add this line to your ~/.bashrc or ~/.zshrc file"
        echo
    fi
    
    print_message $CYAN "$MSG_USAGE"
    echo "  cmd-helper \"list files in current directory\""
    echo "  cmdh \"show disk usage\""
    echo
    
    print_message $CYAN "$MSG_EXAMPLES"
    echo "  cmd-helper \"find large files\""
    echo "  cmdh \"compress this folder\""
    echo "  cmd-helper --lang en \"create a backup\""
    echo
    
    print_message $CYAN "$MSG_CONFIG"
    print_message $YELLOW "$MSG_CONFIG_DESC"
    echo
    echo "$MSG_OPENAI_CONFIG"
    echo "  export OPENAI_API_KEY=\"your-api-key-here\""
    echo
    echo "$MSG_ANTHROPIC_CONFIG"
    echo "  export ANTHROPIC_API_KEY=\"your-api-key-here\""
    echo
    echo "$MSG_CONFIG_FILE"
    echo "  ~/.cmd-helper/.env"
    echo "  ~/.config/cmd-helper/.env"
    echo
}

# Main execution
main() {
    # Setup messages based on system language
    setup_messages
    
    # Show welcome header
    print_header "$MSG_WELCOME"
    print_message $CYAN "$MSG_DESCRIPTION"
    echo
    
    # Run installation steps
    check_python
    check_pip
    install_cmd_helper
    show_summary
}

# Run main function
main "$@"
