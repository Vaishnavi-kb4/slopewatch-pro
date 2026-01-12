
# mine_safety_system/dashboard/views/intelligence.py
import streamlit as st

def render_intelligence():
    st.markdown("## System Intelligence Architecture")
    
    st.markdown("""
    <div class="glass-card">
        <h3>Multi-Agent Neural Network</h3>
        <p>SlopeWatch Pro uses a mesh of 5 specialized agents working in consensus.</p>
    </div>
    """, unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### 📡 1. Sensor Agent")
        st.caption("Inputs: Tilt, Strain, Seismic")
        st.caption("Role: Signal Denoising & Anomaly Detection")
        
        st.markdown("#### 🚁 2. Perception Agent")
        st.caption("Inputs: Drone Imagery, DEM")
        st.caption("Role: Visual Deformation Tracking")
        
        st.markdown("#### 🌧️ 3. Environmental Agent")
        st.caption("Inputs: Rain, Temp, Groundwater")
        st.caption("Role: Pore Pressure Modeling")

    with c2:
        st.markdown("#### 🧠 4. Predictive Brain (Core)")
        st.caption("Model: Ensemble (LSTM + Bayesian)")
        st.caption("Output: Probability of Failure (PoF)")
        
        st.markdown("#### 🚨 5. Alert Agent")
        st.caption("Logic: Thresholds + Human-in-the-loop")
        st.caption("Output: Actionable Mitigation Plans")
