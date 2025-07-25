#!/usr/bin/env python3
"""
🎸 MAXEschine - Monitor en Tiempo Real
=====================================
Ventana GUI para mostrar la actividad MIDI en tiempo real del Maschine Mikro
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
import threading
import time
import mido
from datetime import datetime
import json
from pathlib import Path

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
    # Mapeo correcto de botones laterales para Maschine Mikro (CC 16-19)
    LATERAL_BUTTONS = {
        16: 1,  # Botón 1
        17: 2,  # Botón 2
        18: 3,  # Botón 3
        19: 4   # Botón 4
    }
    SCENE_SELECT_CC = 35


class RealtimeMonitor:
    """Monitor en tiempo real con interfaz GUI"""
    
    def __init__(self):
        self.root = None
        self.midi_input = None
        self.midi_output = None
        self.maschine_outport = None  # Puerto de salida para feedback de LEDs
        self.running = False
        self.message_count = 0
        self.start_time = time.time()
        self.effect_states = {}
        self.active_scene = None  # Escena activa (radiobutton)
        self.active_controller = 1
        self.active_button = 1
        
        # Inicializar estados de efectos
        for effect_name in EFFECT_CC_MAPPING.keys():
            self.effect_states[effect_name] = False
        
        # Variables de la GUI
        self.log_text = None
        self.status_label = None
        self.stats_label = None
        self.pads_frame = None
        self.effects_frame = None
        self.controllers_frame = None
        
    def create_window(self):
        """Crea la ventana principal del monitor"""
        self.root = tk.Tk()
        # Eliminar el título personalizado
        # self.root.title("🎸 MAXEschine - Monitor en Tiempo Real")
        self.root.geometry("800x600")
        self.root.configure(bg='#2b2b2b')
        
        # Configurar estilo
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('Title.TLabel', font=('Arial', 14, 'bold'), foreground='#ffffff', background='#2b2b2b')
        style.configure('Status.TLabel', font=('Arial', 10), foreground='#00ff00', background='#2b2b2b')
        style.configure('Stats.TLabel', font=('Arial', 9), foreground='#cccccc', background='#2b2b2b')
        
        # Frame principal
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Título
        title_label = ttk.Label(main_frame, text="🎸 MAXEschine - Monitor en Tiempo Real", style='Title.TLabel')
        title_label.pack(pady=(0, 10))
        
        # Frame superior para controles
        controls_frame = ttk.Frame(main_frame)
        controls_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Botones de control
        self.start_button = ttk.Button(controls_frame, text="▶️ Iniciar Monitor", command=self.start_monitoring)
        self.start_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.stop_button = ttk.Button(controls_frame, text="⏹️ Detener Monitor", command=self.stop_monitoring, state='disabled')
        self.stop_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.clear_button = ttk.Button(controls_frame, text="🗑️ Limpiar Log", command=self.clear_log)
        self.clear_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Estado de conexión
        self.status_label = ttk.Label(controls_frame, text="🔴 Desconectado", style='Status.TLabel')
        self.status_label.pack(side=tk.RIGHT)
        
        # Frame para estadísticas
        stats_frame = ttk.Frame(main_frame)
        stats_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.stats_label = ttk.Label(stats_frame, text="Mensajes: 0 | Tiempo: 00:00:00", style='Stats.TLabel')
        self.stats_label.pack(side=tk.LEFT)
        
        # Frame para paneles de estado
        panels_frame = ttk.Frame(main_frame)
        panels_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Panel de Pads (Escenas)
        self.create_pads_panel(panels_frame)
        
        # Panel de Efectos
        self.create_effects_panel(panels_frame)
        
        # Panel de Controladores
        self.create_controllers_panel(panels_frame)
        
        # Log de mensajes
        log_frame = ttk.LabelFrame(main_frame, text="📨 Log de Mensajes MIDI")
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        self.log_text = scrolledtext.ScrolledText(
            log_frame, 
            height=15, 
            bg='#1e1e1e', 
            fg='#00ff00', 
            font=('Consolas', 9),
            insertbackground='#00ff00'
        )
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Configurar cierre de ventana
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Iniciar actualización de estadísticas
        self.update_stats()
        
    def create_pads_panel(self, parent):
        """Crea el panel de estado de los pads (escenas)"""
        self.pads_frame = ttk.LabelFrame(parent, text="🎵 Pads 1-4 (Escenas)")
        self.pads_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        # Crear labels para cada pad
        self.pad_labels = {}
        for i in range(1, 5):
            label = ttk.Label(self.pads_frame, text=f"Pad {i}: Escena {i}", style='Stats.TLabel')
            label.pack(anchor=tk.W, padx=5, pady=2)
            self.pad_labels[i] = label
    
    def create_effects_panel(self, parent):
        """Crea el panel de estado de los efectos"""
        self.effects_frame = ttk.LabelFrame(parent, text="🎚️ Efectos (Pads 5-16)")
        self.effects_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Crear labels para cada efecto
        self.effect_labels = {}
        effects = list(EFFECT_CC_MAPPING.keys())
        for i, effect in enumerate(effects):
            pad_num = i + 5
            label = ttk.Label(self.effects_frame, text=f"Pad {pad_num}: {effect} 🔴", style='Stats.TLabel')
            label.pack(anchor=tk.W, padx=5, pady=1)
            self.effect_labels[effect] = label
    
    def create_controllers_panel(self, parent):
        """Crea el panel de controladores externos con feedback visual de botones"""
        self.controllers_frame = ttk.LabelFrame(parent, text="🎛️ Controladores Externos")
        self.controllers_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))
        
        # Controlador activo
        self.active_controller_label = ttk.Label(
            self.controllers_frame, 
            text="Activo: External Controller 1", 
            style='Status.TLabel'
        )
        self.active_controller_label.pack(anchor=tk.W, padx=5, pady=2)
        
        # Botón activo
        self.active_button_label = ttk.Label(
            self.controllers_frame, 
            text="Botón: 1", 
            style='Stats.TLabel'
        )
        self.active_button_label.pack(anchor=tk.W, padx=5, pady=2)
        
        # Feedback visual para los 8 botones laterales
        self.controller_button_labels = {}
        for i in range(1, 9):
            color = "🟢" if i == self.active_button else "🔴"
            label = ttk.Label(self.controllers_frame, text=f"Botón {i}: {color}", style='Stats.TLabel')
            label.pack(anchor=tk.W, padx=10, pady=1)
            self.controller_button_labels[i] = label
        
        # Valor del potenciómetro
        self.pot_value_label = ttk.Label(
            self.controllers_frame, 
            text="Potenciómetro: 0", 
            style='Stats.TLabel'
        )
        self.pot_value_label.pack(anchor=tk.W, padx=5, pady=2)
    
    def log_message(self, message):
        """Agrega un mensaje al log"""
        if self.log_text:
            timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
            self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
            self.log_text.see(tk.END)
    
    def update_pad_status(self, pad_num, status, effect_name=None):
        """Actualiza el estado visual de un pad o efecto"""
        if pad_num <= 4 and pad_num in self.pad_labels:
            # Pads 1-4 (Escenas)
            for i in range(1, 5):
                color = "🟢" if i == self.active_scene else "🔴"
                self.pad_labels[i].config(text=f"Pad {i}: Escena {i} {color}")
        elif effect_name and effect_name in self.effect_labels:
            # Pads 5-16 (Efectos)
            color = "🟢" if status else "🔴"
            self.effect_labels[effect_name].config(text=f"{effect_name} {color}")
    
    def update_controller_status(self, controller_num, button_num, pot_value=None):
        """Actualiza el estado de los controladores y feedback visual"""
        self.active_controller = controller_num
        self.active_button = button_num
        
        # Actualizar feedback visual para botones laterales (solo uno activo)
        if hasattr(self, 'controller_button_labels'):
            for i in range(1, 9):
                color = "🟢" if i == self.active_button else "🔴"
                self.controller_button_labels[i].config(text=f"Botón {i}: {color}")
        
        self.active_controller_label.config(text=f"Activo: External Controller {controller_num}")
        self.active_button_label.config(text=f"Botón: {button_num}")
        
        if pot_value is not None:
            self.pot_value_label.config(text=f"Potenciómetro: {pot_value}")
    
    def update_stats(self):
        """Actualiza las estadísticas en tiempo real"""
        if self.running:
            elapsed = time.time() - self.start_time
            hours = int(elapsed // 3600)
            minutes = int((elapsed % 3600) // 60)
            seconds = int(elapsed % 60)
            
            stats_text = f"Mensajes: {self.message_count} | Tiempo: {hours:02d}:{minutes:02d}:{seconds:02d}"
            self.stats_label.config(text=stats_text)
        
        # Programar próxima actualización
        self.root.after(1000, self.update_stats)
    
    def start_monitoring(self):
        """Inicia el monitoreo MIDI y abre el puerto de salida de la Maschine para feedback de LEDs"""
        try:
            # Buscar puerto MIDI de entrada
            input_ports = mido.get_input_names()
            maschine_input = None
            for port in input_ports:
                if MASCHINE_MIDI_NAME.lower() in port.lower():
                    maschine_input = port
                    break
            if not maschine_input:
                self.log_message("❌ No se encontró el Maschine Mikro")
                return
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
                self.log_message(f"✅ Conectado a Axe-Fx: {axefx_output}")
            else:
                self.log_message("⚠️ Axe-Fx no encontrado - Modo simulación")
            # Abrir puerto de salida de la Maschine para feedback de LEDs
            maschine_output = None
            for port in output_ports:
                if MASCHINE_OUTPUT_NAME.lower() in port.lower():
                    maschine_output = port
                    break
            if maschine_output:
                self.maschine_outport = mido.open_output(maschine_output)
                self.log_message(f"✅ Feedback LED habilitado: {maschine_output}")
            else:
                self.maschine_outport = None
                self.log_message("⚠️ Feedback LED no disponible (no se encontró salida Maschine)")
            self.running = True
            self.start_time = time.time()
            self.message_count = 0
            # Actualizar UI
            self.status_label.config(text="🟢 Conectado")
            self.start_button.config(state='disabled')
            self.stop_button.config(state='normal')
            self.log_message(f"🎸 Monitor iniciado - Conectado a: {maschine_input}")
            # Reflejar estado inicial en LEDs
            self.update_led_feedback()
        except Exception as e:
            self.log_message(f"❌ Error iniciando monitor: {e}")
    
    def stop_monitoring(self):
        """Detiene el monitoreo MIDI y cierra el puerto de salida de la Maschine"""
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
        # Actualizar UI
        self.status_label.config(text="🔴 Desconectado")
        self.start_button.config(state='normal')
        self.stop_button.config(state='disabled')
        self.log_message("⏹️ Monitor detenido")
    
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
        # Pads 1-4: Cambio de escenas (modo radiobutton)
        if note in NOTE_TO_SCENE:
            scene = NOTE_TO_SCENE[note]
            pad_num = note - 35
            self.active_scene = pad_num  # Solo uno activo
            self.log_message(f"🎵 Pad {pad_num} → Escena {scene}")
            self.update_pad_status(pad_num, True)
            # Enviar a Axe-Fx
            if self.midi_output:
                scene_value = scene - 1
                self.midi_output.send(mido.Message('control_change', 
                                                 control=SCENE_SELECT_CC, 
                                                 value=scene_value))
                self.log_message(f"   → CC#{SCENE_SELECT_CC} = {scene_value}")
            # Reflejar en LEDs
            self.update_led_feedback()
        # Pads 5-16: Bypass de efectos
        elif note in PAD_TO_EFFECT:
            effect_name = PAD_TO_EFFECT[note]
            pad_num = note - 19
            self.log_message(f"🎚️ Pad {pad_num} → {effect_name}")
            # Toggle estado del efecto
            self.effect_states[effect_name] = not self.effect_states[effect_name]
            status = self.effect_states[effect_name]
            self.update_pad_status(pad_num, status, effect_name)
            # Enviar a Axe-Fx
            if self.midi_output:
                cc = EFFECT_CC_MAPPING.get(effect_name)
                if cc:
                    self.midi_output.send(mido.Message('control_change', 
                                                     control=cc, 
                                                     value=127))
                    self.log_message(f"   → CC#{cc} = 127 ({'ON' if status else 'OFF'})")
            # Reflejar en LEDs
            self.update_led_feedback()
        else:
            self.log_message(f"⚠️ Nota no mapeada: {note}")
    
    def handle_control_change(self, msg):
        """Maneja mensajes de Control Change"""
        cc = msg.control
        value = msg.value
        # Botones laterales: Selección de controlador
        if cc in LATERAL_BUTTONS:
            button_num = LATERAL_BUTTONS[cc]
            controller_num = button_num
            self.log_message(f"🎛️ Botón {button_num} → External Controller {controller_num}")
            self.update_controller_status(controller_num, button_num)
            # Reflejar en LEDs
            self.update_led_feedback()
        # Potenciómetro: Control de parámetros
        elif cc == 22:
            self.log_message(f"🎚️ Potenciómetro: {value}")
            self.update_controller_status(self.active_controller, self.active_button, value)
            # Enviar a Axe-Fx
            if self.midi_output:
                controller_cc = 15 + self.active_controller  # CC 16-23
                self.midi_output.send(mido.Message('control_change', 
                                                 control=controller_cc, 
                                                 value=value))
                self.log_message(f"   → CC#{controller_cc} = {value}")
        else:
            self.log_message(f"⚠️ CC no mapeado: {cc} = {value}")
    
    def clear_log(self):
        """Limpia el log de mensajes"""
        if self.log_text:
            self.log_text.delete(1.0, tk.END)
    
    def on_closing(self):
        """Maneja el cierre de la ventana"""
        self.stop_monitoring()
        self.root.destroy()
    
    def run(self):
        """Ejecuta la ventana del monitor"""
        self.create_window()
        self.root.mainloop()

    def update_led_feedback(self):
        """Feedback radiobutton real para barra lateral Maschine Mikro (idéntico al backup funcional)"""
        if not self.maschine_outport:
            return
        # Apagar todos los LEDs laterales
        for cc in LATERAL_BUTTONS.keys():
            self.maschine_outport.send(mido.Message('control_change', channel=0, control=cc, value=0))
        # Encender solo el LED del botón activo
        for cc, button_num in LATERAL_BUTTONS.items():
            if button_num == self.active_button:
                self.maschine_outport.send(mido.Message('control_change', channel=0, control=cc, value=127))
        # (El feedback de pads y efectos se mantiene igual)
        for i in range(1, 5):
            note = 35 + i  # Notas 36-39
            velocity = 127 if i == self.active_scene else 0
            self.maschine_outport.send(mido.Message('note_on', note=note, velocity=velocity))
        for idx, effect in enumerate(EFFECT_CC_MAPPING.keys()):
            pad_num = idx + 5
            note = 19 + pad_num  # Notas 24-35
            velocity = 127 if self.effect_states[effect] else 0
            self.maschine_outport.send(mido.Message('note_on', note=note, velocity=velocity))


def main():
    """Función principal para ejecutar el monitor independientemente"""
    monitor = RealtimeMonitor()
    monitor.run()


if __name__ == "__main__":
    main() 