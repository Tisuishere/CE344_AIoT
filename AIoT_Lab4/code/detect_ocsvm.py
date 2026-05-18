import pickle
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.svm import OneClassSVM
from config import (
    FEATURED_DATA_FILE, OUTPUT_DIR, MODEL_DIR,
    OCSVM_NU, OCSVM_KERNEL, OCSVM_GAMMA
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
    
    model = OneClassSVM(
        nu=OCSVM_NU,
        kernel=OCSVM_KERNEL,
        gamma=OCSVM_GAMMA
    )
    
    print("Dang huan luyen One-Class SVM...")
    model.fit(X_scaled)
    
    # Predict returns 1 for inliers, -1 for outliers
    pred = model.predict(X_scaled)
    df["pred_ocsvm"] = (pred == -1).astype(int)
    
    # score_samples returns the unnormalized score (higher is better/more normal)
    df["ocsvm_score"] = model.score_samples(X_scaled)
    
    out_file = OUTPUT_DIR / "ocsvm_results.csv"
    df.to_csv(out_file, index=False)
    
    model_file = MODEL_DIR / "ocsvm_model.pkl"
    scaler_file = MODEL_DIR / "ocsvm_scaler.pkl"
    with open(model_file, "wb") as f:
        pickle.dump(model, f)
    with open(scaler_file, "wb") as f:
        pickle.dump(scaler, f)
        
    print("Da luu ket qua OCSVM tai:", out_file)
    print("Da luu model tai:", model_file)
    print("Da luu scaler tai:", scaler_file)
    print(df[["timestamp", "temperature", "label", "pred_ocsvm", "ocsvm_score"]].head())

if __name__ == "__main__":
    main()
