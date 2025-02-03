#  README - Housing Model avec MLflow et Docker

##  Introduction
Ce projet met en place un modèle de prédiction du prix des maisons en Californie en utilisant **MLflow** pour le suivi des expériences et **Docker** pour le déploiement du modèle en tant que service API.

---

##  Structure du projet
```
/housing-adam-saidane
│── housing-model
│   ├── mlruns/                  # Expériences MLflow
│   ├── app.py                   # Script d'application
│   ├── load_data.py             # Script de préparation des données
│   ├── requirements.txt         # Dépendances
│   ├── scatterplots.png         # Visualisation
│   ├── boxplots.png             # Visualisation
│   ├── geo_scatterplot.png      # Visualisation
│   ├── docker-compose.yaml      # Docker Compose pour l'API
│   ├── meta.yaml                # Fichier MLflow
│   ├── TP 3 ML flow.docx        # Documentation
│── housing-api/                 # API Flask pour l'intégration
│── .gitignore                   # Fichiers ignorés par Git
│── .gitattributes                # Attributs Git
```

---

##  Installation

### 1️ Cloner le projet
```sh
git clone https://github.com/admm7/housing-adam-saidane.git
cd housing-adam-saidane/housing-model
```

### 2️ Installer les dépendances
```sh
pip install -r requirements.txt
```

### 3️ Lancer MLflow Tracking Server (optionnel)
```sh
mlflow ui --host 0.0.0.0 --port 5000
```
---

##  Entraînement et Suivi avec MLflow

### 4️ Charger et nettoyer les données
```sh
python load_data.py
```

### 5️ Entraîner les modèles avec MLflow
```sh
python app.py
```
*Ce script exécute plusieurs modèles (RandomForest, LinearRegression, GradientBoosting) et enregistre les métriques sur MLflow.*

### 6️ Vérifier les expérimentations sur MLflow
Accédez à **MLflow UI** via :
```
http://127.0.0.1:5000
```

---

##  Dockerisation et Déploiement

### 7️ Construire l'image Docker
```sh
docker build -t housing-model .
```

### 8️ Lancer le conteneur Docker
```sh
docker run -p 5001:8000 housing-model
```

### 9️ Vérifier si le modèle tourne
```sh
curl http://127.0.0.1:5001/
```

---

##  Tester l'API

###  Faire une requête POST à l'API Dockerisée
```sh
curl -X POST http://127.0.0.1:5001/invocations \
     -H "Content-Type: application/json" \
     -d '{"dataframe_split": {"columns": [
         "longitude", "latitude", "housing_median_age", "total_rooms", "total_bedrooms",
         "population", "households", "median_income", "ocean_proximity_NEAR BAY"],
         "data": [[-122.23, 37.88, 41.0, 880.0, 129.0, 322.0, 126.0, 8.3252, 1]]
     }}'
```

 **Sortie attendue :**
```json
{"predictions": [482947.76]}
```

---

##  Pusher sur GitHub
```sh
git add .
git commit -m "Mise à jour du modèle housing-model"
git push origin main
```

---

##  Conclusion
- **MLflow** est utilisé pour le suivi des expériences et le logging des modèles.
- **Docker** permet le déploiement du modèle en tant qu'API.
- **GitHub** assure la gestion et versioning du projet.
- il faut savoir que les étapes dans le tp ou j'ai eu le plus de mal c'était le fait de pouvoir dockeriser car j'avais des soucis pour trouver les bons artefacts
- donc c'était souvent des erreurs de chemin qui posait problème
- mais j'ai malgré tout réussi à surmonter ces différentes diffcultés et j'ai fini ce tp par dockeriser avec ML flow , vous trouverez également un fichier word comme pour chaque tp, montrant les différentes étapes que j'ai réalisé durant le tp " voir capture d'écran "

