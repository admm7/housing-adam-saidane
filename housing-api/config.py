import os  # Module OS pour interagir avec le système d'exploitation
from dotenv import load_dotenv  # Module dotenv pour charger les variables d'environnement depuis un fichier .env

# Charger les variables d'environnement depuis un fichier .env
load_dotenv()

# Définition de la classe de configuration de l'application Flask
class Config:
    # Construction de l'URI de connexion à la base de données PostgreSQL en utilisant les variables d'environnement
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@"  # Nom d'utilisateur et mot de passe
        f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"  # Hôte, port et nom de la base de données
    )
    
    # Désactiver le suivi des modifications SQLAlchemy pour économiser les ressources système
    SQLALCHEMY_TRACK_MODIFICATIONS = False
