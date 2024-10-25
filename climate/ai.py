from django.http import JsonResponse
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from django.http import JsonResponse

def ai(request):
    # Sample DataFrame creation (you would replace this with your actual data)
    data = {
        'crop_type': ['wheat', 'corn', 'soybean', 'rice', 'wheat'],
        'temperature': [25, 30, 28, 26, 27],
        'humidity': [60, 55, 65, 70, 60],
        'rainfall': [10, 20, 15, 25, 5],
        'soil_type': ['clay', 'sandy', 'loamy', 'peaty', 'clay'],
        'irrigation_need': [5, 10, 7, 12, 4]  # Target variable
    }

    df = pd.DataFrame(data)

    # Features and target variable
    X = df.drop('irrigation_need', axis=1)
    y = df['irrigation_need']

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Preprocessing for categorical variables with unknown handling
    preprocessor = ColumnTransformer(
        transformers=[
            ('cat', OneHotEncoder(handle_unknown='ignore'), ['crop_type', 'soil_type']),
        ],
        remainder='passthrough'  # Keep numerical columns
    )

    # Create a pipeline with preprocessing and the model
    pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('model', RandomForestRegressor(n_estimators=100, random_state=42))
    ])

    # Fit the model
    pipeline.fit(X_train, y_train)

    # Make predictions
    y_pred = pipeline.predict(X_test)

    # Evaluate the model
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    # Example prediction with new data
    new_data = pd.DataFrame({
        'crop_type': ['corn'],  # Ensure this is in line with training data categories
        'temperature': [29],
        'humidity': [58],
        'rainfall': [12],
        'soil_type': ['sandy']
    })

    predicted_irrigation = pipeline.predict(new_data)

    # Prepare the JSON response
    response_data = {
        'mean_absolute_error': mae,
        'mean_squared_error': mse,
        'r_squared': r2,
        'predicted_irrigation': predicted_irrigation[0],
    }

    return JsonResponse(response_data)
