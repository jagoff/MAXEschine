# Guía de Uso

Esta guía te explica cómo usar Maschine Axe-Fx Control una vez que está instalado y configurado.

## 🚀 Inicio Rápido

### Ejecutar el Sistema

```bash
# Activar entorno virtual (si no está activado)
source venv/bin/activate

# Ejecutar el script principal
python3 run_maschine_control.py
```

### Primera Ejecución

En la primera ejecución, el script te preguntará:

```
¿Quieres verificar la configuración del Axe-Fx III? (s/n): s
```

**Responde `s`** para que configure automáticamente tu Axe-Fx III.

## 🎛️ Controles del Maschine Mikro

### Pads 1-4: Control de Escenas

| Pad | Función | CC# | Descripción |
|-----|---------|-----|-------------|
| 1 | Escena 1 | 35 | Cambia a escena 1 |
| 2 | Escena 2 | 35 | Cambia a escena 2 |
| 3 | Escena 3 | 35 | Cambia a escena 3 |
| 4 | Escena 4 | 35 | Cambia a escena 4 |

**Cómo usar**:
- Presiona cualquier pad 1-4
- El Axe-Fx III cambiará a la escena correspondiente
- Verás en consola: `PAD 01 - CC #35 (SCENE 1)`

### Pads 5-16: Bypass de Efectos

| Pad | Efecto | CC# | Función |
|-----|--------|-----|---------|
| 5 | GEQ1 | 18 | Activa/desactiva Graphic EQ 1 |
| 6 | REVERB1 | 19 | Activa/desactiva Reverb 1 |
| 7 | DELAY1 | 20 | Activa/desactiva Delay 1 |
| 8 | COMP1 | 21 | Activa/desactiva Compressor 1 |
| 9 | AMP1 | 22 | Activa/desactiva Amp 1 |
| 10 | AMP2 | 23 | Activa/desactiva Amp 2 |
| 11 | DRIVE1 | 24 | Activa/desactiva Drive 1 |
| 12 | DRIVE2 | 25 | Activa/desactiva Drive 2 |
| 13 | CAB1 | 26 | Activa/desactiva Cab 1 |
| 14 | CAB2 | 27 | Activa/desactiva Cab 2 |
| 15 | GATE1 | 28 | Activa/desactiva Gate 1 |
| 16 | PITCH1 | 29 | Activa/desactiva Pitch 1 |

**Cómo usar**:
- Presiona cualquier pad 5-16
- El efecto se activará/desactivará (toggle)
- Verás en consola: `PAD 05 - CC #18 (GEQ1 ON)` o `PAD 05 - CC #18 (GEQ1 OFF)`

### Potenciómetro: Control de Parámetros

**Funcionalidad**:
- Controla el External Controller activo
- El External Controller activo se selecciona con los botones laterales
- Rango: 0-127 (0 = mínimo, 127 = máximo)

**Cómo usar**:
1. Presiona un botón lateral para seleccionar qué parámetro controlar
2. Gira el potenciómetro para ajustar el valor
3. Verás en consola: `POTENCIÓMETRO - CC #16 (External Controller 1: 64)`

### Botones Laterales: Selección de Controladores

| Botón | CC# | External Controller | Función |
|-------|-----|-------------------|---------|
| 1 | 112 | External Controller 1 | Selecciona EC1 para control |
| 2 | 113 | External Controller 2 | Selecciona EC2 para control |
| 3 | 114 | External Controller 3 | Selecciona EC3 para control |
| 4 | 115 | External Controller 4 | Selecciona EC4 para control |
| 5 | 116 | External Controller 5 | Selecciona EC5 para control |
| 6 | 117 | External Controller 6 | Selecciona EC6 para control |
| 7 | 118 | External Controller 7 | Selecciona EC7 para control |
| 8 | 119 | External Controller 8 | Selecciona EC8 para control |

**Cómo usar**:
- Presiona cualquier botón lateral
- Solo un botón puede estar activo a la vez (modo radio button)
- La luz del botón activo se encenderá
- El potenciómetro controlará el External Controller seleccionado

## 💡 Sistema de Luces

### Luces de Pads
- **Automáticas**: Se encienden/apagan al presionar los pads
- **No controlables**: No se pueden controlar programáticamente
- **Feedback visual**: Indican cuando presionas un pad

