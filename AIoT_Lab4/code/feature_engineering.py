import pandas as pd
from config import LABELED_DATA_FILE, FEATURED_DATA_FILE
def main():
    if not LABELED_DATA_FILE.exists():
        raise FileNotFoundError(
            f"Khong tim thay du lieu da gan nhan: {LABELED_DATA_FILE}. "
            "Hay chay load_and_label_data.py truoc."
        )
    df = pd.read_csv(LABELED_DATA_FILE, parse_dates=["timestamp"])
    df["lag_1"] = df["temperature"].shift(1)
    df["lag_2"] = df["temperature"].shift(2)
    df["lag_6"] = df["temperature"].shift(6)
    df["rolling_mean_6"] = df["temperature"].rolling(window=6).mean()
    df["rolling_std_6"] = df["temperature"].rolling(window=6).std()
    df["diff_1"] = df["temperature"].diff(1)
    df["hour"] = df["timestamp"].dt.hour
    df["dayofweek"] = df["timestamp"].dt.dayofweek
    df = df.dropna().reset_index(drop=True)
    df.to_csv(FEATURED_DATA_FILE, index=False)
    print("Da tao dac trung va luu tai:", FEATURED_DATA_FILE)
    print(df.head())
if __name__ == "__main__":
    main()