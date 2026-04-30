from sklearn.linear_model import LinearRegression
import joblib 
from preprocess_dataset import X_train, X_test, y_train, y_test 

X_train_lr = X_train.reshape(X_train.shape[0], -1)
X_test_lr = X_test.reshape(X_test.shape[0], -1)

lr_model = LinearRegression()
lr_model.fit(X_train_lr, y_train)

joblib.dump(lr_model, 'models/linear_regression_model.joblib')
print("Huấn luyện thành công và đã lưu model!")