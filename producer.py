from confluent_kafka import Producer
import json
import time

producer_config = {
    "bootstrap.servers": "localhost:29092"
}

producer = Producer(producer_config)

message = {
    "longitude": -122.23,
    "latitude": 37.88,
    "housing_median_age": 52,
    "total_rooms": 880,
    "total_bedrooms": 129,
    "population": 322,
    "households": 126,
    "median_income": 8.3252,
    "median_house_value": 358500,
    "ocean_proximity": "NEAR BAY"
}

topic = "housing_topic"

for i in range(5):
    producer.produce(topic, key=str(i), value=json.dumps(message))
    producer.flush()
    print(f"Message {i} envoyé")
    time.sleep(1)
