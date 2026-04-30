import json
import paho.mqtt.client as mqtt
# Giả sử bạn có file db_utils.py để lưu database
# from db_utils import save_forecast_to_db 

BROKER_HOST = "127.0.0.1" # Hoặc "127.0.0.1" nếu chạy local broker
BROKER_PORT = 1883
TOPIC = "ce344/weather_forecast"

def on_connect(client, userdata, flags, reason_code, properties=None):
    if reason_code == 0:
        print("MQTT Server đã kết nối broker thành công")
        client.subscribe(TOPIC)
        print(f"Đang lắng nghe topic: {TOPIC}")
    else:
        print(f"Kết nối thất bại, mã lỗi: {reason_code}")

def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode("utf-8")
        data = json.loads(payload)

        model_name = data.get("model")
        temp_next_hour = data.get("predicted_temperature_next_hour")
        timestamp = data.get("timestamp")

        
        print(f"\n--- Nhận dữ liệu dự báo từ {model_name} ---")
        print(f"Nhiệt độ dự kiến: {temp_next_hour}°C")
        print(f"Thời gian: {timestamp}")
        
    except Exception as e:
        print("Lỗi xử lý dữ liệu MQTT:", e)

client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message

try:
    print(f"Đang khởi động Server tại {BROKER_HOST}...")
    client.connect(BROKER_HOST, BROKER_PORT, 60)
    client.loop_forever()
except Exception as e:
    print(f"Không thể khởi động Server: {e}")