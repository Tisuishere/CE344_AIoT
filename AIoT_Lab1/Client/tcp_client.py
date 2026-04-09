import socket
import json
import random
from datetime import datetime

HOST = "127.0.0.1"   
PORT = 5001

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

data = {
    "device_id": "sensor_tcp",
    "temperature": round(random.uniform(25.0, 35.0), 2),
    "humidity": round(random.uniform(50.0, 80.0), 2),
    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
}

client.send(json.dumps(data).encode("utf-8"))

response = client.recv(1024).decode("utf-8")
print("Phan hoi tu server:", response)
