
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

## COUCOU

import serial
from serial import SerialException
import time
import os
import matplotlib.pyplot as plt

PORT = '/dev/cu.usbmodem34B7DA6494902'
BAUDRATE = 1000000

# ---- Paramètres expérimentaux ----
TRIAL_DURATION = 10.0      # durée d'un essai en secondes
DT = 0.01                  # période de demande d'échantillon (~100 Hz)
NB_TRIALS = 3              # nombre d'essais à enchaîner
PREFIX = "Sujet01"         # préfixe des fichiers
FOLDER = "data"      # dossier de sauvegarde
SHOW_PLOTS = True          # True = affiche un graphe par essai
# ----------------------------------


os.makedirs(FOLDER, exist_ok=True)

for trial in range(1, NB_TRIALS + 1):
    print(f"\n=== Essai T{trial:02d} ===")

    times = []   # temps en secondes (relatifs Arduino)
    values = []  # valeurs calibrées

    # ----- Ouverture du port série -----
    try:
        ser = serial.Serial(PORT, BAUDRATE, timeout=0.1)
    except SerialException as e:
        print("Impossible d'ouvrir le port série :", e)
        break

    time.sleep(2)  # temps pour que la UNO R4 redémarre
    ser.reset_input_buffer()

    print("Envoi 'r' pour démarrer")
    ser.write(b'r')
    ser.flush()

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

                    # Temps Arduino en secondes
                    times.append(t_ms / 1000.0)
                    values.append(val)
                except ValueError:
                    pass

            # Fin d'essai après TRIAL_DURATION secondes (côté PC)
            if time.time() - t0_pc > TRIAL_DURATION:
                ser.write(b'x')   # reset logiciel demandé
                ser.flush()
                break

            time.sleep(DT)

    except KeyboardInterrupt:
        print("Arrêt manuel demandé")
        ser.write(b'x')
        ser.flush()

    # Fermeture du port pour cet essai
    ser.close()
    print("Port fermé pour cet essai")

    # ----- Post-traitement de l'essai -----
    if not times:
        print("Aucune donnée reçue sur cet essai.")
        continue

    # Temps relatif (0 s au début de l'essai)
    t0_rel = times[0]
    times_rel = [t - t0_rel for t in times]

    print(f"T{trial:02d} : {len(times_rel)} échantillons")
    print(f"  t0 = {times_rel[0]:.3f} s, t_end = {times_rel[-1]:.3f} s")
    print(f"  val min = {min(values):.3f}, val max = {max(values):.3f}")

    # ----- Sauvegarde CSV pour cet essai -----
    filename = f"{PREFIX}_T{trial:02d}.csv"
    filepath = os.path.join(FOLDER, filename)

    with open(filepath, "w") as f:
        f.write("time_s,value\n")
        for t, v in zip(times_rel, values):
            f.write(f"{t:.6f},{v:.6f}\n")

    print(f"Fichier enregistré : {filepath}")

    # ----- Graphe temporel (optionnel) -----
    if SHOW_PLOTS:
        plt.figure()
        plt.plot(times_rel, values)
        plt.xlabel("Temps (s)")
        plt.ylabel("Valeur calibrée")
        plt.title(f"Step 7 - Signal jauge (T{trial:02d})")
        plt.grid(True)
        plt.show()

print("\nTous les essais sont terminés.")