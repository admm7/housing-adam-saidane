import mlflow
import mlflow.sklearn
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.datasets import fetch_california_housing

# Configurer MLflow
mlflow.set_tracking_uri("http://127.0.0.1:5000")
mlflow.set_experiment("housing_experiment")

with mlflow.start_run():
    # Charger les données
    data = fetch_california_housing()
    X_train, X_test, y_train, y_test = train_test_split(data.data, data.target, test_size=0.2, random_state=42)

    # Entraîner le modèle
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Enregistrer le modèle
    mlflow.sklearn.log_model(model, "random-forest-model")

    # Enregistrer dans le registre MLflow
    mlflow.register_model("runs:/{}/random-forest-model".format(mlflow.active_run().info.run_id), "random-forest-model")
