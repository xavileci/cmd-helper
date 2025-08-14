"""
# Cmd Helper - Asistente Inteligente para Línea de Comandos

Herramienta multiplataforma que te ayuda a generar y ejecutar comandos de shell usando lenguaje natural.

## Instalación

1. Clona o descarga el proyecto
2. Instala dependencias:
   ```bash
   pip install -r requirements.txt
   ```
3. Configura tu API key de Google Gemini:
   ```bash
   export GEMINI_API_KEY='tu-api-key-aqui'
   ```
   O crea archivo `.env`:
   ```
   GEMINI_API_KEY=tu-api-key-aqui
   ```

## Uso

```bash
python main.py "listar archivos python modificados hoy"
python main.py "encontrar archivos grandes en este directorio"
python main.py "mostrar espacio en disco"
python main.py "comprimir carpeta backup"
```

## Características

- ✅ Multiplataforma (Linux, macOS, Windows)
- ✅ Análisis de contexto inteligente
- ✅ Confirmación antes de ejecutar
- ✅ Detección de comandos peligrosos
- ✅ Integración con Git
- ✅ Colores y formato amigable

## Comandos de ejemplo

| Petición | Comando generado |
|----------|------------------|
| "listar archivos python" | `find . -name "*.py" -type f` |
| "archivos modificados hoy" | `find . -newermt "$(date +%Y-%m-%d)" -type f` |
| "espacio en disco" | `df -h` |
| "procesos que usan más CPU" | `top -n 1 -b \| head -20` |

## Seguridad

- Confirmación obligatoria para comandos peligrosos
- Timeout de 30 segundos para evitar comandos colgados
- Exclusión automática de directorios sensibles
- Parsing seguro de comandos

## Desarrollo

Para contribuir o modificar:

1. El contexto se analiza en `context_analyzer.py`
2. La comunicación con OpenAI está en `mcp_server.py`
3. La ejecución segura en `command_handler.py`
4. La configuración en `config.py`
"""
