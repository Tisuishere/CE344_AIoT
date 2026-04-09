import socket
import json
from db_utils import save_to_db

HOST = "0.0.0.0"
PORT = 5001

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(5)

print(f"TCP Server dang lang nghe tai {HOST}:{PORT}")

while True:
    conn, addr = server.accept()
    print(f"Ket noi tu {addr}")
    data = conn.recv(1024).decode("utf-8")
    if data:
        try:
            msg = json.loads(data)
            device_id = msg["device_id"]
            temperature = msg["temperature"]
            humidity = msg["humidity"]
            timestamp = msg["timestamp"]

            save_to_db(device_id, temperature, humidity, "TCP", timestamp)

            print("Da nhan va luu du lieu TCP:", msg)
            conn.send("Da luu du lieu TCP".encode("utf-8"))
        except Exception as e:
            print("Loi xu ly du lieu TCP:", e)

    conn.close()
