"""End-to-End Integration Test for TerraTrust AI."""

from datetime import date
import pytest
from terratrust.contracts.schemas import (
    ClimateRequest,
    FinancialAssessmentRequest,
    ScenarioRequest,
    YieldPredictionRequest,
)
from terratrust.engines.climate_engine import ClimateEngine
from terratrust.engines.explanation_engine import ExplanationEngine
from terratrust.engines.financial_engine import FinancialEngine
from terratrust.engines.scenario_engine import ScenarioEngine
from terratrust.engines.yield_engine import YieldEngine


def test_full_workflow_integration():
    """Execute complete 5-engine pipeline from weather observation to stress scenario audit."""
    # 1. Engine A: Climate Intelligence
    climate_engine = ClimateEngine(timeout_seconds=1.0)
    climate_req = ClimateRequest(
        latitude=17.6599,
        longitude=75.9064,
        start_date=date(2026, 6, 1),
        end_date=date(2026, 10, 31),
    )
    climate_rep = climate_engine.analyze_season(climate_req)
    assert climate_rep.total_days == 153
    observed_mean_temp = climate_rep.indicators.mean_temperature_c

    # 2. Engine B: Crop-Yield ML Inference (incorporating observed temperature)
    yield_engine = YieldEngine()
    yield_req = YieldPredictionRequest(
        Fertilizer=120.0,
        temp=observed_mean_temp,
        N=45.0,
        P=35.0,
        K=40.0,
        crop_name="WHEAT",
        region="Maharashtra",
    )
    yield_rep = yield_engine.predict(yield_req)
    assert yield_rep.predicted_yield > 0.0

    # 3. Engine C: Farm Financial Cash Flow
    fin_engine = FinancialEngine()
    fin_req = FinancialAssessmentRequest(
        yield_tonnes_per_ha=yield_rep.predicted_yield,
        farm_area_ha=2.5,
        expected_price_per_tonne=25000.0,
        post_harvest_loss_pct=0.05,
        production_costs=65000.0,
        other_farm_expenses=10000.0,
        other_household_income=15000.0,
        scheduled_debt_service=55000.0,
        currency="INR",
    )
    fin_rep = fin_engine.assess_farm_finances(fin_req)
    assert fin_rep.financials.gross_revenue > 0.0
    assert fin_rep.financials.income_available_for_debt_service > 0.0

    # 4. Engine D: Climate Stress Scenario
    scenario_engine = ScenarioEngine(financial_engine=fin_engine)
    scen_req = ScenarioRequest(scenario_code="DROUGHT_SEVERE")
    scen_rep = scenario_engine.run_stress_scenario(fin_req, scen_req)
    assert scen_rep.deltas.yield_delta_pct == -35.0
    assert scen_rep.stressed.gross_revenue < scen_rep.baseline.gross_revenue

    # 5. Engine E: Explanation, Quality & Credit Gating
    exp_engine = ExplanationEngine()
    audit_rep = exp_engine.audit_assessment(
        yield_request=yield_req,
        yield_prediction=yield_rep.predicted_yield,
        fin_request=fin_req,
        fin_response=fin_rep,
        scenario_assumptions={"scenario_code": "DROUGHT_SEVERE"},
    )
    assert audit_rep.probability_of_default_status == "PD_UNAVAILABLE"
    assert audit_rep.data_quality_score >= 80.0
