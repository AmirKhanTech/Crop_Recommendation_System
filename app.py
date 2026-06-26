import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from joblib import load
from ai import get_ai_response
from voice import get_audio_html

# ══════════════════════════════════════════════════════════════
#  PAGE CONFIG
# ══════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="SmartFarm — AI Agro Intelligence",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════════
#  GLOBAL CSS — DESIGN SYSTEM
# ══════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:ital,wght@0,400;0,500;1,400&display=swap');

/* ─── TOKENS ──────────────────────────────────────────────── */
:root {
  --ink:        #080c0a;
  --s1:         #0c1410;
  --s2:         #101a14;
  --s3:         #152019;
  --s4:         #1b2921;

  --leaf:       #2dba5f;
  --leaf-d:     #1a9147;
  --leaf-glow:  rgba(45,186,95,.18);
  --leaf-edge:  rgba(45,186,95,.30);
  --gold:       #e8a93a;
  --gold-glow:  rgba(232,169,58,.15);
  --sky:        #3ab0e8;
  --sky-glow:   rgba(58,176,232,.14);
  --coral:      #e86060;
  --violet:     #9b7be8;
  --violet-glow:rgba(155,123,232,.14);
  --rose:       #e8607a;

  --t1: #edf5f0;
  --t2: rgba(237,245,240,.65);
  --t3: rgba(237,245,240,.35);
  --t4: rgba(237,245,240,.18);

  --b1: rgba(255,255,255,.055);
  --b2: rgba(255,255,255,.11);
  --b3: rgba(255,255,255,.20);

  --font-d: 'Syne', sans-serif;
  --font-b: 'Space Grotesk', sans-serif;
  --font-m: 'JetBrains Mono', monospace;

  --r-xs: 6px;  --r-sm: 10px;  --r-md: 16px;
  --r-lg: 22px; --r-xl: 32px;  --r-2xl: 44px;
}

/* ─── RESET ───────────────────────────────────────────────── */
*, *::before, *::after { box-sizing: border-box; }
* { font-family: var(--font-b) !important; }

#MainMenu, [data-testid="stToolbar"],
[data-testid="stDecoration"] { visibility: hidden !important; display: none !important; }

/* ─── BACKGROUND ──────────────────────────────────────────── */
[data-testid="stAppViewContainer"] {
  background: var(--ink) !important;
  background-image:
    radial-gradient(ellipse 80% 60% at 10% -5%,  rgba(45,186,95,.07)  0%, transparent 60%),
    radial-gradient(ellipse 60% 50% at 90% 110%, rgba(58,176,232,.05) 0%, transparent 55%),
    radial-gradient(ellipse 40% 40% at 55% 55%,  rgba(232,169,58,.03) 0%, transparent 65%),
    url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='80' height='80'%3E%3Ccircle cx='1' cy='1' r='.6' fill='rgba(255,255,255,0.025)'/%3E%3C/svg%3E") !important;
  min-height: 100vh !important;
}

/* ─── SIDEBAR ─────────────────────────────────────────────── */
[data-testid="stSidebar"] {
  background: var(--s1) !important;
  border-right: 1px solid var(--b1) !important;
  position: relative !important;
}
[data-testid="stSidebar"]::before {
  content: '';
  position: absolute; top: 0; left: 0; right: 0; height: 2px;
  background: linear-gradient(90deg, transparent, var(--leaf), var(--gold), transparent);
  z-index: 10;
}
[data-testid="stSidebarNav"] { display: none !important; }

/* ─── HEADER ──────────────────────────────────────────────── */
[data-testid="stHeader"] {
  background: rgba(8,12,10,.90) !important;
  backdrop-filter: blur(24px) !important;
  border-bottom: 1px solid var(--b1) !important;
}

/* ─── SCROLLBAR ───────────────────────────────────────────── */
::-webkit-scrollbar { width: 3px; height: 3px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--b2); border-radius: 2px; }
::-webkit-scrollbar-thumb:hover { background: var(--b3); }

/* ══════════════════════════════════════════════════════════
   SIDEBAR COMPONENTS
══════════════════════════════════════════════════════════ */
.sf-logo {
  padding: 28px 24px 20px;
  border-bottom: 1px solid var(--b1);
  margin-bottom: 20px;
}
.sf-logo-inner {
  display: flex; align-items: center; gap: 14px;
}
.sf-logo-ico {
  width: 46px; height: 46px; border-radius: 14px; flex-shrink: 0;
  background: linear-gradient(135deg, var(--leaf-d), var(--leaf));
  display: flex; align-items: center; justify-content: center;
  font-size: 22px;
  box-shadow: 0 6px 20px rgba(45,186,95,.35), 0 0 0 1px rgba(45,186,95,.2);
}
.sf-logo-name {
  font-family: var(--font-d) !important;
  font-size: 1.15rem; font-weight: 800; color: var(--t1);
  letter-spacing: -.3px;
}
.sf-logo-sub {
  font-size: .62rem; color: var(--t4); letter-spacing: 2.5px;
  text-transform: uppercase; margin-top: 2px;
}

/* NAV */
.sf-nav-section {
  padding: 0 16px;
  font-size: .60rem; letter-spacing: 2.5px; text-transform: uppercase;
  color: var(--t4); font-weight: 700; margin: 16px 0 8px;
}
.sf-nav-item {
  display: flex; align-items: center; gap: 10px;
  padding: 10px 14px; border-radius: var(--r-sm);
  font-size: .84rem; font-weight: 500; color: var(--t2);
  cursor: default; transition: all .2s; margin: 2px 0;
  border: 1px solid transparent;
}
.sf-nav-item:hover { background: var(--b1); color: var(--t1); }
.sf-nav-item.active {
  background: var(--leaf-glow);
  border-color: var(--leaf-edge);
  color: var(--leaf);
            

}
.sf-nav-badge {
  margin-left: auto; background: var(--leaf); color: white;
  font-size: .58rem; font-weight: 700; letter-spacing: 1px;
  text-transform: uppercase; padding: 2px 7px; border-radius: 20px;
}

