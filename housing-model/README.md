# README: Housing Model API

## Introduction

Cette application permet de prédire la valeur médiane des maisons en fonction de leurs caractéristiques. Elle utilise un modèle de machine learning (Random Forest Regressor) entraîné à partir du jeu de données California Housing Prices.

L'API est développée avec Flask et peut être exécutée localement ou dans un conteneur Docker. Ce fichier README fournit des instructions pour l'installation, l'utilisation et le déploiement de l'API.

---

## Fonctionnalités de l'API

### Endpoints

#### 1. Health Check
- **URL** : `/`
- **Méthode** : `GET`
- **Description** : Permet de vérifier si l'API est en cours d'exécution.
- **Réponse** :
  ```json
  {
    "message": "API is running and ready to predict!"
  }
  ```

#### 2. Prédiction
- **URL** : `/predict`
- **Méthode** : `POST`
- **Description** : Retourne la valeur médiane estimée d'une maison.
- **Données d'entrée attendues** :
  ```json
  {
    "features": [8.0, 50.0, 8000.0, 300.0, 700.0, 150.0, 3.0, -118.0, 34.0, 0.0, 1.0, 0.0, 0.0]
  }
  ```
  - Chaque valeur représente une caractéristique spécifique (par exemple, population, latitude, longitude, etc.).

- **Réponse** :
  ```json
  {
    "prediction": 197243.09
  }
  ```

---

## Prérequis

- Python 3.10+
- Docker
- Pip
- Accès à Docker Hub (facultatif pour le déploiement sur Docker Hub)

---

## Installation et Exécution Locale

### 1. Cloner le dépôt
```bash
git clone https://github.com/admm7/housing-adam-saidane.git
cd housing-adam-saidane/housing-model
```

### 2. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 3. Lancer l'application
```bash
python app.py
```

### 4. Tester l'API
- **Health Check** :
  ```bash
  curl http://127.0.0.1:5000/
  ```
- **Prédiction** :
  ```bash
  curl -X POST -H "Content-Type: application/json" -d '{"features": [8.0, 50.0, 8000.0, 300.0, 700.0, 150.0, 3.0, -118.0, 34.0, 0.0, 1.0, 0.0, 0.0]}' http://127.0.0.1:5000/predict
  ```

---

## Utilisation avec Docker

### 1. Construire l'image Docker
```bash
docker build -t housing-model .
```

### 2. Exécuter le conteneur Docker
```bash
docker run -d -p 5000:5000 housing-model
```

### 3. Tester l'API (même instructions que ci-dessus)

---

## Publier le conteneur sur Docker Hub

### 1. Taguer l'image Docker
```bash
docker tag housing-model admm7/housing-model:latest
```

### 2. Pousser l'image sur Docker Hub
```bash
docker push admm7/housing-model:latest
```

---

## Documentation

Ajoutez des informations complémentaires comme les variables d'environnement, la description des champs dans `features`, ou des exemples d'utilisation avancée.

---

## Contribution

Si vous souhaitez contribuer :
1. Forkez le dépôt.
2. Créez une branche pour vos modifications : `git checkout -b feature/ma-fonctionnalite`.
3. Envoyez une pull request.

---

## License

Ce projet est sous licence MIT. Consultez le fichier LICENSE pour plus de détails.


