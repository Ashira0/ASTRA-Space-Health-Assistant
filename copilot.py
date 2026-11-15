"""ASTRA conversational workflow UI. Decisions always originate in response_engine."""
import json
import requests
import streamlit as st
from response_engine import ResponseState, VERSION, parse_facts, parse_measurements, state_current, incident_report, update, next_step, summary, answer_option, log_event

SOURCES = [
 ('NASA HRP — Five Hazards','https://www.nasa.gov/hrp/hazards/','Five hazards: space radiation, isolation and confinement, distance from Earth, gravity fields, hostile or closed environments.'),
 ('NASA HRP — Human Spaceflight Risks','https://www.nasa.gov/hrp/risks/','NASA studies risks affecting cardiovascular, bone, muscle, immune, sleep, and behavioral health.'),
 ('NASA HRP — Ongoing Research','https://www.nasa.gov/hrp/ongoing-hrp-research/','Research examines spaceflight health and performance risks; research is not a mission-specific treatment procedure.'),
 ('NASA-STD-3001 Volume 1','https://www.nasa.gov/reference/nasa-std-3001v1/','Crew health standards and requirements, not a source of the fictional ARES-01 steps.'),
 ('CSA Radiation Monitoring','https://www.asc-csa.gc.ca/eng/news/articles/2026/2026-02-26-monitoring-radiation-astronaut-health.asp','Dedicated radiation instruments are needed to estimate exposure; synthetic relative index is not a dose.'),
 ('NASA OSD-575','https://osdr.nasa.gov/osdr/data/osd/files/575','Historical Inspiration4 laboratory chemistry; not live crew vital signs.'),
 ('NASA DONKI','https://ccmc.gsfc.nasa.gov/tools/DONKI/','Space weather event metadata are not individual radiation exposure readings.'),
]

def ensure_state(profile,scenario,current):
    signature=f'{profile}|{scenario}'
    state=st.session_state.get('astra_response_state')
    if state is None or state.signature!=signature:
        state=ResponseState(profile,scenario,signature)
        st.session_state.astra_response_state=state
    return state

def explain(question,state,current):
    """Optional model explanation; never changes steps, facts, or actions."""
    branch,sev,step,_=next_step(state,current)
    payload={'crew':state.crew,'scenario':state.scenario,'heart_rate_bpm':round(float(current['Heart rate (bpm)']),1),'spo2_percent':round(float(current['SpO₂ (%)']),1),'sleep_hours':round(float(current['Sleep (h)']),1),'relative_radiation_index':round(float(current['Radiation index (relative)']),2),'facts':state.facts,'workflow_branch':branch,'current_step':step,'question':question,'sources':[{'id':i+1,'title':s[0],'summary':s[2]} for i,s in enumerate(SOURCES)]}
    system=('You explain a fictional astronaut health training workflow. NEVER choose, skip, alter, or invent actions. '
            'Use the current_step supplied by the deterministic engine as the only next action. '
            'Do not claim NASA endorses this workflow, do not provide drug doses, oxygen settings, or medical equipment operation. '
            'SpO2 below 90 in this scenario is concerning; never call it normal. '
            'Be concise (under 120 words); answer why the step matters or clarify the measurement. '
            'Only cite a source for the research fact it supports; the ARES-01 steps are team-authored.')
    try:
        r=requests.post('http://127.0.0.1:11434/api/chat',json={'model':'qwen3:1.7b','stream':False,'think':False,'messages':[{'role':'system','content':system},{'role':'user','content':json.dumps(payload,ensure_ascii=False)}],'options':{'temperature':0.1,'num_predict':230,'num_ctx':3072}},timeout=35)
        r.raise_for_status()
        return r.json()['message']['content'].strip()
    except (requests.RequestException,KeyError,ValueError):
        return None

def submit(question,profile,scenario,current,alerts=None,source_type=None):
    state=ensure_state(profile,scenario,current)
    question=question.strip()[:1200]
    if not question: return
    state.chat.append({'role':'user','content':question})
    q=question.lower()
    if any(term in q for term in ('summarize','summary','every action','incident report','what happened')):
        answer=incident_report(state,current)
    else:
        measurements=parse_measurements(question)
        if measurements:
            state.reported.update(measurements)
            log_event(state,'reported_measurement',str(measurements))
        facts=parse_facts(question)
        if facts: update(state,facts)
        if any(term in q for term in ('oxygen saturation','oxygen reading','spo2','spo₂','low oxygen')):
            state.focus='oxygen'
        # Don't assume a step was completed simply from an ambiguous chat statement.
        if any(term in q for term in ('completed that step','done that step','finished that step')):
            answer=('Please confirm the specific step using the workflow confirmation control so the incident log remains accurate.\n\n'+summary(state,state_current(state,current)))
        else:
            answer=summary(state,state_current(state,current))
            if any(w in q for w in ('why','explain','mean','cause','research','source')):
                extra=explain(question,state,state_current(state,current))
                if extra: answer+='\n\n**Additional research explanation (local AI; may be inaccurate):**\n\n'+extra
    state.chat.append({'role':'assistant','content':answer})
    state.chat=state.chat[-36:]

