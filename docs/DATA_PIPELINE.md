# TerraTrust AI — Data Pipeline & Dataset Strategy

## 1. Overview & Data Sources

TerraTrust AI harmonizes data across five operational tiers:

```
┌──────────────────────────────────────────────────────────────┐
│                    DATA SOURCE ARCHITECTURE                  │
├─────────────────────┬──────────────────┬─────────────────────┤
│     METEOROLOGY     │     EDAPHIC      │      COMMODITY      │
│  Open-Meteo & IMD   │ Soil Health Card │  Agmarknet Mandi    │
│  Rainfall, Temp     │ N, P, K, Fert    │  MSP & Spot Prices  │
├─────────────────────┼──────────────────┼─────────────────────┤
│      SATELLITE      │     FINANCIAL    │      CADASTRE       │
│  Sentinel-2 / SMAP  │ Loan Application │  Land Revenue       │
│  NDVI, EVI, Soil-M  │ Principal, Tenor │  Plot Boundary Area │
└─────────────────────┴──────────────────┴─────────────────────┘
```

---

## 2. Feature Schema & Engineering Constraints

### 2.1 Tabular Yield Feature Matrix
The primary crop yield model (`TT-CYM-01`) operates on 5 standardized numerical columns:
- `Fertilizer` (kg/ha equivalent, range $[0, 500]$)
- `temp` (mean growing temperature in °C, range $[0, 55]$)
- `N` (soil Nitrogen in ppm, range $[0, 300]$)
- `P` (soil Phosphorus in ppm, range $[0, 200]$)
- `K` (soil Potassium in ppm, range $[0, 300]$)

### 2.2 Data Imputation & Scaling
The pipeline includes `SimpleImputer(strategy='median')` fitted strictly on training data to prevent out-of-fold data leakage.

---

## 3. Benchmark Dataset Integration: Zenodo CY-Bench

- **Record URI**: `https://zenodo.org/records/13838912`
- **Feature Set**: Multi-modal time-series incorporating Sentinel-2 optical bands (B2, B3, B4, B8), NDVI, EVI, NASA SMAP root-zone soil moisture, and ERA5 weather grids.
- **Split Strategy**: Strict temporal split (Train $\le 2020$, Test $\ge 2021$) ensuring zero lookahead bias.
- **Architecture Principle**: Soil nutrient tabular models and satellite imagery models are maintained as **separate, isolated inference routes** to avoid schema degradation.
