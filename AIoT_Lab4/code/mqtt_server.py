import paho.mqtt.client as mqtt
import json
from datetime import datetime

# Cấu hình MQTT Broker
BROKER = "127.0.0.1"
PORT = 1883
TOPIC = "iot/anomaly/temperature"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"[{datetime.now()}] Ket noi thanh cong toi MQTT Broker!")
        # Đăng ký lắng nghe topic
        client.subscribe(TOPIC)
        print(f"[{datetime.now()}] Dang lang nghe tren topic: {TOPIC}")
    else:
        print(f"[{datetime.now()}] Loi ket noi, ma loi: {rc}")

def on_message(client, userdata, msg):
    try:
        # Giải mã payload từ JSON
        payload = msg.payload.decode("utf-8")
        data = json.loads(payload)
        
        print("\n" + "="*50)
        print(f"🚨 NHAN DUOC CANH BAO BAT THUONG! 🚨")
        print(f"Topic: {msg.topic}")
        print(f"Thoi gian: {data.get('timestamp')}")
        print(f"Nhiet do: {data.get('temperature')} F")
        print(f"Mo hinh phat hien: {data.get('model')}")
        print(f"Thong diep: {data.get('message')}")
        print("="*50 + "\n")
    except Exception as e:
        print(f"Loi xu ly tin nhan: {e}")

def main():
    # Khởi tạo MQTT Client
    client = mqtt.Client(client_id="AnomalyAlertServer")
    
    # Gán các hàm callback
    client.on_connect = on_connect
    client.on_message = on_message
    
    # Kết nối tới Broker
    print(f"Dang ket noi toi {BROKER}:{PORT}...")
    client.connect(BROKER, PORT, 60)
    
    # Vòng lặp lắng nghe liên tục
    try:
        client.loop_forever()
    except KeyboardInterrupt:
        print("\nDa dung server.")
        client.disconnect()

if __name__ == "__main__":
    main()
