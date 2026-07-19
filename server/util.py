from typing import List, Optional, Any
import pickle
import json
import numpy as np
import os

__locations = None
__data_columns = None
__model = None

def get_estimated_price(location: str, sqft: float, bhk: int, bath: int) -> float:
    """
    Predicts the estimated home price using the loaded linear regression model.

    Args:
        location (str): The neighborhood name in Bangalore.
        sqft (float): Total square footage of the property.
        bhk (int): Number of bedrooms.
        bath (int): Number of bathrooms.

    Returns:
        float: Estimated price in Lakhs, rounded to 2 decimal places.
    """
    try:
        loc_index = __data_columns.index(location.lower())
    except ValueError:
        loc_index = -1

    x = np.zeros(len(__data_columns))
    x[0] = sqft
    x[1] = bath
    x[2] = bhk
    
    if loc_index >= 0:
        x[loc_index] = 1

    # Notice: No [0] immediately after __model!
    return round(__model.predict([x])[0], 2)

def load_saved_artifacts() -> None:
    """
    Loads the serialized machine learning artifacts (model and feature columns)
    from disk into memory for fast inference.
    """
    print("loading saved artifacts...start")
    global __data_columns
    global __locations
    global __model

    # Resolve paths relative to this file, not the process's working directory
    base_dir = os.path.dirname(os.path.abspath(__file__))
    artifacts_dir = os.path.join(base_dir, "artifacts")

    # Load Columns
    with open(os.path.join(artifacts_dir, "columns.json"), "r") as f:
        __data_columns = json.load(f)['data_columns']
        __locations = __data_columns[3:]  # first 3 columns are sqft, bath, bhk

    # Load Model
    if __model is None:
        with open(os.path.join(artifacts_dir, "banglore_home_prices_model.pickle"), "rb") as f:
            __model = pickle.load(f)
            
    print("loading saved artifacts...done")

def get_locations_names() -> List[str]:
    """
    Retrieves the list of valid location names that the model was trained on.

    Returns:
        List[str]: A list of neighborhood strings.
    """
    return __locations

def get_data_columns() -> List[str]:
    """
    Retrieves all feature column names used by the model.

    Returns:
        List[str]: A list of feature columns.
    """
    return __data_columns

if __name__ == '__main__':
    load_saved_artifacts()
    print(get_locations_names())
    print(get_estimated_price('1st Phase JP Nagar', 1000, 3, 3))
    print(get_estimated_price('1st Phase JP Nagar', 1000, 2, 2))
    print(get_estimated_price('Kalhalli', 1000, 2, 2))
    print(get_estimated_price('Ejipura', 1000, 2, 2))
