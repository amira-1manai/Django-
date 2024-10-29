import pickle
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import pandas as pd
import os


# Charger les données depuis le fichier CSV
data_file_path = 'fertilization_data.csv'
df = pd.read_csv(data_file_path)

# Définir les caractéristiques et la cible
X = df[['crop_type', 'soil_type']]
y = df['fertilizer_amount']

# Diviser les données en ensembles d'entraînement et de test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Entraîner le modèle
model = LinearRegression()
model.fit(X_train, y_train)

# Sauvegarder le modèle
current_dir = os.path.dirname(os.path.abspath(__file__))  # Récupérer le chemin du répertoire actuel
file_path = os.path.join(current_dir, 'fertilization_model.pkl')  # Chemin du fichier

# Sauvegarder le modèle
with open(file_path, 'wb') as f:
    pickle.dump(model, f)

print("Modèle entraîné et sauvegardé avec succès!")

# Charger le modèle pour vérification
try:
    with open(file_path, 'rb') as f:
        loaded_model = pickle.load(f)
    print("Modèle chargé avec succès!")
except FileNotFoundError as e:
    print(e)  # Afficher l'erreur si le fichier n'est pas trouvé
