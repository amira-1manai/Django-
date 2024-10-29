import joblib
import numpy as np

# Load the trained model
model = joblib.load('predictions/model.pkl')

def predict_irrigation(inputs):

    soil_type_mapping = {'Loam': 0, 'Clay': 1, 'Sandy': 2}
    crop_type_mapping = {'Corn': 0, 'Wheat': 1, 'Rice': 2}
    
    # Prepare the input for the model
    encoded_inputs = np.array([
        inputs['temperature'],
        inputs['humidity'],
        inputs['rainfall'],
        soil_type_mapping[inputs['soil_type']],
        crop_type_mapping[inputs['crop_type']]
    ]).reshape(1, -1)  # Reshape to fit the model input

    # Make a prediction
    prediction = model.predict(encoded_inputs)

    return prediction[0]  # Return the predicted irrigation amount