def conversation(state):
    for item in state.chat:
        with st.chat_message(item['role']): st.markdown(item['content'])

def workflow_panel(state,current,prefix):
    branch,severity,step,steps=next_step(state,current)
    with st.container(border=True):
        st.markdown(f'**ARES-01 · {branch} · {severity.upper()}**')
        if any(x['id']=='oxygen_support' for x in steps):
            st.success('DECISION: Fictional oxygen-support intervention branch selected. Follow the step confirmations below; no real equipment is operated.')
        st.caption(f'{len(state.completed)} step confirmations · {VERSION}')
        if step is None:
            st.success('All currently applicable steps confirmed. Continue monitoring.')
        else:
            st.progress(min(len(state.completed)/max(len(steps),1),1.0))
            st.markdown(f'#### {step["title"]}')
            st.write(step['instruction'])
            st.caption('Reason: '+step['reason'])
            if step['question']:
                choice=st.radio(step['question'],step['options'],index=None,key=f'{prefix}_{step["id"]}_choice')
                if st.button('Save answer and advance',key=f'{prefix}_{step["id"]}_answer',disabled=choice is None,use_container_width=True):
                    key,value=answer_option(step['id'],choice)
                    if value: update(state,{key:value})
                    state.completed.append(step['id']);log_event(state,'step_confirmed',step['title']+' | '+str(choice))
                    state.chat.append({'role':'assistant','content':summary(state,current)})
                    st.rerun()
            else:
                if st.button('Confirm step complete →',key=f'{prefix}_{step["id"]}_done',use_container_width=True):
                    state.completed.append(step['id']);log_event(state,'step_confirmed',step['title'])
                    state.chat.append({'role':'assistant','content':summary(state,current)})
                    st.rerun()
        with st.expander('Workflow facts and decision trace'):
            st.json(state.facts)
            st.write('**Completed:** '+(', '.join(state.completed) if state.completed else 'None'))
            st.caption('All decisions are deterministic. The model cannot create or authorize interventions.')

def render(profile,scenario,current,alerts,source_type):
    state=ensure_state(profile,scenario,current)
    st.markdown('### ◈ ASTRA COPILOT / GUIDED EMERGENCY RESPONSE')
    st.caption('PERSISTENT DECISION TREE · LOCAL AI EXPLANATIONS · OFFLINE WORKFLOW')
    st.info('Fictional training scenario. ASTRA selects simulated actions using authored rules; it is not a validated medical device.')
    a,b,c=st.columns(3)
    a.metric('SpO₂',f'{float(current["SpO₂ (%)"]):.1f}%')
    b.metric('Heart rate',f'{float(current["Heart rate (bpm)"]):.1f} bpm')
    c.metric('Workflow',next_step(state,current)[0])
    workflow_panel(state,current,'full')
    st.markdown('#### Conversation')
    conversation(state)
    question=st.chat_input('Report a measurement, symptom, or ask what to do next…',key='astra_full_chat')
    if question:
        submit(question,profile,scenario,current,alerts,source_type);st.rerun()
    left,right=st.columns(2)
    if left.button('Reset current emergency',key='astra_reset'):
        st.session_state.pop('astra_response_state',None);st.rerun()
    right.download_button('Export incident log (JSON)',data=json.dumps({'version':VERSION,'crew':state.crew,'scenario':state.scenario,'facts':state.facts,'reported_measurements':state.reported,'focus':state.focus,'events':state.events,'chat':state.chat},indent=2),file_name='astra_incident_log.json',mime='application/json',use_container_width=True)
    with st.expander('Research references and data provenance'):
        for i,(title,url,description) in enumerate(SOURCES,1):
            st.markdown(f'**[{i}] [{title}]({url})** — {description}')
        st.caption('References are curated background summaries, not extracted treatment manuals. Synthetic telemetry, historical OSD-575 lab data, and NASA DONKI events are separate datasets.')

def render_corner(profile,scenario,current,alerts,source_type):
    state=ensure_state(profile,scenario,current)
    with st.container(key='astra_corner_launcher'):
        with st.popover('✦ ASTRA COPILOT · Ask'):
            st.markdown('**ASTRA / QUICK RESPONSE**')
            st.caption(f'{profile} · {next_step(state,current)[0]}')
            with st.expander('Current emergency step',expanded=True):
                workflow_panel(state,current,'mini')
            with st.container(height=240): conversation(state)
            with st.form('astra_corner_form',clear_on_submit=True):
                question=st.text_input('Message',placeholder='What do I do next?',label_visibility='collapsed')
                send=st.form_submit_button('Send',use_container_width=True)
            if send and question.strip():
                submit(question,profile,scenario,current,alerts,source_type);st.rerun()
            st.caption('Open the ASTRA COPILOT tab for full conversation and export.')
