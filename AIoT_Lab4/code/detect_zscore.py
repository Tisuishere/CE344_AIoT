import pandas as pd
from config import FEATURED_DATA_FILE, OUTPUT_DIR, ZSCORE_THRESHOLD
def main():
    if not FEATURED_DATA_FILE.exists():
        raise FileNotFoundError(
            f"Khong tim thay du lieu dac trung: {FEATURED_DATA_FILE}. "
            "Hay chay feature_engineering.py truoc."
        )
    df = pd.read_csv(FEATURED_DATA_FILE, parse_dates=["timestamp"])
    mean_temp = df["temperature"].mean()
    std_temp = df["temperature"].std()
    if std_temp == 0:
        raise ValueError("Do lech chuan bang 0, khong the tinh Z-score.")
    df["zscore"] = (df["temperature"] - mean_temp) / std_temp
    df["pred_zscore"] = (df["zscore"].abs() > ZSCORE_THRESHOLD).astype(int)
    out_file = OUTPUT_DIR / "zscore_results.csv"
    df.to_csv(out_file, index=False)
    print("Da luu ket qua Z-score tai:", out_file)
    print(df[["timestamp", "temperature", "label", "zscore", "pred_zscore"]].head())
if __name__ == "__main__":
    main()