/*
  TRINETRA - LoRa ping-pong range test (ESP32 + SX127x)

  Flash the same sketch to two boards:
    - Board 1: IS_INITIATOR = true   (sends PING, waits for PONG)
    - Board 2: IS_INITIATOR = false  (waits for PING, replies PONG)

  Both boards print RSSI and SNR of every packet received.
  Library: "LoRa" by Sandeep Mistry
*/

#include <SPI.h>
#include <LoRa.h>

// ---- CHECK THESE AGAINST YOUR WIRING ----
#define LORA_SCK   18
#define LORA_MISO  19
#define LORA_MOSI  23
#define LORA_SS    5
#define LORA_RST   14
#define LORA_DIO0  26
#define LORA_FREQ  433E6      // match your module and local regulations
// -----------------------------------------

#define IS_INITIATOR   true
#define REPLY_TIMEOUT  1000   // ms the initiator waits for a PONG
#define PING_INTERVAL  2000   // ms between pings

uint32_t counter = 0;

void sendPacket(const String &msg) {
  LoRa.beginPacket();
  LoRa.print(msg);
  LoRa.endPacket();
}

// Returns true and fills msg if a packet arrives within timeoutMs
bool receivePacket(String &msg, uint32_t timeoutMs) {
  uint32_t start = millis();
  while (millis() - start < timeoutMs) {
    int size = LoRa.parsePacket();
    if (size) {
      msg = "";
      while (LoRa.available()) msg += (char)LoRa.read();
      return true;
    }
    delay(2);
  }
  return false;
}

void logPacket(const String &msg) {
  Serial.printf("RX \"%s\"  RSSI: %d dBm  SNR: %.1f dB\n",
                msg.c_str(), LoRa.packetRssi(), LoRa.packetSnr());
}

void setup() {
  Serial.begin(115200);
  delay(500);

  SPI.begin(LORA_SCK, LORA_MISO, LORA_MOSI, LORA_SS);
  LoRa.setPins(LORA_SS, LORA_RST, LORA_DIO0);

  if (!LoRa.begin(LORA_FREQ)) {
    Serial.println("LoRa init failed - check wiring and antenna");
    while (true) delay(1000);
  }

  LoRa.setSpreadingFactor(7);
  LoRa.setSignalBandwidth(125E3);
  LoRa.setCodingRate4(5);

  Serial.println(IS_INITIATOR ? "LoRa ready (initiator)" : "LoRa ready (responder)");
}

void loop() {
  String msg;

  if (IS_INITIATOR) {
    counter++;
    sendPacket("PING " + String(counter));
    Serial.printf("TX PING %lu\n", (unsigned long)counter);

    if (receivePacket(msg, REPLY_TIMEOUT)) {
      logPacket(msg);
    } else {
      Serial.println("No reply (timeout)");
    }
    delay(PING_INTERVAL);
  } else {
    if (receivePacket(msg, 5000)) {
      logPacket(msg);
      if (msg.startsWith("PING ")) {
        sendPacket("PONG " + msg.substring(5));
        Serial.println("TX PONG");
      }
    }
  }
}
