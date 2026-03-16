"""
IoT Module — Sensor Simulator (replaces physical ESP32)
Publishes realistic sensor JSON to MQTT broker every 5 seconds (demo speed).
Topic: farm/1/zone/{zone}/sensor
Requires: pip install paho-mqtt
Requires: Mosquitto broker running on localhost:1883
"""
import json, time, random, math
import paho.mqtt.client as mqtt

BROKER  = "localhost"
PORT    = 1883
ZONES   = ["A", "B", "C", "D"]
FARM_ID = 1

# Simulate gradual moisture drain + temperature cycle
_moisture = {z: random.uniform(35, 70) for z in ZONES}
_hour     = 0


def _simulate_reading(zone: str) -> dict:
    # Moisture slowly drains; occasionally drops fast to trigger irrigation
    _moisture[zone] -= random.uniform(0.3, 1.2)
    if _moisture[zone] < 15:
        _moisture[zone] = random.uniform(55, 75)   # pump refilled

    hour_of_day = (_hour % 24)
    temp        = 22 + 8 * math.sin(math.pi * hour_of_day / 12) + random.gauss(0, 1)
    humidity    = 70 - 0.3 * temp + random.gauss(0, 3)

    return {
        "farm_id":  FARM_ID,
        "zone":     zone,
        "temp":     round(temp, 2),
        "humidity": round(max(20, min(100, humidity)), 2),
        "moisture": round(max(10, min(100, _moisture[zone])), 2),
        "N":        round(random.uniform(60, 120), 1),
        "P":        round(random.uniform(30, 80),  1),
        "K":        round(random.uniform(20, 60),  1),
        "ph":       round(random.uniform(5.5, 7.5), 2),
        "timestamp": time.time(),
    }


def on_connect(client, userdata, flags, rc):
    print(f"[SIMULATOR] Connected to broker (rc={rc})")


client = mqtt.Client(client_id="esp32_simulator")
client.on_connect = on_connect
client.connect(BROKER, PORT, keepalive=60)
client.loop_start()

print("[SIMULATOR] Publishing sensor data every 5 seconds. Ctrl+C to stop.")
try:
    while True:
        _hour += 1
        for zone in ZONES:
            reading = _simulate_reading(zone)
            topic   = f"farm/{FARM_ID}/zone/{zone}/sensor"
            payload = json.dumps(reading)
            client.publish(topic, payload, qos=1)
            print(f"[PUB] {topic} → moisture={reading['moisture']}%  temp={reading['temp']}°C")
        time.sleep(5)
except KeyboardInterrupt:
    print("[SIMULATOR] Stopped.")
    client.loop_stop()
