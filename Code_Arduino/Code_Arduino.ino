bool startLoop = false;

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);    // En attente de commande
  Serial.begin(1000000);          // Doit matcher le Python
  while(!startLoop) {
    if(Serial.available()) {
      startLoop = ((char)(Serial.read()) == 'r');
    }
  }
}

void loop() {
  digitalWrite(LED_BUILTIN, HIGH);
}
