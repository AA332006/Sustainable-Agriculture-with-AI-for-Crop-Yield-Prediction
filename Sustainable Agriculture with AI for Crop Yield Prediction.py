# -*- coding: utf-8 -*-
"""Untitled3.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1er-iNHXgfOwyyANphuD6-lg56WIYr0Hb
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
from sklearn.model_selection import RandomizedSearchCV
import numpy as np

# Load the dataset
df = pd.read_csv("Agri.csv")

# Encode categorical variables
label_encoder = LabelEncoder()
df["Soilcolor"] = label_encoder.fit_transform(df["Soilcolor"])
df["label"] = label_encoder.fit_transform(df["label"])  # Target variable

# Split features and target
X = df.drop(columns=["label"])
y = df["label"]

# Standardize numerical features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Split into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Hyperparameter tuning using RandomizedSearchCV
param_dist = {
    'n_estimators': np.arange(50, 300, 50),
    'max_depth': [None, 10, 20],
    'min_samples_split': [2, 5],
    'min_samples_leaf': [1, 2]
}

random_search = RandomizedSearchCV(RandomForestClassifier(random_state=42), param_dist, n_iter=10, cv=3, n_jobs=-1, verbose=1, random_state=42)
random_search.fit(X_train, y_train)

# Best model after tuning
best_model = random_search.best_estimator_

# Make predictions
y_pred = best_model.predict(X_test)

# Calculate accuracy
accuracy = accuracy_score(y_test, y_pred)

# Plot model performance
plt.figure(figsize=(6, 4))
plt.bar(["Tuned Random Forest"], [accuracy], color=['green'])
plt.ylim(0, 1)
plt.ylabel("Accuracy")
plt.title("Improved Model Performance on Crop Prediction")
plt.show()

# Print accuracy
print(f"Improved Model Accuracy: {accuracy * 100:.2f}%")