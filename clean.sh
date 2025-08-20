#!/bin/bash
# Script para limpiar archivos temporales y de desarrollo
# Útil para hacer una limpieza completa del proyecto

set -e

echo "🧹 Limpiando archivos temporales y de desarrollo..."

# Confirmar con el usuario
read -p "¿Estás seguro de que quieres eliminar todos los archivos temporales? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Operación cancelada"
    exit 1
fi

echo "🗑️  Eliminando archivos de cobertura..."
rm -rf htmlcov/
rm -f .coverage
rm -f coverage.xml
rm -f test-results.xml

echo "🗑️  Eliminando cache de pytest..."
rm -rf .pytest_cache/
rm -rf tests/__pycache__/

echo "🗑️  Eliminando archivos compilados de Python..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete 2>/dev/null || true
find . -type f -name "*.pyo" -delete 2>/dev/null || true

echo "🗑️  Eliminando archivos de construcción..."
rm -rf build/
rm -rf dist/
rm -rf *.egg-info/

echo "🗑️  Eliminando archivos de SonarQube..."
rm -rf .sonar/
rm -rf .scannerwork/
rm -f sonar-report.json

echo "🗑️  Eliminando archivos temporales del sistema..."
find . -name ".DS_Store" -delete 2>/dev/null || true
find . -name "Thumbs.db" -delete 2>/dev/null || true
find . -name "*.tmp" -delete 2>/dev/null || true
find . -name "*.temp" -delete 2>/dev/null || true
find . -name "*~" -delete 2>/dev/null || true

echo "🗑️  Eliminando logs..."
find . -name "*.log" -delete 2>/dev/null || true

echo "✅ Limpieza completada"
echo ""
echo "📊 Archivos restantes en el directorio:"
echo "$(find . -type f | wc -l) archivos"
echo "$(du -sh . | cut -f1) tamaño total"

echo ""
echo "💡 Para volver a generar los reportes de cobertura:"
echo "   ./run_tests_sonar.sh"
