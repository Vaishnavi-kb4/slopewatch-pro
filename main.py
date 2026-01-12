
# mine_safety_system/main.py
import time
import sys
from mine_safety_system.data.simulation import DataSimulator
from mine_safety_system.agents.sensor_agent import SensorAgent
from mine_safety_system.agents.perception_agent import PerceptionAgent
from mine_safety_system.agents.env_risk_agent import EnvRiskAgent
from mine_safety_system.agents.predictive_agent import PredictiveAgent
from mine_safety_system.agents.alert_agent import AlertAgent
from mine_safety_system.utils.shared_state import state

def main():
    print("Starting Mine Safety System Agents...")
    
    # 1. Init Simulator
    sim = DataSimulator()
    
    # 2. Init Agents
    agents = [
        SensorAgent(sim),
        PerceptionAgent(),
        EnvRiskAgent(),
        PredictiveAgent(),
        AlertAgent()
    ]
    
    # 3. Start Agents
    for a in agents:
        a.start()
        print(f"Started {a.__class__.__name__}")
        
    print("All System Agents Online. Press Ctrl+C to stop.")
    
    try:
        while True:
            # Main thread monitors or logs
            # For prototype, we just keep alive
            time.sleep(1)
            # Maybe print a summary every 10s?
            
    except KeyboardInterrupt:
        print("\nStopping System...")
        for a in agents:
            a.stop()
        for a in agents:
            a.join()
        print("System shutdown complete.")

if __name__ == "__main__":
    main()
