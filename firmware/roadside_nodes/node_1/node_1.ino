/*
  Trinetra07 Roadside Node 1 Placeholder
  TODO: Configure LoRa module, GPS corrections, and health telemetry.
*/

void setup() {
  Serial.begin(115200);
  while (!Serial) {
    ;
  }
  Serial.println("[node_1] Placeholder node initialized");
}

void loop() {
  // TODO: Publish node status packets at project-defined intervals.
  Serial.println("[node_1] Status OK");
  delay(1500);
}
