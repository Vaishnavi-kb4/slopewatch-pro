
# mine_safety_system/dashboard/views/landing.py
import streamlit as st

def render_landing():
    # Hide sidebar on landing page if possible, or just ignore it
    st.markdown('<div style="padding-top: 50px;"></div>', unsafe_allow_html=True)
    
    # Hero Section
    st.markdown('<p class="hero-title">Predict Rockfalls Before They Happen</p>', unsafe_allow_html=True)
    st.markdown('<p class="hero-subtitle">SlopeWatch Pro: Predictive Intelligence for Safer Mines</p>', unsafe_allow_html=True)
    
    # Animated Visual (Placeholder using an image or simple graph)
    # Ideally use a Lottie animation here, but for strict python we'll use a wide graph
    st.markdown("---")
    
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        if st.button("VIEW LIVE SAFETY DASHBOARD", use_container_width=True):
            st.session_state["page"] = "dashboard"
            st.rerun()

    st.markdown("---")

    # 3 Key Benefits
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="glass-card">
            <h3>Early Warning AI</h3>
            <p>Detect micro-movements sensors miss. Get alerts hours before failure.</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="glass-card">
            <h3>Multi-Agent System</h3>
            <p>5 autonomous agents cross-validate data to eliminate false alarms.</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="glass-card">
            <h3>Zero Blind Spots</h3>
            <p>Fusion of Satellite, Drone, and Ground sensor data in real-time.</p>
        </div>
        """, unsafe_allow_html=True)
