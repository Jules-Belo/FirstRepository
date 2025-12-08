
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

## COUCOU

import serial
from serial import SerialException
import time
import matplotlib.pyplot as plt

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
t0_pc = time.time()

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

                # Temps relatif envoyé par l'Arduino (en secondes)
                times.append(t_ms / 1000.0)
                values.append(val)
            except ValueError:
                pass

        # Reset après ~10 s
        if time.time() - t0_pc > 10:
            ser.write(b'x')
            ser.flush()
            break

        time.sleep(dt)

except KeyboardInterrupt:
    print("Arrêt manuel demandé")

finally:
    ser.close()
    print("Port fermé")

# -----------------------------
#   RÉSUMÉ + TRAÇAGE + SAVE
# -----------------------------
if not times:
    print("Aucune donnée reçue (times[] est vide).")
else:
    # On rend le temps relatif au début de l'essai
    t0_rel = times[0]
    times_rel = [t - t0_rel for t in times]

    print(f"t0 = {times_rel[0]:.3f} s, t_end = {times_rel[-1]:.3f} s")
    print(f"val min = {min(values):.3f}, val max = {max(values):.3f}")

    # ---- 1) Affichage du signal (graphe temporel) ----
    plt.figure()
    plt.plot(times_rel, values)
    plt.xlabel("Temps (s)")
    plt.ylabel("Valeur calibrée")
    plt.title("Step 6 - Signal jauge de contrainte")
    plt.grid(True)
    plt.show()

    # ---- 2) Enregistrement dans un fichier ----
    filename = "step6_signal.csv"
    with open(filename, "w") as f:
        f.write("time_s,value\n")
        for t, v in zip(times_rel, values):
            f.write(f"{t:.6f},{v:.6f}\n")

    print(f"Fichier enregistré : {filename}")