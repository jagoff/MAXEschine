import mido
import time

MASCHINE_OUTPUT_NAME = 'Maschine Mikro Output'

# CC y notas típicos de la barra lateral (prueba ambos)
LATERAL_CCS = [16, 17, 18, 19, 112, 113, 114, 115, 116, 117, 118, 119]
LATERAL_NOTES = [36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47]

# Prueba canales 0 y 1
CHANNELS = [0, 1]

# Mensaje SysEx de ejemplo (puede requerir ajuste para Maschine)
# Este es un placeholder, la Maschine puede requerir un formato específico
SYSEX_EXAMPLE = [0xF0, 0x7F, 0x7F, 0x04, 0x01, 0xF7]

def find_port(name, ports):
    for port in ports:
        if name.lower() in port.lower():
            return port
    return None

def main():
    output_ports = mido.get_output_names()
    maschine_output = find_port(MASCHINE_OUTPUT_NAME, output_ports)
    if not maschine_output:
        print(f"No se encontró el puerto de salida: {MASCHINE_OUTPUT_NAME}")
        print("Puertos disponibles:")
        for port in output_ports:
            print(f"  - {port}")
        return
    print(f"Usando puerto: {maschine_output}")
    with mido.open_output(maschine_output) as outport:
        print("\nProbando control_change en canales 0 y 1...")
        for ch in CHANNELS:
            for cc in LATERAL_CCS:
                print(f"CC {cc} ON (canal {ch+1})")
                outport.send(mido.Message('control_change', channel=ch, control=cc, value=127))
                time.sleep(0.3)
                print(f"CC {cc} OFF (canal {ch+1})")
                outport.send(mido.Message('control_change', channel=ch, control=cc, value=0))
                time.sleep(0.1)
        print("\nProbando note_on en canales 0 y 1...")
        for ch in CHANNELS:
            for note in LATERAL_NOTES:
                print(f"Note {note} ON (canal {ch+1})")
                outport.send(mido.Message('note_on', channel=ch, note=note, velocity=127))
                time.sleep(0.3)
                print(f"Note {note} OFF (canal {ch+1})")
                outport.send(mido.Message('note_on', channel=ch, note=note, velocity=0))
                time.sleep(0.1)
        print("\nProbando SysEx...")
        try:
            outport.send(mido.Message('sysex', data=SYSEX_EXAMPLE))
            print("SysEx enviado (puede requerir ajuste para Maschine)")
        except Exception as e:
            print(f"Error enviando SysEx: {e}")
    print("\nTest finalizado. Observa qué mensajes encienden/apagan los LEDs de la barra lateral.")

if __name__ == "__main__":
    main() 