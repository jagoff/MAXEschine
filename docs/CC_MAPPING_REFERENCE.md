# 🎸 MAXEschine - Referencia de Mapeo CC

## 📋 Mapeo Completo de Pads y CC

### 🎵 PADS 1-4 (ESCENAS)
| Pad | Nota MIDI | CC | Función |
|-----|-----------|----|---------|
| Pad 1 | 36 | 35 | Escena 1 |
| Pad 2 | 37 | 35 | Escena 2 |
| Pad 3 | 38 | 35 | Escena 3 |
| Pad 4 | 39 | 35 | Escena 4 |

### 🎯 PADS 5-16 (EFECTOS BYPASS)
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

### 🎚️ EXTERNAL CONTROLLERS (Potenciómetro)
| Controlador | CC | Función |
|-------------|----|---------|
| External Controller 1 | 16 | Controlado por potenciómetro |
| External Controller 2 | 17 | Controlado por potenciómetro |
| External Controller 3 | 18 | Controlado por potenciómetro |
| External Controller 4 | 19 | Controlado por potenciómetro |
| External Controller 5 | 20 | Controlado por potenciómetro |
| External Controller 6 | 21 | Controlado por potenciómetro |
| External Controller 7 | 22 | Controlado por potenciómetro |
| External Controller 8 | 23 | Controlado por potenciómetro |

### 🎛️ BOTONES LATERALES (Selección de Controlador)
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

## ⚙️ Configuración del Axe-Fx III

### Scene Select
- **Ubicación:** `Setup > MIDI/Remote > Scene Select`
- **CC = 35**

### External Controllers
- **Ubicación:** `Setup > MIDI/Remote > External Controllers`
- **CC 16-23** para External Controllers 1-8

### Efectos Bypass
- **Ubicación:** `Setup > MIDI/Remote > [Buscar cada efecto]`
- **Bypass Mode:** Mute FX In
- **Bypass Value:** 127

## 🚀 Uso Rápido

1. **Configurar Axe-Fx III** según la tabla arriba
2. **Ejecutar MAXEschine:**
   ```bash
   ./start.sh
   ```
3. **Probar pads del Maschine Mikro**
4. **Verificar que las escenas cambien (Pads 1-4)**
5. **Verificar que los efectos hagan bypass (Pads 5-16)**
6. **Probar potenciómetro con botones laterales**

## 📝 Notas Importantes

- Todos los CC están en el rango estándar del Axe-Fx III
- La configuración es compatible con cualquier preset
- Los efectos se pueden reorganizar sin cambiar la configuración MIDI
- El potenciómetro solo funciona cuando hay un External Controller activo
- Los botones laterales funcionan como selección única (solo uno activo a la vez) 