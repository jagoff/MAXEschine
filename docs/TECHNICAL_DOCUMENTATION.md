# Documentación Técnica - Maschine Mikro MK1 LED Control

## 🎸 MAXEschine - Control de Luces Físicas

### Resumen Ejecutivo

Este documento describe la implementación técnica del control de luces físicas del Maschine Mikro MK1 para la aplicación MAXEschine. Se incluyen especificaciones de hardware, protocolos MIDI, limitaciones conocidas y soluciones implementadas.

---

## 📋 Especificaciones del Hardware

### Maschine Mikro MK1
- **Fabricante**: Native Instruments
- **Modelo**: Maschine Mikro (Primera generación)
- **Año de lanzamiento**: 2011
- **Tipo de LEDs**: Monocromáticos (blancos/verdes)
- **Intensidad**: Variable (0-127)
- **Cantidad de LEDs laterales**: 8
- **Cantidad de LEDs de pads**: 16

### Características Técnicas
- **Protocolo de comunicación**: MIDI estándar
- **Puerto MIDI**: USB
- **Vendor ID**: 0x17cc
- **Product ID**: 0x1110
- **Buffer HID**: 41 bytes (confirmado)

---

## 💡 Control de Luces Laterales

### ✅ FUNCIONA - Luces Laterales (Botones 1-8)

#### Especificaciones Técnicas
- **CC# utilizados**: 112-119
- **Valores de control**:
  - `0`: Luz apagada
  - `64`: Luz prendida (intensidad media)
  - `127`: Luz prendida (intensidad máxima)
- **Canal MIDI**: 0
- **Comportamiento**: Radiobutton (solo una luz prendida a la vez)

#### Implementación Funcional
```python
# Mapeo de botones laterales a CC#
LATERAL_BUTTONS = {
    112: 1,  # Botón 1 → External Controller 1
    113: 2,  # Botón 2 → External Controller 2
    114: 3,  # Botón 3 → External Controller 3
    115: 4,  # Botón 4 → External Controller 4
    116: 5,  # Botón 5 → External Controller 5
    117: 6,  # Botón 6 → External Controller 6
    118: 7,  # Botón 7 → External Controller 7
    119: 8   # Botón 8 → External Controller 8
}

# Mapeo de luces a CC#
LIGHT_CC_MAP = {
    0: 112,  # Luz 1 → CC#112
    1: 113,  # Luz 2 → CC#113
    2: 114,  # Luz 3 → CC#114
    3: 115,  # Luz 4 → CC#115
    4: 116,  # Luz 5 → CC#116
    5: 117,  # Luz 6 → CC#117
    6: 118,  # Luz 7 → CC#118
    7: 119   # Luz 8 → CC#119
}
```

#### Protocolo de Control
```python
def control_lateral_lights(active_button):
    """Controla las luces laterales en modo radiobutton"""
    # 1. Apagar todas las luces
    for light_num in range(8):
        cc = 112 + light_num
        outport.send(mido.Message('control_change', control=cc, value=0, channel=0))
        time.sleep(0.01)
    
    # 2. Prender solo la luz activa
    if active_button in BUTTON_TO_LIGHT:
        light_num = BUTTON_TO_LIGHT[active_button]
        cc = 112 + light_num
        outport.send(mido.Message('control_change', control=cc, value=64, channel=0))
```

#### Estado Actual
- ✅ **FUNCIONA**: Control completo de luces laterales
- ✅ **Radiobutton**: Solo una luz prendida a la vez
- ✅ **Feedback visual**: Luces reflejan el estado del software
- ✅ **Integración**: Completamente integrado en MAXEschine

---

## 🎵 Control de Luces de Pads

### ❌ NO FUNCIONA - Luces de Pads (Pads 1-16)

#### El Gran Desafío

**Problema Principal**: Las luces de los pads del Maschine Mikro MK1 **NO responden** a comandos MIDI estándar.

#### Especificaciones Técnicas
- **Cantidad de pads**: 16
- **Notas MIDI**: 36-51 (pads 1-16)
- **Comportamiento nativo**: Se prenden automáticamente al tocar físicamente
- **Control programático**: **NO DISPONIBLE**

