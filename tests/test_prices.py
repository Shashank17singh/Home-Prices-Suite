from pathlib import Path

import home_prices_final as training
import pandas as pd
import pytest
from util import HomePricePredictor

ARTIFACTS = Path(__file__).resolve().parent.parent / "server" / "artifacts"


@pytest.fixture(scope="module")
def predictor() -> HomePricePredictor:
    model = HomePricePredictor(str(ARTIFACTS))
    model.load_artifacts()
    return model


def test_predicting_before_loading_is_an_error() -> None:
    with pytest.raises(RuntimeError, match="load_artifacts"):
        HomePricePredictor(str(ARTIFACTS)).get_estimated_price("x", 1000, 2, 2)


def test_locations_exclude_the_numeric_columns(predictor: HomePricePredictor) -> None:
    locations = predictor.get_location_names()

    assert predictor.get_data_columns()[:3] == ["total_sqft", "bath", "bhk"]
    assert locations == predictor.get_data_columns()[3:]


def test_a_larger_home_costs_more(predictor: HomePricePredictor) -> None:
    location = predictor.get_location_names()[0]

    small = predictor.get_estimated_price(location, 1000, 2, 2)
    large = predictor.get_estimated_price(location, 2500, 2, 2)

    assert large > small


def test_location_names_ignore_case(predictor: HomePricePredictor) -> None:
    location = predictor.get_location_names()[0]

    assert predictor.get_estimated_price(location.upper(), 1000, 2, 2) == pytest.approx(
        predictor.get_estimated_price(location, 1000, 2, 2)
    )


def test_an_unknown_location_still_gets_a_price(predictor: HomePricePredictor) -> None:
    assert isinstance(
        float(predictor.get_estimated_price("nowhere", 1000, 2, 2)), float
    )


@pytest.mark.parametrize(
    ("raw", "expected"),
    [("1200", 1200.0), ("1000-2000", 1500.0), ("34.46Sq. Meter", None)],
)
def test_square_feet_values_are_normalised(raw: str, expected: float | None) -> None:
    assert training.convert_sqft_to_num(raw) == expected


def test_bhk_outliers_cheaper_than_the_smaller_flats_are_removed() -> None:
    rows = [{"location": "a", "bhk": 2, "price_per_sqft": 5000} for _ in range(6)]
    rows.append({"location": "a", "bhk": 3, "price_per_sqft": 1000})
    rows.append({"location": "a", "bhk": 3, "price_per_sqft": 9000})

    kept = training.remove_bhk_outliers(pd.DataFrame(rows))

    assert 1000 not in set(kept.price_per_sqft)
    assert 9000 in set(kept.price_per_sqft)
