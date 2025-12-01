#include <avr/wdt.h>

bool started = false;
unsigned long t0 = 0;

#define FORCE_SENSOR_PIN A0  // FSR sur A0

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, HIGH);   // attente

  Serial.begin(1000000, SERIAL_8N1);
  Serial.println("Ready. Waiting for 'r'...");
}

void loop() {

  if (Serial.available()) {
    char c = (char)Serial.read();

    // ----- START -----
    if (!started && (c == 'r' || c == 'R')) {
      started = true;
      t0 = millis();
      digitalWrite(LED_BUILTIN, LOW);
      Serial.println("Start command received.");
      Serial.flush();
    }

    // ----- GET SAMPLE -----
    if (started && c == 'g') {

      unsigned long t = millis() - t0;     // comptage temporel en ms
      int raw = analogRead(FORCE_SENSOR_PIN);

      // Buffer texte pour sprintf
      char buffer[32];
      // Format "time_ms,value"
      sprintf(buffer, "%lu,%d", t, raw);

      Serial.println(buffer);
      Serial.flush();   // on force l'envoi immédiat
    }

    // ----- SOFTWARE RESET -----
    if (c == 'x') {
      Serial.println("Software reset requested...");
      Serial.flush();

      // Active un reset watchdog immédiat
      wdt_enable(WDTO_15MS);
      while (1) {}  // boucle pour déclencher le reset
    }
  }
}
