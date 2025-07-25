#!/usr/bin/env python3
"""
🎸 Test Simple para MAXEschine Monitor
======================================
Script de prueba simple para verificar el monitor
"""

import mido
import time

def test_midi_ports():
    """Prueba básica de puertos MIDI"""
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
    
    return maschine_found

def main():
    """Función principal"""
    print("🎸 MAXEschine - Test Simple del Monitor")
    print("=" * 50)
    
    # Probar puertos MIDI
    maschine_ok = test_midi_ports()
    
    if maschine_ok:
        print("\n✅ Sistema listo para usar")
        print("💡 Ejecuta: ./venv/bin/python realtime_monitor_console.py")
    else:
        print("\n⚠️ Maschine Mikro no detectado")
        print("💡 Asegúrate de que esté conectado y configurado")

if __name__ == "__main__":
    main() 