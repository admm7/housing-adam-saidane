# Pour l'étape 2

# Housing API

Ce projet est une API Flask connectée à une base de données PostgreSQL pour gérer les informations de maisons.

## Installation

Clonez ce dépôt et installez les dépendances :

```bash
git clone https://github.com/admm7/housing-adam-saidane.git
cd housing-adam-saidane
pip install -r requirements.txt

Voici les commandes que j'ai taper pour que ça fonctionne, 
vous trouverez également un fichier word contenant les différentes captures d'écran des mes étapes réalisées

docker compose-down
docker-compose up --build

" en faisant ça, cela m'a permis de lancer les conteneur particulièrement celui de l'Api et de la base de donnée "

Cela est bien fonctionnel, et m'a donné une adresse à accéder : http://127.0.0.1:5000

En accédant à cette adresse j'avais bien un message qui me dis " Connexion à la base de données réussie !"

Ensuite j'ai tester les deux conteneurs pour vérifier leur connectivité, donc entre l'API et la base de donnée

curl http://127.0.0.1:5000/test_db'

Cela m'a bien affiché, dans l'URL http://127.0.0.1:5000/test_db,  "Found 1 houses in the database."

curl http://127.0.0.1:5000/houses

En accédant à l'URL, les données sont afficher ce qui montre bien que les deux conteneurs sont connectés entre eux


