# SlopeWatch Pro

## Predictive Intelligence for Safer Mines

---

## Overview

**SlopeWatch Pro** is an Agentic AI-based Predictive Safety System for Open-Pit Mines. It predicts rockfalls and slope failures before they happen, giving mine operators early warnings to evacuate workers and prevent casualties.

---

## Multi-Agent Architecture

The system uses **5 autonomous AI agents** working together:

| Agent | Input Data | Purpose |
|-------|------------|---------|
| **Sensor Agent** | Tilt, Strain, Seismic | Detects unusual ground movement signals |
| **Perception Agent** | Drone Imagery, Crack Width | Analyzes surface deformation from visuals |
| **Environmental Agent** | Rainfall, Moisture | Tracks weather and pore pressure |
| **Predictive Agent** | All agent outputs | Fuses data → Calculates Probability of Failure |
| **Alert Agent** | Predictions | Triggers alerts with evacuation recommendations |

---

## Input Data (Simulated)

| Data Type | Unit | Real-World Source |
|-----------|------|-------------------|
| Tilt | Degrees | Inclinometers |
| Strain | Micro-strain | Strain gauges |
| Moisture | % | Soil sensors |
| Seismic | Magnitude | Geophones |
| Rainfall | mm/hr | Weather stations |
| Crack Width | cm | Drone imagery |

---

## Zone Detection

The system monitors **3 zones**: Zone A, Zone B, Zone C.

Each zone is an independent monitoring unit representing different slopes of the mine.

**Data Flow:**
1. `DataSimulator` → Generates raw data per zone
2. `SensorAgent` → Smooths and detects anomalies
3. `PerceptionAgent` → Adds visual risk score
4. `EnvRiskAgent` → Calculates pore pressure risk
5. `PredictiveAgent` → Fuses all data → Outputs probability, trend, velocity, contributors

---

## Key Outputs

| Metric | Description |
|--------|-------------|
| Probability | 0-100% chance of failure |
| Risk Level | LOW, MEDIUM, HIGH, CRITICAL |
| Time-to-Failure | Estimated hours until failure |
| Trend | Increasing / Decreasing / Stable |
| Velocity | Rate of change (+X% / 10 min) |
| Contributors | Top factors causing risk |

---

## Formulas

**Probability of Failure:**
```
P = (Sensor × 0.4) + (Terrain × 0.3) + (Env × 0.3)
```

**Risk Velocity:**
```
V = (Current_P - Past_P) × 100
```

---

## Dashboard Features

- **Landing Page**: Hero section with CTA
- **Risk Heatmap**: Visual color-coded zone status
- **Zone Cards**: Real-time metrics per zone
- **What-If Simulation**: Project risk under heavy rainfall
- **Drill Mode**: Demo critical failure scenario
- **Pulse Animation**: Visual alert on critical zones

---

## Use Cases

| Use Case | Feature |
|----------|---------|
| Real-time Monitoring | Dashboard with live risk levels |
| Early Warning | Trend and Velocity metrics |
| Evacuation Decisions | CRITICAL alerts + banner |
| What-If Analysis | Rainfall simulation button |
| Training | Drill Mode toggle |

---

## How to Run

```bash
# Start the dashboard
streamlit run mine_safety_system/dashboard/app.py
```

---

## Technology Stack

- Python 3.x
- Streamlit (Dashboard)
- Altair (Charts)
- Threading (Agent concurrency)
- Shared State (Inter-agent communication)

---

## Project Structure

```
mine_safety_system/
├── agents/
│   ├── sensor_agent.py
│   ├── perception_agent.py
│   ├── env_risk_agent.py
│   ├── predictive_agent.py
│   └── alert_agent.py
├── data/
│   └── simulation.py
├── dashboard/
│   ├── app.py
│   ├── style.py
│   └── views/
│       ├── landing.py
│       ├── main_dashboard.py
│       ├── zone_detail.py
│       └── intelligence.py
├── utils/
│   ├── config.py
│   └── shared_state.py
└── main.py
```

---

## Author

Built with Agentic AI for Mine Safety Monitoring.
