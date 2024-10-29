import pandas as pd
import joblib
import numpy as np
import os 
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.pipeline import Pipeline

# Load synthetic data
df = pd.read_csv('irrigation_data_large.csv')

# Handle missing values (if any)
df.fillna(df.mean(), inplace=True)

# Define features and target variable
X = df[['temperature', 'humidity', 'rainfall', 'soil_type', 'crop_type']]
y = df['irrigation_amount']

# Encode categorical variables
soil_encoder = LabelEncoder()
crop_encoder = LabelEncoder()
X['soil_type'] = soil_encoder.fit_transform(X['soil_type'])
X['crop_type'] = crop_encoder.fit_transform(X['crop_type'])

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create a pipeline for scaling and training the model
pipeline = Pipeline(steps=[
    ('scaler', StandardScaler()),  # Standardizing features
    ('model', RandomForestRegressor())  # Using Random Forest Regressor
])

# Set up hyperparameter tuning
param_grid = {
    'model__n_estimators': [100, 200],
    'model__max_depth': [None, 10, 20, 30],
}

grid_search = GridSearchCV(pipeline, param_grid, cv=5, n_jobs=-1, verbose=2)
grid_search.fit(X_train, y_train)

# Best model after hyperparameter tuning
best_model = grid_search.best_estimator_

# Ensure the predictions directory exists
output_dir = 'predictions'
os.makedirs(output_dir, exist_ok=True)  # Create the directory if it does not exist

# Save the model and encoders
model_file = os.path.join(output_dir, 'model.pkl')
joblib.dump(best_model, model_file)
joblib.dump(soil_encoder, os.path.join(output_dir, 'soil_encoder.pkl'))
joblib.dump(crop_encoder, os.path.join(output_dir, 'crop_encoder.pkl'))

print(f"Best model trained and saved to {model_file}")
