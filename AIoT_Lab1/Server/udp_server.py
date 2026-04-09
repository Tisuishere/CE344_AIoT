import json
import socket

from db_utils import save_to_db

HOST = "0.0.0.0"
PORT = 5002

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind((HOST, PORT))

print(f"UDP Server dang lang nghe tai {HOST}:{PORT}")

while True:
	data, addr = server.recvfrom(1024)
	text = data.decode("utf-8")

	if text:
		try:
			msg = json.loads(text)
			device_id = msg["device_id"]
			temperature = msg["temperature"]
			humidity = msg["humidity"]
			timestamp = msg["timestamp"]

			save_to_db(device_id, temperature, humidity, "UDP", timestamp)

			print("Da nhan va luu du lieu UDP:", msg)
			server.sendto("Da luu du lieu UDP".encode("utf-8"), addr)
		except Exception as e:
			print("Loi xu ly du lieu UDP:", e)
			server.sendto("Du lieu UDP khong hop le".encode("utf-8"), addr)
