#!/bin/bash

# MAXEschine Startup Script
# Control completo de Maschine Mikro + Axe-Fx III

echo "🎸 MAXEschine - Iniciando..."
echo "=================================="

# Activar entorno virtual
source venv/bin/activate

# Verificar que el entorno virtual esté activado
if [ $? -eq 0 ]; then
    echo "✅ Entorno virtual activado"
else
    echo "❌ Error activando entorno virtual"
    exit 1
fi

# Verificar dependencias
echo "📦 Verificando dependencias..."
pip list | grep -E "(mido|rumps|rtmidi)" || {
    echo "❌ Faltan dependencias. Instalando..."
    pip install -r requirements.txt
}

# Iniciar aplicación
echo "🚀 Iniciando MAXEschine..."
python3 menubar_app_advanced.py 