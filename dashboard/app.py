"""
Streamlit Dashboard — Smart Agriculture System
Run: streamlit run dashboard/app.py
Connects to Flask API on localhost:5000
Falls back to direct simulation if API is offline.
"""
import sys, os, time, math, random
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# ── Page config ──────────────────────────────────────────────
st.set_page_config(
    page_title="Smart Agriculture System",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded",
)

API_BASE = "http://localhost:5000"

# ── Helpers ──────────────────────────────────────────────────
def api_get(path):
    try:
        import requests
        r = requests.get(f"{API_BASE}{path}", timeout=2)
        return r.json()
    except Exception:
        return None

def api_post(path, payload):
    try:
        import requests
        r = requests.post(f"{API_BASE}{path}", json=payload, timeout=2)
        return r.json()
    except Exception:
        return None

# Fallback simulated readings when API is offline
_sim_moisture = {"A": 55.0, "B": 42.0, "C": 68.0, "D": 28.0}

def simulated_readings():
    readings = []
    for zone in ["A", "B", "C", "D"]:
        _sim_moisture[zone] = max(10, _sim_moisture[zone] - random.uniform(0.1, 0.4))
        if _sim_moisture[zone] < 15:
            _sim_moisture[zone] = random.uniform(55, 70)
        h = (time.time() / 3600) % 24
        readings.append({
            "zone":     zone,
            "temp":     round(22 + 8 * math.sin(math.pi * h / 12) + random.gauss(0, 0.5), 2),
            "humidity": round(65 + random.gauss(0, 3), 2),
            "moisture": round(_sim_moisture[zone], 2),
            "N": round(random.uniform(60, 120), 1),
            "P": round(random.uniform(30, 80),  1),
            "K": round(random.uniform(20, 60),  1),
            "ph": round(random.uniform(5.5, 7.5), 2),
        })
    return readings

def get_readings():
    data = api_get("/sensors/latest")
    return data if data else simulated_readings()

# ── Sidebar ──────────────────────────────────────────────────
with st.sidebar:
    st.image("https://img.icons8.com/color/96/wheat.png", width=80)
    st.title("🌾 Smart Agriculture")
    st.caption("BCA Major Project | 2024-25")
    st.divider()

    st.subheader("🔮 Crop Recommendation")
    N_val   = st.slider("Nitrogen (N)",    0,   140, 80)
    P_val   = st.slider("Phosphorus (P)",  5,   145, 42)
    K_val   = st.slider("Potassium (K)",   5,   205, 43)
    temp_v  = st.slider("Temperature °C",  8,   44,  21)
    hum_v   = st.slider("Humidity %",      14,  100, 82)
    ph_v    = st.slider("pH",              3.5, 9.5, 6.5)
    rain_v  = st.slider("Rainfall mm",     20,  300, 200)

    if st.button("🌱 Predict Crop", use_container_width=True):
        payload = {"N": N_val, "P": P_val, "K": K_val,
                   "temperature": temp_v, "humidity": hum_v,
                   "ph": ph_v, "rainfall": rain_v}
        result = api_post("/predict/crop", payload)
        if result and "crop" in result:
            st.success(f"**{result['crop'].upper()}**")
            st.metric("Confidence", f"{result['confidence']*100:.1f}%")
        else:
            # Fallback demo
            crops = ["Rice","Maize","Wheat","Cotton","Chickpea","Mango","Banana"]
            st.success(f"**{random.choice(crops).upper()}** (demo mode)")

    st.divider()
    st.subheader("🚜 Zone Route Planner")
    src_z = st.selectbox("From", ["ZoneA","ZoneB","ZoneC","ZoneD"])
    dst_z = st.selectbox("To",   ["ZoneD","ZoneA","ZoneB","ZoneC"])
    if st.button("📍 Find Shortest Route", use_container_width=True):
        result = api_get(f"/route/{src_z}/{dst_z}")
        if result and "path" in result:
            st.info(f"**{' → '.join(result['path'])}**\n\n{result['distance_m']}m")
        else:
            routes = {"ZoneA-ZoneD": ("ZoneA → ZoneB → ZoneD", 350),
                      "ZoneA-ZoneC": ("ZoneA → ZoneC", 300),
                      "ZoneB-ZoneC": ("ZoneB → ZoneA → ZoneC", 450)}
            key = f"{src_z}-{dst_z}"
            r   = routes.get(key, (f"{src_z} → {dst_z}", 200))
            st.info(f"**{r[0]}**\n\n{r[1]}m")

# ── Main dashboard ───────────────────────────────────────────
st.title("🌾 Smart Agriculture System Dashboard")
st.caption("Real-time IoT sensor monitoring · ML predictions · AADS task scheduling")

readings = get_readings()
df_r     = pd.DataFrame(readings)

# ── KPI row ──────────────────────────────────────────────────
cols = st.columns(4)
zone_labels = ["Zone A", "Zone B", "Zone C", "Zone D"]
for i, (col, row) in enumerate(zip(cols, readings)):
    mois  = row["moisture"]
    delta = "🚨 LOW" if mois < 30 else ("✅ OK" if mois >= 50 else "⚠️ MED")
    col.metric(f"💧 {zone_labels[i]} Moisture", f"{mois}%", delta)

