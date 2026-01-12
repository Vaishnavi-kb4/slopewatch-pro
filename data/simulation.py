
# mine_safety_system/data/simulation.py
import time
import random
import math
from mine_safety_system.utils.config import *
from mine_safety_system.utils.shared_state import state

class DataSimulator:
    def __init__(self):
        self.zones = SIMULATION_ZONES
        self.tick = 0
        self.start_time = time.time()
        
        # Initial baselines for each zone
        self.state = {
            z: {
                "tilt": 1.0,        # degrees
                "strain": 0.0005,   # strain
                "moisture": 30.0,   # %
                "seismic": 0.1,     # magnitude
                "rainfall": 0.0,    # mm/hr
                "crack_width": 2.0  # cm (Perception proxy)
            } for z in self.zones
        }
        
    def generate_next_tick(self):
        """
        Advances simulation by one tick and returns the new data snapshot.
        Simulates:
        - Weather changes (Rain)
        - Ground reaction (Moisture -> Strain -> Tilt)
        - Random noise
        """
        self.tick += 1
        snapshot = {}
        
        timestamp = time.time()
        
        for z in self.zones:
            curr = self.state[z]
            
            # --- DRILL MODE INTERCEPTION ---
            if state.get("drill_mode", False) and z == "Zone B":
                curr["rainfall"] = 120.0
                curr["moisture"] = 95.0
                curr["tilt"] = 45.0 + random.uniform(0, 5)
                curr["strain"] = 0.05
                curr["seismic"] = 3.5
            
            # 1. Weather Logic: Random walk for rainfall
            # 5% chance of sudden storm start/stop, else gradual drift
            if random.random() < 0.05:
                curr["rainfall"] = random.uniform(0, 80) if random.random() > 0.7 else 0.0
            else:
                curr["rainfall"] += random.uniform(-2, 2)
            curr["rainfall"] = max(0.0, min(150.0, curr["rainfall"]))
            
            # 2. Moisture Logic: Increases with rain, dries over time
            drying_rate = 0.5
            wetting_rate = curr["rainfall"] * 0.2
            curr["moisture"] += wetting_rate - drying_rate
            curr["moisture"] = max(5.0, min(100.0, curr["moisture"]))
            
            # 3. Ground Instability Logic
            # If moisture > Critical, ground starts moving faster
            instability = 0.0
            if curr["moisture"] > MOISTURE_CRITICAL:
                instability = 0.05 # Acceleration factor
            
            # Add random noise + instability drift
            curr["tilt"] += random.gauss(0, 0.05) + instability
            curr["strain"] += abs(random.gauss(0, 0.00001)) + (instability * 0.0005)
            curr["crack_width"] += abs(random.gauss(0, 0.01)) + (instability * 0.1)
            
            # 4. Seismic: Usually quiet, rare spikes
            base_seismic = 0.2
            if random.random() < 0.02: # 2% chance of tremor
                curr["seismic"] = random.uniform(2.0, 4.5)
            else:
                curr["seismic"] = max(0.0, base_seismic + random.gauss(0, 0.05))
            
            # Save snapshot
            snapshot[z] = {
                "timestamp": timestamp,
                "tilt": round(curr["tilt"], 3),
                "strain": round(curr["strain"], 6),
                "moisture": round(curr["moisture"], 1),
                "rainfall": round(curr["rainfall"], 1),
                "seismic": round(curr["seismic"], 2),
                "crack_width": round(curr["crack_width"], 2)
            }
            
        return snapshot

# Test run
if __name__ == "__main__":
    sim = DataSimulator()
    print(sim.generate_next_tick())
