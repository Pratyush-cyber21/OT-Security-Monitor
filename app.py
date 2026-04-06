# DRIFTNET - OT Security Operations Center
# Production-grade Streamlit dashboard with custom UI

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import time
from datetime import datetime
import streamlit.components.v1 as components

import base64
try:
    with open("beep.wav", "rb") as f:
        ALERT_SOUND_B64 = base64.b64encode(f.read()).decode('utf-8')
except:
    ALERT_SOUND_B64 = ""


st.set_page_config(
    page_title="DRIFTNET — OT Threat Intelligence Platform",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── CUSTOM CSS: Dark industrial SOC aesthetic ──────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Rajdhani:wght@400;600;700&family=Orbitron:wght@400;700;900&display=swap');

/* Global */
html, body, [class*="css"] {
    font-family: 'Rajdhani', sans-serif;
    background-color: #060a10 !important;
    color: #c9d6e3 !important;
}

/* Hide Streamlit branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* App background with grid pattern */
.stApp {
    background-color: #060a10 !important;
    background-image:
        linear-gradient(rgba(0,200,255,0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0,200,255,0.03) 1px, transparent 1px);
    background-size: 40px 40px;
}

/* Main title */
.main-title {
    font-family: 'Orbitron', monospace;
    font-size: 2.4rem;
    font-weight: 900;
    letter-spacing: 0.15em;
    background: linear-gradient(90deg, #00B4D8, #06D6A0, #00B4D8);
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: shine 3s linear infinite;
    margin-bottom: 0;
}
@keyframes shine {
    to { background-position: 200% center; }
}

.sub-title {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.85rem;
    color: #4a7fa5;
    letter-spacing: 0.2em;
    margin-top: 2px;
}

/* Divider */
.custom-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, #00B4D844, #06D6A044, transparent);
    margin: 12px 0 20px 0;
}

/* KPI cards */
.kpi-card {
    background: linear-gradient(135deg, #0d1b2a, #0a1520);
    border: 1px solid #1a3a52;
    border-top: 2px solid #00B4D844;
    border-radius: 6px;
    padding: 18px 20px;
    text-align: center;
    position: relative;
    overflow: hidden;
}
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, #00B4D8, transparent);
}
.kpi-label {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.65rem;
    color: #4a7fa5;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    margin-bottom: 8px;
}
.kpi-value {
    font-family: 'Orbitron', monospace;
    font-size: 1.6rem;
    font-weight: 700;
    color: #00B4D8;
}
.kpi-value.danger { color: #E63946; }
.kpi-value.safe { color: #06D6A0; }
.kpi-value.warn { color: #F4A261; }

/* Attack banner */
.attack-banner {
    background: linear-gradient(135deg, #1a0008, #2d0010);
    border: 1px solid #E63946;
    border-left: 4px solid #E63946;
    border-radius: 6px;
    padding: 14px 20px;
    display: flex;
    align-items: center;
    gap: 12px;
    animation: pulse-border 1s ease-in-out infinite;
}
@keyframes pulse-border {
    0%, 100% { border-left-color: #E63946; box-shadow: 0 0 0 0 #E6394644; }
    50% { border-left-color: #ff6b8a; box-shadow: 0 0 20px 4px #E6394622; }
}
.attack-icon {
    font-size: 1.8rem;
    animation: blink 0.8s step-end infinite;
}
@keyframes blink { 50% { opacity: 0; } }
.attack-title {
    font-family: 'Orbitron', monospace;
    font-size: 1rem;
    font-weight: 700;
    color: #E63946;
    letter-spacing: 0.1em;
}
.attack-detail {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.75rem;
    color: #ff8099;
    margin-top: 3px;
}
.mitre-badge {
    background: #E6394622;
    border: 1px solid #E6394655;
    border-radius: 4px;
    padding: 4px 10px;
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.75rem;
    color: #E63946;
    margin-left: auto;
    white-space: nowrap;
}

/* Normal banner */
.normal-banner {
    background: linear-gradient(135deg, #001a12, #001f16);
    border: 1px solid #06D6A033;
    border-left: 4px solid #06D6A0;
    border-radius: 6px;
    padding: 12px 20px;
    display: flex;
    align-items: center;
    gap: 10px;
}
.normal-text {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.8rem;
    color: #06D6A0;
    letter-spacing: 0.1em;
}

/* Section headers */
.section-header {
    font-family: 'Orbitron', monospace;
    font-size: 0.75rem;
    font-weight: 700;
    color: #4a7fa5;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    margin-bottom: 12px;
    display: flex;
    align-items: center;
    gap: 8px;
}
.section-header::after {
    content: '';
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, #1a3a52, transparent);
}

/* Incident table */
.incident-row-critical { background: #1a0008 !important; border-left: 3px solid #E63946; }
.incident-row-high { background: #1a0d00 !important; border-left: 3px solid #F4A261; }
.incident-row-medium { background: #0d1a0a !important; border-left: 3px solid #FFD166; }

/* Severity pills */
.sev-critical {
    background: #E6394622; color: #E63946;
    border: 1px solid #E6394655;
    border-radius: 3px; padding: 2px 8px;
    font-family: 'Share Tech Mono', monospace; font-size: 0.7rem;
}
.sev-high {
    background: #F4A26122; color: #F4A261;
    border: 1px solid #F4A26155;
    border-radius: 3px; padding: 2px 8px;
    font-family: 'Share Tech Mono', monospace; font-size: 0.7rem;
}
.sev-medium {
    background: #FFD16622; color: #FFD166;
    border: 1px solid #FFD16655;
    border-radius: 3px; padding: 2px 8px;
    font-family: 'Share Tech Mono', monospace; font-size: 0.7rem;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #080d14 !important;
    border-right: 1px solid #1a3a52 !important;
}
section[data-testid="stSidebar"] .stButton > button {
    background: linear-gradient(135deg, #0d1b2a, #0a1520) !important;
    border: 1px solid #1a3a52 !important;
    color: #00B4D8 !important;
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 0.8rem !important;
    letter-spacing: 0.1em !important;
    border-radius: 4px !important;
    transition: all 0.2s !important;
}
section[data-testid="stSidebar"] .stButton > button:active {
    background: #00B4D8 !important;
    color: #000 !important;
    transform: scale(0.95) !important;
    box-shadow: 0 0 20px #00B4D8 !important;
}

/* Attack inject button (primary) */
section[data-testid="stSidebar"] button[kind="primary"] {
    background: linear-gradient(135deg, #1a0008, #2d0010) !important;
    border: 1px solid #E6394655 !important;
    color: #E63946 !important;
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 0.8rem !important;
    letter-spacing: 0.1em !important;
    border-radius: 4px !important;
    transition: all 0.2s !important;
}
section[data-testid="stSidebar"] button[kind="primary"]:hover {
    border-color: #E63946 !important;
    box-shadow: 0 0 12px #E6394622 !important;
}
section[data-testid="stSidebar"] button[kind="primary"]:active {
    background: #E63946 !important;
    color: #fff !important;
    transform: scale(0.95) !important;
    box-shadow: 0 0 20px #E63946 !important;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    background: transparent !important;
    gap: 4px;
    border-bottom: 1px solid #1a3a52;
}
.stTabs [data-baseweb="tab"] {
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 0.75rem !important;
    letter-spacing: 0.15em !important;
    color: #4a7fa5 !important;
    background: transparent !important;
    border: none !important;
    padding: 8px 20px !important;
}
.stTabs [aria-selected="true"] {
    color: #00B4D8 !important;
    border-bottom: 2px solid #00B4D8 !important;
}

/* Metrics */
[data-testid="stMetricValue"] {
    font-family: 'Orbitron', monospace !important;
    font-size: 1.4rem !important;
    color: #00B4D8 !important;
}
[data-testid="stMetricLabel"] {
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 0.65rem !important;
    letter-spacing: 0.15em !important;
    color: #4a7fa5 !important;
    text-transform: uppercase !important;
}

/* Dataframe */
.stDataFrame {
    border: 1px solid #1a3a52 !important;
    border-radius: 6px !important;
}

/* Scrollbar */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #060a10; }
::-webkit-scrollbar-thumb { background: #1a3a52; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #00B4D844; }

/* Selectbox, slider */
.stSelectbox > div > div {
    background: #0d1b2a !important;
    border-color: #1a3a52 !important;
    color: #c9d6e3 !important;
    font-family: 'Share Tech Mono', monospace !important;
}
.stSlider > div > div > div {
    background: #00B4D8 !important;
}
</style>
""", unsafe_allow_html=True)

# ── SESSION STATE INIT ─────────────────────────────────────
defaults = {
    'running': False, 'current_index': 0,
    'packet_count': 0, 'threat_count': 0,
    'sensor_history': [], 'pump_history': [],
    'attack_flags': [], 'confidence': 0.0,
    'models_loaded': False, 'df': None,
    'iso': None, 'svm': None, 'scaler': None, 'cols': None,
    'iso': None, 'svm': None, 'scaler': None, 'cols': None,
    'last_alert': None, 'last_is_attack': False, 'force_attack': False,
    'force_rerun': False
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

from db import init_db, log_incident, get_all_incidents, get_stats, ack_incident
from mitre_map import classify_attack, get_alert_message
init_db()

# Load models
if not st.session_state.models_loaded:
    try:
        from ai_engine import load_models
        (st.session_state.iso, st.session_state.svm,
         st.session_state.scaler, st.session_state.cols) = load_models()
        st.session_state.models_loaded = True
    except:
        st.session_state.models_loaded = False

# Load data
if st.session_state.df is None:
    for path in ['data/batadal_test.csv', 'data/batadal_train2.csv']:
        try:
            from data_pump import load_data
            st.session_state.df = load_data(path)
            break
        except:
            continue

# ── SIDEBAR ────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 10px 0 20px 0;'>
        <div style='font-family: Orbitron, monospace; font-size: 1.3rem;
                    font-weight: 900; color: #00B4D8; letter-spacing: 0.15em;'>
            DRIFT<span style='color:#06D6A0'>NET</span>
        </div>
        <div style='font-family: Share Tech Mono, monospace; font-size: 0.6rem;
                    color: #4a7fa5; letter-spacing: 0.2em; margin-top: 4px;'>
            POWERED BY ISOLATION FOREST + OC-SVM
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div style="height:1px;background:linear-gradient(90deg,transparent,#00B4D844,transparent);margin-bottom:16px;"></div>', unsafe_allow_html=True)

    st.markdown('<div style="font-family: Share Tech Mono, monospace; font-size: 0.65rem; color: #4a7fa5; letter-spacing: 0.2em; margin-bottom: 6px;">DETECTION MODEL</div>', unsafe_allow_html=True)
    model_choice = st.selectbox("", ["Ensemble (Both)", "Isolation Forest", "One-Class SVM"], label_visibility="collapsed")

    st.markdown('<div style="font-family: Share Tech Mono, monospace; font-size: 0.65rem; color: #4a7fa5; letter-spacing: 0.2em; margin: 12px 0 6px 0;">SIMULATION SPEED</div>', unsafe_allow_html=True)
    speed = st.slider("", 1, 5, 1, label_visibility="collapsed")

    st.markdown('<div style="height:1px;background:linear-gradient(90deg,transparent,#1a3a52,transparent);margin: 12px 0;"></div>', unsafe_allow_html=True)

    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("▶  START", use_container_width=True):
            st.session_state.running = True
    with col_b:
        if st.button("⏹  STOP", use_container_width=True):
            st.session_state.running = False

    inject_btn = st.button("⚡ INJECT TEST ATTACK", type="primary", use_container_width=True)

    st.markdown("---")
    mute = st.toggle("🔇 Mute Alerts", value=st.session_state.get("mute_alerts", False), key="mute_toggle")
    st.session_state["mute_alerts"] = mute

    if inject_btn and st.session_state.models_loaded and st.session_state.df is not None:
        st.session_state.force_attack = True

    st.markdown('<div style="height:1px;background:linear-gradient(90deg,transparent,#1a3a52,transparent);margin: 16px 0;"></div>', unsafe_allow_html=True)

    # Engine status
    if st.session_state.models_loaded:
        st.markdown("""
        <div style='background:#001a12; border:1px solid #06D6A033; border-radius:4px;
                    padding:8px 12px; display:flex; align-items:center; gap:8px;'>
            <div style='width:8px;height:8px;border-radius:50%;background:#06D6A0;
                        box-shadow:0 0 6px #06D6A0; animation: pulse 2s infinite;'></div>
            <span style='font-family:Share Tech Mono,monospace;font-size:0.7rem;
                         color:#06D6A0;letter-spacing:0.1em;'>AI ENGINE ONLINE</span>
        </div>
        <style>@keyframes pulse{0%,100%{opacity:1}50%{opacity:0.4}}</style>
        """, unsafe_allow_html=True)
        if st.button("⚙ RETRAIN MODELS", use_container_width=True):
            with st.spinner("Training on BATADAL data..."):
                from ai_engine import train_models, load_models
                train_models()
                (st.session_state.iso, st.session_state.svm,
                 st.session_state.scaler, st.session_state.cols) = load_models()
                st.session_state.models_loaded = True
                st.session_state.last_train_time = datetime.now().strftime("%H:%M:%S")
                st.rerun()
        if st.session_state.get('last_train_time'):
            st.markdown(f"<div style='font-size:0.65rem;color:#8b949e;text-align:center;'>Last retrained: {st.session_state.last_train_time}</div>", unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style='background:#1a0008; border:1px solid #E6394633; border-radius:4px;
                    padding:8px 12px; display:flex; align-items:center; gap:8px;'>
            <div style='width:8px;height:8px;border-radius:50%;background:#E63946;'></div>
            <span style='font-family:Share Tech Mono,monospace;font-size:0.7rem;
                         color:#E63946;letter-spacing:0.1em;'>AI ENGINE OFFLINE</span>
        </div>
        """, unsafe_allow_html=True)
        if st.button("⚙ TRAIN MODELS", use_container_width=True):
            with st.spinner("Training on BATADAL data..."):
                from ai_engine import train_models, load_models
                train_models()
                (st.session_state.iso, st.session_state.svm,
                 st.session_state.scaler, st.session_state.cols) = load_models()
                st.session_state.models_loaded = True
                st.session_state.last_train_time = datetime.now().strftime("%H:%M:%S")
                st.rerun()

    st.markdown('<div style="height:1px;background:linear-gradient(90deg,transparent,#1a3a52,transparent);margin: 16px 0;"></div>', unsafe_allow_html=True)

    stats = get_stats()
    st.markdown('<div style="font-family:Share Tech Mono,monospace;font-size:0.65rem;color:#4a7fa5;letter-spacing:0.2em;margin-bottom:10px;">INCIDENT STATISTICS</div>', unsafe_allow_html=True)
    
    # Mini dashboard inline split
    total = stats['total_incidents']
    if total > 0:
        c_pct = (stats['critical_count']/total)*100
        h_pct = (stats['high_count']/total)*100
        st.markdown(f"""
        <div style="width:100%; height:8px; display:flex; border-radius:4px; overflow:hidden; margin-bottom:8px;">
            <div style="width:{c_pct}%; background:#E63946;"></div>
            <div style="width:{h_pct}%; background:#F4A261;"></div>
            <div style="flex-grow:1; background:#06D6A0;"></div>
        </div>
        """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    c1.metric("TOTAL", stats['total_incidents'])
    c2.metric("OPEN", stats['open_incidents'])
    c3, c4 = st.columns(2)
    c3.metric("CRITICAL", stats['critical_count'])
    c4.metric("HIGH", stats['high_count'])

# ── MAIN HEADER ────────────────────────────────────────────
st.markdown("""
<div style='margin-bottom: 4px;'>
    <div class='main-title'>DRIFTNET</div>
    <div class='sub-title'>// OT THREAT INTELLIGENCE PLATFORM // BATADAL WATER NETWORK //</div>
</div>
<div class='custom-divider'></div>
""", unsafe_allow_html=True)

tab1, tab2, tab3, tab_arch = st.tabs(["  🔴  LIVE MONITOR  ", "  📊  BENCHMARK  ", "  ℹ️  ABOUT  ", "  🏗  ARCHITECTURE  "])

with tab1:
    banner_ph = st.empty()
    st.markdown("<div style='margin:10px 0 6px 0;'></div>", unsafe_allow_html=True)

    # KPI Row
    k1, k2, k3, k4 = st.columns(4)
    status_ph = k1.empty()
    packets_ph = k2.empty()
    threats_ph = k3.empty()
    conf_ph = k4.empty()

    st.markdown("<div style='margin: 16px 0 8px 0;'></div>", unsafe_allow_html=True)
    st.markdown('<div class="section-header">SENSOR TELEMETRY — LIVE FEED</div>', unsafe_allow_html=True)

    c_left, c_right = st.columns([6, 4])
    with c_left:
        chart1_ph = st.empty()
    with c_right:
        chart2_ph = st.empty()

    st.markdown("<div style='margin: 16px 0 8px 0;'></div>", unsafe_allow_html=True)
    hc1, hc2 = st.columns([8, 2])
    with hc1:
        st.markdown('<div class="section-header">🚨 INCIDENT RESPONSE LOG</div>', unsafe_allow_html=True)
    with hc2:
        mute_t2 = st.toggle("🔇 Mute Audio", value=st.session_state.get("mute_alerts", False), key="mute_t2")
        st.session_state["mute_alerts"] = mute_t2

    alert_log_ph = st.empty()
    audio_ph = st.empty()

    def render_incident_board(ph, incidents):
        with ph.container():
            if not incidents:
                st.markdown('<div style="font-family:monospace;font-size:0.75rem;color:#2a5a7a;padding:20px;text-align:center;border:1px solid #1a3a52;border-radius:4px;">// NO INCIDENTS LOGGED — SYSTEM NOMINAL //</div>', unsafe_allow_html=True)
                return
            
            sev_col = {"CRITICAL": "#E63946", "HIGH": "#F4A261", "MEDIUM": "#FFD166", "LOW": "#06D6A0"}
            
            h1, h2, h3, h4, h5 = st.columns([1.5, 3, 2, 4, 1.5])
            h1.markdown("<span style='font-size:0.7rem; color:#8b949e; letter-spacing:1px;'>TIME</span>", unsafe_allow_html=True)
            h2.markdown("<span style='font-size:0.7rem; color:#8b949e; letter-spacing:1px;'>MITRE</span>", unsafe_allow_html=True)
            h3.markdown("<span style='font-size:0.7rem; color:#8b949e; letter-spacing:1px;'>SEVERITY</span>", unsafe_allow_html=True)
            h4.markdown("<span style='font-size:0.7rem; color:#8b949e; letter-spacing:1px;'>ACTION</span>", unsafe_allow_html=True)
            h5.markdown("<span style='font-size:0.7rem; color:#8b949e; letter-spacing:1px;'>STATUS</span>", unsafe_allow_html=True)
            st.markdown("<hr style='margin:4px 0 8px 0; border:none; border-top:1px solid #1a3a52;'>", unsafe_allow_html=True)
            
            for inc in incidents[:4]:
                c1, c2, c3, c4, c5 = st.columns([1.5, 3, 2, 4, 1.5])
                time_str = inc['timestamp'][11:19]
                c1.markdown(f"<span style='font-size:0.75rem;'>{time_str}</span>", unsafe_allow_html=True)
                c2.markdown(f"<span style='font-size:0.75rem; color:#00B4D8;'>{inc['mitre_id']}</span>", unsafe_allow_html=True)
                
                sc = sev_col.get(inc['severity'], "#00B4D8")
                c3.markdown(f"<span style='background:{sc}22; color:{sc}; padding:2px 6px; border:1px solid {sc}55; border-radius:3px; font-size:0.65rem;'>{inc['severity']}</span>", unsafe_allow_html=True)
                
                act = str(inc.get('operator_action', ''))
                act_trunc = act[:25] + "..." if len(act) > 25 else act
                c4.markdown(f"<span title='{act}' style='font-size:0.7rem; color:#8b949e;'>{act_trunc}</span>", unsafe_allow_html=True)
                
                if inc['status'] == 'OPEN':
                    if c5.button("ACK", key=f"ack_{inc['id']}_{time_str}", use_container_width=True):
                        ack_incident(inc['id'])
                        st.session_state.force_rerun = True
                else:
                    c5.markdown(f"<span style='font-size:0.7rem; color:#06D6A0; padding-top:6px; display:inline-block;'>ACK'd</span>", unsafe_allow_html=True)

    # ── STREAMING LOOP ─────────────────────────────────────
    run_frame = st.session_state.running or st.session_state.force_attack
    if run_frame and st.session_state.models_loaded and st.session_state.df is not None:
        df = st.session_state.df
        idx = st.session_state.current_index % len(df)
        row = df.iloc[idx].to_dict()

        if st.session_state.force_attack:
            from data_pump import inject_attack
            row = inject_attack(row)
            st.session_state.force_attack = False

        from ai_engine import predict
        result = predict(row, st.session_state.iso, st.session_state.svm,
                        st.session_state.scaler, st.session_state.cols)

        try:
            lt1 = float(row.get('L_T1', 0))
        except:
            lt1 = 0.0
        try:
            pu1 = float(row.get('F_PU1', 0))
        except:
            pu1 = 0.0

        st.session_state.sensor_history.append(lt1)
        st.session_state.pump_history.append(pu1)
        st.session_state.attack_flags.append(result['is_attack'])
        st.session_state.sensor_history = st.session_state.sensor_history[-60:]
        st.session_state.pump_history = st.session_state.pump_history[-60:]
        st.session_state.attack_flags = st.session_state.attack_flags[-60:]
        st.session_state.packet_count += 1
        st.session_state.current_index += 1
        st.session_state.confidence = result['confidence']
        st.session_state.last_is_attack = result['is_attack']

        if result['is_attack']:
            st.session_state.threat_count += 1
            mitre = classify_attack(result['triggered_features'])
            st.session_state.last_alert = mitre
            log_incident({
                'timestamp': str(datetime.now()),
                'affected_sensors': str(result['triggered_features']),
                'iso_score': result['iso_score'], 'svm_score': result['svm_score'],
                'confidence': result['confidence'], 'mitre_id': mitre['technique_id'],
                'mitre_technique': mitre['technique_name'], 'severity': mitre['severity'],
                'operator_action': mitre['operator_action'], 'status': 'OPEN'
            })

        # Banner
        if result['is_attack'] and st.session_state.last_alert:
            m = st.session_state.last_alert
            sev_col = "#E63946" if m['severity'] == "CRITICAL" else "#F4A261"
            if m['severity'] == "CRITICAL":
                banner_ph.markdown(f"""
                <div style="background:#E63946; color:white; padding:12px 20px; 
                     border-radius:4px; animation:blinker 1s linear infinite; font-family:monospace;">
                🚨 CRITICAL THREAT DETECTED — IMMEDIATE OPERATOR ACTION REQUIRED<br>
                <span style="font-size:0.8rem; color:#ffcccc;">{m['description'][:80]}... | Sensors: {result['triggered_features']}</span>
                </div>
                <style>@keyframes blinker {{ 50% {{ opacity: 0; }} }}</style>
                """, unsafe_allow_html=True)
            else:
                banner_ph.markdown(f"""
                <div class='attack-banner' style="border-color:{sev_col}; border-left-color:{sev_col}; background:linear-gradient(135deg, #1a0000, #2d0000);">
                    <div class='attack-icon'>⚠️</div>
                    <div>
                        <div class='attack-title' style="color:{sev_col};">INTRUSION DETECTED — {m['severity']} SEVERITY</div>
                        <div class='attack-detail' style="color:white;">{m['description'][:80]}... | Sensors: {result['triggered_features']}</div>
                    </div>
                    <div class='mitre-badge' style="color:{sev_col}; border-color:{sev_col}55; background:{sev_col}22;">{m['technique_id']} · {m['technique_name']}</div>
                </div>
                """, unsafe_allow_html=True)
                
            if not st.session_state.get("mute_alerts", False):
                audio_ph.markdown(f"""
                <audio autoplay>
                  <source src="data:audio/wav;base64,{ALERT_SOUND_B64}" type="audio/wav">
                </audio>
                """, unsafe_allow_html=True)
        else:
            banner_ph.markdown("""
            <div class='normal-banner' style="border-color:#06D6A033; border-left-color:#06D6A0;">
                <div style='width:8px;height:8px;border-radius:50%;background:#06D6A0;box-shadow:0 0 8px #06D6A0;flex-shrink:0; animation: pulse 2s infinite;'></div>
                <span class='normal-text' style="color:#06D6A0;">ALL SYSTEMS NOMINAL — MONITORING ACTIVE — NO THREATS DETECTED</span>
            </div>
            """, unsafe_allow_html=True)
            audio_ph.empty()

        # KPIs
        def metric_card(label, value, color="#00B4D8", icon=""):
            return f"""
            <div style="background: #0d1117; border: 1px solid {color}33; border-left: 3px solid {color}; border-radius: 4px; padding: 14px 18px; margin-bottom: 8px;">
                <div style="font-size:10px; color:#8b949e; letter-spacing:2px; text-transform:uppercase;">{icon} {label}</div>
                <div style="font-size:24px; font-weight:700; color:{color}; font-family:monospace; margin-top:4px;">{value}</div>
            </div>
            """
            
        stat_color = "#E63946" if result['is_attack'] else "#06D6A0"
        stat_text = "CRITICAL" if result['is_attack'] else "NOMINAL"
        status_ph.markdown(metric_card("SYSTEM STATUS", stat_text, color=stat_color, icon="🔴" if result['is_attack'] else "🟢"), unsafe_allow_html=True)
        packets_ph.markdown(metric_card("PACKETS SCANNED", f"{st.session_state.packet_count:,}", color="#00B4D8"), unsafe_allow_html=True)
        threats_col = "#E63946" if st.session_state.threat_count > 0 else "#00B4D8"
        threats_ph.markdown(metric_card("ACTIVE THREATS", st.session_state.threat_count, color=threats_col), unsafe_allow_html=True)
        conf_ph.markdown(metric_card("DETECTION CONF.", f"{result['confidence']:.1f}%", color="#00B4D8"), unsafe_allow_html=True)

        # Tank Level Chart
        n = len(st.session_state.sensor_history)
        colors = ['#E63946' if f else '#00B4D8' for f in st.session_state.attack_flags]
        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(
            x=list(range(n)), y=st.session_state.sensor_history,
            mode='lines+markers',
            line=dict(color='#00B4D8', width=2),
            marker=dict(color=colors, size=5, line=dict(width=0)),
            fill='tozeroy',
            fillcolor='rgba(0,200,255,0.05)',
            name='Tank L_T1'
        ))
        
        fig1.update_layout(
            title=dict(text='TANK 1 WATER LEVEL', font=dict(family='Share Tech Mono', size=11, color='#4a7fa5'), x=0),
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#4a7fa5', family='Share Tech Mono', size=10),
            xaxis=dict(gridcolor='#0d1b2a', linecolor='#1a3a52', tickfont=dict(color='#2a5a7a')),
            yaxis=dict(gridcolor='#0d1b2a', linecolor='#1a3a52', tickfont=dict(color='#2a5a7a')),
            margin=dict(l=10, r=10, t=30, b=10), height=280,
            showlegend=False
        )
        chart1_ph.plotly_chart(fig1, use_container_width=True)

        # Pump Gauge
        gauge_color = '#E63946' if result['is_attack'] else '#06D6A0'
        fig2 = go.Figure(go.Indicator(
            mode="gauge+number",
            value=pu1,
            number=dict(font=dict(family='Orbitron', color=gauge_color, size=28)),
            title=dict(text='PUMP 1 FLOW RATE', font=dict(family='Share Tech Mono', color='#4a7fa5', size=10)),
            gauge=dict(
                axis=dict(range=[0, 300], tickcolor='#1a3a52',
                          tickfont=dict(color='#2a5a7a', family='Share Tech Mono', size=9)),
                bar=dict(color=gauge_color, thickness=0.25),
                bgcolor='#0d1b2a',
                bordercolor='#1a3a52',
                steps=[
                    dict(range=[0, 100], color='#0a1520'),
                    dict(range=[100, 200], color='#0d1b2a'),
                    dict(range=[200, 300], color='#1a0d0d')
                ]
            )
        ))
        fig2.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', font=dict(color='#4a7fa5'),
            margin=dict(l=10, r=10, t=10, b=10), height=280
        )
        chart2_ph.plotly_chart(fig2, use_container_width=True)

        # Incident log
        incidents = get_all_incidents()
        render_incident_board(alert_log_ph, incidents)

        if st.session_state.get("force_rerun"):
            st.session_state.force_rerun = False
            st.rerun()

        time.sleep(max(0.3, 1.0 / speed))
        st.rerun()

    else:
        # Static standby state
        if not st.session_state.running:
            banner_ph.markdown("""
            <div style='background:#0d1400;border:1px solid #F4A26133;border-left:4px solid #F4A261;
                        border-radius:6px;padding:12px 20px;display:flex;align-items:center;gap:10px;'>
                <span style='font-size:1.2rem;'>⏸</span>
                <span style='font-family:Share Tech Mono,monospace;font-size:0.8rem;
                             color:#F4A261;letter-spacing:0.1em;'>MONITORING PAUSED — PRESS START TO BEGIN SURVEILLANCE</span>
            </div>
            """, unsafe_allow_html=True)
        status_ph.metric("SYSTEM STATUS", "⏸ STANDBY")
        packets_ph.metric("PACKETS SCANNED", f"{st.session_state.packet_count:,}")
        threats_ph.metric("ACTIVE THREATS", st.session_state.threat_count)
        conf_ph.metric("DETECTION CONF.", "—")
        incidents = get_all_incidents()
        if incidents:
            inc_df = pd.DataFrame(incidents)
            show_cols = ['timestamp', 'mitre_id', 'mitre_technique', 'severity', 'affected_sensors', 'status']
            show_cols = [c for c in show_cols if c in inc_df.columns]
            alert_log_ph.dataframe(inc_df[show_cols], use_container_width=True, height=180)
        else:
            alert_log_ph.markdown('<div style="font-family:Share Tech Mono,monospace;font-size:0.75rem;color:#2a5a7a;padding:20px;text-align:center;border:1px solid #1a3a52;border-radius:4px;">// NO INCIDENTS LOGGED — START MONITORING TO BEGIN //</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="section-header" style="margin-top:16px;">MODEL PERFORMANCE — BATADAL BENCHMARK</div>', unsafe_allow_html=True)
    st.markdown('<div style="font-family:Share Tech Mono,monospace;font-size:0.75rem;color:#4a7fa5;margin-bottom:20px;">Comparing DRIFTNET against Zahoor 2025 (reference paper cited by Hitachi in the problem statement)</div>', unsafe_allow_html=True)
    if st.button("▶  RUN BENCHMARK NOW", use_container_width=False):
        with st.spinner("Running evaluation on BATADAL dataset..."):
            from benchmark import run_benchmark
            our_results, comp_df = run_benchmark()
            if comp_df is not None:
                st.dataframe(comp_df, use_container_width=True)
                fig_b = go.Figure()
                colors_b = ['#00B4D8', '#E63946']
                for i, metric in enumerate(['F1 Score', 'Precision', 'Recall', 'Accuracy']):
                    fig_b.add_trace(go.Bar(
                        name=metric, x=comp_df['Model'], y=comp_df[metric],
                        text=[f"{v:.3f}" for v in comp_df[metric]],
                        textposition='outside',
                        textfont=dict(family='Share Tech Mono', size=10),
                        marker_color=['#00B4D8', '#E63946']
                    ))
                fig_b.update_layout(
                    barmode='group',
                    title=dict(text='DRIFTNET vs ZAHOOR 2025 REFERENCE', font=dict(family='Share Tech Mono', size=11, color='#4a7fa5'), x=0),
                    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#4a7fa5', family='Share Tech Mono', size=10),
                    xaxis=dict(gridcolor='#0d1b2a', linecolor='#1a3a52'),
                    yaxis=dict(gridcolor='#0d1b2a', linecolor='#1a3a52', range=[0, 1.1]),
                    legend=dict(bgcolor='rgba(0,0,0,0)', bordercolor='#1a3a52', borderwidth=1),
                    height=380, margin=dict(t=40)
                )
                st.plotly_chart(fig_b, use_container_width=True)
                st.markdown(f"""
                <div style='background:#001520;border:1px solid #00B4D833;border-left:3px solid #00B4D8;
                            border-radius:4px;padding:14px 18px;font-family:Share Tech Mono,monospace;
                            font-size:0.8rem;color:#00B4D8;'>
                    ✓ DRIFTNET — F1: {our_results['F1 Score']} &nbsp;|&nbsp;
                    Precision: {our_results['Precision']} &nbsp;|&nbsp;
                    Recall: {our_results['Recall']} &nbsp;|&nbsp;
                    Accuracy: {our_results['Accuracy']}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.error("Train models first using the sidebar button.")

with tab_arch:
    st.markdown('<div class="section-header" style="margin-top:16px;">SYSTEM ARCHITECTURE</div>', unsafe_allow_html=True)
    st.graphviz_chart("""
    digraph G {
        rankdir=LR;
        node [shape=box, style=filled, fillcolor="#0d1117", fontcolor="#00B4D8", color="#00B4D8", fontname="monospace"]
        edge [color="#4a7fa5"]
        A [label="BATADAL\\nDataset"]
        B [label="data_pump.py\\nFeature Engineering"]
        C [label="Isolation Forest\\n(n=200, contam=0.06)"]
        D [label="One-Class SVM\\n(kernel=rbf, nu=0.05)"]
        E [label="Weighted Ensemble\\nVoter (0.6 / 0.4)"]
        F [label="DRIFTNET\\nStreamlit Dashboard"]
        G [label="MITRE ATT&CK\\nMapper"]
        
        A -> B -> C -> E
        B -> D -> E
        E -> F
        E -> G -> F
    }
    """)
    
    st.markdown("""
    <div style='font-family:Rajdhani,sans-serif;line-height:1.8;color:#8aa8c0;max-width:800px;'>
    <h3 style='color:#00B4D8;font-family:Orbitron,monospace;font-size:1.1rem;margin-top:20px;'>Why This Architecture?</h3>
    <ul>
    <li><strong style='color:#00B4D8;'>Passive monitoring</strong> — no writes to OT network, zero disruption to Modbus/DNP3 traffic.</li>
    <li><strong style='color:#00B4D8;'>Edge-deployable</strong> — entire stack runs on <2GB RAM, suitable for industrial edge nodes.</li>
    <li><strong style='color:#00B4D8;'>Ensemble design</strong> — IsoForest handles global anomalies; OC-SVM handles boundary cases.</li>
    <li><strong style='color:#00B4D8;'>MITRE ATT&CK ICS mapping</strong> — every alert maps to recognizable standard taxonomy for operator context.</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

with tab3:
    st.markdown('<div class="section-header" style="margin-top:16px;">ABOUT THE PROJECT</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style='font-family:Rajdhani,sans-serif;line-height:1.8;color:#8aa8c0;max-width:800px;'>
    <h2 style='color:#00B4D8;font-family:Orbitron,monospace;font-size:1.4rem;'>Why DRIFTNET?</h2>
    <p>Water treatment plants, power grids, and manufacturing lines run on 30-year-old protocols — 
    Modbus, DNP3, EtherNet/IP — never designed for a connected world.</p>

    <p>DRIFTNET was built with one constraint: <strong style='color:#00B4D8;'>touch nothing, see everything.</strong></p>

    <p>By passively reading process telemetry from sensors already in place, our ensemble 
    AI engine detects behavioral anomalies — pump flow spikes, tank level manipulation, 
    unauthorized command sequences — without a single packet injected into the OT network.</p>

    <h3 style='color:#00B4D8;font-family:Orbitron,monospace;font-size:1.1rem;margin-top:20px;'>Tech Stack</h3>
    <ul>
    <li><strong style='color:#00B4D8;'>Dataset</strong>: BATADAL (Battle of the Attack Detection Algorithms) — Water Distribution</li>
    <li><strong style='color:#00B4D8;'>Models</strong>: Isolation Forest + One-Class SVM (Ensemble)</li>
    <li><strong style='color:#00B4D8;'>Reference</strong>: Zahoor et al., 2025 — used as accuracy benchmark</li>
    <li><strong style='color:#00B4D8;'>Interface</strong>: Streamlit — deployable on any industrial workstation</li>
    </ul>

    <h3 style='color:#00B4D8;font-family:Orbitron,monospace;font-size:1.1rem;margin-top:20px;'>Hackathon Context</h3>
    <p>Built for Hitachi's AI-Assisted OT Security Monitoring challenge.<br>
    Evaluation dimensions: Approach · Architecture · Problem Solving · Maturity · Presentation</p>
    </div>

    <div style='margin-top:40px;font-family:Share Tech Mono,monospace;font-size:0.7rem;
                color:#2a5a7a;text-align:center;padding-top:16px;
                border-top:1px solid #1a3a52;'>
        DRIFTNET · VISISONICS AI'26 HACKATHON · MANIPAL INSTITUTE OF TECHNOLOGY BENGALURU
    </div>
    """, unsafe_allow_html=True)
