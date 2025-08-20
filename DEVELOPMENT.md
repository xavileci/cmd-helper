# Guía de Desarrollo - cmd-helper

## 🧪 Testing

### Configuración del Entorno de Testing

```bash
# Instalar dependencias de desarrollo
pip install -r requirements-dev.txt
```

### Ejecución de Tests

```bash
# Tests básicos
pytest tests/

# Tests con cobertura
pytest tests/ --cov=cmd_helper --cov-report=term

# Tests con reporte detallado
pytest tests/ --cov=cmd_helper --cov-report=html --cov-report=term-missing

# Tests para SonarQube (genera XML)
./run_tests_sonar.sh
```

### Estructura de Tests

```
tests/
├── test_command_handler.py    # Tests para manejo de comandos
├── test_config.py            # Tests para configuración
├── test_context_analyzer.py  # Tests para análisis de contexto
├── test_main.py              # Tests para función principal
├── test_mcp_server.py        # Tests para servidor MCP
└── pytest.ini               # Configuración de pytest
```

### Métricas Actuales

- **Total Tests**: 70
- **Cobertura Global**: 88%
- **Tests Pasando**: 100%

#### Cobertura por Módulo

| Módulo | Líneas | Miss | Cobertura |
|--------|--------|------|-----------|
| `__init__.py` | 8 | 0 | 100% |
| `config.py` | 16 | 0 | 100% |
| `mcp_server.py` | 96 | 5 | 95% |
| `command_handler.py` | 47 | 5 | 89% |
| `main.py` | 73 | 8 | 89% |
| `context_analyzer.py` | 49 | 9 | 82% |
| `i18n.py` | 65 | 15 | 77% |

## 🔍 SonarQube

### Configuración

El proyecto está configurado para análisis automático con SonarQube Cloud:

- **Archivo de configuración**: `sonar-project.properties`
- **Pipeline CI/CD**: `.github/workflows/sonar.yml`
- **Reportes generados**: `coverage.xml`, `test-results.xml`

### Análisis Local

```bash
# Generar reportes para SonarQube
./run_tests_sonar.sh

# Ejecutar análisis local (requiere sonar-scanner)
sonar-scanner
```

### Métricas de Calidad

- ✅ **Cobertura de Tests**: 88% (objetivo: >80%)
- ✅ **Tests Pasando**: 100% (objetivo: 100%)
- ✅ **Duplicación de Código**: <3%
- ✅ **Vulnerabilidades**: 0
- ✅ **Code Smells**: Minimizados

## 🔧 Desarrollo

### Workflow de Desarrollo

1. **Crear rama de feature**
   ```bash
   git checkout -b feature/nueva-funcionalidad
   ```

2. **Desarrollar con tests**
   ```bash
   # Escribir tests primero (TDD)
   # Implementar funcionalidad
   # Ejecutar tests
   pytest tests/
   ```

3. **Verificar calidad**
   ```bash
   # Ejecutar suite completa
   ./run_tests_sonar.sh
   
   # Verificar cobertura
   pytest --cov=cmd_helper --cov-fail-under=85
   ```

4. **Commit y push**
   ```bash
   git add .
   git commit -m "feat: nueva funcionalidad con tests"
   git push origin feature/nueva-funcionalidad
   ```

### Convenciones de Tests

#### Naming

- **Archivos**: `test_<module>.py`
- **Clases**: `Test<ClassName>`
- **Métodos**: `test_<functionality>_<scenario>`

#### Estructura

```python
class TestClassName:
    def setUp(self):
        """Setup común para todos los tests"""
        pass
    
    def test_method_success_case(self):
        """Test caso exitoso"""
        # Arrange
        # Act
        # Assert
        pass
    
    def test_method_error_handling(self):
        """Test manejo de errores"""
        pass
```

#### Mocking

```python
from unittest.mock import patch, MagicMock

@patch('module.external_dependency')
def test_with_mock(self, mock_dependency):
    mock_dependency.return_value = "expected_value"
    # Test implementation
```

### Debugging

#### Tests Específicos

```bash
# Ejecutar test específico
pytest tests/test_main.py::TestMain::test_specific_case -v

# Ejecutar con debugging
pytest tests/ -s --pdb

# Ver salida completa
pytest tests/ -v -s
```

#### Coverage Debug

```bash
# Ver líneas no cubiertas
pytest --cov=cmd_helper --cov-report=term-missing

# Generar reporte HTML
pytest --cov=cmd_helper --cov-report=html
open htmlcov/index.html
```

## 📊 CI/CD Pipeline

### GitHub Actions

El pipeline automático ejecuta:

1. **Setup Python 3.11**
2. **Install Dependencies**
3. **Run Tests with Coverage**
4. **Generate Reports** (XML format)
5. **SonarQube Analysis**
6. **Upload Artifacts**

### Archivos Clave

- `.github/workflows/sonar.yml` - Pipeline principal
- `sonar-project.properties` - Configuración SonarQube
- `requirements-dev.txt` - Dependencias de desarrollo
- `pytest.ini` - Configuración pytest

### Variables de Entorno

En GitHub Secrets:
- `SONAR_TOKEN` - Token de autenticación SonarQube
- `SONAR_HOST_URL` - URL del servidor SonarQube

## 🚨 Troubleshooting

### Tests Fallando

```bash
# Ver detalles de fallo
pytest tests/ -v --tb=short

# Re-ejecutar solo tests fallidos
pytest --lf

# Ejecutar con debug
pytest tests/ --pdb
```

### Problemas de Coverage

```bash
# Verificar archivos incluidos/excluidos
pytest --cov=cmd_helper --cov-report=term --cov-config=.coveragerc

# Forzar re-analysis
rm .coverage coverage.xml
pytest --cov=cmd_helper
```

### Problemas SonarQube

```bash
# Verificar reportes generados
ls -la coverage.xml test-results.xml

# Re-generar reportes
./run_tests_sonar.sh

# Verificar configuración
cat sonar-project.properties
```

## 📝 Contribuir Tests

### Agregar Nuevos Tests

1. **Identificar funcionalidad no cubierta**
   ```bash
   pytest --cov=cmd_helper --cov-report=html
   open htmlcov/index.html
   ```

2. **Crear test file**
   ```python
   # tests/test_new_module.py
   import unittest
   from cmd_helper.new_module import NewClass
   
   class TestNewClass(unittest.TestCase):
       def setUp(self):
           self.instance = NewClass()
       
       def test_new_functionality(self):
           # Implementation
           pass
   ```

3. **Ejecutar y verificar**
   ```bash
   pytest tests/test_new_module.py -v
   pytest --cov=cmd_helper --cov-report=term
   ```

### Best Practices

- ✅ **Un test, un concepto**
- ✅ **Nombres descriptivos**
- ✅ **Arrange-Act-Assert pattern**
- ✅ **Mock dependencies externas**
- ✅ **Test casos edge**
- ✅ **Test error handling**
- ✅ **Mantener tests simples y rápidos**

## 🎯 Objetivos de Calidad

- **Cobertura**: >85% (actual: 88% ✅)
- **Tests**: 100% pasando (actual: 100% ✅)
- **Performance**: Tests <5s total
- **Mantenibilidad**: Rating A en SonarQube
- **Reliability**: Rating A en SonarQube
- **Security**: Rating A en SonarQube
