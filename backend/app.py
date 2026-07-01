from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import pickle
import numpy as np

# Create Flask app
app = Flask(__name__)
CORS(app)

# Load trained model
with open("model.pkl", "rb") as f:
    data = pickle.load(f)

model = data["model"]
encoders = data["encoders"]
columns = data["columns"]


# -----------------------------
# Home Page
# -----------------------------
@app.route("/")
def home():
    return render_template("index.html")


# -----------------------------
# Get Dropdown Options
# -----------------------------
@app.route("/options", methods=["GET"])
def options():
    return jsonify({
        "cut": list(encoders["cut"].classes_),
        "color": list(encoders["color"].classes_),
        "clarity": list(encoders["clarity"].classes_)
    })


# -----------------------------
# Predict Price
# -----------------------------
@app.route("/predict", methods=["POST"])
def predict():
    try:
        payload = request.get_json()

        row = []

        for col in columns:

            value = payload[col]

            if col in encoders:
                value = encoders[col].transform([value])[0]

            row.append(value)

        prediction = model.predict(np.array(row).reshape(1, -1))[0]

        return jsonify({
            "predicted_price": round(float(prediction), 2)
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 400


# -----------------------------
# Run Application
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)