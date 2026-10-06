"""
Flask API serving the home price prediction model.
Handles CORS and routes for locations and price estimation.
"""
from typing import Any

import util
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
util.load_saved_artifacts()


@app.route("/api/get_location_names", methods=["GET"])
def get_location_names() -> Any:
    response = jsonify({"locations": util.get_locations_names()})
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


@app.route("/api/predict_home_price", methods=["POST"])
def predict_home_price() -> Any:
    try:
        total_sqft = float(request.form["total_sqft"])
        location = request.form["location"]
        bhk = int(request.form["bhk"])
        bath = int(request.form["bath"])
        response = jsonify(
            {
                "estimated_price": util.get_estimated_price(
                    location, total_sqft, bhk, bath
                )
            }
        )
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response
    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    print("Starting Python Flask Server for Home Price Prediction...")
    app.run()
