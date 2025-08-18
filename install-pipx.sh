#!/bin/bash

# cmd-helper Installation for Externally Managed Python Environments
# Uses pipx for safe global installation on macOS/Homebrew systems

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
        MSG_WELCOME="🚀 Instalación cmd-helper para macOS/Homebrew"
        MSG_DESCRIPTION="Instalación segura usando pipx para entornos gestionados"
        MSG_CHECKING="🔍 Verificando sistema..."
        MSG_INSTALLING_PIPX="📦 Instalando pipx..."
        MSG_PIPX_OK="✅ pipx disponible"
        MSG_INSTALLING="🔧 Instalando cmd-helper con pipx..."
        MSG_SUCCESS="🎉 ¡Instalación completada!"
        MSG_CONFIGURING="⚙️ Configurando PATH..."
        MSG_TESTING="🧪 Probando instalación..."
        MSG_TEST_OK="✅ cmd-helper funcionando correctamente"
        MSG_MANUAL_PATH="📍 Agrega manualmente a tu PATH:"
        MSG_USAGE="💡 Uso:"
        MSG_CONFIG="🔑 Configuración de API:"
    else
        MSG_WELCOME="🚀 cmd-helper Installation for macOS/Homebrew"
        MSG_DESCRIPTION="Safe installation using pipx for managed environments"
        MSG_CHECKING="🔍 Checking system..."
        MSG_INSTALLING_PIPX="📦 Installing pipx..."
        MSG_PIPX_OK="✅ pipx available"
        MSG_INSTALLING="🔧 Installing cmd-helper with pipx..."
        MSG_SUCCESS="🎉 Installation completed!"
        MSG_CONFIGURING="⚙️ Configuring PATH..."
        MSG_TESTING="🧪 Testing installation..."
        MSG_TEST_OK="✅ cmd-helper working correctly"
        MSG_MANUAL_PATH="📍 Manually add to your PATH:"
        MSG_USAGE="💡 Usage:"
        MSG_CONFIG="🔑 API Configuration:"
    fi
}

check_system() {
    print_message $BLUE "$MSG_CHECKING"
    
    # Check if we're on macOS
    if [[ "$OSTYPE" == "darwin"* ]]; then
        print_message $GREEN "✅ macOS detected"
    else
        print_message $YELLOW "⚠️  Not macOS, but continuing..."
    fi
    
    # Check if Homebrew is available
    if command -v brew &> /dev/null; then
        print_message $GREEN "✅ Homebrew detected"
        HAVE_BREW=true
    else
        print_message $YELLOW "⚠️  Homebrew not found"
        HAVE_BREW=false
    fi
}

install_pipx() {
    if command -v pipx &> /dev/null; then
        print_message $GREEN "$MSG_PIPX_OK"
        return 0
    fi
    
    print_message $BLUE "$MSG_INSTALLING_PIPX"
    
    if [ "$HAVE_BREW" = true ]; then
        # Install via Homebrew
        brew install pipx
        pipx ensurepath
    else
        # Install via pip with --user
        python3 -m pip install --user pipx --break-system-packages 2>/dev/null || \
        python3 -m pip install --user pipx
        python3 -m pipx ensurepath
    fi
    
    print_message $GREEN "$MSG_PIPX_OK"
}

install_cmd_helper() {
    print_message $BLUE "$MSG_INSTALLING"
    
    # Install cmd-helper using pipx
    pipx install .
    
    print_message $GREEN "$MSG_SUCCESS"
}

configure_path() {
    print_message $BLUE "$MSG_CONFIGURING"
    
    # Get pipx bin directory
    PIPX_BIN_DIR="$HOME/.local/bin"
    
    # Check if it's already in PATH
    if [[ ":$PATH:" == *":$PIPX_BIN_DIR:"* ]]; then
        print_message $GREEN "✅ PATH ya configurado correctamente"
        return 0
    fi
    
    # Try to add to shell profile
    SHELL_PROFILE=""
    if [ -n "$ZSH_VERSION" ]; then
        SHELL_PROFILE="$HOME/.zshrc"
    elif [ -n "$BASH_VERSION" ]; then
        SHELL_PROFILE="$HOME/.bashrc"
        # On macOS, also try .bash_profile
        if [[ "$OSTYPE" == "darwin"* ]] && [ -f "$HOME/.bash_profile" ]; then
            SHELL_PROFILE="$HOME/.bash_profile"
        fi
    fi
    
    if [ -n "$SHELL_PROFILE" ] && [ -w "$SHELL_PROFILE" ]; then
        echo "" >> "$SHELL_PROFILE"
        echo "# Added by cmd-helper installer" >> "$SHELL_PROFILE"
        echo "export PATH=\"\$PATH:$PIPX_BIN_DIR\"" >> "$SHELL_PROFILE"
        print_message $GREEN "✅ PATH agregado a $SHELL_PROFILE"
        print_message $YELLOW "Ejecuta: source $SHELL_PROFILE"
    else
        print_message $YELLOW "$MSG_MANUAL_PATH"
        echo "  export PATH=\"\$PATH:$PIPX_BIN_DIR\""
        echo "  # Agrega esta línea a tu ~/.zshrc o ~/.bashrc"
    fi
}

test_installation() {
    print_message $BLUE "$MSG_TESTING"
    
    # Test with full path first
    PIPX_BIN_DIR="$HOME/.local/bin"
    
    if [ -f "$PIPX_BIN_DIR/cmd-helper" ]; then
        if "$PIPX_BIN_DIR/cmd-helper" --version >/dev/null 2>&1; then
            print_message $GREEN "$MSG_TEST_OK"
            return 0
        fi
    fi
    
    # Test if it's in PATH
    if command -v cmd-helper >/dev/null 2>&1; then
        if cmd-helper --version >/dev/null 2>&1; then
            print_message $GREEN "$MSG_TEST_OK"
            return 0
        fi
    fi
    
    print_message $YELLOW "⚠️  Comando instalado pero no accesible. Configura tu PATH."
    return 1
}

show_final_summary() {
    print_header "$MSG_SUCCESS"
    
    print_message $GREEN "Comandos instalados:"
    echo "  • cmd-helper  - Comando completo"
    echo "  • cmdh        - Alias corto"
    echo
    
    print_message $CYAN "Ubicación:"
    echo "  ~/.local/bin/"
    echo
    
    print_message $CYAN "$MSG_USAGE"
    echo "  cmd-helper \"listar archivos del directorio\""
    echo "  cmdh \"mostrar uso de disco\""
    echo
    
    print_message $CYAN "$MSG_CONFIG"
    echo "  export GEMINI_API_KEY=\"tu-api-key\""
    echo "  # Obtén tu API key en: https://makersuite.google.com/app/apikey"
    echo
    
    if ! command -v cmd-helper >/dev/null 2>&1; then
        print_message $YELLOW "Para usar inmediatamente:"
        echo "  export PATH=\"\$PATH:$HOME/.local/bin\""
        echo
    fi
}

main() {
    setup_messages
    
    print_header "$MSG_WELCOME"
    print_message $CYAN "$MSG_DESCRIPTION"
    echo
    
    check_system
    install_pipx
    install_cmd_helper
    configure_path
    
    if test_installation; then
        show_final_summary
    else
        show_final_summary
        print_message $YELLOW "Nota: Es posible que necesites reiniciar tu terminal."
    fi
}

main "$@"
