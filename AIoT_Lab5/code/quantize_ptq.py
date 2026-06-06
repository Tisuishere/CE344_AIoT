import tensorflow as tf
from data_utils import load_and_preprocess_data
import config

def representative_dataset_gen():
    # Sử dụng đúng tên hàm từ data_utils.py
    train_ds, _, _, _ = load_and_preprocess_data()
    # Lấy 100 batch đầu tiên để làm dữ liệu chuẩn hóa (calibration) cho INT8
    for images, _ in train_ds.take(100):
        # Trích xuất từng ảnh trong batch (kích thước batch mặc định là 32)
        for i in range(images.shape[0]):
            yield [tf.expand_dims(images[i], axis=0)]

def run_ptq():
    print("Đang tải mô hình Baseline cho PTQ...")
    # Load model đuôi .h5 mượt mà nhờ thiết lập Legacy Keras
    model = tf.keras.models.load_model(config.BASELINE_MODEL_PATH)
    print("Tải mô hình Baseline thành công.")

    # --- 1. Lượng tử hóa PTQ Dynamic Range ---
    print("Đang chuyển đổi sang PTQ Dynamic Range...")
    converter_dynamic = tf.lite.TFLiteConverter.from_keras_model(model)
    converter_dynamic.optimizations = [tf.lite.Optimize.DEFAULT]
    tflite_dynamic = converter_dynamic.convert()
    with open(config.PTQ_DYNAMIC_PATH, "wb") as f:
        f.write(tflite_dynamic)
    print(f"Đã lưu mô hình Dynamic Range TFLite tại: {config.PTQ_DYNAMIC_PATH}")

    # --- 2. Lượng tử hóa PTQ Float16 ---
    print("Đang chuyển đổi sang PTQ Float16...")
    converter_fp16 = tf.lite.TFLiteConverter.from_keras_model(model)
    converter_fp16.optimizations = [tf.lite.Optimize.DEFAULT]
    converter_fp16.target_spec.supported_types = [tf.float16]
    tflite_fp16 = converter_fp16.convert()
    with open(config.PTQ_FP16_PATH, "wb") as f:
        f.write(tflite_fp16)
    print(f"Đã lưu mô hình Float16 TFLite tại: {config.PTQ_FP16_PATH}")

    # --- 3. Lượng tử hóa PTQ Full Integer (INT8) ---
    print("Đang chuyển đổi sang PTQ Full Integer (INT8)... Quá trình này cần load lại data để Calibration.")
    converter_int8 = tf.lite.TFLiteConverter.from_keras_model(model)
    converter_int8.optimizations = [tf.lite.Optimize.DEFAULT]
    # Gắn hàm load data vào để calibrate các tensor về dạng số nguyên
    converter_int8.representative_dataset = representative_dataset_gen
    converter_int8.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]
    # Định dạng Input và Output cũng phải là số nguyên (rất quan trọng cho thiết bị biên)
    converter_int8.inference_input_type = tf.int8
    converter_int8.inference_output_type = tf.int8
    
    tflite_int8 = converter_int8.convert()
    with open(config.PTQ_INT8_PATH, "wb") as f:
        f.write(tflite_int8)
    print(f"Đã lưu mô hình Full Integer (INT8) TFLite tại: {config.PTQ_INT8_PATH}")

    print("\n--- HOÀN TẤT TOÀN BỘ QUÁ TRÌNH LƯỢNG TỬ HÓA PTQ ---")

if __name__ == "__main__":
    run_ptq()