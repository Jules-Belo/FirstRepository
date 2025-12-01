
## COUCOU

import serial
from serial import SerialException
import time

PORT = '/dev/cu.usbmodem34B7DA6494902'
BAUDRATE = 1000000

times = []
values = []

try:
    ser = serial.Serial(PORT, BAUDRATE, timeout=0.1)
except SerialException as e:
    print("Impossible d'ouvrir le port série :", e)
    raise

time.sleep(2)  # laisse le temps à la carte de booter

print("Envoi 'r' pour démarrer")
ser.write(b'r')
ser.flush()

dt = 0.01  # 100 Hz
t0 = time.time()

print("Acquisition en cours ...")

try:
    while True:
        # Demande un échantillon
        ser.write(b'g')
        ser.flush()

        try:
            line = ser.readline().decode(errors='ignore').strip()
        except SerialException as e:
            print("Erreur série pendant la lecture :", e)
            break

        if line and ',' in line:
            try:
                t_str, v_str = line.split(',', 1)
                t_ms = int(t_str)
                val = float(v_str)
                times.append(t_ms / 1000.0)
                values.append(val)
            except ValueError:
                pass

        # Reset après ~10 s
        if time.time() - t0 > 10:
            ser.write(b'x')
            ser.flush()
            break

        time.sleep(dt)

except KeyboardInterrupt:
    print("Arrêt manuel demandé")

finally:
    ser.close()
    print("Port fermé")

# Résumé en dehors de la boucle
if times:
    print(f"t0 = {times[0]:.3f} s, t_end = {times[-1]:.3f} s")
    print(f"val min = {min(values):.3f}, val max = {max(values):.3f}")
else:
    print("Aucune donnée reçue (times[] est vide).")