#### Métodos Probados (Todos Fallidos)

##### 1. MIDI Note On/Off
```python
# Método 1: Note On/Off
outport.send(mido.Message('note_on', note=36, velocity=127, channel=0))  # Pad 1
outport.send(mido.Message('note_off', note=36, velocity=0, channel=0))
```
**Resultado**: ❌ No responde

##### 2. MIDI Control Change
```python
# Método 2: Control Change
for cc in range(0, 128):
    outport.send(mido.Message('control_change', control=cc, value=127, channel=0))
```
**Resultado**: ❌ No responde

##### 3. SysEx Native Instruments
```python
# Método 3: SysEx NI
sysex_data = [0xF0, 0x47, 0x7F, 0x43, 0x65, 0x00, 0x01, 0x01, 0x00, light_value, 0xF7]
outport.send(mido.Message('sysex', data=sysex_data))
```
**Resultado**: ❌ No responde

##### 4. HID Directo
```python
# Método 4: HID Directo
import hid
device = hid.device(0x17cc, 0x1110)
device.write([0x00] * 41)  # Buffer de 41 bytes
```
**Resultado**: ❌ No responde en macOS

##### 5. SysEx Alternativo
```python
# Método 5: SysEx Alternativo
sysex_data = [0xF0, 0x00, 0x20, 0x29, 0x02, 0x0A, 0x00, led_data, 0xF7]
outport.send(mido.Message('sysex', data=sysex_data))
```
**Resultado**: ❌ No responde

#### Análisis del Problema

##### Limitaciones del Hardware
1. **Firmware propietario**: El MK1 usa firmware cerrado de Native Instruments
2. **Protocolo interno**: Las luces de pads usan un protocolo interno no documentado
3. **Drivers específicos**: Requiere drivers de NI que no están disponibles en Python/macOS
4. **Seguridad**: El dispositivo puede tener protecciones contra control externo

##### Limitaciones del Software
1. **macOS**: Restricciones de acceso a HID
2. **Python**: Falta de librerías específicas para NI
3. **MIDI estándar**: El protocolo no incluye control de luces de pads
4. **SysEx**: Los mensajes SysEx específicos no están documentados públicamente

#### Investigación Realizada

