import json
import pandas as pd
from config import DATA_FILE, LABELS_FILE, LABELED_DATA_FILE, TIMESTAMP_KEY
def load_dataset():
    if not DATA_FILE.exists():
        raise FileNotFoundError(f"Khong tim thay file du lieu: {DATA_FILE}")
    df = pd.read_csv(DATA_FILE)
    expected = {"timestamp", "value"}
    if not expected.issubset(df.columns):
        raise ValueError(f"File du lieu khong dung dinh dang. Can cac cot: {expected}")
    df = df.rename(columns={"value": "temperature"})
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.sort_values("timestamp").reset_index(drop=True)
    return df

def load_labels():
    if not LABELS_FILE.exists():
        raise FileNotFoundError(f"Khong tim thay file nhan: {LABELS_FILE}")
    with open(LABELS_FILE, "r", encoding="utf-8") as f:
        labels_json = json.load(f)
    if TIMESTAMP_KEY not in labels_json:
        raise KeyError(f"Khong tim thay key {TIMESTAMP_KEY} trong file nhan.")
    return pd.to_datetime(labels_json[TIMESTAMP_KEY])

def main():
    df = load_dataset()
    anomaly_times = load_labels()
    df["label"] = 0
    df.loc[df["timestamp"].isin(anomaly_times), "label"] = 1
    LABELED_DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(LABELED_DATA_FILE, index=False)
    print("Da luu du lieu da gan nhan tai:", LABELED_DATA_FILE)
    print(df.head())
    print("\nSo luong nhan:")
    print(df["label"].value_counts())

if __name__ == "__main__":
    main()