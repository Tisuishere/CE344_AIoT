from pathlib import Path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR = PROJECT_ROOT / "outputs"
MODEL_DIR = PROJECT_ROOT / "models"
DATA_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
MODEL_DIR.mkdir(parents=True, exist_ok=True)
DATA_URL = "https://raw.githubusercontent.com/numenta/NAB/master/data/realKnownCause/ambient_temperature_system_failure.csv"
LABELS_URL ="https://raw.githubusercontent.com/numenta/NAB/master/labels/combined_labels.json"
DATA_FILE = DATA_DIR / "ambient_temperature_system_failure.csv"
LABELS_FILE = DATA_DIR / "combined_labels.json"
LABELED_DATA_FILE = OUTPUT_DIR / "labeled_temperature_data.csv"
FEATURED_DATA_FILE = OUTPUT_DIR / "featured_temperature_data.csv"
METRICS_FILE = OUTPUT_DIR / "metrics_summary.txt"
ANOMALY_PLOT_FILE = OUTPUT_DIR / "anomaly_plot.png"
CONFUSION_MATRIX_FILE = OUTPUT_DIR / "confusion_matrix.png"
MODEL_FILE = MODEL_DIR / "isolation_forest_model.pkl"
SCALER_FILE = MODEL_DIR / "standard_scaler.pkl"
MQTT_BROKER = "127.0.0.1"
MQTT_PORT = 1883
MQTT_TOPIC = "iot/anomaly/temperature"
TIMESTAMP_KEY = "realKnownCause/ambient_temperature_system_failure.csv"
ZSCORE_THRESHOLD = 3.0
ISOFOR_CONTAMINATION = 0.01
ISOFOR_N_ESTIMATORS = 200
RANDOM_STATE = 42

# OCSVM configs
OCSVM_NU = 0.01
OCSVM_KERNEL = "rbf"
OCSVM_GAMMA = "scale"

# LSTM configs
LSTM_SEQ_LENGTH = 24
LSTM_EPOCHS = 10
LSTM_BATCH_SIZE = 64
LSTM_UNITS = 32
LSTM_THRESHOLD_SIGMA = 3.0