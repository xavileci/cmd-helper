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

### Opción 1: Instalador Global Robusto (Recomendado)

```bash
# Clona el repositorio
git clone https://github.com/your-username/cmd-helper.git
cd cmd-helper

# Limpia instalaciones previas (opcional)
./cleanup.sh

# Ejecuta el instalador robusto
./install-global.sh
```

### Opción 2: Instalador Básico (Entorno Virtual)

```bash
# Clona el repositorio
git clone https://github.com/your-username/cmd-helper.git
cd cmd-helper

# Ejecuta el instalador básico
./install.sh
```

### Opción 3: Instalación Manual

```bash
# Clona el repositorio
git clone https://github.com/your-username/cmd-helper.git
cd cmd-helper

# Actualiza dependencias críticas
pip install --user --upgrade typing-extensions>=4.14.1

# Instala el paquete
pip install --user .
```

### Opción 4: Usando pip directamente (cuando esté en PyPI)

```bash
pip install --user cmd-helper
```

### 🛠️ Resolución de Problemas

Si encuentras errores de dependencias al instalar globalmente:

```bash
# Paso 1: Limpia instalaciones previas
./cleanup.sh

# Paso 2: Actualiza dependencias críticas
python3 -m pip install --user --upgrade typing-extensions pydantic

# Paso 3: Instala con el script robusto
./install-global.sh
```

---

## ⚙️ Configuración / Configuration

### Configurar API Key de Gemini

Para usar cmd-helper, necesitas configurar tu API key de Google Gemini:

#### Obtener API Key
1. Ve a [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Crea una cuenta o inicia sesión
3. Genera una nueva API key (es gratuita)

#### Configurar la API Key

```bash
export GEMINI_API_KEY="tu-api-key-aqui"
```

### Archivo de Configuración

Puedes crear un archivo `.env` en cualquiera de estas ubicaciones:
- `~/.cmd-helper/.env`
- `~/.config/cmd-helper/.env`  
- `./.env` (directorio actual)

Ejemplo de `.env`:
```bash
# API Key de Gemini
GEMINI_API_KEY=tu-gemini-api-key

# Configuración opcional
CMD_HELPER_LANG=auto  # auto, es, en
MODEL_NAME=gemini-2.5-flash
MAX_TOKENS=1000
TEMPERATURE=0.1
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
- `google-generativeai` - Cliente Google Gemini

---

## 🧪 Testing y Calidad de Código / Testing and Code Quality

### Ejecutar Tests

El proyecto incluye una suite completa de tests con **88% de cobertura de código**:

```bash
# Ejecutar todos los tests
pytest tests/

# Ejecutar tests con reporte de cobertura
pytest tests/ --cov=cmd_helper --cov-report=term

# Ejecutar tests para SonarQube (genera reportes XML)
./run_tests_sonar.sh
```

### Suite de Tests

- **70 tests** cubriendo todos los módulos principales
- **Tests unitarios** con mocking apropiado
- **Tests de integración** para funcionalidad end-to-end
- **Cobertura por módulo**:
  - `config.py`: 100%
  - `mcp_server.py`: 95%
  - `command_handler.py`: 89%
  - `main.py`: 89%
  - `context_analyzer.py`: 82%
  - `i18n.py`: 77%

### SonarQube Integration

El proyecto está configurado para análisis continuo de código con SonarQube:

```bash
# Ejecutar análisis local (requiere sonar-scanner)
sonar-scanner

# El pipeline de CI/CD ejecuta automáticamente:
# - Tests con cobertura
# - Análisis de calidad de código
# - Detección de vulnerabilidades
# - Métricas de mantenibilidad
```

### Archivos de Configuración

- `sonar-project.properties` - Configuración de SonarQube
- `pytest.ini` - Configuración de tests
- `requirements-dev.txt` - Dependencias de desarrollo
- `.github/workflows/sonar.yml` - Pipeline de CI/CD

### Scripts de Desarrollo

```bash
# Ejecutar tests con reportes para SonarQube
./run_tests_sonar.sh

# Limpiar archivos temporales y de desarrollo
./clean.sh

# Ver reporte de cobertura HTML
open htmlcov/index.html
```

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
