
# mine_safety_system/utils/shared_state.py
import threading
import time
from typing import Dict, Any, List

class SharedState:
    def __init__(self):
        self._lock = threading.Lock()
        self.data: Dict[str, Any] = {
            "timestamp": time.time(),
            "sensor_data": {},
            "terrain_data": {},
            "env_data": {},
            "predictions": {},
            "alerts": []
        }
    
    def update(self, key: str, value: Any):
        with self._lock:
            self.data[key] = value
            self.data["timestamp"] = time.time()
            
    def get(self, key: str, default=None):
        with self._lock:
            return self.data.get(key, default)

    def get_all(self):
        with self._lock:
            return self.data.copy()

    def add_alert(self, alert: Dict[str, Any]):
        with self._lock:
            # Keep only last 50 alerts
            self.data["alerts"].append(alert)
            if len(self.data["alerts"]) > 50:
                self.data["alerts"].pop(0)

# Global instance
state = SharedState()
