# ClearCatchICS - OT Security Operations Center
# Production-grade Streamlit dashboard with custom UI

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import time
from datetime import datetime

st.set_page_config(
    page_title="ClearCatchICS — OT Security Monitor",
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
    background: linear-gradient(90deg, #00c8ff, #00ff9d, #00c8ff);
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
    background: linear-gradient(90deg, transparent, #00c8ff44, #00ff9d44, transparent);
    margin: 12px 0 20px 0;
}

/* KPI cards */
.kpi-card {
    background: linear-gradient(135deg, #0d1b2a, #0a1520);
    border: 1px solid #1a3a52;
    border-top: 2px solid #00c8ff44;
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
    background: linear-gradient(90deg, transparent, #00c8ff, transparent);
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
    color: #00c8ff;
}
.kpi-value.danger { color: #ff3b5c; }
.kpi-value.safe { color: #00ff9d; }
.kpi-value.warn { color: #ffb830; }

/* Attack banner */
.attack-banner {
    background: linear-gradient(135deg, #1a0008, #2d0010);
    border: 1px solid #ff3b5c;
    border-left: 4px solid #ff3b5c;
    border-radius: 6px;
    padding: 14px 20px;
    display: flex;
    align-items: center;
    gap: 12px;
    animation: pulse-border 1s ease-in-out infinite;
}
@keyframes pulse-border {
    0%, 100% { border-left-color: #ff3b5c; box-shadow: 0 0 0 0 #ff3b5c44; }
    50% { border-left-color: #ff6b8a; box-shadow: 0 0 20px 4px #ff3b5c22; }
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
    color: #ff3b5c;
    letter-spacing: 0.1em;
}
.attack-detail {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.75rem;
    color: #ff8099;
    margin-top: 3px;
}
.mitre-badge {
    background: #ff3b5c22;
    border: 1px solid #ff3b5c55;
    border-radius: 4px;
    padding: 4px 10px;
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.75rem;
    color: #ff3b5c;
    margin-left: auto;
    white-space: nowrap;
}

/* Normal banner */
.normal-banner {
    background: linear-gradient(135deg, #001a12, #001f16);
    border: 1px solid #00ff9d33;
    border-left: 4px solid #00ff9d;
    border-radius: 6px;
    padding: 12px 20px;
    display: flex;
    align-items: center;
    gap: 10px;
}
.normal-text {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.8rem;
    color: #00ff9d;
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
.incident-row-critical { background: #1a0008 !important; border-left: 3px solid #ff3b5c; }
.incident-row-high { background: #1a0d00 !important; border-left: 3px solid #ffb830; }
.incident-row-medium { background: #0d1a0a !important; border-left: 3px solid #a8ff3b; }

/* Severity pills */
.sev-critical {
    background: #ff3b5c22; color: #ff3b5c;
    border: 1px solid #ff3b5c55;
    border-radius: 3px; padding: 2px 8px;
    font-family: 'Share Tech Mono', monospace; font-size: 0.7rem;
}
.sev-high {
    background: #ffb83022; color: #ffb830;
    border: 1px solid #ffb83055;
    border-radius: 3px; padding: 2px 8px;
    font-family: 'Share Tech Mono', monospace; font-size: 0.7rem;
}
.sev-medium {
    background: #a8ff3b22; color: #a8ff3b;
    border: 1px solid #a8ff3b55;
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
    color: #00c8ff !important;
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 0.8rem !important;
    letter-spacing: 0.1em !important;
    border-radius: 4px !important;
    transition: all 0.2s !important;
}
section[data-testid="stSidebar"] .stButton > button:hover {
    border-color: #00c8ff !important;
    box-shadow: 0 0 12px #00c8ff22 !important;
    background: #0d2030 !important;
}

/* Attack inject button */
.inject-btn > button {
    background: linear-gradient(135deg, #1a0008, #2d0010) !important;
    border: 1px solid #ff3b5c55 !important;
    color: #ff3b5c !important;
}
.inject-btn > button:hover {
    border-color: #ff3b5c !important;
    box-shadow: 0 0 12px #ff3b5c22 !important;
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
    color: #00c8ff !important;
    border-bottom: 2px solid #00c8ff !important;
}

/* Metrics */
[data-testid="stMetricValue"] {
    font-family: 'Orbitron', monospace !important;
    font-size: 1.4rem !important;
    color: #00c8ff !important;
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
::-webkit-scrollbar-thumb:hover { background: #00c8ff44; }

/* Selectbox, slider */
.stSelectbox > div > div {
    background: #0d1b2a !important;
    border-color: #1a3a52 !important;
    color: #c9d6e3 !important;
    font-family: 'Share Tech Mono', monospace !important;
}
.stSlider > div > div > div {
    background: #00c8ff !important;
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
    'last_alert': None, 'last_is_attack': False
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

from db import init_db, log_incident, get_all_incidents, get_stats
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
                    font-weight: 900; color: #00c8ff; letter-spacing: 0.15em;'>
            CLEAR<span style='color:#00ff9d'>CATCH</span>ICS
        </div>
        <div style='font-family: Share Tech Mono, monospace; font-size: 0.6rem;
                    color: #4a7fa5; letter-spacing: 0.2em; margin-top: 4px;'>
            OT SECURITY OPERATIONS CENTER
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div style="height:1px;background:linear-gradient(90deg,transparent,#00c8ff44,transparent);margin-bottom:16px;"></div>', unsafe_allow_html=True)

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

    st.markdown('<div class="inject-btn">', unsafe_allow_html=True)
    inject_btn = st.button("⚡ INJECT TEST ATTACK", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    if inject_btn and st.session_state.models_loaded and st.session_state.df is not None:
        from data_pump import inject_attack
        from ai_engine import predict
        idx = st.session_state.current_index % len(st.session_state.df)
        row = st.session_state.df.iloc[idx].to_dict()
        attacked = inject_attack(row)
        result = predict(attacked, st.session_state.iso, st.session_state.svm,
                        st.session_state.scaler, st.session_state.cols)
        mitre = classify_attack(result['triggered_features'])
        log_incident({
            'timestamp': str(datetime.now()),
            'affected_sensors': str(result['triggered_features']),
            'iso_score': result['iso_score'], 'svm_score': result['svm_score'],
            'confidence': result['confidence'], 'mitre_id': mitre['technique_id'],
            'mitre_technique': mitre['technique_name'], 'severity': mitre['severity'],
            'operator_action': mitre['operator_action'], 'status': 'OPEN'
        })
        st.session_state.threat_count += 1
        st.session_state.last_alert = mitre
        st.session_state.last_is_attack = True

    st.markdown('<div style="height:1px;background:linear-gradient(90deg,transparent,#1a3a52,transparent);margin: 16px 0;"></div>', unsafe_allow_html=True)

    # Engine status
    if st.session_state.models_loaded:
        st.markdown("""
        <div style='background:#001a12; border:1px solid #00ff9d33; border-radius:4px;
                    padding:8px 12px; display:flex; align-items:center; gap:8px;'>
            <div style='width:8px;height:8px;border-radius:50%;background:#00ff9d;
                        box-shadow:0 0 6px #00ff9d; animation: pulse 2s infinite;'></div>
            <span style='font-family:Share Tech Mono,monospace;font-size:0.7rem;
                         color:#00ff9d;letter-spacing:0.1em;'>AI ENGINE ONLINE</span>
        </div>
        <style>@keyframes pulse{0%,100%{opacity:1}50%{opacity:0.4}}</style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style='background:#1a0008; border:1px solid #ff3b5c33; border-radius:4px;
                    padding:8px 12px; display:flex; align-items:center; gap:8px;'>
            <div style='width:8px;height:8px;border-radius:50%;background:#ff3b5c;'></div>
            <span style='font-family:Share Tech Mono,monospace;font-size:0.7rem;
                         color:#ff3b5c;letter-spacing:0.1em;'>AI ENGINE OFFLINE</span>
        </div>
        """, unsafe_allow_html=True)
        if st.button("⚙ TRAIN MODELS", use_container_width=True):
            with st.spinner("Training on BATADAL data..."):
                from ai_engine import train_models, load_models
                train_models()
                (st.session_state.iso, st.session_state.svm,
                 st.session_state.scaler, st.session_state.cols) = load_models()
                st.session_state.models_loaded = True
                st.rerun()

    st.markdown('<div style="height:1px;background:linear-gradient(90deg,transparent,#1a3a52,transparent);margin: 16px 0;"></div>', unsafe_allow_html=True)

    stats = get_stats()
    st.markdown('<div style="font-family:Share Tech Mono,monospace;font-size:0.65rem;color:#4a7fa5;letter-spacing:0.2em;margin-bottom:10px;">INCIDENT STATISTICS</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    c1.metric("TOTAL", stats['total_incidents'])
    c2.metric("OPEN", stats['open_incidents'])
    c3, c4 = st.columns(2)
    c3.metric("CRITICAL", stats['critical_count'])
    c4.metric("HIGH", stats['high_count'])

# ── MAIN HEADER ────────────────────────────────────────────
st.markdown("""
<div style='margin-bottom: 4px;'>
    <div class='main-title'>CLEARCATCHICS</div>
    <div class='sub-title'>// INDUSTRIAL CONTROL SYSTEM — THREAT DETECTION ENGINE // BATADAL WATER NETWORK //</div>
</div>
<div class='custom-divider'></div>
""", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["  🔴  LIVE MONITOR  ", "  📊  BENCHMARK  ", "  ℹ️  ABOUT  "])

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
    st.markdown('<div class="section-header">🚨 INCIDENT RESPONSE LOG</div>', unsafe_allow_html=True)
    alert_log_ph = st.empty()

    # ── STREAMING LOOP ─────────────────────────────────────
    if st.session_state.running and st.session_state.models_loaded and st.session_state.df is not None:
        df = st.session_state.df
        idx = st.session_state.current_index % len(df)
        row = df.iloc[idx].to_dict()

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
            banner_ph.markdown(f"""
            <div class='attack-banner'>
                <div class='attack-icon'>⚠</div>
                <div>
                    <div class='attack-title'>INTRUSION DETECTED — {m['severity']} SEVERITY</div>
                    <div class='attack-detail'>{m['description'][:80]}... | Sensors: {result['triggered_features']}</div>
                </div>
                <div class='mitre-badge'>{m['technique_id']} · {m['technique_name']}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            banner_ph.markdown("""
            <div class='normal-banner'>
                <div style='width:8px;height:8px;border-radius:50%;background:#00ff9d;box-shadow:0 0 8px #00ff9d;flex-shrink:0;'></div>
                <span class='normal-text'>ALL SYSTEMS NOMINAL — MONITORING ACTIVE — NO THREATS DETECTED</span>
            </div>
            """, unsafe_allow_html=True)

        # KPIs
        status_ph.metric("SYSTEM STATUS", "🔴 UNDER ATTACK" if result['is_attack'] else "🟢 NOMINAL")
        packets_ph.metric("PACKETS SCANNED", f"{st.session_state.packet_count:,}")
        threats_ph.metric("ACTIVE THREATS", st.session_state.threat_count)
        conf_ph.metric("DETECTION CONF.", f"{result['confidence']:.1f}%")

        # Tank Level Chart
        n = len(st.session_state.sensor_history)
        colors = ['#ff3b5c' if f else '#00c8ff' for f in st.session_state.attack_flags]
        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(
            x=list(range(n)), y=st.session_state.sensor_history,
            mode='lines+markers',
            line=dict(color='#00c8ff', width=2),
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
        gauge_color = '#ff3b5c' if result['is_attack'] else '#00ff9d'
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
                ],
                threshold=dict(line=dict(color='#ff3b5c', width=2), thickness=0.75, value=250)
            )
        ))
        fig2.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', font=dict(color='#4a7fa5'),
            margin=dict(l=10, r=10, t=10, b=10), height=280
        )
        chart2_ph.plotly_chart(fig2, use_container_width=True)

        # Incident log
        incidents = get_all_incidents()
        if incidents:
            inc_df = pd.DataFrame(incidents)
            show_cols = ['timestamp', 'mitre_id', 'mitre_technique', 'severity', 'affected_sensors', 'operator_action', 'status']
            show_cols = [c for c in show_cols if c in inc_df.columns]
            alert_log_ph.dataframe(inc_df[show_cols], use_container_width=True, height=180)
        else:
            alert_log_ph.markdown('<div style="font-family:Share Tech Mono,monospace;font-size:0.75rem;color:#2a5a7a;padding:20px;text-align:center;border:1px solid #1a3a52;border-radius:4px;">// NO INCIDENTS LOGGED — SYSTEM NOMINAL //</div>', unsafe_allow_html=True)

        time.sleep(max(0.3, 1.0 / speed))
        st.rerun()

    else:
        # Static standby state
        if not st.session_state.running:
            banner_ph.markdown("""
            <div style='background:#0d1400;border:1px solid #ffb83033;border-left:4px solid #ffb830;
                        border-radius:6px;padding:12px 20px;display:flex;align-items:center;gap:10px;'>
                <span style='font-size:1.2rem;'>⏸</span>
                <span style='font-family:Share Tech Mono,monospace;font-size:0.8rem;
                             color:#ffb830;letter-spacing:0.1em;'>MONITORING PAUSED — PRESS START TO BEGIN SURVEILLANCE</span>
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
    st.markdown('<div style="font-family:Share Tech Mono,monospace;font-size:0.75rem;color:#4a7fa5;margin-bottom:20px;">Comparing ClearCatchICS against Zahoor 2025 (reference paper cited by Hitachi in the problem statement)</div>', unsafe_allow_html=True)
    if st.button("▶  RUN BENCHMARK NOW", use_container_width=False):
        with st.spinner("Running evaluation on BATADAL dataset..."):
            from benchmark import run_benchmark
            our_results, comp_df = run_benchmark()
            if comp_df is not None:
                st.dataframe(comp_df, use_container_width=True)
                fig_b = go.Figure()
                colors_b = ['#00c8ff', '#ff3b5c']
                for i, metric in enumerate(['F1 Score', 'Precision', 'Recall', 'Accuracy']):
                    fig_b.add_trace(go.Bar(
                        name=metric, x=comp_df['Model'], y=comp_df[metric],
                        text=[f"{v:.3f}" for v in comp_df[metric]],
                        textposition='outside',
                        textfont=dict(family='Share Tech Mono', size=10),
                        marker_color=['#00c8ff', '#ff3b5c88']
                    ))
                fig_b.update_layout(
                    barmode='group',
                    title=dict(text='CLEARCATCHICS vs ZAHOOR 2025 REFERENCE', font=dict(family='Share Tech Mono', size=11, color='#4a7fa5'), x=0),
                    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#4a7fa5', family='Share Tech Mono', size=10),
                    xaxis=dict(gridcolor='#0d1b2a', linecolor='#1a3a52'),
                    yaxis=dict(gridcolor='#0d1b2a', linecolor='#1a3a52', range=[0, 1.1]),
                    legend=dict(bgcolor='rgba(0,0,0,0)', bordercolor='#1a3a52', borderwidth=1),
                    height=380, margin=dict(t=40)
                )
                st.plotly_chart(fig_b, use_container_width=True)
                st.markdown(f"""
                <div style='background:#001520;border:1px solid #00c8ff33;border-left:3px solid #00c8ff;
                            border-radius:4px;padding:14px 18px;font-family:Share Tech Mono,monospace;
                            font-size:0.8rem;color:#00c8ff;'>
                    ✓ ClearCatchICS — F1: {our_results['F1 Score']} &nbsp;|&nbsp;
                    Precision: {our_results['Precision']} &nbsp;|&nbsp;
                    Recall: {our_results['Recall']} &nbsp;|&nbsp;
                    Accuracy: {our_results['Accuracy']}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.error("Train models first using the sidebar button.")

with tab3:
    st.markdown('<div class="section-header" style="margin-top:16px;">SYSTEM OVERVIEW</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style='font-family:Rajdhani,sans-serif;line-height:1.8;color:#8aa8c0;max-width:800px;'>
    <p><strong style='color:#00c8ff;font-family:Orbitron,monospace;font-size:0.9rem;'>ClearCatchICS</strong>
    is a lightweight AI-powered SOC for Industrial Control System security. It passively monitors
    SCADA telemetry from water treatment infrastructure, detects cyberattacks using ensemble ML,
    and maps every alert to the MITRE ATT&CK for ICS framework — giving operators actionable
    intelligence without disrupting operations.</p>
    </div>

    <div style='margin-top:24px;font-family:Share Tech Mono,monospace;font-size:0.65rem;
                color:#4a7fa5;letter-spacing:0.2em;margin-bottom:10px;'>ARCHITECTURE PIPELINE</div>
    <div style='background:#0a1520;border:1px solid #1a3a52;border-radius:6px;padding:20px;
                font-family:Share Tech Mono,monospace;font-size:0.75rem;color:#00c8ff;
                line-height:2.2;'>
    BATADAL DATASET &nbsp;→&nbsp; DATA PUMP (CSV stream @ 1Hz)
    &nbsp;→&nbsp; AI ENGINE (Isolation Forest + One-Class SVM)
    &nbsp;→&nbsp; ENSEMBLE VOTE &nbsp;→&nbsp; MITRE ATT&CK ICS MAPPING
    &nbsp;→&nbsp; SOC DASHBOARD &nbsp;→&nbsp; SQLITE INCIDENT DB
    </div>

    <div style='margin-top:24px;display:grid;grid-template-columns:1fr 1fr;gap:16px;'>
        <div style='background:#0a1520;border:1px solid #1a3a52;border-radius:6px;padding:16px;'>
            <div style='font-family:Share Tech Mono,monospace;font-size:0.65rem;color:#4a7fa5;
                        letter-spacing:0.2em;margin-bottom:10px;'>DETECTION MODELS</div>
            <div style='font-family:Rajdhani,sans-serif;color:#8aa8c0;font-size:0.95rem;'>
                • Isolation Forest (unsupervised anomaly detection)<br>
                • One-Class SVM (boundary-based detection)<br>
                • Ensemble voting — reduced false positives
            </div>
        </div>
        <div style='background:#0a1520;border:1px solid #1a3a52;border-radius:6px;padding:16px;'>
            <div style='font-family:Share Tech Mono,monospace;font-size:0.65rem;color:#4a7fa5;
                        letter-spacing:0.2em;margin-bottom:10px;'>THREAT INTELLIGENCE</div>
            <div style='font-family:Rajdhani,sans-serif;color:#8aa8c0;font-size:0.95rem;'>
                • MITRE ATT&CK for ICS taxonomy<br>
                • T0831 · T0855 · T0856 · T0801 · T0882<br>
                • Auto-generated incident reports
            </div>
        </div>
        <div style='background:#0a1520;border:1px solid #1a3a52;border-radius:6px;padding:16px;'>
            <div style='font-family:Share Tech Mono,monospace;font-size:0.65rem;color:#4a7fa5;
                        letter-spacing:0.2em;margin-bottom:10px;'>DATASET</div>
            <div style='font-family:Rajdhani,sans-serif;color:#8aa8c0;font-size:0.95rem;'>
                • BATADAL — Battle of Attack Detection Algorithms<br>
                • C-Town water distribution network<br>
                • 43 SCADA sensors · 7 attack scenarios
            </div>
        </div>
        <div style='background:#0a1520;border:1px solid #1a3a52;border-radius:6px;padding:16px;'>
            <div style='font-family:Share Tech Mono,monospace;font-size:0.65rem;color:#4a7fa5;
                        letter-spacing:0.2em;margin-bottom:10px;'>DESIGN PRINCIPLES</div>
            <div style='font-family:Rajdhani,sans-serif;color:#8aa8c0;font-size:0.95rem;'>
                • Zero infrastructure changes — passive only<br>
                • Lightweight — runs on edge hardware<br>
                • Protocol-agnostic at feature level
            </div>
        </div>
    </div>
    <div style='margin-top:20px;font-family:Share Tech Mono,monospace;font-size:0.7rem;
                color:#2a5a7a;text-align:center;padding-top:16px;
                border-top:1px solid #1a3a52;'>
        CLEARCATCHICS · VISISONICS AI'26 HACKATHON · MANIPAL INSTITUTE OF TECHNOLOGY BENGALURU
    </div>
    """, unsafe_allow_html=True)