st.divider()

# ── Sensor charts ────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.subheader("🌡️ Temperature & Humidity by Zone")
    fig = go.Figure()
    fig.add_bar(name="Temperature °C", x=df_r["zone"],
                y=df_r["temp"], marker_color="#FF6B35")
    fig.add_bar(name="Humidity %",     x=df_r["zone"],
                y=df_r["humidity"], marker_color="#4ECDC4")
    fig.update_layout(barmode="group", height=300,
                      plot_bgcolor="#0e1117", paper_bgcolor="#0e1117",
                      font_color="white", margin=dict(t=20, b=20))
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("🌱 Soil Moisture by Zone")
    colors = ["#e74c3c" if v < 30 else "#f39c12" if v < 50 else "#2ecc71"
              for v in df_r["moisture"]]
    fig2 = go.Figure(go.Bar(x=df_r["zone"], y=df_r["moisture"],
                             marker_color=colors, text=df_r["moisture"],
                             textposition="outside"))
    fig2.add_hline(y=30, line_dash="dash", line_color="red",
                   annotation_text="Irrigation threshold (30%)")
    fig2.update_layout(height=300, plot_bgcolor="#0e1117",
                       paper_bgcolor="#0e1117", font_color="white",
                       margin=dict(t=20, b=20))
    st.plotly_chart(fig2, use_container_width=True)

# ── NPK chart ────────────────────────────────────────────────
st.subheader("🧪 NPK Nutrient Levels by Zone")
fig3 = go.Figure()
for nutrient, color in [("N","#3498db"),("P","#e67e22"),("K","#9b59b6")]:
    fig3.add_bar(name=nutrient, x=df_r["zone"], y=df_r[nutrient],
                 marker_color=color)
fig3.update_layout(barmode="group", height=280, plot_bgcolor="#0e1117",
                   paper_bgcolor="#0e1117", font_color="white",
                   margin=dict(t=20, b=20))
st.plotly_chart(fig3, use_container_width=True)

# ── Moisture time-series simulation ──────────────────────────
st.subheader("📈 Soil Moisture Trend (Last 24 Hours — Simulated)")
hours = list(range(24))
fig4  = go.Figure()
np.random.seed(int(time.time()) % 100)
for zone, color in zip(["A","B","C","D"],["#2ecc71","#3498db","#e67e22","#e74c3c"]):
    base = random.uniform(30, 70)
    vals = [max(10, base - i*0.8 + random.gauss(0, 2)) for i in hours]
    fig4.add_scatter(x=hours, y=vals, name=f"Zone {zone}",
                     line=dict(color=color, width=2))
fig4.add_hline(y=30, line_dash="dash", line_color="red",
               annotation_text="Irrigation threshold")
fig4.update_layout(height=300, xaxis_title="Hour",
                   yaxis_title="Moisture %",
                   plot_bgcolor="#0e1117", paper_bgcolor="#0e1117",
                   font_color="white", margin=dict(t=20, b=20))
st.plotly_chart(fig4, use_container_width=True)

# ── Task queue ───────────────────────────────────────────────
st.subheader("📋 AADS Task Queue (Max-Heap Priority)")
tasks = api_get("/tasks")
if tasks:
    df_t = pd.DataFrame(tasks)
    df_t["priority"] = df_t["score"].apply(
        lambda s: "🔴 HIGH" if s > 0.02 else "🟡 MED" if s > 0.01 else "🟢 LOW")
    st.dataframe(df_t[["task_id","type","zone","moisture","score","priority"]],
                 use_container_width=True, hide_index=True)
else:
    demo_tasks = pd.DataFrame([
        {"task_id":1,"type":"Irrigation",  "zone":"ZoneA","moisture":18,"score":0.0278,"priority":"🔴 HIGH"},
        {"task_id":4,"type":"Irrigation",  "zone":"ZoneD","moisture":22,"score":0.0227,"priority":"🔴 HIGH"},
        {"task_id":3,"type":"Pest Control","zone":"ZoneC","moisture":60,"score":0.0083,"priority":"🟡 MED"},
        {"task_id":2,"type":"Fertilize",   "zone":"ZoneB","moisture":45,"score":0.0044,"priority":"🟢 LOW"},
    ])
    st.dataframe(demo_tasks, use_container_width=True, hide_index=True)

# ── Alerts ───────────────────────────────────────────────────
st.subheader("🚨 Active Alerts")
for row in readings:
    if row["moisture"] < 30:
        st.error(f"Zone {row['zone']}: Soil moisture critically low ({row['moisture']}%) — Irrigation triggered")
    elif row["moisture"] < 40:
        st.warning(f"Zone {row['zone']}: Soil moisture low ({row['moisture']}%) — Monitor closely")

# ── Footer ───────────────────────────────────────────────────
st.divider()
col_l, col_r = st.columns([3,1])
col_l.caption("Smart Agriculture System · BCA Major Project 2024-25 · AADS + FML + IoT")
if col_r.button("🔄 Refresh Data"):
    st.rerun()
