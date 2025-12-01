

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import serial
import time

PORT = '/dev/cu.usbmodem34B7DA6494902'
BAUDRATE = 1000000

ser = serial.Serial(PORT, BAUDRATE, timeout=0.1)
time.sleep(2)

print("Envoi 'r' pour démarrer")
ser.write(b'r')
ser.flush()

# Acquisition 100 Hz = 10 ms
dt = 0.01  # 10 ms

print("Acquisition en cours...")
try:
    while True:
        ser.write(b'g')   # demande un échantillon
        ser.flush()

        line = ser.readline().decode(errors='ignore').strip()
        if line:
            print("Arduino >", line)

        time.sleep(dt)

except KeyboardInterrupt:
    print("Arrêt demandé")

ser.close()
print("Port fermé")
