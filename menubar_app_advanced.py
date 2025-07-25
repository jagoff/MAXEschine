#!/usr/bin/env python3
"""
Aplicación de menú de barra para MAXEschine - Maschine Mikro + Axe-Fx III Control
"""

import rumps
import threading
import time
import subprocess
import sys
import os
import fcntl
import signal
import json
from pathlib import Path

# Importar configuración
try:
    from config import MASCHINE_MIDI_NAME, MASCHINE_OUTPUT_NAME, AXEFX_MIDI_NAME
except ImportError:
    # Valores por defecto si no se encuentra config.py
    MASCHINE_MIDI_NAME = 'Maschine Mikro Input'
    MASCHINE_OUTPUT_NAME = 'Maschine Mikro Output'
    AXEFX_MIDI_NAME = 'Axe-Fx III'

# Variable global para el descriptor del bloqueo
lock_fd = None

def cleanup_lock(signum=None, frame=None):
    """Limpia el bloqueo al salir"""
    global lock_fd
    try:
        if lock_fd:
            fcntl.flock(lock_fd, fcntl.LOCK_UN)
            os.close(lock_fd)
    except Exception as e:
        pass

# Sistema de bloqueo para una sola instancia
def ensure_single_instance():
    """Asegura que solo se ejecute una instancia de la aplicación"""
    global lock_fd
    lock_file = Path.home() / ".maxeschine.lock"
    
    # Limpiar archivo de bloqueo si existe pero no está siendo usado
    try:
        if lock_file.exists():
            # Verificar si el proceso que creó el lock aún existe
            try:
                with open(lock_file, 'r') as f:
                    pid = f.read().strip()
                    if pid and pid.isdigit():
                        try:
                            os.kill(int(pid), 0)  # Verificar si el proceso existe
                        except OSError:
                            # Proceso no existe, limpiar lock
                            lock_file.unlink()
                            print(f"🧹 Limpiando lock anterior...")
            except:
                # Archivo corrupto, limpiar
                lock_file.unlink()
                print("🧹 Limpiando lock corrupto...")
    except Exception as e:
        print(f"⚠️ Error limpiando lock: {e}")
    
    try:
        # Intentar crear/abrir el archivo de bloqueo
        lock_fd = os.open(lock_file, os.O_CREAT | os.O_TRUNC | os.O_RDWR)
        
        # Escribir PID actual en el archivo
        os.write(lock_fd, str(os.getpid()).encode())
        os.fsync(lock_fd)
        
        # Intentar obtener un bloqueo exclusivo
        fcntl.flock(lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        
        # Si llegamos aquí, obtuvimos el bloqueo
        print("✅ MAXEschine iniciado correctamente")
        
        # Configurar manejadores de señales
        signal.signal(signal.SIGINT, cleanup_lock)
        signal.signal(signal.SIGTERM, cleanup_lock)
        
        return lock_fd
        
    except (OSError, IOError) as e:
        print("❌ MAXEschine ya está ejecutándose")
        print("💡 Cerrando esta instancia...")
        sys.exit(1)

# Verificar instancia única al inicio
ensure_single_instance()


def detect_midi_devices():
    """
    Detecta dispositivos MIDI conectados y devuelve información detallada
    
    Returns:
        dict: Información sobre dispositivos detectados
    """
    try:
        import mido
        input_ports = mido.get_input_names()
        output_ports = mido.get_output_names()
        
        # Buscar Maschine Mikro con diferentes variaciones de nombres
        maschine_variants = ['maschine mikro', 'maschine', 'mikro']
        maschine_input = None
        maschine_output = None
        
        for port in input_ports:
            for variant in maschine_variants:
                if variant in port.lower():
                    maschine_input = port
                    break
            if maschine_input:
                break
                
        for port in output_ports:
            for variant in maschine_variants:
                if variant in port.lower():
                    maschine_output = port
                    break
            if maschine_output:
                break
        
        # Buscar Axe-Fx III
        axefx_variants = ['axe-fx', 'axefx', 'axe fx', 'axe-fx iii', 'axefx iii']
        axefx_output = None
        axefx_input = None
        
        # Buscar en puertos de salida
        for port in output_ports:
            for variant in axefx_variants:
                if variant in port.lower():
                    axefx_output = port
                    break
            if axefx_output:
                break
        
        # Buscar en puertos de entrada también
        for port in input_ports:
            for variant in axefx_variants:
                if variant in port.lower():
                    axefx_input = port
                    break
            if axefx_input:
                break
        
        return {
            'maschine_detected': maschine_input is not None,
            'maschine_input': maschine_input,
            'maschine_output': maschine_output,
            'axefx_detected': axefx_output is not None or axefx_input is not None,
            'axefx_output': axefx_output,
            'axefx_input': axefx_input,
            'input_ports': input_ports,
            'output_ports': output_ports,
            'error': None
        }
        
    except ImportError:
        return {
            'maschine_detected': False,
            'maschine_input': None,
            'maschine_output': None,
            'axefx_detected': False,
            'axefx_output': None,
            'axefx_input': None,
            'input_ports': [],
            'output_ports': [],
            'error': 'mido no está instalado'
        }
    except Exception as e:
        return {
            'maschine_detected': False,
            'maschine_input': None,
            'maschine_output': None,
            'axefx_detected': False,
            'axefx_output': None,
            'axefx_input': None,
            'input_ports': [],
            'output_ports': [],
            'error': str(e)
        }


def get_device_status_message(device_info):
    """
    Genera un mensaje de estado basado en los dispositivos detectados
    
    Args:
        device_info (dict): Información de dispositivos de detect_midi_devices()
        
    Returns:
        str: Mensaje de estado apropiado
    """
    if device_info.get('error'):
        return "🔍 Verificando MIDI..."
    
    maschine_ok = device_info.get('maschine_detected', False)
    axefx_ok = device_info.get('axefx_detected', False)
    
    maschine_status = "✅" if maschine_ok else "❌"
    axefx_status = "✅" if axefx_ok else "❌"
    
    return f"Maschine Mikro: {maschine_status} | Axe-Fx: {axefx_status}"


class MAXEschineApp(rumps.App):
    """Aplicación de menú de barra para control MIDI"""
    
    def __init__(self):
        """Inicializa la aplicación de menú de barra"""
        super().__init__(
            name="MAXEschine",
            title="⚫ MAXEschine",
            icon=None,  # Sin icono - solo título dinámico
            template=False,
            quit_button=None  # Deshabilitar el botón Quit por defecto
        )
        
        # Estado de la aplicación
        self.is_running = False
        self.control_process = None
        self.control_thread = None
        self.device_info = None
        self.last_device_state = None  # Para detectar cambios en el estado
        
        # Configurar menú
        self.setup_menu()
        
        # Configurar el botón Quit personalizado
        self.menu["Quit"] = rumps.MenuItem("Quit", callback=self.quit_app)
        
        # Detectar dispositivos y actualizar estado inicial
        self.update_device_status()
        
        # Iniciar control automáticamente
        self.start_control()
        
        # Configurar actualización automática cada 3 segundos
        self.timer = rumps.Timer(self.auto_update, 3)
        self.timer.start()

    def auto_update(self, _=None):
        """Actualización automática del estado"""
        self.update_device_status()
        self.update_menu_display()

    def update_device_status(self, _=None):
        """Update the detected MIDI device status (in English)"""
        self.device_info = detect_midi_devices()
        
        # Detectar cambios en el estado
        current_state = (
            self.device_info.get('maschine_detected', False),
            self.device_info.get('axefx_detected', False)
        )
        
        # Si hay cambios, actualizar el menú
        if self.last_device_state != current_state:
            self.last_device_state = current_state
            self.update_menu_display()

    def update_menu_display(self, _=None):
        """Actualiza la visualización del menú en tiempo real"""
        if not self.device_info:
            # Si no hay información de dispositivos, mostrar rojo en ambos
            self.maschine_status.title = "Maschine Mikro 🔴"
            self.axefx_status.title = "Axe-Fx 🔴"
            self.update_guitar_icon()
            return
        
        # Actualizar estado de Maschine Mikro - solo verde o rojo
        maschine_ok = self.device_info.get('maschine_detected', False)
        maschine_status = "🟢" if maschine_ok else "🔴"
        self.maschine_status.title = f"Maschine Mikro {maschine_status}"
        
        # Actualizar estado de Axe-Fx - solo verde o rojo
        axefx_ok = self.device_info.get('axefx_detected', False)
        axefx_status = "🟢" if axefx_ok else "🔴"
        self.axefx_status.title = f"Axe-Fx {axefx_status}"
        
        # Actualizar título principal
        self.update_guitar_icon()

    def update_guitar_icon(self):
        """Actualiza el título dinámico con códigos de colores"""
        if not self.device_info:
            # Si no hay información de dispositivos, mostrar negro
            self.title = "⚫ MAXEschine"
            return

        maschine_ok = self.device_info.get('maschine_detected', False)
        axefx_ok = self.device_info.get('axefx_detected', False)

        # Sistema de códigos de colores simplificado
        if maschine_ok and axefx_ok:
            # Verde: Ambos dispositivos conectados
            self.title = "🟢 MAXEschine"
        elif maschine_ok or axefx_ok:
            # Amarillo: Solo un dispositivo conectado
            self.title = "🟡 MAXEschine"
        else:
            # Negro: Ningún dispositivo conectado
            self.title = "⚫ MAXEschine"

    def setup_menu(self):
        """Set up the application menu (in English)"""
        self.maschine_status = rumps.MenuItem("Maschine Mikro 🔴", callback=None)
        self.axefx_status = rumps.MenuItem("Axe-Fx 🔴", callback=None)
        self.menu = [
            self.maschine_status,
            self.axefx_status,
            None,  # Separator
            rumps.MenuItem("Open Real-time Monitor", callback=self.open_monitor),
            rumps.MenuItem("Show Configuration", callback=self.show_config),
            rumps.MenuItem("GitHub", callback=self.open_docs),
            None,  # Separator
            rumps.MenuItem("About", callback=self.show_about)
        ]
    
    def start_control(self, _=None):
        """Inicia el control MIDI en segundo plano automáticamente"""
        if self.is_running:
            return
        
        try:
            # Actualizar estado inmediatamente
            self.is_running = True
            self.update_device_status()  # Actualizar con estado "activo"
            
            # Iniciar control en segundo plano
            self.control_thread = threading.Thread(target=self._run_control_background, daemon=True)
            self.control_thread.start()
            
        except Exception as e:
            self.is_running = False
            # Error silencioso
            pass
    

    
    def _run_control_background(self):
        """Ejecuta el control MIDI en segundo plano"""
        try:
            # Ejecutar el script principal
            script_path = os.path.join(os.path.dirname(__file__), "realtime_monitor_console.py")
            if os.path.exists(script_path):
                self.control_process = subprocess.Popen(
                    [sys.executable, script_path],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                # Esperar a que termine mientras el control esté activo
                while self.is_running and self.control_process.poll() is None:
                    time.sleep(0.5)
                # Si el proceso terminó inesperadamente, actualizar estado
                if self.is_running:
                    self.is_running = False
                    self.control_process = None
                    self.control_thread = None
            else:
                print(f"❌ Script no encontrado: {script_path}")
                self.is_running = False
        except Exception as e:
            print(f"❌ Error en control de fondo: {e}")
            self.is_running = False
        finally:
            # Limpiar estado
            self.control_process = None
            self.control_thread = None
    
    def show_config(self, _=None):
        """Show current configuration (in English)"""
        if not self.device_info:
            self.update_device_status()
        config_text = f"""
        🎸 MAXEschine - CONFIGURATION

📋 MIDI Devices:
        Maschine Mikro: {'Connected' if self.device_info.get('maschine_detected') else 'Not Connected'}
Axe-Fx: {'Connected' if self.device_info.get('axefx_detected') else 'Not Connected'}

📥 Input Ports:
{chr(10).join(f'  • {port}' for port in self.device_info.get('input_ports', []))}

📤 Output Ports:
{chr(10).join(f'  • {port}' for port in self.device_info.get('output_ports', []))}

🎛️ Control State: {'🟢 Active' if self.is_running else '🔴 Inactive'}
        """
        rumps.alert(
            title="Configuration",
            message=config_text.strip()
        )
    
    def open_docs(self, _=None):
        """Open documentation on GitHub (in English)"""
        import webbrowser
        webbrowser.open("https://github.com/jagoff/MAXEschine")
    
    def open_monitor(self, _=None):
        """Open the real-time monitor console"""
        try:
            import subprocess
            import sys
            import os
            
            # Ruta al script del monitor que ya funciona
            monitor_script = os.path.join(os.path.dirname(__file__), "realtime_monitor_console.py")
            
            if os.path.exists(monitor_script):
                # Ejecutar el monitor en una nueva ventana de terminal
                # Comando robusto que detecta entorno virtual automáticamente
                command = f'cd {os.path.dirname(__file__)} && [ -f venv/bin/activate ] && source venv/bin/activate; python3 realtime_monitor_console.py; exit'
                
                subprocess.Popen([
                    "osascript", "-e", 
                    f'tell application "Terminal" to do script "{command}"'
                ])
            else:
                rumps.alert(
                    title="Error",
                    message="Monitor script not found: realtime_monitor_console.py"
                )
        except Exception as e:
            rumps.alert(
                title="Error",
                message=f"Could not open monitor: {str(e)}"
            )
    
    def show_about(self, _=None):
        """Show about information (in English)"""
        about_text = """
        🎸 MAXEschine - MASCHINE MIKRO + AXE-FX III CONTROL

Version: 2.0.0
System: macOS

        Full MIDI control for Maschine Mikro with Axe-Fx III
and Axe-Fx III with menu bar interface.

Developed with Python and rumps.
        """
        rumps.alert(
            title="About",
            message=about_text.strip()
        )
    
    def quit_app(self, _=None):
        """Cierra la aplicación limpiamente"""
        try:
            # Detener control si está corriendo
            if self.is_running:
                self.is_running = False
                
                # Detener proceso si está corriendo
                if self.control_process and self.control_process.poll() is None:
                    self.control_process.terminate()
                    try:
                        self.control_process.wait(timeout=2)
                    except subprocess.TimeoutExpired:
                        self.control_process.kill()
                
                # Esperar a que el thread termine (máximo 3 segundos)
                if self.control_thread and self.control_thread.is_alive():
                    self.control_thread.join(timeout=3)
            
            # Limpiar bloqueo
            cleanup_lock()
            
            # Cerrar aplicación
            rumps.quit_application()
            
        except Exception as e:
            print(f"❌ Error al cerrar: {e}")
            rumps.quit_application()


def main():
    """Función principal"""
    try:
        app = MAXEschineApp()
        app.run()
    except KeyboardInterrupt:
        print("\n🛑 Interrupción del usuario")
        cleanup_lock()
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        cleanup_lock()


if __name__ == "__main__":
    main() 