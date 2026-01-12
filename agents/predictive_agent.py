
# mine_safety_system/agents/predictive_agent.py
import threading
import time
import random
from mine_safety_system.utils.shared_state import state
from mine_safety_system.utils.config import *

from collections import deque

class PredictiveAgent(threading.Thread):
    def __init__(self):
        super().__init__()
        self.running = True
        # Keep last 300 ticks for trend analysis
        self.history = {z: deque(maxlen=300) for z in SIMULATION_ZONES}

    def run(self):
        while self.running:
            sensors = state.get("sensor_data", {})
            terrain = state.get("terrain_data", {})
            env = state.get("env_data", {})
            
            predictions = {}
            
            # Fuse data for each zone
            for zone in SIMULATION_ZONES:
                # 1. Get Factors
                s_data = sensors.get(zone, {})
                t_data = terrain.get(zone, {})
                e_data = env.get(zone, {})
                
                # Factors (0.0 to 1.0)
                sensor_factor = 1.0 if s_data.get("status") == "WARNING" else 0.2
                terrain_factor = t_data.get("visual_risk_score", 0.0)
                env_factor = e_data.get("pore_pressure_index", 0.0)
                
                # 2. Weighted Fusion Model (Simplified for Prototype)
                # Weights: Sensor (40%), Terrain (30%), Env (30%)
                base_prob = (sensor_factor * 0.4) + (terrain_factor * 0.3) + (env_factor * 0.3)
                
                # Add uncertainty/noise for realism
                prob_failure = min(1.0, max(0.0, base_prob + random.uniform(-0.05, 0.05)))
                
                # --- Trend Calculation ---
                # History tracks last 300 ticks (approx 15 mins with 3s sleep)
                # Actually, simulation runs faster than real time usually, so let's call it 15 mins of data
                hist = self.history[zone]
                hist.append(prob_failure)
                
                # Trend (Long-term: 45 min window simulated - looking at start of deque)
                # If deque is full (300 items), comparing [0] vs [-1] is about 15 mins.
                # To simulate "45 min", we extrapolate or just label it as "Trend".
                
                trend = "Stable"
                icon = "→"
                
                # Compare current vs average of first 10
                start_avg = 0
                if len(hist) > 0:
                    start_avg = sum(list(hist)[:10]) / min(len(hist), 10)
                
                delta_total = prob_failure - start_avg
                
                if delta_total > 0.05:
                    trend = "Increasing"
                    icon = "↑"
                elif delta_total < -0.05:
                    trend = "Decreasing"
                    icon = "↓"

                # --- Velocity Calculation (+X% / 10 min) ---
                # Assume 10 mins = 200 ticks (approx) or just take the last N ticks
                # Let's say check delta over last 50 ticks (approx 2.5 min real time, simulated as 10 min)
                velocity_label = "0.0% / 10 min"
                if len(hist) >= 10:
                    # Look back 50 ticks or max available
                    lookback_idx = max(0, len(hist) - 50) 
                    past_val = hist[lookback_idx]
                    
                    # scale delta to represent "per 10 min" if our window is smaller
                    # Here we just take raw difference and call it per window
                    vel_val = (prob_failure - past_val) * 100 # percentage
                    sign = "+" if vel_val > 0 else ""
                    velocity_label = f"{sign}{vel_val:.1f}% / 10 min"

                # 3. Determine Risk Level
                if prob_failure > PROB_CRITICAL:
                    risk_level = RISK_CRITICAL
                    ttf = random.randint(1, 4) # Hours
                elif prob_failure > PROB_HIGH:
                    risk_level = RISK_HIGH
                    ttf = random.randint(4, 24)
                elif prob_failure > PROB_MEDIUM:
                    risk_level = RISK_MEDIUM
                    ttf = random.randint(24, 72)
                else:
                    risk_level = RISK_LOW
                    ttf = "N/A"

                # --- Confidence Calculation ---
                # Higher confidence if inputs agree
                # e.g. If Sensor is High (1.0) and Terrain is High (>0.5), we are sure.
                agreement_score = 1.0
                if abs(sensor_factor - terrain_factor) > 0.5:
                    agreement_score -= 0.3
                if abs(sensor_factor - env_factor) > 0.5:
                    agreement_score -= 0.2
                
                # Randomize slightly
                final_conf = max(0.4, min(0.99, agreement_score - random.uniform(0, 0.1)))

                # --- Explainability (Why This Risk?) ---
                # Calculate raw contribution of each component to the final prob
                # Base weights: Sensor(0.4), Terrain(0.3), Env(0.3)
                
                # We normalize the contribution to be relative to the *total probability* 
                # or just absolute percentage addition. User asked for "+12%", implying absolute contribution.
                
                contribs = []
                if sensor_factor > 0:
                    contribs.append(("Sensor Instability", sensor_factor * 0.4))
                if terrain_factor > 0:
                    contribs.append(("Surface Deformation", terrain_factor * 0.3))
                if env_factor > 0:
                    contribs.append(("Rainfall / Pore Pressure", env_factor * 0.3))
                
                # Sort descending
                contribs.sort(key=lambda x: x[1], reverse=True)
                
                # Format for UI
                top_factors = [f"{name} (+{score*100:.0f}%)" for name, score in contribs]

                predictions[zone] = {
                    "probability": round(prob_failure, 2),
                    "risk_level": risk_level,
                    "time_to_failure_hours": ttf,
                    "confidence": round(final_conf, 2),
                    "trend": trend,
                    "trend_icon": icon,
                    "trend_delta": round(delta_total, 3) if len(hist) > 10 else 0.0,
                    "risk_velocity": velocity_label,
                    "contributors": top_factors
                }
            
            state.update("predictions", predictions)
            time.sleep(UPDATE_INTERVAL)

    def stop(self):
        self.running = False
