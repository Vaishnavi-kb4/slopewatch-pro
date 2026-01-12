
# mine_safety_system/utils/config.py

# System Configuration
UPDATE_INTERVAL = 3  # Seconds between agent cycles

# thresholds
TILT_THRESHOLD = 5.0  # degrees
STRAIN_THRESHOLD = 0.002 # strain unit
MOISTURE_CRITICAL = 80.0 # percentage
RAINFALL_HEAVY_THRESHOLD = 20.0 # mm/hr

# Risk Levels
RISK_LOW = "LOW"
RISK_MEDIUM = "MEDIUM"
RISK_HIGH = "HIGH"
RISK_CRITICAL = "CRITICAL"

# Probability Thresholds for Risk
PROB_MEDIUM = 0.3
PROB_HIGH = 0.6
PROB_CRITICAL = 0.85

# Simulation
SIMULATION_ZONES = ["Zone A", "Zone B", "Zone C"]
