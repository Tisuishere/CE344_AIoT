import numpy as np
import pickle
import json
from pathlib import Path
from sklearn.metrics import mean_absolute_error, mean_squared_error

def inverse_temperature(scaled_temp, scaler):
    """Chuyển đổi nhiệt độ từ dạng normalized về đơn vị gốc (°C)"""
    temp_dummy = np.zeros((len(scaled_temp), 3))
    temp_dummy[:, 0] = scaled_temp.flatten()
    restored = scaler.inverse_transform(temp_dummy)
    return restored[:, 0]


def evaluate_model(y_true, y_pred, model_name, metrics_dict=None):
    """Tính MAE, RMSE, MAPE và lưu kết quả"""
    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    
    valid_mask = y_true != 0
    if valid_mask.sum() > 0:
        mape = np.mean(np.abs((y_true[valid_mask] - y_pred[valid_mask]) / y_true[valid_mask])) * 100
    else:
        mape = np.nan
    
    print(f"--- {model_name} ---")
    print(f"MAE: {mae:.4f}°C, RMSE: {rmse:.4f}°C, MAPE: {mape:.2f}%")
    
    if metrics_dict is not None:
        metrics_dict[model_name] = {
            "MAE": float(mae),
            "RMSE": float(rmse),
            "MAPE": float(mape)
        }
    
    return {"MAE": mae, "RMSE": rmse, "MAPE": mape}


if __name__ == "__main__":
    print("Đang tải dữ liệu và mô hình để đánh giá...\n")
    
    try:
        print("Tải dữ liệu từ file xử lý...")
        data = np.load('processed/weather_sequences.npz')
        X_test, y_test = data['X_test'], data['y_test']
        
        with open('processed/scaler.pkl', 'rb') as f:
            scaler = pickle.load(f)
        print(f"   ✓ Loaded X_test shape: {X_test.shape}")
        print(f"   ✓ Loaded y_test shape: {y_test.shape}\n")
        
        print("Tải các mô hình đã huấn luyện...")
        
        # Linear Regression
        try:
            import joblib
            lr_model = joblib.load('models/linear_regression_model.joblib')
            print("   ✓ Linear Regression model loaded")
        except:
            lr_model = None
            print("Linear Regression model không tìm thấy")
        
        # LSTM
        try:
            import tensorflow as tf
            lstm_model = tf.keras.models.load_model('models/lstm_model.keras')
            print("   ✓ LSTM model loaded\n")
        except:
            lstm_model = None
            print("LSTM model không tìm thấy\n")
        
        if lr_model is None and lstm_model is None:
            raise FileNotFoundError("Không tìm thấy bất kỳ mô hình nào. Hãy chạy train_*.py trước!")
        
        print("Dự đoán trên tập test...")
        metrics_dict = {}
        
        if lr_model is not None:
            X_test_lr = X_test.reshape(X_test.shape[0], -1)
            y_pred_lr_scaled = lr_model.predict(X_test_lr)
            y_pred_lr = inverse_temperature(y_pred_lr_scaled, scaler)
            y_test_real = inverse_temperature(y_test, scaler)
            print("   ✓ Linear Regression prediction done")
        else:
            y_pred_lr = None
            y_test_real = inverse_temperature(y_test, scaler)
        
        if lstm_model is not None:
            y_pred_lstm_scaled = lstm_model.predict(X_test, verbose=0)
            y_pred_lstm = inverse_temperature(y_pred_lstm_scaled, scaler)
            print("   ✓ LSTM prediction done\n")
        else:
            y_pred_lstm = None
        
        print("=" * 50)
        print("KẾT QUẢ ĐÁNH GIÁ MÔ HÌNH TRÊN TẬP TEST")
        print("=" * 50)
        
        if y_pred_lr is not None:
            evaluate_model(y_test_real, y_pred_lr, "Linear Regression", metrics_dict)
        
        if y_pred_lstm is not None:
            evaluate_model(y_test_real, y_pred_lstm, "LSTM", metrics_dict)
        
        print("\nLưu kết quả...")
        Path("results").mkdir(exist_ok=True)
        
        # Lưu JSON
        with open('results/metrics.json', 'w', encoding='utf-8') as f:
            json.dump(metrics_dict, f, indent=4, ensure_ascii=False)
        print("   ✓ Metrics saved to results/metrics.json")
        
        best_model_info = ""
        if len(metrics_dict) > 1:
            print("\n So sánh mô hình:")
            rmse_values = {name: m["RMSE"] for name, m in metrics_dict.items()}
            best_model = min(rmse_values, key=rmse_values.get)
            best_model_info = f"Mô hình tốt nhất: {best_model} (RMSE: {rmse_values[best_model]:.4f})"
            print(f"   {best_model_info}")
        
        with open('results/metrics.txt', 'w', encoding='utf-8') as f:
            f.write("=" * 50 + "\n")
            f.write("KẾT QUẢ ĐÁNH GIÁ MÔ HÌNH\n")
            f.write("=" * 50 + "\n\n")
            
            for model_name, metrics in metrics_dict.items():
                f.write(f"--- {model_name} ---\n")
                f.write(f"MAE: {metrics['MAE']:.4f}°C\n")
                f.write(f"RMSE: {metrics['RMSE']:.4f}°C\n")
                f.write(f"MAPE: {metrics['MAPE']:.2f}%\n\n")
            
            if best_model_info:
                f.write("=" * 50 + "\n")
                f.write("KẾT LUẬN SO SÁNH\n")
                f.write("=" * 50 + "\n")
                f.write(f"{best_model_info}\n")
                
        print("   ✓ Metrics saved to results/metrics.txt")
        print("\n Đánh giá hoàn tất!")
        
    except FileNotFoundError as e:
        print(f" Lỗi: {e}")