from flask import Flask, request, jsonify
import joblib
import numpy as np
import json
from flask_sqlalchemy import SQLAlchemy
import os

# Charger le modèle sauvegardé
model = joblib.load("best_model.pkl")

# Initialiser l'application Flask
app = Flask(__name__)

# Configurer la base de données SQLite pour stocker les prédictions
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///predictions.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# Définir le modèle de la table Prediction
class Prediction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    features = db.Column(db.Text, nullable=False)
    predicted_value = db.Column(db.Float, nullable=False)

# Créer la table au démarrage de l'application
with app.app_context():
    db.create_all()

# Route pour vérifier que l'API fonctionne
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "API is running and ready to predict!"})

# Route pour effectuer une prédiction et l'enregistrer
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
        prediction = model.predict(features)[0]

        # Sauvegarder la prédiction dans la base de données
        new_prediction = Prediction(
            features=json.dumps(data["features"]),
            predicted_value=float(prediction)
        )
        db.session.add(new_prediction)
        db.session.commit()

        return jsonify({"prediction": prediction})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route pour récupérer toutes les prédictions enregistrées
@app.route("/predictions", methods=["GET"])
def get_predictions():
    predictions = Prediction.query.all()
    predictions_list = [
        {
            "id": p.id,
            "features": json.loads(p.features),
            "predicted_value": p.predicted_value
        }
        for p in predictions
    ]
    return jsonify(predictions_list)

# Lancer l'application Flask
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
