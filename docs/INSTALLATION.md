# Guía de Instalación Detallada

Esta guía te ayudará a instalar y configurar Maschine Axe-Fx Control paso a paso.

## 📋 Requisitos Previos

### Hardware
- **Maschine Mikro** (cualquier versión)
- **Axe-Fx III**
- **Cable USB** para Maschine Mikro
- **Cable MIDI** o **USB** para Axe-Fx III

### Software
- **Python 3.7 o superior**
- **Sistema operativo**: macOS, Windows o Linux
- **Git** (opcional, para clonar el repositorio)

## 🚀 Instalación Paso a Paso

### 1. Verificar Python

Primero, verifica que tienes Python instalado:

```bash
python3 --version
# o
python --version
```

**Deberías ver algo como**: `Python 3.8.10` o superior

Si no tienes Python instalado:
- **macOS**: Instala desde [python.org](https://www.python.org/downloads/)
- **Windows**: Descarga desde [python.org](https://www.python.org/downloads/)
- **Linux**: `sudo apt install python3` (Ubuntu/Debian)

### 2. Descargar el Proyecto

#### Opción A: Clonar con Git (Recomendado)
```bash
git clone https://github.com/tu-usuario/maschine-axefx-control.git
cd maschine-axefx-control
```

#### Opción B: Descargar ZIP
1. Ve a [GitHub](https://github.com/tu-usuario/maschine-axefx-control)
2. Haz clic en "Code" → "Download ZIP"
3. Extrae el archivo
4. Abre terminal en la carpeta extraída

### 3. Crear Entorno Virtual

**¿Por qué un entorno virtual?**
- Aísla las dependencias del proyecto
- Evita conflictos con otros proyectos
- Facilita la gestión de versiones

```bash
# Crear entorno virtual
python3 -m venv venv

# Activar entorno virtual
# En macOS/Linux:
source venv/bin/activate

# En Windows:
venv\Scripts\activate
```

**Deberías ver** `(venv)` al inicio de tu línea de comando.

### 4. Instalar Dependencias

```bash
# Actualizar pip
pip install --upgrade pip

# Instalar dependencias
pip install -r requirements.txt
```

**Dependencias instaladas**:
- `mido`: Librería MIDI para Python
- `python-rtmidi`: Backend MIDI adicional

### 5. Verificar Instalación

```bash
# Verificar que mido está instalado
python3 -c "import mido; print('✅ mido instalado correctamente')"

# Verificar puertos MIDI disponibles
python3 -c "import mido; print('Puertos MIDI:', mido.get_input_names())"
```

## 🔧 Configuración del Hardware

### Conectar Maschine Mikro

1. **Conecta** el Maschine Mikro via USB
2. **Verifica** que aparece en tu sistema:
   - **macOS**: System Preferences → Sound → Input
   - **Windows**: Device Manager → Audio inputs and outputs
   - **Linux**: `lsusb` o `dmesg`

### Conectar Axe-Fx III

#### Opción A: USB (Recomendado)
1. **Conecta** el Axe-Fx III via USB
2. **Instala drivers** si es necesario:
   - **Windows**: Descarga drivers desde Fractal Audio
   - **macOS/Linux**: Generalmente funciona sin drivers

#### Opción B: MIDI Tradicional
1. **Conecta** cable MIDI del Axe-Fx III a tu interfaz MIDI
2. **Verifica** que aparece en los puertos MIDI

### Verificar Conexiones

```bash
# Ejecutar script de verificación
python3 run_maschine_control.py
```

**Deberías ver**:
- ✅ Maschine Mikro detectado
- ✅ Axe-Fx III detectado (si está conectado)
- ✅ Configuración automática completada

## ⚙️ Configuración del Axe-Fx III

### Configuración Automática (Recomendada)

El script configura automáticamente tu Axe-Fx III:

1. **Ejecuta** el script principal:
   ```bash
   python3 run_maschine_control.py
   ```

2. **Responde** `s` cuando pregunte si quieres verificar la configuración

3. **El script configurará**:
   - Scene Select (CC#35)
   - External Controllers 1-8 (CC#16-23)
   - Bypass de efectos (CC#18-29)
   - Main Volume (CC#11)

### Configuración Manual (Opcional)

Si prefieres configurar manualmente:

#### 1. Scene Select
- **Ubicación**: Setup > MIDI/Remote > Scene Select
- **Configuración**: CC = 35

#### 2. External Controllers
- **Ubicación**: Setup > MIDI/Remote > External Controllers
- **Configuración**:
  - External Controller 1: CC = 16
  - External Controller 2: CC = 17
  - External Controller 3: CC = 18
  - External Controller 4: CC = 19
  - External Controller 5: CC = 20
  - External Controller 6: CC = 21
  - External Controller 7: CC = 22
  - External Controller 8: CC = 23

#### 3. Efectos Bypass
- **Ubicación**: Setup > MIDI/Remote > Buscar cada efecto
- **Configuración para cada efecto**:
  - Bypass CC = [número mostrado]
  - Bypass Mode = Mute FX In
  - Bypass Value = 127

## 🧪 Prueba del Sistema

### 1. Ejecutar el Script

```bash
python3 run_maschine_control.py
```

### 2. Probar Funcionalidades

1. **Pads 1-4**: Cambiar escenas
2. **Pads 5-16**: Activar/desactivar efectos
3. **Potenciómetro**: Controlar parámetros
4. **Botones laterales**: Seleccionar controladores

### 3. Verificar Salida

**Deberías ver** en la consola:
```
PAD 05 - CC #18 (GEQ1 ON)
PAD 06 - CC #19 (REVERB1 OFF)
```

## 🔧 Solución de Problemas

### Error: "mido no está instalado"
```bash
pip install mido
```

### Error: "No se encuentra el puerto MIDI"
1. Verifica conexiones USB/MIDI
2. Reinicia el hardware
3. Verifica drivers (Windows)

### Error: "Permission denied" (Linux)
```bash
sudo usermod -a -G audio $USER
# Reinicia sesión
```

### Los pads no responden
1. Verifica que el Maschine Mikro esté en modo MIDI
2. Verifica configuración del Axe-Fx III
3. Revisa logs del script

### Axe-Fx III no responde
1. Verifica conexión USB/MIDI
2. Verifica configuración MIDI en Axe-Fx III
3. Ejecuta configuración automática

## 📞 Soporte

Si tienes problemas:

1. **Revisa** esta guía de instalación
2. **Busca** en [Issues](https://github.com/tu-usuario/maschine-axefx-control/issues)
3. **Crea** un nuevo Issue con:
   - Descripción del problema
   - Pasos para reproducir
   - Información del sistema
   - Logs de error

---

**¡Tu Maschine Mikro + Axe-Fx III está listo para usar! 🎸** 