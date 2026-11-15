"""Manual wellness check-ins. All user-provided measurements are unverified."""
from datetime import datetime, timezone
import pandas as pd
import streamlit as st

def render(profile):
    st.markdown('### ◈ CREW WELLNESS / DAILY CHECK-IN')
    st.caption('Manual inputs supplement the simulation; they do not overwrite the synthetic telemetry.')
    with st.form('astra_wellness_form'):
        a,b,c=st.columns(3)
        sleep=a.number_input('Sleep last night (hours)',0.0,24.0,7.0,0.5)
        mood=b.select_slider('Mood',options=['Very low','Low','Neutral','Good','Excellent'],value='Neutral')
        fatigue=c.slider('Fatigue (0–10)',0,10,3)
        d,e,f=st.columns(3)
        temp=d.number_input('Temperature (°C; optional, 0 = not measured)',0.0,45.0,0.0,0.1)
        systolic=e.number_input('Systolic BP (mmHg; 0 = not measured)',0,260,0)
        diastolic=f.number_input('Diastolic BP (mmHg; 0 = not measured)',0,180,0)
        glucose=st.number_input('Blood glucose (mmol/L; 0 = not measured)',0.0,40.0,0.0,0.1)
        symptoms=st.multiselect('Symptoms',['None','Breathing difficulty','Dizziness','Palpitations','Headache','Nausea','Pain','Other'])
        note=st.text_area('Crew notes (optional)',max_chars=500)
        save=st.form_submit_button('Save check-in',use_container_width=True)
    if save:
        record={'timestamp_utc':datetime.now(timezone.utc).isoformat(timespec='seconds'),'crew':profile,'sleep_h':sleep,'mood':mood,'fatigue_0_10':fatigue,'temp_c':temp or None,'systolic_mmhg':systolic or None,'diastolic_mmhg':diastolic or None,'glucose_mmol_l':glucose or None,'symptoms':', '.join(symptoms),'notes':note}
        st.session_state.setdefault('astra_checkins',[]).append(record)
        st.success('Check-in recorded locally in this browser session.')
    rows=[r for r in st.session_state.get('astra_checkins',[]) if r['crew']==profile]
    if rows:
        st.dataframe(pd.DataFrame(rows),use_container_width=True,hide_index=True)
        st.download_button('Export wellness records (CSV)',pd.DataFrame(rows).to_csv(index=False),file_name='astra_wellness.csv',mime='text/csv')
        if any('Breathing difficulty' in r['symptoms'] for r in rows[-1:]):
            st.warning('Breathing difficulty was reported. The emergency assistant should assess symptoms independently of sensor readings.')
    else: st.caption('No manual check-ins recorded for this crew member.')
