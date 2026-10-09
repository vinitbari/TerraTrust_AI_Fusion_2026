# TerraTrust AI — Engine Interfaces & Data Contracts

This document formalizes the input and output data contracts, types, units, and validation rules connecting the five core computational engines of TerraTrust AI.

---

## 1. Engine Dependency & Execution Flow

```
┌─────────────────────────────────────────────────────────────┐
│ 1. Data Sources & Engineering Pipeline (Weather/Soil/Farm) │
└──────────────────────────────┬──────────────────────────────┘
                               │
                ┌──────────────┴──────────────┐
                ▼                             ▼
   ┌──────────────────────────┐  ┌──────────────────────────┐
   │ Engine A: Climate Intel  │  │ Engine B: Crop Yield ML  │
   │ (Weather & Anomalies)    │  │ (Physical Yield tonnes/ha)│
   └────────────┬─────────────┘  └────────────┬─────────────┘
                │                             │
                └──────────────┬──────────────┘
                               ▼
                 ┌──────────────────────────┐
                 │ Engine C: Farm Financial │
                 │ (Revenue, IADS & DSCR)   │
                 └─────────────┬────────────┘
                               ▼
                 ┌──────────────────────────┐
                 │ Engine D: Scenario Lab   │
                 │ (Stress Shocks & Deltas) │
                 └─────────────┬────────────┘
                               ▼
                 ┌──────────────────────────┐
                 │ Engine E: Quality/Audit  │
                 │ (Provenance & PD Gate)   │
                 └─────────────┬────────────┘
                               ▼
                 ┌──────────────────────────┐
                 │ Interactive Presentation │
                 │ (Streamlit & React UI)   │
                 └──────────────────────────┘
```

---

## 2. Engine A: Climate Intelligence Engine

### 2.1 Input Contract (`ClimateRequest`)
```json
{
  "latitude": 17.6599,
  "longitude": 75.9064,
  "start_date": "2026-06-01",
  "end_date": "2026-10-31",
  "baseline_period_years": 10
}
```

### 2.2 Output Contract (`ClimateReport`)
```json
{
  "location": { "lat": 17.6599, "lon": 75.9064, "region": "Solapur, Maharashtra" },
  "growing_season": { "start": "2026-06-01", "end": "2026-10-31", "days": 153 },
  "indicators": {
    "total_rainfall_mm": 542.4,
    "mean_temperature_c": 27.8,
    "max_temperature_c": 38.2,
    "min_temperature_c": 19.4,
    "growing_degree_days": 1840.5,
    "heat_stress_days_above_35c": 14,
    "consecutive_dry_days_max": 18
  },
  "anomalies": {
    "rainfall_anomaly_pct": -12.4,
    "temperature_anomaly_c": 1.2,
    "status": "SLIGHT_DEFICIT"
  },
  "data_quality": {
    "completeness_pct": 100.0,
    "source": "Open-Meteo Historical Weather API & IMD Grid",
    "warnings": []
  }
}
```

---

## 3. Engine B: Crop-Yield ML Engine

### 3.1 Input Contract (`YieldPredictionRequest`)
```json
{
  "fertilizer_kg_per_ha": 120.0,
  "temperature_c": 26.5,
  "soil_nitrogen_ppm": 45.0,
  "soil_phosphorus_ppm": 35.0,
  "soil_potassium_ppm": 40.0,
  "crop_type": "Wheat",
  "region": "Maharashtra"
}
```

### 3.2 Output Contract (`YieldPredictionResponse`)
```json
{
  "predicted_yield": 3.84,
  "unit": "tonnes_per_hectare",
  "uncertainty_interval": {
    "lower_bound": 3.46,
    "upper_bound": 4.22,
    "confidence_level": 0.90
  },
  "baseline_comparison": {
    "regional_median_yield": 2.45,
    "lift_over_baseline_pct": 56.7
  },
  "model_metadata": {
    "model_name": "ExtraTreesRegressor",
    "version": "1.0.0",
    "status": "PROMOTED",
    "feature_schema": ["Fertilizer", "temp", "N", "P", "K"]
  },
  "limitations": [
    "Trained on experimental agronomic nutrients; does not account for catastrophic pest events."
  ]
}
```

