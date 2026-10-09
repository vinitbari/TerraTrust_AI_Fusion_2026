"""Unit tests for Engine D: Climate Stress Scenario Engine."""

import pytest
from terratrust.contracts.schemas import (
    EvidenceStatus,
    FinancialAssessmentRequest,
    RiskBand,
    ScenarioRequest,
)
from terratrust.engines.scenario_engine import ScenarioEngine


def test_scenario_engine_drought_severe():
    engine = ScenarioEngine()
    base_req = FinancialAssessmentRequest(
        yield_tonnes_per_ha=3.84,
        farm_area_ha=2.5,
        expected_price_per_tonne=25000.0,
        post_harvest_loss_pct=0.05,
        production_costs=65000.0,
        other_farm_expenses=10000.0,
        other_household_income=15000.0,
        scheduled_debt_service=55000.0,
    )
    scen_req = ScenarioRequest(scenario_code="DROUGHT_SEVERE")
    res = engine.run_stress_scenario(base_req, scen_req)

    assert res.scenario_code == "DROUGHT_SEVERE"
    assert res.evidence_status == EvidenceStatus.EVIDENCE_BACKED
    assert res.deltas.yield_delta_pct == -35.0
    assert res.stressed.gross_revenue < res.baseline.gross_revenue
    assert res.stressed.net_farm_income < res.baseline.net_farm_income
    assert res.stressed.iads < res.baseline.iads
    assert res.deltas.dscr_delta < 0.0


def test_scenario_engine_price_shock_only():
    """Verify that a price-only shock changes financial revenue without perturbing yield."""
    engine = ScenarioEngine()
    base_req = FinancialAssessmentRequest(
        yield_tonnes_per_ha=3.84,
        farm_area_ha=2.5,
        expected_price_per_tonne=25000.0,
        production_costs=65000.0,
        scheduled_debt_service=55000.0,
    )
    scen_req = ScenarioRequest(scenario_code="PRICE_SHOCK_20")
    res = engine.run_stress_scenario(base_req, scen_req)

    # Yield remains unchanged
    assert res.deltas.yield_delta_pct == 0.0
    assert res.stressed.yield_tonnes_per_ha == res.baseline.yield_tonnes_per_ha
    # Revenue decreases by exactly 20%
    assert res.deltas.revenue_delta_pct == -20.0
