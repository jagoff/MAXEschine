#!/bin/bash
# MAXEschine - Instalador y lanzador automático para macOS
set -e

echo "🎸 MAXEschine - Instalador automático"
echo "======================================"

# 1. Crear entorno virtual si no existe
if [ ! -d "venv" ]; then
  echo "[INFO] Creando entorno virtual Python..."
  python3 -m venv venv
fi

# 2. Activar entorno virtual
echo "[INFO] Activando entorno virtual..."
source venv/bin/activate

# 3. Instalar Homebrew si no está
if ! command -v brew &> /dev/null; then
  echo "[INFO] Instalando Homebrew..."
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

# 4. Instalar librerías nativas requeridas
echo "[INFO] Instalando dependencias del sistema..."
brew install --quiet python-tk hidapi

# 5. Instalar dependencias Python
echo "[INFO] Instalando dependencias Python..."
pip install --upgrade pip
pip install -r requirements.txt

# 6. Ejecutar la app principal
echo "[INFO] Iniciando MAXEschine..."
echo "✅ Instalación completada. MAXEschine se está iniciando..."
python3 menubar_app_advanced.py 