---

## 4. Engine C: Farm Financial Engine

### 4.1 Input Contract (`FinancialAssessmentRequest`)
```json
{
  "yield_tonnes_per_ha": 3.84,
  "farm_area_ha": 2.5,
  "expected_price_per_tonne": 25000.0,
  "post_harvest_loss_pct": 0.05,
  "production_costs": 65000.0,
  "other_farm_expenses": 10000.0,
  "other_household_income": 15000.0,
  "scheduled_debt_service": 55000.0,
  "currency": "INR"
}
```

### 4.2 Output Contract (`FinancialAssessmentResponse`)
```json
{
  "production": {
    "total_production_tonnes": 9.60,
    "post_harvest_loss_tonnes": 0.48,
    "saleable_production_tonnes": 9.12
  },
  "financials": {
    "gross_revenue": 228000.0,
    "total_costs": 75000.0,
    "net_farm_income": 153000.0,
    "income_available_for_debt_service": 168000.0,
    "scheduled_debt_service": 55000.0,
    "debt_service_coverage_ratio": 3.05,
    "currency": "INR"
  },
  "coverage_status": "STRONG_COVERAGE",
  "zero_debt_flag": false
}
```

---

## 5. Engine D: Climate Stress Scenario Engine

### 5.1 Input Contract (`ScenarioRequest`)
```json
{
  "scenario_code": "DROUGHT_SEVERE",
  "custom_yield_delta_pct": null,
  "custom_price_delta_pct": null,
  "custom_cost_delta_pct": null
}
```

### 5.2 Output Contract (`ScenarioResponse`)
```json
{
  "scenario_code": "DROUGHT_SEVERE",
  "evidence_status": "EVIDENCE_BACKED",
  "description": "Severe 50% precipitation deficit with terminal heat stress at grain filling.",
  "baseline": {
    "yield_tonnes_per_ha": 3.84,
    "gross_revenue": 228000.0,
    "net_farm_income": 153000.0,
    "iads": 168000.0,
    "dscr": 3.05,
    "risk_band": "LOW"
  },
  "stressed": {
    "yield_tonnes_per_ha": 2.50,
    "gross_revenue": 163020.0,
    "net_farm_income": 80520.0,
    "iads": 95520.0,
    "dscr": 1.74,
    "risk_band": "MEDIUM"
  },
  "deltas": {
    "yield_delta_pct": -35.0,
    "revenue_delta_pct": -28.5,
    "net_income_delta_pct": -47.4,
    "dscr_delta": -1.31
  }
}
```

---

## 6. Engine E: Explanation, Quality & Credit Gating

### 6.1 Output Contract (`QualityAndAuditReport`)
```json
{
  "provenance_lineage": {
    "weather_data": "OBSERVED (Open-Meteo & IMD Grid)",
    "soil_nutrients": "USER_ENTERED (Farmer Soil Card)",
    "crop_yield": "MODEL_ESTIMATED (ExtraTreesRegressor v1.0.0)",
    "market_price": "OBSERVED (Agmarknet Mandi MSP/FRP)",
    "scenario_shock": "SCENARIO_ASSUMPTION (Drought Severe -35% Yield)",
    "financial_metrics": "DETERMINISTIC_CALCULATION"
  },
  "credit_risk_gating": {
    "probability_of_default": "PD_UNAVAILABLE",
    "gate_reason": "No validated historical loan default dataset available in repository. Fabricated default probabilities are prohibited by banking regulatory policy.",
    "human_in_the_loop_required": true
  },
  "audit_trail_recorded": true,
  "warnings": []
}
```