##### Recursos Consultados
- [GitHub: LaunchPad-for-Maschine](https://github.com/borisdivjak/LaunchPad-for-Maschine)
- [GitHub: maschine.rs](https://github.com/wrl/maschine.rs)
- [Gist: Maschine LED Control](https://gist.github.com/zewelor/5c0c159cf71200059ffbae7556dced8a)
- [NI Community: NIPatcher](https://community.native-instruments.com/discussion/11786/nipatcher-tool-to-modify-maschine-macos)
- [GitHub: NIPatcher](https://github.com/d1One/NIPatcher)

##### Conclusiones de la Investigación
1. **No hay solución pública**: No existe documentación oficial o no oficial que funcione
2. **Limitaciones confirmadas**: Todos los intentos de control de luces de pads fallan
3. **Alternativas**: Solo las luces laterales son controlables
4. **Workaround**: Usar feedback visual en software en lugar de luces físicas

---

## 🔧 Implementación en MAXEschine

### Arquitectura del Sistema

#### Componentes Principales
1. **Monitor en Tiempo Real** (`realtime_monitor_console.py`)
2. **Control de Luces Laterales** (funcional)
3. **Feedback Visual de Pads** (simulado en software)
4. **Integración con Axe-Fx III**

#### Flujo de Control
```
Usuario presiona botón lateral
    ↓
Monitor detecta CC#112-119
    ↓
Actualiza estado interno
    ↓
Controla luz física lateral (CC#112-119)
    ↓
Envía CC# al Axe-Fx III
    ↓
Feedback visual en monitor
```

### Configuración MIDI

#### Puertos Utilizados
- **Entrada**: `Maschine Mikro Input`
- **Salida Axe-Fx**: `Axe-Fx III`
- **Salida Maschine**: `Maschine Mikro Output`

#### Mapeo de CC#
```python
# Botones laterales → External Controllers
112: External Controller 1 (CC#16)
113: External Controller 2 (CC#17)
114: External Controller 3 (CC#18)
115: External Controller 4 (CC#19)
116: External Controller 5 (CC#20)
117: External Controller 6 (CC#21)
118: External Controller 7 (CC#22)
119: External Controller 8 (CC#23)

# Luces laterales (mismo CC# que botones)
112: Luz lateral 1
113: Luz lateral 2
114: Luz lateral 3
115: Luz lateral 4
116: Luz lateral 5
117: Luz lateral 6
118: Luz lateral 7
119: Luz lateral 8
```

---

## 🚫 Limitaciones Conocidas

### Limitaciones de Hardware
1. **Luces de pads no controlables**: Limitación fundamental del MK1
2. **Firmware cerrado**: No hay acceso al protocolo interno
3. **Drivers específicos**: Requiere software propietario de NI

### Limitaciones de Software
1. **macOS**: Restricciones de acceso a HID
2. **Python**: Falta de librerías específicas
3. **MIDI estándar**: No incluye control de luces de pads

### Limitaciones de Protocolo
1. **SysEx no documentado**: Los mensajes específicos no están disponibles
2. **HID restringido**: Acceso limitado en macOS
3. **Propietario**: Protocolo interno de NI no accesible

---

## ✅ Soluciones Implementadas

### 1. Control de Luces Laterales
- ✅ **Completamente funcional**
- ✅ **Modo radiobutton**
- ✅ **Integración completa**

### 2. Feedback Visual de Pads
- ✅ **Simulación en software**
- ✅ **Estado visual en monitor**
- ✅ **Indicadores de estado**

### 3. Integración con Axe-Fx III
- ✅ **Control de External Controllers**
- ✅ **Cambio de escenas**
- ✅ **Bypass de efectos**

---

## 🔮 Posibles Soluciones Futuras

### Opciones Técnicas
1. **Reverse Engineering**: Análisis profundo del firmware
2. **Drivers personalizados**: Desarrollo de drivers específicos
3. **Hardware modificado**: Modificaciones físicas del dispositivo
4. **Alternativas de hardware**: Uso de otros controladores

### Opciones de Software
1. **Librerías nativas**: Desarrollo de librerías específicas
2. **Kernel extensions**: Acceso directo al hardware
3. **Virtualización**: Emulación del protocolo NI
4. **Alternativas de protocolo**: Uso de otros protocolos de comunicación

### Recomendaciones
1. **Aceptar limitaciones**: Las luces de pads no son controlables
2. **Enfocarse en luces laterales**: Funcionan perfectamente
3. **Mejorar feedback visual**: Compensar con indicadores en software
4. **Considerar hardware alternativo**: Para control completo de luces

---

## 📊 Estado Actual del Proyecto

### ✅ Funcionalidades Completas
- Control de luces laterales (radiobutton)
- Integración con Axe-Fx III
- Monitor en tiempo real
- Feedback visual en software
- Aplicación menubar funcional

### ❌ Limitaciones Aceptadas
- Luces de pads no controlables
- Dependencia de firmware propietario
- Restricciones de macOS

### 🎯 Objetivos Cumplidos
- Control MIDI completo
- Integración con Axe-Fx III
- Feedback visual funcional
- Aplicación estable y confiable

---

## 📝 Conclusión

El control de luces del Maschine Mikro MK1 presenta limitaciones fundamentales debido al hardware propietario y firmware cerrado de Native Instruments. Sin embargo, se ha logrado implementar un sistema funcional que:

1. **Controla completamente las luces laterales** en modo radiobutton
2. **Proporciona feedback visual completo** en el software
3. **Integra perfectamente con el Axe-Fx III**
4. **Ofrece una experiencia de usuario satisfactoria**

Las limitaciones de las luces de pads son una restricción del hardware que no puede ser superada con las herramientas actuales, pero no afectan la funcionalidad principal de la aplicación MAXEschine.

---

*Documento técnico generado el: $(date)*
*Versión: 1.0*
*Estado: Finalizado* 