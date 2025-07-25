#!/usr/bin/env python3
"""
🎸 Test de Detección de Dispositivos MIDI
========================================
Script para probar la detección de Maschine Mikro y Axe-Fx III
"""

import mido

def test_detection():
    """Prueba la detección de dispositivos MIDI"""
    print("🎸 MAXEschine - Test de Detección de Dispositivos")
    print("=" * 50)
    
    # Obtener puertos MIDI
    input_ports = mido.get_input_names()
    output_ports = mido.get_output_names()
    
    print("📥 Puertos de Entrada:")
    for port in input_ports:
        print(f"  - {port}")
    
    print("\n📤 Puertos de Salida:")
    for port in output_ports:
        print(f"  - {port}")
    
    # Buscar Maschine Mikro
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
    
    # Mostrar resultados
    print("\n🎯 RESULTADOS DE DETECCIÓN:")
    print("-" * 30)
    
    # Maschine Mikro
    if maschine_input:
        print(f"✅ Maschine Mikro (Entrada): {maschine_input}")
    else:
        print("❌ Maschine Mikro (Entrada): No encontrado")
    
    if maschine_output:
        print(f"✅ Maschine Mikro (Salida): {maschine_output}")
    else:
        print("❌ Maschine Mikro (Salida): No encontrado")
    
    # Axe-Fx III
    if axefx_input:
        print(f"✅ Axe-Fx III (Entrada): {axefx_input}")
    else:
        print("❌ Axe-Fx III (Entrada): No encontrado")
    
    if axefx_output:
        print(f"✅ Axe-Fx III (Salida): {axefx_output}")
    else:
        print("❌ Axe-Fx III (Salida): No encontrado")
    
    # Estado general
    maschine_detected = maschine_input is not None
    axefx_detected = axefx_output is not None or axefx_input is not None
    
    print(f"\n📊 ESTADO GENERAL:")
    print(f"  Maschine Mikro: {'✅ Conectado' if maschine_detected else '❌ No conectado'}")
    print(f"  Axe-Fx III: {'✅ Conectado' if axefx_detected else '❌ No conectado'}")
    
    if maschine_detected and axefx_detected:
        print("\n🎸 ¡Sistema listo para usar!")
    elif maschine_detected:
        print("\n⚠️ Maschine Mikro detectado, pero Axe-Fx III no encontrado")
    elif axefx_detected:
        print("\n⚠️ Axe-Fx III detectado, pero Maschine Mikro no encontrado")
    else:
        print("\n❌ No se detectaron dispositivos")

if __name__ == "__main__":
    test_detection() 