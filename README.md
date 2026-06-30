# MAXEschine 🎸

**Full control of Maschine Mikro + Axe-Fx III**

MAXEschine is a macOS menu bar app that lets you fully control your Axe-Fx III using a Maschine Mikro as a MIDI controller.

## ✨ Features

- 🎛️ **Scene Control**: Pads 1-4 switch between Axe-Fx scenes
- 🎚️ **Effect Control**: Pads 5-16 toggle effects on/off
- 🎛️ **Knob**: Controls external Axe-Fx parameters
- 🎯 **Side Buttons**: Select which parameter to control
- 📱 **Clean Interface**: Menu bar with status indicators
- 🔒 **Single Instance**: Only one instance can run at a time
- 🎨 **Visual Indicators**: Custom icon that changes with state
- 📊 **Real-time Monitor**: GUI window to monitor MIDI activity

## 🚀 Quick Install

### Requirements
- macOS
- Python 3.7+
- Maschine Mikro
- Axe-Fx III

### Automatic Install

1. **Clone the repository:**
```bash
git clone https://github.com/jagoff/MAXEschine.git
cd MAXEschine
```

2. **Run the automatic installer:**
```bash
chmod +x start.sh
./start.sh
```

That's it! MAXEschine installs automatically and starts.

### Manual Install

If you prefer to install manually:

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run
python3 menubar_app_advanced.py
```

## 🎛️ Axe-Fx III Configuration

See the full documentation in [docs/README.md](docs/README.md) for detailed Axe-Fx III setup.

## 📊 Real-time Monitor

To open the real-time monitor:
1. Click the MAXEschine icon in the menu bar
2. Select "Open Real-time Monitor"

Or run it directly:
```bash
source venv/bin/activate
python3 realtime_monitor_console.py
```

## 🎸 Your Maschine Mikro will be fully functional with the Axe-Fx III!

---

**Built with ❤️ for the guitar community**

---
---

# MAXEschine 🎸 (Español)

**Control completo de Maschine Mikro + Axe-Fx III**

MAXEschine es una aplicación de menú de barra para macOS que permite controlar completamente tu Axe-Fx III usando un Maschine Mikro como controlador MIDI.

## ✨ Características

- 🎛️ **Control de Escenas**: Pads 1-4 cambian entre escenas del Axe-Fx
- 🎚️ **Control de Efectos**: Pads 5-16 activan/desactivan efectos
- 🎛️ **Potenciómetro**: Controla parámetros externos del Axe-Fx
- 🎯 **Botones Laterales**: Seleccionan qué parámetro controlar
- 📱 **Interfaz Limpia**: Menú de barra con indicadores de estado
- 🔒 **Instancia Única**: Solo una instancia puede ejecutarse
- 🎨 **Indicadores Visuales**: Icono personalizado que cambia según el estado
- 📊 **Monitor en Tiempo Real**: Ventana GUI para monitorear actividad MIDI

## 🚀 Instalación Rápida

### Requisitos
- macOS
- Python 3.7+
- Maschine Mikro
- Axe-Fx III

### Instalación Automática

1. **Clonar el repositorio:**
```bash
git clone https://github.com/jagoff/MAXEschine.git
cd MAXEschine
```

2. **Ejecutar el instalador automático:**
```bash
chmod +x start.sh
./start.sh
```

¡Eso es todo! MAXEschine se instalará automáticamente y se iniciará.

### Instalación Manual

Si prefieres instalar manualmente:

```bash
# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar
python3 menubar_app_advanced.py
```

## 🎛️ Configuración del Axe-Fx III

Consulta la documentación completa en [docs/README.md](docs/README.md) para la configuración detallada del Axe-Fx III.

## 📊 Monitor en Tiempo Real

Para abrir el monitor en tiempo real:
1. Haz clic en el icono de MAXEschine en la barra de menú
2. Selecciona "Open Real-time Monitor"

O ejecuta directamente:
```bash
source venv/bin/activate
python3 realtime_monitor_console.py
```

## 🎸 ¡Tu Maschine Mikro estará completamente funcional con el Axe-Fx III!

---

**Desarrollado con ❤️ para la comunidad de guitarristas**
