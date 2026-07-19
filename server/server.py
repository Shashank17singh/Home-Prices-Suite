from typing import Tuple, Any
from flask import Flask, request, jsonify
from flask_cors import CORS
import util

app = Flask(__name__)
CORS(app)

# Load the machine learning artifacts
util.load_saved_artifacts()

@app.route('/api/get_location_names', methods=['GET'])
def get_location_names() -> Any:
    """
    API Endpoint: Returns the list of available locations.
    
    Returns:
        Flask Response: A JSON object containing the list of locations and CORS headers.
    """
    response = jsonify({
        'locations': util.get_locations_names()
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/api/predict_home_price', methods=['POST'])
def predict_home_price() -> Any:
    """
    API Endpoint: Predicts the home price based on input form data (location, sqft, bhk, bath).
    
    Returns:
        Flask Response: A JSON object containing the estimated_price or an error message.
    """
    try:
        total_sqft = float(request.form['total_sqft'])
        location = request.form['location']
        bhk = int(request.form['bhk'])
        bath = int(request.form['bath'])

        response = jsonify({
            'estimated_price': util.get_estimated_price(location, total_sqft, bhk, bath)
        })
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == "__main__":
    print("Starting Python Flask Server for Home Price Prediction...")
    app.run()
