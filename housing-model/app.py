from flask import Flask, request, jsonify
import joblib
import numpy as np

# Charger le modèle sauvegardé
model = joblib.load("best_model.pkl")

# Initialiser l'application Flask
app = Flask(__name__)

# Route pour vérifier que l'API fonctionne
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "API is running and ready to predict!"})

# Route pour effectuer une prédiction
@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Récupérer les données de la requête JSON
        data = request.get_json()
        
        # Vérifier si les données contiennent les caractéristiques nécessaires
        if "features" not in data:
            return jsonify({"error": "Les données doivent inclure une clé 'features'."}), 400
        
        # Convertir les caractéristiques en format numpy
        features = np.array(data["features"]).reshape(1, -1)
        
        # Faire une prédiction
        prediction = model.predict(features)
        
        # Renvoyer le résultat
        return jsonify({"prediction": prediction[0]})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Lancer l'application Flask
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
