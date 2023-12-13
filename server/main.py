from .model_potability import water_potability
from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
ORIGIN_URL = os.getenv("ORIGIN_URL")
CORS(app, origins=[ORIGIN_URL])

@app.route("/", methods=["GET"])
def home():
    values = ["ph", "Hardness", "Solids", "Chloramines", "Sulfate", "Conductivity", "OrganicCarbon", "Trihalomethanes", "Turbidity"]
    for i, value in enumerate(values):
        values[i] = "{}: {}".format(value, float(request.args.get(value)))
    
    result = water_potability(values)
    if result.data:
        value = int(float(result.data["waterPotability"][0]["predicionPotability"]))
        return jsonify({ "Potability": "Not Potable" if value == 0 else "Potable" })
    return jsonify({ "message": "Error en la prediccion" })

if __name__ == "__main__":
    app.run(port=3000, host="0.0.0.0", debug=True)