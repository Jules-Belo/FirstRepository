#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import serial
import time

PORT = '/dev/cu.usbmodem34B7DA6494902'
BAUDRATE = 1000000

ser = serial.Serial(PORT, BAUDRATE, timeout=0.1)
time.sleep(2)  # laisse le temps au reset Arduino

print("Envoi 'r' pour démarrer")
ser.write(b'r')
ser.flush()

dt = 0.01  # 100 Hz

times = []   # en secondes
values = []  # optionnel : pour le FSR

t0 = time.time()
print("Acquisition en cours ...")

try:
    while True:
        # Demande un échantillon
        ser.write(b'g')
        ser.flush()

        line = ser.readline().decode(errors='ignore').strip()
        if line and ',' in line:
            # On attend "time_ms,value"
            try:
                t_str, v_str = line.split(',', 1)
                t_ms = int(t_str)
                value = int(v_str)

                # Stockage en secondes
                times.append(t_ms / 1000.0)
                values.append(value)
            except ValueError:
                # ligne non valide -> on ignore à ce step
                pass

        # RESET après ~10 s
        if time.time() - t0 > 10:
            ser.write(b'x')   # demande de reset logiciel
            ser.flush()
            break

        time.sleep(dt)

except KeyboardInterrupt:
    print("Arrêt manuel demandé")
    # on pourrait envoyer 'x' ou pas, au choix

ser.close()
print("Port fermé")

# Résumé (hors boucle, donc ça ne gêne pas le timing)
print(f"Step 4 terminé : {len(times)} échantillons reçus.")
if times:
    print(f"Premier temps : {times[0]:.3f} s, dernier temps : {times[-1]:.3f} s")