#include <WiFi.h>
#include <PubSubClient.h>

// WiFi credentials
const char* ssid = "<Wi-Fi_Name>";
const char* password = "<password>";

// MQTT broker (your laptop's IP)
const char* mqtt_server = "<IP of mqtt msg sending device>";
const int mqtt_port = 1883;
const char* mqtt_topic = "test";

WiFiClient espClient;
PubSubClient client(espClient);

// Built-in LED pin
const int ledPin = 2;

// Callback to handle received MQTT messages
void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message arrived on topic: ");
  Serial.println(topic);

  String message;
  for (unsigned int i = 0; i < length; i++) {
    message += (char)payload[i];
  }

  Serial.print("Payload: ");
  Serial.println(message);

  // Check if payload contains "on" or "off"
  if (message=="on") {
    digitalWrite(ledPin, HIGH);
    Serial.println("LED ON");
  } else if (message=="off") {
    digitalWrite(ledPin, LOW);
    Serial.println("LED OFF");
  } else {
    Serial.println("Invalid state received");
  }
}

void reconnect() {
  while (!client.connected()) {
    Serial.print("Connecting to MQTT broker...");
    if (client.connect("ESP32Client")) {
      Serial.println("Connected!");
      client.subscribe(mqtt_topic);
    } else {
      Serial.print("Failed. State=");
      Serial.print(client.state());
      Serial.println(" Retrying in 5 seconds...");
      delay(5000);
    }
  }
}

void setup() {
  Serial.begin(115200);

  pinMode(ledPin, OUTPUT);  // Setup LED pin

  WiFi.begin(ssid, password);
  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi connected");

  client.setServer(mqtt_server, mqtt_port);
  client.setCallback(callback);
}

void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();  // Required for MQTT to work
}
