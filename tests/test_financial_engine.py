"""Unit tests for Engine C: Farm Financial Engine."""

import pytest
from terratrust.contracts.schemas import FinancialAssessmentRequest, RiskBand
from terratrust.engines.financial_engine import FinancialEngine


def test_financial_engine_standard_assessment():
    engine = FinancialEngine()
    req = FinancialAssessmentRequest(
        yield_tonnes_per_ha=3.84,
        farm_area_ha=2.5,
        expected_price_per_tonne=25000.0,
        post_harvest_loss_pct=0.05,
        production_costs=65000.0,
        other_farm_expenses=10000.0,
        other_household_income=15000.0,
        scheduled_debt_service=55000.0,
        currency="INR",
    )
    res = engine.assess_farm_finances(req)

    # 3.84 * 2.5 = 9.60 tonnes
    assert res.production.total_production_tonnes == 9.60
    # 9.60 * 0.05 = 0.48 tonnes loss
    assert res.production.post_harvest_loss_tonnes == 0.48
    # 9.12 tonnes saleable
    assert res.production.saleable_production_tonnes == 9.12
    # 9.12 * 25000 = 228,000 INR Gross Revenue
    assert res.financials.gross_revenue == 228000.0
    # Total costs = 65000 + 10000 = 75000
    assert res.financials.total_costs == 75000.0
    # Net Income = 228000 - 75000 = 153000
    assert res.financials.net_farm_income == 153000.0
    # IADS = 153000 + 15000 = 168000
    assert res.financials.income_available_for_debt_service == 168000.0
    # DSCR = 168000 / 55000 = 3.05
    assert res.financials.debt_service_coverage_ratio == 3.05
    assert res.risk_band == RiskBand.LOW
    assert not res.zero_debt_flag


def test_financial_engine_zero_debt_handling():
    engine = FinancialEngine()
    req = FinancialAssessmentRequest(
        yield_tonnes_per_ha=2.0,
        farm_area_ha=1.0,
        expected_price_per_tonne=20000.0,
        production_costs=15000.0,
        scheduled_debt_service=0.0,  # Zero debt
    )
    res = engine.assess_farm_finances(req)
    assert res.zero_debt_flag is True
    assert res.financials.debt_service_coverage_ratio is None
    assert res.coverage_status == "NO_DEBT_OBLIGATIONS"
