bool started = false;
unsigned long t0 = 0;

#define GAUGE_PIN A0

// Calibration (à ajuster)
const int OFFSET = 512;
const float GAIN = 0.005f;

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, HIGH);

  Serial.begin(1000000);
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

      unsigned long t = millis() - t0;
      int raw = analogRead(GAUGE_PIN);

      float calibrated = (raw - OFFSET) * GAIN;

      char buffer[32];
      sprintf(buffer, "%lu,%.3f", t, calibrated);

      Serial.println(buffer);
      Serial.flush();
    }

    // ----- SOFTWARE RESET (UNO R4) -----
    if (c == 'x') {
      Serial.println("Software reset requested...");
      Serial.flush();
      NVIC_SystemReset();   // reset matériel Cortex-M
    }
  }
}
