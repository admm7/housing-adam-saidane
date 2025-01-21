# Importation des modules nécessaires
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError
from config import Config
import os
from flask_migrate import Migrate

# Fix pour l'encodage UTF-8
os.environ['PYTHONIOENCODING'] = 'utf-8'

# Initialisation de l'application Flask et de SQLAlchemy
app = Flask(__name__)
app.config.from_object(Config)  # Charger la configuration depuis le fichier config.py
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Définir le modèle House
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
        db.session.execute('SELECT 1')  # Tester une requête simple
        return "Connexion à la base de données réussie !", 200
    except SQLAlchemyError as e:
        return jsonify({"error": f"Erreur de connexion : {str(e)}"}), 500

# Route pour ajouter une maison
@app.route('/houses', methods=['POST'])
def add_house():
    try:
        data = request.get_json()
        required_fields = [
            'longitude', 'latitude', 'housing_median_age',
            'total_rooms', 'total_bedrooms', 'population',
            'households', 'median_income', 'median_house_value', 'ocean_proximity'
        ]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Le champ '{field}' est manquant."}), 400

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

        db.session.add(new_house)
        db.session.commit()
        return jsonify({"message": "Maison ajoutée avec succès !"}), 201
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": f"Erreur SQL : {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": f"Erreur serveur : {str(e)}"}), 500

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
    except SQLAlchemyError as e:
        return jsonify({"error": f"Erreur SQL : {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"Erreur serveur : {str(e)}"}), 500
    
@app.route('/test_db', methods=['GET'])
def test_db():
    try:
        houses = House.query.all()
        return f"Found {len(houses)} houses in the database.", 200
    except Exception as e:
        return f"Error: {str(e)}", 500

@app.route('/test_houses', methods=['GET'])
def test_houses():
    try:
        result = db.session.execute("SELECT * FROM houses").fetchall()
        houses = [dict(row) for row in result]
        return jsonify(houses), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Point d'entrée
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
