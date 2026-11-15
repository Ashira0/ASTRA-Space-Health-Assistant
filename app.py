import json
from datetime import date

from donki import fetch_sep_events

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title='ASTRA | Mission Control', page_icon='🛰️', layout='wide', initial_sidebar_state='expanded')
st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&display=swap');
:root{--a:#07101d;--panel:#0d1c2d;--edge:#1d3b51;--ice:#eaf7ff;--cyan:#67e9f4;--muted:#829fb4}
html,body,.stApp,[class*=css]{font-family:'DM Sans',sans-serif!important}
.stApp{background:radial-gradient(ellipse at 65% -20%,#12364b 0%,transparent 52%),#050d19;color:var(--ice)}
[data-testid=stSidebar]{background:#081523!important;border-right:1px solid #1c3447}
[data-testid=stSidebar] p,[data-testid=stSidebar] label{color:#a5c0d0!important}
.block-container{max-width:1670px!important;padding-top:.75rem!important;padding-bottom:3rem!important}
h1,h2,h3{font-family:'Space Grotesk',sans-serif!important;letter-spacing:-.035em!important}
h3{font-size:1.1rem!important}
.stTabs [data-baseweb=tab-list]{gap:9px;border-bottom:1px solid #1c3549;padding-bottom:4px}
.stTabs [data-baseweb=tab]{font-size:.83rem;font-weight:800;letter-spacing:.055em;color:#92b3c6;border-radius:8px 8px 0 0;padding:10px 14px}
.stTabs [aria-selected=true]{color:#79edfa!important;background:#102c3d!important}
[data-testid=stMetric]{background:#0b1d2e;border:1px solid #214155;border-radius:13px;padding:16px}
[data-testid=stMetricValue]{font-family:'Space Grotesk';color:#f1fcff!important}
[data-testid=stMetricLabel]{color:#a2bccc!important}
[data-testid=stDataFrame]{border:1px solid #244054;border-radius:12px}
[data-testid=stAlert]{border-radius:11px}
.stButton button,.stDownloadButton button{border-radius:9px}
hr{border-color:#1a364a!important}
.mast{display:flex;align-items:center;justify-content:space-between;gap:18px;border:1px solid #244a60;background:linear-gradient(95deg,#102a3d,#0a1c2b 65%,#0c2638);padding:16px 22px;border-radius:15px;margin-bottom:14px;position:relative;overflow:hidden}
.mast:after{content:'';width:230px;height:230px;position:absolute;right:18%;top:-170px;border:1px solid #5edff533;border-radius:50%;box-shadow:0 0 0 28px #6ae2f00a,0 0 0 58px #6ae2f008;pointer-events:none}
.brand{font:800 30px 'Space Grotesk',sans-serif;letter-spacing:-.065em;color:#f4fbff;line-height:1.1}
.brand em{font-style:normal;color:#65e9f4}.mast-sub{color:#a7c4d3;font-size:12px;margin-top:4px}.mast-right{text-align:right;z-index:1}.micro{font-size:10px;letter-spacing:.18em;text-transform:uppercase;font-weight:800;color:#75d8e8}.mast-state{font:700 15px 'Space Grotesk';color:#d9f6ff;margin-top:5px}.led{display:inline-block;background:#44e6b4;width:8px;height:8px;border-radius:50%;box-shadow:0 0 14px #44e6b4;margin-right:7px}
.section-kicker{font-size:10px;letter-spacing:.2em;text-transform:uppercase;color:#74ddec;font-weight:800;margin:12px 0 10px}
.overview{display:grid;grid-template-columns:1.1fr 1.1fr .8fr;gap:12px;margin:8px 0 14px}
.info-panel{border:1px solid #244457;background:linear-gradient(140deg,#10283a,#0b1b2b);border-radius:12px;padding:15px 17px;min-height:86px}
.info-label{font-size:10px;color:#83a9bf;letter-spacing:.14em;font-weight:800;text-transform:uppercase}.info-value{font:700 20px 'Space Grotesk';margin-top:6px;color:#f1faff}.info-small{font-size:11px;color:#90aec0;margin-top:5px}.info-value.alert{color:#ffbf8d}
.vitals{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px;margin:12px 0 16px}
.vital{position:relative;overflow:hidden;background:linear-gradient(145deg,#11293c,#0a1b2a);border:1px solid #29485d;border-radius:14px;padding:17px 17px 13px;min-height:145px}
.vital:before{content:'';position:absolute;left:0;top:0;bottom:0;width:3px;background:var(--accent)}.vital.bad{border-color:#a96c4e;background:linear-gradient(145deg,#302327,#151a25)}
.vital-top{display:flex;justify-content:space-between;align-items:center;gap:7px}.vital-label{font-size:11px;letter-spacing:.11em;text-transform:uppercase;color:#a1bdce;font-weight:800}.vital-symbol{color:var(--accent);font-size:18px}.vital-number{font:700 clamp(25px,2.6vw,39px) 'Space Grotesk';color:#f4fbff;letter-spacing:-.05em;margin:13px 0 2px;line-height:1}.vital-number span{font:600 13px 'DM Sans';letter-spacing:0;color:#a5bdce;margin-left:5px}.vital-footer{display:flex;justify-content:space-between;gap:8px;align-items:center;margin-top:13px;font-size:11px;color:#9ab4c5}.vital-state{font-size:10px;color:#6fe7c0;letter-spacing:.07em;font-weight:800}.vital.bad .vital-state{color:#ffb17e}
.ops-grid{display:grid;grid-template-columns:1.02fr 1.65fr 1fr;gap:13px;margin:0 0 12px;align-items:stretch}
.instrument{border:1px solid #214257;background:linear-gradient(150deg,#0e2435,#081a2a);border-radius:14px;padding:17px;min-width:0;position:relative;overflow:hidden}.instrument-title{font:700 14px 'Space Grotesk';color:#f0f9ff}.instrument-caption{font-size:11px;color:#8eafc1;margin:5px 0 14px}.instrument .micro{font-size:9px}
.body-wrap{height:270px;display:flex;align-items:center;justify-content:center;position:relative;background:radial-gradient(circle at 50% 43%,#17445b66,transparent 60%)}.body-wrap svg{height:255px;max-width:100%;filter:drop-shadow(0 0 18px #4be7ed25)}
.body-marker{fill:#58e4f0;filter:drop-shadow(0 0 4px #58e4f0)}.body-marker.warning{fill:#ff9d73;filter:drop-shadow(0 0 6px #ff9d73)}
.body-key{display:flex;justify-content:space-between;border-top:1px solid #24445a;padding-top:11px;color:#8eb2c4;font-size:10px}.body-key b{color:#cce7f2}
.signal-list{display:flex;flex-direction:column;gap:10px;margin-top:10px}.signal-row{display:flex;justify-content:space-between;align-items:center;gap:10px;border-bottom:1px solid #1e394b;padding-bottom:9px}.signal-row:last-child{border-bottom:0}.signal-label{color:#a7c1d1;font-size:11px}.signal-value{color:#edf9ff;font:700 13px 'Space Grotesk'}.signal-track{height:5px;border-radius:10px;background:#193547;overflow:hidden;margin-top:7px}.signal-fill{height:100%;border-radius:10px;background:var(--bar);width:var(--width)}
.alert-panel{border:1px solid #275463;border-radius:11px;background:#0a2a2d;padding:12px;margin-top:10px}.alert-panel.warn{background:#30251e;border-color:#966e46}.alert-title{font-weight:800;font-size:12px;color:#b7f8df}.alert-panel.warn .alert-title{color:#ffd0a0}.alert-copy{font-size:11px;color:#b2c7ce;margin-top:6px;line-height:1.55}
.readout{font:700 28px 'Space Grotesk';color:#eafaff;letter-spacing:-.04em;margin:8px 0}.readout small{font:500 11px 'DM Sans';color:#92b2c6}
.panel-bottom{border-top:1px solid #203c50;padding-top:12px;margin-top:14px;font-size:10px;color:#8faabc}
@media(max-width:1100px){.ops-grid{grid-template-columns:1fr 1.4fr}.ops-grid .instrument:last-child{grid-column:1/-1}.vitals{grid-template-columns:repeat(2,1fr)}}
@media(max-width:720px){.mast{padding:13px}.mast-right{display:none}.overview{grid-template-columns:1fr}.ops-grid{grid-template-columns:1fr}.ops-grid .instrument:last-child{grid-column:auto}.vitals{grid-template-columns:1fr 1fr}.vital{padding:13px;min-height:120px}.vital-number{font-size:25px}}

/* Phase 9: fast, simultaneous telemetry sweep on each chart render. */
@keyframes astra-signal-sweep {from{stroke-dashoffset:var(--astra-length, 2400)}to{stroke-dashoffset:0}}
@media (prefers-reduced-motion: no-preference) {
  .astra-wave {stroke-dasharray:2400;stroke-dashoffset:2400;animation:astra-signal-sweep 1s cubic-bezier(.22,.8,.3,1) forwards;}
  .js-plotly-plot .scatterlayer .trace .js-line {stroke-dasharray:2400!important;stroke-dashoffset:2400;animation:astra-signal-sweep 1s cubic-bezier(.22,.8,.3,1) forwards;}
}
/* Phase 8: unified premium research / intelligence / methodology surfaces */
.page-hero{border:1px solid #28516a;border-radius:16px;background:radial-gradient(circle at 92% 10%,#17536c66,transparent 45%),linear-gradient(110deg,#102b40,#091a2b);padding:24px 27px;margin:12px 0 19px}
.hero-tag{font-size:10px;font-weight:800;letter-spacing:.2em;color:#6de9f3}.hero-title{font:700 27px 'Space Grotesk',sans-serif;letter-spacing:-.04em;color:#f1fbff;margin:7px 0}.hero-copy{font-size:13px;line-height:1.6;color:#a5c3d3;max-width:900px}
.kpi-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px;margin:15px 0 19px}.kpi{background:linear-gradient(140deg,#10283a,#0a1c2c);border:1px solid #24465c;border-radius:12px;padding:16px 18px}.kpi-label{font-size:10px;color:#9cb8c8;letter-spacing:.12em;text-transform:uppercase;font-weight:800}.kpi-value{font:700 26px 'Space Grotesk';color:#f1fbff;margin:8px 0 3px}.kpi-note{font-size:10px;color:#87adbd}
.notice-strip{padding:13px 16px;background:#0b2831;border:1px solid #255768;border-radius:11px;color:#a8dce2;font-size:12px;line-height:1.6;margin:10px 0 17px}
.notice-strip.warn{background:#30231e;border-color:#a46b48;color:#ffd0ad}
.stButton>button[kind=primary]{background:#1c8598!important;border:1px solid #4cc7d8!important;color:white!important;font-weight:700}
@media(max-width:950px){.kpi-grid{grid-template-columns:repeat(2,minmax(0,1fr))}}
</style>""",unsafe_allow_html=True)
SCENARIOS = {
 'Nominal operations': 'Stable health indicators during routine operations.',
 'Exercise recovery': 'Elevated pulse after scheduled exercise, followed by recovery.',
 'Possible hypoxia': 'A progressive decline in simulated oxygen saturation.',
 'Radiation sensor anomaly': 'A rising dimensionless radiation sensor index.',
 'Sleep deprivation': 'Reduced reported sleep duration during a demanding mission.',
 'Multi-system emergency drill': 'Independent synthetic disturbances across all four monitoring channels; not a physiological prediction.'
}

@st.cache_data
def generate(scenario, seed, intensity=100):
    rng=np.random.default_rng(seed); t=np.arange(60)
    hr=72+rng.normal(0,2.2,60)
    oxygen=98+rng.normal(0,.35,60)
    sleep=7.5+rng.normal(0,.13,60)
    rad=.45+rng.normal(0,.04,60)
    if scenario=='Exercise recovery':
        hr[25:]=np.r_[np.linspace(75,140,11),np.linspace(138,84,24)]+rng.normal(0,2,35)
    elif scenario=='Possible hypoxia':
        oxygen[25:]=np.linspace(98,89,35)+rng.normal(0,.28,35)
    elif scenario=='Radiation sensor anomaly':
        rad[30:]=np.linspace(.5,2.9,30)+rng.normal(0,.05,30)
    elif scenario=='Sleep deprivation':
        sleep[25:]=4.2+rng.normal(0,.15,35)
    elif scenario=='Multi-system emergency drill':
        # Independent scripted channels, NOT a model of simultaneous human deterioration.
        ramp=np.linspace(0,1,35)**1.15
        hr[25:]+=76*ramp
        oxygen[25:]-=13*ramp
        sleep[25:]-=4.7*ramp
        rad[25:]+=3.1*ramp
    # Demonstration-only severity scaling: interpolate between nominal and the
    # scenario-specific simulated channel, not a medical outcome model.
    if scenario != 'Nominal operations':
        weight=intensity/100.0
        base_rng=np.random.default_rng(seed)
        base_hr=72+base_rng.normal(0,2.2,60)
        base_oxygen=98+base_rng.normal(0,.35,60)
        base_sleep=7.5+base_rng.normal(0,.13,60)
        base_rad=.45+base_rng.normal(0,.04,60)
        hr=base_hr+(hr-base_hr)*weight
        oxygen=base_oxygen+(oxygen-base_oxygen)*weight
        sleep=base_sleep+(sleep-base_sleep)*weight
        rad=base_rad+(rad-base_rad)*weight
    hr=np.clip(hr,0,300); oxygen=np.clip(oxygen,0,100); sleep=np.clip(sleep,0,24); rad=np.maximum(rad,0)
    return pd.DataFrame({'Minute':t,'Heart rate (bpm)':hr.round(1),'SpO₂ (%)':oxygen.round(1),'Sleep (h)':sleep.round(1),'Radiation index (relative)':rad.round(2)})

def evaluate(row):
    alerts=[]
    if row['Heart rate (bpm)']>120:
        alerts.append(('HIGH PULSE','Check recent activity and sensor quality; request crew medical review if persistent.'))
    if row['SpO₂ (%)']<94:
        alerts.append(('LOW OXYGEN READING','Verify sensor placement and escalate through mission medical procedures.'))
    if row['Sleep (h)']<5:
        alerts.append(('LOW REPORTED SLEEP','Review rest opportunities and operational workload.'))
    if row['Radiation index (relative)']>2:
        alerts.append(('RADIATION SENSOR FLAG','Verify sensor reading and consult mission radiation procedures.'))
    return alerts

st.sidebar.markdown('### ◈ ASTRA / FLIGHT SYSTEMS')
st.sidebar.caption('ARES-01   /   CREW OPERATIONS')
profile=st.sidebar.selectbox('ACTIVE CREW MEMBER',['Commander Vega','Specialist Orion','Engineer Nova'])
scenario=st.sidebar.selectbox('MISSION SIMULATION',list(SCENARIOS))
intensity=st.sidebar.slider('SCENARIO INTENSITY',0,150,100,5,help='Demonstration-only stress-test scaling; 0% = nominal baseline, 100% = original scenario, 150% = amplified synthetic scenario. Not a clinical severity scale.',disabled=scenario=='Nominal operations')
st.sidebar.caption('0% nominal · 100% scripted disturbance · 150% amplified')
st.sidebar.caption('For simultaneous alerts choose **Multi-system emergency drill**. All channels are independently scripted, not causally linked.')
seed=st.sidebar.number_input('Simulation seed',min_value=0,max_value=99999,value=42)
st.sidebar.caption('Scenario intensity changes simulated inputs only. Alerts use illustrative rules, not medical predictions.')
st.sidebar.divider()
st.sidebar.markdown('**DATA CHANNELS**')
st.sidebar.caption('01 · Synthetic crew telemetry\n\n02 · NASA OSD-575 laboratory data\n\n03 · NASA DONKI space weather')
st.sidebar.divider()
st.sidebar.caption('ASTRA / Research prototype · 2026')
st.markdown("""<div class='mast'><div><div class='micro'>◈ ARES-01 &nbsp; / &nbsp; CREW HEALTH INTELLIGENCE</div><div class='brand'>ASTRA <em>/</em> FLIGHT SYSTEMS</div><div class='mast-sub'>Autonomous Space Telemetry & Risk Assessment · Mission operations console</div></div><div class='mast-right'><div class='micro'>TELEMETRY SOURCE</div><div class='mast-state'><span class='led'></span>SIMULATION ACTIVE</div><div class='mast-sub'>RESEARCH PROTOTYPE &nbsp; • &nbsp; NOT FOR CLINICAL USE</div></div></div>""",unsafe_allow_html=True)

df=generate(scenario,seed,intensity)
st.sidebar.divider()
st.sidebar.markdown('### Optional telemetry import')
upload=st.sidebar.file_uploader('Upload compatible CSV',type=['csv'],help='Expected columns: Minute, Heart rate (bpm), SpO₂ (%), Sleep (h), Radiation index (relative). Imported readings are not automatically NASA data.')
if upload is not None:
    try:
        candidate=pd.read_csv(upload)
        required=['Minute','Heart rate (bpm)','SpO₂ (%)','Sleep (h)','Radiation index (relative)']
        missing=[c for c in required if c not in candidate.columns]
        if missing: raise ValueError('Missing columns: '+', '.join(missing))
        candidate=candidate[required].copy()
        if len(candidate)<2 or len(candidate)>10000: raise ValueError('CSV must contain 2 to 10,000 rows.')
        for col in required: candidate[col]=pd.to_numeric(candidate[col],errors='raise')
        if not np.isfinite(candidate.to_numpy(dtype=float)).all(): raise ValueError('All readings must be finite numbers.')
        if not candidate['Minute'].is_monotonic_increasing or candidate['Minute'].duplicated().any(): raise ValueError('Minute must be strictly increasing.')
        if not candidate['SpO₂ (%)'].between(0,100).all(): raise ValueError('SpO₂ must be between 0 and 100.')
        if not candidate['Heart rate (bpm)'].between(0,300).all() or not candidate['Sleep (h)'].between(0,24).all(): raise ValueError('Implausible heart rate or sleep values.')
        if not candidate['Radiation index (relative)'].ge(0).all(): raise ValueError('Radiation index cannot be negative.')
        df=candidate.reset_index(drop=True)
        st.sidebar.success(f'Loaded {len(df)} rows')
    except Exception as exc:
        st.sidebar.error(f'Import rejected: {exc}')
        st.stop()
if upload is not None:
    st.warning('Imported CSV: source and measurement definitions are user-supplied and unverified. Alert rules remain illustrative; do not use for medical decisions.')
tab_ops, tab_research, tab_weather, tab_method, tab_checkin, tab_copilot = st.tabs(['◈  LIVE OPERATIONS','◈  HUMAN RESEARCH','◈  SPACE WEATHER','◈  DATA & METHODS','◈  WELLNESS CHECK-IN','◈  ASTRA COPILOT'])
# The timeline lives in Live Operations; persist its value for all tabs and the quick assistant.
if 'astra_sample_index' not in st.session_state:
    st.session_state.astra_sample_index=len(df)-1
st.session_state.astra_sample_index=min(int(st.session_state.astra_sample_index),len(df)-1)
with tab_ops:
    from html import escape
    minute=st.slider('MISSION TIMELINE · SAMPLE INDEX',0,len(df)-1,key='astra_sample_index',help='Scrub to review the evolution of simulated alerts. Sample index is not a real mission clock.')
    visible=df.iloc[:minute+1]; current=df.iloc[minute]; alerts=evaluate(current)
    active={name for name,_ in alerts}
    source_label='USER-IMPORTED / UNVERIFIED' if upload is not None else 'SYNTHETIC / SCENARIO ENGINE'
    status='REVIEW REQUIRED' if alerts else 'ALL CHANNELS NOMINAL'
    st.markdown(f"<div class='overview'><div class='info-panel'><div class='info-label'>ACTIVE CREW / ARES-01</div><div class='info-value'>{escape(profile.upper())}</div><div class='info-small'>Crew health station · Selected profile</div></div><div class='info-panel'><div class='info-label'>MISSION CONDITION</div><div class='info-value {'alert' if alerts else ''}'>{status}</div><div class='info-small'>{escape(scenario)} · {len(alerts)} active demonstration flag(s)</div></div><div class='info-panel'><div class='info-label'>DATA FEED / SAMPLE</div><div class='info-value'>#{minute:03d} <span style='color:#67e9f4;font-size:12px'>/ {len(df)-1:03d}</span></div><div class='info-small'>{source_label}</div></div></div>",unsafe_allow_html=True)
    metrics=[('Heart rate (bpm)','HEART RATE','bpm','#63e5f3','♡','HIGH PULSE'),('SpO₂ (%)','OXYGEN SATURATION','%','#67e5bb','◉','LOW OXYGEN READING'),('Sleep (h)','REPORTED SLEEP','h','#b7a4ff','◷','LOW REPORTED SLEEP'),('Radiation index (relative)','RADIATION SENSOR','index','#f6bb76','✳','RADIATION SENSOR FLAG')]
    cards=[]
    for key,label,unit,color,symbol,alertname in metrics:
        val=float(current[key]); baseline=float(df.iloc[:min(20,len(df))][key].mean()); bad=alertname in active
        cards.append(f"<div class='vital {'bad' if bad else ''}' style='--accent:{color}'><div class='vital-top'><span class='vital-label'>{label}</span><span class='vital-symbol'>{symbol}</span></div><div class='vital-number'>{val:.1f}<span>{unit}</span></div><div class='vital-footer'><span>Δ {val-baseline:+.1f} vs initial</span><span class='vital-state'>{'● FLAGGED' if bad else '● NO FLAG'}</span></div></div>")
    st.markdown("<div class='section-kicker'>01 &nbsp; / &nbsp; CREW BIOMETRIC INSTRUMENTS</div><div class='vitals'>"+''.join(cards)+"</div>",unsafe_allow_html=True)
    if scenario=='Multi-system emergency drill' and upload is None:
        st.warning('MULTI-SYSTEM TRAINING EXERCISE — These four trends are independently scripted. They do not represent a validated medical progression, actual radiation dose, or predicted patient outcome.')
    if alerts:
        with st.expander('MISSION RESPONSE PLAYBOOK · TRAINING GUIDANCE',expanded=(scenario=='Multi-system emergency drill')):
            st.markdown('**Immediate operational response:** Confirm the data feed and sensor quality; contact the designated crew medical officer / ground medical support; follow mission-approved emergency procedures. Do not rely on this prototype for diagnosis or treatment.')
            playbook={'HIGH PULSE':'Verify pulse sensor and recent exertion; request clinical assessment and review activity under mission procedures.', 'LOW OXYGEN READING':'Check oxygen sensor fit and repeat measurement; request immediate medical review and use approved oxygen/environmental checklists.', 'LOW REPORTED SLEEP':'Confirm sleep-log accuracy; review workload, rest opportunities, and fatigue-related task assignments.', 'RADIATION SENSOR FLAG':'Cross-check calibrated radiation instruments and mission space-weather guidance; follow approved sheltering and exposure protocols if warranted.'}
            for name,_ in alerts: st.markdown(f'**{name}:** {playbook[name]}')
            st.markdown('**Survival probability: Not estimable.** A percentage would require validated physiological models, exposure units, duration, clinical context, and outcome data. ASTRA has none of these; displaying a number would be misleading.')
    def wave_svg(key,color):
        vals=visible[key].to_numpy(dtype=float)
        if len(vals)<2: vals=np.r_[vals,vals]
        low,high=float(np.min(vals)),float(np.max(vals))
        span=max(high-low,1.0 if key!='Radiation index (relative)' else .1)
        mid=(high+low)/2
        pts=' '.join(f'{i*500/(len(vals)-1):.1f},{56-(v-mid)*62/span:.1f}' for i,v in enumerate(vals))
        return f"<svg viewBox='0 0 500 112' preserveAspectRatio='none' width='100%' height='94' role='img' aria-label='{escape(key)} trend'><defs><linearGradient id='grad{metrics.index(next(m for m in metrics if m[0]==key))}' x1='0' x2='0' y1='0' y2='1'><stop offset='0%' stop-color='{color}' stop-opacity='.14'/><stop offset='100%' stop-color='{color}' stop-opacity='0'/></linearGradient></defs><path d='M0 28H500 M0 56H500 M0 84H500' stroke='#254457' stroke-width='.8' stroke-dasharray='3 6'/><polyline class='astra-wave' points='{pts}' fill='none' stroke='{color}' stroke-width='2.8' stroke-linecap='round' stroke-linejoin='round' vector-effect='non-scaling-stroke'/></svg>"
    iswarn=bool(alerts)
    body_svg="""<svg viewBox='0 0 260 320' xmlns='http://www.w3.org/2000/svg' aria-label='Illustrative crew body sensor map'><defs><linearGradient id='bodyg' x1='0' y1='0' x2='1' y2='1'><stop stop-color='#1b5165'/><stop offset='1' stop-color='#0b2537'/></linearGradient></defs><g stroke='#67d7e9' stroke-opacity='.7' stroke-width='1.6' fill='url(#bodyg)'><circle cx='130' cy='38' r='24'/><path d='M109 65 Q89 68 78 80 L53 155 Q48 169 60 174 Q70 176 75 161 L95 114 L99 187 L88 285 Q86 298 99 299 Q111 300 114 286 L130 209 L146 286 Q149 300 161 299 Q174 298 172 285 L161 187 L165 114 L185 161 Q190 176 200 174 Q212 169 207 155 L182 80 Q171 68 151 65 Z'/></g><g stroke='#67e8f0' opacity='.25' fill='none'><circle cx='130' cy='139' r='88'/><circle cx='130' cy='139' r='116' stroke-dasharray='3 8'/><path d='M0 139H260 M130 0V320' stroke-dasharray='3 8'/></g><g stroke='#8cdce9' stroke-width='1.3' fill='none'><path d='M133 106L204 92H247'/><path d='M130 161L205 193H248'/><path d='M128 228L54 252H12'/></g><circle class='body-marker' cx='133' cy='106' r='5'/><circle class='body-marker"""+(' warning' if 'LOW OXYGEN READING' in active else '')+"""' cx='130' cy='161' r='5'/><circle class='body-marker' cx='128' cy='228' r='5'/><g fill='#9fd6e8' font-family='sans-serif' font-size='9'><text x='204' y='84'>CARDIAC</text><text x='205' y='186'>RESPIRATORY</text><text x='12' y='245'>MOBILITY</text></g></svg>"""
    main_signal=metrics[0]
    sig_html=[]
    for key,label,unit,color,symbol,alertname in metrics:
        val=float(current[key]); bad=alertname in active
        sig_html.append(f"<div class='signal-row'><div style='flex:1;min-width:0'><div class='signal-label'>{label} <span style='color:{'#ffb381' if bad else '#6bd9b5'}'>●</span></div><div class='signal-track' style='--bar:{color};--width:{min(100,max(5,(val / {'Heart rate (bpm)':150,'SpO₂ (%)':100,'Sleep (h)':10,'Radiation index (relative)':3}[key])*100)):.0f}%'><div class='signal-fill'></div></div></div><div class='signal-value'>{val:.1f} <span style='font-size:10px;color:#92adbd'>{unit}</span></div></div>")
    warn_html=''.join(f"<div class='alert-panel warn'><div class='alert-title'>▲ {escape(name)}</div><div class='alert-copy'>{escape(action)}</div></div>" for name,action in alerts)
    if not warn_html: warn_html="<div class='alert-panel'><div class='alert-title'>● ALL CHANNELS WITHIN DEMONSTRATION LIMITS</div><div class='alert-copy'>No active flags at this sample. Switch scenarios to test anomaly response.</div></div>"
    html=f"""<div class='section-kicker'>02 &nbsp; / &nbsp; INTEGRATED PHYSIOLOGICAL SURVEILLANCE</div><div class='ops-grid'>
    <div class='instrument'><div class='micro'>SENSOR TOPOLOGY / SCHEMATIC</div><div class='instrument-title' style='margin-top:6px'>Crew physiological map</div><div class='instrument-caption'>Illustrative sensor placement · not an anatomical scan</div><div class='body-wrap'>{body_svg}</div><div class='body-key'><span>◈ <b>3</b> sensor regions</span><span>● <b>{'REVIEW' if iswarn else 'CONNECTED'}</b></span></div></div>
    <div class='instrument'><div class='micro'>MULTICHANNEL SIGNALS / HISTORY</div><div class='instrument-title' style='margin-top:6px'>Telemetry stream</div><div class='instrument-caption'>Four independent synthetic channels · samples 0–{minute}</div>
    <div style='display:grid;grid-template-columns:1fr 1fr;gap:12px'>"""
    for key,label,unit,color,symbol,alertname in metrics:
        html+=f"<div style='background:#0a1a29;border:1px solid #1e3b4d;border-radius:10px;padding:12px;min-width:0'><div style='display:flex;justify-content:space-between;gap:5px'><span class='micro' style='letter-spacing:.08em;color:{color}'>{label}</span><span style='color:#9fb6c5;font-size:10px'>{float(current[key]):.1f}</span></div>{wave_svg(key,color)}</div>"
    html+="</div><div class='panel-bottom'>◉ STREAM ACTIVE &nbsp; · &nbsp; SYNTHETIC VALUES &nbsp; · &nbsp; SELECT CHANNEL BELOW FOR FULL ANALYSIS</div></div>"
    html+=f"<div class='instrument'><div class='micro'>AUTONOMOUS TRIAGE / RULE ENGINE</div><div class='instrument-title' style='margin-top:6px'>Mission decision support</div><div class='instrument-caption'>Explainable threshold flags · human verification required</div><div class='readout'>{len(alerts):02d} <small>ACTIVE FLAGS</small></div>{''.join(sig_html)}{warn_html}<div class='panel-bottom'>DEMONSTRATION THRESHOLDS ONLY · NOT MEDICAL ADVICE</div></div></div>"
    st.markdown(html,unsafe_allow_html=True)
    st.markdown("<div class='section-kicker'>03 &nbsp; / &nbsp; CHANNEL FORENSICS &amp; EVENT HISTORY</div>",unsafe_allow_html=True)
    left,right=st.columns([1.6,1])
    with left:
        focus_map={'LOW OXYGEN READING':'SpO₂ (%)','HIGH PULSE':'Heart rate (bpm)','LOW REPORTED SLEEP':'Sleep (h)','RADIATION SENSOR FLAG':'Radiation index (relative)'}
        scenario_signature=(scenario,profile,int(seed),upload is not None)
        if st.session_state.get('_astra_focus_signature') != scenario_signature:
            st.session_state['_astra_focus_signature']=scenario_signature
            st.session_state['inspect_signal']=next((focus_map[a] for a in focus_map if a in active),'Heart rate (bpm)')
        key=st.selectbox('Inspect signal', [m[0] for m in metrics],key='inspect_signal')
        col=next(m[3] for m in metrics if m[0]==key)
        fig=go.Figure()
        fig.add_trace(go.Scatter(x=visible['Minute'],y=visible[key],mode='lines',line=dict(color=col,width=3),fill='none',name=key))
        fig.add_hline(y=float(df.iloc[:min(20,len(df))][key].mean()),line_dash='dot',line_color='#9eb5c6',annotation_text='Initial baseline')
        vals=visible[key].astype(float)
        low=float(vals.min()); high=float(vals.max()); spread=max(high-low,{'Heart rate (bpm)':8,'SpO₂ (%)':3,'Sleep (h)':1,'Radiation index (relative)':.25}[key])
        y_bounds=[max(0,low-.22*spread),high+.22*spread]
        if key=='SpO₂ (%)': y_bounds[1]=min(100,y_bounds[1])
        fig.update_layout(template='plotly_dark',height=305,margin=dict(l=15,r=20,t=12,b=15),paper_bgcolor='#0c1e2d',plot_bgcolor='#0c1e2d',font=dict(color='#a8c3d6'),xaxis=dict(title='Mission sample / supplied index',gridcolor='#203c4e'),yaxis=dict(title=key,gridcolor='#203c4e',range=y_bounds,zeroline=False),showlegend=False,hovermode='x unified')
        st.plotly_chart(fig,use_container_width=True,config={'displayModeBar':False})
    with right:
        st.markdown('#### Threshold transition log')
        events=[]; previous=set()
        for _,r in visible.iterrows():
            current_set={a[0] for a in evaluate(r)}
            for item in sorted(current_set-previous): events.append({'Sample':int(r['Minute']),'Event':item,'Type':'Entered'})
            for item in sorted(previous-current_set): events.append({'Sample':int(r['Minute']),'Event':item,'Type':'Cleared'})
            previous=current_set
        if events: st.dataframe(pd.DataFrame(events).iloc[::-1],use_container_width=True,hide_index=True)
        else: st.info('No threshold transitions recorded in this window.')
        st.caption('Signals are illustrative. Sleep represents reported duration, not a continuously sensed waveform. Radiation is a dimensionless synthetic index.')

with tab_research:
    st.markdown("<div class='section-eyebrow'>02 / NASA OSD-575 · AUTHENTIC HUMAN RESEARCH</div>",unsafe_allow_html=True)
    # Authentic human-spaceflight laboratory measurements: OSD-575.
    st.markdown("<div class='page-hero'><div class='hero-tag'>RESEARCH ARCHIVE / NASA OSD-575</div><div class='hero-title'>Human Spaceflight Research</div><div class='hero-copy'>Explore authentic Inspiration4 blood chemistry measurements across discrete study collection points. This research archive is independent of ASTRA's simulated mission telemetry.</div></div>",unsafe_allow_html=True)
    st.markdown("<div class='kpi-grid'><div class='kpi'><div class='kpi-label'>Research samples</div><div class='kpi-value'>28</div><div class='kpi-note'>Original source records</div></div><div class='kpi'><div class='kpi-label'>Coded participants</div><div class='kpi-value'>04</div><div class='kpi-note'>C001–C004</div></div><div class='kpi'><div class='kpi-label'>Collection labels</div><div class='kpi-value'>07</div><div class='kpi-note'>Discrete timepoints per participant</div></div><div class='kpi'><div class='kpi-label'>Data integrity</div><div class='kpi-value'>NASA</div><div class='kpi-note'>OSD-575 / LSDS-8</div></div></div>",unsafe_allow_html=True)
    st.markdown('''**Authentic laboratory measurements, not simulated telemetry.** This panel uses the public NASA OSD-575 / LSDS-8 transformed comprehensive metabolic panel. The 28 samples are from four coded participants, with seven collection labels each. These are discrete serum tests, **not minute-by-minute wearable readings**.''')
    @st.cache_data
    def load_cmp():
        return pd.read_csv(Path(__file__).with_name('nasa_osd575_cmp.csv'))
    from pathlib import Path
    cmp = load_cmp()
    parts = cmp['Sample Name'].str.extract(r'^(C\d+)_serum_([LR])([+-]\d+)$')
    cmp = cmp.assign(Participant=parts[0], Phase=parts[1], Offset=parts[2].astype(int))
    research_metrics = {
        'Glucose (mg/dL)': ('glucose', 'milligram_per_deciliter'),
        'Creatinine (mg/dL)': ('creatinine', 'milligram_per_deciliter'),
        'Sodium (mmol/L)': ('sodium', 'millimol_per_liter'),
        'Potassium (mmol/L)': ('potassium', 'millimol_per_liter'),
        'Albumin (g/dL)': ('albumin', 'gram_per_deciliter'),
        'Calcium (mg/dL)': ('calcium', 'milligram_per_deciliter'),
        'ALT (U/L)': ('alt', 'units_per_liter'),
        'AST (U/L)': ('ast', 'units_per_liter'),
        'Urea nitrogen / BUN (mg/dL)': ('urea_nitrogen_bun', 'milligram_per_deciliter'),
    }
    rc1, rc2 = st.columns(2)
    with rc1:
        selected_cmp = st.selectbox('Research biomarker', list(research_metrics), key='cmp_metric')
    with rc2:
        participants = st.multiselect('Coded participants', sorted(cmp['Participant'].unique()), default=sorted(cmp['Participant'].unique()), key='cmp_subjects')
    base_name, units = research_metrics[selected_cmp]
    value_col=f'{base_name}_value_{units}'
    min_col=f'{base_name}_range_min_{units}'
    max_col=f'{base_name}_range_max_{units}'
    subset=cmp[cmp['Participant'].isin(participants)].copy()
    subset['Collection label']=subset['Phase']+subset['Offset'].map(lambda n:f'{n:+d}')
    order=['L-92','L-44','L-3','R+1','R+45','R+82','R+194']
    subset['Collection label']=pd.Categorical(subset['Collection label'], categories=order, ordered=True)
    subset=subset.sort_values(['Participant','Collection label'])
    if subset.empty:
        st.info('Select at least one participant to see the NASA measurements.')
    else:
        chart=go.Figure()
        for participant,group in subset.groupby('Participant'):
            chart.add_trace(go.Scatter(x=group['Collection label'].astype(str), y=group[value_col], mode='lines+markers', name=participant, hovertemplate='Collection %{x}<extra>'+participant+'</extra><br>Value %{y}'))
        chart.update_layout(template='plotly_dark',height=430,legend=dict(orientation='h',y=1.12,x=0),hovermode='x unified', xaxis_title='Study collection label (not mission minutes)', yaxis_title=selected_cmp, paper_bgcolor='#0c1d2e',plot_bgcolor='#0c1d2e',margin=dict(l=20,r=20,t=25,b=30))
        st.plotly_chart(chart,use_container_width=True)
        st.caption('Each line represents a coded study participant. L and R labels are retained from the source; consult study metadata for their precise collection definitions. Lines connect discrete samples for readability and do not imply continuous monitoring.')
        show=subset[['Participant','Sample Name',value_col,min_col,max_col]].copy()
        show.columns=['Participant','Sample identifier','Measured value','Reference minimum','Reference maximum']
        show['Outside supplied reference range']=(show['Measured value']<show['Reference minimum']) | (show['Measured value']>show['Reference maximum'])
        st.markdown('#### Measurement register / source reference intervals')
        st.dataframe(show,use_container_width=True,hide_index=True)
        st.download_button('Download selected research measurements',show.to_csv(index=False).encode(),file_name='astra_osd575_selected.csv',mime='text/csv')
        st.caption('Reference intervals are reproduced from the source CSV and may differ by sample. An out-of-range laboratory value is **not** a medical diagnosis or proof of a spaceflight effect.')
    st.markdown('**Provenance:** [NASA OSD-575 study files](https://osdr.nasa.gov/osdr/data/osd/files/575) · Source file: `LSDS-8_Comprehensive_Metabolic_Panel_CMP_TRANSFORMED.csv` · Local bundled copy: `nasa_osd575_cmp.csv`. No health thresholds in the synthetic crew simulator were trained or calibrated on these measurements.')


with tab_weather:
    st.markdown("<div class='section-eyebrow'>03 / EXTERNAL SPACE WEATHER INTELLIGENCE</div>",unsafe_allow_html=True)
    # NASA DONKI integration: actual event records are fetched on demand, never simulated.
    @st.cache_data(ttl=1800, show_spinner=False)
    def cached_nasa_sep(start_iso: str, end_iso: str):
        return fetch_sep_events(date.fromisoformat(start_iso), date.fromisoformat(end_iso))

    st.markdown("<div class='page-hero'><div class='hero-tag'>EXTERNAL INTELLIGENCE / NASA DONKI</div><div class='hero-title'>Space Weather Watch</div><div class='hero-copy'>Investigate NASA-recorded solar energetic particle events. Event metadata supports operational awareness; it does not establish astronaut radiation dose or clinical risk.</div></div>",unsafe_allow_html=True)
    st.markdown("<div class='kpi-grid'><div class='kpi'><div class='kpi-label'>Intelligence source</div><div class='kpi-value'>DONKI</div><div class='kpi-note'>NASA CCMC records</div></div><div class='kpi'><div class='kpi-label'>Event class</div><div class='kpi-value'>SEP</div><div class='kpi-note'>Solar energetic particles</div></div><div class='kpi'><div class='kpi-label'>Acquisition</div><div class='kpi-value'>ON DEMAND</div><div class='kpi-note'>Internet connection required</div></div><div class='kpi'><div class='kpi-label'>Crew exposure</div><div class='kpi-value'>N/A</div><div class='kpi-note'>Not measured by this feed</div></div></div>",unsafe_allow_html=True)
    st.markdown('''**Real NASA event records, separate from synthetic crew telemetry.** NASA's DONKI database reports solar energetic particle (SEP) events. Such events are relevant to space radiation operations, but a DONKI event record **does not measure astronaut radiation dose, predict exposure at the spacecraft, or establish a medical emergency**.''')
    st.caption('Source: NASA Community Coordinated Modeling Center (CCMC), DONKI SEP API. This panel retrieves event metadata over the internet; it does not manufacture NASA records.')
    with st.container(border=True):
        dc1, dc2, dc3 = st.columns([1,1,1])
        with dc1:
            nasa_start = st.date_input('Start date (UTC)', value=date(2024,5,1), max_value=date.today(), key='nasa_start')
        with dc2:
            nasa_end = st.date_input('End date (UTC)', value=date(2024,5,20), max_value=date.today(), key='nasa_end')
        with dc3:
            st.write('')
            st.write('')
            fetch_clicked = st.button('Fetch NASA events', type='primary', use_container_width=True)
        if fetch_clicked:
            try:
                with st.spinner('Contacting NASA DONKI…'):
                    st.session_state['nasa_sep_result'] = cached_nasa_sep(nasa_start.isoformat(), nasa_end.isoformat())
                    st.session_state.pop('nasa_sep_error', None)
            except Exception as exc:
                st.session_state['nasa_sep_result'] = None
                st.session_state['nasa_sep_error'] = str(exc)
        if st.session_state.get('nasa_sep_error'):
            st.error('NASA API could not be reached. Your local ASTRA scenarios still work. ' + st.session_state['nasa_sep_error'])
            st.caption('Check your connection and retry. Alternatively, inspect the official NASA DONKI web app linked below. No fake events are shown as a fallback.')
        nasa_result = st.session_state.get('nasa_sep_result')
        if nasa_result is not None:
            event_rows = nasa_result['events']
            st.markdown(f"<div class='notice-strip'><b>NASA DATA RECEIVED</b> &nbsp; · &nbsp; {len(event_rows)} recorded SEP events &nbsp; · &nbsp; {nasa_result['start']} → {nasa_result['end']}</div>",unsafe_allow_html=True)
            st.caption(f"Fetched {nasa_result['retrieved_utc']} · Source: {nasa_result['source']}")
            if event_rows:
                nasa_df = pd.DataFrame(event_rows)
                event_times=pd.to_datetime(nasa_df['Event time (UTC)'],errors='coerce',utc=True)
                if event_times.notna().any():
                    timeline=go.Figure(go.Scatter(x=event_times,y=[1]*len(event_times),mode='markers',marker=dict(size=15,color='#6de9f3',line=dict(width=2,color='#153b4f')),text=nasa_df['Event ID'],hovertemplate='%{x}<br>Event %{text}<extra></extra>'))
                    timeline.update_layout(template='plotly_dark',height=190,paper_bgcolor='#0c1e2d',plot_bgcolor='#0c1e2d',margin=dict(l=15,r=15,t=15,b=20),xaxis=dict(title='Recorded event time (UTC)',gridcolor='#203c4e'),yaxis=dict(visible=False,range=[0.6,1.4]),showlegend=False)
                    st.plotly_chart(timeline,use_container_width=True)
                st.markdown('#### NASA event register')
                st.dataframe(nasa_df, hide_index=True, use_container_width=True)
                st.download_button('Download NASA event metadata (CSV)', nasa_df.to_csv(index=False).encode('utf-8'), 'nasa_donki_sep_events.csv', 'text/csv')
                st.download_button('Download original NASA API response (JSON)', json.dumps(nasa_result['raw'], indent=2).encode('utf-8'), 'nasa_donki_sep_raw.json', 'application/json')
                chosen = st.selectbox('Inspect an observed event', range(len(event_rows)), format_func=lambda i: f"{event_rows[i]['Event time (UTC)']} · {event_rows[i]['Event ID']}")
                event = event_rows[chosen]
                st.info(f"**Mission review prompt:** NASA recorded an SEP event at {event['Event time (UTC)']}. A crew-support system should check mission-specific space-weather guidance, spacecraft shielding, and calibrated radiation instruments. This record alone cannot determine crew exposure or whether sheltering is required.")
            else:
                st.info('No SEP event records were returned for the selected period. This does not guarantee the environment was radiation-free.')
        else:
            st.markdown("<div class='notice-strip'><b>AWAITING DATA REQUEST</b> &nbsp; · &nbsp; Choose a historical date range and fetch authentic NASA SEP event records. Suggested range: May 1–20, 2024. No fabricated event data will be displayed.</div>",unsafe_allow_html=True)
        st.markdown('[NASA DONKI information](https://ccmc.gsfc.nasa.gov/tools/DONKI/) · [NASA DONKI interactive database](https://ccmc.gsfc.nasa.gov/DONKI/) · [NASA API portal](https://api.nasa.gov/)')
    st.markdown('**Documented historical example (available offline):** NASA CCMC reported a solar energetic particle event observed by **STEREO A on May 11, 2024, beginning at 04:07 UTC**. [NASA May 2024 storm case study](https://ccmc.gsfc.nasa.gov/storms/may2024/) · [Original event notification (legacy URL)](https://kauai.ccmc.gsfc.nasa.gov/DONKI/view/Alert/30728/1). This is a sourced historical case, **not a live API result or a measurement of astronaut dose**.')
    st.caption('**Provenance:** DONKI event timestamps and instruments are NASA-hosted records retrieved on demand. Heart rate, oxygen, sleep, and radiation index in the mission simulator remain synthetic. The two timelines are not synchronized.')


with tab_method:
    st.markdown("<div class='section-eyebrow'>04 / TRANSPARENCY &amp; SCIENTIFIC TRACEABILITY</div>",unsafe_allow_html=True)
    st.markdown("<div class='page-hero'><div class='hero-tag'>SYSTEM ASSURANCE / TRANSPARENCY</div><div class='hero-title'>Data, Methods &amp; Scientific Integrity</div><div class='hero-copy'>Trace every displayed channel to its origin, distinguish simulation from research, and review the limits of this educational prototype.</div></div>",unsafe_allow_html=True)
    st.markdown("<div class='kpi-grid'><div class='kpi'><div class='kpi-label'>Crew monitoring</div><div class='kpi-value'>SIM</div><div class='kpi-note'>Reproducible scenario engine</div></div><div class='kpi'><div class='kpi-label'>Human research</div><div class='kpi-value'>REAL</div><div class='kpi-note'>NASA OSD-575 source CSV</div></div><div class='kpi'><div class='kpi-label'>Space weather</div><div class='kpi-value'>API</div><div class='kpi-note'>NASA DONKI on demand</div></div><div class='kpi'><div class='kpi-label'>Medical validation</div><div class='kpi-value'>NONE</div><div class='kpi-note'>Educational prototype only</div></div></div>",unsafe_allow_html=True)
    with st.expander('Telemetry data & CSV export'):
        st.dataframe(visible.iloc[::-1],use_container_width=True,hide_index=True)
        st.download_button('Download displayed telemetry',df.to_csv(index=False).encode(),'astra_telemetry.csv','text/csv')
    with st.expander('Scientific integrity, methodology & limitations'):
        st.markdown('''**Data:** Built-in readings are locally generated, reproducible synthetic examples, not NASA astronaut telemetry. Optional CSV imports are user-supplied and are not authenticated or verified as NASA data.\n\n**Method:** Four independent, illustrative rules check heart rate >120 bpm, SpO₂ <94%, sleep <5 hours, and a **dimensionless** radiation sensor index >2. These values are demonstration choices, **not astronaut clinical thresholds**. The radiation index is not a dose and must not be interpreted as mSv or exposure risk. The first up to 20 samples provide a visual baseline, not a validated personal reference range.\n\n**Multi-system emergency drill:** The combined scenario independently scripts changes in all four channels. It demonstrates alert handling, not a plausible physiological causal model. **Survival percentages cannot be calculated** from these synthetic signals. Response playbooks are operational prompts for qualified human review, not treatment instructions.

**Limitations:** No medical diagnosis, actual sensors, machine learning, radiation dosimetry, validated astronaut models, or automated treatment. Real deployment requires qualified medical oversight, validated thresholds, calibrated hardware, fault handling, privacy/security controls, and mission-specific procedures.\n\n**Background reading:** [NASA Human Research Program](https://www.nasa.gov/hrp/) · [NASA Human Research Roadmap](https://humanresearchroadmap.nasa.gov/) · [NASA Space Apps](https://www.spaceappschallenge.org/). These are background references, not endorsements or sources for the demonstration thresholds.''')
    st.subheader('Scientific evidence & traceability')
    st.markdown('''ASTRA is **research-informed, not research-calibrated**. The NASA sources below motivate *what to monitor*; they do **not** validate the numeric alert cutoffs or make synthetic telemetry representative of astronauts.''')
    evidence=pd.DataFrame([
     {'Channel':'Heart rate','Research motivation':'Cardiovascular changes and exercise during spaceflight','What ASTRA uses':'Synthetic bpm + illustrative >120 bpm alert','Evidence status':'NASA background only; cutoff not validated'},
     {'Channel':'Oxygen saturation','Research motivation':'Physiological monitoring and oxygen-related operational concerns','What ASTRA uses':'Synthetic SpO₂ + illustrative <94% alert','Evidence status':'NASA background only; cutoff not validated'},
     {'Channel':'Sleep','Research motivation':'Sleep loss and fatigue during missions','What ASTRA uses':'Synthetic sleep hours + illustrative <5 h alert','Evidence status':'NASA background only; cutoff not validated'},
     {'Channel':'Radiation','Research motivation':'Space radiation health risks','What ASTRA uses':'Synthetic unitless sensor index + illustrative >2 alert','Evidence status':'Not a radiation dose; cannot estimate exposure'}
    ])
    st.dataframe(evidence,hide_index=True,use_container_width=True)
    st.markdown('''**NASA source starting points**

    - [NASA Human Research Roadmap](https://humanresearchroadmap.nasa.gov/) — risk and evidence documentation for human spaceflight.
    - [NASA Open Science Data Repository](https://osdr.nasa.gov/) — space biology datasets and associated study metadata. **OSD-575 CMP measurements are bundled in the research panel.**
    - [NASA Human Research Program](https://www.nasa.gov/hrp/) — context for astronaut health research.

    **Data provenance:** Built-in simulations are generated by the app's `generate()` function. The optional CSV importer expects the application's own schema; NASA OSDR files generally require dataset-specific preprocessing and cannot be assumed compatible. Do not label imported data as NASA-sourced without identifying the dataset, variables, units, and transformations.

    **NASA space-weather integration:** The NASA Data / Space Weather Watch panel retrieves Solar Energetic Particle event records from NASA DONKI. Those are real space-weather event metadata, **not physiological measurements or radiation dose**. No DONKI events are used to calibrate the synthetic health thresholds. OSD-575 serum chemistry is displayed in its own panel, separate from synthetic vital signs.''')
    st.caption('ASTRA v8 · NASA DONKI space-weather event integration + synthetic crew telemetry · Independent student project · Not affiliated with or endorsed by NASA')


with tab_checkin:
    from checkin import render as render_checkin
    render_checkin(profile)

with tab_copilot:
    from copilot import render as render_copilot
    render_copilot(profile,scenario,current,alerts,source_label)

# Shared floating quick assistant, visible regardless of selected tab.
# CSS only positions the launcher; Streamlit handles the popover and chat form.
st.markdown("""<style>
.st-key-astra_corner_launcher {
    position: fixed; bottom: 22px; right: 24px; z-index: 9999;
    width: auto; padding: 0; background: transparent;
}
.st-key-astra_corner_launcher button {
    background: #103449 !important; border: 1px solid #5fdce9 !important;
    color: #eaffff !important; border-radius: 30px !important;
    box-shadow: 0 5px 28px rgba(0,0,0,.55);
    font-weight: 700;
}
@media (max-width: 650px) {
    .st-key-astra_corner_launcher {right: 10px;bottom: 10px;}
}
</style>""",unsafe_allow_html=True)
from copilot import render_corner
render_corner(profile,scenario,current,alerts,source_label)
