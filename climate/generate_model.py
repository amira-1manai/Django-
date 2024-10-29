import pandas as pd
from sklearn.linear_model import LinearRegression
import pickle

# Prepare your dataset with equal lengths for 'capacity' and 'target'
data = {
    'capacity': [
        1000.0, 5000.0, 2000.0, 1500.0, 3000.0, 
        8000.0, 2500.0, 10000.0, 1200.0, 6000.0, 
        4500.0, 3500.0, 4000.0, 20000.0, 3000.0, 
        9000.0, 1800.0, 2200.0, 7500.0, 500.0,
        3200.0, 1600.0, 2800.0, 5500.0, 6500.0,
        4000.0, 15000.0, 1200.0, 5000.0
    ],
    'target': [
        150, 800, 300, 200, 500, 
        1500, 400, 2000, 250, 1200,
        900, 700, 800, 3000, 600, 
        1200, 350, 500, 1000, 100,
        700, 200, 400, 800, 1000,
        1500, 1000, 2000, 3000
    ]
}

# Check if both lists are the same length
assert len(data['capacity']) == len(data['target']), "Length mismatch!"

# Create the DataFrame
df = pd.DataFrame(data)

# Prepare data for training
X = df[['capacity']]
y = df['target']

# Create and train the model
model = LinearRegression()
model.fit(X, y)

# Save the model to a .pkl file
with open('water_optimization_model.pkl', 'wb') as f:
    pickle.dump(model, f)

print("Model trained and saved successfully as water_optimization_model.pkl!")
