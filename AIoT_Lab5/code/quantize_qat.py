import os
import tensorflow as tf
import tensorflow_model_optimization as tfmot
from data_utils import load_and_preprocess_data
import config

def run_qat():
    train_ds, val_ds, _, _ = load_and_preprocess_data()
    
    print("Đang tải mô hình Baseline để thực hiện QAT...")
    model = tf.keras.models.load_model(config.BASELINE_MODEL_PATH)

    print("Đang trải phẳng (flatten) cấu trúc lồng nhau để tương thích với QAT...")
    
    # 1. Trích xuất mô hình con MobileNetV2 (đang là lớp đầu tiên của Sequential)
    base_model = model.layers[0]
    
    # Mở khóa toàn bộ mạng để học vi chỉnh (Fine-tuning) với cấu hình QAT
    base_model.trainable = True 
    
    # 2. Xây dựng lại thành cấu trúc Functional Model phẳng
    inputs = base_model.input
    x = base_model.output
    
    # Móc nối các lớp phân loại phía sau vào đuôi của MobileNetV2
    for layer in model.layers[1:]:
        x = layer(x)
        
    flat_model = tf.keras.Model(inputs=inputs, outputs=x)

    print("Chèn các khối mô phỏng lượng tử hóa (QAT)...")
    # Lượng tử hóa model phẳng sẽ không còn bị lỗi "nested" nữa
    qat_model = tfmot.quantization.keras.quantize_model(flat_model)
    
    qat_model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=1e-5),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"]
    )

    print("Bắt đầu fine-tune QAT (2 epochs)...")
    qat_model.fit(train_ds, validation_data=val_ds, epochs=2)

    print("Đang convert QAT model sang TFLite...")
    converter = tf.lite.TFLiteConverter.from_keras_model(qat_model)
    converter.optimizations = [tf.lite.Optimize.DEFAULT]
    qat_tflite = converter.convert()
    
    with open(config.QAT_MODEL_PATH, "wb") as f:
        f.write(qat_tflite)
        
    print(f"\nĐã lưu mô hình QAT TFLite thành công tại: {config.QAT_MODEL_PATH}")

if __name__ == "__main__":
    run_qat()