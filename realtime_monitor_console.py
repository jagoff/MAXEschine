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
    LATERAL_BUTTONS = {112: 1, 113: 2, 114: 3, 115: 4, 116: 5, 117: 6, 118: 7, 119: 8}
    SCENE_SELECT_CC = 35


class ConsoleMonitor:
    """Monitor en tiempo real con interfaz de consola"""
    
    def __init__(self):
        self.midi_input = None
        self.midi_output = None
        self.running = False
        self.message_count = 0
        self.start_time = time.time()
        self.effect_states = {}
        self.active_controller = 1
        self.active_button = 1
        self.pot_value = 0
        
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
        
        # Panel de Controladores
        print("\n🎛️ CONTROLADORES EXTERNOS:")
        print("-" * 30)
        print(f"  Controller {self.active_controller} CC#{15 + self.active_controller}")
        print(f"  Potenciómetro: {self.pot_value:3d}")
    
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
    
    def handle_control_change(self, msg):
        """Maneja mensajes de Control Change"""
        cc = msg.control
        value = msg.value
        
        # Botones laterales: Selección de controlador
        if cc in LATERAL_BUTTONS:
            button_num = LATERAL_BUTTONS[cc]
            controller_num = button_num
            self.active_controller = controller_num
            self.active_button = button_num
            self.add_message(f"Button {button_num} Controller {controller_num}")
            
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