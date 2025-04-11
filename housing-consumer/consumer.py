from confluent_kafka import Consumer, KafkaException
import requests
import json
import os

# 🔹 Détermine si Docker est utilisé
USE_DOCKER = os.getenv("USE_DOCKER", "false").lower() == "true"
KAFKA_BROKER_URL = "broker:9092" if USE_DOCKER else "localhost:29092"

consumer_config = {
    "bootstrap.servers": KAFKA_BROKER_URL,
    "group.id": "housing-group",
    "auto.offset.reset": "earliest"
}

consumer = Consumer(consumer_config)
consumer.subscribe(["housing_topic"])

# 🔹 Définition des URL de l'API pour stocker les données et des prédictions MLflow
API_URL = "http://127.0.0.1:5001/houses"  # API Flask pour stocker les données
PREDICTION_URL = "http://127.0.0.1:5002/invocations"  # MLflow Model

print("✅ Kafka Consumer démarré...")

try:
    while True:
        msg = consumer.poll(1.0)

        if msg is None:
            continue

        if msg.error():
            print(f"⚠️ Erreur Consumer: {msg.error()}")
            continue

        if msg.value() is None:
            print("⚠️ Message vide reçu, on ignore.")
            continue

        try:
            raw_message = msg.value().decode("utf-8").strip()
            print(f"📥 Message brut reçu : {raw_message}")

            data = json.loads(raw_message)
            print(f"📜 JSON Décodé : {data}")

        except json.JSONDecodeError as e:
            print(f"❌ Erreur de décodage JSON: {e}")
            print(f"❌ Message corrompu : {msg.value()}")
            continue

        # 🔹 Transformation des données pour la prédiction
        try:
            features = [
                data['longitude'], data['latitude'], data['housing_median_age'],
                data['total_rooms'], data['total_bedrooms'], data['population'],
                data['households'], data['median_income']
            ]

            prediction_payload = {
                "dataframe_split": {
                    "columns": [
                        "longitude", "latitude", "housing_median_age", "total_rooms",
                        "total_bedrooms", "population", "households", "median_income"
                    ],
                    "data": [features]
                }
            }

            prediction_response = requests.post(PREDICTION_URL, json=prediction_payload, headers={"Content-Type": "application/json"})
            prediction_response.raise_for_status()
            predicted_value = prediction_response.json()["predictions"][0]
            print(f"🔮 Prédiction du modèle: {predicted_value}")

        except requests.RequestException as e:
            print(f"❌ Erreur lors de la requête de prédiction : {e}")
            continue

        # 🔹 Envoi des données + prédiction à l'API Flask
        try:
            data["estimated_median_house_value"] = predicted_value  # Ajoute la prédiction aux données
            response = requests.post(API_URL, json=data, headers={"Content-Type": "application/json"})
            response.raise_for_status()
            print(f"✅ Données enregistrées : {response.json()}")

        except requests.RequestException as e:
            print(f"❌ Erreur lors de l'enregistrement dans l'API Flask : {e}")
            continue

except KeyboardInterrupt:
    print("\n🛑 Arrêt du Consumer...")
finally:
    consumer.close()
    print("✅ Consumer fermé proprement.")
