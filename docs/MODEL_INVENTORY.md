# TerraTrust AI — Model Inventory & Provenance Record

This document provides a systematic inventory of all Machine Learning and statistical baseline models available within the TerraTrust AI repository.

---

## 1. Inventory Summary

| Model ID | Model Name | Algorithm / Type | Target & Unit | Artifact Location | Status |
|---|---|---|---|---|---|
| `TT-CYM-01` | TerraTrust Physical Crop Yield Estimator | `ExtraTreesRegressor` (Pipeline with `SimpleImputer`) | `tonnes_per_hectare` | `apps/api/models/terratust_crop_yield_model.pkl` (33.2 MB) | **Promoted & Verified** |
| `TT-BASE-01` | Historical / Regional Median Baseline | Group-Median Regressor | `tonnes_per_hectare` | Embedded in `YieldEngine` | **Verified Baseline** |
| `TT-CYB-01` | CY-Bench Multi-Modal Sentinel/ERA5 Evaluator | Satellite & Weather Temporal Benchmark | `tonnes_per_hectare` | `scripts/cy_bench_evaluation.py` | **Evaluated Benchmark** |

---

## 2. Deep Dive: `TT-CYM-01` (Physical Crop Yield Model)

### 2.1 Technical Specifications
- **Framework**: Scikit-Learn (Serialized via Joblib / Pickle).
- **Architecture**: `sklearn.pipeline.Pipeline`
  - Step 1: `SimpleImputer(strategy='median')`
  - Step 2: `ExtraTreesRegressor(n_estimators=500, min_samples_split=10, n_jobs=-1, random_state=42)`
- **File Size**: 33,218,410 bytes (~33.2 MB).

### 2.2 Input Feature Schema
The model consumes exactly 5 continuous numeric agronomic and meteorological features:

| Feature Key | Display Name | Unit | Valid Range | Description |
|---|---|---|---|---|
| `Fertilizer` | Fertilizer Rate | kg/ha | $[0, 500]$ | Total fertilizer nutrient application rate per hectare. |
| `temp` | Mean Growing Temperature | °C | $[0, 55]$ | Average ambient air temperature during the growing season. |
| `N` | Soil Nitrogen Content | mg/kg (ppm) | $[0, 300]$ | Available elemental Nitrogen in topsoil. |
| `P` | Soil Phosphorus Content | mg/kg (ppm) | $[0, 200]$ | Available Phosphorus ($P_2O_5$) in topsoil. |
| `K` | Soil Potassium Content | mg/kg (ppm) | $[0, 300]$ | Available Potassium ($K_2O$) in topsoil. |

### 2.3 Performance Metrics & Evaluation Split
- **Dataset**: Kaggle Soil Nutrients & Crop Production Agronomic Dataset.
- **Evaluation Split**: Held-out 20% test partition (stratified random split).
- **Observed Metrics**:
  - **MAE (Mean Absolute Error)**: `0.11401` tonnes/ha
  - **RMSE (Root Mean Squared Error)**: `0.17560` tonnes/ha
  - **$R^2$ (Coefficient of Determination)**: `0.99173`

### 2.4 Governance & Agronomic Limitations
- **Synthetic/Experimental Bias**: High $R^2$ reflects controlled tabular conditions. Real-world farm yields are subject to unmeasured pest incidence, drainage constraints, and field microclimates.
- **Uncertainty Bounds**: YieldEngine bounds predictions with $\pm 10\%$ confidence intervals to represent field-level variance.
- **Credit Gating**: This model outputs **physical crop yield only**. It does NOT predict borrower default probability or creditworthiness.

---

## 3. Baseline Predictor: `TT-BASE-01`

- **Algorithm**: Training-set crop/regional median yield predictor.
- **Purpose**: Serves as a defensible dumb baseline against which the `ExtraTreesRegressor` is measured.
- **Baseline MAE**: `1.420` tonnes/ha ($R^2 = 0.00$).
- **Performance Lift**: `TT-CYM-01` reduces prediction error by over $91.9\%$ compared to the naive median baseline.

---

## 4. CY-Bench Multi-Modal Benchmark: `TT-CYB-01`

- **Purpose**: Advances the system toward multi-spectral satellite imagery and reanalysis weather data.
- **Data Inputs**: Sentinel-2 NDVI/EVI canopy vigor indices, NASA SMAP root-zone soil moisture, and ERA5 weather time series.
- **Evaluation Methodology**: Strict temporal split (Train $\le 2020$, Test $\ge 2021$) to avoid lookahead leakage.
- **Results Documented**: `docs/cy_bench_audit_report.json`.
