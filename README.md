#  Housing Price Prediction with Kafka and Flask

Ce projet implémente un système de prédiction de prix de maisons en utilisant **Kafka**, **Flask**, et **PostgreSQL**. L'architecture repose sur une communication entre plusieurs services Dockerisés :

1. Un **Producer Kafka** qui envoie des messages contenant des données sur les maisons.
2. Un **Consumer Kafka** qui écoute ces messages, les stocke dans une base de données et envoie une requête à l'API de prédiction.
3. Une **API Flask (housing-api)** qui stocke les maisons dans une base PostgreSQL.
4. Une **API Flask de prédiction (housing-model)** qui utilise un modèle de Machine Learning pour estimer le prix d'une maison.

---

##  Structure du projet

```
 tp-housing-adam-saidane
│── housing-api/                     # API Flask pour gérer les données de logement
│   │── app.py                        # Code principal de l'API Flask
│   │── config.py                     # Configuration de la base de données
│   │── data.json                      # Données JSON (si applicable)
│   │── dockerfile                     # Dockerfile pour l'API
│   │── requirements.txt               # Dépendances Python pour l'API
│
│── housing-consumer/                  # Consumer Kafka qui récupère et envoie les données
│   │── consumer.py                    # Code du consommateur Kafka
│   │── dockerfile                     # Dockerfile pour le consumer
│   │── requirements.txt               # Dépendances pour le consumer
│
│── housing-model/                      # API Flask pour les prédictions
│   │── app.py                          # Code principal de l'API de prédiction
│   │── best_model.pkl                  # Modèle entraîné sauvegardé
│   │── dockerfile                       # Dockerfile pour le modèle
│   │── requirements.txt                 # Dépendances du modèle
│   │── load_data.py                     # Script pour charger les données
│   │── housing.csv                      # Dataset original
│   │── housing_cleaned.csv              # Dataset nettoyé
│   │── Etape 3 housing-model/           # Dossier pour l'analyse et visualisation
│   │   │── geo_scatterplot.png          # Visualisation des données géographiques
│   │   │── boxplots.png                 # Boxplots des données
│   │   │── scatterplots.png             # Autres visualisations
│
│── mlflow/                              # (Optionnel) Suivi des expériences avec MLflow
│
│── venv/                                # Environnement virtuel Python
│── .gitignore                           # Fichiers et dossiers à ignorer par Git
│── docker-compose.yml                    # Configuration Docker Compose pour l'orchestration
│── producer.py                          # Script Kafka Producer
│── README.md                            # Documentation du projet
```

---

##  Démarrage du projet

### 1️⃣ Prérequis

- [Docker](https://www.docker.com/) et [Docker Compose](https://docs.docker.com/compose/)
- [Kafka](https://kafka.apache.org/)
- [Python 3.9+](https://www.python.org/)

### 2️⃣ Lancer les services

git clone https://github.com/ton-repo/tp-housing-adam-saidane.git
cd tp-housing-adam-saidane


```sh

docker-compose up --build
docker ps

```


### 3️⃣ Vérifier les services

1. **Tester l'API de gestion des maisons**  
   ➜ [http://127.0.0.1:5001/houses](http://127.0.0.1:5001/houses)

2. **Tester l'API de prédiction**  
   ➜ [http://127.0.0.1:5002](http://127.0.0.1:5002)

3. **Envoyer un message Kafka depuis le Producer**  
   ```sh
   python producer.py
   ```

4. **Vérifier que le Consumer reçoit les messages**  
   ```sh
   python consumer.py
   ```

---

## Fonctionnalités
## Endpoints de l'API

###  Ajouter une maison
```powershell
Invoke-RestMethod -Uri "http://127.0.0.1:5001/houses" -Method Post -Headers @{"Content-Type"="application/json"} -Body '{"longitude": -122.23, "latitude": 37.88, "housing_median_age": 52, "total_rooms": 880, "total_bedrooms": 129, "population": 322, "households": 126, "median_income": 8.3252, "median_house_value": 358500, "ocean_proximity": "NEAR BAY"}'
```
 **Réponse** : `"Maison ajoutée avec succès !"`

###  Consommer les données Kafka
```powershell
docker exec -it broker kafka-console-consumer --bootstrap-server broker:9092 --topic housing_topic --from-beginning
```
 **Description** : Consomme les messages du topic Kafka `housing_topic` en affichant toutes les données depuis le début.

###  Vérification du fonctionnement de l'API
```powershell
Invoke-WebRequest -Uri "http://127.0.0.1:5002" -Method GET
```
 **Réponse** : `{"message": "API is running and ready to predict!"}`

###  Prédiction du prix d'un logement
```powershell
Invoke-WebRequest -Uri "http://127.0.0.1:5002/predict" -Method POST -Headers @{"Content-Type"="application/json"} -Body '{"features": [-122.23, 37.88, 52, 880, 129, 322, 126, 8.3252, 358500, 1, 0, 0, 0]}'
```
 **Réponse** : `{"prediction": 443793.62}`

### 🗄 Requête SQL pour afficher les logements stockés
```powershell
docker exec -it housing-db psql -U housing_user -d housing -c "SELECT * FROM houses;"
```
 **Description** : Affiche toutes les maisons enregistrées dans la base de données PostgreSQL.

---

##  Conteneurisation avec Docker (Optionnel)

1. Construire l'image Docker :
   ```bash
   docker build -t housing-api .
   ```
2. Lancer le conteneur :
   ```bash
   docker run -p 5001:5001 housing-api
   ```

---

##  Auteurs
**Adam Saidane** - Étudiant en **Cloud Engineering** à **IA Institut**.

---



