import hid
import sys
import time

VENDOR_ID = 0x17cc  # Native Instruments
PRODUCT_ID = 0x1110  # Maschine Mikro MK1

LED_BUFFER_SIZE = 41  # MK1: 16 pads + laterales + otros
PAD_IDX = {pad: (pad - 1) for pad in range(1, 17)}  # Pads 1-16, bytes 0-15
LATERAL_IDX = {1: 32, 2: 33, 3: 34, 4: 35}  # Ejemplo: botones laterales en bytes 32-35

# Intensidades típicas
INTENSITIES = {
    'off': 0,
    'low': 32,
    'med': 64,
    'high': 127,
    'on': 127,
}

def set_pad(buffer, pad, intensity):
    idx = PAD_IDX.get(pad)
    if idx is not None:
        buffer[idx] = INTENSITIES.get(intensity, 0)

def set_lateral(buffer, button, on):
    idx = LATERAL_IDX.get(button)
    if idx is not None:
        buffer[idx] = 127 if on else 0

def main():
    print("Dispositivos HID detectados:")
    for d in hid.enumerate():
        print(d)
    if len(sys.argv) < 3:
        print("Uso: python maschine_hid_led.py pad|lateral <num> <on|off|low|med|high>")
        print("Ejemplo: python maschine_hid_led.py pad 1 high")
        print("         python maschine_hid_led.py lateral 2 on")
        return
    led_type = sys.argv[1]
    num = int(sys.argv[2])
    value = sys.argv[3]
    buffer = bytearray([0] * LED_BUFFER_SIZE)
    if led_type == 'pad':
        set_pad(buffer, num, value)
    elif led_type == 'lateral':
        set_lateral(buffer, num, value == 'on' or value == 'high')
    else:
        print("Tipo de LED desconocido")
        return
    try:
        print("Intentando abrir con hid.device()...")
        dev = hid.device()
        dev.open(VENDOR_ID, PRODUCT_ID)
        dev.write([0x00] + list(buffer))
        print(f"Enviado (hid.device): {led_type} {num} {value}")
        time.sleep(0.2)
        dev.close()
        return
    except Exception as e:
        print(f"hid.device() falló: {e}")
    try:
        print("Intentando abrir con hid.Device()...")
        with hid.Device(VENDOR_ID, PRODUCT_ID) as dev2:
            dev2.write([0x00] + list(buffer))
            print(f"Enviado (hid.Device): {led_type} {num} {value}")
            time.sleep(0.2)
        return
    except Exception as e:
        print(f"hid.Device() falló: {e}")
    print("No se pudo abrir el dispositivo HID con ninguna API. Revisa la instalación de hidapi y los permisos.")

if __name__ == "__main__":
    main() 