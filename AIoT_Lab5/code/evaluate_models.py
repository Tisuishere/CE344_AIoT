import tensorflow as tf
import numpy as np
from sklearn.metrics import accuracy_score, f1_score
from data_utils import load_and_preprocess_data
import config
from tqdm import tqdm
import os

def evaluate_keras_model(model_path, test_ds):
    model = tf.keras.models.load_model(model_path)
    y_true, y_pred = [], []
    for images, labels in test_ds:
        preds = model.predict(images, verbose=0)
        y_pred.extend(np.argmax(preds, axis=1))
        y_true.extend(labels.numpy())
    return accuracy_score(y_true, y_pred), f1_score(y_true, y_pred, average='macro')

def evaluate_tflite_model(tflite_path, test_ds):
    interpreter = tf.lite.Interpreter(model_path=tflite_path)
    interpreter.allocate_tensors()
    input_details = interpreter.get_input_details()[0]
    output_details = interpreter.get_output_details()[0]
    
    is_int8 = input_details['dtype'] == np.int8
    scale, zero_point = input_details['quantization']

    y_true, y_pred = [], []
    
    for images, labels in tqdm(test_ds, desc=f"Evaluating {tflite_path.split('/')[-1]}"):
        images_np = images.numpy()
        for i in range(images_np.shape[0]):
            input_data = np.expand_dims(images_np[i], axis=0)
            
            # Xử lý chuẩn hóa ngược cho mô hình INT8
            if is_int8:
                input_data = (input_data / scale + zero_point).astype(np.int8)
                
            interpreter.set_tensor(input_details['index'], input_data)
            interpreter.invoke()
            output_data = interpreter.get_tensor(output_details['index'])
            
            y_pred.append(np.argmax(output_data))
            y_true.append(labels[i].numpy())

    return accuracy_score(y_true, y_pred), f1_score(y_true, y_pred, average='macro')

def run_evaluation():
    # Gọi đúng hàm load_and_preprocess_data() từ data_utils
    _, _, test_ds, _ = load_and_preprocess_data()
    
    models = {
        "Baseline (H5)": (config.BASELINE_MODEL_PATH, "keras"),
        "PTQ Dynamic": (config.PTQ_DYNAMIC_PATH, "tflite"),
        "PTQ FP16": (config.PTQ_FP16_PATH, "tflite"),
        "PTQ INT8": (config.PTQ_INT8_PATH, "tflite"),
        "QAT": (config.QAT_MODEL_PATH, "tflite")
    }

    report_path = os.path.join(config.REPORT_DIR, "evaluation_report.txt")

    # Mở file để ghi kết quả vào thư mục reports
    with open(report_path, "w", encoding="utf-8") as f:
        header = "\n--- KẾT QUẢ ĐÁNH GIÁ ---\n"
        print(header, end="")
        f.write(header)
        
        for name, (path, m_type) in models.items():
            if not os.path.exists(path):
                error_no_file = f"{name:15s} | Lỗi: Không tìm thấy file mô hình tại {path}\n"
                print(error_no_file, end="")
                f.write(error_no_file)
                continue
                
            try:
                if m_type == "keras":
                    acc, f1 = evaluate_keras_model(path, test_ds)
                else:
                    acc, f1 = evaluate_tflite_model(path, test_ds)
                
                result_line = f"{name:15s} | Accuracy: {acc:.4f} | Macro F1: {f1:.4f}\n"
                print(result_line, end="")
                f.write(result_line)
                
            except Exception as e:
                error_line = f"{name:15s} | Lỗi hệ thống: {str(e)}\n"
                print(error_line, end="")
                f.write(error_line)

    print(f"\nĐã xuất báo cáo thành công ra file: {report_path}")

if __name__ == "__main__":
    run_evaluation()