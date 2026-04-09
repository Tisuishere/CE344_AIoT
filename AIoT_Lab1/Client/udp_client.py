import json
import random
import socket
from datetime import datetime

HOST = "127.0.0.1"  # doi thanh IP server neu can
PORT = 5002

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

data = {
	"device_id": "sensor_udp",
	"temperature": round(random.uniform(25.0, 35.0), 2),
	"humidity": round(random.uniform(50.0, 80.0), 2),
	"timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
}

client.sendto(json.dumps(data).encode("utf-8"), (HOST, PORT))
response, _ = client.recvfrom(1024)
print("Phan hoi tu server:", response.decode("utf-8"))

client.close()
