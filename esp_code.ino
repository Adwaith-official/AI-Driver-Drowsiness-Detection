#include <WiFi.h>
#include <WebServer.h>

// ----------- WiFi Credentials -----------
const char* ssid = "iqoo";
const char* password = "12345678";

// ----------- Web Server -----------
WebServer server(80);

// ----------- LED Pin -----------
const int ledPin = 2;

// ----------- Handlers -----------
// NOTE: Inverted logic for ESP32 built-in LED

void handleLED_ON() {
  digitalWrite(ledPin, LOW);   // ✅ LED ON
  server.send(200, "text/plain", "LED ON");
}

void handleLED_OFF() {
  digitalWrite(ledPin, HIGH);  // ❌ LED OFF
  server.send(200, "text/plain", "LED OFF");
}

// ----------- Setup -----------
void setup() {
  Serial.begin(115200);

  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, HIGH);  // Start with LED OFF

  // Connect to WiFi
  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi");

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nConnected!");
  Serial.print("ESP32 IP Address: ");
  Serial.println(WiFi.localIP());

  // Define routes
  server.on("/led=ON", handleLED_ON);
  server.on("/led=OFF", handleLED_OFF);

  server.begin();
  Serial.println("Server started");
}

// ----------- Loop -----------
void loop() {
  server.handleClient();
}