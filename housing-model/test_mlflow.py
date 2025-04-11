import requests

url = "http://127.0.0.1:5000/api/2.0/mlflow/runs/search"
params = {"experiment_ids": ["1"], "max_results": 10}

response = requests.post(url, json=params)

print("Status Code:", response.status_code)
print("Response JSON:", response.json())
