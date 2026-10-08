/*
  Trinetra07 Roadside Node 2 Placeholder
  TODO: Configure local sensing inputs and packet forwarding logic.
*/

void setup() {
  Serial.begin(115200);
  while (!Serial) {
    ;
  }
  Serial.println("[node_2] Placeholder node initialized");
}

void loop() {
  // TODO: Read node sensors and forward summarized data.
  Serial.println("[node_2] Status OK");
  delay(1500);
}
