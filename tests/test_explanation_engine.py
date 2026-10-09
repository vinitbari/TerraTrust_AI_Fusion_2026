"""Unit tests for Engine E: Explanation and Quality Engine."""

import pytest
from terratrust.contracts.schemas import (
    EvidenceStatus,
    FinancialAssessmentRequest,
    YieldPredictionRequest,
)
from terratrust.engines.explanation_engine import ExplanationEngine
from terratrust.engines.financial_engine import FinancialEngine


def test_explanation_engine_audit_and_credit_gating():
    fin_engine = FinancialEngine()
    exp_engine = ExplanationEngine()

    yield_req = YieldPredictionRequest(
        Fertilizer=120.0,
        temp=26.5,
        N=45.0,
        P=35.0,
        K=40.0,
    )
    fin_req = FinancialAssessmentRequest(
        yield_tonnes_per_ha=3.84,
        farm_area_ha=2.5,
        expected_price_per_tonne=25000.0,
        production_costs=65000.0,
        scheduled_debt_service=55000.0,
    )
    fin_res = fin_engine.assess_farm_finances(fin_req)

    report = exp_engine.audit_assessment(
        yield_request=yield_req,
        yield_prediction=3.84,
        fin_request=fin_req,
        fin_response=fin_res,
        scenario_assumptions={"scenario_code": "DROUGHT_SEVERE"},
    )

    # 1. Verify Probability of Default is strictly gated
    assert report.probability_of_default_status == "PD_UNAVAILABLE"
    assert "banking regulations" in report.gating_rationale.lower()
    assert report.human_in_the_loop_required is True

    # 2. Verify Lineage Provenance Items
    assert len(report.provenance) >= 5
    statuses = [p.evidence_status for p in report.provenance]
    assert EvidenceStatus.USER_ENTERED in statuses
    assert EvidenceStatus.OBSERVED in statuses
    assert EvidenceStatus.MODEL_ESTIMATED in statuses
    assert EvidenceStatus.SCENARIO_ASSUMPTION in statuses

    # 3. Data Quality score
    assert report.data_quality_score >= 80.0
