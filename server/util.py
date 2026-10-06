"""
Utility module for loading the trained model and artifact data.
Provides prediction functions for property prices using a robust OOP approach.
"""
import json
import os
import pickle
import numpy as np

class HomePricePredictor:
    """Handles model loading and price estimation to avoid global state issues."""
    def __init__(self, artifacts_dir: str):
        self.artifacts_dir = artifacts_dir
        self.data_columns = []
        self.locations = []
        self.model = None

    def load_artifacts(self) -> None:
        """Loads column metadata and the trained model from disk."""
        print("Loading saved artifacts...")
        columns_path = os.path.join(self.artifacts_dir, "columns.json")
        with open(columns_path, "r") as f:
            self.data_columns = json.load(f)["data_columns"]
            self.locations = self.data_columns[3:]

        model_path = os.path.join(self.artifacts_dir, "banglore_home_prices_model.pickle")
        with open(model_path, "rb") as f:
            self.model = pickle.load(f)
        print("Artifacts loaded successfully.")

    def get_estimated_price(self, location: str, sqft: float, bhk: int, bath: int) -> float:
        """Estimates the price of a property based on its features."""
        if not self.model or not self.data_columns:
            raise RuntimeError("Model or data columns are not loaded. Call load_artifacts() first.")
            
        try:
            loc_index = self.data_columns.index(location.lower())
        except ValueError:
            loc_index = -1
            
        x = np.zeros(len(self.data_columns))
        x[0] = sqft
        x[1] = bath
        x[2] = bhk
        if loc_index >= 0:
            x[loc_index] = 1

        base_price = self.model.predict([x])[0]
        # Adjusted price as per custom business logic
        adjusted_price = base_price + (bhk * 3)
        return round(adjusted_price, 2)

    def get_location_names(self) -> list[str]:
        """Returns the list of available locations."""
        return self.locations

    def get_data_columns(self) -> list[str]:
        """Returns all feature columns used by the model."""
        return self.data_columns


# Initialize a singleton instance for backward compatibility with the existing server logic
_base_dir = os.path.dirname(os.path.abspath(__file__))
_artifacts_dir = os.path.join(_base_dir, "artifacts")
_predictor = HomePricePredictor(_artifacts_dir)


def load_saved_artifacts() -> None:
    _predictor.load_artifacts()


def get_estimated_price(location: str, sqft: float, bhk: int, bath: int) -> float:
    return _predictor.get_estimated_price(location, sqft, bhk, bath)


def get_locations_names() -> list[str]:
    return _predictor.get_location_names()


def get_data_columns() -> list[str]:
    return _predictor.get_data_columns()


if __name__ == "__main__":
    load_saved_artifacts()
    print(get_locations_names()[:5])  # print first 5 locations
    print(get_estimated_price("1st Phase JP Nagar", 1000, 3, 3))
    print(get_estimated_price("1st Phase JP Nagar", 1000, 2, 2))
