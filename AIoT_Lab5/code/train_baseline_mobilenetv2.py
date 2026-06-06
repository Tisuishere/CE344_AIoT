import tensorflow as tf
from data_utils import load_and_preprocess_data
import config

def train_baseline():
    train_ds, val_ds, _, num_classes = load_and_preprocess_data()

    print("Khởi tạo mô hình MobileNetV2 Baseline...")
    base_model = tf.keras.applications.MobileNetV2(
        input_shape=(config.IMAGE_SIZE[0], config.IMAGE_SIZE[1], 3),
        include_top=False,
        weights="imagenet"
    )
    base_model.trainable = False # Đóng băng base model ban đầu (Transfer Learning)

    model = tf.keras.Sequential([
        base_model,
        tf.keras.layers.GlobalAveragePooling2D(),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(num_classes, activation='softmax')
    ])

    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=1e-3),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"]
    )

    print("Bắt đầu huấn luyện Baseline...")
    model.fit(train_ds, validation_data=val_ds, epochs=10) 

    model.save(config.BASELINE_MODEL_PATH)
    print(f"Đã lưu mô hình Baseline tại {config.BASELINE_MODEL_PATH}")

if __name__ == "__main__":
    train_baseline()