# Cmd Helper - Guía de Instalación

## 🚀 Instalación Automática (Recomendada)

### Opción 1: Script de instalación
```bash
# Clona el repositorio
git clone https://github.com/yourusername/cmd-helper.git
cd cmd-helper

# Ejecuta el instalador automático
./install.sh
```

### Opción 2: Instalación con pip desde el código fuente
```bash
# Clona e instala en un solo paso
git clone https://github.com/yourusername/cmd-helper.git
cd cmd-helper
pip install -e .

# Configura tu API key
python3 setup_config.py
```

### Opción 3: Instalación desde PyPI (cuando esté publicado)
```bash
pip install cmd-helper
cmd-helper --setup  # Configuración inicial
```

## 🔧 Instalación Manual

### Requisitos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Clave API de Google Gemini (gratis)

### Pasos

1. **Clona el repositorio:**
   ```bash
   git clone https://github.com/yourusername/cmd-helper.git
   cd cmd-helper
   ```

2. **Instala las dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Instala el paquete:**
   ```bash
   pip install -e .
   ```

4. **Obtén tu API key de Gemini:**
   - Ve a: https://makersuite.google.com/app/apikey
   - Haz clic en "Create API Key"
   - Copia la clave generada

5. **Configura la aplicación:**
   ```bash
   # Opción A: Configuración interactiva
   python3 setup_config.py
   
   # Opción B: Configuración manual
   mkdir -p ~/.cmd-helper
   echo "GEMINI_API_KEY=tu_clave_aqui" > ~/.cmd-helper/config.env
   echo "CMD_HELPER_LANG=auto" >> ~/.cmd-helper/config.env
   ```

## ✅ Verificación de la instalación

Después de la instalación, verifica que todo funcione:

```bash
# Prueba el comando
cmd-helper "listar archivos Python"

# O usa el alias corto
cmdh "como comprimir una carpeta"

# Verificar versión
cmd-helper --version
```

## 🌍 Ubicaciones de configuración

Cmd Helper busca configuración en este orden:
1. `.env` en el directorio actual (desarrollo)
2. `~/.cmd-helper/config.env` (instalación de usuario)
3. `~/.config/cmd-helper/config.env` (estándar XDG)

## 🔄 Actualización

```bash
# Si instalaste desde código fuente
git pull
pip install -e . --upgrade

# Si instalaste desde PyPI
pip install --upgrade cmd-helper
```

## 🗑️ Desinstalación

```bash
# Desinstalar el paquete
pip uninstall cmd-helper

# Limpiar configuración (opcional)
rm -rf ~/.cmd-helper
rm -rf ~/.config/cmd-helper
```

## 🆘 Resolución de problemas

### Error: "Command not found"
- Asegúrate de que el directorio de pip esté en tu PATH
- Usa `pip show cmd-helper` para verificar la instalación

### Error: "API key not found"
- Verifica que tienes una clave API válida de Gemini
- Ejecuta `python3 setup_config.py` para reconfigurar

### Error: "Import error"
- Reinstala las dependencias: `pip install -r requirements.txt`
- Verifica tu versión de Python: `python3 --version`

## 📞 Soporte

- Issues: https://github.com/yourusername/cmd-helper/issues
- Documentación: README.md
- Email: your.email@example.com
