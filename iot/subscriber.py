"""
IoT Module — MQTT Subscriber + Auto-Irrigation + Max-Heap Scheduler
Receives sensor JSON, computes priority, pushes to Max-Heap,
triggers relay ON command when moisture < 30%.
"""
import json, sys, os
import paho.mqtt.client as mqtt

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from aads.heap import MaxHeap, Task

BROKER        = "localhost"
PORT          = 1883
MOISTURE_LOW  = 30      # % threshold — triggers irrigation
task_heap     = MaxHeap()
task_counter  = 0


def on_connect(client, userdata, flags, rc):
    print(f"[SUBSCRIBER] Connected (rc={rc})")
    client.subscribe("farm/+/zone/+/sensor", qos=1)
    print("[SUBSCRIBER] Subscribed to farm/+/zone/+/sensor")


def on_message(client, userdata, msg):
    global task_counter
    try:
        r    = json.loads(msg.payload.decode())
        zone = r.get("zone", "?")
        mois = r.get("moisture", 50)

        # Push to Max-Heap scheduler
        task_counter += 1
        task = Task(
            task_id       = task_counter,
            task_type     = "Irrigation" if mois < MOISTURE_LOW else "Monitor",
            zone          = f"Zone{zone}",
            moisture      = mois,
            days_until_due= 1 if mois < MOISTURE_LOW else 3,
        )
        task_heap.insert(task)
        print(f"[HEAP]  Inserted {task}  (heap size={task_heap.size()})")

        # Auto-irrigation relay command
        if mois < MOISTURE_LOW:
            cmd   = json.dumps({"relay": "irrigation", "state": "ON", "duration": 300})
            topic = f"farm/{r.get('farm_id',1)}/zone/{zone}/command"
            client.publish(topic, cmd, qos=1)
            print(f"[RELAY] Irrigation ON → {topic}  moisture={mois}%")

    except Exception as e:
        print(f"[ERROR] {e}")


client = mqtt.Client(client_id="python_subscriber")
client.on_connect = on_connect
client.on_message = on_message
client.connect(BROKER, PORT, keepalive=60)

print("[SUBSCRIBER] Waiting for sensor data. Ctrl+C to stop.")
try:
    client.loop_forever()
except KeyboardInterrupt:
    print("[SUBSCRIBER] Stopped.")
