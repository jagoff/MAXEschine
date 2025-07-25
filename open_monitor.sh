#!/bin/bash

# Script para abrir el monitor en una nueva ventana de terminal
# MAXEschine - Monitor en Tiempo Real

# Obtener el directorio del script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Activar el entorno virtual
source "$SCRIPT_DIR/venv/bin/activate"

# Cambiar al directorio del proyecto
cd "$SCRIPT_DIR"

# Ejecutar el monitor
python3 realtime_monitor_console.py 