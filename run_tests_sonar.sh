#!/bin/bash
# Script para ejecutar tests y generar reportes de cobertura para SonarQube
# Este script replica lo que hace el pipeline de CI/CD

set -e  # Exit on any error

echo "🧪 Ejecutando tests con reporte de cobertura para SonarQube..."

# Instalar dependencias si no están instaladas
echo "📦 Verificando dependencias..."
python -m pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt > /dev/null 2>&1
pip install -r requirements-dev.txt > /dev/null 2>&1

# Limpiar reportes anteriores
echo "🧹 Limpiando reportes anteriores..."
rm -f coverage.xml test-results.xml .coverage

# Ejecutar tests con cobertura
echo "🚀 Ejecutando tests..."
python -m pytest tests/ \
    --cov=cmd_helper \
    --cov-report=xml:coverage.xml \
    --cov-report=term \
    --cov-report=html:htmlcov \
    --junitxml=test-results.xml \
    -v

# Mostrar resumen
echo ""
echo "📊 Resumen de cobertura:"
python -m coverage report

echo ""
echo "✅ Reportes generados:"
echo "   - coverage.xml (para SonarQube)"
echo "   - test-results.xml (para SonarQube)"
echo "   - htmlcov/ (reporte HTML local)"

echo ""
echo "🔍 Para subir a SonarQube manualmente:"
echo "   sonar-scanner"

echo ""
echo "📂 Para ver el reporte HTML:"
echo "   open htmlcov/index.html"
