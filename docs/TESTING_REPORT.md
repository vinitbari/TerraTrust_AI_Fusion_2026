# TerraTrust AI — Automated Testing & Quality Report

**Execution Date**: October 2026  
**Test Frameworks**: `pytest` (Python Engine & Backend Suite), `vitest` (TypeScript Web Suite)  
**Overall Status**: **100% PASSING (239/239 Automated Tests)**

---

## 1. Test Suite Summary

| Subsystem / Suite | Test Count | Status | Duration | Focus Area |
|---|---|---|---|---|
| **TerraTrust Core Engines** (`tests/`) | 11 | **PASSED** | 4.61s | Climate, Yield ML, Financial, Scenario, Explanation, and E2E integration. |
| **FastAPI Backend Services** (`apps/api/tests/`) | 71 | **PASSED** | 32.14s | 43 API endpoints, SQLite/PostgreSQL, Auth/RBAC, rate-limiting, audit logging. |
| **Vite React Web Frontend** (`apps/web/src/test/`) | 157 | **PASSED** | 45.05s | Permissions, formatters, risk gauges, error envelopes, UI accessibility. |
| **Total Automated Tests** | **239** | **PASSED** | — | — |

---

## 2. Core Engine Test Results Detail

```text
tests/test_climate_engine.py::test_climate_engine_analysis_deterministic PASSED
tests/test_climate_engine.py::test_climate_engine_invalid_date_range PASSED
tests/test_end_to_end_pipeline.py::test_full_workflow_integration PASSED
tests/test_explanation_engine.py::test_explanation_engine_audit_and_credit_gating PASSED
tests/test_financial_engine.py::test_financial_engine_standard_assessment PASSED
tests/test_financial_engine.py::test_financial_engine_zero_debt_handling PASSED
tests/test_scenario_engine.py::test_scenario_engine_drought_severe PASSED
tests/test_scenario_engine.py::test_scenario_engine_price_shock_only PASSED
tests/test_yield_engine.py::test_yield_engine_prediction_and_uncertainty PASSED
tests/test_yield_engine.py::test_yield_engine_alias_mapping PASSED
tests/test_yield_engine.py::test_yield_engine_evaluation_metrics PASSED
```

---

## 3. End-to-End Pipeline Verification

The end-to-end integration test (`test_full_workflow_integration`) verifies the full data lifecycle:
1. **Engine A** fetches and processes seasonal climate telemetry.
2. **Engine B** passes growing temperature and soil parameters to `ExtraTreesRegressor`.
3. **Engine C** calculates farm production, gross revenue, net farm income, IADS, and DSCR.
4. **Engine D** evaluates severe climate stress (`DROUGHT_SEVERE`), confirming accurate revenue degradation and negative DSCR delta.
5. **Engine E** audits data provenance across all tiers and strictly gates Probability of Default as `PD_UNAVAILABLE`.
