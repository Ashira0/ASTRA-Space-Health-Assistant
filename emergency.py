"""ASTRA fictional mission protocol: deterministic, inspectable simulation logic.

All actions are simulated. Never controls hardware or administers treatment.
"""
import streamlit as st

PROTOCOL_VERSION = 'ARES-01 / SIM-MED-001 v1.0 (fictional, team-authored)'


def context_key(profile, scenario, current):
    return (profile, scenario, round(float(current['SpO₂ (%)']), 1), round(float(current['Heart rate (bpm)']), 1))


def plan(current, symptoms, signal, atmosphere, oxygen_available):
    spo2 = float(current['SpO₂ (%)'])
    hr = float(current['Heart rate (bpm)'])
    concerning = spo2 < 94 or hr > 120 or symptoms in ('Breathing difficulty', 'Unresponsive / abnormal breathing')
    if not concerning:
        return ('MONITOR', [
            'Record current measurements and reported symptoms.',
            'Continue scheduled health checks; reassess if symptoms appear or readings change.'
        ])
    steps = [
        'Alert the designated crew medical responder and initiate the simulated emergency log.',
        'Check responsiveness and breathing. If unresponsive or breathing abnormally, initiate the simulated crew emergency response immediately.',
        'Check the sensor signal and repeat SpO₂/heart-rate readings if feasible; do not delay the emergency response.',
    ]
    if atmosphere == 'Cabin alarm / abnormal pressure or oxygen':
        steps.append('Treat the cabin alert as a concurrent spacecraft emergency: notify flight operations and follow the simulated cabin-atmosphere response branch.')
    elif atmosphere == 'Not checked / unknown':
        steps.append('Inspect available cabin oxygen, pressure, and atmosphere alarms; report any abnormal result.')
    else:
        steps.append('Record that cabin indicators are reported nominal; continue evaluating the crew member.')
    if symptoms == 'Unresponsive / abnormal breathing':
        steps.append('Prioritize the simulated unresponsive-crew emergency workflow; do not wait for additional telemetry.')
    elif spo2 < 90 and signal == 'Confirmed with repeat reading':
        if oxygen_available == 'Yes — simulated crew oxygen kit':
            steps.append('SIMULATED INTERVENTION: The fictional ARES-01 protocol selects supplemental oxygen support. In the demo, mark the crew oxygen kit as prepared and oxygen support as simulated; no device is controlled and no real administration instructions are provided.')
        else:
            steps.append('SIMULATED INTERVENTION: Oxygen support is indicated by this fictional branch, but equipment availability is unconfirmed or absent. Flag the resource constraint and request medical responder assistance.')
    elif spo2 < 90:
        steps.append('Prepare for the simulated oxygen-support decision; confirm the reading and check available equipment while the responder assesses the crew member.')
    else:
        steps.append('Continue the simulated assessment; current inputs do not select the oxygen-support branch.')
    steps.append('Recheck vital signs, symptoms and cabin indicators; document changes and escalate if the condition worsens.')
    return ('CRITICAL SIMULATION' if spo2 < 90 or symptoms == 'Unresponsive / abnormal breathing' else 'REVIEW REQUIRED', steps)


def render(profile, scenario, current, compact=False):
    st.markdown('**◈ GUIDED EMERGENCY RESPONSE / SIMULATION**')
    st.caption(PROTOCOL_VERSION + ' · Demo logic, not a validated treatment protocol')
    key = context_key(profile, scenario, current)
    prefix = 'mini' if compact else 'full'
    with st.container(border=True):
        st.write(f"**{profile}** · SpO₂ **{float(current['SpO₂ (%)']):.1f}%** · HR **{float(current['Heart rate (bpm)']):.1f} bpm**")
        symptoms = st.selectbox('Crew symptoms', ['Unknown / not assessed', 'No symptoms reported', 'Breathing difficulty', 'Dizziness / palpitations', 'Unresponsive / abnormal breathing'], key=f'{prefix}_symptoms')
        signal = st.selectbox('Measurement verification', ['Not yet verified', 'Confirmed with repeat reading', 'Poor / unreliable signal'], key=f'{prefix}_signal')
        atmosphere = st.selectbox('Cabin environment', ['Not checked / unknown', 'Cabin indicators nominal', 'Cabin alarm / abnormal pressure or oxygen'], key=f'{prefix}_cabin')
        oxygen_available = st.selectbox('Simulation equipment', ['Unknown', 'Yes — simulated crew oxygen kit', 'No'], key=f'{prefix}_oxygen')
        # Shared chat-derived context informs the visible workflow. Explicit widget
        # selections take precedence once changed by the astronaut.
        facts = st.session_state.get('emergency_facts', {})
        symptoms = symptoms if symptoms != 'Unknown / not assessed' else facts.get('symptoms', symptoms)
        signal = signal if signal != 'Not yet verified' else facts.get('signal', signal)
        atmosphere = atmosphere if atmosphere != 'Not checked / unknown' else facts.get('atmosphere', atmosphere)
        oxygen_available = oxygen_available if oxygen_available != 'Unknown' else facts.get('oxygen_available', oxygen_available)
        severity, steps = plan(current, symptoms, signal, atmosphere, oxygen_available)
        st.markdown(f'**Decision: {severity}**')
        st.caption('Branch selection is deterministic. The chatbot does not choose or modify interventions.')
        index_key = f'{prefix}_response_step'
        context_state_key = f'{prefix}_response_context'
        if st.session_state.get(context_state_key) != key:
            st.session_state[context_state_key] = key
            st.session_state[index_key] = 0
        index = min(st.session_state.get(index_key, 0), len(steps)-1)
        st.progress((index + 1) / len(steps))
        st.info(f'**STEP {index+1} / {len(steps)}**\n\n{steps[index]}')
        a, b = st.columns(2)
        if a.button('← Previous', disabled=index == 0, key=f'{prefix}_prev'):
            st.session_state[index_key] = index-1
            st.rerun()
        if b.button('Confirm / Next →', disabled=index == len(steps)-1, key=f'{prefix}_next'):
            st.session_state[index_key] = index+1
            log = st.session_state.setdefault('emergency_log', [])
            log.append({'crew':profile,'scenario':scenario,'step':index+1,'instruction':steps[index],'result':'confirmed in demo'})
            st.rerun()
        if index == len(steps)-1:
            st.success('End of simulated workflow. Reassess if measurements or symptoms change.')
        with st.expander('Why was this action selected?'):
            st.write('Fictional ARES-01 decision policy: concerning measurements or symptoms trigger assessment. A confirmed SpO₂ below 90% with a simulated oxygen kit available selects a **simulated oxygen-support intervention**. These cutoffs and actions are team-authored demo rules, not NASA medical thresholds or instructions.')
            st.write('Evidence context: NASA-STD-3001 provides crew-health requirements; NASA HRP describes spaceflight hazards. Neither source is represented as endorsing this fictional protocol.')
        if not compact:
            with st.expander('Simulated action log'):
                st.dataframe(st.session_state.get('emergency_log', []), use_container_width=True)
