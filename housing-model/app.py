import mlflow
import mlflow.sklearn
import os
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import pandas as pd

#  1. Charger les données
housing = pd.read_csv("housing.csv")
print(" Données chargées avec succès !")

#  2. Prétraitement des données
housing['total_bedrooms'].fillna(housing['total_bedrooms'].median(), inplace=True)

X = housing.drop("median_house_value", axis=1)
y = housing["median_house_value"]

#  3. Diviser les données
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print(f" Données divisées : Entraînement {X_train.shape}, Test {X_test.shape}")

#  4. Définir les modèles
models = {
    "Random_Forest": RandomForestRegressor(n_estimators=10, random_state=42),
    "Linear_Regression": LinearRegression(),
    "Gradient_Boosting": GradientBoostingRegressor(random_state=42),
}

#  5. Configuration MLflow
print("🔄 Configuration MLflow...")
mlflow.set_tracking_uri("http://127.0.0.1:5000")

experiment_name = "Housing_Prediction"
experiment = mlflow.get_experiment_by_name(experiment_name)

if experiment is None:
    print(f" Création de l'expérience MLflow : {experiment_name}...")
    mlflow.create_experiment(experiment_name)
    experiment = mlflow.get_experiment_by_name(experiment_name)

mlflow.set_experiment(experiment_name)
print(f" Expérience MLflow {experiment_name} configurée avec succès !")

#  6. Entraîner les modèles et enregistrer le meilleur
best_model = None
best_model_name = None
best_mse = float("inf")
best_r2 = None

print(" Début de l'entraînement des modèles...")
for model_name, model in models.items():
    try:
        print(f" Entraînement du modèle : {model_name}...")
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        print(f" {model_name} -> MSE: {mse:.2f}, R²: {r2:.2f}")

        if mse < best_mse:
            best_mse = mse
            best_model = model
            best_model_name = model_name
            best_r2 = r2
    except Exception as e:
        print(f"Erreur avec le modèle {model_name} : {e}")

#  7. Enregistrement propre du meilleur modèle
if best_model is None:
    print(" Aucun modèle entraîné avec succès. Vérifie tes données.")
    exit()

safe_model_name = best_model_name.replace(" ", "_").replace("-", "_")  # 🔹 Supprime les espaces

print(f"\n Meilleur modèle : {safe_model_name} avec MSE = {best_mse:.2f} et R² = {best_r2:.2f}")

try:
    with mlflow.start_run(run_name=f"Best_Model_{safe_model_name}") as run:
        run_id = run.info.run_id  # Récupérer l'ID du run pour retrouver les artefacts

        mlflow.log_param("model_name", safe_model_name)
        mlflow.log_metric("MSE", best_mse)
        mlflow.log_metric("R2", best_r2)

        input_example = X_test[:1]  # Exemple d’entrée
        signature = mlflow.models.infer_signature(X_test, best_model.predict(X_test))

        artifact_path = f"best_model_{safe_model_name}"  # 🔹 Nom propre sans espaces
        mlflow.sklearn.log_model(best_model, artifact_path, signature=signature, input_example=input_example)

        print(f" Meilleur modèle {safe_model_name} enregistré avec succès dans MLflow !")
        print(f" Artefacts stockés sous : mlruns/{run_id}/artifacts/{artifact_path}")
        print(f" View in MLflow UI: http://127.0.0.1:5000/#/experiments/{experiment.experiment_id}/runs/{run_id}")
except Exception as e:
    print(f" Erreur lors de l'enregistrement du modèle dans MLflow : {e}")

print("\n Fin de l'entraînement et enregistrement du modèle !")
