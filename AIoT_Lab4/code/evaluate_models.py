import pandas as pd
from sklearn.metrics import precision_score, recall_score, f1_score, confusion_matrix
from config import OUTPUT_DIR

def evaluate_model(y_true, y_pred, model_name):
    precision = precision_score(y_true, y_pred, zero_division=0)
    recall = recall_score(y_true, y_pred, zero_division=0)
    f1 = f1_score(y_true, y_pred, zero_division=0)
    cm = confusion_matrix(y_true, y_pred)
    
    print(f"--- Evaluation for {model_name} ---")
    print(f"Precision: {precision:.4f}")
    print(f"Recall:    {recall:.4f}")
    print(f"F1-Score:  {f1:.4f}")
    print("Confusion Matrix:")
    print(cm)
    print("-" * 35)
    
    return precision, recall, f1, cm

def main():
    # Paths for results
    zscore_file = OUTPUT_DIR / "zscore_results.csv"
    iforest_file = OUTPUT_DIR / "iforest_results.csv"
    ocsvm_file = OUTPUT_DIR / "ocsvm_results.csv"
    lstm_file = OUTPUT_DIR / "lstm_results.csv"
    
    with open(OUTPUT_DIR / "metrics_summary.txt", "w", encoding='utf-8') as f:
        # Evaluate Z-score

        if zscore_file.exists():
            df_z = pd.read_csv(zscore_file)
            p, r, f1, cm = evaluate_model(df_z["label"], df_z["pred_zscore"], "Z-Score")
            f.write(f"--- Evaluation for Z-Score ---\nPrecision: {p:.4f}\nRecall: {r:.4f}\nF1-Score: {f1:.4f}\nConfusion Matrix:\n{cm}\n\n")
            
        # Evaluate Isolation Forest
        if iforest_file.exists():
            df_i = pd.read_csv(iforest_file)
            p, r, f1, cm = evaluate_model(df_i["label"], df_i["pred_iforest"], "Isolation Forest")
            f.write(f"--- Evaluation for Isolation Forest ---\nPrecision: {p:.4f}\nRecall: {r:.4f}\nF1-Score: {f1:.4f}\nConfusion Matrix:\n{cm}\n\n")

        # Evaluate OCSVM
        if ocsvm_file.exists():
            df_o = pd.read_csv(ocsvm_file)
            p, r, f1, cm = evaluate_model(df_o["label"], df_o["pred_ocsvm"], "One-Class SVM")
            f.write(f"--- Evaluation for One-Class SVM ---\nPrecision: {p:.4f}\nRecall: {r:.4f}\nF1-Score: {f1:.4f}\nConfusion Matrix:\n{cm}\n\n")
            
        # Evaluate LSTM
        if lstm_file.exists():
            df_l = pd.read_csv(lstm_file)
            # Dữ liệu LSTM bị khuyết phần đầu do sequence_length, dropna hoặc fillna
            df_l = df_l.dropna(subset=['pred_lstm'])
            p, r, f1, cm = evaluate_model(df_l["label"], df_l["pred_lstm"], "LSTM Forecasting")
            f.write(f"--- Evaluation for LSTM Forecasting ---\nPrecision: {p:.4f}\nRecall: {r:.4f}\nF1-Score: {f1:.4f}\nConfusion Matrix:\n{cm}\n\n")

    print("Đã lưu các chỉ số đánh giá vào outputs/metrics_summary.txt")

if __name__ == "__main__":
    main()
