bool started = false;
unsigned long t0 = 0;

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, HIGH);   // attente

  Serial.begin(1000000, SERIAL_8N1);
  Serial.println("Ready. Waiting for 'r'...");
}

void loop() {

  // Lecture de commande
  if (Serial.available()) {
    char c = (char)Serial.read();

    if (!started && (c == 'r' || c == 'R')) {
      started = true;
      t0 = millis();
      digitalWrite(LED_BUILTIN, LOW);
      Serial.println("Start command received.");
    }

    // Commande de demande d'échantillon
    if (started && c == 'g') {
      unsigned long t = millis() - t0;
      Serial.println(t);
    }
  }
}
