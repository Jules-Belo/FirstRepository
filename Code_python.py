

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

dt = 0.01  # 100 Hz
t0 = time.time()

print("Acquisition en cours...")
try:
    while True:
        ser.write(b'g')
        ser.flush()

        line = ser.readline().decode(errors='ignore').strip()
        if line:
            print("Arduino >", line)

        # RESET 10s
        if time.time() - t0 > 10:
            print("Envoi du reset 'x'")
            ser.write(b'x')
            ser.flush()
            break

        time.sleep(dt)

except KeyboardInterrupt:
    print("Arrêt manuel")

ser.close()
print("Port fermé")