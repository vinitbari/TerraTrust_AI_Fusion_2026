"""Engine D: Climate Stress Scenario Engine.

Simulates bounded environmental, agronomic, and market stress shocks against baseline farm
assessments and calculates delta impacts on yield, revenue, net income, and DSCR.
"""

from typing import Any, Dict, Optional
from terratrust.contracts.schemas import (
    EvidenceStatus,
    FinancialAssessmentRequest,
    FinancialAssessmentResponse,
    RiskBand,
    ScenarioDeltas,
    ScenarioRequest,
    ScenarioResponse,
    StressedFinancials,
)
from terratrust.engines.financial_engine import FinancialEngine


class ScenarioEngine:
    """Engine D — Climate Stress Scenario Engine."""

    PREDEFINED_SCENARIOS = {
        "DROUGHT_MODERATE": {
            "yield_delta_pct": -0.15,
            "price_delta_pct": 0.05,
            "cost_delta_pct": 0.05,
            "evidence_status": EvidenceStatus.EVIDENCE_BACKED,
            "description": "Moderate 25% seasonal rainfall deficit with partial irrigation offset.",
        },
        "DROUGHT_SEVERE": {
            "yield_delta_pct": -0.35,
            "price_delta_pct": 0.10,
            "cost_delta_pct": 0.10,
            "evidence_status": EvidenceStatus.EVIDENCE_BACKED,
            "description": "Severe 50% precipitation deficit with terminal heat stress at grain filling.",
        },
        "HEAT_STRESS": {
            "yield_delta_pct": -0.20,
            "price_delta_pct": 0.0,
            "cost_delta_pct": 0.0,
            "evidence_status": EvidenceStatus.EVIDENCE_BACKED,
            "description": "Persistent daytime temperatures exceeding 35C during flowering stage.",
        },
        "FLOOD_EXCESS": {
            "yield_delta_pct": -0.40,
            "price_delta_pct": -0.05,
            "cost_delta_pct": 0.15,
            "evidence_status": EvidenceStatus.EVIDENCE_BACKED,
            "description": "Excess rainfall causing prolonged field waterlogging and fungal lodging.",
        },
        "PRICE_SHOCK_20": {
            "yield_delta_pct": 0.0,
            "price_delta_pct": -0.20,
            "cost_delta_pct": 0.0,
            "evidence_status": EvidenceStatus.EVIDENCE_BACKED,
            "description": "Mandi market price contraction of 20% due to regional supply surge or import tariff change.",
        },
        "COST_INFLATION_25": {
            "yield_delta_pct": 0.0,
            "price_delta_pct": 0.0,
            "cost_delta_pct": 0.25,
            "evidence_status": EvidenceStatus.EVIDENCE_BACKED,
            "description": "25% surge in fuel, chemical fertilizer, and harvesting machinery costs.",
        },
        "COMPOUND_SHOCK": {
            "yield_delta_pct": -0.30,
            "price_delta_pct": -0.15,
            "cost_delta_pct": 0.10,
            "evidence_status": EvidenceStatus.ILLUSTRATIVE_ASSUMPTION,
            "description": "Concurrent climate yield depression and commodity market price drop.",
        },
    }

    def __init__(self, financial_engine: Optional[FinancialEngine] = None):
        self.financial_engine = financial_engine or FinancialEngine()

    def run_stress_scenario(
        self,
        baseline_request: FinancialAssessmentRequest,
        scenario_request: ScenarioRequest,
    ) -> ScenarioResponse:
        """Apply stress perturbations to baseline farm financials and compute deltas."""
        # 1. Baseline Evaluation
        baseline_res = self.financial_engine.assess_farm_finances(baseline_request)

        # 2. Determine Perturbations
        config = self.PREDEFINED_SCENARIOS.get(
            scenario_request.scenario_code,
            {
                "yield_delta_pct": scenario_request.custom_yield_delta_pct or -0.10,
                "price_delta_pct": scenario_request.custom_price_delta_pct or 0.0,
                "cost_delta_pct": scenario_request.custom_cost_delta_pct or 0.0,
                "evidence_status": EvidenceStatus.ILLUSTRATIVE_ASSUMPTION,
                "description": scenario_request.description or "Custom user-specified stress scenario.",
            },
        )

        yield_delta = (
            scenario_request.custom_yield_delta_pct
            if scenario_request.custom_yield_delta_pct is not None
            else config["yield_delta_pct"]
        )
        price_delta = (
            scenario_request.custom_price_delta_pct
            if scenario_request.custom_price_delta_pct is not None
            else config["price_delta_pct"]
        )
        cost_delta = (
            scenario_request.custom_cost_delta_pct
            if scenario_request.custom_cost_delta_pct is not None
            else config["cost_delta_pct"]
        )
        evidence_status = config["evidence_status"]
        description = config["description"]

        # 3. Create Stressed Request
        stressed_yield = max(0.01, round(baseline_request.yield_tonnes_per_ha * (1.0 + yield_delta), 2))
        stressed_price = max(0.01, round(baseline_request.expected_price_per_tonne * (1.0 + price_delta), 2))
        stressed_prod_costs = max(0.0, round(baseline_request.production_costs * (1.0 + cost_delta), 2))

        stressed_req = FinancialAssessmentRequest(
            yield_tonnes_per_ha=stressed_yield,
            farm_area_ha=baseline_request.farm_area_ha,
            expected_price_per_tonne=stressed_price,
            post_harvest_loss_pct=baseline_request.post_harvest_loss_pct,
            production_costs=stressed_prod_costs,
            other_farm_expenses=baseline_request.other_farm_expenses,
            other_household_income=baseline_request.other_household_income,
            scheduled_debt_service=baseline_request.scheduled_debt_service,
            currency=baseline_request.currency,
        )

        stressed_res = self.financial_engine.assess_farm_finances(stressed_req)

        # 4. Compute Deltas
        base_rev = baseline_res.financials.gross_revenue
        stress_rev = stressed_res.financials.gross_revenue
        rev_delta_pct = round(((stress_rev - base_rev) / base_rev) * 100.0, 1) if base_rev != 0 else 0.0

        base_net = baseline_res.financials.net_farm_income
        stress_net = stressed_res.financials.net_farm_income
        net_delta_pct = round(((stress_net - base_net) / abs(base_net)) * 100.0, 1) if base_net != 0 else -100.0

        base_iads = baseline_res.financials.income_available_for_debt_service
        stress_iads = stressed_res.financials.income_available_for_debt_service
        iads_delta_pct = round(((stress_iads - base_iads) / abs(base_iads)) * 100.0, 1) if base_iads != 0 else -100.0

        base_dscr = baseline_res.financials.debt_service_coverage_ratio
        stress_dscr = stressed_res.financials.debt_service_coverage_ratio
        dscr_delta = round(stress_dscr - base_dscr, 2) if (base_dscr is not None and stress_dscr is not None) else None

        deltas = ScenarioDeltas(
            yield_delta_pct=round(yield_delta * 100.0, 1),
            revenue_delta_pct=rev_delta_pct,
            net_income_delta_pct=net_delta_pct,
            iads_delta_pct=iads_delta_pct,
            dscr_delta=dscr_delta,
        )

        baseline_summary = StressedFinancials(
            yield_tonnes_per_ha=baseline_request.yield_tonnes_per_ha,
            gross_revenue=base_rev,
            net_farm_income=base_net,
            iads=base_iads,
            dscr=base_dscr,
            risk_band=baseline_res.risk_band,
        )

        stressed_summary = StressedFinancials(
            yield_tonnes_per_ha=stressed_yield,
            gross_revenue=stress_rev,
            net_farm_income=stress_net,
            iads=stress_iads,
            dscr=stress_dscr,
            risk_band=stressed_res.risk_band,
        )

        changed_assumptions = {
            "yield_delta_pct": f"{yield_delta * 100:+.1f}%",
            "price_delta_pct": f"{price_delta * 100:+.1f}%",
            "cost_delta_pct": f"{cost_delta * 100:+.1f}%",
            "baseline_yield": f"{baseline_request.yield_tonnes_per_ha} tonnes/ha",
            "stressed_yield": f"{stressed_yield} tonnes/ha",
            "baseline_price": f"{baseline_request.currency} {baseline_request.expected_price_per_tonne}/tonne",
            "stressed_price": f"{baseline_request.currency} {stressed_price}/tonne",
        }

        return ScenarioResponse(
            scenario_code=scenario_request.scenario_code,
            evidence_status=evidence_status,
            description=description,
            baseline=baseline_summary,
            stressed=stressed_summary,
            deltas=deltas,
            changed_assumptions=changed_assumptions,
        )
