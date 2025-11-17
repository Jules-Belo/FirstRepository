## Code nous fonctionnel
```python
import serial
import time

PORT = '/dev/cu.usbmodem34B7DA6494902'
BAUDRATE = 1000000

try:
    print("Ouverture du port série...")
    ser = serial.Serial(
        port=PORT,
        baudrate=BAUDRATE,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=1
    )
except serial.SerialException as e:
    print("Erreur : impossible d'ouvrir le port série :", e)
    exit()

# L'Arduino reset à chaque ouverture → on attend 2 secondes
print("Attente du reboot Arduino...")
time.sleep(2)

try:
    print("Envoi du caractère 'r'...")
    ser.write(b'r')
    ser.flush()
    time.sleep(0.1)  # petite marge pour s'assurer du bon envoi
    print("Commande envoyée.")

except Exception as e:
    print("Erreur lors de l'envoi :", e)

finally:
    ser.close()
    print("Port série fermé.")
``

## Code prof peu fonctionnel
```python
import serial
from serial.serialutil import SerialException

serialPort = serial.Serial();
serialPort.baudrate = 1000000;
serialPort.port = '/dev/cu.usbmodem34B7DA6494902';
serialPort.parity = serial. PARITY_NONE;
serialPort.stopbits = serial.STOPBITS_ONE;
serialPort.bytesize = serial. EIGHTBITS;

try :
    serialPort.open();
except SerialException as serialException:
    print(serialException)

if(not serialPort.isOpen()):
    print('Serial port not opened')
    exit()

try :
    print('Serial port opened. Write run character.')
    cmd = "r";
    serialPort.write(cmd.encode(encoding='ascii'))
    serialPort.close()
    print('Port closed')
except Exception as exception:
    print( 'Exception occurred while writing run character')
    print(exception)
    serialPort.close()
    print('Port Close')
```
