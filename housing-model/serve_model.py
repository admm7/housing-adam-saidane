from flask import Flask, request, jsonify
import mlflow.pyfunc
import numpy as np

app = Flask(__name__)

# Charger le modèle depuis MLflow
model_name = "random-forest-model"
model = mlflow.pyfunc.load_model(f"models:/{model_name}/latest")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        input_data = np.array(data["features"]).reshape(1, -1)
        prediction = model.predict(input_data)
        return jsonify({"prediction": prediction.tolist()})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
