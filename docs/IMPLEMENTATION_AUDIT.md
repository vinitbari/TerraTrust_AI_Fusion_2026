# TerraTrust AI — Repository Implementation Audit

**Problem Statement**: FIN-03 — Climate-Aware Credit Risk Assessment for Agriculture  
**Tagline**: *Turning Climate Uncertainty into Smarter Agricultural Credit Decisions.*  
**Audit Date**: October 2026  
**Auditor**: TerraTrust AI Core Engineering Team

---

## 1. Executive Summary & Repository Status

TerraTrust AI is engineered to bridge agricultural climate intelligence, agronomic crop production modeling, and farm cash-flow analytics to provide transparent, explainable decision support for rural lenders and credit committees.

This audit evaluates the codebase against the architectural blueprint, data integrity standards, and credit regulatory governance rules.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                            TERRATRUST AI WORKSPACE                          │
├──────────────────────────┬──────────────────────────┬───────────────────────┤
│       APPLICATIONS       │      CORE ENGINES        │      CONTRACTS & DATA │
│                          │                          │                       │
│  FastAPI Backend (8000)  │  Engine A: Climate       │  OpenAPI 3.1 Spec     │
│  React/Vite Web UI (3000)│  Engine B: Crop Yield ML │  JSON Schemas         │
│  Streamlit App (app.py)  │  Engine C: Farm Finance  │  Kaggle Agronomic Data│
│  SQLite / PostgreSQL DB  │  Engine D: Scenarios     │  CY-Bench Benchmark   │
│                          │  Engine E: Quality/Audit │  Open-Meteo Weather   │
└──────────────────────────┴──────────────────────────┴───────────────────────┘
```

---

## 2. Component Inventory & Verification Status

| Component / Subsystem | Path / Location | Classification | Current State & Verification Notes |
|---|---|---|---|
| **Engine A: Climate Intelligence** | `src/terratrust/engines/climate_engine.py` | **Implemented & Tested** | Live Open-Meteo weather API client with offline fallback, GDD, heat days, dry spells, historical anomalies. |
| **Engine B: Crop Yield ML** | `apps/api/models/terratust_crop_yield_model.pkl` & `src/terratrust/engines/yield_engine.py` | **Implemented & Tested** | 33.2MB ExtraTreesRegressor pipeline (`Fertilizer, temp, N, P, K`), median baseline model, error metrics ($R^2=0.9917$, MAE=0.114). |
| **Engine C: Farm Financials** | `src/terratrust/engines/financial_engine.py` | **Implemented & Tested** | Mathematical calculations for Saleable Yield, Gross Revenue, Production Costs, Net Farm Income, IADS, and DSCR. |
| **Engine D: Scenario Engine** | `src/terratrust/engines/scenario_engine.py` | **Implemented & Tested** | Stresses price, costs, explicit yield, and climate temperature/rainfall. Computes absolute and percentage deltas. |
| **Engine E: Explanation & Quality** | `src/terratrust/engines/explanation_engine.py` | **Implemented & Tested** | Data provenance, assumption tracking, calculation step breakdown, and strict credit gating (`PD_UNAVAILABLE`). |
| **FastAPI Backend Service** | `apps/api/` | **Implemented & Tested** | 43 API endpoints, SQLite/PostgreSQL persistence, JWT auth, RBAC, audit logging, health probes. 71/71 tests passing. |
| **React / Vite Frontend UI** | `apps/web/` | **Implemented & Tested** | Full single-page application with dashboard, borrower registration, farm mapping, scenario lab, PDF reports. 157/157 tests passing. |
| **Interactive Streamlit App** | `app.py` | **Implemented & Tested** | Multi-page decision-support workspace covering Overview, Climate Intelligence, Farm Assessment, Scenario Lab, and Model Evaluation. |
| **OpenAPI & JSON Schemas** | `packages/contracts/` & `openapi.yaml` | **Implemented & Tested** | Formal contract schemas for error envelopes, yield inference requests, and scenario payloads. |

---

## 3. Existing Model Artifacts & Provenance

- **Artifact**: `apps/api/models/terratust_crop_yield_model.pkl` (33,218,410 bytes)
- **Pipeline Structure**: `sklearn.pipeline.Pipeline` with `SimpleImputer(strategy='median')` and `ExtraTreesRegressor(n_estimators=500, min_samples_split=10, random_state=42)`.
- **Input Features**: `['Fertilizer', 'temp', 'N', 'P', 'K']`
- **Target**: Crop yield in `tonnes_per_hectare`.
- **Verification**: Loaded and verified in Python 3.14 with scikit-learn 1.7.2. Produces valid continuous non-negative predictions.
- **Benchmark Integration**: CY-Bench multi-modal satellite/weather benchmark audit available in `docs/cy_bench_audit_report.json`.

---

## 4. Key Regulatory & Scientific Constraints

1. **Crop Yield $\neq$ Loan Default**: Physical crop yield is distinct from financial default. Probability of default (PD) is strictly set to `PD_UNAVAILABLE` because no validated historical loan default dataset is present in this repository.
2. **Deterministic Financials**: Revenue, Net Farm Income, IADS, and DSCR are mathematical formulas and never estimated using opaque machine learning.
3. **Traceable Stress Scenarios**: Climate shocks are explicitly labeled as `EVIDENCE_BACKED` (when backed by meteorological data) or `ILLUSTRATIVE_ASSUMPTION` (when manually specified by analysts).
4. **Data Provenance**: Every output explicitly displays its source: `OBSERVED`, `USER_ENTERED`, `MODEL_ESTIMATED`, `SCENARIO_ASSUMPTION`, or `UNAVAILABLE`.

---

## 5. Test Suite Verification Summary

- **Backend Pytest Suite**: 71/71 tests passing (`apps/api/tests/` and `tests/`).
- **Frontend Vitest Suite**: 157/157 tests passing (`apps/web/src/test/`).
- **Full E2E Engine Integration**: Validated end-to-end data flow from weather inputs $\to$ ML yield $\to$ IADS $\to$ scenario comparison $\to$ decision dossier.
