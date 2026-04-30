import pandas as pd
import numpy as np
import pickle
from pathlib import Path
from sklearn.preprocessing import MinMaxScaler

df = pd.read_csv("data/weather_btth_hourly.csv")
df["time"] = pd.to_datetime(df["time"])
df = df.sort_values("time").drop_duplicates().dropna()

print("\n=== THỐNG KÊ DỮ LIỆU THỜI TIẾT ===")
print("\nMô tả dữ liệu:")
print(df[["temp", "rhum", "pres"]].describe())
print("\nMa trận tương quan:")
print(df[["temp", "rhum", "pres"]].corr())
print(f"\nTổng số dòng: {len(df)}")
print(f"Khoảng thời gian: {df['time'].min()} -> {df['time'].max()}")

features = df[["temp", "rhum", "pres"]].values

scaler = MinMaxScaler()
scaled_data = scaler.fit_transform(features)

def create_sequences(data, window_size=24, target_col=0):
    X, y = [], []
    for i in range(len(data) - window_size):
        X.append(data[i:i + window_size])
        y.append(data[i + window_size, target_col])
    return np.array(X), np.array(y)

X, y = create_sequences(scaled_data, window_size=24, target_col=0)

train_size = int(len(X) * 0.8)
X_train, X_test = X[:train_size], X[train_size:]
y_train, y_test = y[:train_size], y[train_size:]

Path("processed").mkdir(exist_ok=True)
with open('processed/scaler.pkl', 'wb') as f:
    pickle.dump(scaler, f)

np.savez('processed/weather_sequences.npz', 
         X_train=X_train, X_test=X_test, y_train=y_train, y_test=y_test)
print("\n✓ Đã lưu dữ liệu chuỗi vào processed/weather_sequences.npz")
print("✓ Đã lưu scaler vào processed/scaler.pkl")