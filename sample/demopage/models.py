import os
import numpy as np
import cv2
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.metrics import accuracy_score
from sklearn.decomposition import IncrementalPCA
from sklearn.utils.class_weight import compute_class_weight
from sklearn.preprocessing import StandardScaler
import joblib
from django.conf import settings

# Paths
data_dir = os.path.join(settings.BASE_DIR, 'skin_disease_dataset', 'train_set')
if not os.path.exists(data_dir):
    raise FileNotFoundError(f"Directory not found: {data_dir}")

classes = os.listdir(data_dir)

# Parameters
img_height, img_width = 128, 128
num_classes = len(classes)

# Load and preprocess images
X, y = [], []
for label, class_name in enumerate(classes):
    class_dir = os.path.join(data_dir, class_name)
    for img_name in os.listdir(class_dir):
        img_path = os.path.join(class_dir, img_name)
        img = cv2.imread(img_path, cv2.IMREAD_COLOR)
        img = cv2.resize(img, (img_width, img_height))
        
        # Apply preprocessing (color histogram)
        hist = cv2.calcHist([img], [0, 1, 2], None, [32, 32, 32], [0, 256, 0, 256, 0, 256])
        X.append(hist.flatten())
        y.append(label)

X = np.array(X)
y = np.array(y)

# Normalize data
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Incremental PCA (Increase number of components)
pca = IncrementalPCA(n_components=200)  # Increase number of components
X_pca = pca.fit_transform(X_scaled)

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(X_pca, y, test_size=0.2, random_state=42)

# Handle class imbalance
class_weights = compute_class_weight('balanced', classes=np.unique(y_train), y=y_train)
class_weight_dict = {i: class_weights[i] for i in range(len(class_weights))}

# Random Forest with GridSearchCV for hyperparameter tuning
param_grid = {
    'n_estimators': [100, 300, 500],
    'max_depth': [10, 20, 30],
    'min_samples_split': [2, 4],
    'min_samples_leaf': [1, 2],
    'max_features': ['sqrt', 'log2']
}

grid_search = GridSearchCV(estimator=RandomForestClassifier(class_weight=class_weight_dict, random_state=42),
                           param_grid=param_grid, cv=3, n_jobs=-1, verbose=2)
grid_search.fit(X_train, y_train)

# Best model after hyperparameter tuning
rf_model = grid_search.best_estimator_

# Train and evaluate model using cross-validation
scores = cross_val_score(rf_model, X_pca, y, cv=5)
print(f"Cross-validated accuracy: {scores.mean() * 100:.2f}%")

# Alternatively, train the model directly if you want to evaluate on the test set
rf_model.fit(X_train, y_train)
y_pred = rf_model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Test set accuracy: {accuracy * 100:.2f}%")

# Save models
joblib.dump(rf_model, os.path.join(settings.BASE_DIR, 'skin_disease_rf_model.pkl'))
joblib.dump(pca, os.path.join(settings.BASE_DIR, 'pca_model.pkl'))
joblib.dump(scaler, os.path.join(settings.BASE_DIR, 'scaler.pkl'))
