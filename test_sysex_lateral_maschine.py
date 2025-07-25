import mido
import time

MASCHINE_OUTPUT_NAME = 'Maschine Mikro Output'

# Mensaje SysEx de ejemplo (ajustar según respuesta)
SYSEX_EXAMPLES = [
    [0xF0, 0x47, 0x7F, 0x43, 0x65, 0x00, 0x01, 0x01, 0x00, 0x01, 0xF7],
    [0xF0, 0x47, 0x7F, 0x43, 0x65, 0x00, 0x01, 0x01, 0x00, 0x00, 0xF7],
    [0xF0, 0x47, 0x7F, 0x43, 0x65, 0x00, 0x01, 0x01, 0x00, 0x7F, 0xF7],
]

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
        for idx, sysex in enumerate(SYSEX_EXAMPLES):
            print(f"Enviando SysEx ejemplo {idx+1}: {sysex}")
            outport.send(mido.Message('sysex', data=sysex[1:-1]))  # mido no requiere F0/F7
            time.sleep(1)
    print("\nTest finalizado. Observa si algún LED lateral responde a los mensajes SysEx.")

if __name__ == "__main__":
    main() 