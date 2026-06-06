import numpy as np
import pickle
import json
import joblib
from pathlib import Path
import matplotlib
matplotlib.use('Agg')  # Chế độ không hiển thị cửa sổ biểu đồ
import matplotlib.pyplot as plt
from datetime import datetime
import paho.mqtt.client as mqtt

BROKER_HOST = "127.0.0.1" 
BROKER_PORT = 1883
TOPIC = "ce344/weather_forecast"

def inverse_temperature(scaled_temp, scaler):
    """Chuyển đổi nhiệt độ từ dạng chuẩn hóa về đơn vị gốc (°C)"""
    temp_dummy = np.zeros((len(scaled_temp), 3))
    temp_dummy[:, 0] = scaled_temp.flatten()
    restored = scaler.inverse_transform(temp_dummy)
    return restored[:, 0]

def send_prediction_mqtt(data_payload):
    """Gửi dữ liệu lên MQTT Broker theo kiến trúc Publisher/Subscriber"""
    client = mqtt.Client(callback_api_version=mqtt.CallbackAPIVersion.VERSION2)
    try:
        client.connect(BROKER_HOST, BROKER_PORT, 60)
        client.publish(TOPIC, json.dumps(data_payload, ensure_ascii=False))
        print(f"Đã gửi dữ liệu dự báo lên {BROKER_HOST}: {data_payload['predicted_temperature_next_hour']}°C")
        client.disconnect()
        return True
    except Exception as e:
        print(f"Lỗi gửi MQTT: {e}")
        return False

if __name__ == "__main__":
    print("Bắt đầu dự đoán và Publish dữ liệu AIoT...\n")
    
    try:
        data = np.load('processed/weather_sequences.npz')
        X_test, y_test = data['X_test'], data['y_test']
        with open('processed/scaler.pkl', 'rb') as f:
            scaler = pickle.load(f)
        
        y_test_real = inverse_temperature(y_test, scaler)

        # --- Linear Regression ---
        try:
            lr_model = joblib.load('models/linear_regression_model.joblib')
            X_test_lr = X_test.reshape(X_test.shape[0], -1)
            y_pred_lr = inverse_temperature(lr_model.predict(X_test_lr), scaler)
            print(" ✓ Đã tải Linear Regression")
        except: y_pred_lr = None

        # --- LSTM ---
        try:
            import tensorflow as tf
            lstm_model = tf.keras.models.load_model('models/lstm_model.keras')
            y_pred_lstm = inverse_temperature(lstm_model.predict(X_test, verbose=0), scaler)
            print(" ✓ Đã tải LSTM")
        except: y_pred_lstm = None

        if y_pred_lr is None and y_pred_lstm is None:
            raise FileNotFoundError("Không tìm thấy mô hình nào để dự báo!")

        Path("results").mkdir(exist_ok=True)
        plt.figure(figsize=(12, 5))
        samples = min(150, len(y_test_real))
        plt.plot(y_test_real[-samples:], label="Thực tế", color='green', linewidth=2)
        if y_pred_lstm is not None:
            plt.plot(y_pred_lstm[-samples:], label="Dự báo (LSTM)", color='blue', linestyle='--')
        if y_pred_lr is not None:
            plt.plot(y_pred_lr[-samples:], label="Dự báo (Linear)", color='orange', linestyle=':')
        plt.title("So sánh thực tế và dự báo nhiệt độ")
        plt.legend()
        plt.savefig('results/forecast_comparison.png')
        plt.close()
        print(" ✓ Biểu đồ đã lưu vào results/")

        final_val = y_pred_lstm[-1] if y_pred_lstm is not None else y_pred_lr[-1]
        
        timestamp_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        success_all = True

        if y_pred_lr is not None:
            payload_lr = {
                "device_id": "ai_station_vinhlong",
                "timestamp": timestamp_now,
                "model": "Linear Regression",
                "predicted_temperature_next_hour": round(float(y_pred_lr[-1]), 2)
            }
            if not send_prediction_mqtt(payload_lr):
                success_all = False

        if y_pred_lstm is not None:
            payload_lstm = {
                "device_id": "ai_station_vinhlong",
                "timestamp": timestamp_now,
                "model": "LSTM",
                "predicted_temperature_next_hour": round(float(y_pred_lstm[-1]), 2)
            }
            if not send_prediction_mqtt(payload_lstm):
                success_all = False

        if not success_all:
            combined_payload = {
                "timestamp": timestamp_now,
                "linear": round(float(y_pred_lr[-1]), 2) if y_pred_lr is not None else None,
                "lstm": round(float(y_pred_lstm[-1]), 2) if y_pred_lstm is not None else None
            }
            with open('results/latest_payload.json', 'w', encoding='utf-8') as f:
                json.dump(combined_payload, f, indent=4, ensure_ascii=False)
            print("Lưu dự phòng dữ liệu vào file JSON")

        print("\nHoàn tất pipeline dự báo!")
    except Exception as e:
        print(f"Lỗi hệ thống: {e}")