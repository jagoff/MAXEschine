# 🎸 MAXEschine - Monitor en Tiempo Real

## 📊 Funcionalidades Implementadas

### 🖥️ **Monitor de Consola en Tiempo Real**
- **Archivo:** `realtime_monitor_console.py`
- **Interfaz:** Consola con actualización en tiempo real
- **Compatibilidad:** Funciona en todos los sistemas (sin dependencias GUI)

### 🎯 **Características del Monitor**

#### 📨 **Log de Mensajes MIDI**
- Muestra todos los mensajes MIDI en tiempo real
- Timestamps precisos con milisegundos
- Buffer de 50 mensajes recientes
- Formato claro y legible

#### 🎵 **Estado de Pads (Escenas)**
- Visualización de Pads 1-4
- Indicadores 🟢/🔴 para estado activo
- Mapeo directo a escenas del Axe-Fx III

#### 🎚️ **Estado de Efectos**
- Visualización de Pads 5-16
- Estados ON/OFF para cada efecto
- Mapeo a CC# correspondientes
- Toggle automático de estados

#### 🎛️ **Controladores Externos**
- Controlador activo actual
- Botón lateral seleccionado
- Valor del potenciómetro
- Mapeo a External Controllers 1-8

#### 📊 **Estadísticas en Tiempo Real**
- Contador de mensajes MIDI
- Tiempo de ejecución
- Estado de conexión
- Información de dispositivos

### 🚀 **Integración con Menú de Barra**

#### 📱 **Acceso desde la Aplicación Principal**
- Opción "📊 Open Real-time Monitor" en el menú
- Ejecución en proceso separado
- No interfiere con la aplicación principal

#### 🔧 **Configuración Automática**
- Detección automática de dispositivos MIDI
- Conexión automática al Maschine Mikro
- Conexión automática al Axe-Fx III (si está disponible)
- Modo simulación si Axe-Fx no está conectado

### 🎹 **Mapeo MIDI Completo**

#### 🎵 **Pads 1-4 (Escenas)**
| Pad | Nota MIDI | CC | Función |
|-----|-----------|----|---------|
| Pad 1 | 36 | 35 | Escena 1 |
| Pad 2 | 37 | 35 | Escena 2 |
| Pad 3 | 38 | 35 | Escena 3 |
| Pad 4 | 39 | 35 | Escena 4 |

#### 🎚️ **Pads 5-16 (Efectos)**
| Pad | Nota MIDI | CC | Efecto |
|-----|-----------|----|--------|
| Pad 5 | 24 | 18 | GEQ1 |
| Pad 6 | 25 | 19 | REVERB1 |
| Pad 7 | 26 | 20 | DELAY1 |
| Pad 8 | 27 | 21 | COMP1 |
| Pad 9 | 28 | 22 | AMP1 |
| Pad 10 | 29 | 23 | AMP2 |
| Pad 11 | 30 | 24 | DRIVE1 |
| Pad 12 | 31 | 25 | DRIVE2 |
| Pad 13 | 32 | 26 | CAB1 |
| Pad 14 | 33 | 27 | CAB2 |
| Pad 15 | 34 | 28 | GATE1 |
| Pad 16 | 35 | 29 | PITCH1 |

#### 🎛️ **Botones Laterales**
| Botón | CC | External Controller |
|-------|----|-------------------|
| Botón 1 | 112 | External Controller 1 |
| Botón 2 | 113 | External Controller 2 |
| Botón 3 | 114 | External Controller 3 |
| Botón 4 | 115 | External Controller 4 |
| Botón 5 | 116 | External Controller 5 |
| Botón 6 | 117 | External Controller 6 |
| Botón 7 | 118 | External Controller 7 |
| Botón 8 | 119 | External Controller 8 |

#### 🎚️ **Potenciómetro**
- **CC#22** → Controla el External Controller activo
- **Rango:** 0-127
- **Actualización:** En tiempo real

### 🛠️ **Uso del Monitor**

#### 🚀 **Iniciar desde Menú de Barra**
1. Haz clic en el ícono 🎸 en la barra de menú
2. Selecciona "📊 Open Real-time Monitor"
3. Se abrirá una ventana de terminal con el monitor

#### 🎸 **Ejecutar Independientemente**
```bash
./venv/bin/python realtime_monitor_console.py
```

#### 🎹 **Probar Funcionalidad**
```bash
./venv/bin/python test_monitor_simple.py
```

### 📋 **Comandos del Monitor**

#### 💡 **Comandos Disponibles**
- **Ctrl+C**: Salir del monitor
- **Actualización automática**: Cada 100ms
- **Buffer de mensajes**: Últimos 50 mensajes
- **Pantalla completa**: Limpieza automática

#### 📊 **Información Mostrada**
- **Encabezado**: Título, tiempo, estadísticas
- **Paneles de estado**: Pads, efectos, controladores
- **Mensajes recientes**: Log de actividad MIDI
- **Ayuda**: Comandos disponibles

### 🔧 **Configuración Técnica**

#### 📦 **Dependencias**
- `mido`: Biblioteca MIDI
- `python-rtmidi`: Soporte MIDI avanzado
- **Sin dependencias GUI**: Compatible con todos los sistemas

#### ⚙️ **Configuración**
- **Archivo de configuración**: `config.py`
- **Mapeo de CC**: `cc_pad_mapping.json`
- **Detección automática**: Puertos MIDI

#### 🔄 **Procesamiento en Tiempo Real**
- **Callback MIDI**: Procesamiento inmediato
- **Buffer de mensajes**: Gestión eficiente
- **Actualización de UI**: 10 FPS (100ms)
- **Manejo de señales**: Cierre limpio

### 🎯 **Beneficios del Monitor**

#### 👁️ **Visibilidad Completa**
- Ve exactamente qué está enviando el Maschine Mikro
- Monitorea la comunicación con el Axe-Fx III
- Identifica problemas de configuración

#### 🎛️ **Control Total**
- Verifica que los mapeos funcionen correctamente
- Prueba cada pad y control individualmente
- Valida la configuración del Axe-Fx III

#### 🔧 **Depuración**
- Identifica mensajes MIDI no mapeados
- Detecta problemas de conexión
- Valida la configuración de CC#

#### 📊 **Análisis**
- Estadísticas de uso
- Patrones de actividad
- Rendimiento del sistema

### 🎸 **Integración Perfecta**

El monitor en tiempo real se integra perfectamente con MAXEschine:

- ✅ **No interfiere** con la aplicación principal
- ✅ **Proceso separado** para máxima estabilidad
- ✅ **Detección automática** de dispositivos
- ✅ **Configuración compartida** con la app principal
- ✅ **Interfaz consistente** con el resto del sistema

---

**🎸 MAXEschine ahora incluye un monitor en tiempo real completo y funcional que te permite ver exactamente qué está pasando con tu Maschine Mikro y Axe-Fx III!** 