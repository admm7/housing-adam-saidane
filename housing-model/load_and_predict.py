import mlflow.pyfunc

# Nom du modèle enregistré
model_name = "random-forest-model"

# Charger la dernière version du modèle depuis MLflow Model Registry
model = mlflow.pyfunc.load_model(f"models:/{model_name}/latest")

# Tester avec des données fictives (modifier selon ton cas)
import numpy as np
sample_data = np.array([[8.3252, 41.0, 6.9841, 1.0238, 322.0, 2.5556, 37.88, -122.23]])

# Faire une prédiction
prediction = model.predict(sample_data)
print(f"🔮 Prédiction du modèle : {prediction}")
