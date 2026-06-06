import os

# --- ÉP BUỘC SỬ DỤNG LEGACY KERAS ĐỂ TRÁNH XUNG ĐỘT HỆ THỐNG ---
os.environ["TF_USE_LEGACY_KERAS"] = "1"

# --- Cấu hình Dữ liệu ---
IMAGE_SIZE = (160, 160)
MIN_FACES = 20
BATCH_SIZE = 32
RANDOM_STATE = 42

# --- Đường dẫn ---
CODE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(CODE_DIR)
OUTPUT_DIR = os.path.join(BASE_DIR, 'outputs')
MODEL_DIR = os.path.join(OUTPUT_DIR, 'models')
REPORT_DIR = os.path.join(OUTPUT_DIR, 'reports')

# Tạo thư mục nếu chưa tồn tại
os.makedirs(MODEL_DIR, exist_ok=True)
os.makedirs(REPORT_DIR, exist_ok=True)

# --- Sử dụng lại định dạng .h5 tiêu chuẩn ổn định của Legacy Keras ---
BASELINE_MODEL_PATH = os.path.join(MODEL_DIR, "baseline_mobilenetv2.h5")
PTQ_DYNAMIC_PATH = os.path.join(MODEL_DIR, "mobilenetv2_ptq_dynamic.tflite")
PTQ_FP16_PATH = os.path.join(MODEL_DIR, "mobilenetv2_ptq_fp16.tflite")
PTQ_INT8_PATH = os.path.join(MODEL_DIR, "mobilenetv2_ptq_int8.tflite")
QAT_MODEL_PATH = os.path.join(MODEL_DIR, "mobilenetv2_qat.tflite")