#!/usr/bin/env python3
"""
Configuración centralizada para Maschine Mikro + Axe-Fx III Control
"""

# =============================================================================
# CONFIGURACIÓN MIDI
# =============================================================================

# Nombres de puertos MIDI
MASCHINE_MIDI_NAME = 'Maschine Mikro Input'
MASCHINE_OUTPUT_NAME = 'Maschine Mikro Output'
AXEFX_MIDI_NAME = 'Axe-Fx III'

# =============================================================================
# MAPEO DE PADS Y ESCENAS
# =============================================================================

# Mapeo de pads 1-4 a escenas (notas MIDI 36-39)
NOTE_TO_SCENE = {
    36: 1,  # Pad 1 → Escena 1
    37: 2,  # Pad 2 → Escena 2
    38: 3,  # Pad 3 → Escena 3
    39: 4   # Pad 4 → Escena 4
}

# CC# para selección de escenas
SCENE_SELECT_CC = 35

# =============================================================================
# MAPEO DE EFECTOS Y PADS
# =============================================================================

# Mapeo real de pads 5-16 a efectos (CC CONSECUTIVOS para facilitar configuración)
PAD_TO_EFFECT = {
    24: 'GEQ1',     # Pad físico 5 → GEQ 1 → CC#18
    25: 'REVERB1',  # Pad físico 6 → Reverb 1 → CC#19
    26: 'DELAY1',   # Pad físico 7 → Delay 1 → CC#20
    27: 'COMP1',    # Pad físico 8 → Compressor 1 → CC#21
    28: 'AMP1',     # Pad físico 5 (duplicado) → Amp 1 → CC#22
    29: 'AMP2',     # Pad físico 6 (duplicado) → Amp 2 → CC#23
    30: 'DRIVE1',   # Pad físico 7 (duplicado) → Drive 1 → CC#24
    31: 'DRIVE2',   # Pad físico 8 (duplicado) → Drive 2 → CC#25
    32: 'CAB1',     # Pad físico 5 (duplicado) → Cab 1 → CC#26
    33: 'CAB2',     # Pad físico 6 (duplicado) → Cab 2 → CC#27
    34: 'GATE1',    # Pad físico 7 (duplicado) → Gate 1 → CC#28
    35: 'PITCH1',   # Pad físico 8 (duplicado) → Pitch 1 → CC#29
}

# CC# para bypass de efectos
EFFECT_CC_MAPPING = {
    'GEQ1': 18,
    'REVERB1': 19,
    'DELAY1': 20,
    'COMP1': 21,
    'AMP1': 22,
    'AMP2': 23,
    'DRIVE1': 24,
    'DRIVE2': 25,
    'CAB1': 26,
    'CAB2': 27,
    'GATE1': 28,
    'PITCH1': 29
}

# =============================================================================
# EXTERNAL CONTROLLERS
# =============================================================================

# CC# para External Controllers (controlados por potenciómetro)
EXTERNAL_CONTROLLERS = {
    1: 16,  # External Controller 1 → CC#16
    2: 17,  # External Controller 2 → CC#17
    3: 18,  # External Controller 3 → CC#18
    4: 19,  # External Controller 4 → CC#19
    5: 20,  # External Controller 5 → CC#20
    6: 21,  # External Controller 6 → CC#21
    7: 22,  # External Controller 7 → CC#22
    8: 23   # External Controller 8 → CC#23
}

# =============================================================================
# BOTONES LATERALES
# =============================================================================

# CC# para botones laterales (selección de controlador activo)
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

# =============================================================================
# CONTROL DE LUCES
# =============================================================================

# Mapeo de botones laterales a luces
BUTTON_TO_LIGHT = {
    112: 0,  # Botón 1 → Luz 1
    113: 1,  # Botón 2 → Luz 2
    114: 2,  # Botón 3 → Luz 3
    115: 3,  # Botón 4 → Luz 4
    116: 4,  # Botón 5 → Luz 5
    117: 5,  # Botón 6 → Luz 6
    118: 6,  # Botón 7 → Luz 7
    119: 7   # Botón 8 → Luz 8
}

# Mapeo de efectos a luces laterales (para feedback visual)
EFFECT_TO_LIGHT = {
    'GEQ1': 0,      # GEQ1 → Luz lateral 1
    'REVERB1': 1,   # REVERB1 → Luz lateral 2
    'DELAY1': 2,    # DELAY1 → Luz lateral 3
    'COMP1': 3,     # COMP1 → Luz lateral 4
    'AMP1': 4,      # AMP1 → Luz lateral 5
    'AMP2': 5,      # AMP2 → Luz lateral 6
    'DRIVE1': 6,    # DRIVE1 → Luz lateral 7
    'DRIVE2': 7,    # DRIVE2 → Luz lateral 8
    'CAB1': 0,      # CAB1 → Luz lateral 1 (compartida)
    'CAB2': 1,      # CAB2 → Luz lateral 2 (compartida)
    'GATE1': 2,     # GATE1 → Luz lateral 3 (compartida)
    'PITCH1': 3     # PITCH1 → Luz lateral 4 (compartida)
}

# =============================================================================
# CONFIGURACIÓN POR DEFECTO
# =============================================================================

# Valores por defecto
DEFAULT_ACTIVE_CONTROLLER = 1  # External Controller 1
DEFAULT_ACTIVE_BUTTON = 112    # Botón lateral 1
DEFAULT_EFFECT_STATE = True    # Efectos activos por defecto

# Configuración de debug
DEBUG_ENABLED = True
PAD_DEBUG_ENABLED = True

# =============================================================================
# FUNCIONES DE UTILIDAD
# =============================================================================

def get_effect_cc(effect_name):
    """Obtiene el CC# para un efecto específico"""
    return EFFECT_CC_MAPPING.get(effect_name, None)

def get_external_controller_cc(controller_num):
    """Obtiene el CC# para un External Controller específico"""
    return EXTERNAL_CONTROLLERS.get(controller_num, None)

def get_button_light(button_cc):
    """Obtiene el número de luz para un botón específico"""
    return BUTTON_TO_LIGHT.get(button_cc, None)

def get_effect_light(effect_name):
    """Obtiene el número de luz para un efecto específico"""
    return EFFECT_TO_LIGHT.get(effect_name, None)

def get_controller_from_button(button_cc):
    """Obtiene el número de controlador para un botón específico"""
    return LATERAL_BUTTONS.get(button_cc, None) 