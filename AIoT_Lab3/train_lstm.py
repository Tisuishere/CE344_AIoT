import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Input, LSTM, Dense, Dropout
from preprocess_dataset import X_train, X_test, y_train, y_test 

print(f"Kích thước X_train cho LSTM: {X_train.shape}") 

model = Sequential()

model.add(Input(shape=(X_train.shape[1], X_train.shape[2]))) 
model.add(LSTM(units=50, activation='relu'))
model.add(Dropout(0.2)) 

model.add(Dense(units=1))

model.compile(optimizer='adam', loss='mean_squared_error')

print("Đang tiến hành huấn luyện mô hình LSTM...")
history = model.fit(
    X_train, y_train,
    epochs=20, 
    batch_size=32,
    validation_data=(X_test, y_test),
    verbose=1
)

y_pred_lstm = model.predict(X_test)

model.save('models/lstm_model.keras')
print("Huấn luyện xong và đã lưu mô hình LSTM vào thư mục models/ !")