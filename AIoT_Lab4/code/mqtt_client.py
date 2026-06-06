import paho.mqtt.client as mqtt
import json
import pandas as pd
import time
from datetime import datetime
from config import OUTPUT_DIR

# Cấu hình MQTT Broker
BROKER = "127.0.0.1"
PORT = 1883
TOPIC = "iot/anomaly/temperature"

def main():
    # Khởi tạo MQTT Client
    client = mqtt.Client(client_id="AnomalyDetectionClient")
    
    # Kết nối tới Broker
    print(f"Dang ket noi toi {BROKER}:{PORT}...")
    try:
        client.connect(BROKER, PORT, 60)
        print("Ket noi thanh cong!")
    except Exception as e:
        print(f"Khong the ket noi toi MQTT Broker: {e}")
        return

    # Khởi động loop dưới nền để giữ kết nối
    client.loop_start()

    # Đọc dữ liệu từ file kết quả Isolation Forest (hoặc file khác tùy chọn)
    result_file = OUTPUT_DIR / "iforest_results.csv"
    if not result_file.exists():
        print(f"Khong tim thay file ket qua: {result_file}")
        return

    print(f"Dang doc du lieu tu {result_file}...")
    df = pd.read_csv(result_file)

    # Lọc ra chỉ những điểm bất thường
    anomalies = df[df["pred_iforest"] == 1]
    
    print(f"Tim thay {len(anomalies)} diem bat thuong. Bat dau gui canh bao...")

    for index, row in anomalies.iterrows():
        # Đóng gói dữ liệu thành JSON
        payload = {
            "timestamp": str(row["timestamp"]),
            "temperature": round(row["temperature"], 2),
            "model": "Isolation Forest",
            "anomaly_score": round(row["iforest_score"], 4) if "iforest_score" in row else None,
            "message": "Nhiet do vuot muc binh thuong hoac co hanh vi bat thuong!"
        }
        
        json_payload = json.dumps(payload)
        
        # Publish lên topic
        client.publish(TOPIC, json_payload)
        print(f"[{datetime.now()}] Da gui canh bao: {json_payload}")
        
        # Dừng 1 chút để mô phỏng thời gian thực
        time.sleep(2)

    print("Hoan thanh gui canh bao.")
    client.loop_stop()
    client.disconnect()

if __name__ == "__main__":
    main()
