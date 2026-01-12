
# mine_safety_system/agents/perception_agent.py
import threading
import time
import random
from mine_safety_system.utils.shared_state import state
from mine_safety_system.utils.config import *

class PerceptionAgent(threading.Thread):
    """
    Simulates processing of Drone/DEM data.
    In a real system, this would process images.
    Here, it monitors 'crack_width' and 'elevation_delta' proxies.
    """
    def __init__(self):
        super().__init__()
        self.running = True

    def run(self):
        while self.running:
            # Fetch latest raw sensor data to see ground truth 'crack_width'
            # In reality, this would be its own independent data source (Images)
            # We access the "latest" sensor data as a proxy for the physical reality
            current_state = state.get("sensor_data")
            
            terrain_analysis = {}
            if current_state:
                for zone, data in current_state.items():
                    raw = data.get("raw", {})
                    crack_width = raw.get("crack_width", 0)
                    
                    # Image Processing Simulation:
                    # Detect if crack width is expanding
                    risk_score = 0.0
                    if crack_width > 5.0:
                        risk_score = 0.8 # High visible deformation
                    elif crack_width > 2.0:
                        risk_score = 0.4 # Minor cracking
                    
                    terrain_analysis[zone] = {
                        "visual_risk_score": risk_score,
                        "detected_features": ["CRACK_SET_A"] if risk_score > 0.5 else [],
                        "last_drone_scan": time.time()
                    }

            state.update("terrain_data", terrain_analysis)
            time.sleep(UPDATE_INTERVAL * 2) # Drone updates are slower

    def stop(self):
        self.running = False
