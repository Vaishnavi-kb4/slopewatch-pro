
# mine_safety_system/dashboard/views/main_dashboard.py
import streamlit as st
import pandas as pd
import altair as alt
import time
from mine_safety_system.utils.shared_state import state
from mine_safety_system.utils.config import SIMULATION_ZONES

def render_dashboard():
    st.markdown("## Live Safety Dashboard", unsafe_allow_html=True)
    
    # 1. Fetch Data
    predictions = state.get("predictions", {})
    sensor_data = state.get("sensor_data", {})
    env_data = state.get("env_data", {})
    alerts = state.get("alerts", [])
    
    # 2. Main Layout: Left (Nav/Filter is handled by appSidebar), Center (Heatmap), Right (Stats)
    # Since sidebar is global, we use columns here for Center/Right split
    
    col_center, col_right = st.columns([2, 1])
    
    with col_center:
        st.markdown("### Risk Heatmap")
        # Reuse Altair Heatmap Logic
        heatmap_data = []
        for z, p in predictions.items():
            x = 0
            if z == "Zone B": x = 1
            if z == "Zone C": x = 2
            heatmap_data.append({"x": x, "y": 0, "risk": p["probability"], "zone": z})
            
        df_heat = pd.DataFrame(heatmap_data)
        if not df_heat.empty:
            c = alt.Chart(df_heat).mark_rect().encode(
                x=alt.X('zone:N', title=""),
                y=alt.Y('y:O', axis=None),
                color=alt.Color('risk:Q', scale=alt.Scale(scheme='redyellowgreen', reverse=True), legend=None),
                tooltip=['zone', 'risk']
            ).properties(height=300)
            st.altair_chart(c, use_container_width=True)
        else:
            st.info("Initializing Map...")
            
    with col_right:
        st.markdown("### Live Stats")
        
        # Calculate Stats
        sorted_by_prob = sorted(predictions.items(), key=lambda x: x[1]['probability'], reverse=True)
        sorted_by_delta = sorted(predictions.items(), key=lambda x: x[1].get('trend_delta', 0), reverse=True)
        
        most_volatile = sorted_by_prob[0][0] if sorted_by_prob else "N/A"
        safest = sorted_by_prob[-1][0] if sorted_by_prob else "N/A"
        
        fastest_increase = "N/A"
        if sorted_by_delta and sorted_by_delta[0][1].get('trend_delta', 0) > 0.01:
            fastest_increase = sorted_by_delta[0][0]
        
        # --- Zone Comparison Summary Card ---
        st.markdown(f"""
        <div class="glass-card">
            <h4>Zone Comparison Summary</h4>
            <p><strong>Most Volatile:</strong> {most_volatile}</p>
            <p><strong>Safest Zone:</strong> {safest}</p>
            <p><strong>Fastest Rising:</strong> {fastest_increase}</p>
        </div>
        """, unsafe_allow_html=True)

        # --- Readiness ---
        top_prob = sorted_by_prob[0][1]['probability'] if sorted_by_prob else 0
        readiness = "Stable"
        r_color = "#3FB950"
        if top_prob >= 0.85:
            readiness = "CRITICAL"
            r_color = "#F85149"
        elif top_prob >= 0.6:
            readiness = "WARNING"
            r_color = "#D29922"
        elif top_prob >= 0.3:
            readiness = "PRE-WARNING"
            r_color = "#D29922"
        elif top_prob >= 0.1:
            readiness = "MONITORING"
            r_color = "#2f81f7"
            
        st.markdown(f"""
        <div class="glass-card">
            <h4>System Status</h4>
            <h2 style="color:{r_color}">{readiness}</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # --- What-If Simulation ---
        st.markdown("### What-If Simulation")
        with st.container(): # Use container for grouping
             if st.button("Simulate Heavy Rainfall (+50%)", use_container_width=True):
                 st.markdown("#### Simulation Results")
                 # Logic: Recalculate prob with Env factor * 1.5
                 # Formula: (S*0.4) + (T*0.3) + (E*0.3)
                 
                 # Terrain & Sensor inputs (approx from state)
                 terrain = state.get("terrain_data", {})
                 
                 for zone in SIMULATION_ZONES:
                     # Get current Env
                     e_data = env_data.get(zone, {})
                     current_env = e_data.get("pore_pressure_index", 0.0)
                     sim_env = min(1.0, current_env * 1.5)
                     
                     # Get others
                     s_data = sensor_data.get(zone, {})
                     s_factor = 1.0 if s_data.get("status") == "WARNING" else 0.2
                     
                     t_data = terrain.get(zone, {})
                     t_factor = t_data.get("visual_risk_score", 0.0)
                     
                     # Calc
                     current_prob = predictions.get(zone, {}).get("probability", 0.0)
                     sim_prob = (s_factor * 0.4) + (t_factor * 0.3) + (sim_env * 0.3)
                     sim_prob = min(1.0, max(0.0, sim_prob)) # clamp
                     
                     if sim_prob > current_prob + 0.01:
                         # TTF estimation (simple heuristic)
                         sim_ttf = "N/A"
                         if sim_prob > 0.8: sim_ttf = "< 4h"
                         elif sim_prob > 0.6: sim_ttf = "12h"
                         
                         st.error(f"**{zone}**: Risk rises to {sim_prob*100:.0f}% (TTF: {sim_ttf})")
                     else:
                         st.success(f"**{zone}**: Stable at {sim_prob*100:.0f}%")

    # 3. Zone Details Row
    st.markdown("### Zone Intelligence")
    
    # Check for Critical System State for Banner
    if sorted_by_prob and sorted_by_prob[0][1]['probability'] > 0.8:
        st.error("🚨 **CRITICAL ALERT: IMMEDIATE EVACUATION ORDER FOR ACTIVE ZONES** 🚨")
    
    cols = st.columns(len(SIMULATION_ZONES))
    for idx, zone in enumerate(SIMULATION_ZONES):
        pred = predictions.get(zone, {})
        with cols[idx]:
            st.markdown(f"#### {zone}")
            
            risk_lvl = pred.get("risk_level", "LOW")
            prob = pred.get("probability", 0)
            conf = pred.get("confidence", 0)
            trend_icon = pred.get("trend_icon", "→")
            
            r_class = "risk-low"
            card_class = "glass-card"
            
            if risk_lvl == "HIGH": 
                r_class = "risk-med"
            if risk_lvl == "CRITICAL": 
                r_class = "risk-high"
                card_class = "glass-card pulse-critical" # Pulse Animation
            
            # Larger Font for Probability
            prob_html = f'<span class="big-prob {r_class}">{prob*100:.0f}%</span>'
            
            st.markdown(f"""
            <div class="{card_class}">
                <span class="{r_class}">{risk_lvl}</span><br>
                {prob_html}<br>
                Trend: {trend_icon} {pred.get('trend', 'Stable')} (45 min)<br>
                Velocity: {pred.get('risk_velocity', '0% / 10min')}<br>
                Conf: {conf*100:.0f}%
            </div>
            """, unsafe_allow_html=True)
            
            # Why This Risk?
            contribs = pred.get("contributors", [])
            with st.expander("Why This Risk?"):
                for c in contribs:
                    st.caption(f"• {c}")
