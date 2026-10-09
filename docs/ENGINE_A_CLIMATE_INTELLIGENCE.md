# TerraTrust AI — Engine A: Climate Intelligence Engine Specification

## 1. Overview & Purpose
The **Climate Intelligence Engine (Engine A)** connects high-resolution meteorological telemetry (live Open-Meteo archive API and IMD gridded reference data) with agricultural crop-cycle schedules to calculate agronomic indicators and evaluate climate anomalies against historical 10-year baselines.

---

## 2. Calculated Agronomic Indicators

| Indicator | Agronomic Formula | Unit | Purpose |
|---|---|---|---|
| **Total Precipitation** | $\sum \text{Daily Rain}$ | mm | Season cumulative moisture availability |
| **Mean Temperature** | $\frac{1}{N} \sum T_{\text{mean}}$ | °C | Thermal growing envelope |
| **Growing Degree Days (GDD)** | $\sum \max(0, T_{\text{mean}} - T_{\text{base}})$ ($T_{\text{base}}=10^\circ\text{C}$) | GDD | Phenological crop development pacing |
| **Heat Stress Days** | $\sum \mathbb{I}(T_{\text{max}} \ge 35^\circ\text{C})$ | days | Flowering and grain-filling abortion risk |
| **Max Consecutive Dry Days** | $\max(\text{Dry Spell Length})$ ($\text{Rain} < 1\text{mm}$) | days | Extended agricultural drought indicator |

---

## 3. Climate Anomalies & Historical Baselines

Anomalies are computed against 10-year historical reference means:
- **Rainfall Anomaly (%)**:
  $$\Delta_{\text{Rain}}\% = \frac{\text{Observed Rainfall} - \text{Baseline Rainfall}}{\text{Baseline Rainfall}} \times 100$$
- **Temperature Anomaly (°C)**:
  $$\Delta_T = \text{Observed Mean Temp} - \text{Baseline Mean Temp}$$

### Classification Thresholds:
- $\Delta_{\text{Rain}} \le -25\% \implies \text{SEVERE\_DEFICIT}$
- $-25\% < \Delta_{\text{Rain}} \le -10\% \implies \text{MODERATE\_DEFICIT}$
- $-10\% < \Delta_{\text{Rain}} < +25\% \implies \text{NORMAL\_RANGE}$
- $\Delta_{\text{Rain}} \ge +25\% \implies \text{EXCESS\_RAINFALL}$

---

## 4. Telemetry Source & Failover Strategy
1. **Primary**: Open-Meteo High-Resolution Historical Reanalysis & Archive API.
2. **Offline Fallback**: IMD Regional Gridded Telemetry fixture with deterministic agricultural parameters.
3. **Data Completeness**: Flagged and recorded on every assessment response.
