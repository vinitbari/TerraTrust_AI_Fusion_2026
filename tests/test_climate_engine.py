"""Unit tests for Engine A: Climate Intelligence Engine."""

from datetime import date
import pytest
from terratrust.contracts.schemas import ClimateRequest
from terratrust.engines.climate_engine import ClimateEngine


def test_climate_engine_analysis_deterministic():
    engine = ClimateEngine(timeout_seconds=1.0)
    req = ClimateRequest(
        latitude=17.6599,
        longitude=75.9064,
        start_date=date(2026, 6, 1),
        end_date=date(2026, 10, 31),
        baseline_years=10,
    )
    report = engine.analyze_season(req)

    assert report.total_days == 153
    assert report.indicators.total_rainfall_mm >= 0.0
    assert report.indicators.mean_temperature_c > 0.0
    assert report.indicators.growing_degree_days > 0.0
    assert report.indicators.heat_stress_days_above_35c >= 0
    assert report.indicators.consecutive_dry_days_max >= 0
    assert report.completeness_pct == 100.0
    assert len(report.daily_records) == 153
    assert report.anomalies.status in ["SEVERE_DEFICIT", "MODERATE_DEFICIT", "NORMAL_RANGE", "EXCESS_RAINFALL"]


def test_climate_engine_invalid_date_range():
    engine = ClimateEngine()
    req = ClimateRequest(
        latitude=17.6599,
        longitude=75.9064,
        start_date=date(2026, 10, 31),
        end_date=date(2026, 6, 1),  # End before start
    )
    with pytest.raises(ValueError):
        engine.analyze_season(req)