/* STATUS CARD */
.sf-status {
  margin: 24px 16px 20px;
  background: rgba(45,186,95,.05);
  border: 1px solid rgba(45,186,95,.15);
  border-radius: var(--r-md); padding: 16px;
}
.sf-status-head {
  font-size: .62rem; letter-spacing: 2.5px; text-transform: uppercase;
  color: rgba(45,186,95,.65); font-weight: 700; margin-bottom: 12px;
}
.sf-status-row {
  display: flex; align-items: center; gap: 9px;
  font-size: .78rem; color: var(--t2); margin: 6px 0;
}
.sf-dot {
  width: 6px; height: 6px; border-radius: 50%; background: var(--leaf);
  box-shadow: 0 0 8px var(--leaf); flex-shrink: 0;
  animation: pulse-dot 2s ease-in-out infinite;
}
.sf-dot.d2 { animation-delay: .5s; }
.sf-dot.d3 { animation-delay: 1s; }
@keyframes pulse-dot {
  0%, 100% { opacity: 1; transform: scale(1); }
  50%       { opacity: .35; transform: scale(.7); }
}

/* ══════════════════════════════════════════════════════════
   HERO HEADER
══════════════════════════════════════════════════════════ */
.sf-hero {
  text-align: center; padding: 48px 20px 32px;
  position: relative; overflow: hidden;
}
.sf-hero::before {
  content: '';
  position: absolute; top: 0; left: 50%; transform: translateX(-50%);
  width: 600px; height: 1px;
  background: linear-gradient(90deg, transparent, var(--leaf), var(--gold), var(--sky), transparent);
}
.sf-eyebrow {
  display: inline-flex; align-items: center; gap: 8px;
  background: var(--leaf-glow); border: 1px solid var(--leaf-edge);
  border-radius: 100px; padding: 6px 18px;
  font-size: .65rem; font-weight: 700; letter-spacing: 2.5px;
  text-transform: uppercase; color: var(--leaf); margin-bottom: 18px;
  animation: fade-down .6s ease both;
}
@keyframes fade-down {
  from { opacity: 0; transform: translateY(-14px); }
  to   { opacity: 1; transform: translateY(0); }
}
.sf-title {
  font-family: var(--font-d) !important;
  font-size: clamp(2rem, 4.5vw, 3.8rem) !important;
  font-weight: 800 !important; color: var(--t1) !important;
  letter-spacing: -2px !important; line-height: 1.1 !important;
  margin: 0 !important; text-align: center !important;
  animation: fade-up .7s ease .1s both;
}
.sf-title em {
  font-style: normal;
  background: linear-gradient(90deg, var(--leaf) 0%, var(--gold) 50%, var(--sky) 100%);
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.sf-sub {
  font-size: .92rem !important; color: var(--t3) !important;
  margin-top: 14px !important; font-weight: 400 !important;
  text-align: center !important; letter-spacing: .2px !important;
  animation: fade-up .7s ease .2s both;
}
@keyframes fade-up {
  from { opacity: 0; transform: translateY(18px); }
  to   { opacity: 1; transform: translateY(0); }
}

/* ══════════════════════════════════════════════════════════
   STAT CARDS
══════════════════════════════════════════════════════════ */
.sf-stats {
  display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px;
  margin-bottom: 8px; animation: fade-up .6s ease .2s both;
}
.sf-stat {
  background: var(--s2); border: 1px solid var(--b1);
  border-radius: var(--r-lg); padding: 22px 22px 18px;
  position: relative; overflow: hidden;
  transition: transform .25s, border-color .25s, box-shadow .25s;
}
.sf-stat:hover {
  transform: translateY(-4px); border-color: var(--b2);
  box-shadow: 0 16px 40px rgba(0,0,0,.45);
}
.sf-stat::before {
  content: ''; position: absolute; inset: 0;
  background: linear-gradient(135deg, rgba(255,255,255,.03) 0%, transparent 55%);
  pointer-events: none;
}
.sf-stat-accent {
  position: absolute; top: 0; left: 0; right: 0; height: 2px;
}
.sf-stat-icon { font-size: 1.3rem; margin-bottom: 12px; opacity: .7; }
.sf-stat-val {
  font-family: var(--font-d) !important;
  font-size: 2.2rem; font-weight: 800; line-height: 1;
  letter-spacing: -1.5px; margin-bottom: 6px;
}
.sf-stat-key {
  font-size: .62rem; font-weight: 700; letter-spacing: 2px;
  text-transform: uppercase; color: var(--t4);
}
.gv { background: linear-gradient(135deg, var(--leaf), var(--gold)); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.sv { background: linear-gradient(135deg, var(--sky), #6be8da); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.av { background: linear-gradient(135deg, var(--gold), #f0d060); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.vv { background: linear-gradient(135deg, var(--violet), #c4aaff); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }

/* ══════════════════════════════════════════════════════════
   SECTION LABEL
══════════════════════════════════════════════════════════ */
.sf-sec {
  display: flex; align-items: center; gap: 14px; margin: 36px 0 20px;
}
.sf-sec-line { flex: 1; height: 1px; }
.sf-sec-line.l { background: linear-gradient(90deg, transparent, var(--b2)); }
.sf-sec-line.r { background: linear-gradient(270deg, transparent, var(--b2)); }
.sf-sec-tag {
  font-size: .63rem; font-weight: 700; letter-spacing: 2.5px;
  text-transform: uppercase; color: var(--t4); white-space: nowrap;
}

/* ══════════════════════════════════════════════════════════
   MODEL INFO
══════════════════════════════════════════════════════════ */
.sf-model-wrap {
  background: var(--s2); border: 1px solid var(--b1);
  border-radius: var(--r-xl); padding: 32px;
  position: relative; overflow: hidden; margin-bottom: 12px;
}
.sf-model-wrap::after {
  content: ''; position: absolute; top: 0; left: 10%; right: 10%; height: 1px;
  background: linear-gradient(90deg, transparent, var(--leaf), var(--gold), transparent);
}
.sf-mini-stats {
  display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px;
  margin-bottom: 24px;
}
.sf-mini {
  background: rgba(255,255,255,.03); border: 1px solid var(--b1);
  border-radius: var(--r-md); padding: 16px; text-align: center;
}
.sf-mini-val {
  font-family: var(--font-d) !important;
  font-size: 1.8rem; font-weight: 800;
  background: linear-gradient(135deg, var(--leaf), var(--gold));
  -webkit-background-clip: text; -webkit-text-fill-color: transparent;
  letter-spacing: -1px; margin-bottom: 4px;
}
.sf-mini-key {
  font-size: .6rem; letter-spacing: 2px; text-transform: uppercase;
  color: var(--t4); font-weight: 600;
}
.sf-model-desc {
  font-size: .88rem; line-height: 1.9; color: var(--t2);
  background: rgba(255,255,255,.025); border: 1px solid var(--b1);
  border-radius: var(--r-md); padding: 18px 20px; margin-bottom: 20px;
}
.sf-crop-grid {
  display: flex; flex-wrap: wrap; gap: 8px; justify-content: center;
}
.sf-crop-tag {
  background: rgba(255,255,255,.035); border: 1px solid var(--b1);
  border-radius: 100px; padding: 5px 15px;
  font-size: .76rem; color: var(--t2);
  transition: all .18s; cursor: default;
}
.sf-crop-tag:hover {
  background: var(--leaf-glow); border-color: var(--leaf-edge);
  color: var(--leaf); transform: translateY(-2px);
}

/* ══════════════════════════════════════════════════════════
   INPUT CARDS
══════════════════════════════════════════════════════════ */
.sf-input-card {
  background: var(--s2); border: 1px solid var(--b1);
  border-radius: var(--r-md); padding: 14px 16px 10px;
  margin-bottom: 12px; position: relative;
  transition: border-color .2s, box-shadow .2s;
}
.sf-input-card:hover,
.sf-input-card:focus-within {
  box-shadow: 0 6px 24px rgba(0,0,0,.35);
}
.sf-input-card.g  { border-left: 3px solid var(--leaf); }
.sf-input-card.g:focus-within { border-color: var(--leaf-edge); box-shadow: 0 0 0 3px rgba(45,186,95,.06); }
.sf-input-card.s  { border-left: 3px solid var(--sky); }
.sf-input-card.s:focus-within { border-color: rgba(58,176,232,.4); box-shadow: 0 0 0 3px rgba(58,176,232,.06); }
.sf-input-card.a  { border-left: 3px solid var(--gold); }
.sf-input-card.a:focus-within { border-color: rgba(232,169,58,.4); box-shadow: 0 0 0 3px rgba(232,169,58,.06); }
.sf-input-card.v  { border-left: 3px solid var(--violet); }
.sf-input-card.v:focus-within { border-color: rgba(155,123,232,.4); box-shadow: 0 0 0 3px rgba(155,123,232,.06); }

/* ─── STREAMLIT NUMBER INPUT ──────────────────────────────── */
.stNumberInput label {
  color: var(--t3) !important; font-weight: 600 !important;
  font-size: .74rem !important; letter-spacing: .5px !important;
  text-transform: uppercase !important;
}
.stNumberInput > div > div {
  background: rgba(255,255,255,.04) !important;
  border: 1px solid var(--b1) !important;
  border-radius: var(--r-sm) !important;
  color: var(--t1) !important;
  font-family: var(--font-m) !important;
  transition: all .2s !important;
}
.stNumberInput > div > div:focus-within {
  border-color: rgba(45,186,95,.45) !important;
  box-shadow: 0 0 0 3px rgba(45,186,95,.08) !important;
}
.stNumberInput input {
  color: var(--t1) !important;
  font-family: var(--font-m) !important;
  font-size: 1.05rem !important;
}

/* ─── PREDICT BUTTON ──────────────────────────────────────── */
.stButton > button {
  background: linear-gradient(135deg, #0f5128 0%, var(--leaf-d) 50%, var(--leaf) 100%) !important;
  color: #fff !important; border: none !important;
  border-radius: var(--r-lg) !important;
  padding: 1rem 2.2rem !important;
  font-family: var(--font-d) !important;
  font-size: 1rem !important; font-weight: 700 !important;
  letter-spacing: .3px !important; width: 100% !important;
  transition: all .3s cubic-bezier(.16,1,.3,1) !important;
  box-shadow: 0 6px 28px rgba(45,186,95,.3), inset 0 1px 0 rgba(255,255,255,.12) !important;
  position: relative !important; overflow: hidden !important;
}
.stButton > button::after {
  content: '' !important; position: absolute !important; inset: 0 !important;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,.08), transparent) !important;
  transform: translateX(-100%) !important; transition: transform .55s !important;
}
.stButton > button:hover::after { transform: translateX(100%) !important; }
.stButton > button:hover {
  transform: translateY(-3px) !important;
  box-shadow: 0 14px 36px rgba(45,186,95,.45), inset 0 1px 0 rgba(255,255,255,.15) !important;
}
.stButton > button:active { transform: scale(.99) !important; }

/* ─── SIDEBAR BUTTON OVERRIDE ─────────────────────────────── */
[data-testid="stSidebar"] .stButton > button {
  background: rgba(255,255,255,.045) !important;
  border: 1px solid var(--b2) !important;
  color: var(--t2) !important; box-shadow: none !important;
  font-size: .82rem !important; padding: .6rem 1rem !important;
  border-radius: var(--r-sm) !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
  background: rgba(232,96,96,.1) !important;
  border-color: rgba(232,96,96,.3) !important;
  color: var(--coral) !important; transform: none !important;
}

/* ══════════════════════════════════════════════════════════
   RESULTS
══════════════════════════════════════════════════════════ */
.sf-result-hero {
  background: var(--s2);
  border: 1px solid rgba(45,186,95,.22);
  border-radius: var(--r-2xl); padding: 44px 32px;
  text-align: center; position: relative; overflow: hidden;
  box-shadow: 0 0 80px rgba(45,186,95,.07), 0 32px 60px rgba(0,0,0,.45);
  animation: pop-in .55s cubic-bezier(.34,1.56,.64,1) both;
}
@keyframes pop-in {
  from { opacity: 0; transform: scale(.88) translateY(24px); }
  to   { opacity: 1; transform: scale(1) translateY(0); }
}
.sf-result-hero::before {
  content: ''; position: absolute; inset: 0;
  background: radial-gradient(ellipse 70% 60% at 50% -5%, rgba(45,186,95,.12), transparent);
}
.sf-result-hero::after {
  content: ''; position: absolute; top: 0; left: 12%; right: 12%; height: 1px;
  background: linear-gradient(90deg, transparent, var(--leaf), var(--gold), transparent);
}
.sf-r-eyebrow {
  font-size: .63rem; letter-spacing: 3px; text-transform: uppercase;
  color: rgba(45,186,95,.6); font-weight: 700; margin-bottom: 16px;
  position: relative;
}
.sf-r-crop {
  font-family: var(--font-d) !important;
  font-size: 3.5rem !important; font-weight: 800 !important;
  letter-spacing: -2px !important; line-height: 1 !important;
  background: linear-gradient(135deg, var(--leaf) 0%, var(--gold) 55%, var(--sky) 100%);
  -webkit-background-clip: text !important; -webkit-text-fill-color: transparent !important;
  margin: 0 0 14px !important; position: relative;
}
.sf-r-conf {
  font-family: var(--font-m) !important;
  font-size: .82rem; color: var(--t3); position: relative;
}
.sf-r-conf span { color: var(--leaf); font-size: 1.05rem; font-weight: 600; }

/* ─── RANK ITEMS ──────────────────────────────────────────── */
.sf-rank {
  display: flex; align-items: center; gap: 16px;
  padding: 14px 20px; border-radius: var(--r-md);
  border: 1px solid transparent; margin: 8px 0;
  transition: all .22s;
}
.sf-rank:hover { transform: translateX(7px); border-color: var(--b2); }
.sf-rank-num { font-size: 1rem; min-width: 26px; text-align: center; }
.sf-rank-name { flex: 1; font-weight: 600; font-size: .95rem; }
.sf-rank-bar-bg {
  width: 120px; height: 4px;
  background: rgba(255,255,255,.06); border-radius: 2px; overflow: hidden;
}
.sf-rank-bar { height: 100%; border-radius: 2px; transition: width .9s cubic-bezier(.16,1,.3,1); }
.sf-rank-pct {
  font-family: var(--font-m) !important;
  font-size: .82rem; min-width: 48px; text-align: right;
}

/* ─── AI CARD ─────────────────────────────────────────────── */
.sf-ai-wrap {
  background: var(--s2); border: 1px solid var(--b1);
  border-left: 3px solid var(--leaf); border-radius: var(--r-md);
  padding: 24px 28px; position: relative; overflow: hidden;
}
.sf-ai-quote {
  position: absolute; top: 4px; left: 16px;
  font-family: var(--font-d) !important; font-size: 6rem;
  color: rgba(45,186,95,.08); line-height: 1; pointer-events: none;
  user-select: none;
}
.sf-ai-header {
  display: flex; align-items: center; gap: 10px; margin-bottom: 16px;
  position: relative;
}
.sf-ai-badge {
  background: var(--leaf-glow); border: 1px solid var(--leaf-edge);
  color: var(--leaf); font-size: .62rem; font-weight: 700;
  letter-spacing: 1.5px; text-transform: uppercase;
  padding: 4px 10px; border-radius: 20px;
}
.sf-ai-ts {
  font-family: var(--font-m) !important;
  font-size: .7rem; color: var(--t4);
}
.sf-ai-body {
  font-size: .9rem; line-height: 1.9; color: var(--t2); position: relative;
}

/* ─── VOICE SECTION ───────────────────────────────────────── */
.sf-voice-wrap {
  background: var(--s2); border: 1px solid var(--b1);
  border-left: 3px solid var(--sky); border-radius: var(--r-md);
  padding: 20px 24px;
}
.sf-voice-head {
  display: flex; align-items: center; gap: 10px; margin-bottom: 14px;
}
.sf-voice-badge {
  background: var(--sky-glow); border: 1px solid rgba(58,176,232,.25);
  color: var(--sky); font-size: .62rem; font-weight: 700;
  letter-spacing: 1.5px; text-transform: uppercase; padding: 4px 10px; border-radius: 20px;
}

/* ─── DATAFRAME ───────────────────────────────────────────── */
[data-testid="stDataFrame"] {
  border-radius: var(--r-md) !important;
  overflow: hidden !important;
  border: 1px solid var(--b1) !important;
}
[data-testid="stDataFrame"] th {
  background: var(--s3) !important; color: var(--t3) !important;
  font-family: var(--font-m) !important; font-size: .72rem !important;
  letter-spacing: 1.2px !important; text-transform: uppercase !important;
}
[data-testid="stDataFrame"] td {
  font-family: var(--font-m) !important;
  font-size: .8rem !important; color: var(--t2) !important;
}

/* ─── PROGRESS ────────────────────────────────────────────── */
[data-testid="stProgress"] > div > div {
  background: rgba(255,255,255,.05) !important; height: 3px !important; border-radius: 2px !important;
}
[data-testid="stProgress"] > div > div > div {
  background: linear-gradient(90deg, var(--leaf), var(--gold)) !important;
  border-radius: 2px !important; transition: width 1s cubic-bezier(.16,1,.3,1) !important;
}

/* ─── DIVIDER ─────────────────────────────────────────────── */
.sf-div {
  height: 1px; margin: 36px 0;
  background: linear-gradient(90deg, transparent, var(--b2), transparent);
  position: relative;
}
.sf-div::after {
  content: '◆'; position: absolute; top: 50%; left: 50%;
  transform: translate(-50%,-50%); font-size: .45rem; color: var(--t4);
  background: var(--ink); padding: 0 10px;
}

/* ─── PLOTLY TWEAKS ───────────────────────────────────────── */
.js-plotly-plot { border-radius: var(--r-md) !important; }

/* ─── TOOLTIP ─────────────────────────────────────────────── */
[data-testid="stTooltipIcon"] { color: var(--t4) !important; }

/* ─── ANIMATIONS ──────────────────────────────────────────── */
@keyframes shimmer {
  0%   { background-position: -200% center; }
  100% { background-position:  200% center; }
}
.sf-glow-line {
  height: 1px; margin: 4px 0 28px;
  background: linear-gradient(90deg, transparent, var(--leaf), var(--gold), var(--sky), transparent);
  background-size: 200% auto; animation: shimmer 3s linear infinite;
}
</style>
""", unsafe_allow_html=True)

# URL parametrlarini tekshirish
if "name" not in st.query_params:
    st.error("⚠️ Iltimos, avval tizimga kiring!")
    st.markdown('<meta http-equiv="refresh" content="2;URL=\'http://localhost:5000/\'">', unsafe_allow_html=True)
    st.stop()

# Foydalanuvchi ismini saqlab olamiz
user_name = st.query_params.get("name", "Foydalanuvchi")



# ══════════════════════════════════════════════════════════════
#  DATA & MODEL
# ══════════════════════════════════════════════════════════════
@st.cache_data
def load_data():
    return pd.read_csv('Crop_recommendation.csv')

@st.cache_resource
def load_model():
    return load('final_rdf_clf.pkl')

df       = load_data()
rdf_clf  = load_model()
X        = df.drop('label', axis=1)
all_crops = sorted(df['label'].unique())

CROP_EMOJIS = {
    'rice':'🌾','maize':'🌽','chickpea':'🫘','kidneybeans':'🫘','pigeonpeas':'🌿',
    'mothbeans':'🌱','mungbean':'🟢','blackgram':'⚫','lentil':'🟤','pomegranate':'🍎',
    'banana':'🍌','mango':'🥭','grapes':'🍇','watermelon':'🍉','muskmelon':'🍈',
    'apple':'🍏','orange':'🍊','papaya':'🧡','coconut':'🥥','cotton':'🤍',
    'jute':'🪢','coffee':'☕'
}

# ══════════════════════════════════════════════════════════════
#  SIDEBAR
# ══════════════════════════════════════════════════════════════
with st.sidebar:

    # Logo
    st.markdown("""
    <div class="sf-logo">
      <div class="sf-logo-inner">
        <div class="sf-logo-ico">🌾</div>
        <div>
          <div class="sf-logo-name">SmartFarm</div>
          <div class="sf-logo-sub">AI Agro Intelligence</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)



with st.sidebar:
    # Foydalanuvchi ismini chiqarish (Ixtiyoriy)
    st.markdown(f"### 👤 Salom, {user_name}!")
    st.info("Tizimga muvaffaqiyatli kirdingiz!")
    
    if st.button("🚪 Tizimdan chiqish"):
        # Flask serveriga qaytarish
        st.markdown('<meta http-equiv="refresh" content="0;URL=\'http://localhost:5000/\'">', unsafe_allow_html=True)


    # Navigation
    st.markdown('<div class="sf-nav-section">Boshqaruv</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="sf-nav-item active">
      <span>🧪</span> Bashorat qilish
      <span class="sf-nav-badge">YANGI</span>
    </div>
    <div class="sf-nav-item">
      <span>📊</span> Analitika
    </div>
    <div class="sf-nav-item">
      <span>🤖</span> Model ma'lumotlari
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sf-nav-section">Ma\'lumotlar</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="sf-nav-item">
      <span>🌱</span> Ekin katalogi
    </div>
    <div class="sf-nav-item">
      <span>📋</span> Tarix
    </div>
    <div class="sf-nav-item">
      <span>⚙️</span> Sozlamalar
    </div>
    """, unsafe_allow_html=True)

    # Status
    st.markdown("""
    <div class="sf-status">
      <div class="sf-status-head">● Tizim holati</div>
      <div class="sf-status-row">
        <div class="sf-dot"></div>
        <span>Random Forest · Faol</span>
      </div>
      <div class="sf-status-row">
        <div class="sf-dot d2"></div>
        <span>AI Maslahat · Faol</span>
      </div>
      <div class="sf-status-row">
        <div class="sf-dot d3"></div>
        <span>API Server · Faol</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # Sidebar reset button
    st.button("🗑  Tozalash", key="sidebar_clear")


# ══════════════════════════════════════════════════════════════
#  HERO HEADER
# ══════════════════════════════════════════════════════════════
st.markdown("""
<div class="sf-hero">
  <div class="sf-eyebrow">⬡ AI — Agro Intelligence Platform</div>
  <h1 class="sf-title">
    Tuproqni <em>tahlil qiling</em>,<br>ekinni aniqlang
  </h1>
  <p class="sf-sub">
    Random Forest · 22 ekin · 99% aniqlik · Real-vaqt AI maslahat
  </p>
</div>
<div class="sf-glow-line"></div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  HERO STATS
# ══════════════════════════════════════════════════════════════
st.markdown("""
<div class="sf-stats">
  <div class="sf-stat">
    <div class="sf-stat-accent" style="background:linear-gradient(90deg,#2dba5f,#1a9147)"></div>
    <div class="sf-stat-icon">🤖</div>
    <div class="sf-stat-val gv">RF</div>
    <div class="sf-stat-key">Model turi</div>
  </div>
  <div class="sf-stat">
    <div class="sf-stat-accent" style="background:linear-gradient(90deg,#3ab0e8,#6be8da)"></div>
    <div class="sf-stat-icon">🌱</div>
    <div class="sf-stat-val sv">22</div>
    <div class="sf-stat-key">Ekin turlari</div>
  </div>
  <div class="sf-stat">
    <div class="sf-stat-accent" style="background:linear-gradient(90deg,#e8a93a,#f0d060)"></div>
    <div class="sf-stat-icon">📐</div>
    <div class="sf-stat-val av">7</div>
    <div class="sf-stat-key">Xususiyatlar</div>
  </div>
  <div class="sf-stat">
    <div class="sf-stat-accent" style="background:linear-gradient(90deg,#9b7be8,#c4aaff)"></div>
    <div class="sf-stat-icon">🎯</div>
    <div class="sf-stat-val vv">99%</div>
    <div class="sf-stat-key">Test aniqligi</div>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  MODEL INFO (collapsible)
# ══════════════════════════════════════════════════════════════
_, c_btn, _ = st.columns([2, 1.5, 2])
with c_btn:
    show_model = st.button("⬡  Model ma'lumotlari", key="model_btn")

if show_model:
    st.markdown("<div class='sf-model-wrap'>", unsafe_allow_html=True)

    st.markdown("""
    <div style="text-align:center;margin-bottom:24px">
      <span style="font-size:.63rem;letter-spacing:2.5px;text-transform:uppercase;
        color:rgba(45,186,95,.6);font-weight:700">Texnik spetsifikatsiya</span>
    </div>
    <div class="sf-mini-stats">
      <div class="sf-mini">
        <div class="sf-mini-val">RF</div>
        <div class="sf-mini-key">Model turi</div>
      </div>
      <div class="sf-mini">
        <div class="sf-mini-val">22</div>
        <div class="sf-mini-key">Ekin turlari</div>
      </div>
      <div class="sf-mini">
        <div class="sf-mini-val">7</div>
        <div class="sf-mini-key">Xususiyatlar</div>
      </div>
      <div class="sf-mini">
        <div class="sf-mini-val">99%</div>
        <div class="sf-mini-key">Aniqlik</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="sf-model-desc">
      <strong style="color:var(--leaf)">Random Forest</strong> — ko'plab qaror daraxtlaridan iborat
      ansambl modeli. Har bir daraxt mustaqil bashorat qiladi, keyin ovoz berish orqali
      yakuniy natija aniqlanadi.<br><br>
      Model <strong style="color:var(--sky)">2 200 ta namuna</strong> (har bir ekin uchun 100 ta)
      asosida o'qitilgan. <strong style="color:var(--leaf)">N, P, K, pH, harorat, namlik</strong> va
      <strong style="color:var(--gold)">yog'ingarchilik</strong> — 7 ta parametr asosida ishlaydi.
      Test aniqlik: <strong style="color:var(--coral)">~99%</strong>.
    </div>
    <p style="font-size:.62rem;letter-spacing:2px;text-transform:uppercase;
      color:var(--t4);font-weight:700;text-align:center;margin-bottom:10px">
      Barcha ekin turlari (22 ta)
    </p>
    """, unsafe_allow_html=True)

    crop_html = "<div class='sf-crop-grid'>"
    for crop in all_crops:
        em = CROP_EMOJIS.get(crop.lower(), '🌱')
        crop_html += f"<span class='sf-crop-tag'>{em} {crop.capitalize()}</span>"
    crop_html += "</div>"
    st.markdown(crop_html, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
#  FEATURE IMPORTANCE CHART
# ══════════════════════════════════════════════════════════════
st.markdown("""
<div class="sf-div"></div>
<div class="sf-sec">
  <div class="sf-sec-line l"></div>
  <div class="sf-sec-tag">📊 Parametrlar ahamiyati</div>
  <div class="sf-sec-line r"></div>
</div>
""", unsafe_allow_html=True)

importance_df = (
    pd.DataFrame({'Feature': list(X.columns),
                  'Importance': rdf_clf.feature_importances_})
    .sort_values('Importance', ascending=True)
)
importance_df['Importance'] *= 100

FEAT_COLORS = ['#0f5128','#1a9147','#2dba5f','#4fd48a','#6be8b0','#3ab0e8','#9b7be8']

_, cc, _ = st.columns([0.5, 6, 0.5])
with cc:
    fig = go.Figure()
    for i, (_, row) in enumerate(importance_df.iterrows()):
        fig.add_trace(go.Bar(
            x=[row['Importance']],
            y=[row['Feature']],
            orientation='h',
            marker=dict(
                color=FEAT_COLORS[i % len(FEAT_COLORS)],
                line=dict(width=0),
                opacity=.85,
            ),
            showlegend=False,
            text=f"{row['Importance']:.1f}%",
            textposition='outside',
            textfont=dict(color='rgba(237,245,240,.5)', size=11, family='JetBrains Mono'),
        ))

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=260,
        margin=dict(l=0, r=60, t=10, b=10),
        bargap=.38,
        xaxis=dict(
            gridcolor='rgba(255,255,255,.04)',
            color='rgba(237,245,240,.25)',
            ticksuffix='%', zeroline=False,
            tickfont=dict(family='JetBrains Mono', size=10),
        ),
        yaxis=dict(
            gridcolor='rgba(0,0,0,0)',
            color='rgba(237,245,240,.55)',
            tickfont=dict(family='JetBrains Mono', size=11),
        ),
    )
    st.plotly_chart(fig, use_container_width=True)


# ─── DYNAMIK OB-HAVO VIDJETI ────────────────────────────────
if 'weather_data' not in st.session_state:
    from weather import get_auto_weather
    st.session_state.weather_data = get_auto_weather()

w = st.session_state.weather_data

with st.sidebar:
    st.markdown("---") # Ajratuvchi chiziq
    if w:
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #00c6ff 0%, #0072ff 100%);
            padding: 20px;
            border-radius: 20px;
            color: white;
            box-shadow: 0 10px 20px rgba(0,114,255,0.3);
            margin: 10px 5px;
            font-family: 'Inter', sans-serif;
        ">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <span style="font-size: 0.8rem; font-weight: 600; opacity: 0.9;">Hozirgi sharoit</span>
                <span style="font-size: 1.2rem;">📍</span>
            </div>
            <h2 style="margin: 5px 0; color: white; font-size: 1.4rem;">{w['city']}</h2>
            <div style="display: flex; align-items: center; gap: 15px; margin-top: 10px;">
                <span style="font-size: 2.5rem; font-weight: 800;">{int(w['temp'])}°</span>
                <div style="font-size: 0.8rem; opacity: 0.9;">
                    <div>💦 Namlik: {w['humidity']}%</div>
                    <div>🌧️ Yog'in: {w['rain']} mm</div>
                </div>
            </div>
            <div style="margin-top: 15px; padding-top: 10px; border-top: 1px solid rgba(255,255,255,0.2); font-size: 0.7rem; text-align: center; font-style: italic;">
                Ma'lumotlar avtomatik yangilandi
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.error("📍 Ob-havoni aniqlab bo'lmadi")

# ══════════════════════════════════════════════════════════════
#  INPUT SECTION
# ══════════════════════════════════════════════════════════════

# 📸 Kamera bloki
st.markdown("### 📸 Ekin holatini rasmga oling")
img_file = st.camera_input("Kamera orqali vizual tahlil")

if img_file:
    st.image(img_file, caption="Yuklangan rasm", width=300)

st.markdown("""
<div class="sf-div"></div>
<div class="sf-sec">
  <div class="sf-sec-line l"></div>
  <div class="sf-sec-tag">🧪 Tuproq parametrlarini kiriting</div>
  <div class="sf-sec-line r"></div>
</div>
""", unsafe_allow_html=True)

# Ob-havo qiymatlarini tayyorlab olamiz
# Agar w bo'lsa o'shani, bo'lmasa default qiymatlarni oladi
temp_val = float(w['temp']) if w else 20.8
hum_val = float(w['humidity']) if w else 82.0
rain_val = float(w['rain']) if w else 202.9

col_l, col_gap, col_r = st.columns([4, .5, 4])

with col_l:
    st.markdown("<div class='sf-input-card g'>", unsafe_allow_html=True)
    n_in = st.number_input('🌱 Azot (N) — kg/ha', min_value=0, max_value=140,
                            value=90, help='0–140 kg/ha')
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='sf-input-card s'>", unsafe_allow_html=True)
    p_in = st.number_input('💧 Fosfor (P) — kg/ha', min_value=5, max_value=145,
                            value=42, help='5–145 kg/ha')
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='sf-input-card a'>", unsafe_allow_html=True)
    k_in = st.number_input('⚡ Kaliy (K) — kg/ha', min_value=5, max_value=205,
                            value=43, help='5–205 kg/ha')
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='sf-input-card v'>", unsafe_allow_html=True)
    temp_in = st.number_input('🌡️ Harorat — °C', min_value=9., max_value=43.,
                               value=temp_val, step=.1, format='%.1f')
    st.markdown("</div>", unsafe_allow_html=True)

with col_r:
    st.markdown("<div class='sf-input-card s'>", unsafe_allow_html=True)
    hum_in = st.number_input('💦 Namlik — %', min_value=15., max_value=99.,
                              value=hum_val, step=.1, format='%.1f')
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='sf-input-card g'>", unsafe_allow_html=True)
    ph_in = st.number_input('⚗️ pH qiymati', min_value=3.6, max_value=9.9,
                             value=6.5, step=.1, format='%.1f')
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='sf-input-card a'>", unsafe_allow_html=True)
    rain_val = max(21.0, rain_val)
    rain_in = st.number_input(
    "🌧️ Yog'ingarchilik — mm",
    min_value=21.0,
    max_value=298.0,
    value=rain_val,
    step=0.5,
    format='%.1f'
    )
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div style='margin-top:14px'>", unsafe_allow_html=True)
    predict_btn = st.button("⬡  Ekinni aniqlash →", key="predict_main")
    st.markdown("</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════
#  PREDICTION & RESULTS
# ══════════════════════════════════════════════════════════════
inputs = [[n_in, p_in, k_in, temp_in, hum_in, ph_in, rain_in]]

if predict_btn:
    proba      = rdf_clf.predict_proba(inputs)[0]
    classes    = rdf_clf.classes_
    top5_idx   = proba.argsort()[::-1][:5]
    top5       = [(classes[i], round(proba[i] * 100, 1)) for i in top5_idx]
    best_crop  = top5[0][0]
    best_emoji = CROP_EMOJIS.get(best_crop.lower(), '🌱')

    st.markdown("<div class='sf-div'></div>", unsafe_allow_html=True)

    # ── HERO RESULT ─────────────────────────────────────────
    st.markdown("""
    <div class="sf-sec">
      <div class="sf-sec-line l"></div>
      <div class="sf-sec-tag">✦ Tavsiya natijalari</div>
      <div class="sf-sec-line r"></div>
    </div>
    """, unsafe_allow_html=True)

    _, rc, _ = st.columns([1, 4, 1])
    with rc:
        st.markdown(f"""
        <div class="sf-result-hero">
          <div class="sf-r-eyebrow">✦ Tavsiya etilgan ekin</div>
          <div class="sf-r-crop">{best_emoji} {best_crop.capitalize()}</div>
          <div class="sf-r-conf">
            Ishonch darajasi &nbsp;·&nbsp; <span>{top5[0][1]}%</span>
          </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)

    # ── TOP 5 ────────────────────────────────────────────────
    st.markdown("""
    <div class="sf-sec">
      <div class="sf-sec-line l"></div>
      <div class="sf-sec-tag">🏆 Top 5 tavsiyalar</div>
      <div class="sf-sec-line r"></div>
    </div>
    """, unsafe_allow_html=True)

    RANK_STYLES = [
        ("rgba(45,186,95,.08)",   "rgba(45,186,95,.22)",   "var(--leaf)",   "var(--leaf)",   "🥇"),
        ("rgba(58,176,232,.06)",  "rgba(58,176,232,.18)",  "var(--sky)",    "var(--sky)",    "🥈"),
        ("rgba(232,169,58,.06)",  "rgba(232,169,58,.18)",  "var(--gold)",   "var(--gold)",   "🥉"),
        ("rgba(155,123,232,.05)", "rgba(155,123,232,.15)", "var(--violet)", "var(--violet)", "④"),
        ("rgba(255,255,255,.03)", "var(--b1)",              "var(--t2)",     "var(--t3)",     "⑤"),
    ]

    _, rc2, _ = st.columns([1, 4, 1])
    with rc2:
        for i, (crop_name, pct) in enumerate(top5):
            bg, border, nc, bc, medal = RANK_STYLES[i]
            em = CROP_EMOJIS.get(crop_name.lower(), '🌱')
            st.markdown(f"""
            <div class="sf-rank" style="background:{bg};border-color:{border}">
              <div class="sf-rank-num">{medal}</div>
              <div class="sf-rank-name" style="color:{nc}">{em} {crop_name.capitalize()}</div>
              <div class="sf-rank-bar-bg">
                <div class="sf-rank-bar"
                  style="width:{int(pct)}%;background:{bc};
                         animation:none;width:{int(pct)}%">
                </div>
              </div>
              <div class="sf-rank-pct" style="color:{nc}">{pct}%</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div class='sf-div'></div>", unsafe_allow_html=True)

    # ── STATISTICS ───────────────────────────────────────────
    st.markdown("""
    <div class="sf-sec">
      <div class="sf-sec-line l"></div>
      <div class="sf-sec-tag">📈 Ekin statistikasi</div>
      <div class="sf-sec-line r"></div>
    </div>
    """, unsafe_allow_html=True)

    df_pred = df[df['label'] == best_crop]
    st.dataframe(
        df_pred.describe().style.format("{:.2f}"),
        use_container_width=True,
    )

    # ── CROP DISTRIBUTION CHART ──────────────────────────────
    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    fig2 = px.violin(
        df_pred.melt(id_vars='label'),
        x='variable', y='value', box=True,
        color='variable',
        color_discrete_sequence=['#2dba5f','#3ab0e8','#e8a93a','#9b7be8','#e86060','#4fd48a','#6be8da'],
    )
    fig2.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=300,
        showlegend=False,
        font=dict(color='rgba(237,245,240,.5)', family='JetBrains Mono', size=10),
        xaxis=dict(gridcolor='rgba(255,255,255,.04)', color='rgba(237,245,240,.3)', zeroline=False),
        yaxis=dict(gridcolor='rgba(255,255,255,.04)', color='rgba(237,245,240,.3)', zeroline=False),
        margin=dict(l=0, r=0, t=16, b=0),
    )
    fig2.update_traces(
        line_color='rgba(255,255,255,.15)',
        marker=dict(size=3, opacity=.5),
        meanline_visible=True,
    )
    st.plotly_chart(fig2, use_container_width=True)

    st.markdown("<div class='sf-div'></div>", unsafe_allow_html=True)

    # ── AI PROMPT ────────────────────────────────────────────
    ai_prompt = f"""
    Tuproq ma'lumotlari:
    Azot (N): {n_in} kg/ha
    Fosfor (P): {p_in} kg/ha
    Kaliy (K): {k_in} kg/ha
    Harorat: {temp_in}°C
    Namlik: {hum_in}%
    pH: {ph_in}
    Yog'ingarchilik: {rain_in} mm

    Tavsiya etilgan ekin: {best_crop.capitalize()}

    Qisqa va aniq tushuntirish ber:
    - Nima uchun bu ekin mos keladi
    - Qanday qilib hosilni yaxshilash mumkin
    - Ogohlantirish yoki tavsiyalar
    """

    # ── VOICE ────────────────────────────────────────────────
    st.markdown("""
    <div class="sf-sec">
      <div class="sf-sec-line l"></div>
      <div class="sf-sec-tag">🔊 Ovozli maslahat</div>
      <div class="sf-sec-line r"></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='sf-voice-wrap'>", unsafe_allow_html=True)
    st.markdown("""
    <div class="sf-voice-head">
      <span class="sf-voice-badge">OVOZLI AI</span>
      <span style="font-size:.72rem;color:var(--t4);font-family:'JetBrains Mono',monospace">
        Text-to-Speech · Real-vaqt
      </span>
    </div>
    """, unsafe_allow_html=True)


    with st.spinner("🤖 AI tahlil qilmoqda va ovoz yaratmoqda..."):
        # AI dan javob olish va uni audyoga o'girish bir vaqtda kutiladi
        ai_response = get_ai_response(ai_prompt)
        audio_html = get_audio_html(ai_response)
    
    # Spinner tugagach, audio pleyerni chiqaramiz
    if audio_html:
        st.markdown(audio_html, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='sf-div'></div>", unsafe_allow_html=True)

    # ── AI TEXT RESPONSE ─────────────────────────────────────
    st.markdown("""
    <div class="sf-sec">
      <div class="sf-sec-line l"></div>
      <div class="sf-sec-tag">🤖 AI Tahlili</div>
      <div class="sf-sec-line r"></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="sf-ai-wrap">
      <div class="sf-ai-quote">"</div>
      <div class="sf-ai-header">
        <span class="sf-ai-badge">AI MASLAHAT</span>
        <span class="sf-ai-ts">Real-vaqt tahlil · {best_crop.capitalize()}</span>
      </div>
      <div class="sf-ai-body">{ai_response}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='height:40px'></div>", unsafe_allow_html=True)

    # ── FOOTER CROP GRID ─────────────────────────────────────
    st.markdown("""
    <div class="sf-sec">
      <div class="sf-sec-line l"></div>
      <div class="sf-sec-tag">🌿 Barcha ekin turlari</div>
      <div class="sf-sec-line r"></div>
    </div>
    """, unsafe_allow_html=True)

    footer_crops = "<div class='sf-crop-grid' style='margin-bottom:40px'>"
    for crop in all_crops:
        em  = CROP_EMOJIS.get(crop.lower(), '🌱')
        highlight = "background:var(--leaf-glow);border-color:var(--leaf-edge);color:var(--leaf)" \
                    if crop == best_crop else ""
        footer_crops += f"<span class='sf-crop-tag' style='{highlight}'>{em} {crop.capitalize()}</span>"
    footer_crops += "</div>"
    st.markdown(footer_crops, unsafe_allow_html=True)