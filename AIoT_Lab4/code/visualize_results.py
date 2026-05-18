import pandas as pd
import matplotlib.pyplot as plt
from config import LABELED_DATA_FILE, OUTPUT_DIR

def plot_labeled_data(df, output_path=None):
    """
    Vẽ chuỗi nhiệt độ theo thời gian và đánh dấu các điểm bất thường đã gán nhãn
    """
    plt.figure(figsize=(15, 6))
    
    # Plot normal data
    plt.plot(df['timestamp'], df['temperature'], label='Nhiệt độ', color='blue', alpha=0.6)
    
    # Plot anomalies
    anomalies = df[df['label'] == 1]
    plt.scatter(anomalies['timestamp'], anomalies['temperature'], color='red', label='Bất thường (Label=1)', zorder=5)
    
    plt.title('Biểu đồ nhiệt độ theo thời gian và các điểm bất thường')
    plt.xlabel('Thời gian')
    plt.ylabel('Nhiệt độ (F)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    
    if output_path:
        plt.savefig(output_path)
        print(f"Đã lưu biểu đồ tại: {output_path}")
    else:
        plt.show()

def plot_anomalies_comparison(df, pred_col, model_name, output_path=None):
    """
    Vẽ chuỗi nhiệt độ, đánh dấu anomaly thật và anomaly dự đoán để phân tích FP, FN
    """
    plt.figure(figsize=(15, 6))
    
    # Plot normal data
    plt.plot(df['timestamp'], df['temperature'], label='Nhiệt độ', color='blue', alpha=0.6)
    
    # True anomalies
    true_anomalies = df[df['label'] == 1]
    plt.scatter(true_anomalies['timestamp'], true_anomalies['temperature'], color='green', marker='o', s=100, label='True Anomaly', zorder=5)
    
    # Predicted anomalies
    pred_anomalies = df[df[pred_col] == 1]
    plt.scatter(pred_anomalies['timestamp'], pred_anomalies['temperature'], color='red', marker='x', s=100, label=f'Predicted Anomaly ({model_name})', zorder=6)
    
    plt.title(f'So sánh bất thường thật và dự đoán - {model_name}')
    plt.xlabel('Thời gian')
    plt.ylabel('Nhiệt độ (F)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    
    if output_path:
        plt.savefig(output_path)
        print(f"Đã lưu biểu đồ tại: {output_path}")
    else:
        plt.show()

if __name__ == "__main__":
    if LABELED_DATA_FILE.exists():
        df = pd.read_csv(LABELED_DATA_FILE, parse_dates=['timestamp'])
        output_file = OUTPUT_DIR / "labeled_data_plot.png"
        plot_labeled_data(df, output_file)
    else:
        print(f"Không tìm thấy file dữ liệu: {LABELED_DATA_FILE}")

    zscore_file = OUTPUT_DIR / "zscore_results.csv"
    if zscore_file.exists():
        df_z = pd.read_csv(zscore_file, parse_dates=['timestamp'])
        plot_anomalies_comparison(df_z, "pred_zscore", "Z-Score", OUTPUT_DIR / "zscore_comparison_plot.png")

    iforest_file = OUTPUT_DIR / "iforest_results.csv"
    if iforest_file.exists():
        df_i = pd.read_csv(iforest_file, parse_dates=['timestamp'])
        plot_anomalies_comparison(df_i, "pred_iforest", "Isolation Forest", OUTPUT_DIR / "iforest_comparison_plot.png")

    ocsvm_file = OUTPUT_DIR / "ocsvm_results.csv"
    if ocsvm_file.exists():
        df_o = pd.read_csv(ocsvm_file, parse_dates=['timestamp'])
        plot_anomalies_comparison(df_o, "pred_ocsvm", "One-Class SVM", OUTPUT_DIR / "ocsvm_comparison_plot.png")
        
    lstm_file = OUTPUT_DIR / "lstm_results.csv"
    if lstm_file.exists():
        df_l = pd.read_csv(lstm_file, parse_dates=['timestamp'])
        df_l = df_l.dropna(subset=['pred_lstm']) # Bỏ các hàng NaN do sequence
        plot_anomalies_comparison(df_l, "pred_lstm", "LSTM Forecasting", OUTPUT_DIR / "lstm_comparison_plot.png")
