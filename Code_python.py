

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import serial
from serial.serialutil import SerialException
import time

PORT = '/dev/cu.usbmodem34B7DA6494902'
BAUDRATE = 1000000

try:
    ser = serial.Serial(PORT, BAUDRATE, timeout=0.1)
except SerialException as e:
    print("Erreur ouverture port :", e)
    exit()

if not ser.is_open:
    print("Port non ouvert")
    exit()

print("Port ouvert, envoi de 'r'")
ser.write(b'r')
ser.flush()

t0 = time.time()
while time.time() - t0 < 2.0:
    line = ser.readline().decode(errors='ignore').strip()
    if line:
        print("Arduino >", line)

ser.close()
print("Port fermé")
