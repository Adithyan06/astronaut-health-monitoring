import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, date, time, timedelta
import json, os

st.set_page_config(page_title="ORBIT | Astronaut Health", page_icon="🛰️", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Manrope:wght@400;500;600;700;800&display=swap');
html, body, [class*="css"] {font-family:'Manrope',sans-serif;}
.stApp {background:linear-gradient(135deg,#07111f 0%,#0a1828 55%,#101e31 100%); color:#eaf2ff;}
.block-container {padding-top:1.5rem; max-width:1450px;}
[data-testid="stMetric"] {background:#10243a;border:1px solid #25415d;padding:16px;border-radius:14px;}
[data-testid="stMetricLabel"] {color:#9bb3cb;}
[data-testid="stMetricValue"] {color:#f2f7ff;}
div[data-testid="stTabs"] button {color:#a9bfd5;}
.orbit-card {background:#10243a;border:1px solid #25415d;border-radius:16px;padding:18px 20px;margin:8px 0;}
.muted {color:#9bb3cb;font-size:0.88rem;}
.kicker {font-family:'DM Mono',monospace;color:#62d9c2;letter-spacing:2px;font-size:0.75rem;}
.big {font-size:2rem;font-weight:800;color:#f2f7ff;}
.good {color:#55d6a7;font-weight:700}.warn {color:#ffc56d;font-weight:700}.bad {color:#ff7f88;font-weight:700}
div.stButton > button {border-radius:10px;border:1px solid #3b6988;background:#15334d;color:#f2f7ff;font-weight:700;}
div.stButton > button:hover {border-color:#62d9c2;color:#62d9c2;}
</style>
""", unsafe_allow_html=True)

if "logs" not in st.session_state:
    st.session_state.logs = [
        {"date": (date.today()-timedelta(days=6)).isoformat(),"hr":62,"sleep":7.4,"spo2":98,"temp":36.7,"fatigue":2,"mood":4,"pain":0,"exercise":35},
        {"date": (date.today()-timedelta(days=5)).isoformat(),"hr":64,"sleep":7.0,"spo2":98,"temp":36.6,"fatigue":2,"mood":4,"pain":0,"exercise":30},
        {"date": (date.today()-timedelta(days=4)).isoformat(),"hr":66,"sleep":6.8,"spo2":97,"temp":36.8,"fatigue":3,"mood":3,"pain":1,"exercise":25},
        {"date": (date.today()-timedelta(days=3)).isoformat(),"hr":65,"sleep":7.2,"spo2":98,"temp":36.7,"fatigue":2,"mood":4,"pain":0,"exercise":40},
        {"date": (date.today()-timedelta(days=2)).isoformat(),"hr":68,"sleep":6.5,"spo2":97,"temp":36.9,"fatigue":3,"mood":3,"pain":1,"exercise":20},
        {"date": (date.today()-timedelta(days=1)).isoformat(),"hr":67,"sleep":7.1,"spo2":98,"temp":36.8,"fatigue":2,"mood":4,"pain":0,"exercise":35},
        {"date": date.today().isoformat(),"hr":66,"sleep":7.3,"spo2":98,"temp":36.7,"fatigue":2,"mood":4,"pain":0,"exercise":30},
    ]

st.sidebar.markdown('<div class="kicker">MISSION CONTROL / CREW HEALTH</div>', unsafe_allow_html=True)
st.sidebar.title("🛰️ ORBIT")
st.sidebar.caption("Operational Readiness & Bio-telemetry")
crew = st.sidebar.text_input("Crew member", "Commander A. Morgan")
mission_day = st.sidebar.number_input("Mission day", min_value=1, value=126, step=1)
st.sidebar.markdown("---")
page = st.sidebar.radio("Navigation", ["Mission overview","Daily check-in","Health trends","Guidance & response","About ORBIT"])
st.sidebar.markdown("---")
st.sidebar.caption("PROTOTYPE • SIMULATED DATA • NOT A MEDICAL DEVICE")

df = pd.DataFrame(st.session_state.logs).sort_values("date")
latest = df.iloc[-1]

def status_for(v, low, high, critical_low=None, critical_high=None):
    if (critical_low is not None and v < critical_low) or (critical_high is not None and v > critical_high):
        return "RED", "bad"
    if v < low or v > high: return "AMBER", "warn"
    return "NOMINAL", "good"

def risk_summary(row):
    flags=[]
    if row["spo2"] < 94: flags.append(("Oxygen saturation", "Below 94% in this demo rule. Recheck sensor fit and follow medical protocol.", "RED"))
    elif row["spo2"] < 96: flags.append(("Oxygen saturation", "Below the demo nominal band. Recheck and trend.", "AMBER"))
    if row["hr"] < 50 or row["hr"] > 100: flags.append(("Resting heart rate", "Outside the demo screening band; assess symptoms and repeat measurement.", "AMBER"))
    if row["sleep"] < 6: flags.append(("Sleep duration", "Less than 6 hours; consider sleep opportunity and workload.", "AMBER"))
    if row["fatigue"] >= 4: flags.append(("Fatigue", "High self-reported fatigue; consider workload adjustment and crew check-in.", "AMBER"))
    if row["mood"] <= 2: flags.append(("Behavioral wellbeing", "Low mood score; consider confidential peer/behavioral-health support.", "AMBER"))
    if row["pain"] >= 4: flags.append(("Pain", "High pain score; report to medical officer according to mission protocol.", "RED"))
    return flags

flags = risk_summary(latest)
red = sum(1 for x in flags if x[2]=="RED")
amber = sum(1 for x in flags if x[2]=="AMBER")
overall = "ACTION REQUIRED" if red else ("ATTENTION" if amber else "NOMINAL")
overall_color = "#ff7f88" if red else ("#ffc56d" if amber else "#55d6a7")

st.markdown('<div class="kicker">LONG-DURATION SPACEFLIGHT / CREW SELF-MONITORING</div>', unsafe_allow_html=True)
st.title("ORBIT Health Monitor")
st.markdown(f'<div class="muted">{crew} &nbsp;•&nbsp; Mission day {mission_day} &nbsp;•&nbsp; Last sync: {datetime.now().strftime("%d %b %Y, %H:%M")}</div>', unsafe_allow_html=True)

if page == "Mission overview":
    st.markdown(f'<div class="orbit-card"><div class="kicker">CREW HEALTH STATUS</div><div class="big" style="color:{overall_color}">{overall}</div><div class="muted">Based on the latest entered indicators and transparent prototype screening rules. Not a diagnosis.</div></div>', unsafe_allow_html=True)
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Resting HR", f'{int(latest.hr)} bpm', "Latest check")
    c2.metric("SpO₂", f'{int(latest.spo2)} %', "Oxygen saturation")
    c3.metric("Sleep", f'{latest.sleep:.1f} h', "Last sleep period")
    c4.metric("Fatigue", f'{int(latest.fatigue)}/5', "Self-report")
    st.subheader("System watch")
    cards = [
        ("CARDIOVASCULAR", "Resting heart rate", f'{int(latest.hr)} bpm', status_for(latest.hr,50,100)[0], "Trend resting pulse alongside symptoms and workload."),
        ("OXYGENATION", "SpO₂", f'{int(latest.spo2)}%', status_for(latest.spo2,96,100,90, None)[0], "Check sensor placement; compare repeated readings."),
        ("SLEEP & RECOVERY", "Sleep duration", f'{latest.sleep:.1f} h', "AMBER" if latest.sleep<6 else "NOMINAL", "Protect sleep opportunity and note persistent disruption."),
        ("BEHAVIORAL HEALTH", "Mood / fatigue", f'{int(latest.mood)}/5 mood • {int(latest.fatigue)}/5 fatigue', "AMBER" if latest.mood<=2 or latest.fatigue>=4 else "NOMINAL", "Use private check-ins and request support early."),
    ]
    cols=st.columns(2)
    for i,(category,name,val,status,desc) in enumerate(cards):
        with cols[i%2]:
            color="#55d6a7" if status=="NOMINAL" else "#ffc56d"
            st.markdown(f'<div class="orbit-card"><div class="kicker">{category}</div><b>{name}</b><div class="big">{val}</div><span style="color:{color};font-weight:800">{status}</span><p class="muted">{desc}</p></div>',unsafe_allow_html=True)
    st.subheader("Attention items")
    if not flags: st.success("No prototype screening flags from the latest entry. Continue routine monitoring.")
    for title,desc,level in flags:
        (st.error if level=="RED" else st.warning)(f"**{level} · {title}** — {desc}")
    st.caption("Thresholds shown are illustrative software-demo rules only. Mission medical protocols and clinician judgement always take precedence.")

elif page == "Daily check-in":
    st.subheader("Crew daily health check-in")
    st.write("Enter current measurements and how you feel. Values are saved in this browser session.")
    with st.form("checkin"):
        a,b,c = st.columns(3)
        hr=a.number_input("Resting heart rate (bpm)",30,180,int(latest.hr))
        spo2=b.number_input("SpO₂ (%)",70,100,int(latest.spo2))
        sleep=c.number_input("Sleep (hours)",0.0,16.0,float(latest.sleep),0.1)
        d,e,f=st.columns(3)
        temp=d.number_input("Body temperature (°C)",34.0,42.0,float(latest.temp),0.1)
        fatigue=e.slider("Fatigue (1 = low, 5 = severe)",1,5,int(latest.fatigue))
        mood=f.slider("Mood (1 = very low, 5 = good)",1,5,int(latest.mood))
        g,h=st.columns(2)
        pain=g.slider("Pain (0 = none, 10 = severe)",0,10,int(latest.pain))
        exercise=h.number_input("Exercise / countermeasure (minutes)",0,240,int(latest.exercise))
        notes=st.text_area("Symptoms / notes (optional)",placeholder="e.g. headache, dizziness, unusual breathlessness, sleep disruption…")
        submitted=st.form_submit_button("Save daily check-in",use_container_width=True)
    if submitted:
        entry={"date":date.today().isoformat(),"hr":hr,"sleep":sleep,"spo2":spo2,"temp":temp,"fatigue":fatigue,"mood":mood,"pain":pain,"exercise":exercise,"notes":notes}
        if st.session_state.logs and st.session_state.logs[-1]["date"]==entry["date"]:
            st.session_state.logs[-1]=entry
        else: st.session_state.logs.append(entry)
        st.success("Check-in saved for this session. Open Mission overview to review flags.")
        st.rerun()
    st.info("If you experience chest pain, severe shortness of breath, fainting, confusion, or another emergency symptom, do not rely on this app—activate the mission medical/emergency protocol immediately.")

elif page == "Health trends":
    st.subheader("Personal health timeline")
    st.caption("Demo data is preloaded to make the prototype explorable. Submit a check-in to add today's values.")
    metric=st.selectbox("Choose indicator",["Resting heart rate (bpm)","SpO₂ (%)","Sleep (hours)","Fatigue (1–5)","Mood (1–5)","Pain (0–10)","Exercise (minutes)"])
    mapping={"Resting heart rate (bpm)":"hr","SpO₂ (%)":"spo2","Sleep (hours)":"sleep","Fatigue (1–5)":"fatigue","Mood (1–5)":"mood","Pain (0–10)":"pain","Exercise (minutes)":"exercise"}
    key=mapping[metric]
    chart=df.set_index("date")[[key]]
    st.line_chart(chart, use_container_width=True)
    st.subheader("Recent entries")
    st.dataframe(df.tail(14).rename(columns={"hr":"HR bpm","spo2":"SpO₂ %","sleep":"Sleep h","temp":"Temp °C","fatigue":"Fatigue","mood":"Mood","pain":"Pain","exercise":"Exercise min"}),use_container_width=True,hide_index=True)
    st.download_button("Export health log (CSV)",df.to_csv(index=False).encode("utf-8"),"orbit_health_log.csv","text/csv")

elif page == "Guidance & response":
    st.subheader("What should I do next?")
    st.markdown("Use this as a **decision-support checklist**, not as a substitute for flight medical direction.")
    if red:
        st.error("One or more RED prototype flags are present. Recheck the measurement if safe, document symptoms, and contact the flight surgeon / medical officer immediately under mission protocol.")
    elif amber:
        st.warning("One or more AMBER flags are present. Repeat questionable measurements, review recent workload/sleep/hydration, and discuss persistent or worsening changes with the medical officer.")
    else:
        st.success("No current demo flags. Maintain routine measurements, countermeasures, and scheduled crew-health communication.")
    st.markdown("#### Symptom-led escalation")
    st.markdown("""
    - **Emergency symptoms:** chest pain, severe breathlessness, fainting, new neurological symptoms, severe confusion, or rapidly worsening condition → activate mission emergency protocol immediately.
    - **Persistent change:** repeated abnormal readings, new pain, sustained sleep disruption, or worsening mood → record the pattern and contact the medical officer.
    - **Daily prevention:** follow prescribed exercise/resistance countermeasures, sleep schedule, nutrition/hydration plan, and radiation-safety instructions.
    """)
    st.markdown("#### Mission health domains")
    with st.expander("Radiation exposure"):
        st.write("Integrate dosimeter / mission radiation alerts when available. ORBIT does not estimate radiation dose from symptoms. Follow shelter and operational guidance from mission control.")
    with st.expander("Bone and muscle health"):
        st.write("Track prescribed resistance and aerobic countermeasures, exercise completion, discomfort, and any mission-approved bone-health measurements.")
    with st.expander("Cardiovascular health"):
        st.write("Trend resting heart rate, blood pressure if available, symptoms, and exercise tolerance. Interpret changes against the crew member's baseline.")
    with st.expander("Behavioral health and isolation"):
        st.write("Offer private mood, stress, sleep, and social-connection check-ins. A low score is a prompt to seek support—not a diagnosis.")
    with st.expander("Sensor and data quality"):
        st.write("Repeat unexpected readings, confirm sensor contact and calibration, record timestamps, and mark missing or suspect data rather than silently treating it as normal.")

elif page == "About ORBIT":
    st.subheader("Operational Readiness & Bio-telemetry")
    st.write("ORBIT is a hackathon prototype concept for astronaut-led health awareness during long-duration missions.")
    st.markdown("""
    **Prototype capabilities**
    - Unified daily check-in for physiological and behavioral indicators
    - At-a-glance status with transparent rule-based flags
    - Personal trend visualization and CSV export
    - Action-oriented escalation guidance and mission-health education
    - Local session demo data; no external medical-device integration

    **Next engineering steps**
    1. Connect validated wearable / medical-device data streams with timestamps and quality metadata.
    2. Establish individualized baselines and clinician-approved thresholds for each crew member.
    3. Add secure authentication, encryption, role-based access, audit logs, and offline-first sync.
    4. Integrate radiation dosimetry, exercise countermeasure records, and approved clinical workflows.
    5. Validate usability, false-alert rates, and clinical safety with qualified aerospace medical teams.
    """)
    st.warning("Safety notice: ORBIT is not an FDA/medical-certified device, does not diagnose or predict disease, and uses simulated demo data plus illustrative thresholds. Never use it for real astronaut care or to override NASA flight rules or medical personnel.")
    st.markdown("**Privacy:** This starter prototype stores check-ins only in the active Streamlit session. It is not designed for real personal health information.")

st.markdown("---")
st.markdown('<div class="muted">ORBIT • Crew-centered health awareness • Prototype build 0.1 • Simulated data</div>',unsafe_allow_html=True)
