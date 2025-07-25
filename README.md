# MAXEschine 🎸

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