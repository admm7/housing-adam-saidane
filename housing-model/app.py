# Importation des bibliothèques nécessaires
import mlflow  # Bibliothèque pour le suivi des expériences de Machine Learning
import mlflow.sklearn  # Module pour l'intégration de modèles scikit-learn avec MLflow
import os  # Module pour gérer les fichiers et variables d'environnement
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor  # Modèles de régression avancés
from sklearn.linear_model import LinearRegression  # Modèle de régression linéaire
from sklearn.model_selection import train_test_split  # Fonction pour diviser les données en jeu d'entraînement et de test
from sklearn.metrics import mean_squared_error, r2_score  # Métriques d'évaluation des modèles
import pandas as pd  # Bibliothèque pour manipuler les données sous forme de DataFrame

# 1. Charger les données
housing = pd.read_csv("housing.csv")  # Chargement du fichier CSV contenant les données de logement
print("Données chargées avec succès !")

# 2. Prétraitement des données
housing['total_bedrooms'].fillna(housing['total_bedrooms'].median(), inplace=True)  # Remplacement des valeurs manquantes par la médiane

# Séparation des variables explicatives (X) et de la variable cible (y)
X = housing.drop("median_house_value", axis=1)  # Suppression de la colonne cible du jeu de données
y = housing["median_house_value"]  # Stockage de la variable cible

# 3. Division des données en jeu d'entraînement et de test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print(f"Données divisées : Entraînement {X_train.shape}, Test {X_test.shape}")

# 4. Définition des modèles à tester
models = {
    "Random_Forest": RandomForestRegressor(n_estimators=10, random_state=42),  # Modèle de forêt aléatoire
    "Linear_Regression": LinearRegression(),  # Modèle de régression linéaire
    "Gradient_Boosting": GradientBoostingRegressor(random_state=42),  # Modèle de boosting de gradient
}

# 5. Configuration MLflow
print("Configuration MLflow...")
mlflow.set_tracking_uri("http://127.0.0.1:5000")  # Spécification de l'URL du serveur MLflow

# Vérification de l'existence de l'expérience MLflow
experiment_name = "Housing_Prediction"
experiment = mlflow.get_experiment_by_name(experiment_name)

if experiment is None:
    print(f"Création de l'expérience MLflow : {experiment_name}...")
    mlflow.create_experiment(experiment_name)  # Création de l'expérience si elle n'existe pas
    experiment = mlflow.get_experiment_by_name(experiment_name)

mlflow.set_experiment(experiment_name)  # Définition de l'expérience active
print(f"Expérience MLflow {experiment_name} configurée avec succès !")

# 6. Entraîner les modèles et identifier le meilleur
best_model = None  # Stockage du meilleur modèle
best_model_name = None  # Nom du meilleur modèle
best_mse = float("inf")  # Initialisation du meilleur MSE (erreur quadratique moyenne)
best_r2 = None  # Score R² du meilleur modèle

print("Début de l'entraînement des modèles...")
for model_name, model in models.items():
    try:
        print(f"Entraînement du modèle : {model_name}...")
        model.fit(X_train, y_train)  # Entraînement du modèle
        y_pred = model.predict(X_test)  # Prédictions sur l'ensemble de test
        mse = mean_squared_error(y_test, y_pred)  # Calcul du MSE
        r2 = r2_score(y_test, y_pred)  # Calcul du score R²
        print(f"{model_name} -> MSE: {mse:.2f}, R²: {r2:.2f}")

        # Mise à jour du meilleur modèle en fonction du plus bas MSE
        if mse < best_mse:
            best_mse = mse
            best_model = model
            best_model_name = model_name
            best_r2 = r2
    except Exception as e:
        print(f"Erreur avec le modèle {model_name} : {e}")

# 7. Enregistrement du meilleur modèle avec MLflow
if best_model is None:
    print("Aucun modèle entraîné avec succès. Vérifie tes données.")
    exit()

# Nettoyage du nom du modèle (remplacement des espaces et caractères spéciaux)
safe_model_name = best_model_name.replace(" ", "_").replace("-", "_")

print(f"\nMeilleur modèle : {safe_model_name} avec MSE = {best_mse:.2f} et R² = {best_r2:.2f}")

try:
    # Démarrage d'un nouveau run MLflow pour enregistrer les informations du modèle
    with mlflow.start_run(run_name=f"Best_Model_{safe_model_name}") as run:
        run_id = run.info.run_id  # Récupération de l'ID du run pour retrouver les artefacts

        # Enregistrement des paramètres et métriques
        mlflow.log_param("model_name", safe_model_name)
        mlflow.log_metric("MSE", best_mse)
        mlflow.log_metric("R2", best_r2)

        # Création d'un exemple d'entrée pour documenter le modèle
        input_example = X_test[:1]
        signature = mlflow.models.infer_signature(X_test, best_model.predict(X_test))

        # Définition du chemin où sera enregistré le modèle
        artifact_path = f"best_model_{safe_model_name}"

        # Enregistrement du modèle scikit-learn dans MLflow avec sa signature et un exemple d'entrée
        mlflow.sklearn.log_model(best_model, artifact_path, signature=signature, input_example=input_example)

        print(f"Meilleur modèle {safe_model_name} enregistré avec succès dans MLflow !")
        print(f"Artefacts stockés sous : mlruns/{run_id}/artifacts/{artifact_path}")
        print(f"View in MLflow UI: http://127.0.0.1:5000/#/experiments/{experiment.experiment_id}/runs/{run_id}")

except Exception as e:
    print(f"Erreur lors de l'enregistrement du modèle dans MLflow : {e}")

print("\nFin de l'entraînement et enregistrement du modèle !")
