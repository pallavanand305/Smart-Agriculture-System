// ============================================================
// Smart Agriculture — ESP32 Firmware
// Reads DHT22 (temp/humidity) + ADC (soil moisture) + NPK
// Publishes JSON to MQTT broker via Wi-Fi
// Subscribes to command topic for relay (irrigation pump) control
// ============================================================
#include <WiFi.h>
#include <PubSubClient.h>
#include <DHT.h>
#include <ArduinoJson.h>

// ── Pin definitions ──────────────────────────────────────────
#define DHT_PIN       4       // DHT22 data pin
#define MOISTURE_PIN  34      // Capacitive soil moisture (ADC)
#define RELAY_PIN     26      // Relay module — irrigation pump
#define DHT_TYPE      DHT22

// ── Network & MQTT config ────────────────────────────────────
const char* WIFI_SSID     = "FarmNet";
const char* WIFI_PASS     = "agri2024";
const char* MQTT_BROKER   = "192.168.1.100";
const int   MQTT_PORT     = 1883;
const char* SENSOR_TOPIC  = "farm/1/zone/A/sensor";
const char* COMMAND_TOPIC = "farm/1/zone/A/command";

DHT          dht(DHT_PIN, DHT_TYPE);
WiFiClient   espClient;
PubSubClient mqtt(espClient);

// ── Setup ────────────────────────────────────────────────────
void setup() {
    Serial.begin(115200);
    dht.begin();
    pinMode(RELAY_PIN, OUTPUT);
    digitalWrite(RELAY_PIN, LOW);

    // Connect Wi-Fi
    WiFi.begin(WIFI_SSID, WIFI_PASS);
    Serial.print("Connecting to Wi-Fi");
    while (WiFi.status() != WL_CONNECTED) { delay(500); Serial.print("."); }
    Serial.println("\nWi-Fi connected: " + WiFi.localIP().toString());

    // Connect MQTT
    mqtt.setServer(MQTT_BROKER, MQTT_PORT);
    mqtt.setCallback(onCommand);
    reconnect();
}

// ── Main loop ────────────────────────────────────────────────
void loop() {
    if (!mqtt.connected()) reconnect();
    mqtt.loop();

    float temp     = dht.readTemperature();
    float humidity = dht.readHumidity();

    // Map ADC (4095=dry, 1500=wet) to 0-100%
    int   raw      = analogRead(MOISTURE_PIN);
    float moisture = map(raw, 4095, 1500, 0, 100);
    moisture       = constrain(moisture, 0, 100);

    // Build JSON payload
    StaticJsonDocument<256> doc;
    doc["farm_id"]  = 1;
    doc["zone"]     = "A";
    doc["temp"]     = temp;
    doc["humidity"] = humidity;
    doc["moisture"] = moisture;
    doc["N"]        = 80;   // Replace with actual NPK sensor read
    doc["P"]        = 42;
    doc["K"]        = 45;
    doc["ph"]       = 6.5;

    char payload[256];
    serializeJson(doc, payload);
    mqtt.publish(SENSOR_TOPIC, payload, true);
    Serial.println("Published: " + String(payload));

    delay(300000);   // publish every 5 minutes
}

// ── MQTT command callback ────────────────────────────────────
void onCommand(char* topic, byte* msg, unsigned int len) {
    StaticJsonDocument<128> cmd;
    deserializeJson(cmd, msg, len);
    String state    = cmd["state"];
    int    duration = cmd["duration"] | 300;

    if (state == "ON") {
        digitalWrite(RELAY_PIN, HIGH);
        Serial.println("[RELAY] Irrigation ON for " + String(duration) + "s");
        delay(duration * 1000UL);
        digitalWrite(RELAY_PIN, LOW);
        Serial.println("[RELAY] Irrigation OFF");
    } else {
        digitalWrite(RELAY_PIN, LOW);
    }
}

// ── Reconnect helper ─────────────────────────────────────────
void reconnect() {
    while (!mqtt.connected()) {
        Serial.print("Connecting to MQTT...");
        if (mqtt.connect("ESP32_ZoneA")) {
            Serial.println("connected");
            mqtt.subscribe(COMMAND_TOPIC);
        } else {
            Serial.print("failed rc="); Serial.println(mqtt.state());
            delay(3000);
        }
    }
}
