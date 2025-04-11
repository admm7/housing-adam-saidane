# Importation des modules nécessaires pour l'application Flask
from flask import Flask, request, jsonify  # Flask pour créer l'API, request pour récupérer les requêtes, jsonify pour retourner des réponses JSON
from flask_sqlalchemy import SQLAlchemy  # SQLAlchemy pour interagir avec la base de données
from sqlalchemy.exc import SQLAlchemyError  # Gestion des erreurs SQLAlchemy
from config import Config  # Importation des configurations de l'application
import os  # Module OS pour gérer les variables d'environnement
from flask_migrate import Migrate  # Flask-Migrate pour gérer les migrations de la base de données

# Fix pour l'encodage UTF-8 afin d'éviter des problèmes d'affichage des caractères spéciaux
os.environ['PYTHONIOENCODING'] = 'utf-8'

# Initialisation de l'application Flask
app = Flask(__name__)

# Chargement de la configuration depuis le fichier config.py
app.config.from_object(Config)

# Initialisation de l'objet SQLAlchemy avec l'application Flask
db = SQLAlchemy(app)

# Initialisation de Flask-Migrate pour gérer les migrations de la base de données
migrate = Migrate(app, db)

# Définition du modèle House, qui représente une table dans la base de données
class House(db.Model):
    __tablename__ = 'houses'  # Nom explicite de la table

    # Définition des colonnes de la table
    id = db.Column(db.Integer, primary_key=True)  # Clé primaire unique
    longitude = db.Column(db.Float, nullable=False)  # Coordonnée géographique
    latitude = db.Column(db.Float, nullable=False)  # Coordonnée géographique
    housing_median_age = db.Column(db.Integer, nullable=False)  # Âge médian des maisons
    total_rooms = db.Column(db.Integer, nullable=False)  # Nombre total de pièces
    total_bedrooms = db.Column(db.Integer, nullable=False)  # Nombre total de chambres
    population = db.Column(db.Integer, nullable=False)  # Nombre d'habitants dans la zone
    households = db.Column(db.Integer, nullable=False)  # Nombre de ménages
    median_income = db.Column(db.Float, nullable=False)  # Revenu médian des habitants
    median_house_value = db.Column(db.Float, nullable=False)  # Valeur médiane des maisons
    ocean_proximity = db.Column(db.String, nullable=False)  # Proximité de l'océan

# Route pour tester la connexion à la base de données
@app.route('/')
def test_connection():
    try:
        db.session.execute('SELECT 1')  # Exécuter une requête simple pour tester la connexion
        return "Connexion à la base de données réussie !", 200  # Retourner un message de succès
    except SQLAlchemyError as e:
        return jsonify({"error": f"Erreur de connexion : {str(e)}"}), 500  # En cas d'erreur, retourner un message JSON

# Route pour ajouter une maison dans la base de données
@app.route('/houses', methods=['POST'])
def add_house():
    try:
        data = request.get_json()  # Récupérer les données envoyées en format JSON

        # Liste des champs obligatoires pour l'ajout d'une maison
        required_fields = [
            'longitude', 'latitude', 'housing_median_age',
            'total_rooms', 'total_bedrooms', 'population',
            'households', 'median_income', 'median_house_value', 'ocean_proximity'
        ]

        # Vérifier que tous les champs requis sont présents dans la requête
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Le champ '{field}' est manquant."}), 400

        # Création d'un nouvel objet House avec les données reçues
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

        db.session.add(new_house)  # Ajouter la nouvelle maison à la session de base de données
        db.session.commit()  # Valider l'ajout dans la base de données

        return jsonify({"message": "Maison ajoutée avec succès !"}), 201  # Retourner un message de succès

    except SQLAlchemyError as e:
        db.session.rollback()  # Annuler les changements en cas d'erreur SQL
        return jsonify({"error": f"Erreur SQL : {str(e)}"}), 400  # Retourner un message d'erreur SQL
    except Exception as e:
        return jsonify({"error": f"Erreur serveur : {str(e)}"}), 500  # Gérer toute autre erreur

# Route pour récupérer toutes les maisons enregistrées dans la base de données
@app.route('/houses', methods=['GET'])
def get_houses():
    try:
        houses = House.query.all()  # Récupérer toutes les maisons

        # Transformer les objets en dictionnaires pour les retourner en JSON
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
        return jsonify(houses_list), 200  # Retourner la liste des maisons en JSON
    except SQLAlchemyError as e:
        return jsonify({"error": f"Erreur SQL : {str(e)}"}), 500  # En cas d'erreur SQL
    except Exception as e:
        return jsonify({"error": f"Erreur serveur : {str(e)}"}), 500  # Gérer toute autre erreur

# Route de test pour vérifier le nombre d'entrées dans la base de données
@app.route('/test_db', methods=['GET'])
def test_db():
    try:
        houses = House.query.all()  # Récupérer toutes les maisons
        return f"Found {len(houses)} houses in the database.", 200  # Afficher le nombre de maisons trouvées
    except Exception as e:
        return f"Error: {str(e)}", 500  # En cas d'erreur, afficher un message

# Route de test pour vérifier le contenu de la table houses
@app.route('/test_houses', methods=['GET'])
def test_houses():
    try:
        result = db.session.execute("SELECT * FROM houses").fetchall()  # Exécuter une requête SQL pour récupérer toutes les maisons
        houses = [dict(row) for row in result]  # Transformer le résultat en liste de dictionnaires
        return jsonify(houses), 200  # Retourner les maisons en JSON
    except Exception as e:
        return jsonify({"error": str(e)}), 500  # En cas d'erreur, retourner un message JSON

# Point d'entrée de l'application Flask
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)  # Lancer l'application sur le port 5000, accessible depuis n'importe quelle adresse IP