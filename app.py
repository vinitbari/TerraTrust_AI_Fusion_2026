"""TerraTrust AI — Interactive Climate-Aware Agricultural Credit Decision-Support Platform.

Problem Statement: FIN-03 — Climate-Aware Credit Risk Assessment for Agriculture
Tagline: Turning Climate Uncertainty into Smarter Agricultural Credit Decisions.
"""

from datetime import date, timedelta
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from terratrust.contracts.schemas import (
    ClimateRequest,
    EvidenceStatus,
    FinancialAssessmentRequest,
    RiskBand,
    ScenarioRequest,
    YieldPredictionRequest,
)
from terratrust.engines.climate_engine import ClimateEngine
from terratrust.engines.explanation_engine import ExplanationEngine
from terratrust.engines.financial_engine import FinancialEngine
from terratrust.engines.scenario_engine import ScenarioEngine
from terratrust.engines.yield_engine import YieldEngine

# Page configuration
st.set_page_config(
    page_title="TerraTrust AI | Climate-Aware Credit Intelligence",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS styling for premium institutional look
st.markdown(
    """
    <style>
    .main {
        background-color: #0b1120;
        color: #f8fafc;
    }
    .metric-card {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 15px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
    }
    .metric-title {
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #94a3b8;
        margin-bottom: 6px;
    }
    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        color: #38bdf8;
    }
    .metric-subtitle {
        font-size: 0.8rem;
        color: #64748b;
        margin-top: 4px;
    }
    .badge-evidence {
        background-color: #065f46;
        color: #34d399;
        padding: 3px 8px;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    .badge-assumption {
        background-color: #78350f;
        color: #fbbf24;
        padding: 3px 8px;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    .badge-gated {
        background-color: #831843;
        color: #f472b6;
        padding: 3px 8px;
        border-radius: 6px;
        font-size: 0.75rem;
        font-weight: 600;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Initialize Core Engines
@st.cache_resource
def get_engines():
    climate = ClimateEngine()
    yield_ml = YieldEngine()
    financial = FinancialEngine()
    scenario = ScenarioEngine(financial_engine=financial)
    explanation = ExplanationEngine()
    return climate, yield_ml, financial, scenario, explanation

climate_eng, yield_eng, fin_eng, scen_eng, exp_eng = get_engines()

# Sidebar Navigation
st.sidebar.image("https://img.icons8.com/color/96/sprout.png", width=64)
st.sidebar.title("TerraTrust AI")
st.sidebar.caption("FIN-03 Climate-Aware Agricultural Credit Decision-Support")
st.sidebar.markdown("---")

navigation = st.sidebar.radio(
    "Navigation Workspace",
    [
        "1. Overview & Architecture",
        "2. Climate Intelligence (Engine A)",
        "3. Farm Assessment & Yield ML (Engine B & C)",
        "4. Climate Stress Scenario Lab (Engine D)",
        "5. Explanation & Credit Gating (Engine E)",
        "6. ML Model Evaluation & Benchmarks",
    ],
)

st.sidebar.markdown("---")
st.sidebar.subheader("Default Institutional Profile")
st.sidebar.info(
    "**Institution**: Apex Rural Development Bank\n\n"
    "**Branch**: Solapur South (BR-SOL-01)\n\n"
    "**Loan Officer**: Rajesh Sharma\n\n"
    "**Borrower**: Ramesh Patil (CUST-MH-2026-001)"
)


# ==============================================================================
# SECTION 1: OVERVIEW & ARCHITECTURE
# ==============================================================================
if navigation == "1. Overview & Architecture":
    st.title("🌱 TerraTrust AI: Turning Climate Uncertainty into Smarter Credit Decisions")
    st.markdown(
        "**FIN-03: Climate-Aware Agricultural Credit Risk Decision-Support System**\n\n"
        "TerraTrust AI connects high-resolution meteorological telemetry, agronomic soil nutrients, "
        "and physical crop yield machine learning with deterministic farm cash-flow modeling. It empowers "
        "rural lenders to evaluate debt-service capacity under adverse climate stress before approving agricultural loans."
    )

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(
            '<div class="metric-card">'
            '<div class="metric-title">Core Inference Engine</div>'
            '<div class="metric-value">ExtraTrees</div>'
            '<div class="metric-subtitle">R² = 0.9917 | MAE = 0.114 t/ha</div>'
            '</div>',
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            '<div class="metric-card">'
            '<div class="metric-title">Weather Integration</div>'
            '<div class="metric-value">Open-Meteo</div>'
            '<div class="metric-subtitle">High-Res Reanalysis + IMD Fallback</div>'
            '</div>',
            unsafe_allow_html=True,
        )
    with col3:
        st.markdown(
            '<div class="metric-card">'
            '<div class="metric-title">Cash-Flow Standard</div>'
            '<div class="metric-value">IADS & DSCR</div>'
            '<div class="metric-subtitle">Deterministic transparent arithmetic</div>'
            '</div>',
            unsafe_allow_html=True,
        )
    with col4:
        st.markdown(
            '<div class="metric-card">'
            '<div class="metric-title">Regulatory Gating</div>'
            '<div class="metric-value">PD Gated</div>'
            '<div class="metric-subtitle">No fabricated default percentages</div>'
            '</div>',
            unsafe_allow_html=True,
        )

    st.subheader("System Workflow Pipeline")
    st.markdown(
        """
        ```text
        1. Agricultural & Climate Telemetry (Open-Meteo / IMD / Soil Health Cards)
           │
           ├──► 2. Engine A: Climate Intelligence (GDD, Heat Days, Dry Spells, Anomalies)
           │
           ├──► 3. Engine B: Physical Crop-Yield ML (ExtraTreesRegressor Inference)
           │
           ├──► 4. Engine C: Farm Financial Engine (Gross Revenue, Production Costs, IADS, DSCR)
           │
           ├──► 5. Engine D: Climate Scenario Lab (Drought, Heat Stress, Market Price Shocks)
           │
           └──► 6. Engine E: Explanation, Quality & Regulatory Gating (Lineage & Human Sign-off)
        ```
        """
    )

    st.subheader("Core Differentiators & Regulatory Guardrails")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(
            "**🛡️ 1. Crop Yield $\neq$ Loan Default**\n\n"
            "Physical agronomic yield is scientifically distinct from credit default. "
            "Because this repository does not include an audited historical loan loss dataset, "
            "probability of default is strictly **gated** as `PD_UNAVAILABLE`. Fabricated risk scores are strictly prohibited."
        )
        st.markdown(
            "**📊 2. Deterministic Financials**\n\n"
            "Farm Revenue, Net Income, Income Available for Debt Service (IADS), and Debt Service Coverage Ratios (DSCR) "
            "are calculated using transparent mathematical formulas approved by credit risk committees."
        )
    with c2:
        st.markdown(
            "**🌦️ 3. Evidence-Backed Stress Scenarios**\n\n"
            "Every scenario explicitly declares its evidence provenance as either `EVIDENCE_BACKED` "
            "(grounded in empirical weather/price data) or `ILLUSTRATIVE_ASSUMPTION` (analyst stress testing)."
        )
        st.markdown(
            "**🔍 4. Complete Audit Traceability**\n\n"
            "Every assessment tracks input provenance across `OBSERVED`, `USER_ENTERED`, `MODEL_ESTIMATED`, and `SCENARIO_ASSUMPTION`."
        )


# ==============================================================================
# SECTION 2: CLIMATE INTELLIGENCE (ENGINE A)
# ==============================================================================
elif navigation == "2. Climate Intelligence (Engine A)":
    st.title("🌦️ Engine A: Climate Intelligence Engine")
    st.markdown(
        "Ingests historical and forecast weather telemetry from Open-Meteo API (or IMD gridded telemetry), "
        "computes agronomic growing season indicators, and evaluates climate anomalies against historical 10-year baselines."
    )

    col_in1, col_in2, col_in3, col_in4 = st.columns(4)
    with col_in1:
        lat = st.number_input("Latitude", value=17.6599, format="%.4f", help="Solapur district default")
    with col_in2:
        lon = st.number_input("Longitude", value=75.9064, format="%.4f")
    with col_in3:
        sowing = st.date_input("Season Start (Sowing)", value=date(2026, 6, 1))
    with col_in4:
        harvest = st.date_input("Season End (Harvest)", value=date(2026, 10, 31))

    if st.button("Run Climate Analysis", type="primary"):
        with st.spinner("Fetching meteorological telemetry and calculating indicators..."):
            req = ClimateRequest(latitude=lat, longitude=lon, start_date=sowing, end_date=harvest)
            report = climate_eng.analyze_season(req)
            st.session_state["climate_report"] = report

    if "climate_report" in st.session_state:
        rep = st.session_state["climate_report"]

        st.success(f"Telemetry Loaded successfully from: **{rep.source}**")
        if rep.warnings:
            for w in rep.warnings:
                st.warning(w)

        m1, m2, m3, m4, m5 = st.columns(5)
        m1.metric("Total Rainfall", f"{rep.indicators.total_rainfall_mm:.1f} mm", delta=f"{rep.anomalies.rainfall_anomaly_pct:+.1f}% vs baseline")
        m2.metric("Mean Temperature", f"{rep.indicators.mean_temperature_c:.1f} °C", delta=f"{rep.anomalies.temperature_anomaly_c:+.1f} °C")
        m3.metric("Growing Degree Days", f"{rep.indicators.growing_degree_days:.0f} GDD")
        m4.metric("Heat Stress Days (>35°C)", f"{rep.indicators.heat_stress_days_above_35c} days")
        m5.metric("Max Dry Spell", f"{rep.indicators.consecutive_dry_days_max} days")

        # Visualizations
        df_weather = pd.DataFrame([
            {
                "Date": r.date,
                "Precipitation (mm)": r.precipitation_mm,
                "Mean Temp (°C)": r.temperature_mean_c,
                "Max Temp (°C)": r.temperature_max_c,
                "Min Temp (°C)": r.temperature_min_c,
            }
            for r in rep.daily_records
        ])

        col_g1, col_g2 = st.columns(2)
        with col_g1:
            fig_rain = px.bar(
                df_weather,
                x="Date",
                y="Precipitation (mm)",
                title="Daily Precipitation Series (mm)",
                color_discrete_sequence=["#38bdf8"],
            )
            fig_rain.update_layout(template="plotly_dark", height=320)
            st.plotly_chart(fig_rain, use_container_width=True)

        with col_g2:
            fig_temp = px.line(
                df_weather,
                x="Date",
                y=["Max Temp (°C)", "Mean Temp (°C)", "Min Temp (°C)"],
                title="Growing Season Thermal Envelope (°C)",
                color_discrete_map={
                    "Max Temp (°C)": "#ef4444",
                    "Mean Temp (°C)": "#f59e0b",
                    "Min Temp (°C)": "#10b981",
                },
            )
            fig_temp.add_hline(y=35.0, line_dash="dot", line_color="red", annotation_text="Terminal Heat Threshold (35°C)")
            fig_temp.update_layout(template="plotly_dark", height=320)
            st.plotly_chart(fig_temp, use_container_width=True)


# ==============================================================================
# SECTION 3: FARM ASSESSMENT & YIELD ML (ENGINE B & C)
# ==============================================================================
elif navigation == "3. Farm Assessment & Yield ML (Engine B & C)":
    st.title("🌾 Engines B & C: Crop Yield ML & Farm Financials")
    st.markdown(
        "Combines agronomic soil nutrient features (`Fertilizer`, `temp`, `N`, `P`, `K`) to estimate physical crop yield (tonnes/ha), "
        "then evaluates farm cash flow, debt service capacity (IADS), and Debt Service Coverage Ratio (DSCR)."
    )

    col_ag1, col_ag2 = st.columns(2)
    with col_ag1:
        st.subheader("1. Agronomic & Edaphic Inputs")
        crop_type = st.selectbox("Cultivated Crop", ["WHEAT", "RICE", "COTTON", "SOYBEAN", "SUGARCANE"])
        farm_area = st.number_input("Cultivated Area (Hectares)", min_value=0.5, max_value=100.0, value=2.5, step=0.5)
        temperature = st.slider("Mean Growing Season Temperature (°C)", 15.0, 45.0, 26.5, step=0.5)
        fertilizer_rate = st.slider("Fertilizer Application Rate (kg/ha)", 0.0, 300.0, 120.0, step=10.0)
        
        c_n, c_p, c_k = st.columns(3)
        with c_n:
            soil_n = st.number_input("Soil Nitrogen (N ppm)", min_value=0.0, max_value=250.0, value=45.0)
        with c_p:
            soil_p = st.number_input("Soil Phosphorus (P ppm)", min_value=0.0, max_value=150.0, value=35.0)
        with c_k:
            soil_k = st.number_input("Soil Potassium (K ppm)", min_value=0.0, max_value=250.0, value=40.0)

    with col_ag2:
        st.subheader("2. Commodity Market & Farm Financial Parameters")
        currency = st.selectbox("Currency", ["INR", "USD"])
        default_price = 25000.0 if currency == "INR" else 300.0
        price_per_tonne = st.number_input(f"Expected Price per Tonne ({currency})", min_value=100.0, value=default_price, step=500.0)
        post_harvest_loss = st.slider("Post-Harvest Handling Loss (%)", 0.0, 30.0, 5.0, step=1.0) / 100.0
        
        default_costs = 65000.0 if currency == "INR" else 800.0
        production_costs = st.number_input(f"Cultivation & Input Costs ({currency})", min_value=0.0, value=default_costs, step=5000.0)
        other_expenses = st.number_input(f"Other Farm Overhead ({currency})", min_value=0.0, value=10000.0 if currency == "INR" else 150.0)
        household_income = st.number_input(f"Off-Farm Income ({currency})", min_value=0.0, value=15000.0 if currency == "INR" else 200.0)
        debt_service = st.number_input(f"Scheduled Loan Debt Service ({currency})", min_value=0.0, value=55000.0 if currency == "INR" else 600.0)

    if st.button("Calculate Farm Assessment & Credit Capacity", type="primary"):
        with st.spinner("Running ExtraTrees ML Regressor and Financial Cash-Flow Calculator..."):
            # 1. Yield Inference
            yield_req = YieldPredictionRequest(
                Fertilizer=fertilizer_rate,
                temp=temperature,
                N=soil_n,
                P=soil_p,
                K=soil_k,
                crop_name=crop_type,
            )
            yield_res = yield_eng.predict(yield_req)

            # 2. Financial Assessment
            fin_req = FinancialAssessmentRequest(
                yield_tonnes_per_ha=yield_res.predicted_yield,
                farm_area_ha=farm_area,
                expected_price_per_tonne=price_per_tonne,
                post_harvest_loss_pct=post_harvest_loss,
                production_costs=production_costs,
                other_farm_expenses=other_expenses,
                other_household_income=household_income,
                scheduled_debt_service=debt_service,
                currency=currency,
            )
            fin_res = fin_eng.assess_farm_finances(fin_req)

            st.session_state["assessment_results"] = {
                "yield_req": yield_req,
                "yield_res": yield_res,
                "fin_req": fin_req,
                "fin_res": fin_res,
            }

    if "assessment_results" in st.session_state:
        res = st.session_state["assessment_results"]
        y_res = res["yield_res"]
        f_res = res["fin_res"]
        f_req = res["fin_req"]

        st.markdown("---")
        st.subheader("Assessment Results & Financial Capacity")

        r1, r2, r3, r4 = st.columns(4)
        r1.metric("Predicted Crop Yield", f"{y_res.predicted_yield:.2f} t/ha", delta=f"{y_res.lift_over_baseline_pct:+.1f}% vs regional median")
        r2.metric("Gross Farm Revenue", f"{f_req.currency} {f_res.financials.gross_revenue:,.2f}")
        r3.metric("Income Available for Debt Service (IADS)", f"{f_req.currency} {f_res.financials.income_available_for_debt_service:,.2f}")
        
        dscr_val = f"{f_res.financials.debt_service_coverage_ratio:.2f}x" if f_res.financials.debt_service_coverage_ratio else "N/A"
        r4.metric("Debt Service Coverage (DSCR)", dscr_val, help="IADS divided by scheduled loan obligations")

        st.info(f"**Coverage Status**: {f_res.coverage_status} | **Risk Band**: `{f_res.risk_band.value}`")

        # Step by step breakdown
        with st.expander("🔍 Step-by-Step Mathematical Calculation Breakdown", expanded=True):
            for step_key, step_text in f_res.calculation_steps.items():
                st.markdown(f"- **{step_key.replace('_', ' ').title()}**: `{step_text}`")


# ==============================================================================
# SECTION 4: CLIMATE STRESS SCENARIO LAB (ENGINE D)
# ==============================================================================
elif navigation == "4. Climate Stress Scenario Lab (Engine D)":
    st.title("⚡ Engine D: Climate Stress-Testing Scenario Lab")
    st.markdown(
        "Evaluates the sensitivity of farm cash flow and Debt Service Coverage Ratios (DSCR) under adverse climate shocks "
        "(drought, terminal heat stress, flood) and commodity market price volatility."
    )

    if "assessment_results" not in st.session_state:
        st.warning("Please execute a baseline assessment in Tab 3 first, or use the default institutional baseline below.")
        default_fin_req = FinancialAssessmentRequest(
            yield_tonnes_per_ha=3.84,
            farm_area_ha=2.5,
            expected_price_per_tonne=25000.0,
            post_harvest_loss_pct=0.05,
            production_costs=65000.0,
            other_farm_expenses=10000.0,
            other_household_income=15000.0,
            scheduled_debt_service=55000.0,
            currency="INR",
        )
    else:
        default_fin_req = st.session_state["assessment_results"]["fin_req"]

    c_sc1, c_sc2 = st.columns([1, 2])
    with c_sc1:
        st.subheader("Select Stress Scenario")
        scenario_choice = st.selectbox(
            "Predefined Scenario",
            [
                "DROUGHT_SEVERE",
                "DROUGHT_MODERATE",
                "HEAT_STRESS",
                "FLOOD_EXCESS",
                "PRICE_SHOCK_20",
                "COST_INFLATION_25",
                "COMPOUND_SHOCK",
                "CUSTOM_USER_STRESS",
            ],
        )

        custom_y = None
        custom_p = None
        custom_c = None
        if scenario_choice == "CUSTOM_USER_STRESS":
            custom_y = st.slider("Custom Yield Shock (%)", -60.0, 20.0, -25.0, step=5.0) / 100.0
            custom_p = st.slider("Custom Price Shock (%)", -40.0, 20.0, -10.0, step=5.0) / 100.0
            custom_c = st.slider("Custom Cost Inflation (%)", 0.0, 50.0, 15.0, step=5.0) / 100.0

        if st.button("Simulate Stress Scenario", type="primary"):
            scen_req = ScenarioRequest(
                scenario_code=scenario_choice,
                custom_yield_delta_pct=custom_y,
                custom_price_delta_pct=custom_p,
                custom_cost_delta_pct=custom_c,
            )
            scen_res = scen_eng.run_stress_scenario(default_fin_req, scen_req)
            st.session_state["scenario_result"] = scen_res

    with c_sc2:
        if "scenario_result" in st.session_state:
            s_res = st.session_state["scenario_result"]

            st.subheader(f"Stress Analysis: {s_res.scenario_code}")
            badge_class = "badge-evidence" if s_res.evidence_status == EvidenceStatus.EVIDENCE_BACKED else "badge-assumption"
            st.markdown(
                f'<span class="{badge_class}">{s_res.evidence_status.value}</span> '
                f'— *{s_res.description}*',
                unsafe_allow_html=True,
            )

            c_met1, c_met2, c_met3, c_met4 = st.columns(4)
            c_met1.metric("Stressed Yield", f"{s_res.stressed.yield_tonnes_per_ha:.2f} t/ha", delta=f"{s_res.deltas.yield_delta_pct:+.1f}%")
            c_met2.metric("Stressed Revenue", f"INR {s_res.stressed.gross_revenue:,.0f}", delta=f"{s_res.deltas.revenue_delta_pct:+.1f}%")
            c_met3.metric("Stressed Net Income", f"INR {s_res.stressed.net_farm_income:,.0f}", delta=f"{s_res.deltas.net_income_delta_pct:+.1f}%")
            
            dscr_delta_str = f"{s_res.deltas.dscr_delta:+.2f}x" if s_res.deltas.dscr_delta else "N/A"
            dscr_stressed_str = f"{s_res.stressed.dscr:.2f}x" if s_res.stressed.dscr else "N/A"
            c_met4.metric("Stressed DSCR", dscr_stressed_str, delta=dscr_delta_str)

            # Bar chart comparison
            df_comp = pd.DataFrame([
                {"Metric": "Gross Revenue", "Baseline": s_res.baseline.gross_revenue, "Stressed": s_res.stressed.gross_revenue},
                {"Metric": "Net Farm Income", "Baseline": s_res.baseline.net_farm_income, "Stressed": s_res.stressed.net_farm_income},
                {"Metric": "IADS (Debt Capacity)", "Baseline": s_res.baseline.iads, "Stressed": s_res.stressed.iads},
            ])
            fig_comp = go.Figure(data=[
                go.Bar(name="Baseline", x=df_comp["Metric"], y=df_comp["Baseline"], marker_color="#10b981"),
                go.Bar(name="Stressed", x=df_comp["Metric"], y=df_comp["Stressed"], marker_color="#ef4444"),
            ])
            fig_comp.update_layout(barmode="group", template="plotly_dark", height=320, title="Baseline vs Stressed Financial Comparison (INR)")
            st.plotly_chart(fig_comp, use_container_width=True)


# ==============================================================================
# SECTION 5: EXPLANATION & CREDIT GATING (ENGINE E)
# ==============================================================================
elif navigation == "5. Explanation & Credit Gating (Engine E)":
    st.title("🛡️ Engine E: Explanation, Quality & Credit Gating")
    st.markdown(
        "Maintains complete data provenance lineage, audits data quality, and enforces strict regulatory credit risk gating."
    )

    # Compile sample audit
    sample_y_req = YieldPredictionRequest(Fertilizer=120.0, temp=26.5, N=45.0, P=35.0, K=40.0)
    sample_f_req = FinancialAssessmentRequest(
        yield_tonnes_per_ha=3.84,
        farm_area_ha=2.5,
        expected_price_per_tonne=25000.0,
        production_costs=65000.0,
        scheduled_debt_service=55000.0,
    )
    sample_f_res = fin_eng.assess_farm_finances(sample_f_req)
    audit_report = exp_eng.audit_assessment(
        yield_request=sample_y_req,
        yield_prediction=3.84,
        fin_request=sample_f_req,
        fin_response=sample_f_res,
        scenario_assumptions={"scenario_code": "DROUGHT_SEVERE"},
    )

    st.subheader("1. Data Provenance & Evidence Classification")
    df_prov = pd.DataFrame([
        {
            "Feature / Input": p.feature_name,
            "Value": p.value,
            "Evidence Classification": p.evidence_status.value,
            "Data Source Description": p.source_description,
        }
        for p in audit_report.provenance
    ])
    st.dataframe(df_prov, use_container_width=True)

    st.markdown("---")
    st.subheader("2. Regulatory Credit Risk Gating Notice")
    st.markdown(
        f'<div style="background-color: #450a0a; border: 1px solid #b91c1c; border-radius: 8px; padding: 16px;">'
        f'<h4 style="color: #f87171; margin-top: 0;">⚠️ Probability of Default: {audit_report.probability_of_default_status}</h4>'
        f'<p style="color: #fca5a5; font-size: 0.9rem;">{audit_report.gating_rationale}</p>'
        f'<p style="color: #f87171; font-weight: 600; margin-bottom: 0;">Mandatory Policy: Human Credit Committee Sign-Off Required</p>'
        f'</div>',
        unsafe_allow_html=True,
    )

    st.markdown("---")
    st.subheader("3. Model Limitations & Disclaimers")
    for lim in audit_report.limitations:
        st.markdown(f"- ℹ️ {lim}")


# ==============================================================================
# SECTION 6: ML MODEL EVALUATION & BENCHMARKS
# ==============================================================================
elif navigation == "6. ML Model Evaluation & Benchmarks":
    st.title("📈 ML Model Evaluation & Benchmark Registry")
    st.markdown(
        "Examines the held-out validation metrics of the `ExtraTreesRegressor` model artifact (`terratust_crop_yield_model.pkl`) "
        "and reviews the multi-modal satellite/ERA5 **Zenodo CY-Bench** benchmark integration."
    )

    metrics = yield_eng.get_evaluation_metrics()

    c_m1, c_m2, c_m3, c_m4 = st.columns(4)
    c_m1.metric("Coefficient of Determination (R²)", f"{metrics['r2_score']:.4f}", help="Observed on held-out experimental test partition")
    c_m2.metric("Mean Absolute Error (MAE)", f"{metrics['mae']:.4f} t/ha", delta="-91.9% vs baseline median")
    c_m3.metric("Root Mean Squared Error (RMSE)", f"{metrics['rmse']:.4f} t/ha")
    c_m4.metric("Baseline Median MAE", f"{metrics['baseline_mae']:.3f} t/ha")

    st.subheader("Baseline vs ML Candidate Lift Comparison")
    df_eval = pd.DataFrame([
        {"Model Architecture": "Regional Median Baseline (TT-BASE-01)", "MAE (tonnes/ha)": metrics["baseline_mae"], "R² Score": 0.00},
        {"Model Architecture": "ExtraTreesRegressor (TT-CYM-01)", "MAE (tonnes/ha)": metrics["mae"], "R² Score": metrics["r2_score"]},
    ])
    st.dataframe(df_eval, use_container_width=True)

    st.subheader("CY-Bench Benchmark Status (docs/cy_bench_audit_report.json)")
    st.markdown(
        """
        - **Source**: Zenodo Record 13838912 (Multi-Modal Crop Yield Benchmark)
        - **Inputs**: Sentinel-2 MSI Vegetation Indices (NDVI/EVI), NASA SMAP Root-Zone Soil Moisture, ERA5 Reanalysis Weather.
        - **Validation Strategy**: Strict temporal split (Train $\le 2020$, Test $\ge 2021$) to eliminate forward lookahead leakage.
        - **Model Isolation**: Kaggle edaphic soil nutrient models and CY-Bench satellite imagery models are maintained as **distinct routing tiers** to prevent schema pollution.
        """
    )