### Luces Laterales
- **Indicadores de estado**: Muestran qué botón lateral está activo
- **Modo radio button**: Solo una luz encendida a la vez
- **Feedback visual**: Indican qué External Controller está seleccionado

## 🎵 Casos de Uso Típicos

### Configuración Básica de Guitarra

1. **Selecciona escena**: Presiona Pad 1 para escena 1
2. **Activa efectos básicos**:
   - Pad 5: GEQ1 (ajuste de tono)
   - Pad 8: COMP1 (compresión)
   - Pad 9: AMP1 (amplificador)
   - Pad 13: CAB1 (cabina)
3. **Ajusta parámetros**:
   - Presiona botón lateral 1 (External Controller 1)
   - Gira potenciómetro para ajustar gain del amp

### Configuración con Efectos

1. **Selecciona escena**: Presiona Pad 2 para escena 2
2. **Activa efectos**:
   - Pad 6: REVERB1 (reverberación)
   - Pad 7: DELAY1 (delay)
   - Pad 11: DRIVE1 (overdrive)
3. **Ajusta parámetros**:
   - Presiona botón lateral 2 (External Controller 2)
   - Gira potenciómetro para ajustar mix de reverb

### Control en Tiempo Real

1. **Durante una canción**:
   - Presiona Pad 3 para cambiar a escena 3
   - Presiona Pad 10 para activar AMP2
   - Presiona botón lateral 3 y gira potenciómetro para ajustar drive

## 📊 Lectura de la Consola

### Salida Típica

```
🎸 MASCHINE MIKRO + AXE-FX III CONTROL
============================================================
✅ Configuración automática completada
PRESIONA LOS PADS 1-4, GIRA EL POTENCIÓMETRO O PRESIONA LOS BOTONES SUPERIORES...

PAD 01 - CC #35 (SCENE 1)
PAD 05 - CC #18 (GEQ1 ON)
PAD 06 - CC #19 (REVERB1 OFF)
POTENCIÓMETRO - CC #16 (External Controller 1: 64)
```

### Interpretación

- **PAD XX**: Indica qué pad físico fue presionado
- **CC #XX**: Número de Control Change enviado
- **Efecto ON/OFF**: Estado del efecto (activado/desactivado)
- **External Controller X: Y**: Valor del controlador (0-127)

## 🔧 Configuración Avanzada

### Personalizar Mapeo

Para cambiar el mapeo de pads a efectos:

1. **Edita** `maschine_to_axefx.py`
2. **Modifica** el diccionario `PAD_TO_EFFECT`
3. **Actualiza** `EFFECT_CC_MAPPING` si cambias CC#
4. **Reinicia** el script

### Agregar Nuevos Efectos

1. **Agrega** el efecto al mapeo:
   ```python
   'NUEVO_EFECTO': 30,  # Nuevo CC#
   ```

2. **Configura** el CC# en tu Axe-Fx III
3. **Asigna** el efecto a un pad disponible

### Cambiar CC# de Escenas

1. **Edita** `maschine_to_axefx.py`
2. **Modifica** `SCENE_CC = 35` a tu CC# preferido
3. **Configura** Scene Select en Axe-Fx III con el nuevo CC#

## 🛑 Detener el Sistema

### Método Normal
- Presiona `Ctrl+C` en la terminal
- El script se detendrá limpiamente

### Método Forzado
```bash
# En otra terminal
pkill -f "python.*maschine"
```

## 🔍 Diagnóstico

### Verificar Conexiones

```bash
# Ver puertos MIDI disponibles
python3 -c "import mido; print('Inputs:', mido.get_input_names()); print('Outputs:', mido.get_output_names())"
```

### Verificar Configuración

```bash
# Ejecutar configuración simple
python3 simple_axefx_config.py
```

### Logs Detallados

El script muestra información detallada en consola:
- Estado de conexiones
- Configuración automática
- Comandos MIDI enviados
- Errores y advertencias

## 📞 Soporte

Si tienes problemas:

1. **Revisa** los logs en consola
2. **Verifica** conexiones de hardware
3. **Consulta** la guía de instalación
4. **Busca** en Issues de GitHub
5. **Crea** un nuevo Issue si es necesario

---

**¡Disfruta controlando tu Axe-Fx III con el Maschine Mikro! 🎸** 