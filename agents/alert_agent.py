
# mine_safety_system/agents/alert_agent.py
import threading
import time
from mine_safety_system.utils.shared_state import state
from mine_safety_system.utils.config import *

class AlertAgent(threading.Thread):
    def __init__(self):
        super().__init__()
        self.running = True
        self.last_alert_time = {} # Debounce alerts

    def run(self):
        while self.running:
            preds = state.get("predictions", {})
            
            for zone, p_data in preds.items():
                risk = p_data.get("risk_level")
                prob = p_data.get("probability", 0)
                
                # Check for critical thresholds
                if risk in [RISK_HIGH, RISK_CRITICAL]:
                    self.trigger_alert(zone, risk, prob, p_data.get("time_to_failure_hours"))
            
            time.sleep(UPDATE_INTERVAL)

    def trigger_alert(self, zone, risk, prob, ttf):
        # Debounce: Don't spam alerts for same zone every second
        last = self.last_alert_time.get(zone, 0)
        if time.time() - last < 10: # 10 seconds cooldown
            return

        # Mitigation Logic
        mitigation = "Continue monitoring."
        if risk == RISK_CRITICAL:
            mitigation = "EVACUATE IMMEDIATELY. Stop all machinery."
        elif risk == RISK_HIGH:
            mitigation = "Suspend excavation. Inspect slope stability."
        
        alert = {
            "timestamp": time.time(),
            "zone": zone,
            "level": risk,
            "message": f"Slope instability detected in {zone}. Prob: {prob*100:.1f}%",
            "mitigation": mitigation,
            "ttf": ttf
        }
        
        state.add_alert(alert)
        self.last_alert_time[zone] = time.time()
        # In a real system, this would send SMS/Email/Siren

    def stop(self):
        self.running = False
