import pickle
from xml.parsers.expat import model
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import IsolationForest
from config import (
    FEATURED_DATA_FILE, OUTPUT_DIR, MODEL_FILE, SCALER_FILE,
    ISOFOR_CONTAMINATION, ISOFOR_N_ESTIMATORS, RANDOM_STATE
)
FEATURE_COLS = [
    "temperature", "lag_1", "lag_2", "lag_6",
    "rolling_mean_6", "rolling_std_6", "diff_1",
    "hour", "dayofweek"
]
def main():
    if not FEATURED_DATA_FILE.exists():
        raise FileNotFoundError(
            f"Khong tim thay du lieu dac trung: {FEATURED_DATA_FILE}. "
            "Hay chay feature_engineering.py truoc."
        )
    df = pd.read_csv(FEATURED_DATA_FILE, parse_dates=["timestamp"])
    X = df[FEATURE_COLS].values
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    model = IsolationForest(
        n_estimators=ISOFOR_N_ESTIMATORS,
        contamination=ISOFOR_CONTAMINATION,
        random_state=RANDOM_STATE
    )
    model.fit(X_scaled)
    pred = model.predict(X_scaled)
    df["pred_iforest"] = (pred == -1).astype(int)
    df["iforest_score"] = model.decision_function(X_scaled)
    out_file = OUTPUT_DIR / "iforest_results.csv"
    df.to_csv(out_file, index=False)
    with open(MODEL_FILE, "wb") as f:
        pickle.dump(model, f)
    with open(SCALER_FILE, "wb") as f:
        pickle.dump(scaler, f)
    print("Da luu ket qua Isolation Forest tai:", out_file)
    print("Da luu model tai:", MODEL_FILE)
    print("Da luu scaler tai:", SCALER_FILE)
    print(df[["timestamp", "temperature", "label", "pred_iforest", "iforest_score"]].head())
if __name__ == "__main__":
    main()