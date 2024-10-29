import joblib
import os

def load_prediction_model():
    model_path = os.path.join(os.path.dirname(__file__), 'model.pkl')
    return joblib.load(model_path)

# Load the model when the server starts
model = load_prediction_model()