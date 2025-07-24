#!/usr/bin/env python3
"""
Controlador MIDI Maschine Mikro → Axe-Fx III
Lee el mapeo desde cc_pad_mapping.json y envía mensajes CC según los pads.
"""
import json
import mido
import sys
import argparse
import os
from pathlib import Path

MAPPING_FILE = 'cc_pad_mapping.json'
MIDI_PORT_NAME = 'Axe-Fx'  # Cambia esto según tu dispositivo MIDI


def load_mapping(mapping_file):
    """Carga el mapeo de pads a CC desde un archivo JSON."""
    try:
        with open(mapping_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"[ERROR] No se encontró el archivo de mapeo: {mapping_file}")
        print(f"[INFO] Asegúrate de que {mapping_file} esté en el directorio actual")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"[ERROR] Error en el formato JSON del archivo {mapping_file}: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR] No se pudo cargar el mapeo: {e}")
        sys.exit(1)


def find_midi_output(port_hint):
    """Busca un puerto de salida MIDI que contenga el hint dado."""
    available_ports = mido.get_output_names()
    
    if not available_ports:
        print("[ERROR] No se encontraron puertos MIDI de salida disponibles.")
        print("[INFO] Asegúrate de que tu Axe-Fx III esté conectado y configurado.")
        sys.exit(1)
    
    for name in available_ports:
        if port_hint.lower() in name.lower():
            return name
    
    print(f"[ERROR] No se encontró un puerto MIDI que contenga '{port_hint}'.")
    print("[INFO] Puertos MIDI disponibles:")
    for name in available_ports:
        print(f"  - {name}")
    print(f"\n[INFO] Puedes cambiar el nombre del puerto en el script o usar --port")
    sys.exit(1)


def list_midi_ports():
    """Lista todos los puertos MIDI disponibles."""
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
    
    if not inputs and not outputs:
        print("  No se encontraron dispositivos MIDI")
        print("  Asegúrate de que tu Axe-Fx III esté conectado")


def send_midi_cc(outport, cc, value, pad_info):
    """Envía un mensaje MIDI CC."""
    try:
        msg = mido.Message('control_change', control=cc, value=value)
        outport.send(msg)
        effect_name = pad_info.get('effect', 'N/A')
        print(f"[MIDI] Enviado CC#{cc} (valor {value}) → {effect_name}")
        return True
    except Exception as e:
        print(f"[ERROR] Error enviando mensaje MIDI: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Controlador MIDI Maschine Mikro → Axe-Fx III",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  %(prog)s                    # Usar configuración por defecto
  %(prog)s --port "Axe-Fx"    # Especificar puerto MIDI
  %(prog)s --list-ports       # Listar puertos disponibles
  %(prog)s --mapping config.json  # Usar archivo de mapeo personalizado
        """
    )
    
    parser.add_argument('--port', '-p', 
                       help='Nombre del puerto MIDI de salida (por defecto: "Axe-Fx")')
    parser.add_argument('--mapping', '-m', 
                       help='Archivo de mapeo JSON (por defecto: cc_pad_mapping.json)')
    parser.add_argument('--list-ports', '-l', action='store_true',
                       help='Listar puertos MIDI disponibles y salir')
    parser.add_argument('--version', '-v', action='version', version='2.0.0')
    
    args = parser.parse_args()
    
    # Mostrar banner
    print("🎸 MASCHINE MIKRO → AXE-FX III MIDI CONTROL")
    print("=" * 50)
    
    # Listar puertos si se solicita
    if args.list_ports:
        list_midi_ports()
        return
    
    # Cargar mapeo
    mapping_file = args.mapping or MAPPING_FILE
    mapping = load_mapping(mapping_file)
    pads = mapping.get('pads', {})
    
    if not pads:
        print("[ERROR] No hay pads definidos en el mapeo.")
        sys.exit(1)
    
    print(f"[INFO] Cargado mapeo desde: {mapping_file}")
    print(f"[INFO] Pads configurados: {len(pads)}")
    
    # Encontrar puerto MIDI
    port_hint = args.port or MIDI_PORT_NAME
    port_name = find_midi_output(port_hint)
    print(f"[INFO] Usando puerto MIDI: {port_name}")
    
    # Conectar al puerto MIDI
    try:
        with mido.open_output(port_name) as outport:
            print("\n🎯 Controlador activo. Comandos disponibles:")
            print("  - Número de pad (ej: 5, 6, 7...) para activar efecto")
            print("  - 'list' para ver pads disponibles")
            print("  - 'status' para ver estado actual")
            print("  - 'q' o Ctrl+C para salir")
            print("-" * 50)
            
            while True:
                try:
                    user_input = input("🎹 Pad: ").strip()
                    
                    if user_input.lower() in ['q', 'quit', 'exit']:
                        break
                    
                    if user_input.lower() == 'list':
                        print("\n📋 Pads disponibles:")
                        for pad_num, pad_info in pads.items():
                            effect = pad_info.get('effect', 'N/A')
                            cc = pad_info.get('cc', 'N/A')
                            print(f"  {pad_num}: {effect} (CC#{cc})")
                        continue
                    
                    if user_input.lower() == 'status':
                        print(f"\n📊 Estado:")
                        print(f"  Puerto MIDI: {port_name}")
                        print(f"  Pads configurados: {len(pads)}")
                        print(f"  Archivo de mapeo: {mapping_file}")
                        continue
                    
                    if user_input not in pads:
                        print(f"[WARN] Pad '{user_input}' no está mapeado.")
                        print("[INFO] Usa 'list' para ver pads disponibles")
                        continue
                    
                    pad_info = pads[user_input]
                    cc = pad_info['cc']
                    value = 127  # ON
                    
                    if send_midi_cc(outport, cc, value, pad_info):
                        print(f"✅ Pad {user_input} activado")
                    
                except KeyboardInterrupt:
                    print("\n[INFO] Saliendo...")
                    break
                except EOFError:
                    print("\n[INFO] Saliendo...")
                    break
                    
    except Exception as e:
        print(f"[ERROR] Error conectando al puerto MIDI: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main() 