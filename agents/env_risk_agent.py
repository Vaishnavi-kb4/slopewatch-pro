
# mine_safety_system/agents/env_risk_agent.py
import threading
import time
from mine_safety_system.utils.shared_state import state
from mine_safety_system.utils.config import *

class EnvRiskAgent(threading.Thread):
    def __init__(self):
        super().__init__()
        self.running = True

    def run(self):
        while self.running:
            current_state = state.get("sensor_data")
            env_risks = {}
            
            if current_state:
                for zone, data in current_state.items():
                    raw = data.get("raw", {})
                    rainfall = raw.get("rainfall", 0.0)
                    moisture = raw.get("moisture", 0.0)
                    
                    # Model: Pore Pressure Risk
                    # Risk increases if high moisture AND continuing rainfall
                    pore_pressure_risk = 0.0
                    if moisture > MOISTURE_CRITICAL:
                        pore_pressure_risk += 0.5
                    
                    if rainfall > RAINFALL_HEAVY_THRESHOLD:
                        pore_pressure_risk += 0.4
                        
                    env_risks[zone] = {
                        "pore_pressure_index": min(1.0, pore_pressure_risk),
                        "weather_condition": "HEAVY_RAIN" if rainfall > 20 else "NORMAL",
                        "storm_alert": rainfall > 50
                    }
            
            state.update("env_data", env_risks)
            time.sleep(UPDATE_INTERVAL)

    def stop(self):
        self.running = False
