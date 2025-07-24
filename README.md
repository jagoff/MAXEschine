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
- 🎨 **Indicadores Visuales**: Códigos de color para el estado de conexión

## 🚀 Instalación

### Requisitos
- macOS
- Python 3.7+
- Maschine Mikro
- Axe-Fx III

### Instalación Rápida

1. **Clonar el repositorio:**
```bash
git clone https://github.com/jagoff/MAXEschine.git
cd MAXEschine
```

2. **Crear entorno virtual:**
```bash
python3 -m venv venv
source venv/bin/activate
```

3. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

4. **Ejecutar la aplicación:**
```bash
python3 menubar_app_advanced.py
```

## 🎛️ Configuración del Axe-Fx III

### ⚠️ IMPORTANTE
Sigue estos pasos **EXACTAMENTE** en el orden indicado para que el Maschine funcione perfectamente.

### 1️⃣ Configurar Scene Select
**Ubicación:** `Setup > MIDI/Remote > Scene Select`
- **CC = 35**
- Esto permite que los Pads 1-4 del Maschine cambien de escena

### 2️⃣ Configurar External Controllers
**Ubicación:** `Setup > MIDI/Remote > External Controllers`

Configuración para cada External Controller:
- **External Controller 1:** CC = 16
- **External Controller 2:** CC = 17
- **External Controller 3:** CC = 18
- **External Controller 4:** CC = 19
- **External Controller 5:** CC = 20
- **External Controller 6:** CC = 21
- **External Controller 7:** CC = 22
- **External Controller 8:** CC = 23

💡 Esto permite que el potenciómetro del Maschine controle diferentes parámetros

### 3️⃣ Configurar Efectos para Bypass
**Ubicación:** `Setup > MIDI/Remote > Buscar cada efecto en la lista`

Para cada efecto, configura **EXACTAMENTE**:

| Efecto | Pad | CC | Bypass Mode | Bypass Value |
|--------|-----|----|-------------|--------------|
| COMP1 | 1 | 21 | Mute FX In | 127 |
| DISTORT1 | 2 | 33 | Mute FX In | 127 |
| DELAY1 | 3 | 45 | Mute FX In | 127 |
| REVERB1 | 4 | 41 | Mute FX In | 127 |
| CHORUS1 | 5 | 53 | Mute FX In | 127 |
| FLANGER1 | 6 | 57 | Mute FX In | 127 |
| PHASER1 | 7 | 65 | Mute FX In | 127 |
| WAH1 | 8 | 69 | Mute FX In | 127 |
| VOLUME1 | 9 | 77 | Mute FX In | 127 |
| TREMOLO1 | 10 | 81 | Mute FX In | 127 |
| PITCH1 | 11 | 85 | Mute FX In | 127 |
| FILTER1 | 12 | 89 | Mute FX In | 127 |

### 4️⃣ Configuración Adicional (Opcional)
**Main Volume:**
- **Ubicación:** `Setup > MIDI/Remote > Output 1 Volume`
- **Configura:** CC = 11

## 🎯 Mapeo Completo del Maschine Mikro

### 🎵 PADS 1-4 (ESCENAS)
- **Pad 1** → Escena 1 (CC#35 = 0)
- **Pad 2** → Escena 2 (CC#35 = 1)
- **Pad 3** → Escena 3 (CC#35 = 2)
- **Pad 4** → Escena 4 (CC#35 = 3)

### 🎯 PADS 5-16 (EFECTOS BYPASS)
- **Pad 5** → GEQ1 (CC#18)
- **Pad 6** → REVERB1 (CC#41)
- **Pad 7** → DELAY1 (CC#45)
- **Pad 8** → NO MAPEADO (necesita configuración)
- **Pad 9** → AMP1 (CC#11)
- **Pad 10** → AMP2 (CC#12)
- **Pad 11** → DRIVE1 (CC#13)
- **Pad 12** → DRIVE2 (CC#14)
- **Pad 13** → CAB1 (CC#15)
- **Pad 14** → CAB2 (CC#16)
- **Pad 15** → GATE1 (CC#17)
- **Pad 16** → PITCH1 (CC#85)

### 🎚️ POTENCIÓMETRO
Controla el External Controller activo
El External Controller activo se selecciona con botones laterales

### 🎛️ BOTONES LATERALES
- **Botón 1** (CC#112) → External Controller 1
- **Botón 2** (CC#113) → External Controller 2
- **Botón 3** (CC#114) → External Controller 3
- **Botón 4** (CC#115) → External Controller 4
- **Botón 5** (CC#116) → External Controller 5
- **Botón 6** (CC#117) → External Controller 6
- **Botón 7** (CC#118) → External Controller 7
- **Botón 8** (CC#119) → External Controller 8

## 🔧 Configuración de Preset

**IMPORTANTE:** Después de configurar todos los CC#, guarda tu preset:

1. Presiona **STORE** en tu Axe-Fx III
2. Selecciona el preset actual
3. Presiona **ENTER** para confirmar
4. Esto guardará toda la configuración MIDI

## 💡 Consejos Adicionales

- Todos los CC# utilizados están en el rango estándar del Axe-Fx III
- La configuración es compatible con cualquier preset
- Los efectos se pueden reorganizar en tu preset sin cambiar la configuración MIDI
- Si un efecto no existe en tu preset, simplemente no responderá al pad correspondiente
- El potenciómetro solo funciona cuando hay un External Controller activo
- Los botones laterales funcionan como selección única (solo uno activo a la vez)

## ✅ Verificación

Después de configurar todo, verifica que:

- ✅ Los Pads 1-4 del Maschine cambien de escena (CC#35)
- ✅ Los Pads 5-16 hagan bypass toggle de efectos
- ✅ El potenciómetro controle el External Controller activo
- ✅ Los botones laterales seleccionen qué External Controller usar

## 🎵 Uso

1. **Configura tu Axe-Fx III** siguiendo las instrucciones arriba
2. **Guarda tu preset**
3. **Ejecuta MAXEschine:**
```bash
source venv/bin/activate
python3 menubar_app_advanced.py
```
4. **Prueba cada pad del Maschine**
5. **Verifica que las escenas cambien correctamente**
6. **Verifica que los efectos hagan bypass toggle**
7. **Prueba el potenciómetro con diferentes External Controllers**

## 🎸 ¡Tu Maschine Mikro estará completamente funcional con el Axe-Fx III!

---

**Desarrollado con ❤️ para la comunidad de guitarristas**
