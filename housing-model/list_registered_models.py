import mlflow

# Création d'un client MLflow
client = mlflow.tracking.MlflowClient()

# Récupérer la liste des modèles enregistrés
registered_models = client.search_registered_models()

# Afficher les modèles enregistrés
if registered_models:
    print("📌 Modèles enregistrés dans MLflow Model Registry :")
    for model in registered_models:
        print(model)
else:
    print("⚠️ Aucun modèle enregistré trouvé dans MLflow Model Registry.")
