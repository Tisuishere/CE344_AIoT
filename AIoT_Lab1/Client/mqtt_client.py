import json
import random
from datetime import datetime

import paho.mqtt.client as mqtt

BROKER_HOST = "127.0.0.1"
BROKER_PORT = 1883
TOPIC = "iot/sensor/data"

data = {
	"device_id": "sensor_mqtt",
	"temperature": round(random.uniform(25.0, 35.0), 2),
	"humidity": round(random.uniform(50.0, 80.0), 2),
	"timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
}

client = mqtt.Client()
client.connect(BROKER_HOST, BROKER_PORT, 60)
client.publish(TOPIC, json.dumps(data))
print("Da gui du lieu MQTT:", data)
client.disconnect()
