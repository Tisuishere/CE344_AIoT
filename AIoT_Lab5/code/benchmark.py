import tensorflow as tf
import numpy as np
import time
import os
from data_utils import load_and_preprocess_data
import config

def get_model_size(file_path):
    size_bytes = os.path.getsize(file_path)
    return size_bytes / (1024 * 1024) # Trả về MB

def benchmark_keras(model_path, test_ds):
    model = tf.keras.models.load_model(model_path)
    # Khởi động (Warm-up)
    sample_images = next(iter(test_ds))[0]
    model.predict(sample_images[:1], verbose=0)
    
    latencies = []
    for images, _ in test_ds:
        for i in range(images.shape[0]):
            img = np.expand_dims(images[i].numpy(), axis=0)
            start = time.time()
            model.predict(img, verbose=0)
            latencies.append((time.time() - start) * 1000) # Đổi sang ms
            if len(latencies) >= 100: # Đo trên 100 sample là đủ
                break
        if len(latencies) >= 100: break
    return np.mean(latencies)

def benchmark_tflite(tflite_path, test_ds):
    interpreter = tf.lite.Interpreter(model_path=tflite_path)
    interpreter.allocate_tensors()
    input_details = interpreter.get_input_details()[0]
    
    is_int8 = input_details['dtype'] == np.int8
    if is_int8:
        scale, zero_point = input_details['quantization']

    latencies = []
    # Khởi động (Warm-up)
    dummy_input = np.zeros(input_details['shape'], dtype=input_details['dtype'])
    interpreter.set_tensor(input_details['index'], dummy_input)
    interpreter.invoke()

    for images, _ in test_ds:
        for i in range(images.shape[0]):
            input_data = np.expand_dims(images[i].numpy(), axis=0)
            if is_int8:
                input_data = (input_data / scale + zero_point).astype(np.int8)
                
            interpreter.set_tensor(input_details['index'], input_data)
            
            start = time.time()
            interpreter.invoke()
            latencies.append((time.time() - start) * 1000)
            
            if len(latencies) >= 100:
                break
        if len(latencies) >= 100: break
    return np.mean(latencies)

def run_benchmark():
    _, _, test_ds, _ = load_and_preprocess_data()
    
    models = {
        "Baseline (H5)": (config.BASELINE_MODEL_PATH, "keras"),
        "PTQ Dynamic": (config.PTQ_DYNAMIC_PATH, "tflite"),
        "PTQ FP16": (config.PTQ_FP16_PATH, "tflite"),
        "PTQ INT8": (config.PTQ_INT8_PATH, "tflite"),
        "QAT": (config.QAT_MODEL_PATH, "tflite")
    }

    report_path = os.path.join(config.REPORT_DIR, "benchmark_report.txt")

    # Mở file ghi báo cáo Benchmark
    with open(report_path, "w", encoding="utf-8") as f:
        header1 = "\n--- KẾT QUẢ BENCHMARK ---\n"
        header2 = f"{'Mô hình':<15} | {'Dung lượng (MB)':<15} | {'Latency (ms/sample)':<20}\n"
        header3 = "-" * 55 + "\n"
        
        # Ghi Header
        for h in [header1, header2, header3]:
            print(h, end="")
            f.write(h)

        for name, (path, m_type) in models.items():
            try:
                size = get_model_size(path)
                if m_type == "keras":
                    latency = benchmark_keras(path, test_ds)
                else:
                    latency = benchmark_tflite(path, test_ds)
                
                result_line = f"{name:<15} | {size:<15.2f} | {latency:<20.2f}\n"
                print(result_line, end="")
                f.write(result_line)
                
            except Exception as e:
                error_line = f"{name:<15} | Lỗi: {str(e)}\n"
                print(error_line, end="")
                f.write(error_line)

    print(f"\nĐã xuất báo cáo thành công ra file: {report_path}")

if __name__ == "__main__":
    run_benchmark()