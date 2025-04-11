import requests

url = "http://127.0.0.1:5000/api/2.0/mlflow/registered-models/list"
response = requests.get(url)

print("Status Code:", response.status_code)

try:
    print("Response JSON:", response.json())
except requests.exceptions.JSONDecodeError:
    print("La réponse n'est pas un JSON valide")
