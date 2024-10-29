import pickle
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score

# Sample data preparation (replace this with your actual dataset)
data = {
    'Electrical_Conductivity_uS': [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000],
    'pH': [6.5, 7.0, 7.5, 8.0, 8.5, 6.0, 6.8, 7.3, 7.9, 8.1],
    'Sodium_Adsorption_Ratio': [1.0, 1.5, 2.0, 2.5, 3.0, 1.2, 1.8, 2.2, 2.8, 3.2],
    'Turbidity_NTU': [1.0, 2.0, 3.0, 4.0, 5.0, 1.5, 2.5, 3.5, 4.5, 5.5],
    'Hardness_mg_L': [100, 150, 200, 250, 300, 120, 180, 230, 270, 320],
    'Total_Dissolved_Solids_mg_L': [100, 200, 300, 400, 500, 150, 250, 350, 450, 550],
    'Chloride_mg_L': [10, 15, 20, 25, 30, 12, 18, 22, 28, 32],
    'Sulfate_mg_L': [5, 10, 15, 20, 25, 6, 11, 16, 21, 26],
    'Nitrate_mg_L': [1, 2, 3, 4, 5, 1, 3, 2, 4, 5],
    'Suitability': ['Suitable', 'Suitable', 'Not Suitable', 'Not Suitable', 'Suitable', 
                    'Suitable', 'Not Suitable', 'Suitable', 'Suitable', 'Not Suitable']
}

# Create a DataFrame
df = pd.DataFrame(data)

# Split the data into features and labels
X = df.drop('Suitability', axis=1)
y = df['Suitability']

# Split into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a model (Random Forest Classifier as an example)
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# Make predictions on the test set
y_pred = model.predict(X_test)

# Print classification report and accuracy
print("Classification Report:")
print(classification_report(y_test, y_pred))
print("Accuracy Score:", accuracy_score(y_test, y_pred))

# Save the trained model to a .pkl file
with open('water_quality_model.pkl', 'wb') as f:
    pickle.dump(model, f)

print("Model saved as water_quality_model.pkl")
