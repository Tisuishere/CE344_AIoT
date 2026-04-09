import json

import paho.mqtt.client as mqtt

from db_utils import save_to_db

BROKER_HOST = "127.0.0.1"
BROKER_PORT = 1883
TOPIC = "iot/sensor/data"


def on_connect(client, userdata, flags, rc):
	if rc == 0:
		print("MQTT Server da ket noi broker")
		client.subscribe(TOPIC)
		print(f"Dang lang nghe topic: {TOPIC}")
	else:
		print(f"Ket noi broker that bai, ma loi: {rc}")


def on_message(client, userdata, msg):
	try:
		payload = msg.payload.decode("utf-8")
		data = json.loads(payload)

		device_id = data["device_id"]
		temperature = data["temperature"]
		humidity = data["humidity"]
		timestamp = data["timestamp"]

		save_to_db(device_id, temperature, humidity, "MQTT", timestamp)
		print("Da nhan va luu du lieu MQTT:", data)
	except Exception as e:
		print("Loi xu ly du lieu MQTT:", e)


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER_HOST, BROKER_PORT, 60)
client.loop_forever()
