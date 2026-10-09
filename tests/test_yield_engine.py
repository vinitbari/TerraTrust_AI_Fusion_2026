"""Unit tests for Engine B: Crop-Yield ML Engine."""

import pytest
from terratrust.contracts.schemas import YieldPredictionRequest
from terratrust.engines.yield_engine import YieldEngine


def test_yield_engine_prediction_and_uncertainty():
    engine = YieldEngine()
    req = YieldPredictionRequest(
        Fertilizer=120.0,
        temp=26.5,
        N=45.0,
        P=35.0,
        K=40.0,
        crop_name="WHEAT",
        region="Maharashtra",
    )
    res = engine.predict(req)

    assert res.predicted_yield > 0.0
    assert res.unit == "tonnes_per_hectare"
    assert res.uncertainty_interval.lower_bound < res.predicted_yield
    assert res.uncertainty_interval.upper_bound > res.predicted_yield
    assert res.uncertainty_interval.confidence_level == 0.90
    assert res.baseline_median_yield > 0.0
    assert len(res.limitations) >= 1


def test_yield_engine_alias_mapping():
    # Remap lowercase aliases
    req = YieldPredictionRequest(
        fertilizer=100.0,
        temperature=28.0,
        nitrogen=50.0,
        phosphorus=30.0,
        potassium=40.0,
    )
    assert req.Fertilizer == 100.0
    assert req.temp == 28.0
    assert req.N == 50.0
    assert req.P == 30.0
    assert req.K == 40.0


def test_yield_engine_evaluation_metrics():
    engine = YieldEngine()
    metrics = engine.get_evaluation_metrics()
    assert metrics["r2_score"] > 0.90
    assert metrics["mae"] < 0.50
    assert metrics["rmse"] < 0.50
