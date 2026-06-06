#!/usr/bin/env python3
"""
PIPELINE DỰ BÁO THỜI TIẾT - ORCHESTRATOR
Chạy toàn bộ pipeline từ tải dữ liệu -> train -> đánh giá -> dự đoán -> publish MQTT
"""

import subprocess
import sys
from pathlib import Path

def run_script(script_name, description, *args):
    """Chạy một script Python và kiểm tra lỗi"""
    print(f"\n{'='*60}")
    print(f"{'='*60}")
    print(f"{description}")
    print(f"{'='*60}\n")
    
    cmd = [sys.executable, script_name] + list(args)
    try:
        result = subprocess.run(cmd, cwd=Path(__file__).parent, check=True)
        print(f"\n {description} hoàn tất")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n {description} thất bại (exit code: {e.returncode})")
        return False
    except Exception as e:
        print(f"\n Lỗi khi chạy {script_name}: {e}")
        return False


def main():
    
    steps_completed = []
    
    # BƯỚC 1: Tải dữ liệu
    if run_script('download_dataset_meteostat.py', 'Tải dữ liệu từ Meteostat'):
        steps_completed.append("1. Tải dữ liệu ✓")
    else:
        print("  Tải dữ liệu thất bại, tiếp tục với dữ liệu cũ...")
    
    # BƯỚC 2: Tiền xử lý (preprocess)
    if run_script('preprocess_dataset.py', 'Tiền xử lý và chuẩn hóa dữ liệu'):
        steps_completed.append("2. Tiền xử lý ✓")
    else:
        print(" Tiền xử lý thất bại. Dừng pipeline.")
        return
    
    # BƯỚC 3: Huấn luyện Linear Regression
    if run_script('train_linear_regression.py', 'Huấn luyện mô hình Linear Regression'):
        steps_completed.append("3. Train Linear Regression ✓")
    else:
        print("  Linear Regression thất bại")
    
    # BƯỚC 4: Huấn luyện LSTM
    if run_script('train_lstm.py', 'Huấn luyện mô hình LSTM'):
        steps_completed.append("4. Train LSTM ✓")
    else:
        print("  LSTM thất bại")
    
    # BƯỚC 5: Đánh giá mô hình
    if run_script('evaluate_models.py', 'Đánh giá mô hình (MAE, RMSE, MAPE)'):
        steps_completed.append("5. Đánh giá mô hình ✓")
    else:
        print("  Đánh giá thất bại")
    
    # BƯỚC 6: Dự đoán và vẽ biểu đồ
    if run_script('predict_and_publish_mqtt.py', 'Dự đoán và publish MQTT/lưu biểu đồ'):
        steps_completed.append("6. Dự đoán + Publish ✓")
    else:
        print("  Dự đoán thất bại")
    
    # TÓM TẮT KẾT QUẢ
    print(f"\n{'='*60}")
    print(" KẾT QUẢ PIPELINE")
    print(f"{'='*60}\n")
    
    if steps_completed:
        print(" Các bước hoàn tất:")
        for step in steps_completed:
            print(f"   {step}")
    else:
        print(" Không bước nào hoàn tất thành công")
    
    print("\n Các file output được tạo:")
    output_paths = [
        "processed/weather_sequences.npz (Dữ liệu chuỗi)",
        "processed/scaler.pkl (Bộ chuẩn hóa)",
        "models/linear_regression.pkl (Mô hình LR)",
        "models/lstm.keras (Mô hình LSTM)",
        "results/metrics.json (Kết quả đánh giá - JSON)",
        "results/metrics.txt (Kết quả đánh giá - TXT)",
        "results/forecast_comparison.png (Biểu đồ so sánh)",
        "results/latest_payload.json (Dự đoán mới nhất)",
    ]
    
    for path in output_paths:
        print(f"    {path}")
    
    print(f"\n{'='*60}")
    print(" PIPELINE HOÀN TẤT!\n")


if __name__ == "__main__":
    main()