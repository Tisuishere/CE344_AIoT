import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.preprocessing import StandardScaler
from config import (
    FEATURED_DATA_FILE, OUTPUT_DIR, MODEL_DIR,
    LSTM_SEQ_LENGTH, LSTM_EPOCHS, LSTM_BATCH_SIZE, LSTM_UNITS, LSTM_THRESHOLD_SIGMA
)

FEATURE_COLS = [
    "temperature", "lag_1", "lag_2", "lag_6",
    "rolling_mean_6", "rolling_std_6", "diff_1",
    "hour", "dayofweek"
]
TARGET_COL_IDX = 0 # "temperature"

def create_sequences(data, seq_length):
    X = []
    y = []
    for i in range(len(data) - seq_length):
        X.append(data[i:i + seq_length])
        y.append(data[i + seq_length, TARGET_COL_IDX])
    return np.array(X), np.array(y)

def main():
    if not FEATURED_DATA_FILE.exists():
        raise FileNotFoundError("Chưa có data đặc trưng. Hãy chạy feature_engineering.py")
    
    df = pd.read_csv(FEATURED_DATA_FILE, parse_dates=["timestamp"])
    
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(df[FEATURE_COLS].values)
    
    X, y = create_sequences(scaled_data, LSTM_SEQ_LENGTH)
    
    model = tf.keras.Sequential([
        tf.keras.layers.Input(shape=(LSTM_SEQ_LENGTH, len(FEATURE_COLS))),
        tf.keras.layers.LSTM(LSTM_UNITS, activation='relu'),
        tf.keras.layers.Dense(1)
    ])
    
    model.compile(optimizer='adam', loss='mse')
    
    print(f"Đang huấn luyện LSTM ({LSTM_EPOCHS} epochs, batch {LSTM_BATCH_SIZE})...")
    model.fit(X, y, epochs=LSTM_EPOCHS, batch_size=LSTM_BATCH_SIZE, validation_split=0.1, verbose=1)
    
    print("Đang dự đoán...")
    preds = model.predict(X).flatten()
    
    errors = np.abs(y - preds)
    mean_err = np.mean(errors)
    std_err = np.std(errors)
    threshold = mean_err + LSTM_THRESHOLD_SIGMA * std_err
    
    print(f"Mean Error: {mean_err:.4f}, Std Error: {std_err:.4f}, Threshold: {threshold:.4f}")
    
    anomalies = (errors > threshold).astype(int)
    
    df["pred_lstm"] = 0
    df.loc[LSTM_SEQ_LENGTH:, "pred_lstm"] = anomalies
    df["lstm_error"] = 0.0
    df.loc[LSTM_SEQ_LENGTH:, "lstm_error"] = errors
    
    out_file = OUTPUT_DIR / "lstm_results.csv"
    df.to_csv(out_file, index=False)
    
    model_file = MODEL_DIR / "lstm_model.keras"
    model.save(model_file)
    
    print("Đã lưu kết quả LSTM tại:", out_file)
    print("Đã lưu model tại:", model_file)

if __name__ == "__main__":
    main()
