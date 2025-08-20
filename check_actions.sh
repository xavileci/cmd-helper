#!/bin/bash
# Script para verificar las versiones de GitHub Actions en los workflows

echo "🔍 Verificando versiones de GitHub Actions..."
echo "=============================================="

echo ""
echo "📄 Workflows encontrados:"
find .github/workflows -name "*.yml" -o -name "*.yaml" | sed 's/^/   - /'

echo ""
echo "🔧 Actions utilizadas:"
grep -h "uses:" .github/workflows/*.yml | sort | uniq | sed 's/^/   - /'

echo ""
echo "⚠️  Verificando versiones potencialmente deprecadas:"

# Buscar versiones v3 que podrían estar deprecadas
if grep -r "@v3" .github/workflows/ 2>/dev/null; then
    echo "   ❌ Encontradas versiones v3 (posiblemente deprecadas)"
else
    echo "   ✅ No se encontraron versiones v3 deprecadas"
fi

# Buscar versiones v2 que están definitivamente deprecadas
if grep -r "@v2" .github/workflows/ 2>/dev/null; then
    echo "   ❌ Encontradas versiones v2 (deprecadas)"
else
    echo "   ✅ No se encontraron versiones v2 deprecadas"
fi

# Buscar versiones v1 que están obsoletas
if grep -r "@v1" .github/workflows/ 2>/dev/null; then
    echo "   ❌ Encontradas versiones v1 (obsoletas)"
else
    echo "   ✅ No se encontraron versiones v1 obsoletas"
fi

echo ""
echo "✅ Estado de las actions principales:"

# Verificar actions específicas
actions=(
    "actions/checkout@v4"
    "actions/setup-python@v5"
    "actions/cache@v4"
    "actions/upload-artifact@v4"
    "SonarSource/sonarqube-scan-action@v6"
)

for action in "${actions[@]}"; do
    if grep -q "$action" .github/workflows/*.yml; then
        echo "   ✅ $action - Encontrada"
    else
        echo "   ❓ $action - No encontrada (puede estar bien)"
    fi
done

echo ""
echo "🎯 Resumen:"
total_workflows=$(find .github/workflows -name "*.yml" -o -name "*.yaml" | wc -l)
echo "   - Total workflows: $total_workflows"
echo "   - Verificación completada"

echo ""
echo "🚀 Para probar los workflows localmente:"
echo "   act -l  # Listar workflows"
echo "   act     # Ejecutar workflows con act"
