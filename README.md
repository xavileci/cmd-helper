# 🚀 cmd-helper

**Asistente inteligente para línea de comandos con IA** / **Intelligent AI-powered command line assistant**

cmd-helper es una herramienta que convierte peticiones en lenguaje natural en comandos de línea de comandos, utilizando inteligencia artificial para ayudarte a ser más productivo en la terminal.

---

## 🌟 Características / Features

- 🤖 **IA Integrada**: Soporte para OpenAI GPT y Anthropic Claude
- 🌐 **Multiidioma**: Interfaz en español e inglés con detección automática
- ⚡ **Rápido**: Comandos optimizados con alias corto `cmdh`
- 🔧 **Configurable**: Configuración flexible con archivos .env
- 🎯 **Inteligente**: Análisis de contexto del directorio actual
- 📦 **Fácil Instalación**: Script de instalación automático

---

## 🚀 Instalación Rápida / Quick Installation

### Opción 1: Instalador Automático (Recomendado)

```bash
# Clona el repositorio
git clone https://github.com/your-username/cmd-helper.git
cd cmd-helper

# Ejecuta el instalador
./install.sh
```

### Opción 2: Instalación Manual

```bash
# Clona el repositorio
git clone https://github.com/your-username/cmd-helper.git
cd cmd-helper

# Instala usando pip
pip install --user .

# O para desarrollo
pip install --user -e .
```

### Opción 3: Usando pip directamente (cuando esté en PyPI)

```bash
pip install --user cmd-helper
```

---

## ⚙️ Configuración / Configuration

### Configurar API Keys

Para usar las funciones de IA, necesitas configurar al menos una API key:

#### OpenAI
```bash
export OPENAI_API_KEY="tu-api-key-aqui"
```

#### Anthropic (Claude)
```bash
export ANTHROPIC_API_KEY="tu-api-key-aqui"
```

### Archivo de Configuración

Puedes crear un archivo `.env` en cualquiera de estas ubicaciones:
- `~/.cmd-helper/.env`
- `~/.config/cmd-helper/.env`
- `./.env` (directorio actual)

Ejemplo de `.env`:
```bash
# API Keys
OPENAI_API_KEY=tu-openai-key
ANTHROPIC_API_KEY=tu-anthropic-key

# Configuración
LANG=auto  # auto, es, en
OPENAI_MODEL=gpt-4
ANTHROPIC_MODEL=claude-3-sonnet-20240229
API_TIMEOUT=30
MAX_RETRIES=3
```

---

## 💡 Uso / Usage

### Comandos Disponibles

- `cmd-helper` - Comando completo
- `cmdh` - Alias corto (recomendado)

### Ejemplos / Examples

```bash
# Listar archivos grandes
cmdh "encuentra archivos grandes en este directorio"

# Comprimir carpeta
cmd-helper "comprime la carpeta docs en un zip"

# Monitorear sistema
cmdh "muestra el uso de CPU y memoria"

# Gestión de archivos
cmd-helper "encuentra todos los archivos .log y los borra"

# Con idioma específico
cmd-helper --lang en "find large files"
cmdh --lang es "crear un backup"
```

### Opciones

```bash
cmd-helper [OPTIONS] REQUEST

Options:
  --version            Mostrar versión
  --lang [es|en|auto]  Establecer idioma
  --help               Mostrar ayuda
```

---

## 🛠️ Desarrollo / Development

### Configurar entorno de desarrollo

```bash
# Clonar repositorio
git clone https://github.com/your-username/cmd-helper.git
cd cmd-helper

# Crear entorno virtual
python3 -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Instalar en modo desarrollo
pip install -e .
```

### Ejecutar tests

```bash
# Instalar dependencias de desarrollo
pip install pytest pytest-cov

# Ejecutar tests
pytest

# Con cobertura
pytest --cov=cmd_helper
```

### Estructura del Proyecto

```
cmd-helper/
├── cmd_helper/           # Paquete principal
│   ├── __init__.py      # Inicialización del paquete
│   ├── main.py          # Punto de entrada principal
│   ├── config.py        # Gestión de configuración
│   ├── command_handler.py # Manejo de comandos
│   ├── context_analyzer.py # Análisis de contexto
│   ├── mcp_server.py    # Servidor MCP
│   ├── i18n.py          # Internacionalización
│   └── locales/         # Archivos de traducción
│       ├── en.json
│       └── es.json
├── setup.py             # Configuración de instalación
├── requirements.txt     # Dependencias
├── install.sh          # Script de instalación
├── README.md           # Documentación
└── LICENSE             # Licencia
```

---

## 📋 Requisitos / Requirements

- **Python**: 3.8 o superior
- **Sistema Operativo**: macOS, Linux, Windows
- **Dependencias**: Ver `requirements.txt`

### Dependencias Principales

- `click` - Interfaz de línea de comandos
- `colorama` - Colores en terminal
- `python-dotenv` - Gestión de variables de entorno
- `requests` - Peticiones HTTP
- `openai` - Cliente OpenAI
- `anthropic` - Cliente Anthropic

---

## 🤝 Contribuir / Contributing

¡Las contribuciones son bienvenidas! Para contribuir:

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/amazing-feature`)
3. Commit tus cambios (`git commit -m 'Add amazing feature'`)
4. Push a la rama (`git push origin feature/amazing-feature`)
5. Abre un Pull Request

### Reportar Issues

Si encuentras un bug o tienes una sugerencia:
1. Busca en los issues existentes
2. Si no existe, crea uno nuevo con:
   - Descripción clara del problema
   - Pasos para reproducir
   - Comportamiento esperado vs actual
   - Información del sistema

---

## 📄 Licencia / License

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

---

## 🙏 Agradecimientos / Acknowledgments

- Gracias a todos los contribuidores
- Inspirado por herramientas como GitHub Copilot CLI
- Powered by OpenAI y Anthropic

---

## 📞 Soporte / Support

- **Issues**: [GitHub Issues](https://github.com/your-username/cmd-helper/issues)
- **Documentación**: Este README
- **Email**: tu-email@ejemplo.com

---

**¿Te gusta cmd-helper? ⭐ ¡Dale una estrella en GitHub!**
