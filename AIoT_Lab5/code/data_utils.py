import tensorflow as tf
from sklearn.datasets import fetch_lfw_people
from sklearn.model_selection import train_test_split
import config

def preprocess(image, label):
    """Hàm tiền xử lý theo yêu cầu đề bài"""
    # Resize về 160x160
    image = tf.image.resize(image, config.IMAGE_SIZE)
    # Đưa dải pixel về [-1, 1] cho MobileNetV2
    image = tf.keras.applications.mobilenet_v2.preprocess_input(image)
    return image, label

def load_and_preprocess_data():
    """Tải và chia dữ liệu (70/15/15), trả về tf.data.Dataset và số lượng classes"""
    print("Đang tải dataset LFW...")
    lfw = fetch_lfw_people(min_faces_per_person=config.MIN_FACES, color=True, resize=0.5)
    
    X = lfw.images
    y = lfw.target
    num_classes = len(lfw.target_names)
    
    print(f"Tổng số ảnh: {X.shape[0]}, Số lớp: {num_classes}")

    # Chia train: 70%, val: 15%, test: 15%
    X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.3, random_state=config.RANDOM_STATE)
    X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=config.RANDOM_STATE)

    def make_dataset(images, labels, shuffle=False):
        ds = tf.data.Dataset.from_tensor_slices((images, labels))
        if shuffle:
            ds = ds.shuffle(buffer_size=len(images))
        ds = ds.map(preprocess, num_parallel_calls=tf.data.AUTOTUNE)
        ds = ds.batch(config.BATCH_SIZE).prefetch(tf.data.AUTOTUNE)
        return ds

    train_ds = make_dataset(X_train, y_train, shuffle=True)
    val_ds = make_dataset(X_val, y_val)
    test_ds = make_dataset(X_test, y_test)

    return train_ds, val_ds, test_ds, num_classes

# ... (giữ nguyên các hàm phía trên) ...

if __name__ == "__main__":
    print("=== BẮT ĐẦU QUÁ TRÌNH TẢI VÀ TIỀN XỬ LÝ DỮ LIỆU ===")
    # Gọi hàm để kích hoạt quá trình tải từ sklearn
    train_ds, val_ds, test_ds, num_classes = load_and_preprocess_data()
    print("=== HOÀN TẤT TẢI DỮ LIỆU! Sẵn sàng cho huấn luyện. ===")