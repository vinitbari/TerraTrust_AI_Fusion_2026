"""Data contracts and validation schemas for TerraTrust AI engines."""

from datetime import date
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field, field_validator, model_validator


class EvidenceStatus(str, Enum):
    OBSERVED = "OBSERVED"
    USER_ENTERED = "USER_ENTERED"
    MODEL_ESTIMATED = "MODEL_ESTIMATED"
    EVIDENCE_BACKED = "EVIDENCE_BACKED"
    ILLUSTRATIVE_ASSUMPTION = "ILLUSTRATIVE_ASSUMPTION"
    SCENARIO_ASSUMPTION = "SCENARIO_ASSUMPTION"
    UNAVAILABLE = "UNAVAILABLE"


class RiskBand(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    SEVERE = "SEVERE"


# ==============================================================================
# Engine A: Climate Schemas
# ==============================================================================
class ClimateRequest(BaseModel):
    latitude: float = Field(..., ge=-90.0, le=90.0, description="Plot latitude")
    longitude: float = Field(..., ge=-180.0, le=180.0, description="Plot longitude")
    start_date: date = Field(..., description="Sowing or season start date")
    end_date: date = Field(..., description="Expected harvest date")
    baseline_years: int = Field(default=10, ge=1, le=30, description="Historical reference window")


class DailyWeatherRecord(BaseModel):
    date: date
    precipitation_mm: float
    temperature_mean_c: float
    temperature_max_c: float
    temperature_min_c: float


class ClimateIndicators(BaseModel):
    total_rainfall_mm: float
    mean_temperature_c: float
    max_temperature_c: float
    min_temperature_c: float
    growing_degree_days: float
    heat_stress_days_above_35c: int
    consecutive_dry_days_max: int


class ClimateAnomalies(BaseModel):
    rainfall_anomaly_pct: float
    temperature_anomaly_c: float
    status: str


class ClimateReport(BaseModel):
    latitude: float
    longitude: float
    season_start: date
    season_end: date
    total_days: int
    indicators: ClimateIndicators
    anomalies: ClimateAnomalies
    daily_records: List[DailyWeatherRecord]
    completeness_pct: float
    source: str
    warnings: List[str] = Field(default_factory=list)


# ==============================================================================
# Engine B: Yield ML Schemas
# ==============================================================================
class YieldPredictionRequest(BaseModel):
    Fertilizer: float = Field(..., ge=0.0, le=1000.0, description="Fertilizer rate (kg/ha)")
    temp: float = Field(..., ge=-10.0, le=60.0, description="Growing season temperature (C)")
    N: float = Field(..., ge=0.0, le=500.0, description="Soil Nitrogen (mg/kg)")
    P: float = Field(..., ge=0.0, le=300.0, description="Soil Phosphorus (mg/kg)")
    K: float = Field(..., ge=0.0, le=500.0, description="Soil Potassium (mg/kg)")
    crop_name: str = Field(default="WHEAT", description="Crop variety or code")
    region: str = Field(default="Maharashtra", description="Geographical zone")

    @model_validator(mode="before")
    @classmethod
    def remap_aliases(cls, data: Any) -> Any:
        if isinstance(data, dict):
            mapped = dict(data)
            if "fertilizer" in mapped and "Fertilizer" not in mapped:
                mapped["Fertilizer"] = mapped["fertilizer"]
            if "temperature" in mapped and "temp" not in mapped:
                mapped["temp"] = mapped["temperature"]
            if "nitrogen" in mapped and "N" not in mapped:
                mapped["N"] = mapped["nitrogen"]
            if "phosphorus" in mapped and "P" not in mapped:
                mapped["P"] = mapped["phosphorus"]
            if "potassium" in mapped and "K" not in mapped:
                mapped["K"] = mapped["potassium"]
            return mapped
        return data


class UncertaintyInterval(BaseModel):
    lower_bound: float
    upper_bound: float
    confidence_level: float = 0.90


class YieldPredictionResponse(BaseModel):
    predicted_yield: float
    unit: str = "tonnes_per_hectare"
    uncertainty_interval: UncertaintyInterval
    baseline_median_yield: float
    lift_over_baseline_pct: float
    model_name: str = "ExtraTreesRegressor"
    model_version: str = "1.0.0"
    status: str = "PROMOTED"
    feature_schema: List[str] = ["Fertilizer", "temp", "N", "P", "K"]
    limitations: List[str] = Field(default_factory=list)


# ==============================================================================
# Engine C: Farm Financial Schemas
# ==============================================================================
class FinancialAssessmentRequest(BaseModel):
    yield_tonnes_per_ha: float = Field(..., gt=0.0, description="Crop yield in tonnes/ha")
    farm_area_ha: float = Field(..., gt=0.0, description="Cultivated land area in hectares")
    expected_price_per_tonne: float = Field(..., gt=0.0, description="Commodity price per tonne")
    post_harvest_loss_pct: float = Field(default=0.05, ge=0.0, le=0.50, description="Post-harvest loss fraction")
    production_costs: float = Field(..., ge=0.0, description="Input costs (seeds, fertilizer, fuel, labor)")
    other_farm_expenses: float = Field(default=0.0, ge=0.0, description="Incidental farm maintenance costs")
    other_household_income: float = Field(default=0.0, ge=0.0, description="Off-farm verified income")
    scheduled_debt_service: float = Field(default=0.0, ge=0.0, description="Annual/Seasonal loan obligations")
    currency: str = Field(default="INR", description="Currency symbol/code")


class ProductionSummary(BaseModel):
    total_production_tonnes: float
    post_harvest_loss_tonnes: float
    saleable_production_tonnes: float


class FinancialMetrics(BaseModel):
    gross_revenue: float
    total_costs: float
    net_farm_income: float
    income_available_for_debt_service: float
    scheduled_debt_service: float
    debt_service_coverage_ratio: Optional[float]
    currency: str


class FinancialAssessmentResponse(BaseModel):
    production: ProductionSummary
    financials: FinancialMetrics
    coverage_status: str
    risk_band: RiskBand
    zero_debt_flag: bool
    calculation_steps: Dict[str, str] = Field(default_factory=dict)


# ==============================================================================
# Engine D: Scenario Schemas
# ==============================================================================
class ScenarioRequest(BaseModel):
    scenario_code: str
    custom_yield_delta_pct: Optional[float] = None
    custom_price_delta_pct: Optional[float] = None
    custom_cost_delta_pct: Optional[float] = None
    description: Optional[str] = None


class StressedFinancials(BaseModel):
    yield_tonnes_per_ha: float
    gross_revenue: float
    net_farm_income: float
    iads: float
    dscr: Optional[float]
    risk_band: RiskBand


class ScenarioDeltas(BaseModel):
    yield_delta_pct: float
    revenue_delta_pct: float
    net_income_delta_pct: float
    iads_delta_pct: float
    dscr_delta: Optional[float]


class ScenarioResponse(BaseModel):
    scenario_code: str
    evidence_status: EvidenceStatus
    description: str
    baseline: StressedFinancials
    stressed: StressedFinancials
    deltas: ScenarioDeltas
    changed_assumptions: Dict[str, Any]


# ==============================================================================
# Engine E: Quality & Explanation Schemas
# ==============================================================================
class ProvenanceItem(BaseModel):
    feature_name: str
    value: Any
    evidence_status: EvidenceStatus
    source_description: str


class QualityAndAuditReport(BaseModel):
    provenance: List[ProvenanceItem]
    data_quality_score: float
    probability_of_default_status: str = "PD_UNAVAILABLE"
    gating_rationale: str
    human_in_the_loop_required: bool = True
    warnings: List[str] = Field(default_factory=list)
    limitations: List[str] = Field(default_factory=list)
