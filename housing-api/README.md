# Housing API - Étape 2

Ce projet est une API Flask connectée à une base de données PostgreSQL pour gérer les informations de maisons. Cette API permet d'ajouter, de récupérer et de vérifier les données des maisons stockées dans une base de données.

## Prérequis

Avant de commencer, assurez-vous d'avoir les outils suivants installés sur votre machine :
- **Docker** et **Docker Compose**
- **Git**
- **Python 3.9** ou une version compatible

## Installation et Lancement

### 1. Cloner le dépôt

Clonez ce dépôt Git en local avec la commande suivante :

```bash
git clone https://github.com/admm7/housing-adam-saidane.git
cd housing-adam-saidane
```

### 2. Installer les dépendances Python

Installez les dépendances nécessaires avec la commande suivante :

```bash
pip install -r requirements.txt
```

### 3. Lancer les conteneurs avec Docker Compose

Exécutez les commandes suivantes pour lancer les conteneurs Docker, y compris celui de l'API et de la base de données PostgreSQL :

```bash
docker-compose down
docker-compose up --build
```

Une fois les conteneurs démarrés, l'API sera accessible via l'adresse suivante :  
**http://127.0.0.1:5000**

### 4. Vérification de la connectivité des conteneurs

#### Tester la connexion à la base de données
Pour vérifier si l'API est bien connectée à la base de données, ouvrez un navigateur ou utilisez `curl` pour accéder à l'URL suivante :

```bash
curl http://127.0.0.1:5000
```

Vous devriez voir le message suivant :  
**"Connexion à la base de données réussie !"**

#### Tester les données de la base
Vous pouvez ensuite vérifier si l'API et la base de données communiquent correctement avec l'URL suivante :

```bash
curl http://127.0.0.1:5000/test_db
```

Cela devrait retourner une réponse comme :  
**"Found 1 houses in the database."**

#### Récupérer toutes les maisons
Pour récupérer les informations des maisons dans la base de données, utilisez l'URL suivante :

```bash
curl http://127.0.0.1:5000/houses
```

Cela retournera les données stockées dans la base de données sous forme de JSON.

---

## Fonctionnalités de l'API

- **GET /** : Vérifie la connexion à la base de données.
- **GET /test_db** : Vérifie la connectivité entre l'API et la base de données et retourne le nombre de maisons dans la base.
- **GET /houses** : Récupère la liste complète des maisons dans la base de données.
- **POST /houses** : Ajoute une nouvelle maison à la base de données. Exemple de corps JSON pour l'ajout :
  ```json
  {
      "longitude": -122.23,
      "latitude": 37.88,
      "housing_median_age": 41,
      "total_rooms": 880,
      "total_bedrooms": 129,
      "population": 322,
      "households": 126,
      "median_income": 8.3252,
      "median_house_value": 452600,
      "ocean_proximity": "NEAR BAY"
  }
  ```

---

## Captures d'écran

Un fichier Word contenant toutes les captures d'écran des étapes réalisées est disponible dans le dépôt pour référence.

---

