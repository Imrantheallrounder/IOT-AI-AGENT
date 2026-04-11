// #include <WiFi.h>
#include <ESP8266WiFi.h>
#include <PubSubClient.h>

// WiFi credentials
const char* ssid = "Wi-Fi";
const char* password = "92461";

// MQTT broker (your laptop's IP)
const char* mqtt_server = "192.168.X.X";

const int mqtt_port = 1884;
const char* mqtt_topic = "bedroom";

const char* bulb_1  = "bulb-001";
const char* bulb_2  = "bulb-002";

WiFiClient espClient;
PubSubClient client(espClient);

// Built-in LED pin
// const int ledPin_1 = 2;
#define ledPin_1 D0
#define ledPin_2 D4

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


  // --- Parse key and value from {'bulb-001': 'on'} ---
  // Extract key: between first ' and second '
  int keyStart = message.indexOf('\'') + 1;
  int keyEnd   = message.indexOf('\'', keyStart);
  String key   = message.substring(keyStart, keyEnd);

  // Extract value: between third ' and fourth '
  int valStart = message.indexOf('\'', keyEnd + 1) + 1;
  int valEnd   = message.indexOf('\'', valStart);
  String value = message.substring(valStart, valEnd);

  Serial.print("Key: ");   Serial.println(key);
  Serial.print("Value: "); Serial.println(value);

  // --- Only act if this message is meant for this device ---
  if (key == String(bulb_1)) {
    if (value=="on") {
      digitalWrite(ledPin_1, HIGH);
      Serial.println("LED ON");
    } else if (value=="off") {
      digitalWrite(ledPin_1, LOW);
      Serial.println("LED OFF");
    } else {
      Serial.println("Invalid state received");
    }
  }
  if (key == String(bulb_2)) {
    if (value=="on") {
      digitalWrite(ledPin_2, HIGH);
      Serial.println("LED ON");
    } else if (value=="off") {
      digitalWrite(ledPin_2, LOW);
      Serial.println("LED OFF");
    } else {
      Serial.println("Invalid state received");
    }
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

  pinMode(ledPin_1, OUTPUT);  // Setup LED pin
  pinMode(ledPin_2, OUTPUT);  // Setup LED pin

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
