# MAXEschine 🎸

**Full control of Maschine Mikro + Axe-Fx III**

MAXEschine is a macOS menu bar app that lets you fully control your Axe-Fx III using a Maschine Mikro as a MIDI controller.

## 🧠 How it works

<p align="center">
  <img src="docs/architecture.svg" alt="MAXEschine signal flow: Maschine Mikro to Axe-Fx III" width="900">
</p>

The Maschine Mikro sends MIDI (pad notes and CCs) over USB. The engine `realtime_monitor_console.py` (built on `mido`) reads those messages and routes them:

- **Pads 1-4 → CC 35** select Axe-Fx **scenes**.
- **Pads 5-16 → CC 18-29** toggle **effect bypass** (12 blocks).
- **Side buttons → CC 16-23** pick the active **External Controller** (radio-button behavior).
- **Knob (CC 22) → CC 16-23** sends a value to the active External Controller.

It then sends those Control Change messages to the **Axe-Fx III**, and lights the Maschine's side LEDs back as feedback (**CC 112-119**). `menubar_app_advanced.py` (rumps) detects the devices, launches the engine, and shows status in the menu bar; `config.py` holds all pad/note/CC mappings.

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

## 🧠 Cómo funciona

<p align="center">
  <img src="docs/architecture.svg" alt="Flujo de señal de MAXEschine: Maschine Mikro hacia Axe-Fx III" width="900">
</p>

El Maschine Mikro envía MIDI (notas de pads y CCs) por USB. El motor `realtime_monitor_console.py` (basado en `mido`) lee esos mensajes y los rutea:

- **Pads 1-4 → CC 35** seleccionan **escenas** del Axe-Fx.
- **Pads 5-16 → CC 18-29** activan/desactivan el **bypass de efectos** (12 bloques).
- **Botones laterales → CC 16-23** eligen el **External Controller** activo (comportamiento radiobutton).
- **Potenciómetro (CC 22) → CC 16-23** envía un valor al External Controller activo.

Luego envía esos mensajes Control Change al **Axe-Fx III**, y prende las luces laterales del Maschine como feedback (**CC 112-119**). `menubar_app_advanced.py` (rumps) detecta los dispositivos, lanza el motor y muestra el estado en la barra de menú; `config.py` contiene todos los mapeos pad/nota/CC.

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
