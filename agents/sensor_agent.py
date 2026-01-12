
# mine_safety_system/agents/sensor_agent.py
import threading
import time
import numpy as np
from collections import deque
from mine_safety_system.utils.shared_state import state
from mine_safety_system.utils.config import *

class SensorAgent(threading.Thread):
    def __init__(self, simulator_ref):
        super().__init__()
        self.sim = simulator_ref
        self.running = True
        self.history = {z: {"tilt": deque(maxlen=10), "strain": deque(maxlen=10)} for z in SIMULATION_ZONES}

    def run(self):
        while self.running:
            raw_data = self.sim.generate_next_tick()
            processed_data = {}

            for zone, metrics in raw_data.items():
                # 1. Store history
                self.history[zone]["tilt"].append(metrics["tilt"])
                self.history[zone]["strain"].append(metrics["strain"])

                # 2. Smooth data (Moving Average)
                avg_tilt = np.mean(self.history[zone]["tilt"])
                avg_strain = np.mean(self.history[zone]["strain"])

                # 3. Detect Anomalies (Simple Z-score like check against threshold)
                tilt_status = "NORMAL"
                if abs(avg_tilt) > TILT_THRESHOLD:
                    tilt_status = "WARNING"
                
                processed_data[zone] = {
                    "tilt_smooth": round(avg_tilt, 3),
                    "strain_smooth": round(avg_strain, 6),
                    "status": tilt_status,
                    "raw": metrics
                }
            
            # Publish to shared state
            state.update("sensor_data", processed_data)
            time.sleep(UPDATE_INTERVAL)

    def stop(self):
        self.running = False
