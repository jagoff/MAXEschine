#!/usr/bin/env python3
"""
🎸 Test Script para MAXEschine Monitor
======================================
Script de prueba para verificar que el monitor funciona correctamente
"""

import mido
import time
import threading
from realtime_monitor import RealtimeMonitor

def test_midi_ports():
    """Prueba la detección de puertos MIDI"""
    print("🎵 Puertos MIDI disponibles:")
    print("=" * 40)
    
    inputs = mido.get_input_names()
    outputs = mido.get_output_names()
    
    print("📥 Entrada:")
    for name in inputs:
        print(f"  - {name}")
    
    print("\n📤 Salida:")
    for name in outputs:
        print(f"  - {name}")
    
    # Buscar Maschine Mikro
    maschine_found = False
    for port in inputs:
        if 'maschine' in port.lower():
            maschine_found = True
            print(f"\n✅ Maschine Mikro encontrado: {port}")
            break
    
    if not maschine_found:
        print("\n❌ Maschine Mikro no encontrado")
    
    # Buscar Axe-Fx
    axefx_found = False
    for port in outputs:
        if 'axe' in port.lower():
            axefx_found = True
            print(f"✅ Axe-Fx encontrado: {port}")
            break
    
    if not axefx_found:
        print("❌ Axe-Fx no encontrado")
    
    return maschine_found, axefx_found

def test_monitor():
    """Prueba el monitor en tiempo real"""
    print("\n🎸 Iniciando prueba del monitor...")
    
    # Crear instancia del monitor
    monitor = RealtimeMonitor()
    
    # Crear ventana en un thread separado
    def run_monitor():
        monitor.run()
    
    monitor_thread = threading.Thread(target=run_monitor, daemon=True)
    monitor_thread.start()
    
    # Esperar un poco para que la ventana se abra
    time.sleep(2)
    
    print("✅ Monitor iniciado correctamente")
    print("💡 La ventana del monitor debería estar abierta")
    print("🎹 Prueba presionando los pads del Maschine Mikro")
    
    # Mantener el script corriendo
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n⏹️ Deteniendo prueba...")
        if monitor.root:
            monitor.root.quit()

def main():
    """Función principal"""
    print("🎸 MAXEschine - Test del Monitor en Tiempo Real")
    print("=" * 50)
    
    # Probar puertos MIDI
    maschine_ok, axefx_ok = test_midi_ports()
    
    if not maschine_ok:
        print("\n⚠️ Maschine Mikro no detectado")
        print("💡 Asegúrate de que esté conectado y configurado")
        return
    
    # Preguntar si continuar con la prueba del monitor
    print("\n¿Deseas continuar con la prueba del monitor? (s/n): ", end="")
    try:
        response = input().lower().strip()
        if response in ['s', 'si', 'sí', 'y', 'yes']:
            test_monitor()
        else:
            print("Prueba cancelada")
    except KeyboardInterrupt:
        print("\nPrueba cancelada")

if __name__ == "__main__":
    main() 