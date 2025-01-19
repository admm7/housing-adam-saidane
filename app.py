from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text  # Importer text pour les requêtes SQL explicites
from config import Config
import os

# Fix pour l'encodage UTF-8
os.environ['PYTHONIOENCODING'] = 'utf-8'

# Initialisation de l'application Flask et de SQLAlchemy
app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

# Définir le modèle House correspondant à la table `houses` dans PostgreSQL
class House(db.Model):
    __tablename__ = 'houses'

    id = db.Column(db.Integer, primary_key=True)
    longitude = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    housing_median_age = db.Column(db.Integer, nullable=False)
    total_rooms = db.Column(db.Integer, nullable=False)
    total_bedrooms = db.Column(db.Integer, nullable=False)
    population = db.Column(db.Integer, nullable=False)
    households = db.Column(db.Integer, nullable=False)
    median_income = db.Column(db.Float, nullable=False)
    median_house_value = db.Column(db.Float, nullable=False)
    ocean_proximity = db.Column(db.String, nullable=False)

# Route pour tester la connexion à la base de données
@app.route('/')
def test_connection():
    try:
        # Test de la connexion
        db.session.execute(text('SELECT 1'))
        return "Connexion à la base de données réussie !"
    except Exception as e:
        # Débogage : Affichez les informations exactes de l'erreur
        return f"Erreur de connexion : {e}, Position : {e.args if hasattr(e, 'args') else 'Pas de détails supplémentaires'}"

# Route pour ajouter une maison dans la base de données
@app.route('/houses', methods=['POST'])
def add_house():
    try:
        # Récupérer les données JSON envoyées dans la requête
        data = request.get_json()

        # Vérifier que toutes les clés nécessaires sont présentes
        required_fields = [
            'longitude', 'latitude', 'housing_median_age',
            'total_rooms', 'total_bedrooms', 'population',
            'households', 'median_income', 'median_house_value', 'ocean_proximity'
        ]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Le champ '{field}' est manquant."}), 400

        # Créer une instance du modèle House
        new_house = House(
            longitude=data['longitude'],
            latitude=data['latitude'],
            housing_median_age=data['housing_median_age'],
            total_rooms=data['total_rooms'],
            total_bedrooms=data['total_bedrooms'],
            population=data['population'],
            households=data['households'],
            median_income=data['median_income'],
            median_house_value=data['median_house_value'],
            ocean_proximity=data['ocean_proximity']
        )

        # Ajouter la maison à la base de données
        db.session.add(new_house)
        db.session.commit()

        return jsonify({"message": "Maison ajoutée avec succès !"}), 201
    except Exception as e:
        db.session.rollback()  # Annuler les modifications en cas d'erreur
        return jsonify({"error": str(e)}), 400

# Route pour récupérer toutes les maisons
@app.route('/houses', methods=['GET'])
def get_houses():
    try:
        houses = House.query.all()
        houses_list = [
            {
                "id": house.id,
                "longitude": house.longitude,
                "latitude": house.latitude,
                "housing_median_age": house.housing_median_age,
                "total_rooms": house.total_rooms,
                "total_bedrooms": house.total_bedrooms,
                "population": house.population,
                "households": house.households,
                "median_income": house.median_income,
                "median_house_value": house.median_house_value,
                "ocean_proximity": house.ocean_proximity
            }
            for house in houses
        ]
        return jsonify(houses_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
