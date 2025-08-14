# Internacionalización (i18n) - Guía para Desarrolladores

## Estructura del Sistema i18n

El sistema de internacionalización de Cmd Helper está diseñado para ser simple pero extensible:

```
cmd-helper/
├── i18n.py                    # Clase principal de traducción
├── locales/
│   ├── es.json               # Traducciones en español
│   └── en.json               # Traducciones en inglés
└── config.py                 # Configuración de idioma
```

## Archivos de Traducción

### Estructura JSON

Los archivos de traducción están organizados por categorías:

```json
{
  "app": {
    "name": "Nombre de la aplicación",
    "version": "Versión"
  },
  "messages": {
    "key": "Mensaje traducido"
  },
  "commands": {
    "key": "Comando relacionado"
  }
}
```

### Categorías Disponibles

- **app**: Información general de la aplicación
- **messages**: Mensajes generales del sistema
- **commands**: Textos relacionados con comandos
- **security**: Advertencias y mensajes de seguridad
- **config**: Mensajes de configuración
- **context**: Análisis de contexto y errores
- **help**: Textos de ayuda

## Uso en el Código

### Importar el Sistema de Traducción

```python
from i18n import t, get_translator
```

### Obtener Traducciones

```python
# Método simple
mensaje = t('messages.analyzing_request')

# Con valor por defecto
mensaje = t('messages.unknown_key', 'Valor por defecto')

# Usar notación de punto para acceso anidado
titulo = t('app.name')
```

### Configurar Idioma

```python
# Auto-detectar idioma del sistema
translator = get_translator()

# Forzar idioma específico
translator = get_translator('es')
translator = get_translator('en')

# Cambiar idioma dinámicamente
translator.set_language('en')
```

## Agregar Nuevos Idiomas

### 1. Crear Archivo de Traducción

Crea un nuevo archivo JSON en `locales/` con el código ISO del idioma:

```bash
# Ejemplo para francés
cp locales/es.json locales/fr.json
```

### 2. Traducir Contenido

Edita el archivo JSON con las traducciones correspondientes:

```json
{
  "app": {
    "name": "Cmd Helper - Assistant de Ligne de Commande IA"
  },
  "messages": {
    "analyzing_request": "🤖 Analyse de votre demande..."
  }
}
```

### 3. Actualizar Configuración

El nuevo idioma estará disponible automáticamente. Solo asegúrate de que:

- El archivo JSON sea válido
- Todas las claves principales estén presentes
- Los códigos de idioma sean consistentes

## Detección Automática de Idioma

El sistema detecta automáticamente el idioma usando:

1. **Variable de entorno**: `CMD_HELPER_LANG`
2. **Argumento de línea de comandos**: `--lang`
3. **Detección del sistema**: `locale.getdefaultlocale()`
4. **Fallback**: Español (es)

## Mejores Prácticas

### Para Desarrolladores

1. **Usa claves descriptivas**: `messages.command_executed_successfully` en lugar de `msg1`
2. **Organiza por categorías**: Agrupa textos relacionados
3. **Proporciona contexto**: Usa nombres de claves que expliquen cuándo se usan
4. **Mantén consistencia**: Usa el mismo estilo en todas las traducciones

### Para Traductores

1. **Mantén el contexto**: Entiende dónde y cuándo se usa cada texto
2. **Preserva formatos**: Mantén placeholders como `{variable}` o emojis
3. **Adapta culturalmente**: No solo traduzcas literalmente
4. **Prueba en contexto**: Verifica que las traducciones funcionen en la interfaz

## Ejemplos de Uso Avanzado

### Interpolación de Variables

```python
# En el código
mensaje = f"{t('security.timeout_error')} ({timeout}s)"

# En la traducción
"security.timeout_error": "Error: Command exceeded time limit"
```

### Pluralización Simple

```python
# Para casos simples, usa claves separadas
files_count = 5
if files_count == 1:
    mensaje = t('files.single')
else:
    mensaje = t('files.multiple')
```

### Formateo Específico por Idioma

```python
# Diferentes formatos según el idioma
translator = get_translator()
if translator.language == 'en':
    date_format = "%m/%d/%Y"
else:
    date_format = "%d/%m/%Y"
```

## Configuración de Entorno

### Variables de Entorno

```bash
# Configurar idioma por defecto
export CMD_HELPER_LANG=en

# Auto-detectar (por defecto)
export CMD_HELPER_LANG=auto
```

### Archivo .env

```env
# Configuración de idioma
CMD_HELPER_LANG=es
```

## Solución de Problemas

### Problema: Clave no encontrada

```python
# Siempre proporciona un fallback
texto = t('clave.inexistente', 'Texto por defecto')
```

### Problema: Archivo de traducción corrupto

El sistema automáticamente regresa al español si hay errores:

```python
# En i18n.py se maneja automáticamente
except Exception as e:
    print(f"Error loading translations: {e}")
    # Fallback a traducciones básicas en español
```

### Problema: Idioma no soportado

```python
# Verificar idiomas disponibles
translator = get_translator()
idiomas = translator.get_available_languages()
print(f"Idiomas soportados: {idiomas}")
```
