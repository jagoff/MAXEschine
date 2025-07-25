#!/usr/bin/env python3
"""
🎸 MAXEschine - Monitor en Tiempo Real (Consola)
================================================
Monitor en tiempo real para Maschine Mikro usando interfaz de consola
"""

import mido
import time
import signal
import sys
import os
from datetime import datetime
import threading
from collections import deque

# Importar configuración
try:
    from config import (
        MASCHINE_MIDI_NAME, MASCHINE_OUTPUT_NAME, AXEFX_MIDI_NAME,
        NOTE_TO_SCENE, PAD_TO_EFFECT, EFFECT_CC_MAPPING,
        LATERAL_BUTTONS, SCENE_SELECT_CC
    )
except ImportError:
    # Valores por defecto si no se encuentra config.py
    MASCHINE_MIDI_NAME = 'Maschine Mikro Input'
    MASCHINE_OUTPUT_NAME = 'Maschine Mikro Output'
    AXEFX_MIDI_NAME = 'Axe-Fx III'
    
    # Mapeos por defecto
    NOTE_TO_SCENE = {36: 1, 37: 2, 38: 3, 39: 4}
    PAD_TO_EFFECT = {
        24: "GEQ1", 25: "REVERB1", 26: "DELAY1", 27: "COMP1",
        28: "AMP1", 29: "AMP2", 30: "DRIVE1", 31: "DRIVE2",
        32: "CAB1", 33: "CAB2", 34: "GATE1", 35: "PITCH1"
    }
    EFFECT_CC_MAPPING = {
        "GEQ1": 18, "REVERB1": 19, "DELAY1": 20, "COMP1": 21,
        "AMP1": 22, "AMP2": 23, "DRIVE1": 24, "DRIVE2": 25,
        "CAB1": 26, "CAB2": 27, "GATE1": 28, "PITCH1": 29
    }
    LATERAL_BUTTONS = {16: 1, 17: 2, 18: 3, 19: 4, 20: 5, 21: 6, 22: 7, 23: 8}
    SCENE_SELECT_CC = 35


