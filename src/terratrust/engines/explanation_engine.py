"""Engine E: Explanation and Quality Engine.

Tracks data provenance, audits input validity, generates transparent mathematical breakdowns,
and enforces regulatory credit risk gating (prohibiting unverified probability of default).
"""

from typing import Any, Dict, List, Optional
from terratrust.contracts.schemas import (
    EvidenceStatus,
    FinancialAssessmentRequest,
    FinancialAssessmentResponse,
    ProvenanceItem,
    QualityAndAuditReport,
    YieldPredictionRequest,
)


class ExplanationEngine:
    """Engine E — Explanation and Quality Engine."""

    REGULATORY_GATING_RATIONALE = (
        "Under financial governance and banking regulations (RBI/BCBS), loan repayment "
        "probabilities cannot be simulated or estimated without an empirically audited credit loss "
        "dataset containing historical loan default labels. This system evaluates physical agronomic "
        "yield and farm cash flow for human credit committee decision support."
    )

    def audit_assessment(
        self,
        yield_request: Optional[YieldPredictionRequest],
        yield_prediction: Optional[float],
        fin_request: FinancialAssessmentRequest,
        fin_response: FinancialAssessmentResponse,
        scenario_assumptions: Optional[Dict[str, Any]] = None,
    ) -> QualityAndAuditReport:
        """Compile comprehensive data provenance, data quality score, and regulatory audit dossier."""
        provenance: List[ProvenanceItem] = []
        warnings: List[str] = []
        limitations: List[str] = []

        # 1. Yield & Soil Nutrients Provenance
        if yield_request is not None:
            provenance.append(
                ProvenanceItem(
                    feature_name="Soil Nutrients (N, P, K, Fertilizer)",
                    value=f"N={yield_request.N}, P={yield_request.P}, K={yield_request.K}, Fert={yield_request.Fertilizer}",
                    evidence_status=EvidenceStatus.USER_ENTERED,
                    source_description="Farmer-declared Soil Health Card observation",
                )
            )
            provenance.append(
                ProvenanceItem(
                    feature_name="Growing Temperature",
                    value=f"{yield_request.temp} °C",
                    evidence_status=EvidenceStatus.OBSERVED,
                    source_description="Open-Meteo High-Resolution Reanalysis Grid",
                )
            )
            if yield_request.temp > 42.0:
                warnings.append("Growing temperature exceeds 42C; severe thermal inhibition may occur.")
            if yield_request.N < 10.0:
                warnings.append("Critically low soil Nitrogen (< 10 ppm) detected.")

        if yield_prediction is not None:
            provenance.append(
                ProvenanceItem(
                    feature_name="Physical Crop Yield Estimate",
                    value=f"{yield_prediction} tonnes/ha",
                    evidence_status=EvidenceStatus.MODEL_ESTIMATED,
                    source_description="ExtraTreesRegressor agronomic inference pipeline (v1.0.0)",
                )
            )

        # 2. Market & Farm Parameters Provenance
        provenance.append(
            ProvenanceItem(
                feature_name="Commodity Market Price",
                value=f"{fin_request.currency} {fin_request.expected_price_per_tonne:,.2f}/tonne",
                evidence_status=EvidenceStatus.OBSERVED,
                source_description="Agmarknet APMC Mandi Statutory Minimum Support Price (MSP/FRP)",
            )
        )
        provenance.append(
            ProvenanceItem(
                feature_name="Cultivated Farm Area",
                value=f"{fin_request.farm_area_ha} hectares",
                evidence_status=EvidenceStatus.USER_ENTERED,
                source_description="Land Revenue Record / Cadastral Plot Registration",
            )
        )
        provenance.append(
            ProvenanceItem(
                feature_name="Production & Operating Costs",
                value=f"{fin_request.currency} {fin_request.production_costs:,.2f}",
                evidence_status=EvidenceStatus.USER_ENTERED,
                source_description="Farm operational input expenditure statement",
            )
        )

        # 3. Scenario Shocks Provenance
        if scenario_assumptions:
            provenance.append(
                ProvenanceItem(
                    feature_name="Climate / Market Stress Scenario",
                    value=str(scenario_assumptions.get("scenario_code", "CUSTOM")),
                    evidence_status=EvidenceStatus.SCENARIO_ASSUMPTION,
                    source_description="Credit committee sensitivity stress test parameter",
                )
            )

        # 4. Data Quality Score calculation
        quality_score = 100.0
        if len(warnings) > 0:
            quality_score -= len(warnings) * 10.0
        if fin_request.post_harvest_loss_pct > 0.25:
            warnings.append("High post-harvest loss (> 25%) declared; requires on-site verification.")
            quality_score -= 10.0

        quality_score = max(50.0, min(100.0, quality_score))

        limitations.extend([
            "Physical crop yield model does not incorporate unobserved catastrophic pest outbreaks.",
            "Farm income does not account for intra-season commodity price hedging instruments.",
            "Decision support output; final lending decision rests with authorized human loan committee.",
        ])

        return QualityAndAuditReport(
            provenance=provenance,
            data_quality_score=quality_score,
            probability_of_default_status="PD_UNAVAILABLE",
            gating_rationale=self.REGULATORY_GATING_RATIONALE,
            human_in_the_loop_required=True,
            warnings=warnings,
            limitations=limitations,
        )
