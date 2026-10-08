/*
  Trinetra07 Vehicle Unit Placeholder
  TODO: Wire real sensors, map GPIOs, and replace placeholder telemetry.
*/

void setup() {
  Serial.begin(115200);
  while (!Serial) {
    ;
  }
  Serial.println("[vehicle_unit] Placeholder firmware initialized");
}

void loop() {
  // TODO: Replace with real sensor acquisition + LoRa transmission.
  Serial.println("[vehicle_unit] Heartbeat");
  delay(1000);
}
