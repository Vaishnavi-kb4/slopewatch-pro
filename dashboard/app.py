
# mine_safety_system/dashboard/app.py
import sys
import os
import time
import streamlit as st

# Add parent of parent dir to path to import mine_safety_system as a package
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from dashboard.style import apply_custom_style
from mine_safety_system.dashboard.views.landing import render_landing
from mine_safety_system.dashboard.views.main_dashboard import render_dashboard
from mine_safety_system.dashboard.views.zone_detail import render_zone_detail
from mine_safety_system.dashboard.views.intelligence import render_intelligence
from mine_safety_system.utils.shared_state import state

from mine_safety_system.data.simulation import DataSimulator
from mine_safety_system.agents.sensor_agent import SensorAgent
from mine_safety_system.agents.perception_agent import PerceptionAgent
from mine_safety_system.agents.env_risk_agent import EnvRiskAgent
from mine_safety_system.agents.predictive_agent import PredictiveAgent
from mine_safety_system.agents.alert_agent import AlertAgent

# Page Config
st.set_page_config(page_title="SlopeWatch Pro", layout="wide", page_icon=None)

# Apply CSS
apply_custom_style()

# --- Agent Startup ---
@st.cache_resource
def start_system():
    sim = DataSimulator()
    agents = [
        SensorAgent(sim),
        PerceptionAgent(),
        EnvRiskAgent(),
        PredictiveAgent(),
        AlertAgent()
    ]
    for a in agents:
        a.start()
    return agents

_ = start_system()

# --- Router Logic ---
if "page" not in st.session_state:
    st.session_state["page"] = "landing"

# Sidebar Navigation (Hidden on Landing Page)
if st.session_state["page"] != "landing":
    with st.sidebar:
        st.markdown("## SlopeWatch Pro")
        st.markdown("---")
        
        nav = st.radio("Navigation", ["Live Dashboard", "Zone Details", "System Intelligence"])
        
        if nav == "Live Dashboard":
            st.session_state["page"] = "dashboard"
        elif nav == "Zone Details":
            st.session_state["page"] = "details"
        elif nav == "System Intelligence":
            st.session_state["page"] = "intelligence"
            
        st.markdown("---")
        # --- Drill Toggle ---
        drill = st.toggle("Demo Critical Scenario")
        state.update("drill_mode", drill)
        if drill:
            st.caption("🔴 DRILL ACTIVE: Zone B Critical")
            
        st.markdown("---")
        if st.button("Logout"):
            st.session_state["page"] = "landing"
            st.rerun()

# Page Rendering
if st.session_state["page"] == "landing":
    render_landing()
elif st.session_state["page"] == "dashboard":
    render_dashboard()
    time.sleep(2) # Auto-refresh
    st.rerun()
elif st.session_state["page"] == "details":
    render_zone_detail()
elif st.session_state["page"] == "intelligence":
    render_intelligence()
