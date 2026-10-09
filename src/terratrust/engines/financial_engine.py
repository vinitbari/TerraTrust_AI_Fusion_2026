"""Engine C: Farm Financial Engine.

Performs transparent deterministic financial calculations converting physical crop yields
and market prices into Gross Revenue, Net Farm Income, IADS, and DSCR.
"""

from typing import Dict
from terratrust.contracts.schemas import (
    FinancialAssessmentRequest,
    FinancialAssessmentResponse,
    FinancialMetrics,
    ProductionSummary,
    RiskBand,
)


class FinancialEngine:
    """Engine C — Farm Financial Engine."""

    def assess_farm_finances(self, request: FinancialAssessmentRequest) -> FinancialAssessmentResponse:
        """Compute full farm financial cash-flow and debt-service capacity."""
        # 1. Physical Production Quantities
        total_production = round(request.yield_tonnes_per_ha * request.farm_area_ha, 2)
        post_harvest_loss_ratio = max(0.0, min(0.50, request.post_harvest_loss_pct))
        loss_tonnes = round(total_production * post_harvest_loss_ratio, 2)
        saleable_production = round(total_production - loss_tonnes, 2)

        # 2. Monetary Inflows & Outflows
        gross_revenue = round(saleable_production * request.expected_price_per_tonne, 2)
        total_costs = round(request.production_costs + request.other_farm_expenses, 2)
        net_farm_income = round(gross_revenue - total_costs, 2)

        # 3. Income Available for Debt Service (IADS)
        iads = round(net_farm_income + request.other_household_income, 2)

        # 4. Debt Service Coverage Ratio (DSCR)
        zero_debt = request.scheduled_debt_service <= 0.0
        if zero_debt:
            dscr = None
            risk_band = RiskBand.LOW if iads >= 0 else RiskBand.MEDIUM
            coverage_status = "NO_DEBT_OBLIGATIONS"
        else:
            dscr = round(iads / request.scheduled_debt_service, 2)
            if dscr >= 1.50:
                risk_band = RiskBand.LOW
                coverage_status = "STRONG_COVERAGE (DSCR >= 1.50x)"
            elif dscr >= 1.20:
                risk_band = RiskBand.MEDIUM
                coverage_status = "ADEQUATE_COVERAGE (1.20x - 1.49x)"
            elif dscr >= 1.00:
                risk_band = RiskBand.HIGH
                coverage_status = "TIGHT_MARGIN (1.00x - 1.19x)"
            else:
                risk_band = RiskBand.SEVERE
                coverage_status = "DEBT_SERVICE_DEFICIT (DSCR < 1.00x)"

        step_breakdown = {
            "step_1_total_production": f"{request.yield_tonnes_per_ha} tonnes/ha * {request.farm_area_ha} ha = {total_production} tonnes",
            "step_2_saleable_production": f"{total_production} tonnes * (1 - {post_harvest_loss_ratio:.2f}) = {saleable_production} tonnes",
            "step_3_gross_revenue": f"{saleable_production} tonnes * {request.currency} {request.expected_price_per_tonne}/tonne = {request.currency} {gross_revenue:,.2f}",
            "step_4_net_income": f"{request.currency} {gross_revenue:,.2f} - {request.currency} {total_costs:,.2f} = {request.currency} {net_farm_income:,.2f}",
            "step_5_iads": f"{request.currency} {net_farm_income:,.2f} + {request.currency} {request.other_household_income:,.2f} = {request.currency} {iads:,.2f}",
            "step_6_dscr": f"{request.currency} {iads:,.2f} / {request.currency} {request.scheduled_debt_service:,.2f} = {dscr}x" if not zero_debt else "No debt scheduled",
        }

        production_summary = ProductionSummary(
            total_production_tonnes=total_production,
            post_harvest_loss_tonnes=loss_tonnes,
            saleable_production_tonnes=saleable_production,
        )

        financial_metrics = FinancialMetrics(
            gross_revenue=gross_revenue,
            total_costs=total_costs,
            net_farm_income=net_farm_income,
            income_available_for_debt_service=iads,
            scheduled_debt_service=request.scheduled_debt_service,
            debt_service_coverage_ratio=dscr,
            currency=request.currency,
        )

        return FinancialAssessmentResponse(
            production=production_summary,
            financials=financial_metrics,
            coverage_status=coverage_status,
            risk_band=risk_band,
            zero_debt_flag=zero_debt,
            calculation_steps=step_breakdown,
        )
