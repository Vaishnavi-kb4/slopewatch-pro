
# mine_safety_system/dashboard/style.py
import streamlit as st

def apply_custom_style():
    st.markdown("""
        <style>
        /* Import Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&family=Roboto+Mono:wght@400;700&display=swap');

        /* Global Theme */
        .stApp {
            background-color: #0E1117; /* Dark Background */
            color: #E0E0E0;
            font-family: 'Inter', sans-serif;
        }

        /* Headings */
        h1, h2, h3 {
            color: #FFFFFF;
            font-weight: 700;
        }
        
        /* Sidebar */
        section[data-testid="stSidebar"] {
            background-color: #161B22;
        }

        /* Cards / Metrics */
        div[data-testid="metric-container"] {
            background-color: #1D232F;
            border-radius: 10px;
            padding: 15px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
            border: 1px solid #30363D;
        }

        /* Custom Cards (div wrapper) */
        .glass-card {
            background: rgba(29, 35, 47, 0.9);
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            border: 1px solid rgba(255,255,255,0.05);
            margin-bottom: 20px;
        }

        /* Buttons (CTA) */
        .stButton button {
            background-color: #238636; /* GitHub Green */
            color: white;
            border-radius: 6px;
            font-weight: 600;
            border: none;
            padding: 10px 24px;
        }
        .stButton button:hover {
            background-color: #2EA043;
        }

        /* Landing Page Hero Text */
        .hero-title {
            font-size: 3rem !important;
            font-weight: 800;
            background: -webkit-linear-gradient(45deg, #00C9FF, #92FE9D);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-align: center;
            margin-bottom: 1rem;
        }
        .hero-subtitle {
            font-size: 1.5rem;
            color: #A0A0A0;
            text-align: center;
            margin-bottom: 2rem;
        }
        
        /* Risk Colors */
        .risk-low { color: #3FB950; font-weight: bold; }
        .risk-med { color: #D29922; font-weight: bold; }
        .risk-high { color: #F85149; font-weight: bold; }
        
        /* Animations */
        @keyframes pulse-red {
            0% { box-shadow: 0 0 0 0 rgba(248, 81, 73, 0.7); }
            70% { box-shadow: 0 0 0 10px rgba(248, 81, 73, 0); }
            100% { box-shadow: 0 0 0 0 rgba(248, 81, 73, 0); }
        }
        .pulse-critical {
            animation: pulse-red 2s infinite;
            border: 1px solid #F85149 !important;
        }
        
        /* Typography */
        .big-prob {
            font-size: 2.2rem !important;
            font-weight: 800;
        }
        </style>
    """, unsafe_allow_html=True)