class ConsoleMonitor:
    """Monitor en tiempo real con interfaz de consola"""
    
    def __init__(self):
        self.midi_input = None
        self.midi_output = None
        self.maschine_outport = None  # Puerto de salida para controlar luces del Maschine
        self.running = False
        self.message_count = 0
        self.start_time = time.time()
        self.effect_states = {}
        self.active_controller = 1  # Por defecto, controlador 1
        self.active_button = 1
        self.pot_value = 0
        self.last_lateral_button = 1  # Último botón lateral usado
        self.lateral_button_states = {1: False, 2: False, 3: False, 4: False, 5: False, 6: False, 7: False, 8: False}  # Estado de cada botón
        
        # Buffer para mensajes recientes
        self.recent_messages = deque(maxlen=50)
        
        # Inicializar estados de efectos
        for effect_name in EFFECT_CC_MAPPING.keys():
            self.effect_states[effect_name] = False
        
        # Configurar manejador de señales
        signal.signal(signal.SIGINT, self.signal_handler)
    
    def signal_handler(self, sig, frame):
        """Maneja la señal de interrupción"""
        print("\n⏹️ Deteniendo monitor...")
        self.stop_monitoring()
        sys.exit(0)
    
    def clear_screen(self):
        """Limpia la pantalla de la consola"""
        os.system('clear' if os.name == 'posix' else 'cls')
    
    def print_header(self):
        """Imprime el encabezado del monitor"""
        print("🎸 MAXEschine - Monitor en Tiempo Real")
        print("=" * 60)
        print(f"📊 Mensajes: {self.message_count}")
        print("=" * 60)
    
    def print_status_panels(self):
        """Imprime los paneles de estado"""
        # Panel de Pads (Escenas)
        print("\n🎵 PADS 1-4 (ESCENAS):")
        print("-" * 30)
        for i in range(1, 5):
            status = "ON" if self.is_pad_active(i) else "OFF"
            print(f"  PAD {i:02d} CC#{SCENE_SELECT_CC} {status}")
        
        # Panel de Efectos
        print("\n🎚️ EFECTOS (PADS 5-16):")
        print("-" * 30)
        effects = list(EFFECT_CC_MAPPING.keys())
        for i, effect in enumerate(effects):
            pad_num = i + 5
            cc = EFFECT_CC_MAPPING[effect]
            status = "ON" if self.effect_states[effect] else "OFF"
            print(f"  PAD {pad_num:02d} CC#{cc:02d} {effect:8s} {status}")
        
        # Panel de Controladores con estado de botones laterales
        print("\n🎛️ CONTROLADORES EXTERNOS:")
        print("-" * 30)
        print(f"  Controller {self.active_controller} CC#{15 + self.active_controller}")
        print(f"  Potenciómetro: {self.pot_value:3d}")
        print(f"  Último botón usado: {self.last_lateral_button}")
        
        # Estado de botones laterales
        print("\n🔘 BOTONES LATERALES:")
        print("-" * 30)
        for button_num in range(1, 9):
            status = "🟢" if self.lateral_button_states[button_num] else "⚫"
            print(f"  Botón {button_num}: {status}")
    
    def print_recent_messages(self):
        """Imprime los mensajes recientes"""
        print("\n📨 MENSAJES RECIENTES:")
        print("-" * 60)
        
        if not self.recent_messages:
            print("  No hay mensajes recientes")
            return
        
        for msg in list(self.recent_messages)[-5:]:  # Últimos 5 mensajes
            print(f"  {msg}")
    
    def print_help(self):
        """Imprime la ayuda"""
        print("\n💡 COMANDOS:")
        print("-" * 30)
        print("  'q' o Ctrl+C: Salir")
        print("  'c': Limpiar pantalla")
        print("  'h': Mostrar esta ayuda")
        print("  's': Mostrar estadísticas")
        print("  'm': Mostrar mapeo")
    
    def print_mapping(self):
        """Imprime el mapeo de controles"""
        print("\n🎹 MAPEO DE CONTROLES:")
        print("-" * 40)
        
        print("PADS 1-4 (ESCENAS):")
        for note, scene in NOTE_TO_SCENE.items():
            pad_num = note - 35
            print(f"  Pad {pad_num}: Nota {note} → Escena {scene} (CC#{SCENE_SELECT_CC})")
        
        print("\nPADS 5-16 (EFECTOS):")
        for note, effect in PAD_TO_EFFECT.items():
            pad_num = note - 19
            cc = EFFECT_CC_MAPPING.get(effect, "N/A")
            print(f"  Pad {pad_num:2d}: Nota {note:2d} → {effect:8s} (CC#{cc})")
        
        print("\nBOTONES LATERALES:")
        for cc, button_num in LATERAL_BUTTONS.items():
            print(f"  Botón {button_num}: CC#{cc} → External Controller {button_num}")
        
        print("\nPOTENCIÓMETRO:")
        print(f"  CC#22 → External Controller {self.active_controller}")
    
    def get_elapsed_time(self):
        """Obtiene el tiempo transcurrido formateado"""
        elapsed = time.time() - self.start_time
        hours = int(elapsed // 3600)
        minutes = int((elapsed % 3600) // 60)
        seconds = int(elapsed % 60)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    
    def is_pad_active(self, pad_num):
        """Verifica si un pad está activo (simulado)"""
        # Simulación simple - en una implementación real esto vendría del hardware
        return False
    
    def add_message(self, message):
        """Agrega un mensaje al buffer"""
        self.recent_messages.append(message)
    
    def update_display(self):
        """Actualiza la pantalla completa"""
        self.clear_screen()
        self.print_header()
        self.print_status_panels()
        self.print_recent_messages()
        self.print_help()
    
    def start_monitoring(self):
        """Inicia el monitoreo MIDI"""
        try:
            # Buscar puerto MIDI de entrada
            input_ports = mido.get_input_names()
            maschine_input = None
            
            for port in input_ports:
                if MASCHINE_MIDI_NAME.lower() in port.lower():
                    maschine_input = port
                    break
            
            if not maschine_input:
                print("❌ No se encontró el Maschine Mikro")
                print("Puertos disponibles:")
                for port in input_ports:
                    print(f"  - {port}")
                return False
            
            # Conectar al puerto MIDI
            self.midi_input = mido.open_input(maschine_input, callback=self.midi_callback)
            
            # Buscar puerto de salida para Axe-Fx
            output_ports = mido.get_output_names()
            axefx_output = None
            
            for port in output_ports:
                if AXEFX_MIDI_NAME.lower() in port.lower():
                    axefx_output = port
                    break
            
            if axefx_output:
                self.midi_output = mido.open_output(axefx_output)
                self.add_message(f"✅ Conectado a Axe-Fx: {axefx_output}")
            else:
                self.add_message("⚠️ Axe-Fx no encontrado - Modo simulación")
            
            # Buscar puerto de salida para Maschine (para controlar luces)
            maschine_output = None
            for port in output_ports:
                if MASCHINE_OUTPUT_NAME.lower() in port.lower():
                    maschine_output = port
                    break
            
            if maschine_output:
                self.maschine_outport = mido.open_output(maschine_output)
                self.add_message(f"✅ Conectado a Maschine: {maschine_output}")
                
                # Activar automáticamente el último botón lateral usado o el botón 1 por defecto
                self.activate_lateral_button(self.last_lateral_button)
                self.add_message(f"🎛️ Activado automáticamente: Botón lateral {self.last_lateral_button}")
            else:
                self.add_message("⚠️ Maschine Output no encontrado - No se pueden controlar luces")
            
            self.running = True
            self.start_time = time.time()
            self.message_count = 0
            
            self.add_message(f"🎸 Monitor iniciado - Conectado a: {maschine_input}")
            return True
            
        except Exception as e:
            self.add_message(f"❌ Error iniciando monitor: {e}")
            return False
    
    def stop_monitoring(self):
        """Detiene el monitoreo MIDI"""
        self.running = False
        
        if self.midi_input:
            self.midi_input.close()
            self.midi_input = None
        
        if self.midi_output:
            self.midi_output.close()
            self.midi_output = None
        
        if self.maschine_outport:
            self.maschine_outport.close()
            self.maschine_outport = None
        
        self.add_message("⏹️ Monitor detenido")
    
    def midi_callback(self, msg):
        """Callback para mensajes MIDI entrantes"""
        if not self.running:
            return
        
        self.message_count += 1
        
        if msg.type == 'note_on' and msg.velocity > 0:
            self.handle_note_on(msg)
        elif msg.type == 'control_change':
            self.handle_control_change(msg)
    
    def handle_note_on(self, msg):
        """Maneja mensajes de nota ON (pads)"""
        note = msg.note
        velocity = msg.velocity
        
        # Pads 1-4: Cambio de escenas
        if note in NOTE_TO_SCENE:
            scene = NOTE_TO_SCENE[note]
            pad_num = note - 35
            self.add_message(f"PAD {pad_num:02d} CC#{SCENE_SELECT_CC} Scene {scene}")
            
            # Enviar a Axe-Fx
            if self.midi_output:
                scene_value = scene - 1
                self.midi_output.send(mido.Message('control_change', 
                                                 control=SCENE_SELECT_CC, 
                                                 value=scene_value))
            
        # Pads 5-16: Bypass de efectos
        elif note in PAD_TO_EFFECT:
            effect_name = PAD_TO_EFFECT[note]
            pad_num = note - 19
            cc = EFFECT_CC_MAPPING.get(effect_name)
            
            # Toggle estado del efecto
            self.effect_states[effect_name] = not self.effect_states[effect_name]
            status = self.effect_states[effect_name]
            
            self.add_message(f"PAD {pad_num:02d} CC#{cc:02d} {effect_name} {'ON' if status else 'OFF'}")
            
            # Enviar a Axe-Fx
            if self.midi_output:
                if cc:
                    self.midi_output.send(mido.Message('control_change', 
                                                     control=cc, 
                                                     value=127))
        else:
            self.add_message(f"⚠️ Nota no mapeada: {note}")
    
    def activate_lateral_button(self, button_num):
        """Activa un botón lateral específico (radiobutton)"""
        if button_num < 1 or button_num > 8:
            return
        
        # Desactivar todos los botones
        for i in range(1, 9):
            self.lateral_button_states[i] = False
        
        # Activar el botón seleccionado
        self.lateral_button_states[button_num] = True
        self.active_controller = button_num
        self.active_button = button_num
        self.last_lateral_button = button_num
        
        # PRIMERO: Controlar luces físicas (radiobutton)
        self.control_lateral_lights(button_num)
        
        # SEGUNDO: Enviar mensaje MIDI al Axe-Fx para activar el controlador
        if self.midi_output:
            controller_cc = 15 + button_num  # CC 16-23
            self.midi_output.send(mido.Message('control_change', 
                                             control=controller_cc, 
                                             value=127))
            self.add_message(f"🎛️ Activado: External Controller {button_num} (CC#{controller_cc})")
    
    def control_lateral_lights(self, active_button):
        """Controla las luces físicas del Maschine Mikro usando MIDI CC"""
        if not self.maschine_outport:
            return
            
        try:
            # Mapeo de botones laterales a luces (CC# para controlar luces)
            BUTTON_TO_LIGHT = {
                1: 0,  # Botón 1 → Luz 1
                2: 1,  # Botón 2 → Luz 2
                3: 2,  # Botón 3 → Luz 3
                4: 3,  # Botón 4 → Luz 4
                5: 4,  # Botón 5 → Luz 5
                6: 5,  # Botón 6 → Luz 6
                7: 6,  # Botón 7 → Luz 7
                8: 7,  # Botón 8 → Luz 8
            }
            
            # Mapeo de luces a CC# (del backup funcional - CC#112-119)
            LIGHT_CC_MAP = {
                0: 112,  # Luz 1 → CC#112 (mismo que botón 1)
                1: 113,  # Luz 2 → CC#113 (mismo que botón 2)
                2: 114,  # Luz 3 → CC#114 (mismo que botón 3)
                3: 115,  # Luz 4 → CC#115 (mismo que botón 4)
                4: 116,  # Luz 5 → CC#116 (mismo que botón 5)
                5: 117,  # Luz 6 → CC#117 (mismo que botón 6)
                6: 118,  # Luz 7 → CC#118 (mismo que botón 7)
                7: 119,  # Luz 8 → CC#119 (mismo que botón 8)
            }
            
            # Primero apagar todas las luces laterales
            for light_num in range(8):
                if light_num in LIGHT_CC_MAP:
                    cc = LIGHT_CC_MAP[light_num]
                    # Usar valores diferentes para distinguir entre botón presionado (127) y luz prendida (64)
                    self.maschine_outport.send(mido.Message('control_change', control=cc, value=0, channel=0))
                    time.sleep(0.01)  # Pequeña pausa para evitar saturar el MIDI
            
            # Prender SOLO la luz del botón activo (radio button behavior)
            if active_button in BUTTON_TO_LIGHT:
                light_num = BUTTON_TO_LIGHT[active_button]
                if light_num in LIGHT_CC_MAP:
                    cc = LIGHT_CC_MAP[light_num]
                    # Usar valor 64 para luz prendida (diferente de 127 para botón presionado)
                    self.maschine_outport.send(mido.Message('control_change', control=cc, value=64, channel=0))
                    time.sleep(0.01)
                    self.add_message(f"💡 Luz lateral {light_num} prendida (botón {active_button} activo)")
                else:
                    self.add_message(f"❌ Error: Luz {light_num} no mapeada")
            else:
                self.add_message(f"❌ Error: Botón {active_button} no mapeado")
                
        except Exception as e:
            self.add_message(f"❌ Error controlando luces: {e}")
    
    def handle_control_change(self, msg):
        """Maneja mensajes de Control Change"""
        cc = msg.control
        value = msg.value
        
        # Botones laterales: Selección de controlador (RADIOBUTTON)
        if cc in LATERAL_BUTTONS:
            button_num = LATERAL_BUTTONS[cc]
            
            # Comportamiento RADIOBUTTON: solo uno activo a la vez
            if value > 0:  # Solo cuando se presiona (no cuando se suelta)
                self.activate_lateral_button(button_num)
                self.add_message(f"Button {button_num} Controller {button_num} [RADIOBUTTON]")
            
        # Potenciómetro: Control de parámetros
        elif cc == 22:
            self.pot_value = value
            self.add_message(f"Pot {value}")
            
            # Enviar a Axe-Fx
            if self.midi_output:
                controller_cc = 15 + self.active_controller  # CC 16-23
                self.midi_output.send(mido.Message('control_change', 
                                                 control=controller_cc, 
                                                 value=value))
        else:
            self.add_message(f"CC {cc} = {value}")
    
    def run(self):
        """Ejecuta el monitor"""
        print("🎸 MAXEschine - Monitor en Tiempo Real (Consola)")
        print("=" * 60)
        
        # Iniciar monitoreo
        if not self.start_monitoring():
            return
        
        # Bucle principal
        try:
            while self.running:
                self.update_display()
                time.sleep(0.1)  # Actualizar cada 100ms
                
        except KeyboardInterrupt:
            pass
        finally:
            self.stop_monitoring()
            print("\n👋 Monitor cerrado")


def main():
    """Función principal"""
    monitor = ConsoleMonitor()
    monitor.run()


if __name__ == "__main__":
    main() 