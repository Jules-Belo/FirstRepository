bool startLoop = false;

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, HIGH);   // HIGH = en attente

  Serial.begin(1000000, SERIAL_8N1);
  Serial.println("Ready. Waiting for 'r'...");
  
  while (!startLoop) {
    if (Serial.available()) {
      char c = (char)Serial.read();
      if (c == 'r' || c == 'R') {
        startLoop = true;
        Serial.println("Start command received.");
        digitalWrite(LED_BUILTIN, LOW);   // ON passe en mode acquisition
      }
    }
  }
}

void loop() {
  // Pour l’instant : on ne fait que confirmer qu’on est dans loop()
  digitalWrite(LED_BUILTIN, LOW);
}
