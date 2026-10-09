# 🌱 TerraTrust AI (FIN-03)

**Climate-Aware Agricultural Credit Risk Decision-Support System**  
*Turning Climate Uncertainty into Smarter Agricultural Credit Decisions.*

---

## 🚀 Quick Start Guide

### 1. Prerequisites
- Python 3.12+ (tested on Python 3.14)
- Node.js 18+ (tested on Node.js v24)
- Pip & npm

### 2. Running the Interactive Streamlit Decision-Support Dashboard
To run the full 5-engine interactive visual workspace:
```bash
# Set Python path and launch Streamlit
$env:PYTHONPATH="src;apps/api"
streamlit run app.py
```
Access in your browser at: **`http://localhost:8501`**

---

### 3. Running the Enterprise Full-Stack Service (FastAPI + React)

#### Start the FastAPI Backend (Port 8000)
```bash
cd apps/api
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```
- Interactive Swagger API Docs: **`http://localhost:8000/api/v1/docs`**
- Health Probe: **`http://localhost:8000/health`**

#### Start the React / Vite Frontend (Port 3000)
```bash
npm install
npm run dev
```
- Institutional Web Portal: **`http://localhost:3000`**
- **Default Officer Login**: `officer@fin03.local` / `password123`
- **Default Risk Analyst Login**: `analyst@fin03.local` / `password123`

---

## 🧩 The 5 Core Engines

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
                 └──────────────────────────┘
```

1. **Engine A: Climate Intelligence Engine** ([`src/terratrust/engines/climate_engine.py`](src/terratrust/engines/climate_engine.py))
   - Ingests Open-Meteo live historical reanalysis & IMD gridded telemetry.
   - Calculates GDD, heat stress days (>35°C), maximum dry spells, and historical climate anomalies.
2. **Engine B: Crop-Yield ML Engine** ([`src/terratrust/engines/yield_engine.py`](src/terratrust/engines/yield_engine.py))
   - Loads `terratust_crop_yield_model.pkl` (`ExtraTreesRegressor` pipeline with `SimpleImputer`).
   - Evaluates continuous agronomic nutrients (`Fertilizer, temp, N, P, K`).
   - Achieves $R^2=0.9917$, MAE $=0.114$ tonnes/ha against held-out partition; provides $\pm 10\%$ uncertainty intervals.
3. **Engine C: Farm Financial Engine** ([`src/terratrust/engines/financial_engine.py`](src/terratrust/engines/financial_engine.py))
   - Computes Total & Saleable Production, Gross Revenue, Production Costs, Net Farm Income, IADS, and DSCR.
4. **Engine D: Climate Stress Scenario Engine** ([`src/terratrust/engines/scenario_engine.py`](src/terratrust/engines/scenario_engine.py))
   - Simulates drought, heatwaves, flood waterlogging, and commodity price slumps.
   - Calculates baseline vs. stressed financial and DSCR deltas.
5. **Engine E: Explanation and Quality Engine** ([`src/terratrust/engines/explanation_engine.py`](src/terratrust/engines/explanation_engine.py))
   - Tracks data provenance (`OBSERVED`, `USER_ENTERED`, `MODEL_ESTIMATED`, `SCENARIO_ASSUMPTION`).
   - Enforces regulatory credit risk gating: **Probability of Default is strictly `PD_UNAVAILABLE`** to comply with banking governance.

---

## 🧪 Running Automated Tests

```bash
# Run Core Python Engine Test Suite (11 tests)
$env:PYTHONPATH="src;apps/api"
python -m pytest tests/ -v

# Run Full Backend API Test Suite (71 tests)
python -m pytest apps/api/tests/ -v

# Run Frontend Vitest Test Suite (157 tests)
npm run test
```

---

## 📚 Documentation Index
- [Implementation Audit](docs/IMPLEMENTATION_AUDIT.md)
- [Model Inventory](docs/MODEL_INVENTORY.md)
- [Engine Contracts & Interfaces](docs/ENGINE_CONTRACTS.md)
- [Engine A Specification](docs/ENGINE_A_CLIMATE_INTELLIGENCE.md)
- [Data Pipeline & Strategy](docs/DATA_PIPELINE.md)
- [Automated Testing Report](docs/TESTING_REPORT.md)
