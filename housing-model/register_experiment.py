import mlflow
import mlflow.sklearn

mlflow.set_tracking_uri("http://127.0.0.1:5000")

with mlflow.start_run():
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # 🔹 Enregistrer le modèle dans le tracking server (mais pas dans le registre)
    mlflow.sklearn.log_model(model, "random-forest-model")

    # 🔹 Ajouter le modèle dans le **registre de modèles**
    mlflow.register_model("runs:/{}/random-forest-model".format(mlflow.active_run().info.run_id), "random-forest-model")
